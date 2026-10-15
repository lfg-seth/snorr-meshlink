# Stock RAK pilot repeaters

Prepared 2026-10-14 at the owner's request, using two connected on-hand RAK4631s. This is bench preparation for the existing Meshtastic pilot, not installation approval or field acceptance. Custom survey firmware remains deferred.

| Label | Current Windows port | Meshtastic ID | Stock firmware |
| --- | --- | --- | --- |
| R001 | COM8 | `!a65601b3` | `2.7.26.54e0d8d` |
| R002 | COM9 | `!b456f760` | `2.7.26.54e0d8d` |
| R003 | COM14 | `!05237743` | `2.7.26.54e0d8d` |

Ports can change; verify hardware identity before writing settings. Physically label the boards R001/R002 before separating them. Owner confirms suitable 915 MHz antennas attached. Exact antenna model/gain, radio frequency SKU markings, fitted sensors and battery assembly are not independently inspected.

## Saved bench profile

- Role `ROUTER`, keeping infrastructure visible in the node list; `LOCAL_ONLY` rebroadcast to limit forwarding to decryptable local channels. The human repeater label does not require the deprecated firmware `REPEATER` role. Node information interval 10,800 seconds.
- Exact private `SNORRbench` channel/key copied from verified G001, with other channels disabled. Both channel uplink and downlink disabled on the RAKs. Keys and complete exports stay in ignored `private/bench/`.
- US region, `LONG_FAST` preset (250 kHz, SF11, CR 4/5), explicit frequency slot 35, hop limit 3, transmit enabled at 10 dBm, receive boosted gain enabled. Matches the current bench radio profile except that gateways remain transmit-disabled. This is a low-power bench baseline; site antenna/power selection and compliance review remain separate.
- Ignore MQTT-originated packets; forwarding consent matches the pilot. RAK MQTT and Wi-Fi disabled; no broker credentials installed. Neither RAK replaces a V3 backhaul.
- Old fixed positions cleared; fixed-position mode off and GPS disabled. No invented site coordinates or verified GPS hardware. Configure an actual location deliberately before deployment. Position interval 21,600 seconds does not create a valid position.
- Device telemetry explicitly enabled (`device_telemetry_enabled=true`) with interval 900 seconds. The initial setup saved only the interval and missed the enable flag; corrected on both boards and independently verified after configuration reboot on 2026-10-14. Stock device metrics include battery voltage and battery level; charging/no-battery status uses level 101 rather than a percentage. Actual battery-voltage calibration and periodic RF delivery remain unmeasured. Environmental/air-quality measurements disabled pending identified hardware. No solar, current-sensor, intrusion or runtime result implied. Portal telemetry ingestion remains unimplemented.
- Power-saving flag off for continuous relay reception. USB bench power used; battery chemistry, cell count/capacity, pack arrangement, solar charging and endurance remain unknown.
- Serial administration retained, Bluetooth configured for random PIN, legacy admin keys/channel removed, fresh device keypairs after full reset. Keep exported private keys out of Git.

## Installation and recovery evidence

Both originally ran older `2.7.17` builds and prior SNORR profiles. Save private before-state exports before reset. Both report WisBlock RAK4631 bootloader `0.4.3`, SoftDevice S140 `6.1.1`.

