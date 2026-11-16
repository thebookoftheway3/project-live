// SPDX-License-Identifier: AGPL-3.0-only
#include "research_mmu.h"
#include <cstdlib>
#include <iostream>
#include <limits>
using namespace live::bench;

void require(bool pass) { if (!pass) { std::cerr << "MMU invariant failed\n"; std::exit(1); } }
int main() {
    // Bounded enumerated domain, not a proof for all hardware or all C++ states.
    for (int scheduled = 0; scheduled <= 100; ++scheduled)
        for (int requested = 0; requested <= 200; ++requested) {
            const auto r = transition({}, {0, double(requested), double(scheduled), true, false, true});
            require(r.simulated_basal && *r.simulated_basal <= scheduled && *r.simulated_basal >= 0);
        }
    auto r = transition({}, {0, 0.1, 1, true, false, true});
    for (std::uint64_t t = 1000; t < max_green_ms; t += 1000) {
        r = transition(r.state, {t, 0.1, 1, true, false, true});
        require(r.reason == Reason::bounded && r.state.green_started == 0);
    }
    r = transition(r.state, {max_green_ms, 0.1, 1, true, false, true});
    require(r.reason == Reason::watchdog && *r.simulated_basal == 1);
    r = transition(r.state, {max_green_ms + clearance_lockout_ms - 1, 0.1, 1, true, false, true});
    require(r.reason == Reason::lockout);
    r = transition(r.state, {max_green_ms + clearance_lockout_ms, 0.1, 1, true, false, true});
    require(r.reason == Reason::bounded);
    r = transition(r.state, {r.state.last_ms + 1, 0.1, 1, true, true, true});
    require(r.reason == Reason::lockout);
    require(!transition(r.state, {0, 0.1, 1, true, false, true}).simulated_basal);
    for (double invalid : {-1.0, std::numeric_limits<double>::infinity(),
                           std::numeric_limits<double>::quiet_NaN()}) {
        require(!transition({}, {0, invalid, 1, true, false, true}).simulated_basal);
        require(!transition({}, {0, 1, invalid, true, false, true}).simulated_basal);
    }
    require(transition({}, {0, 0, 1, true, false, false}).reason == Reason::budget);
    BasalLedger ledger;
    for (std::uint64_t t = 0; t < 179; ++t) require(ledger.record(t, 100, 55));
    require(ledger.status(178) == BudgetStatus::unknown);
    require(ledger.record(179, 100, 55));
    require(ledger.status(179) == BudgetStatus::floor_met);
    require(ledger.projected_status(180, 100, 54) == BudgetStatus::below_floor);
    require(ledger.projected_status(180, 100, 55) == BudgetStatus::floor_met);
    require(ledger.status(179) == BudgetStatus::floor_met);  // no fabricated delivery
    const bool projected_ok = ledger.projected_status(180, 100, 0) == BudgetStatus::floor_met;
    require(transition({}, {180000, 0, 1, true, false, projected_ok}).reason == Reason::budget);
    require(!ledger.record(179, 100, 100));
    require(ledger.record(180, 100, 54));
    require(ledger.status(180) == BudgetStatus::below_floor);
    require(ledger.record(181, 100, 56));
    require(ledger.status(181) == BudgetStatus::floor_met);
    require(ledger.status(182) == BudgetStatus::unknown);
    require(ledger.record(184, 100, 55));
    require(ledger.status(184) == BudgetStatus::unknown);
    require(!ledger.record(185, -1, 0));
    require(!ledger.record(185, 1000001, 0));
    require(!ble_capabilities().real_device_transport);
    require(select_bearer(true, true) == Bearer::wifi);
    require(select_bearer(false, true) == Bearer::ltem);
    require(select_bearer(false, false) == Bearer::offline);
    std::cout << "PASS: bounded host MMU invariants; no hardware validation\n";
}
