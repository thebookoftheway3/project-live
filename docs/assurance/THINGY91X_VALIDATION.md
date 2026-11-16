# Thingy:91 X verification record

Date: 2026-11-16. Baseline: merged PR #16, `fd65696297e7ce95755b4ee92c60b70a72b2ece3`.
Scope: [ADR 0005](../decisions/0005-nordic-thingy91x-hardware-target.md),
[WP1](../../wp1-deterministic-mmu-bridge/README.md), R01/R03/R07/R12/R14/R20/R26.
This record concerns source/host/build checks, not clinical validation.

## Executed evidence

Environment: macOS arm64, Python 3.12.14, Ruff 0.17.4, rumdl 0.3.2,
Zizmor 1.32.0, pytest 9.2.0 and Apple Clang. Verification tools use the unchanged
`requirements/ci.txt` lock; API dependencies use the existing service lock.
Pytest was installed only in the temporary verification venv.

| Exact check (from repository root with verification venv on PATH) | Result |
| --- | --- |
| `python -m unittest discover -s tests -v` | 76 tests passed, including WP2/WP3 discovery |
| `PYTHONPATH=wp2-bayesian-voi-engine/src:wp3-edge-vision-pipelines/topdown-quantifier:wp3-edge-vision-pipelines/topological-room-graph python -m pytest tests wp2-bayesian-voi-engine/tests wp2-bayesian-voi-engine/service_tests wp3-edge-vision-pipelines/tests -q` | 80 tests and 9,933 subtests passed; one existing Starlette/httpx deprecation warning |
| `python -m project_live.cli replay data/synthetic_example.jsonl` | Six synthetic records replayed |
| `sh tools/check_mmu.sh` | Preserved C++17 suite and new C99 suite passed under warnings-as-errors |
| `python tools/check_negative_controls.py` | All 28 offline mutations detected, including seven new C99 probes |
| `ruff check .` and `ruff format --check .` | Passed |
| `rumdl check .` and `python tools/check_templates.py` | Passed documentation/link and template checks |
| `zizmor --offline --no-progress --strict-collection --persona auditor .github` | No findings |
| `python -m pip_audit --no-deps --disable-pip -r requirements/ci.txt` | No known vulnerabilities |
| `python -m pip_audit --no-deps --disable-pip -r wp2-bayesian-voi-engine/requirements-service.txt` | No known vulnerabilities |
| `python tools/check_negative_controls.py --audit-only` | Known vulnerable Django metadata detected; package not installed |
| `git diff --check` and `git diff --cached --check` | Passed, including unmodified vendor files |

The C99 suite enumerates 20,100 rate pairs and exercises lease/guard/lockout
boundaries, complete projected budgets, invalid/stale/gapped history, clock
regression, overflow and fault latching. An additional host run compiled the C99
source and test with `cc -std=c99 -Wall -Wextra -Werror -pedantic
-fsanitize=address,undefined`; it passed with no sanitizer findings. This does not
test all possible states or establish physical bypass resistance.

All 16 extracted/snapshot artifact hashes match MANIFEST.md. Every SDK snapshot
also matches the pinned SDK checkout byte-for-byte. Official archive hashes were
computed before extraction. CAD files remain unmodified; Git binary attributes
preserve their bytes and avoid treating STEP geometry as source diffs.

## Zephyr target build

A complete sysbuild succeeded for `thingy91x/nrf5340/cpuapp`, including
`ipc_radio` on `thingy91x/nrf5340/cpunet`, MCUboot and the SDK boot images.
The build used NCS v3.2.1, Zephyr commit
`ec78104f15691cccd94682cf4b22e0a013f28dd8`, west 1.5.0, CMake 4.4.5,
Ninja 1.13.2 and **Zephyr SDK 0.17.4 / GCC 12.2.0** on macOS arm64.
This is the tested compiler, not a claim about every Nordic toolchain bundle.

The ARM toolchain archive from the
[official SDK release](https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.17.4/toolchain_macos-aarch64_arm-zephyr-eabi.tar.xz)
matched the release's `sha256.sum`:
`c0fbf111d2232dd533d813f49ddfbcc45014c4e2da7f2a17bf80599ac5bfbdeb`.

