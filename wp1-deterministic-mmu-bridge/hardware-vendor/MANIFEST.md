# Nordic Thingy:91 X vendor manifest

Retrieved 2026-11-16 from [Nordic Downloads](https://www.nordicsemi.com/Products/Development-hardware/Nordic-Thingy-91-X/Download).
SHA-256 values below were computed from downloaded bytes; they are integrity
records, not Nordic signatures or proof of safety. ZIP/HEX files remain outside
Git. No reference firmware was flashed, executed, provisioned or connected to a
cloud. The reference applications can transmit data when run; they are not this
project's runtime. Vendor licences remain distinct from Project LIVE's licences.

## Distribution archives (reference only)

| Package | SHA-256 | Official download |
| --- | --- | --- |
| pca20065-thingy91-x-2_0_0.zip | `616c0bc511e8bb98be50fbc0a7f046382eaaa7f7ae21c9214e4afc2ea24d91ca` | [Nordic package](https://nsscprodmedia.blob.core.windows.net/prod/software-and-other-downloads/dev-kits/thingy91-x/hardware-files/pca20065-thingy91-x-2_0_0.zip) |
| thingy91x_mfw-2.0.4_sdk-3.2.1.zip | `e2382f292b462b9c2981042b49447c5c95353425b19b12c349aa9db50d09489a` | [Nordic package](https://nsscprodmedia.blob.core.windows.net/prod/software-and-other-downloads/dev-kits/thingy91-x/application-firmware/thingy91x_mfw-2.0.4_sdk-3.2.1.zip) |
| mfw_nrf91x1_2.0.4.zip | `60a44f339d2d6d7821a0ea65418cea06499302faa49f7b08844fd803e6f550ad` | [Nordic package](https://nsscprodmedia.blob.core.windows.net/prod/software-and-other-downloads/sip/nrf91x1-sip/nrf91x1-lte-modem-firmware/mfw_nrf91x1_2.0.4.zip) |

The modem package is actually named `mfw_nrf91x1_2.0.4.zip`, supporting nRF9151;
there is no invented `mfw_nrf9151` archive here. The application bundle is based on
NCS 3.2.1 and contains Nordic's AT Client, modem and connectivity-bridge baselines.
These are references, not a working LIVE Wi-Fi/LTE failover implementation.

## Extracted hardware files, unmodified

PCA20065 hardware package **2.0.0**. [Licence](License.txt) and
[legal disclaimer](Legal_Disclaimer.pdf) accompany the redistributed extracts.
The Nordic five-clause licence restricts use to Nordic integrated circuits and
restricts reverse engineering of supplied binaries. These assets are not AGPL.

| Local file | Original archive member | SHA-256 |
| --- | --- | --- |
| [Thingy91_X_Base.step](Thingy91_X_Base.step) | `Thingy91_X - Hardware files 2_0_0/CASING/Thingy91_X_Base.step` | `17b913c02f8a6e473763216386fdc5b4ec761e15aa8139d7881035dece18a649` |
| [Thingy91_X_Top.step](Thingy91_X_Top.step) | `Thingy91_X - Hardware files 2_0_0/CASING/Thingy91_X_Top.step` | `cd0f232672c69b792f1b6d13bca2c7a986a4bbed3ed1e900b8ea61205131f378` |
| [Legal_Disclaimer.pdf](Legal_Disclaimer.pdf) | `Thingy91_X - Hardware files 2_0_0/Legal_Disclaimer.pdf` | `5d7f374471055c027a6b19aaa963acfde116801f227ac649db2f2556bb7bc4c1` |
| [License.txt](License.txt) | `Thingy91_X - Hardware files 2_0_0/License.txt` | `83fc3fb97785c73dbb5dbf436434a50d2cf35de8dcc7ec95812b268ae940a644` |
| [PCA20065_Schematic_And_PCB.pdf](PCA20065_Schematic_And_PCB.pdf) | `Thingy91_X - Hardware files 2_0_0/PCA20065-Thingy91 X Board 2_0_0/Schematic_Layout pdf files/PCA20065_Schematic_And_PCB.pdf` | `821ed72c1ac4ae1dd917ff03d458298f471f51a369b5c2f065eafcfc19c7dfeb` |

The actual schematic includes PCB drawings. The actual enclosure has separate
base/top STEP files; neither is renamed to an invented `PCA20065.step`. Use these
for future guards and clips after identifying the delivered board revision and
measuring button travel, antenna clearances and access. The older Walter SCAD
concept is retained as historical research and does not fit this target.

## SDK source snapshot

Pin: nRF Connect SDK **v3.2.1**, sdk-nrf revision
`d8887f6f32df9e958f393d3490f00b5c4ef88601`; SDK Zephyr tag `ncs-v3.2.1`
revision `ec78104f15691cccd94682cf4b22e0a013f28dd8`.
Board files live in **sdk-nrf**, not upstream Zephyr's board directory.
[Release manifest](https://github.com/nrfconnect/sdk-nrf/blob/v3.2.1/west.yml)
selects the rest of the SDK. This is a reference subset, not a standalone SDK.
Build against the complete pinned SDK; do not substitute these copies for it.
The individual headers and [SDK licence](sdk-board/LICENSE) retain Nordic terms.

| File | SHA-256 | Immutable source |
| --- | --- | --- |
| [LICENSE](sdk-board/LICENSE) | `47d92141c69e74a0166c319a41e5005ce2b87f0498e5dbd5a0c5a34f9ef63954` | [Nordic source](https://raw.githubusercontent.com/nrfconnect/sdk-nrf/d8887f6f32df9e958f393d3490f00b5c4ef88601/LICENSE) |
| [thingy91x_common.dtsi](sdk-board/thingy91x_common.dtsi) | `7bafd21dab2439267a98df4ecc04ef29d581ff3e7d410295e33158de6ae94123` | [Nordic source](https://raw.githubusercontent.com/nrfconnect/sdk-nrf/d8887f6f32df9e958f393d3490f00b5c4ef88601/boards/nordic/thingy91x/thingy91x_common.dtsi) |
| [thingy91x_nrf5340_cpuapp.dts](sdk-board/thingy91x_nrf5340_cpuapp.dts) | `64d232505b5a2866da5d98ab231aa0b832829dc2b9848345c1c1eb2e36f308b8` | [Nordic source](https://raw.githubusercontent.com/nrfconnect/sdk-nrf/d8887f6f32df9e958f393d3490f00b5c4ef88601/boards/nordic/thingy91x/thingy91x_nrf5340_cpuapp.dts) |
| [thingy91x_nrf5340_cpuapp_common-pinctrl.dtsi](sdk-board/thingy91x_nrf5340_cpuapp_common-pinctrl.dtsi) | `874aeea20c33036bc00261941db9a7584480e5c1685c255b1da2cf835b454637` | [Nordic source](https://raw.githubusercontent.com/nrfconnect/sdk-nrf/d8887f6f32df9e958f393d3490f00b5c4ef88601/boards/nordic/thingy91x/thingy91x_nrf5340_cpuapp_common-pinctrl.dtsi) |
| [thingy91x_nrf5340_cpuapp_common.dtsi](sdk-board/thingy91x_nrf5340_cpuapp_common.dtsi) | `0b195ee21a1e60c4deb7835fc7907618c2f47346144c30b079d5524aa6000daf` | [Nordic source](https://raw.githubusercontent.com/nrfconnect/sdk-nrf/d8887f6f32df9e958f393d3490f00b5c4ef88601/boards/nordic/thingy91x/thingy91x_nrf5340_cpuapp_common.dtsi) |
| [thingy91x_nrf5340_cpuapp_ns.dts](sdk-board/thingy91x_nrf5340_cpuapp_ns.dts) | `938bc2e37561bd399ab6f41e38e8f798f00902f6be546e8c5f27aa82cf9fa2e6` | [Nordic source](https://raw.githubusercontent.com/nrfconnect/sdk-nrf/d8887f6f32df9e958f393d3490f00b5c4ef88601/boards/nordic/thingy91x/thingy91x_nrf5340_cpuapp_ns.dts) |
| [thingy91x_nrf5340_cpunet.dts](sdk-board/thingy91x_nrf5340_cpunet.dts) | `41d1301deb6bd16f31ea97107b68733a419bef6170279010a167a23249eb49a8` | [Nordic source](https://raw.githubusercontent.com/nrfconnect/sdk-nrf/d8887f6f32df9e958f393d3490f00b5c4ef88601/boards/nordic/thingy91x/thingy91x_nrf5340_cpunet.dts) |
| [thingy91x_nrf9151.dts](sdk-board/thingy91x_nrf9151.dts) | `65461ba32f3af6a90811348ac041d1ecacb941bcb978a42d695f0b3824d5da0c` | [Nordic source](https://raw.githubusercontent.com/nrfconnect/sdk-nrf/d8887f6f32df9e958f393d3490f00b5c4ef88601/boards/nordic/thingy91x/thingy91x_nrf9151.dts) |
| [thingy91x_nrf9151_common-pinctrl.dtsi](sdk-board/thingy91x_nrf9151_common-pinctrl.dtsi) | `e8ffd24f48ecbae19b121213f89252594e731f6a66b40b6b7e8fd48ec929aab1` | [Nordic source](https://raw.githubusercontent.com/nrfconnect/sdk-nrf/d8887f6f32df9e958f393d3490f00b5c4ef88601/boards/nordic/thingy91x/thingy91x_nrf9151_common-pinctrl.dtsi) |
| [thingy91x_nrf9151_common.dtsi](sdk-board/thingy91x_nrf9151_common.dtsi) | `d88de029a4cb61cd469716119390dfeb16cb9e5561e77c615ed68591bef926be` | [Nordic source](https://raw.githubusercontent.com/nrfconnect/sdk-nrf/d8887f6f32df9e958f393d3490f00b5c4ef88601/boards/nordic/thingy91x/thingy91x_nrf9151_common.dtsi) |
| [thingy91x_nrf9151_ns.dts](sdk-board/thingy91x_nrf9151_ns.dts) | `bf1fbc2db93c57324381e806adc1bf4bda228d0579208536c52572d760570116` | [Nordic source](https://raw.githubusercontent.com/nrfconnect/sdk-nrf/d8887f6f32df9e958f393d3490f00b5c4ef88601/boards/nordic/thingy91x/thingy91x_nrf9151_ns.dts) |

## Project overlay and routing

[The app overlay](overlays/thingy91x_nrf5340_cpuapp.overlay) is authored by this
project (AGPL-3.0-only), not manufacturer-certified routing. Git tracks changes;
the source snapshots above remain byte-for-byte vendor evidence.

| Signal | SDK evidence and use |
| --- | --- |
| app-core `sw0` | SDK Button 2, P0.24, active low; 60-minute research carb guard |
| app-core `sw1` | Added alias for P1.15, SDK `zephyr,user/button1-gpios`; input only, 180-minute research concert guard |
| nRF9151 `sw0` | SDK Button 1, P0.26; aliases are processor-relative, not interchangeable |
| `watchdog0` | app-core `wdt0`, enabled in overlay; requested 10-second timeout |
| nPM1300 | `pmic_main` on I2C2; nRF9151 common DTS enables PMIC/charger; app-side nodes disabled by default |
| nRF7002 | `nrf70` on SPI3, board-specific control/IRQ GPIOs; disabled by default |
| nRF9151 | Separate processor target `thingy91x/nrf9151/ns`; modem integration needs its own application/IPC contract |

Do not equate silkscreen SW1/SW2, physical Button 1/2 and Zephyr aliases. In
particular, board power/debug switches are not two dedicated preemption buttons.
Shared button/reset behavior with the other processor's firmware must be tested
before use. No app-side PMIC ownership, fuel-gauge telemetry or Wi-Fi driver is
claimed by merely importing a DTS file.
