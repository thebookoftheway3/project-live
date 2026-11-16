# ADR 0005: Nordic Thingy:91 X hardware target

- Status: Proposed
- Date: 2026-11-16
- Authority: owner selected THINGY91X/PCA20065 for the PR following merged PR #16; implementation authorized, ADR acceptance awaits explicit review.
- Review: Codex-assisted; no independent hardware, security or clinical reviewer.
- References: R01/R03/R07/R12/R14/R20/R26; LIVE-014/016/019; ADR 0004.
- Preserves: non-actuating research, independent treatment, original C++17 tests.

## Problem and alternatives

WP1 has host simulations and a conceptual ESP-IDF component, without an identified
board power design, reproducible RTOS entry point or manufacturer CAD provenance.
The intended change is a reviewable Thingy:91 X C99 bench application and retained
portable C++ tests. It is not a pump bridge or a clinically validated interlock.

| Alternative | Benefits | Costs / decision |
| --- | --- | --- |
| Keep host-only scaffold | Fast, reproducible experiments | Retained as regression reference, insufficient for requested hardware work |
| Continue Walter / generic ESP32-S3 / LilyGO exploration | Existing conceptual enclosure and modem seam | No integrated-board evidence in this repository; deferred, not a blanket vendor safety judgment |
| Thingy:91 X with nRF Connect SDK / Zephyr | Integrated power, multiple processors/radios, vendor CAD and board support | Selected; shared peripherals, IPC, RF coexistence and bootloader ownership add integration work |

## Manufacturer evidence and corrections

Versioned downloads, extracted schematics/enclosure CAD, licences, source snapshots
and SHA-256 hashes are in the [vendor manifest](../../wp1-deterministic-mmu-bridge/hardware-vendor/MANIFEST.md).

- **Power integrity:** Nordic lists nPM1300/nPM6001 and a 1350 mAh Li-Po battery.
  This gives a documented power/charging design instead of requiring new external
  LiPo/TP4056 wiring. Fuel gauging combines PMIC measurements with software and a
  battery model; it is not implemented SoC telemetry merely because the IC exists.
  The enclosure and CE listing do not certify this modified application as a
  medical device or establish thermal, battery or pocket-use safety.
- **BLE:** nRF5340 dual-core silicon supports Bluetooth LE 5.4. Its native maximum
  TX power is **+3 dBm**, not the requested +8 dBm. Select the supported controller
  setting on the network core. Shared Nordic silicon reduces the SDK/vendor mix;
  it cannot eliminate device protocol, authentication, coexistence or stack
  compatibility problems. No G7 or O5 pairing/transport is present.
- **Redundancy:** nRF7002 Wi-Fi 6 and nRF9151 LTE-M/NB-IoT offer candidate network
  paths. The CPU watchdog offers local fault detection during a radio blackout;
  it is not a third communications path or an independent dosing controller.
  Nordic advertises bundled Onomondo/Wireless Logic SIM cards. A soldered MFF2
  multi-IMSI eSIM is not established for the delivered kit and is not assumed.
  Registration, TLS, authenticated acknowledgements, queues, expiry and measured
  failover remain future work; MQTT Kconfig alone does not implement failover.
- **Tactile inputs:** the app core's `sw0` is Button 2/P0.24. The second button
  is P1.15 in `zephyr,user/button1-gpios`, not an SDK `sw1` alias. A project overlay
  exposes an input-only `sw1`. Processor-specific aliases and shared button/reset
  signals require a delivered-board review. Do not label the power/debug switches
  as preemption buttons or drive a shared reset line.

Sources: [Nordic kit](https://www.nordicsemi.com/Products/Development-hardware/Nordic-Thingy-91-X),
[nRF5340 radio specification](https://docs.nordicsemi.com/r/bundle/ps_nrf5340/page/radio.html),
[nRF5340 feature comparison](https://www.nordicsemi.com/Products/nRF5340),
[nPM1300 fuel gauge](https://www.nordicsemi.com/Products/nPM1300), and the pinned
SDK DTS files in the manifest. Hardware availability and source inspection are
not observations of a working composed system.

## Implementation contract

NCS **v3.2.1** owns the `thingy91x/nrf5340/cpuapp` and `thingy91x/nrf9151/ns`
board targets. The new C99 application targets only the nRF5340 application core;
a separate sysbuild IPC radio image owns the Bluetooth controller. The nRF9151
firmware package is referenced and hashed, not integrated or flashed. Keep the
existing C++17 model unchanged as a host regression reference.

The evaluator is a pure calculation over explicit temporal state and a read-only
ledger. “Stateless” means no hidden state or I/O; watchdogs and hysteresis still
require history. Experimental integer units per minute are not a wire protocol.

1. Valid output never exceeds the supplied scheduled value. Invalid input/state
   produces no valid output and latches a fault.
2. Green leases last at most 30 minutes. Renewal cannot extend their original end;
   shorter commands may shorten it. Exit/expiry imposes 15 minutes of lockout.
3. `sw0` latches a 60-minute fast-carb guard; `sw1` latches a 180-minute concert
   guard. Both inhibit experimental reduction, never mute clinical alarms.
4. The 180 completed, contiguous minute bins must be fresh and meet the 55% floor.
   Every projected minute of the candidate's duration must also meet it. Projection
   never becomes an observed delivery. The experiment assumes a flat future
   schedule for that lease; real profile changes require a new contract.
5. Unknown history inhibits green. Reboot starts a 180-minute hold covering a
   possibly interrupted protection window; clock regression latches a fault.
   There is no authenticated persistence or delivery adapter.

The 55% floor is **not evidence of DKA prevention**. The 30/15/60/180-minute choices
are owner-specified experiments, not medical recommendations. Timed guards cannot
establish actual carbohydrate absorption or a physiological safety envelope.

GPIO ISRs only latch events. Main owns state and evaluates at 1 Hz; event handling
can therefore take one loop period. Held buttons extend protection, including at
startup. A 10-second hardware watchdog is fed only after initialization and a
successful loop; it is distinct from the 30-minute logical lease. Initialization,
GPIO-read, evaluator or watchdog-feed failure stops feeding. The main application
has no schedule source, recorded delivery, green-request source, BLE scan/connect,
pump encoding, credentials, MQTT publish or remote destination.

## Verification, risks and rollback

[Target build and host evidence](../assurance/THINGY91X_VALIDATION.md) records actual
results and omitted checks. Preserve both required Python CI job names and their
lint, mutation and dependency gates. Add C99 boundary/property tests and targeted
mutations to the existing MMU/negative-control checks.

No device has been flashed. Hardware watchdog reset latency, GPIO routing and
bounce, RF/BLE interoperability, PMIC/SoC telemetry, current consumption, radio
blackout recovery, Wi-Fi/LTE failover, CAD fit and accessibility tests remain
pending hardware delivery. The SDK's public development signing keys are not
production trust roots; this PR adds no signing key or release provisioning.

Revert this focused branch to restore the host-only target. Reopen the decision
before actuation, network provisioning, shared-peripheral ownership, durable
state recovery, clinical evaluation or production release. The old Walter CAD
remains historical evidence, not a Thingy enclosure or a supported hardware target.
