/* SPDX-License-Identifier: AGPL-3.0-only */
#include <errno.h>
#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/watchdog.h>
#include <zephyr/bluetooth/bluetooth.h>
#include <zephyr/sys/atomic.h>
#include "conflict_monitor.h"

/* No pump protocol, scan, connection request, network destination or credentials.
 * The bench result is local only; this image never commands delivery. */
static const struct gpio_dt_spec carbs = GPIO_DT_SPEC_GET(DT_ALIAS(sw0), gpios);
static const struct gpio_dt_spec concert = GPIO_DT_SPEC_GET(DT_ALIAS(sw1), gpios);
static const struct device *const watchdog = DEVICE_DT_GET(DT_ALIAS(watchdog0));
static struct gpio_callback carb_callback, concert_callback;
static atomic_t pending;
static struct mmu_ledger ledger;
static struct mmu_result last_result;

static void button_event(const struct device *port, struct gpio_callback *cb, uint32_t pins)
{
    ARG_UNUSED(port);
    ARG_UNUSED(pins);
    /* ISR only latches a bounded event. Main owns all evaluator state. */
    atomic_or(&pending, cb == &carb_callback ? 1 : 2);
}

static int configure_button(const struct gpio_dt_spec *button, struct gpio_callback *cb)
{
    int err;
    if (!gpio_is_ready_dt(button)) { return -ENODEV; }
    err = gpio_pin_configure_dt(button, GPIO_INPUT);
    if (err != 0) { return err; }
    gpio_init_callback(cb, button_event, BIT(button->pin));
    err = gpio_add_callback(button->port, cb);
    if (err != 0) { return err; }
    return gpio_pin_interrupt_configure_dt(button, GPIO_INT_EDGE_TO_ACTIVE);
}

int main(void)
{
    struct wdt_timeout_cfg timeout = {
        .window = {.min = 0, .max = 10000},
        .callback = NULL,
        .flags = WDT_FLAG_RESET_SOC
    };
    struct mmu_state state = mmu_init((uint64_t)k_uptime_get());
    uint64_t last_carb = 0, last_concert = 0;
    bool seen_carb = false, seen_concert = false;
    int channel, err;
    if (!device_is_ready(watchdog)) { return -ENODEV; }
    channel = wdt_install_timeout(watchdog, &timeout);
    if (channel < 0) { return channel; }
    err = wdt_setup(watchdog, 0); /* watchdog continues during sleep/debug halt */
    if (err != 0) { return err; }
    err = configure_button(&carbs, &carb_callback);
    if (err != 0) { return err; } /* no further feed: reset after setup failure */
    err = configure_button(&concert, &concert_callback);
    if (err != 0) { return err; }
    /* Host/HCI initialization only; the cpunet image owns the controller. */
    err = bt_enable(NULL);
    if (err != 0) { return err; }

    for (;;) {
        uint64_t now = (uint64_t)k_uptime_get();
        atomic_val_t events = atomic_set(&pending, 0);
        int carb_level = gpio_pin_get_dt(&carbs);
        int concert_level = gpio_pin_get_dt(&concert);
        struct mmu_input input = {0};
        if (carb_level < 0 || concert_level < 0) { return -EIO; }
        /* Sample held inputs too: a held button at boot must not be missed.
         * Bounce coalesces; repeated events can only extend protection. */
        if (((events & 1) || carb_level) && (!seen_carb || now - last_carb >= 50)) {
            state = mmu_preempt(state, now, true);
            last_carb = now; seen_carb = true;
        }
        if (((events & 2) || concert_level) && (!seen_concert || now - last_concert >= 50)) {
            state = mmu_preempt(state, now, false);
            last_concert = now; seen_concert = true;
        }
        input.now_ms = now;
        /* No schedule/delivery adapter exists. Do not invent a delivery history,
         * issue green proposals or use the 55% rule as a treatment instruction. */
        last_result = mmu_evaluate(state, input, &ledger);
        state = last_result.state;
        if (!last_result.valid) { return -EINVAL; }
        if (wdt_feed(watchdog, channel) != 0) { return -EIO; }
        k_sleep(K_TIMEOUT_ABS_MS((int64_t)(now + 1000)));
    }
}