Source was copied byte-for-byte to `/private/tmp/live-target-source`, keeping
`firmware/` and `hardware-vendor/` adjacent to avoid the SDK's path-space issue.
From the isolated west workspace `/private/tmp/live-ncs`:

```sh
PATH=/private/tmp/live-ncs-tools/bin:$PATH ZEPHYR_TOOLCHAIN_VARIANT=zephyr ZEPHYR_SDK_INSTALL_DIR=/private/tmp/live-zephyr-sdk west build --sysbuild -p always -b thingy91x/nrf5340/cpuapp   /private/tmp/live-target-source/firmware -d /private/tmp/live-thingy-build
```

The SDK workspace fetched only these build dependencies at their release-manifest
revisions: zephyr, cmsis, cmsis_6, hal_nordic, nrfxlib, mcuboot, mbedtls,
oberon-psa-crypto, zcbor, segger, picolibc, open-amp and libmetal. Build tools and
sources stayed outside Git. Generated HEX/ZIP files and SDK development-key
signatures are build artifacts, not a release or provisioned device.

Resolved app Kconfig includes GPIO, watchdog, BT central with two connections,
networking, MQTT and MQTT TLS. The controller resolves two connections and +3 dBm.
Native TLS requires the Nordic security backend plus explicit cryptographic
capabilities; library enable flags alone did not link. No TLS session was opened.

Upstream board/boot images emit deprecation and unused UART/log/footer-setting
warnings. Dtc is absent in this host toolchain; Zephyr's Python devicetree parsing
and header generation succeed, but the optional external Dtc diagnostics were not
run. Warning policies were not changed to force success. Build success does not
claim warning-free SDK code. No firmware was flashed or executed on hardware.

Hosted CI results belong to the pushed commit and are linked in the PR; local
results above do not substitute for those runs. Existing required Python job
names/permissions remain unchanged; their MMU step now runs both C++ and C99.
The target cross-build is local evidence, not a new hosted CI gate.

## Corrections and negative results

- Manufacturer inspection corrected +8 dBm to nRF5340's supported +3 dBm, the
  assumed second SDK button alias to a project overlay, and a claimed soldered
  eSIM to unverified hardware (Nordic lists included SIM cards).
- Actual archive names differ from the requested illustrative names; unmodified
  schematic and separate base/top CAD filenames are preserved in the manifest.
- The board sources are in sdk-nrf, not sdk-zephyr; an initial lookup there returned
  404. Release tags were dereferenced to immutable commits before recording URLs.
- An initial local mutation invocation omitted the verification venv from PATH
  and could not find Ruff. This was an environment failure, not a passing probe.

- One initial mutation of the first historical-budget check was masked by the
  later projected-budget check. Added a case where the next minute recovers the
  deficit to distinguish the two requirements; the mutation is now detected.
- SDK preparation initially lacked PATH prerequisites and OpenAMP/libmetal. The
  official SDK installer required unavailable wget; the compiler archive was
  downloaded directly and checked against official hashes instead.
- Initial sysbuild failed on the checkout's space-containing path. An identical
  source copy under `/private/tmp` resolved it; build instructions record this.
- Initial linking exposed missing native TLS symbols; explicit Nordic crypto/TLS
  configuration then exposed missing key-exchange capabilities. Enabling the
  specified ECDHE/ECDSA/AES-GCM capabilities produced the successful build.

## Unverified hardware and product claims

Physical hardware/RF/BLE tests remain pending hardware delivery. No flashing,
modem registration, credential provisioning, cloud traffic or pump commands occurred.
Button/reset routing, shared peripheral ownership, watchdog timeout/reset behavior,
current consumption/SoC telemetry, BLE interoperability, Wi-Fi/LTE-M failover,
mechanical fit and real-time scheduling under load remain unmeasured. The 55%
experimental budget does not prove DKA prevention or treatment adequacy. There is
no schedule/delivery adapter, durable interlock state or validated medical device.
