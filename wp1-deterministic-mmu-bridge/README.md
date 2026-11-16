# WP1 — Deterministic MMU bridge research

**Implemented:** host-only C++17 transition and ledger models, bearer selection
oracle, negative device-capability declaration and a parametric enclosure concept.
Run `sh tools/check_mmu.sh` from the repository root.

`transition` is a pure function over explicit state. Green requests are bounded by
the scheduled value. Repeated requests do not refresh the 30-minute timer. Manual
clearance, watchdog expiry or exit from green begins a 15-minute lockout. Invalid
numbers, invalid timing or clock regression produce no simulated value. This is
not a fallback instruction for a real pump. On actual hardware, independent state
ownership, reset recovery, signed configuration and physical separation remain open.

The ledger retains 180 contiguous one-minute bins in integer experimental units.
It reports whether recorded delivery meets 55% of the corresponding schedule;
partial, stale, gapped or zero-schedule history is UNKNOWN. It never infers actual
delivery from a command. `projected_status` evaluates a proposed next bin on a
copy; its result can inhibit simulated green without recording a hypothetical
delivery as real. The floor is **not evidence of DKA prevention**, and the
model does not compensate for a historical deficit by commanding more insulin.

**Reserved, not integrated:** ESP-IDF scheduling, independent hardware watchdog,
Dexcom G7 Slot 2, Omnipod 5 BLE protocol, simultaneous central connections, +9 dBm,
Walter modem driver, 1NCE provisioning, authenticated MQTT retry/deduplication and
measured Wi-Fi/LTE-M failover. `ble_dual_manager.cpp` explicitly reports no real
transport. `ltem_failover.cpp` only selects an already acknowledged simulated bearer.

Walter's documented [ESP32-S3/Sequans platform](https://github.com/QuickSpot/walter-arduino)
and [ESP-IDF BLE API](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/bluetooth/esp_gap_ble.html)
do not prove the requested device interoperability. The component CMake file is
unverified on ESP-IDF. No pump protocol is imported.

The OpenSCAD enclosure uses assumed fit-test dimensions. Tactile guards are a
concept; PCB/battery fit, antenna keepout, thermal, drop, ingress and accessibility
tests are outstanding. It is not a validated wearable enclosure.

See [ADR 0004](../docs/decisions/0004-work-package-research-monorepo.md),
[FMEA](../docs/FMEA_SAFETY_ANALYSIS.md) and [verification plan](../docs/GRANT_VERIFICATION_PLAN.md).
