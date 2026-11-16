/* SPDX-License-Identifier: AGPL-3.0-only */
#include "conflict_monitor.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CHECK(x, message) do { if (!(x)) { fprintf(stderr, "%s\n", message); exit(1); } } while (0)
static const uint64_t start = 180 * MMU_MINUTE_MS;
static struct mmu_ledger full(uint64_t minute, uint32_t delivered)
{
    struct mmu_ledger l = {0};
    uint64_t i;
    for (i = minute - MMU_BINS; i < minute; ++i) {
        CHECK(mmu_record(&l, i, 100, delivered), "record contiguous history");
    }
    return l;
}
static struct mmu_input proposal(uint64_t now)
{
    struct mmu_input in = {now, 100, 50, (uint32_t)MMU_MAX_GREEN_MS, true, false};
    return in;
}
int main(void)
{
    struct mmu_state s = mmu_init(0);
    struct mmu_ledger l = full(180, 100), copy;
    struct mmu_input in = proposal(start);
    struct mmu_result r;
    uint32_t requested, scheduled;
    CHECK(mmu_evaluate(s, proposal(0), &l).reason == MMU_LOCKOUT, "reset lockout");
    for (scheduled = 1; scheduled <= 100; ++scheduled) {
        for (requested = 0; requested <= 200; ++requested) {
            in.scheduled = scheduled; in.requested = requested;
            r = mmu_evaluate(s, in, &l);
            CHECK(r.valid && r.simulated_basal <= scheduled, "zero upward invariant");
        }
    }
    in = proposal(start);
    r = mmu_evaluate(s, in, &l);
    CHECK(r.reason == MMU_BOUNDED && r.simulated_basal == 50, "bounded candidate");
    s = r.state;
    in.now_ms = start + 1000;
    r = mmu_evaluate(s, in, &l);
    CHECK(r.state.command_end_ms == start + MMU_MAX_GREEN_MS, "renewal cannot extend lease");
    in.now_ms = start + MMU_MAX_GREEN_MS;
    r = mmu_evaluate(r.state, in, &l);
    CHECK(r.reason == MMU_WATCHDOG && r.simulated_basal == 100, "max green expiry");
    s = r.state;
    in.now_ms += MMU_LOCKOUT_MS - 1;
    CHECK(mmu_evaluate(s, in, &l).reason == MMU_LOCKOUT, "lockout before boundary");
    ++in.now_ms;
    l = full(in.now_ms / MMU_MINUTE_MS, 100);
    CHECK(mmu_evaluate(s, in, &l).reason == MMU_BOUNDED, "lockout exact boundary");
    s = mmu_init(0); in = proposal(start); l = full(180, 100);
    in.duration_ms = UINT32_MAX;
    r = mmu_evaluate(s, in, &l);
    CHECK(r.state.command_end_ms == start + MMU_MAX_GREEN_MS, "duration clamped");
    in.duration_ms = 1000;
    r = mmu_evaluate(s, in, &l);
    in.now_ms += 1000;
    CHECK(mmu_evaluate(r.state, in, &l).reason == MMU_WATCHDOG, "short lease expiry");
    in = proposal(start); in.manual_clearance = true;
    r = mmu_evaluate(s, in, &l);
    CHECK(r.simulated_basal == 100, "manual clearance");
    in.manual_clearance = false;
    CHECK(mmu_evaluate(r.state, in, &l).reason == MMU_LOCKOUT, "manual lockout while idle");
    s = mmu_preempt(s, start, true);
    CHECK(mmu_evaluate(s, in, &l).reason == MMU_CARB, "carb guard");
    in.now_ms += MMU_CARB_MS - 1;
    CHECK(mmu_evaluate(s, in, &l).reason == MMU_CARB, "carb before boundary");
    ++in.now_ms; l = full(in.now_ms / MMU_MINUTE_MS, 100);
    CHECK(mmu_evaluate(s, in, &l).reason == MMU_BOUNDED, "carb exact boundary");
    s = mmu_preempt(s, in.now_ms, false);
    CHECK(mmu_evaluate(s, in, &l).reason == MMU_CONCERT, "concert guard");
    in.now_ms += MMU_CONCERT_MS;
    l = full(in.now_ms / MMU_MINUTE_MS, 100);
    CHECK(mmu_evaluate(s, in, &l).reason == MMU_BOUNDED, "concert exact boundary");
    s = mmu_init(0); in = proposal(start); l = full(180, 55); copy = l;
    CHECK(mmu_evaluate(s, in, &l).reason == MMU_BUDGET, "projected floor rejects deficit");
    in.requested = 55;
    CHECK(mmu_evaluate(s, in, &l).reason == MMU_BOUNDED, "exact 55 percent floor");
    CHECK(memcmp(&l, &copy, sizeof(l)) == 0, "projection never records delivery");
    l = full(180, 60); in.requested = 0;
    CHECK(mmu_evaluate(s, in, &l).reason == MMU_BUDGET, "whole duration budget");
    l = full(180, 55); l.bins[0].observed = 0;
    CHECK(!mmu_budget_allows(&l, 180, 100, 100, 1), "historical deficit rejected");
    l = full(180, 54);
    CHECK(!mmu_budget_allows(&l, 180, 100, 100, 1), "historical deficit rejected");
    l = full(180, 100);
    CHECK(!mmu_budget_allows(&l, 181, 100, 50, 1), "stale history rejected");
    CHECK(!mmu_record(&l, 179, 100, 100) && l.count == 0, "duplicate invalidates history");
    l = full(180, 100);
    CHECK(mmu_record(&l, 181, 100, 100) && l.count == 1, "gap discards coverage");
    CHECK(!mmu_budget_allows(&l, 182, 100, 50, 1), "incomplete history rejected");
    l = full(180, 100); l.bins[0].minute = 8;
    CHECK(!mmu_budget_allows(&l, 180, 100, 50, 1), "corrupt chronology rejected");
    l = full(180, 100); l.bins[0].observed = UINT32_MAX;
    CHECK(!mmu_budget_allows(&l, 180, 100, 50, 1), "overflow input rejected");
    l = full(180, 100); in = proposal(start);
    s = mmu_evaluate(s, in, &l).state; --in.now_ms;
    r = mmu_evaluate(s, in, &l);
    CHECK(!r.valid && r.state.fault, "clock regression latches fault");
    in.now_ms = start + 1;
    CHECK(!mmu_evaluate(r.state, in, &l).valid, "latched fault persists");
    in = proposal(UINT64_MAX - 1);
    CHECK(!mmu_evaluate(mmu_init(0), in, &l).valid, "deadline overflow rejected");
    in = proposal(start); in.duration_ms = 0;
    CHECK(!mmu_evaluate(mmu_init(0), in, &l).valid, "zero duration rejected");
    in = proposal(start); in.scheduled = UINT32_MAX;
    CHECK(!mmu_evaluate(mmu_init(0), in, &l).valid, "rate overflow rejected");
    s = mmu_init(0); s.green = true; s.green_since_ms = 1;
    CHECK(!mmu_evaluate(s, proposal(start), &l).valid, "future state rejected");
    CHECK(!mmu_budget_allows(NULL, 180, 100, 50, 1), "missing ledger rejected");
    CHECK(!mmu_record(NULL, 0, 100, 100), "missing ledger record rejected");
    puts("C99 MMU invariants passed (20,100 bounded-rate cases plus temporal/budget failures)");
    return 0;
}
