// SPDX-License-Identifier: AGPL-3.0-only
#include "research_mmu.h"

namespace live::bench {
Bearer select_bearer(bool wifi_mqtt_ack, bool ltem_mqtt_ack) {
    // Pure selection oracle. An association/registration alone is not delivery.
    // No modem/SIM credentials, MQTT socket or physical failover timing exists.
    if (wifi_mqtt_ack) return Bearer::wifi;
    if (ltem_mqtt_ack) return Bearer::ltem;
    return Bearer::offline;
}
}  // namespace live::bench
