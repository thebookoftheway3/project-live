/* SPDX-License-Identifier: AGPL-3.0-only */
#ifndef LIVE_CONFLICT_MONITOR_H
#define LIVE_CONFLICT_MONITOR_H
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/* Research units per minute, not a pump wire format or a dosing API. */
#define MMU_MINUTE_MS UINT64_C(60000)
#define MMU_MAX_GREEN_MS (30 * MMU_MINUTE_MS)
#define MMU_LOCKOUT_MS (15 * MMU_MINUTE_MS)
#define MMU_CARB_MS (60 * MMU_MINUTE_MS)
#define MMU_CONCERT_MS (180 * MMU_MINUTE_MS)
#define MMU_BINS 180U
#define MMU_MAX_UNITS UINT32_C(1000000)

struct mmu_bin { uint64_t minute; uint32_t scheduled, observed; };
struct mmu_ledger {
    struct mmu_bin bins[MMU_BINS];
    size_t count, next;
};
struct mmu_state {
    uint64_t last_ms, green_since_ms, command_end_ms;
    uint64_t lockout_until_ms, carb_until_ms, concert_until_ms;
    bool green, fault;
};
struct mmu_input {
    uint64_t now_ms;
    uint32_t scheduled, requested, duration_ms;
    bool request_green, manual_clearance;
};
enum mmu_reason {
    MMU_SCHEDULE, MMU_BOUNDED, MMU_WATCHDOG, MMU_CARB,
    MMU_CONCERT, MMU_LOCKOUT, MMU_BUDGET, MMU_INVALID
};
struct mmu_result {
    struct mmu_state state;
    uint32_t simulated_basal;
    bool valid;
    enum mmu_reason reason;
};

/* Explicit state, no hidden globals, clocks, I/O or allocation in the evaluator. */
struct mmu_state mmu_init(uint64_t now_ms);
bool mmu_record(struct mmu_ledger *ledger, uint64_t minute,
                uint32_t scheduled, uint32_t observed);
bool mmu_budget_allows(const struct mmu_ledger *ledger, uint64_t now_minute,
                       uint32_t scheduled, uint32_t candidate, uint32_t minutes);
struct mmu_state mmu_preempt(struct mmu_state previous, uint64_t now_ms, bool carbs);
struct mmu_result mmu_evaluate(struct mmu_state previous, struct mmu_input input,
                               const struct mmu_ledger *ledger);
#endif
