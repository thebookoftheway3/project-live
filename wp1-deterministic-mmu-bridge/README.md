# WP1 — Thingy:91 X deterministic research target

**Hardware target:** Nordic Thingy:91 X (`THINGY91X`, `PCA20065`), Zephyr through
nRF Connect SDK **v3.2.1**. [ADR 0005](../docs/decisions/0005-nordic-thingy91x-hardware-target.md)
records the selection and corrects the requested TX power, SIM and button assumptions.
[Manufacturer artifacts](hardware-vendor/MANIFEST.md) include hashed schematics,
enclosure STEP files, board-source snapshots, licences and the project overlay.

**Implemented:** the unchanged C++17 host model plus a C99 pure evaluator, host
invariant tests and a Zephyr app entry point. The app configures a 10-second CPU
watchdog, input interrupts, BLE initialization and 1 Hz evaluation. There is no
schedule/delivery adapter, green proposal source, pump transport, scan/connect
request or MQTT transmission. Host checks and a compilable image, when recorded,
are not evidence of hardware safety or a functioning medical-device connection.

```sh
sh tools/check_mmu.sh
```

Both host models use explicit temporal state. The C99 path clamps experimental
rates at schedule, caps command duration at 30 minutes without renewal extension,
and imposes a 15-minute clearance lockout. Button events inhibit reductions for
60 minutes (carbs) or 180 minutes (concert); held inputs extend protection.
Clock/state errors latch a fault. Reboot starts a conservative 180-minute hold.

The C99 ledger requires 180 fresh, contiguous completed minute bins and tests the
55% floor over every projected minute of a candidate command (flat future schedule
assumption). It never records a candidate as observed delivery. Missing, stale or
invalid history inhibits green. The floor is **not evidence of DKA prevention**;
none of these research parameters is a treatment recommendation. C++ behavior is
preserved as the earlier reference rather than silently changed to the C99 API.

## Build the app

Install Nordic's matching SDK/toolchain in a separate workspace. Follow the
[official SDK installation instructions](https://docs.nordicsemi.com/bundle/ncs-3.2.1/page/nrf/installation/install_ncs.html).
The release manifest pins Zephyr and modules; the vendor snapshot is not an SDK.
Use a source/build path without spaces (the pinned sysbuild splits Kconfig paths
on whitespace). Copy the WP1 directory to such a path if needed; keep `firmware/`
and `hardware-vendor/` adjacent. From the SDK's activated toolchain shell,
substituting that absolute path:

```sh
west build --sysbuild -p always -b thingy91x/nrf5340/cpuapp \
  /path/to/project-live/wp1-deterministic-mmu-bridge/firmware \
  -d /tmp/project-live-thingy91x-build
```

Sysbuild includes the nRF5340 network-core `ipc_radio` image. Controller capacity
and **+3 dBm** configuration belong in `firmware/sysbuild/ipc_radio.conf`; the
app core owns the host. `CONFIG_BT_CTLR_TX_PWR_PLUS_8` is unsupported by nRF5340.
`CONFIG_MQTT_LIB_TLS` enables library support, not a network connection. Wi-Fi,
modem, fuel-gauge reporting, TLS provisioning and acknowledged failover are absent.
`thingy91x/nrf9151/ns` identifies the separate modem-side application target;
this app must not be built for it or represented as a combined modem implementation.

No flash command is supplied or executed. SDK development keys are public examples,
not production identities. Read the build evidence and gaps in
[THINGY91X_VALIDATION](../docs/assurance/THINGY91X_VALIDATION.md) before using an image.

## Hardware work remaining

- Match delivered PCB revision to the pinned PCA20065 2.0.0 files.
- Verify `sw0`/P0.24 and input-only `sw1`/P1.15, shared reset behavior, button bounce,
  1 Hz response latency, boot/held-button behavior and watchdog fault injection.
- Resolve processor ownership of I2C/SPI/PMIC/flash, HCI IPC, RF front-end power and
  Wi-Fi/BLE coexistence before radio or power claims.
- Measure SoC estimation, battery runtime, reset recovery, CGM interoperability,
  TLS/session expiry and Wi-Fi/LTE-M failover with explicit consent and no actuation.
- Design/test guards and clips against the actual base/top CAD, antenna keepouts,
  button travel, thermal, drop and accessibility constraints.

`hardware-cad/walter_pocket_case.scad` remains a historical concept with assumed
fit; it is not the Thingy enclosure. `ble_dual_manager.cpp` still declares no
real transport, and `ltem_failover.cpp` remains a simulated acknowledged-bearer
selector. Physical hardware/RF/BLE tests are **pending hardware delivery**.

See [FMEA](../docs/FMEA_SAFETY_ANALYSIS.md) and
[verification plan](../docs/GRANT_VERIFICATION_PLAN.md).
