# Hardware inventory

## 2026-10-25 - R005 ordinary firmware and three-minute reporting

Existing **R005 `!f95b5501`**, USB **`E93C5FF0F97DD76B`**, COM19, moves from
`2.7.26.0b65f2e` to verified ordinary **rak4631 / 2.7.26.4c96b9b**. Complete
intended profile/keys/private channel persist through explicit reboot: CLIENT,
device and existing environment telemetry enabled at **180 seconds**,
power telemetry disabled, over-LoRa SNNS using the saved 180-second baseline.
The prior removal from active portal inventory remains in effect; this radio
update does not restore a server record or establish a field assignment. No
sensor, stock quantity, site, battery/antenna allocation or purchase change.
[Image, profile, delivery and limits](../docs/operations/r005-three-minute.md).

## 2026-10-25 - R001 ordinary firmware and three-minute reporting

Existing **R001 `!a65601b3`**, USB **`AA474A4710B85C2C`**, COM8, moves from
`2.7.26.0b65f2e` to verified ordinary **rak4631 / 2.7.26.4c96b9b**. Complete
intended profile/keys/private channel persist through explicit reboot: CLIENT,
device and existing environment telemetry enabled at **180 seconds**,
power telemetry disabled, over-LoRa SNNS using the saved 180-second baseline.
No sensor, stock quantity, site, battery/antenna allocation or purchase change.
[Image, profile, delivery and limits](../docs/operations/r001-three-minute.md).

## 2026-10-25 - R003 ordinary firmware and three-minute reporting

Existing **R003 `!05237743`**, USB **`397EBE4F36E1F126`**, COM14, moves from
`2.7.26.0b65f2e` to verified ordinary **rak4631 / 2.7.26.4c96b9b**. Complete
intended profile/keys/private channel persist through explicit reboot: CLIENT,
device and existing environment telemetry enabled at **180 seconds**,
power telemetry disabled, over-LoRa SNNS using the saved 180-second baseline.
No sensor, stock quantity, site, battery/antenna allocation or purchase change.
[Image, profile, delivery and limits](../docs/operations/r003-three-minute.md).

## 2026-10-24 - B002 latest firmware and three-minute reporting

Existing original OLED V4 **B002 `!699ca878`**, USB
**`90:70:69:9C:A8:78`**, COM4, now runs selected
**heltec-v4-gateway / 2.7.26.a56466d** from published source **`a56466d8c`**.
Application digest and complete intended member profile/identity/keys pass
through explicit reboot. Device telemetry is enabled at **180 seconds**;
over-LoRa SNNS follows the same saved baseline with jitter/admission. Preserve
CLIENT, private RF/channel settings, 10 dBm configured TX power/FEM, disabled
Wi-Fi/MQTT and GPS acquisition/reporting at **60/120 seconds**. External
environment/power reporting remains disabled. Existing 3000 mAh LiPo/no-solar
allocation and stock totals are unchanged. This supersedes B002's historical
stock-firmware state below. [Image, backup, profile and delivery evidence](../docs/operations/b002-three-minute.md).

## 2026-10-24 - R004 battery and solar allocation

Owner confirms **R004 has four standard EVE 18650 cells and one solar panel**.
Live metadata now uses `eve-26v-1s`, the confirmed cell/panel counts and solar
equipment present. This supersedes R004's unknown allocation below. Total pack
capacity remains unset pending wiring confirmation; panel electrical ratings,
sensor calibration and runtime remain unverified. No stock-total or purchase
change inferred.

Private consistent pre-update backup:
`/var/lib/meshlink/private-inventory-updates/20261024T185832Z/before.db`.
Authenticated portal snapshot verifies the profile, four-cell description and
one-panel description. Preserve all other R004 configuration. No radio,
firmware, deployment or demo change.

## 2026-10-24 - Active-device battery and solar allocations

Owner decommissions **B001** and **R005** and requests removal. Their active
portal device records are removed; historical observations, positions,
assignments and raw MQTT archive remain stored. B001's board was reassigned
to G004 as recorded below; decommissioning the old B001 label does not remove
the replacement G004. R005's physical disposition is unspecified; no stock
count, disposal, purchase or valuation is inferred.

Owner confirms these allocations, now reflected in live portal metadata:

| Device | Battery | Solar |
| --- | --- | --- |
| B002 | 3000 mAh LiPo; `lipo-1s` | None |
| G003 | 8 standard EVE 18650 cells; `eve-26v-1s` | 1 large 5 V panel |
| G004 | 4 standard EVE 18650 cells; `eve-26v-1s` | 2 panels |
| R006 | 4 standard EVE 18650 cells; `eve-26v-1s` | 1 panel |

Interpret the owner's 18650 shorthand using the existing standard EVE cell
inventory/profile. The known EVE 26V reference is 2550 mAh per cell; total
pack capacity remains unset pending confirmation of wiring. Panel ratings
beyond G003's stated 5 V, output, charging path, sensor accuracy and measured
runtime remain unverified. Solar equipment flags record fitted hardware,
not a measured solar input. This supersedes earlier unknown/planned allocations
for these devices. R004's battery allocation remains unknown.

Before mutation, take a consistent root-private database backup at
`/var/lib/meshlink/private-inventory-updates/20261024T185016Z/before.db`.
Independent authenticated portal snapshot confirms updated profiles and
absence of B001/R005; history-table counts do not decrease. No firmware,
radio settings, source deployment or demo-state change.

