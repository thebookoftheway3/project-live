// SPDX-License-Identifier: AGPL-3.0-only
#include "research_mmu.h"
#include <algorithm>
#include <cmath>

namespace live::bench {
Result transition(State previous, Input in) {
    if (in.now_ms < previous.last_ms ||
        (previous.green_started && *previous.green_started > previous.last_ms) ||
        (previous.cleared_at && *previous.cleared_at > previous.last_ms) ||
        !std::isfinite(in.requested_basal) || !std::isfinite(in.scheduled_basal) ||
        in.requested_basal < 0 || in.scheduled_basal < 0) {
        // Invalid time/state is not interpreted as permission or as a zero dose.
        previous.green_started.reset();
        previous.cleared_at = previous.last_ms;
        return {previous, std::nullopt, Reason::invalid};
    }
    State next = previous;
    next.last_ms = in.now_ms;
    auto clear = [&](Reason reason) -> Result {
        next.green_started.reset();
        next.cleared_at = in.now_ms;
        return {next, in.scheduled_basal, reason};
    };
    if (in.manual_clearance) return clear(Reason::lockout);
    if (next.green_started && in.now_ms - *next.green_started >= max_green_ms)
        return clear(Reason::watchdog);
    if (!in.budget_floor_met) {
        if (next.green_started) return clear(Reason::budget);
        return {next, in.scheduled_basal, Reason::budget};
    }
    if (!in.request_green || in.requested_basal >= in.scheduled_basal) {
        if (next.green_started) return clear(Reason::schedule);
        return {next, in.scheduled_basal, Reason::schedule};
    }
    if (next.cleared_at && in.now_ms - *next.cleared_at < clearance_lockout_ms)
        return {next, in.scheduled_basal, Reason::lockout};
    if (!next.green_started) next.green_started = in.now_ms;
    // Repeated requests cannot renew green_started and evade the watchdog.
    return {next, std::min(in.requested_basal, in.scheduled_basal), Reason::bounded};
}
}  // namespace live::bench
