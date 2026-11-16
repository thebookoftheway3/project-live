/* SPDX-License-Identifier: AGPL-3.0-only */
#include "conflict_monitor.h"

static uint64_t deadline(uint64_t now, uint64_t delta)
{
    return now > UINT64_MAX - delta ? UINT64_MAX : now + delta;
}

struct mmu_state mmu_init(uint64_t now_ms)
{
    struct mmu_state s = {0};
    s.last_ms = now_ms;
    /* Reset cannot clear a potentially active 180-minute protection interval. */
    s.lockout_until_ms = deadline(now_ms, MMU_CONCERT_MS);
    return s;
}

static void clear_green(struct mmu_state *s, uint64_t now)
{
    if (s->green) {
        uint64_t until = deadline(now, MMU_LOCKOUT_MS);
        if (until > s->lockout_until_ms) { s->lockout_until_ms = until; }
    }
    s->green = false;
    s->green_since_ms = 0;
    s->command_end_ms = 0;
}

bool mmu_record(struct mmu_ledger *l, uint64_t minute,
                uint32_t scheduled, uint32_t observed)
{
    if (l == NULL) { return false; }
    if (l->count > MMU_BINS || l->next >= MMU_BINS ||
        scheduled > MMU_MAX_UNITS || observed > MMU_MAX_UNITS) {
        l->count = 0; l->next = 0;
        return false;
    }
    if (l->count != 0) {
        uint64_t last = l->bins[(l->next + MMU_BINS - 1) % MMU_BINS].minute;
        if (minute <= last) {
            l->count = 0; l->next = 0;
            return false;
        }
        if (minute - last != 1) { l->count = 0; l->next = 0; }
    }
    l->bins[l->next] = (struct mmu_bin){minute, scheduled, observed};
    l->next = (l->next + 1) % MMU_BINS;
    if (l->count < MMU_BINS) { ++l->count; }
    return true;
}

bool mmu_budget_allows(const struct mmu_ledger *l, uint64_t now_minute,
                       uint32_t scheduled, uint32_t candidate, uint32_t minutes)
{
    uint64_t sum_s = 0, sum_o = 0;
    size_t i;
    if (l == NULL || l->count != MMU_BINS || l->next >= MMU_BINS ||
        now_minute < MMU_BINS || scheduled == 0 || scheduled > MMU_MAX_UNITS ||
        candidate > scheduled || minutes == 0 || minutes > 30) { return false; }
    for (i = 0; i < MMU_BINS; ++i) {
        const struct mmu_bin *b = &l->bins[(l->next + i) % MMU_BINS];
        if (b->minute != now_minute - MMU_BINS + i ||
            b->scheduled > MMU_MAX_UNITS || b->observed > MMU_MAX_UNITS) { return false; }
        sum_s += b->scheduled;
        sum_o += b->observed;
    }
    if (sum_s == 0 || sum_o * 100 < sum_s * 55) { return false; }
    /* Check every projected minute of a flat-profile command, on totals only.
     * No candidate value is ever recorded as observed delivery. */
    for (i = 0; i < minutes; ++i) {
        const struct mmu_bin *b = &l->bins[(l->next + i) % MMU_BINS];
        sum_s = sum_s - b->scheduled + scheduled;
        sum_o = sum_o - b->observed + candidate;
        if (sum_s == 0 || sum_o * 100 < sum_s * 55) { return false; }
    }
    return true;
}

static bool state_valid(struct mmu_state s, uint64_t now)
{
    return !s.fault && now >= s.last_ms &&
           (!s.green || (s.green_since_ms <= s.last_ms &&
             s.command_end_ms > s.green_since_ms &&
             s.command_end_ms - s.green_since_ms <= MMU_MAX_GREEN_MS));
}

struct mmu_state mmu_preempt(struct mmu_state s, uint64_t now, bool carbs)
{
    uint64_t until;
    if (!state_valid(s, now)) { s.fault = true; return s; }
    clear_green(&s, now);
    until = deadline(now, MMU_LOCKOUT_MS);
    if (until > s.lockout_until_ms) { s.lockout_until_ms = until; }
    if (carbs) { s.carb_until_ms = deadline(now, MMU_CARB_MS); }
    else { s.concert_until_ms = deadline(now, MMU_CONCERT_MS); }
    s.last_ms = now;
    return s;
}

struct mmu_result mmu_evaluate(struct mmu_state s, struct mmu_input in,
                               const struct mmu_ledger *ledger)
{
    struct mmu_result r = {s, in.scheduled, true, MMU_SCHEDULE};
    uint32_t duration = in.duration_ms;
    if (!state_valid(s, in.now_ms) || in.scheduled > MMU_MAX_UNITS ||
        in.requested > MMU_MAX_UNITS ||
        (in.request_green && (duration == 0 || in.now_ms > UINT64_MAX - MMU_MAX_GREEN_MS))) {
        r.state.fault = true;
        clear_green(&r.state, in.now_ms);
        r.valid = false; r.simulated_basal = 0; r.reason = MMU_INVALID;
        return r;
    }
    r.state.last_ms = in.now_ms;
    if (duration > MMU_MAX_GREEN_MS) { duration = (uint32_t)MMU_MAX_GREEN_MS; }
    if (s.green && (in.now_ms - s.green_since_ms >= MMU_MAX_GREEN_MS ||
                    in.now_ms >= s.command_end_ms)) { r.reason = MMU_WATCHDOG; }
    else if (in.manual_clearance) {
        uint64_t until = deadline(in.now_ms, MMU_LOCKOUT_MS);
        if (until > r.state.lockout_until_ms) { r.state.lockout_until_ms = until; }
    }
    else if (in.now_ms < s.carb_until_ms) { r.reason = MMU_CARB; }
    else if (in.now_ms < s.concert_until_ms) { r.reason = MMU_CONCERT; }
    else if (!in.request_green || in.requested >= in.scheduled) { /* schedule */ }
    else if (in.now_ms < s.lockout_until_ms) { r.reason = MMU_LOCKOUT; }
    else if (!mmu_budget_allows(ledger, in.now_ms / MMU_MINUTE_MS,
                  in.scheduled, in.requested,
                  (duration + (uint32_t)MMU_MINUTE_MS - 1) / (uint32_t)MMU_MINUTE_MS)) {
        r.reason = MMU_BUDGET;
    }
    else {
        r.reason = MMU_BOUNDED;
        r.simulated_basal = in.requested; /* already strictly below schedule */
        if (!s.green) {
            r.state.green = true;
            r.state.green_since_ms = in.now_ms;
            r.state.command_end_ms = in.now_ms + duration;
        }
        /* A repeated proposal can shorten, never renew, the original lease. */
        if (in.now_ms + duration < r.state.command_end_ms) {
            r.state.command_end_ms = in.now_ms + duration;
        }
        return r;
    }
    clear_green(&r.state, in.now_ms);
    return r;
}