2026-10-24 R002 ordinary firmware / confirmed INA219 - Owner confirms existing
R002 **`!b456f760`**, USB **`BADB1E79E9739FC4`**, COM9, also has an **INA219**.
This supersedes its earlier no-INA219 bench sensor selection, without adding
stock or inferring a purchase. Verified ordinary **rak4631 / 2.7.26.4c96b9b**
replaces `2.7.26.0b65f2e`; complete original-profile equality passes after flashing.
Full intended profile/keys/channel/radio settings persist through explicit
reboot: CLIENT, enabled device/environment/**INA219 power** at **180 seconds**,
over-LoRa SNNS using the saved 180-second baseline, separate standard
NeighborInfo at 21,600 seconds. Existing temperature telemetry stays enabled;
actual fresh environment packets contain INA219 voltage/current, with no
temperature/humidity fields. Fresh channel-1 power **4.068 V / -229.2 mA**
reaches both gateways; physical path/calibration remain unverified.
Battery-INA address remains unset. No site, battery/antenna allocation,
stock quantity or purchase change inferred.
[Image, sensor delivery and limits](../docs/operations/r002-three-minute.md).

2026-10-24 R004 ordinary firmware / INA219 telemetry - Reconnected existing
**`!77fdb9f1`**, USB **`820C9B4F0C2D7675`**, COM17, replaces diagnostic
`2.7.26.09d8a9d` with verified ordinary **rak4631 / 2.7.26.4c96b9b** at the
owner's request. Complete intended profile/keys/channel/radio settings persist
through explicit reboot: CLIENT, enabled device/environment/**INA219 power**
telemetry at **180 seconds**, over-LoRa SNNS with saved 180-second baseline,
separate standard NeighborInfo at 21,600 seconds. INA219 initializes/opens.
Historical temperature sensor remains enabled; no sensor removal is inferred.
Accuracy, physical bridge state, battery-only behavior and runtime remain
unverified. No stock quantity, purchase, site or equipment allocation change.
[Exact image, delivery and limits](../docs/operations/r004-three-minute.md).

2026-10-24 G004 disconnected / owner hold - Owner disconnects G004
**`!849ae664`** pending hardware investigation and closes the chat. Retain the
verified firmware installation and failed configuration evidence below. The
board is not commissioned as a working gateway/time source. No additional
hardware change, stock count or purchase is inferred; resume bench work only
when the owner brings it forward.

2026-10-24 G004 application installation / power hold - Independently identify
the owner's V3/INA219/GT-U7 assembly on COM6 as ESP32-S3 v0.2 / 8 MB, MAC
`b0:81:84:9a:e6:64`, node **`!849ae664`**, hardware ID
`74bdf87af2ebb4a61d657eb19bf72422`. Application-only installation and independent
verification of **heltec-v3-gateway / 2.7.26.4c96b9b** pass; boot/partition/old
OTA/filesystem retained. INA219 is detected at **0x40**. Owner requests G003's
profile plus GPS RX45/TX46 and RF TX, but five logged **brownout resets**
interrupt configuration. Full-profile verification fails: only G004's name
persists; region/GPS/network/telemetry remain unprovisioned in last readback.
Do not treat this as a working gateway or mesh time source. Await stable power
and another saved-profile/reboot check, then GPS/telemetry/time-transfer tests.
GPS operation, supply fault, battery, antenna/site and sensor path remain
unverified. No new stock or purchase inferred. [Evidence and next check](../docs/operations/g004-gps-time.md#commissioning-attempt---2026-10-24).

2026-10-24 G004 owner-reported assembly - Owner assigns another Heltec V3
with **INA219 and GT-U7 GPS** to **G004**, for mesh time supporting telemetry;
location is not needed for its application role. Clarified wiring is **GT-U7
TX → GPIO45, GT-U7 RX → GPIO46**, corresponding to MCU GPS RX=45/TX=46.
This supersedes the earlier blanket statement that no V3 has GPS. Hardware
identity, installed firmware, GPS operation/baud, power wiring, INA219 address
and measurement path, battery, antenna and site remain unverified. Retain the
last confirmed nine-V3 total; this report does not establish a purchase or an
additional stock count. [Source review and bench follow-up](../docs/operations/g004-gps-time.md).

2026-10-24 G003 commissioning - Owner assigns the attached Heltec V3 with
INA219 **G003**, independently identified as ESP32-S3 revision v0.2 / 8 MB,
MAC `9c:13:9e:9f:16:7c`, Meshtastic **`!9e9f167c`**, hardware device ID
`4393827189e95c03021dd7b37007a6a0`. The original Heltec factory demo is fully
backed up before first installation of dedicated **heltec-v3-gateway /
2.7.26.4c96b9b**. All installed images verify; complete intended profile/new
PKI identity persists through explicit reboot. CLIENT, receive-only private
pilot/Wi-Fi/MQTT, enabled **180-second device and INA219 power telemetry**,
environment off and local-only neighbor collector. INA219 is detected at
0x40 on the external I2C bus. Pack/capacity, physical measurement path,
shunt/polarity/calibration, antenna and site remain unverified. This assigns
an existing connected board; no purchase or change to stock totals is inferred.
[Installation, delivery evidence and limits](../docs/operations/g003-gateway-preparation.md).

2026-10-24 saved-interval bench - Existing R006 `!da581e5f` receives ordinary
`rak4631 / 2.7.26.4c96b9b`; G001 `!9ea13cc0` and G002 `!849ad7a0` receive
dedicated `heltec-v3-gateway / 2.7.26.4c96b9b`, all from reviewed source
`4c96b9ba0`. Application-only writes and independent complete original
identity/key/channel/local/module comparison pass through reboot. Both V3s
remain CLIENT/TX disabled/local-only with individual Wi-Fi/MQTT profiles;
G001 device telemetry stays disabled, G002 stays enabled at 300 seconds.
B002 `!699ca878` is the existing original V4 controller on unchanged stock
`2.7.26.54e0d8d`. R006 retains INA219-only and intended 180-second device/power
settings. No purchase, quantity, antenna, sensor or pack allocation change.
[Images, preservation and bench evidence](../docs/operations/repeater-update.md#r006-and-gateway-admin-bench---2026-10-24).

2026-10-23 planned gateway outdoor configuration - Owner retains Heltec V3
and selects INA219 sensing and a Muzi whip antenna. Per-gateway battery option
is **four or eight 18650 cells**; solar option is **two 60 x 100 mm panels** or
an external larger **5 V USB solar charger advertised as 6 W**. These are design
requirements/alternatives, not installed allocations or new stock counts.
Exact models, capacities, pack topology/protection/charging path, panel output,
antenna specifications and quantities on hand remain unverified. The last
confirmed G001/G002 installed packs remain one 1000 mAh LiPo each until a
physical change is recorded. No purchase, cost, measured power or runtime is
inferred. Custom 3D-printed enclosure and Wi-Fi/solar characterization are
planned in [LOCAL-4](../.scratch/pilot/issues/26-gateway-production-readiness.md).
[Hardware documentation](../docs/hardware/README.md).

2026-10-23 R006 three-minute update - Existing RAK19003/RAK4631 **R006
`!da581e5f`**, hardware `b8bc8fa95c2cb1e95f1e58dafebb06cc`, USB
`E9B12C5CA98FBCB8`, now runs ordinary **rak4631 / 2.7.26.0634b77** from the
explicitly verified unpublished local bundle. Corrected native Windows UF2
update and full intended owner/key/channel/local/module profile equality pass
through explicit reboot at **2026-10-24T00:51:19Z**. CLIENT, device/power
telemetry **180 seconds**, environmental reporting disabled, private SNNS
compiled at 180 seconds and standard NeighborInfo 21,600 seconds. Retain
**INA219 only/no temperature sensor**. The initial serial-only DFU attempt
stopped before an application write; verified application-only serial OTA
recovery precedes the successful corrected UF2 retry. Independent comparison
also preserves the entire original profile/identity/keys/channels across
recovery, with only intended final changes. Serial closed; three automatic
device/power/SNNS cycles reach both gateways, with device/power measurement
gaps 180/180 s and SNNS 195/195 s including jitter. Portal acceptance remains
unverified. R001–R005 unchanged/unconnected; battery allocation,
current calibration and map placement remain unverified. No purchase, stock
quantity or fitted-hardware change. [Image and acceptance](../docs/operations/repeater-update.md#r006-installed-verification).

2026-10-23 R006 commissioning - Owner assigns the fresh RAK19003/RAK4631
assembly **R006**, with **INA219 only and no temperature sensor**. Identity
`!da581e5f`, hardware ID `b8bc8fa95c2cb1e95f1e58dafebb06cc`, USB
`E9B12C5CA98FBCB8`. Ordinary `rak4631` **2.7.26.09d8a9d** replaces the
diagnostic image; CLIENT pilot profile, device and power telemetry at 900
seconds, environmental reporting off. Initial PKI keys are created from the
previously keyless UNSET profile and persist through reboot. 18650 source
count/capacity/arrangement, antenna and site remain unconfigured; shunt polarity
and independent accuracy remain unverified. No purchase or stock-total change
inferred. [Production preparation](../docs/operations/ina219-audit.md#r006-production-preparation--2026-10-23).

2026-10-23 fresh INA219 bench assembly - Owner confirms a brand-new RAK19003/RAK4631 and INA219 inline with the 18650 battery, currently USB-powered and charging. Device identifies as `!da581e5f`, default short name `1e5f`, USB serial `E9B12C5CA98FBCB8`; **R006 remains provisional and is not assigned**. Original firmware **2.7.15.567b8ea** is replaced with diagnostic `rak4631-ina219-debug` **2.7.26.09d8a9d**, verified by device version readback. Owner reports approximately **280 mA at 5 V** on the USB input meter, a separate measurement path from the battery-inline sensor. Exact shunt value, polarity, carrier revision and calibrated current accuracy remain unverified. Relationship to previously inventoried stock is unknown; no purchase, cost or stock-total change inferred. [Diagnostic evidence](../docs/operations/ina219-audit.md#fresh-rak190034631-comparison--2026-10-23).

2026-10-21 G002 second Wi-Fi replacement - Existing HELTEC_V3 `!849ad7a0`, COM6, retains **2.7.26.9d2fd8f** and enabled five-minute telemetry. Exact independent full profile comparison shows only the owner-requested Wi-Fi SSID differs; supplied password already matches. IP acquisition/MQTT connection and publication activity observed. LoRa TX remains disabled; quantities and other boards unchanged. [Evidence and limits](../docs/operations/g002-neighbor-gateway.md#clifford-int24-wi-fi-update---2026-10-21).

2026-10-21 gateway batteries - Owner confirms **G001 and G002 each have one installed 1000 mAh LiPo**. This supersedes the prior unspecified gateway pack allocation and earlier 1100 mAh description for these two packs. Preserve the previously reported total of six small V3 packs; no purchase or additional stock inferred. Both portal records now independently verify `lipo-1s`, 1000 mAh and the owner-confirmed pack description. G002 battery cadence is five minutes; G001 still has no battery reports and no cadence inferred. Remaining pack labels, actual capacity, calibration and runtime are unverified. [Graph investigation and deployment](../docs/operations/gateway-battery-graphs.md).

2026-10-21 R004 INA219 diagnosis - Owner confirms installed R100 and battery → INA219 → RAK placement on existing R004 `!77fdb9f1` / USB `820C9B4F0C2D7675`, COM17. Authorized diagnostic target `rak4631-ina219-debug` **2.7.26.09d8a9d** is flashed; independent full identity/key/channel/local/module profile comparison passes. Device/environment remain 900 seconds, power telemetry disabled, battery INA address unset. Sensor at 0x40 uses the correct 0.1-ohm calibration; first held conversion repeats −40.09 mV / −400.9 mA exactly. Physical voltage/current accuracy, polarity, other branches and cause of conversion variation remain unverified. No stock quantity/purchase change. [Audit and image evidence](../docs/operations/ina219-audit.md#r004-reinvestigation--2026-10-21).

2026-10-21 G002 device telemetry - Owner enables five-minute device reports on existing HELTEC_V3 `!849ad7a0`, COM6, unchanged **2.7.26.9d2fd8f**. Independent profile comparison confirms only telemetry enablement/300-second interval change. LoRa TX remains disabled; first **4.25 V** report reaches production observations. G001 and hardware quantities unchanged. [Evidence/limits](../docs/operations/g002-neighbor-gateway.md#five-minute-device-telemetry-enabled---2026-10-21).

2026-10-21 G002 Wi-Fi replacement ? Existing HELTEC_V3 `!849ad7a0` independently identifies on COM6, unchanged **2.7.26.9d2fd8f**. Owner-supplied Wi-Fi saved; complete private profile comparison confirms only requested network fields change. Console obtains IP, connects MQTT and publishes a queued message. Quantities unchanged. [Evidence and limits](../docs/operations/g002-neighbor-gateway.md#wi-fi-replacement--2026-10-21).

2026-10-19 G001 gateway collector — Existing Heltec V3 `!9ea13cc0`, now COM6 / ESP32-S3 / 8 MB, receives the same checksum-verified `heltec-v3-gateway` **2.7.26.9d2fd8f** application already used on G002. Complete board-specific profile/full-flash backup, partition/app hash checks and full intended identity/key/profile equality pass through explicit reboot. Preserve CLIENT, LoRa TX disabled and existing Wi-Fi/MQTT; enable local-only neighbor collection. Fresh G001-originated three-row RSSI/SNR/hearing-age/count report is accepted by the portal and matches authenticated state. Both gateways now run the collector; G002/MC00 untouched during this run, quantities unchanged. [Evidence and limits](../docs/operations/g001-neighbor-gateway.md).

2026-10-19 G002 gateway collector — Existing Heltec V3 `!849ad7a0`, COM6 / ESP32-S3 / 8 MB flash, is updated from stock `2.7.26.54e0d8d` to dedicated `heltec-v3-gateway` **2.7.26.9d2fd8f**. Complete profile/full flash backed up privately; app-only flash/hash verification and full identity/key/channel/intended-profile preservation pass through reboot. CLIENT and LoRa TX disabled, neighbor collector enabled/local-only, owner-authorized replacement Wi-Fi saved; MQTT unchanged. G002's own five-row RSSI/SNR/hearing-age/count report reaches MQTT/archive/normalized portal, alongside correctly deduplicated repeater copies. G001 and MC00 unchanged; hardware quantities unchanged. [Evidence and limits](../docs/operations/g002-neighbor-gateway.md).

2026-10-19 R005 bench reflash — Existing RAK4631 `!f95b5501` changed from one-off dummy-load `2.7.26.8dd4dac` to ordinary verified neighbor-signal release `2.7.26.0b65f2e`, removing the GPIO31 HIGH startup override. CLIENT, device/environment 900-second telemetry, disabled power measurements/display and unconfigured battery INA address pass independent readback through explicit reboot. Identity/keys/channel/radio profile/Fahrenheit preference preserved. Physical load/sensor removal and current draw remain unverified; no inventory quantity or resolution of historical power discrepancies inferred. Other radios/live portal metadata unchanged. R001–R005 now share the requested release/CLIENT/temperature measurement policy. [Evidence](../docs/operations/r005-client-bench.md).

2026-10-19 R004 bench reflash — Existing RAK4631 `!77fdb9f1` reflashed with verified released neighbor-signal firmware `2.7.26.0b65f2e`. CLIENT, device/environment 900-second telemetry, disabled power measurements/display and unconfigured battery INA address pass independent readback through explicit reboot. Preserve identity/keys/channel/radio profile and existing Fahrenheit preference. This supersedes historical enabled INA219/power configuration; physical sensor removal/model/calibration remain unverified, and no stock change or resolution of current discrepancy is inferred. Other radios/live portal metadata unchanged. [Evidence](../docs/operations/r004-client-bench.md).

2026-10-19 R003 bench reflash — Existing RAK4631 `!05237743` upgraded from AHT image `2.7.26.cc5907b` to released neighbor-signal firmware `2.7.26.0b65f2e`, retaining AHT support. CLIENT, device/environment 900-second telemetry, disabled power measurements/display and unconfigured battery INA address pass independent readback through explicit reboot. Identity/keys/channel/radio profile preserved. Temperature sensor model/calibration remain unverified; historical readings are separate from this run. Other radios, stock quantities and live portal metadata unchanged. [Evidence](../docs/operations/r003-client-bench.md).

2026-10-19 R002 bench reflash — Owner connects R002 RAK4631 `!b456f760` and requests the same CLIENT/temperature-only profile as R001. Verified released neighbor-signal firmware `2.7.26.0b65f2e` reflashed; CLIENT and device/environment 900-second telemetry persist through reboot, power telemetry disabled and battery INA address unconfigured. Complete identity/keys/channel/radio profile preserved. Requested temperature configuration supersedes the earlier no-external-sensor profile; physical sensor/model/calibration remain unverified. Other radios, stock quantities and live portal metadata unchanged. [Evidence](../docs/operations/r002-client-bench.md).

2026-10-19 bench profile update — Owner requests temperature sensors only and no INA219 configuration across the repeater reflash rollout. R001 RAK4631 `!a65601b3` now runs released `2.7.26.0b65f2e` as **CLIENT**, with device/environment telemetry at 900 seconds and power telemetry disabled; identity/keys/channel persist through reboot. Other repeaters are unchanged pending individual connection/update. This records the requested current configuration and owner-reported temperature-only equipment scope; it does not establish physical removal/disposal of historically fitted INA219 boards or change stock quantities. [Evidence](../docs/operations/r001-client-bench.md).

2026-10-16 shunt inspection — Owner reports removing an R100 sensor shunt, measuring 0.45 Ω out of circuit and then 0.16 Ω with the probes shorted on the same range. Estimated difference is 0.29 Ω; actual shunt resistance remains uncalibrated because meter/contact uncertainty is unknown. Exact sensor/board allocation and reinstallation remain unconfirmed. Record an altered sensor assembly without changing stock/purchase totals. [INA219 audit](../docs/operations/ina219-audit.md).

2026-10-16 INA219 audit — Owner confirms R100 shunt markings and reports a desk-multimeter battery-only R004 draw of 8–16 mA, despite roughly one amp reported by the sensor. R100 is compatible with the RAK driver's 0.1 Ω calibration. Fresh USB-connected R004 readings are −5.9/−5.8 mA; these are different supply conditions, not a calibration result. [Audit and source fix](../docs/operations/ina219-audit.md). No stock, purchase, wiring or fitted-board allocation change inferred.

2026-10-16 R005 power-check follow-up — Owner replaces the disconnected battery assembly with one reportedly fully charged cell and inserts a USB input meter reading 0.08 A. Cell chemistry/capacity and allocation from existing stock remain unspecified; no purchase or quantity change. Total USB input is separate from INA219 branch current and does not establish dummy-load draw. [Readings](../docs/operations/r005-preparation.md#sensor-evidence).

2026-10-16 R005 allocation — Fifth undamaged on-hand RAK identifies as RAK4631 `!f95b5501`, hardware ID `6bd77df9f05f3ce901555bf96d5ed7fc`, COM19/USB serial `E93C5FF0F97DD76B`. Owner reports RAK19007, temperature sensor, INA219, and a dummy load controlled by AIN1 through a 2 kΩ resistor to a 2N2222 base. Owner says the load runs through the INA219 and expects roughly 50 mA; this is an expectation, not a measurement. One-off firmware `2.7.26.8dd4dac` asserts GPIO31 HIGH at normal startup. Profile/keys persist through reboot; live database registration shares R001's private planned location. Total stock unchanged: five prepared, two undamaged on-hand units remain untested, one damaged carrier, plus two remotely deployed. Exact battery/antenna/solar assembly, sensor model/calibration and physical load current remain unverified. [Evidence](../docs/operations/r005-preparation.md).

2026-10-16 R002 update — Owner confirms no external sensors. Identity-checked RAK4631 `!b456f760` (COM9) now runs verified released `2.7.26.0b65f2e`; all original local settings/channels/owner/keys survive explicit reboot. Device battery telemetry remains enabled at 900 seconds; environment/power/air-quality/health measurements are disabled and neighbor transmission enabled. Portal firmware/no-sensor metadata updated; quantities and planned location/equipment preserved. [Evidence](../docs/operations/r002-release-update.md).

2026-10-16 R004 allocation — Connected inventoried RAK4631 `!77fdb9f1` (normal COM17) is labelled R004 and flashed with verified released `2.7.26.0b65f2e`, preserving device keys. Pilot profile and enabled 900-second device/environment/power telemetry plus neighbor transmission pass readback through reboot. Owner reports the same temperature sensor as other RAKs and a fitted INA219; local reports and fresh G001-to-portal battery/weather reception pass, with INA219 wiring/calibration/current interpretation unverified. R004 shares R001's private planned location; its battery, antenna and solar remain unknown. This allocates a fourth of seven undamaged on-hand HW-001 candidates; total remains eight on hand including one damaged, plus two deployed. Three undamaged on-hand candidates remain untested. No sensor-stock total or purchase inferred. [Preparation](../docs/operations/r004-preparation.md).

2026-10-16 INA219 wiring clarification — Owner reports the INA219 inline between the battery and RAK: battery → INA219 → RAK. Record battery/load-path voltage/current sensing, not solar-input measurement. Exact board allocation/fitted quantity, charger connection point, shunt orientation/current sign, calibration and live telemetry remain unverified. The branch current is not automatically total battery charge/discharge current; identify the charger path before making that claim. No quantity, purchase or measured result added. [Flashing/configuration handoff](../docs/operations/board-flashing-handoff.md).

2026-10-15 INA219 plan — Owner intends INA219 current/power sensors (HW-006) on repeaters and gateways. Fitted quantities, installation, wiring/current direction and live mA telemetry remain unverified; no stock count or purchase change. Portal shows unavailable current until measured data is supplied.

2026-10-15 member battery support — Owner identifies the purchase-list 1000/3000 mAh member packs as LiPo and requests configurable type/capacity with voltage-derived charge estimates. Preserve HW-009's earlier owner-reported 1100 mAh label alongside the source's 1000 mAh description; no quantity or installed-per-device capacity changes. Portal suggestions include 1000, 1100 and 3000 mAh. Generic 3.7/4.2 V 1S profile remains uncalibrated; exact pack labels, protection and actual capacity/runtime need verification. [Profile and sources](../docs/research/member-battery-charge.md).

2026-10-15 cell identity follow-up — Owner identifies the relevant repeater cells as **EVE 26V 18650, 2550 mAh, 7.5 A**, and confirms telemetry measures the battery directly. Owner supplies nominal 3.6 V, full charge 4.2 V and cell discharge cutoff 2.5 V, consistent with EVE reference specifications. This resolves the earlier unknown cell model and nominal profile for these packs; per-device two/four-cell arrangement, physical assembly, voltage calibration, actual capacity, protection/node cutoff and endurance remain unverified. EVE lists this family under cylindrical NCM lithium-ion cells. No stock quantities change. Local UI estimate and primary references: [battery charge estimate](../docs/research/battery-charge-estimate.md).

2026-10-15 battery UI clarification — Owner reports the infrastructure batteries under discussion are 2550 mAh 18650 cells in either two-cell or four-cell parallel arrangements. This clarifies intended parallel wiring (1S2P/1S4P), superseding the prior wholly unknown wiring statement for these packs; exact per-device arrangement, cell make/model/chemistry and assembly verification remain unknown. Rated totals would be 5100/10200 mAh for matched cells as stated, not measured usable capacity. No stock quantities or completed-assembly claims change. Voltage-derived state-of-charge estimation is discussed; no curve, calibration or implementation selected.

2026-10-14 planned repeater equipment — Owner allocates R001/R002/R003 to two planned locations, with Muzi whip on R001/R002 and fiberglass on R003. Each is planned for 4 × 18650 rated 2.55 Ah per cell and a 160 mA solar cell: 12 cells planned, without changing the last confirmed 88-cell on-hand count or claiming completed assemblies. Chemistry, wiring/pack capacity, actual cell condition/capacity, panel voltage/wattage and solar-input sensing remain unknown. All three identities/equipment are registered privately in PocketBase; actual voltage arrives for each, and temperature/humidity for R003. [Verification](field-results.md#test-009--live-repeater-provisioning-and-telemetry).

2026-10-14 R003 AHT compatibility follow-up — Same RAK4631 `!05237743`/COM14 now runs custom `2.7.26.cc5907b` from published project source, after owner-authorized build/flash of the AHT detection fix. Local temperature/humidity and automatic reports through both V3s pass; stock profile/keys retained exactly. AHT-family sensor operation is now observed; the owner's tentative AHT21 model and calibration remain unverified. No stock-count, antenna, battery/solar specification or field-allocation change; R001/R002 remain stock. [TEST-008](field-results.md#test-008--r003-custom-aht-build-and-radio-telemetry).

2026-10-14 R003 addition — Owner connects a third on-hand RAK, confirms antenna attached and tentatively identifies a fitted AHT21 temperature/humidity sensor at I2C 0x38. API verifies RAK4631 R003 (`!05237743`, COM14). Stock `2.7.26.54e0d8d` and complete matching pilot profile verified; device battery telemetry reaches both V3s. Environmental enable/900-second cadence saved, but no temperature/humidity observed: pinned stock RAK target excludes AHT detection. Sensor identity/wiring remain owner-reported/unverified. This allocates a third of the 7 undamaged on-hand HW-001 candidates; other 4 remain untested, with total stock unchanged (8 on hand including 1 damaged, plus 2 deployed). This is not a new purchase or automatic expansion of the two-repeater field allocation. One fitted sensor reported; total HW-021 stock remains unknown. [TEST-007](field-results.md#test-007--r003-stock-setup-and-environmental-sensor-limit).

2026-10-14 RAK bench allocation — Two connected on-hand HW-001 units identify through the device API as RAK4631: R001 (`!a65601b3`, COM8) and R002 (`!b456f760`, COM9). Both now run official stock Meshtastic `2.7.26.54e0d8d`, with independent private pilot-profile readback and successful mutual/two-V3 direct encrypted reception (6/6 checks). Owner confirms suitable 915 MHz antennas connected; physical frequency SKU, antenna model, carrier revision, sensors, battery assembly and solar hardware are not independently inspected. Old fixed positions/admin keys cleared; no site coordinates invented. This allocates 2 of the 7 previously untested undamaged on-hand RAK candidates; total stock remains 8 on hand including 1 damaged carrier, plus 2 deployed. Other 5 undamaged on-hand units remain untested. Forced relaying, field coverage and endurance remain unmeasured. [Setup](../docs/operations/rak-pilot-setup.md), [TEST-006](field-results.md#test-006--stock-rak-pilot-repeater-preparation).

2026-10-14 live-ingestion preparation — Native Windows protocol readbacks identify B002 (`!699ca878`) on COM4, B001 (`!699c2ed8`) on COM5, G001 (`!9ea13cc0`) on COM6 and G002 (`!849ad7a0`) on COM7. This supersedes the earlier V4 port-label assumption; follow verified device identity when ports change. Four distinct firmware-reported hardware identities match between independent reads, including across the gateways' Wi-Fi update/restart. Owner supplies replacement Wi-Fi; both V3s save/read back the new settings, with exact MQTT and LoRa configurations preserved and LoRa transmit still disabled. Credentials and physical identity readbacks stay private; quantities, stock firmware and RAK readiness are unchanged.

Updated: 2026-10-12. Imported the owner's [original purchase list](<../Mesh Purchase List - Purchase List.csv>) without modifying it. Listed quantities come from the source `Total QTY` column. Six higher-value groups now have owner-confirmed on-hand counts from the 2026-10-12 inventory check-in; other counts remain unknown. These are owner reports, not independent inspections or bench tests. Blank/dash source quantities remain unknown, not zero.

Source row numbers count the header as row 1. Stable IDs below link to the original rows. Split entries into identifiable units when counted or assigned; preserve the original source references. Specs and roles below are source labels, not verified compatibility or performance.

| ID | Source row | Category | Item / source spec | Listed quantity | Confirmed on hand | Verification / notes |
| --- | --- | --- | --- | --- | --- | --- |
| HW-001 | 2 | Repeater | RAKwireless WisBlock RAK19007 | 10 | 8 | One has a damaged carrier, excluded from ready stock. Five undamaged units identified/prepared as RAK4631 R001–R005; two undamaged on-hand units remain untested. Plus two deployed remotely at Mount Charleston, recover when replacements are ready. Ten accounted for against ten listed; carrier revisions/remaining cores unverified |
| HW-002 | 3 | Repeater | 18650 cells; source EVE 2550mAh | Unknown (source dash) | 88 | Owner confirms 88 on hand. Additional cells in mountain repeaters estimated at perhaps 4 per repeater (about 8 across the 2 reported deployments); excluded from on-hand stock. On-hand cell identities, capacities, condition, and test results unverified; do not assume all match the source EVE label |
| HW-003 | 4 | Repeater | Solar panel; 6W | 4 | Unknown | Source describes an externally mounted alternative; output untested |
| HW-004 | 5 | Repeater | Solar panel; 1W | 40 | Unknown | Source note estimates closer to 0.25W each; not a measured project result |
| HW-005 | 6 | Repeater | Fiberglass antenna; labelled 5.8dBi LoRa 915MHz | 10 | 10 | Owner-confirmed count matches listed quantity; condition and actual connectors/variant unverified |
| HW-006 | 7 | Repeater | INA219 current/power sensor | 10 | Unknown | Verify boards and interfaces |
| HW-007 | 8 | Repeater | Four-slot 18650 holder | 18 | Unknown | Verify wiring/layout; source quantity is holders, not cells |
| HW-008 | 9 | Repeater | Coax; Type N to U.F.L1 | 10 | Unknown | Source associates these with fiberglass antennas |
| HW-009 | 10 | Client | Battery; source 1000mAh, earlier owner report 1100mAh | 4 | 6 | Owner previously reported six small V3 LiPo packs; on 2026-10-21 confirms G001/G002 each have an installed 1000mAh pack. Retain total without adding stock; remaining capacity labels, connectors and condition unverified |
| HW-010 | 11 | Client | Battery; 3000mAh | 2 | 2 | Owner confirms 2 × 3000mAh batteries for V4 units; LiPo per owner; exact pack label, connector and condition unverified. Owner suspects larger batteries are needed; capacity choice awaits runtime testing |
| HW-011 | 12 | Client | Whip antenna; labelled 915MHz | 16 | 11 | Owner identifies these as Muzi whip antennas; exact model, condition, and connectors unverified. 5 fewer on hand than listed; disposition unknown |
| HW-012 | 13 | Client | Heltec V3 | 4 | 9 | Earlier no-GPS report superseded 2026-10-24 for G004: owner reports fitted GT-U7 GPS plus INA219, intended for mesh time. Other units' GPS status and G004 operation remain unverified. Proposed use: internet/backhaul nodes, possibly repeaters depending on installation. Count is 5 above source quantity; provenance, exact radio variant, and condition unknown |
| HW-013 | 14 | Client | Heltec V4 | 6 | 2 | Owner confirms both have GPS modules. On 2026-10-12 owner plans to order 2 more and recover 2 member-held units, all with GPS and 3000mAh batteries. Planned additions are not available stock; purchase, recovery, exact variants, and condition remain unverified |
| HW-014 | 15 | Client | SMA roof mount / antenna base | 2 | Unknown | Verify connector and cable |
| HW-015 | 16 | Both | Case filament; first source entry | 2 | Unknown | Separate source product link; amount remaining unknown |
| HW-016 | 17 | Both | Case filament; second source entry | 2 | Unknown | Separate source product link; amount remaining unknown |
| HW-017 | 18 | Client | Power switch | 20 | Unknown | Verify switch type |
| HW-018 | 19 | Client | USB-C jack | 20 | Unknown | Verify breakout/wiring |
| HW-019 | 20 | Client | Push button; black | 30 | Unknown | Verify type |
| HW-020 | 21 | Client | Push button; red | 10 | Unknown | Verify type |
| HW-021 | 22 | Repeater | Temperature sensor | 10 | Unknown | Model not stated in source item fields |
| HW-022 | 23 | Repeater | Battery cable | 20 | Unknown | Confirm connector and polarity |
| HW-023 | 24 | Repeater | Solar cable | 10 | Unknown | Confirm connector and polarity |
| HW-024 | 25 | Misc | Solder | 1 | Unknown | Amount remaining unknown |
| HW-025 | 26 | Client | LILYGO T-Deck (source: “Tdfeck”) | 2 | 2 | Owner confirms 2 brand-new devices with GPS modules and their own included batteries; battery capacity unknown. Exact variant/frequency and bench operation unverified |
| HW-026 | 27 | Repeater | M3×20 screws | 120 | Unknown | Count remaining |
| HW-027 | 28 | Repeater | M3×30 screws | 120 | Unknown | Count remaining |
| HW-028 | 29 | Repeater | O-ring seal | 1 | Unknown | Verify dimensions/material and remaining amount |
| HW-029 | 30 | RF | Coax; SMA female to U.F.L1 | Unknown (blank) | Unknown | Source shows 2 packs, with no pack size or total quantity |
| HW-030 | 31 | Client | SD card adapter | Unknown (blank) | Unknown | Source shows 1 pack, with no pack size or total quantity |
| HW-031 | 32 | Client | SD card; data logging/testing | Unknown (blank) | Unknown | Source shows 1 pack, with no pack size or total quantity |
| HW-032 | 33 | Camera | Card labelled “SD Card” | Unknown (blank) | Unknown | Source explicitly excludes it from mesh project; track separately for content equipment |
| HW-033 | Owner report 2026-10-12 | Field computing | Rugged Dell laptop/tablet running Linux | Not in source CSV | 1 | Owner reports available for field use. Exact model, Linux distribution, battery condition/runtime, ports, and Meshtastic app/browser compatibility unverified. No purchase/value recorded |

## First confirmation pass

2026-10-14 desktop access check — Four connected boards enumerate on Windows: V4 USB identities match B001 on COM4 and B002 on COM5. Initially both CP2102 bridges lacked drivers (error 28); following owner driver installation and reconnection, both report healthy drivers (error 0) on COM6 and COM7. All four ports pass native serial open/close with DTR/RTS disabled; per-V3 mapping remains unverified here. Ubuntu-24.04 WSL starts but has no USB serial passthrough. No quantities, firmware or radio configuration changed; GPS/MQTT delivery was not retested.

2026-10-14 development workflow confirmation — Owner identifies the current machine as the Dell laptop running Linux and the other development machine as a Windows desktop with WSL, and will regularly alternate between them. No new hardware, quantity or expense; desktop specifications/Docker operation and whether this Dell is HW-033 remain unverified. [Handoff](../docs/operations/development-handoff.md).

2026-10-14 GPS/network follow-up — Owner reconnects the four bench boards and changes hotspot. Both V3s persist the new private Wi-Fi settings, preserve MQTT/receive-only profiles and reconnect. Both original V4s now have internal GPS positions and each automatic encrypted GPS report reaches MQTT through both gateways (4/4 paths; measured ages about 21–35 seconds). Short sample only; runtime/field coverage remain unknown. No quantity, purchase or member assignment change. [TEST-004](field-results.md#test-004--automatic-gps-positions-through-both-mqtt-gateways).

2026-10-14 networking follow-up — Both bench V3s associate with the owner's hotspot and connect to MQTT after the owner runs the tested stock-password compatibility fix. Both 30-byte gateway credentials and receive-only profiles match saved readbacks privately. Each V4 encrypted fixture reaches MQTT through both V3s (4/4 checks). GPS freshness/runtime remain unmeasured; no hardware quantity, purchase or member assignment changes. [TEST-003](field-results.md#test-003--first-real-mqtt-gateway-provisioning-attempt).

2026-10-14 — Bench completion: owner reconnects second V4 and runs temporary runtime access helper; all four nodes are independently identified and stock `2.7.26.54e0d8d` image installs verified. B001 (`!699c2ed8`) and B002 (`!699ca878`) are original V4s with 16MB flash/2MB PSRAM; G001 (`!9ea13cc0`) and G002 (`!849ad7a0`) are V3s with 8MB flash. Owner confirms attached antennas and US selection; exact fitted antenna models and radio SKU markings are not independently inspected. All saved profiles/roles pass reboot checks; each V4 bench fixture reaches both V3s. V4 GPS is configured but fresh fixes/runtime remain unmeasured; V3 Wi-Fi/MQTT provisioning remains pending private credentials. Counts unchanged; these bench labels do not assign members. [TEST-001 / TEST-002](field-results.md#test-001--stock-heltec-provisioning).

2026-10-14 — Bench follow-up: chip inspection identifies original V4 `!699c2ed8` (16MB flash/2MB PSRAM) and V3s `!9ea13cc0` / `!849ad7a0` (8MB flash each). All three receive verified stock `2.7.26.54e0d8d` factory/recovery/filesystem images after private backups. Both V3s boot and receive private transmit-disabled profiles, checked through reboot/readback. V4 post-boot API/GPS setup remains blocked after reset removes its temporary serial ACL; other V4 (USB serial ending `A878`) is disconnected/unflashed. Radio band, antennas, GPS fixes and battery condition/runtime remain unverified; counts unchanged. [Provisioning evidence](field-results.md#test-001--stock-heltec-provisioning).

2026-10-14 — Owner connects 2 V4 and 2 V3 units for bench setup and authorizes formatting/flashing as needed. Host USB discovery confirms four serial devices: `/dev/ttyACM0`, `/dev/ttyACM1`, `/dev/ttyUSB0` and `/dev/ttyUSB1`; one native USB descriptor identifies original V4 with 16MB flash/2MB PSRAM, the other is a generic Espressif descriptor, and both USB bridges are CP2102. Exact per-unit board mapping and firmware/GPS configuration await serial access. Linux device nodes are owned by root/dialout; the current account lacks access and noninteractive sudo requires a password. Requested a temporary per-user ACL on only these four ports. Counts unchanged; connected does not yet establish functioning GPS/radio or battery condition.

2026-10-13 — Development resources: owner reports a home desktop with WSL/Docker potentially available for portal development/integration; exact specs, remote access and working service setup are unverified. Owner's current development laptop is a low-powered Dell; whether this is the same device as HW-033 remains unconfirmed. Initially no Proxmox VM existed; owner subsequently created an Ubuntu LXC for the portal (see below). No purchase, value or production capacity is inferred.

2026-10-13 — One portal LXC confirmed by owner and inspected over authorized SSH: Ubuntu 24.04.5 amd64, 4 logical CPUs, 8192 MiB RAM, 512 MiB swap allowance and 64 GiB SSD-backed root storage. These are virtual resource allocations, not new physical equipment or dedicated host capacity. Unprivileged-container configuration, physical Proxmox specs and off-host backups were not independently inspected. [Deployment record](sites.md#portal-hosting-record--owners-proxmox-lxc). No radio quantity, expense or donation value changed.

The updated pass accounts for 21 radio boards/devices on hand: 8 RAK (1 with a broken carrier board), 9 Heltec V3, 2 Heltec V4, and 2 LILYGO T-Deck. Excluding the damaged RAK leaves 20 candidates for inspection, not 20 bench-verified working devices. Another 2 RAK units are deployed and unavailable for the bench pilot pending replacement and recovery. Member-held Heltec V4 quantities remain unknown.

The first pass recorded four on-hand devices with owner-confirmed GPS modules:
2 Heltec V4 and 2 T-Deck. On 2026-10-24 the owner also reports GT-U7 GPS on V3
G004, superseding the original all-V3s-without-GPS statement. RAK GPS status
remains unknown. These inventory reports alone do not establish working GPS
or passive tracking; later device-specific bench records own those results.
Identify exact radio/core builds and GPS models, then confirm operation and
HW-002 cells before a pilot parts decision. Source-listed quantities remain
historical references even where current counts differ.

Owner-directed planning baseline: use only confirmed on-hand stock. Exclude the 2 deployed RAK units, possible member-held V4s, and the damaged RAK until its carrier board is replaced and operation verified. The newly found RAK closes the numerical difference against the source-listed 10; the prior possible third repeater/destroyed-unit explanation is no longer needed to reconcile that count. Historical differences do not block this first-pass inventory closure.

2026-10-12 — Pilot planning update: owner explicitly expanded the planning baseline to include 2 Heltec V4 purchases and recovery of 2 member-held V4s, each intended to have GPS and a 3000mAh battery. This would provide 6 V4s including the 2 on hand, with the 2 existing T-Decks a separate potential addition to the pilot. Actual trial participant count remains to be agreed. Keep the 4 planned V4s and their batteries separate from confirmed on-hand counts until received/recovered. No order, recovery, price, or additional battery stock confirmed.

Available member-device batteries: 6 × 1100mAh for V3, 2 × 3000mAh for V4, plus included batteries in both T-Decks. V3 backhaul/repeater use is a proposed role, not a firmware decision. Larger V4 batteries are a concern to evaluate against mission duration and measured GPS/runtime behavior, not a confirmed purchase requirement.

2026-10-12 — Owner set battery runtime to a 4-hour minimum and 12-hour target, and is open to purchasing larger batteries. Evaluate runtime before selecting a larger capacity; no new battery size, quantity, order, or available stock established.

No charge-controller or battery-protection hardware is separately identified in this CSV. Check whether it is integrated, owned separately, or absent before treating it as a purchase gap.

Source rows for INA219 and RF coax have unusual per-repeater/unit-cost placement. Use source `Total QTY` only when present; do not use the purchase sheet's per-device columns as an approved bill of materials. Preserve source quantities and replace only the separate confirmed-count field when physically verified.

## Additional inventory to capture

2026-10-13 — Owner identifies the RAK cores as RAK4631. Exact frequency variants, individual unit labels and working condition remain unverified. Counts unchanged. Owner selects Dell-driven testing through the V4 with a GUI/readout.

2026-10-13 — Repeater planning: owner intends solar RAK builds with 2–4 18650 cells and either Muzi whip or fiberglass antenna, plus a GPS-equipped Heltec V4 testing node tethered to the Dell for logs. This is a proposed allocation/configuration, not additional stock or a verified assembly. Exact RAK cores, cell chemistry/condition/pack arrangement, panel/controller, antenna/feedline and tether compatibility remain to verify. No counts, purchases or measured capacities changed. [Operations/survey draft](../docs/research/repeater-operations-survey.md).

2026-10-12 — Future SOS hardware idea: owner suggested adding a buzzer or similar audible alert to Heltec boards, alongside an OLED popup/flashing alert. No buzzer model, quantity on hand, GPIO/driver compatibility, wiring, cost, or purchase confirmed. Evaluate existing parts and the selected board before choosing hardware; SOS remains beyond the passive-tracking MVP.

2026-10-12 — Pilot infrastructure allocation: owner includes RAK repeaters from HW-001 (count/builds still open) and 2 Heltec V3s from the 9 on hand in HW-012. These 2 V3s are planned receive-only internet backhauls, not member GPS trackers or RF repeaters. Internet forwarding with radio silence is an intended requirement, not a tested capability. Allocations do not change stock counts. Use on-hand RAK candidates; the damaged unit requires repair/verification and the 2 deployed units are not assumed available.

2026-10-12 — Portal-planning amendment: owner authorizes one of the 2 allocated V3 backhauls to transmit portal-originated shared-channel replies. The other remains receive-only/uplink-only. Individual unit selection and firmware/radio behavior are unverified; this changes proposed roles, not the confirmed count of 9 V3s or any working-device count. Owner proposes stable numeric device labels with portal-managed member assignments/self-claims; no physical labelling or assignment performed yet.

2026-10-12 — Owner selected 2 undamaged, on-hand RAKs for initial relay evaluation, subject to identifying cores and verifying operation. Select from the 7 undamaged on-hand units; no individual units are assigned yet and stock counts are unchanged. Owner also reports 1 rugged Linux Dell laptop/tablet (HW-033) available for field viewing. Both companion-app and laptop/portal viewing remain intended; the first local-viewing MVP may use the Meshtastic app.

2026-10-12 — Final pilot scope: owner selected the 6 planned V4s only and excluded the 2 T-Decks to reduce device/firmware complexity. T-Decks remain in inventory for later use. Confirmed on-hand counts are unchanged; 2 V4 purchases and 2 recoveries remain pending.

- Complete nodes and radio boards: exact model, frequency variant, count, current firmware if known.
- GPS modules: model, count, which nodes already contain one.
- Antennas, feedlines, connectors, mounts, and enclosures.
- Solar panels, charge controllers, and battery protection hardware.
- 18650 cells/packs: count, cell identity if known, condition, and any test results.
- Keyboard/display nodes and other member-facing hardware.
- Backhaul equipment and spares.

Photos, labels, receipts, and bench tests can support entries later. Record unknowns explicitly. Link spending or contributions to the same hardware IDs in [finances](finances.md). Do not overwrite the purchase-list source when reconciling stock.

## Existing hosted service — MQTT broker

2026-10-13 — Owner confirms Mike Rollins hosts the existing old-pilot server at `mqtt.spp.lol`, a domain owned by the project owner. One existing broker service identified and inspected; physical server/VM ownership, specifications and quantity are unknown, and it is not counted as owner-held radio hardware. Mosquitto is running; certificate renewal and topic-permission checks remain before MeshLink integration. Possible new hostnames are `mqtt.snorr.vegas` or `mqtt.snorr.org`, with no migration selected. [Hosting record](sites.md#broker-hosting-record--mike-rollins). No purchase, donation value or inventory valuation inferred.

2026-10-13 hosted-service update — Fresh pilot Mosquitto configuration installed on the existing Mike-hosted service; local loopback 1883 and auth/ACL checks verified. Old MQTT state privately archived; no hardware quantity, purchase or service valuation changed. Public/proxy access and real node integration remain pending.

## Dedicated debug V3 — 2026-10-16

Owner allocates an existing Heltec V3 to airtime debugging: **MC00 `!9ea0432c`**, currently COM6, distinct from G001/G002. API/flash inspection confirms HELTEC_V3 / ESP32-S3 / 8 MB flash; exact subrevision and antenna model remain unknown. Original `2.7.17.55580d10f` configuration, identity, channel/security keys and full flash are privately backed up. Dedicated application `2.7.26.f95a443` is flashed/verified with CLIENT_MUTE, TX/Wi-Fi/Bluetooth/MQTT disabled and original RF/key/identity preservation. It receives on US channel 35 / 910.625 MHz, BW250/SF11/CR4/5. Total V3 ownership remains **nine**, with one now allocated to debugging; no purchase or operational-gateway change. [Operation and verification](../docs/operations/airtime-sniffer.md).

## 2026-10-24 - Four-gateway firmware and radio fallback

Confirm the four connected operational gateways as G001 `!9ea13cc0`, G002
`!849ad7a0`, G003 `!9e9f167c` (Heltec V3), and replacement G004 `!699c2ed8`
(OLED Heltec V4, formerly B001). No purchase or hardware quantity change.
All four now run checked **2.7.26.6fea6aa**, with CLIENT/private radio TX,
180-second device telemetry and over-LoRa SNNS; G003/G004 retain enabled
180-second INA219 power telemetry. Preserve each identity, keys, RF/GPS and
network profile. G001's original network is restored through reboot after the
controlled outage test. [Image hashes, full backups and live outage/recovery](../docs/operations/gateway-backhaul-health.md#completed-bench-and-deployment---2026-10-24).
This supersedes earlier receive-only/local-only gateway profiles. Sensor
calibration, battery/runtime and field installation remain unverified.
