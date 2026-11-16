// SPDX-License-Identifier: AGPL-3.0-only
#include "research_mmu.h"

namespace live::bench {
BleCapabilities ble_capabilities() {
    // Reserved adapter seam only. Dexcom G7 Slot 2, O5 protocol, +9 dBm radio
    // setup and concurrent device operation have NOT been implemented/verified.
    // Deliberately no ESP-IDF BLE initialization or pump write characteristic.
    return {false, false, false};
}
}  // namespace live::bench
