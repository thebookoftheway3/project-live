// SPDX-License-Identifier: AGPL-3.0-only
#pragma once
#include <array>
#include <cstdint>
#include <optional>

// HOST SIMULATION ONLY. No command encoder, device address, radio or pump API.
namespace live::bench {
constexpr std::uint64_t max_green_ms = 30 * 60 * 1000;
constexpr std::uint64_t clearance_lockout_ms = 15 * 60 * 1000;
struct State {
    std::uint64_t last_ms = 0;
    std::optional<std::uint64_t> green_started;
    std::optional<std::uint64_t> cleared_at;
};
struct Input {
    std::uint64_t now_ms;
    double requested_basal;
    double scheduled_basal;
    bool request_green;
    bool manual_clearance;
    bool budget_floor_met;
};
enum class Reason { bounded, schedule, watchdog, lockout, budget, invalid };
struct Result {
    State state;
    std::optional<double> simulated_basal;
    Reason reason;
};
Result transition(State previous, Input input);

enum class BudgetStatus { unknown, below_floor, floor_met };
class BasalLedger {
public:
    // Integer simulated delivery per one-minute bin; never commands delivery.
    bool record(std::uint64_t minute, std::int64_t scheduled, std::int64_t delivered);
    BudgetStatus status(std::uint64_t minute) const;
    BudgetStatus projected_status(std::uint64_t minute, std::int64_t scheduled,
                                  std::int64_t candidate_delivered) const;
private:
    struct Bin { std::uint64_t minute; std::int64_t scheduled; std::int64_t delivered; };
    std::array<Bin, 180> bins_{};
    std::size_t next_ = 0;
    std::size_t size_ = 0;
    std::optional<std::uint64_t> last_;
};

enum class Bearer { offline, wifi, ltem };
Bearer select_bearer(bool wifi_mqtt_ack, bool ltem_mqtt_ack);
struct BleCapabilities {
    bool simulated_cgm;
    bool simulated_pod;
    bool real_device_transport;
};
BleCapabilities ble_capabilities();
}  // namespace live::bench