Official [release package](https://github.com/meshtastic/firmware/releases/tag/v2.7.26.54e0d8d): `firmware-nrf52840-2.7.26.54e0d8d.zip`, SHA256 `69ae5c1f38474e32d815dc8bc54291944fb1eb2bf0c3bd0abf5513cb078de5b2`, matched against GitHub's release asset digest. Exact standard target `firmware-rak4631-2.7.26.54e0d8d.uf2`, SHA256 `34fb3710683494aec9cf7b999a324ac9247beb649549fb7ac19cba9ddb3e8e1b`.

UF2 installation followed by full configuration/Bluetooth reset left both normal serial APIs timing out. A 1200-baud serial touch exposed Nordic serial recovery ports COM12/COM13; the matching official `firmware-rak4631-2.7.26.54e0d8d-ota.zip` successfully reinstalled the stock application using `adafruit-nrfutil 0.5.3.post16`. Both normal APIs then returned. No bootloader update or hardware programmer was used. The precise cause of the post-reset timeout is unresolved; successful recovery does not identify it.

Stock firmware applies role defaults when changing to `ROUTER`, overriding the initial rebroadcast/telemetry choices. Apply the role first, reconnect, then apply the explicit profile again. Independent readback must verify actual values after reboot rather than assuming the first transaction retained them. Private verification confirms fresh keypairs, cleared old admin keys/locations, firmware, role, radio/channel equality and the profile above on both boards.

References: official [RAK4631 target](https://meshtastic.org/docs/hardware/devices/rak-wireless/wisblock/core-module/?rakcore=RAK4631), [role behavior](https://meshtastic.org/docs/configuration/radio/device/), [nRF52 recovery methods](https://meshtastic.org/docs/getting-started/flashing-firmware/nrf52/update-nrf52-bootloader/). Exact role default behavior was checked in pinned [NodeDB.cpp](https://github.com/meshtastic/firmware/blob/54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb/src/mesh/NodeDB.cpp).

## Next checks

See [TEST-006](../../records/field-results.md#test-006--stock-rak-pilot-repeater-preparation). Direct bench reception does not establish a forced relay path. Next reconnect a GPS-equipped V4, isolate direct reception so each RAK is demonstrably required in turn, and verify original GPS measurement timestamps through both V3 gateways and the portal. Then test internet loss/local viewing, sustained freshness and the actual battery/solar assembly before site placement.

## R003 environmental sensor follow-up — 2026-10-14

Owner connects a third on-hand RAK, labels it R003, confirms its antenna, and tentatively identifies its temperature sensor as **AHT21 at 0x38**. Sensor model/wiring are not independently inspected. This prepares another board; the original two-repeater field allocation is not automatically expanded.

R003's older `2.7.17.36133d29d` settings are backed up privately. Full reset followed by 1200-baud entry exposes COM15 Nordic recovery; install the same official stock `firmware-rak4631-2.7.26.54e0d8d-ota.zip`. Normal identity remains COM14/`!05237743`. Apply the matching pilot profile twice to account for role defaults. Independent full readback passes, including fresh keys, cleared fixed position/admin keys and matching radio/channel settings. Device telemetry and environmental measurement are explicitly enabled at **900 seconds** each. Unrelated power/air-quality/health sensor options are cleared; displayed-temperature preference reset to Celsius. Brief private USB debug collection is restored to disabled afterward.

Both receive-only V3s receive R003's automatic device metrics, including reported voltages **4.259 V** and **4.278 V** in two startup samples; level 101 reports charging/external-power/no-battery status rather than 101%. These are firmware-reported readings, not meter-verified battery voltages. No temperature or humidity is returned in gateway observation or the short local sensor request/observation. Do not claim environmental reporting works.

Pinned-source explanation: standard RAK4631 [variant.h](https://github.com/meshtastic/firmware/blob/54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb/variants/nrf52840/rak4631/variant.h) defines `HAS_NCP5623`. [ScanI2CTwoWire.cpp](https://github.com/meshtastic/firmware/blob/54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb/src/detect/ScanI2CTwoWire.cpp) then includes NCP5623 LED-controller detection and compiles out the AHT sensor case behind `#ifndef HAS_NCP5623`. The [AHT driver](https://github.com/meshtastic/firmware/blob/54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb/src/modules/Telemetry/Sensor/AHT10.cpp) would otherwise supply temperature and relative humidity through Adafruit AHTX0. This stock-target exclusion explains why merely enabling telemetry cannot activate the owner's reported AHT sensor. It does not independently prove its wiring, precise AHT21 model or driver compatibility.

Keep stock firmware as requested. Environmental enable remains saved, but actual AHT reporting requires a separately authorized firmware compatibility change or a compatible sensor choice. Neither a custom build, sensor replacement, portal telemetry implementation nor purchase was performed. [TEST-007](../../records/field-results.md#test-007--r003-stock-setup-and-environmental-sensor-limit).
