// SPDX-License-Identifier: AGPL-3.0-only
#include "research_mmu.h"

namespace live::bench {
bool BasalLedger::record(std::uint64_t minute, std::int64_t scheduled, std::int64_t delivered) {
    // Bound arithmetic and reject reordered/repeated bins. Missing bins invalidate
    // coverage rather than being filled with assumed delivery.
    if (scheduled < 0 || delivered < 0 || scheduled > 1000000 || delivered > 1000000 ||
        (last_ && minute <= *last_)) return false;
    if (last_ && minute - *last_ != 1) { size_ = 0; next_ = 0; }
    bins_[next_] = {minute, scheduled, delivered};
    next_ = (next_ + 1) % bins_.size();
    if (size_ < bins_.size()) ++size_;
    last_ = minute;
    return true;
}
BudgetStatus BasalLedger::status(std::uint64_t minute) const {
    if (size_ != bins_.size() || !last_ || minute != *last_) return BudgetStatus::unknown;
    std::int64_t scheduled = 0, delivered = 0;
    for (const auto& bin : bins_) { scheduled += bin.scheduled; delivered += bin.delivered; }
    // A zero scheduled total carries no interpretable fractional floor.
    if (!scheduled) return BudgetStatus::unknown;
    return delivered * 100 >= scheduled * 55 ? BudgetStatus::floor_met : BudgetStatus::below_floor;
}
BudgetStatus BasalLedger::projected_status(std::uint64_t minute, std::int64_t scheduled,
                                          std::int64_t candidate_delivered) const {
    // Evaluate a hypothetical next bin without recording it as actual delivery.
    auto projected = *this;
    if (!projected.record(minute, scheduled, candidate_delivered)) return BudgetStatus::unknown;
    return projected.status(minute);
}
}  // namespace live::bench
