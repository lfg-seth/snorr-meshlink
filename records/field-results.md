# Field testing and tangible results

## 2026-10-24 - R004 ordinary firmware and INA219 three-minute profile

Owner-requested R004 **`!77fdb9f1`**, USB **`820C9B4F0C2D7675`**, receives
ordinary **rak4631 / 2.7.26.4c96b9b** from the reviewed local application image;
its original diagnostic captures remain retained. Exact image hash and full
original-profile equality pass after flashing. Complete intended
owner/identity/keys/channel/local/module equality passes through an explicit
reboot: CLIENT, enabled device/environment/INA219 power at **180 seconds**,
over-LoRa SNNS with saved 180-second baseline, and separate standard
NeighborInfo at 21,600 seconds. INA219 initializes/opens.

Fresh automatic encrypted MQTT reports reach **both G001 and G002** over a
validating-TLS subscription after the final reboot. Device **3.654 V**,
environment **27.317 degrees C / 27.094% RH**, channel-1 INA219 power
**3.660 V / -298.2 mA**, and the new boot's SNNS sequence 1/source uptime
113 seconds pass independent wire-adapter validation. These are reported
values, not calibrated physical-current/charging measurements.
Two distinct automatic reports per type reach each gateway. Device/environment/
power measurement gaps are **180 seconds**; SNNS sequences 1/2 share one boot
and differ by **195 source-uptime seconds**, including the baseline and jitter.
[Exact image, cadence and private evidence references](../docs/operations/r004-three-minute.md).

Authenticated portal ingestion/cadence metadata, physical accuracy/bridge state,
battery-only behavior, runtime, sustained operation and field coverage remain
unverified. No other board/server/portal mutation or site installation occurs.

## 2026-10-24 - G003 first installation and INA219 gateway telemetry

Owner-requested **G003 `!9e9f167c`** receives dedicated
**heltec-v3-gateway / 2.7.26.4c96b9b** from the exact reviewed local build.
Original factory-demo flash is fully backed up; gateway factory, official
recovery and matching filesystem images pass independent byte verification.
Complete intended owner/new PKI/channel/local/module profile matches through
explicit reboot, including corrected supplied Wi-Fi, CLIENT, LoRa TX disabled,
local-only collector, and enabled **180-second device/power telemetry**.
INA219 is detected at **0x40** and initialized; environment stays off.

Independent validating-TLS MQTT observation receives fresh non-retained
encrypted source/transport-G003 device voltage **4.069 V** at 16:14:26 UTC and
INA219 channel-1 **3.920 V / -489.4 mA** at 16:14:51 UTC. Values/sign are retained
without calibration or charging-path interpretation. A 275-second observation
captures two reports of each type: MQTT receipt gaps **180.353 / 180.176 seconds**
for device/power, respective measurement-clock gaps **180 / 181 seconds**.
Second power is **3.924 V / -489.3 mA**; second device voltage is **4.073 V**.
Five own-source local API telemetry packets are also captured. Serial and MQTT
handles close. [Exact images, private evidence and acceptance limits](../docs/operations/g003-gateway-preparation.md).

No production gateway/source mapping or portal record is changed. Separate
broker credentials, authenticated portal acceptance, sensor calibration/path,
pack/runtime, sustained delivery and field coverage remain follow-ups.
No other board is changed.

## 2026-10-23 - R006 three-minute firmware/profile bench acceptance

At **2026-10-24T00:51:19Z / October 23 17:51:19 Pacific**, the corrected
native Windows UF2 updater completes on R006 `!da581e5f`, ordinary
**rak4631 / 2.7.26.0634b77**, source `0634b775f65804968f5a18a7e8824db415556db2`,
UF2 SHA256 **0734127c43d85ef846caff0f161590183aea964268fcf8fdf1649142970cc9ba**.
Complete intended identity/keys/channel/local/module configuration matches
after an explicit reboot: CLIENT, device/power telemetry **180 seconds**,
environment disabled for INA219-only/no-temperature hardware, SNNS compiled
at 180 seconds and separate standard NeighborInfo at 21,600 seconds.
Serial closed; [acceptance evidence and procedure](../docs/operations/repeater-update.md#r006-installed-verification).

The earlier 1200-baud attempt selected serial-only DFU and stopped before an
application write. Verified application-only serial OTA recovery completes
with 759,304 application bytes and zero SoftDevice/bootloader bytes in
45.03 seconds before the successful corrected API-driven UF2 retry. The
local bundle remains explicitly unpublished; public CI/download verification
is pending. Independent original-before/corrected-before and
intended-final/reboot comparisons preserve the entire original
profile/identity/keys/channels through recovery.

After the final clock gate, three automatic nonretained device, power and
private SNNS packets each reach both G001/G002: nine source packets / 18
gateway copies during **00:52:07.802–00:58:53.068 UTC**. Device and power
measurement gaps are **180 / 180 seconds**; same-boot consecutive SNNS gaps
are **195 / 195 seconds**, including jitter/scheduling. Latest device voltage
is 4.164 V; signed INA219 channel 1 is **4.196 V / -0.2 mA**. No environmental
packet is observed. Independent TLS MQTT receipt passes; authenticated portal
ingestion, upstream queue-age bounds, sustained cadence, physical current
accuracy, battery-only behavior, runtime and field coverage remain unverified.
Linux hardware is untested. R001–R005 are unchanged/unconnected;
R006's owner-requested map point is still pending server access.

## 2026-10-23 - R006 INA219-only production preparation

Owner assigns **R006**, INA219 only/no temperature sensor. Ordinary
**rak4631 / 2.7.26.09d8a9d** replaces the diagnostic target, with verified
INA219 fixes and no diagnostic/dummy-load flags. Full intended profile and
new initial PKI pair persist through reboot: CLIENT, existing US/private
pilot channel at 10 dBm, device/power **900 seconds**, environmental reporting
off, GPS off, neighbor transmission enabled and random-PIN Bluetooth.

Register the unlocated R006 in the live portal without copying a site or
battery capacity. Exact quiesced preservation checks pass for all 31 live /
32 demo tables/schema and protected files, apart from the intended additive
R006 provisioning records/mappings. After the final startup, **three unique
reports / six fresh G001+G002 copies** produce one battery observation,
one channel-1 power observation and one SNNS report, retaining both gateways'
receipts with correct deduplication. At **14:13:05 Pacific**, INA219 reports
**3.856 V / −275.7 mA**; first portal receipt **14:13:08.071**. Device battery
is **3.882 V**; no temperature/humidity and weather capability false.

Fresh delivery passes for both gateways, including GH-5's outstanding power
path. Independent physical current accuracy, battery-only behavior, repeated
15-minute cadence, runtime, native UI and installed-site/field acceptance
remain unverified. Serial closed; other radios unchanged. [Full evidence,
image hash and recovery checks](../docs/operations/ina219-audit.md#r006-production-preparation--2026-10-23).

## 2026-10-23 - Fresh RAK19003/4631 INA219 comparison

Owner-authorized new assembly `!da581e5f` / default `1e5f`, provisional R006,
is flashed to checksum-verified existing diagnostic **2.7.26.09d8a9d**.
Independent version and intended-profile verification pass; identity/keys and
channels are preserved, environmental measurement enabled, and five automatic
firmware-upgrade field changes are recorded. Region stays UNSET. With USB
connected and the 18650 charging, **five fresh replies** give **−270.7 to
−279.4 mA at 3.844–3.848 V**. **Six initialized held triples** repeat their
individual values exactly, with correct calibration/configuration and raw
current arithmetic; no captured overflow or diagnostic transport errors.
An early uninitialized zero-calibration triple is excluded.

The prior amp-scale symptom is absent in these two short captures. Owner's
**280 mA at 5 V USB-input** observation is a separate measurement path;
physical current accuracy, shunt marking/polarity and battery-only behavior
remain unverified. No RF/MQTT/portal, runtime or field-readiness test. Serial
closed; R004 unchanged. [Detailed evidence and next measurement](../docs/operations/ina219-audit.md#fresh-rak190034631-comparison--2026-10-23).

## 2026-10-21 - G002 second Wi-Fi replacement bench check

Owner-authorized COM6 G002 `!849ad7a0`, unchanged **2.7.26.9d2fd8f**. New complete private backup and independent post-restart comparison pass; only Wi-Fi SSID differs, with supplied password already matching. Retained console observes IP acquisition, MQTT connected and publication activity. Five-minute telemetry, identity/keys/channel/MQTT and LoRa TX disabled preserved. Serial closed. Short local bench result; independent broker/production receipt, sustained reconnect, runtime and field coverage unverified. [Evidence](../docs/operations/g002-neighbor-gateway.md#clifford-int24-wi-fi-update---2026-10-21).

## 2026-10-21 - R004 INA219 register diagnosis

Owner authorizes R004 diagnostic flashing with an installed R100 inline between battery and board. Existing firmware reproduces **−1,152.6 mA**; first diagnostic image reaches **−1,437.4 mA**. Address 0x40 configuration/calibration **0x399F / 0x1000** are correct. Updated diagnostic **2.7.26.09d8a9d** independently preserves full identity/keys/channels/profile. Three reads of one held conversion repeat **−40.09 mV / −400.9 mA**, with exact expected raw-current multiplication; ordinary continuous readings vary between conversions. This narrows the issue upstream of portal/unit scaling, without validating the actual voltage drop or current. Physical same-path meter evidence and exact wiring remain pending. Local bench evidence only; RF/MQTT/portal delivery, calibration, runtime and field acceptance are not tested. [Detailed evidence](../docs/operations/ina219-audit.md#r004-reinvestigation--2026-10-21), [investigation](https://github.com/lfg-seth/snorr-meshlink/issues/4).

## 2026-10-21 - G002 five-minute telemetry configuration and first receipt

[Issue #41](https://github.com/lfg-seth/snorr-meshlink/issues/41). Complete independent profile readback passes after enabling device telemetry at **300 seconds** on G002 only. At **10:17:13 Pacific**, packet **14076657** reports **4.25 V** over encrypted MQTT while LoRa TX remains disabled; production stores the voltage at **10:17:14.159**, retaining measurement time **10:17:13.000**. G001 unchanged. First-report delivery passes; repeated cadence, calibrated battery measurement, runtime and reconnect reliability remain unmeasured. [Evidence](../docs/operations/g002-neighbor-gateway.md#five-minute-device-telemetry-enabled---2026-10-21).

## 2026-10-21 ? G002 replacement Wi-Fi bench check

Owner-authorized configuration on COM6 G002 `!849ad7a0`. Replacement Wi-Fi survives network-setting restart; independent complete profile comparison passes with only requested network fields changed. Console observes association/IP acquisition, MQTT connected and queued publish. Firmware unchanged `2.7.26.9d2fd8f`, LoRa TX disabled. Short bench check only: production ingestion, sustained freshness/runtime, reconnect reliability and field coverage unverified. [Evidence and capture limits](../docs/operations/g002-neighbor-gateway.md#wi-fi-replacement--2026-10-21); raw profiles/logs remain private.

## TEST-022 — G001 completes passive gateway neighbor rollout

2026-10-19 Pacific. Owner connects identified G001 `!9ea13cc0` for the same authorized collector update. Full private profile/flash backup, exact cached image/partition comparison, application-only **2.7.26.9d2fd8f** flash/hash verification and complete intended profile comparison pass through explicit reboot. CLIENT/TX disabled and Wi-Fi/MQTT preserved; neighbor enabled/local-only. No rebuild, reset or other-board write.

First 180.3-second validating-TLS window records six G001 deliveries/no decoder errors. At **19:57:55.391**, non-retained own-observer SNNS packet **a1a5ea71**, sequence 1 / boot 1325647066 / uptime 72 seconds, is normalized/accepted with three direct rows: R005 −43 dBm/6.00 dB, R002 −62/6.25, R004 −81/5.50; hearing ages 48/36/33 seconds at encoding, counts 1. Independent authenticated snapshot matches every value/provenance field, preserves null absolute hearing clocks, all nine devices and 13 existing G002 reports. Fresh forwarded GPS/telemetry/neighbors and expected duplicate gateway receipts also pass. [Full image/backup/evidence](../docs/operations/g001-neighbor-gateway.md).

Passive continuation reaches six rows at **19:59:10** / sequence 2 and all seven bench senders (**R001–R005/B001/B002**) at **20:00:25** / sequence 3. R002/R004/B002 counts increase to 2 with updated readings/hearing ages. No active probe or further serial connection is used for this continuation.

Both gateway collector rollout checks pass. Sustained cadence/freshness, calibration, independent RF silence, runtime, coverage and the separate disabled-power-telemetry follow-up remain unverified.

## TEST-021 — G002 gateway-originated passive neighbor reports

2026-10-19 Pacific. Owner activates richer measurements on the V3 gateways. Identified/backed-up G002 `!849ad7a0` receives app-only `heltec-v3-gateway` **2.7.26.9d2fd8f**, with partition/hash verification and complete intended profile/keys preserved through explicit reboot. CLIENT, TX disabled, collector enabled/local-only; owner-authorized replacement Wi-Fi restores backhaul after repeated no-access-point reason 201. Existing MQTT settings unchanged.

Live worker source mapping gains the two existing gateway node IDs after private backup. At **19:42:36**, fresh non-retained G002-originated SNNS packet **b92f2bfd**, sequence 1 / uptime 70 seconds, is normalized/accepted with five direct rows: R002 −45 dBm/6.25 dB, R004 −69/6.50, R001 −50/6.75, B002 −49/5.75, R005 −45/6.00. Hearing ages 28–62 seconds at encoding, counts 1; original observer and gateway both correctly G002. Fresh R005/R002/R001 neighbor copies through G002 are recorded as duplicates without losing gateway receipts. See [full evidence, build/hash and limits](../docs/operations/g002-neighbor-gateway.md).

G001 unmodified; power telemetry, sustained cadence, calibrated readings, RF-silence instrumentation, runtime and field coverage remain unverified. Configuration/source/bench acceptance does not establish field readiness.

## TEST-020 — Fresh post-reflash gateway receipts

After owner repairs DNS, read-only portal archive inspection at **19:19 Pacific** confirms normalized G001 receipts for **all five**: R001 19:15:37, R002 19:15:22, R003 19:17:04, R004 19:15:28, R005 19:15:08. Recent raw envelopes are non-retained with matching topic/gateway identity and recent radio-receipt clocks. Normalized temperature observations: R003 **24.769783°C**, R004 **27.470970°C**, R005 **26.064301°C**; measurement clocks unknown. Actual `meshlink-worker` and API are active; initial probe of nonexistent `meshlink-mqtt-worker` was not a service failure. No recent G002 copy or R001/R002 temperature found. This supersedes the initial short-window/access limits below; calibration, sustained cadence and direct-versus-relayed path remain unverified.

2026-10-19 Pacific, two read-only MQTT windows at 19:14:39–19:15:35 and 19:16:18–19:17:13. Owner asks whether the five reflashed radios reach a gateway and requests retry after changing desktop networks. Both TLS broker subscriptions pass; seven non-retained repeater deliveries match G001 topic/envelope identity with recent gateway radio-receipt clocks. **R003/R004/R005 reach G001/MQTT**: all three send SNNS; R004 also sends device telemetry; R003 sends **24.769783°C**. No R001/R002 or G002 copies observed in these short windows; absence does not establish failure. [Packets, clocks and limits](../docs/operations/repeater-gateway-check-20261019.md).

R003 temperature operation now observed after reflash; sensor calibration and wall-clock measurement time remain unverified (`time=151`, separate from fresh gateway/desktop receipt). First window has one unclassified decode error. No forced-relay, complete-reporting-cycle, utilization/runtime or portal-normalization result claimed. Portal hostname returns NXDOMAIN even through both local DNS servers; current address requested. Private summaries ignored under `private/bench/repeater-gateway-check-20261019*.json`; raw locations/keys not published.

## TEST-019 — R005 ordinary-release CLIENT temperature-only reflash

2026-10-19 Pacific; owner connects R005 RAK4631 `!f95b5501` for the same authorized CLIENT/temperature-only rollout. Match USB identity on COM19/DFU COM20 and E: RAK4631 bootloader; fresh private complete backup saved. Replace one-off dummy-load `2.7.26.8dd4dac` with checksum-verified ordinary neighbor-signal `2.7.26.0b65f2e`, removing GPIO31 HIGH startup override without rebuild/reset/key replacement. Physical load behavior/current unmeasured. [Image/profile/evidence](../docs/operations/r005-client-bench.md).

Planned configuration/preservation criteria **pass** through full independent readback and explicit reboot: CLIENT, device/environment 900 seconds, formerly enabled power measurements now disabled, power display disabled, battery INA address unconfigured, neighbor transmission enabled. Identity/keys/channel/radio profile/Fahrenheit preference preserved, accounting for role-dependent API sleep readback. Other radios/live portal metadata unchanged.

Local environment request plus 45 seconds returns **no temperature/environment metrics**. API device values with uptime 1,453,310 seconds excluded as cached pre-reboot evidence. Sensor operation, fresh RF/MQTT/portal delivery, calibration, sustained cadence/utilization reduction, runtime and field coverage remain unverified. No physical INA219/load removal or resolution of earlier current/load discrepancies claimed. Raw evidence stays ignored under `private/bench/R005-client-20261019/`. [Issue #30](https://github.com/lfg-seth/snorr-meshlink/issues/30) retains sensor verification.

## TEST-018 — R004 CLIENT temperature-only bench reflash

2026-10-19 Pacific; owner connects R004 RAK4631 `!77fdb9f1` for the same authorized CLIENT/temperature-only rollout. Match USB identity on COM17/DFU COM18 and D: RAK4631 bootloader; fresh complete private backup saved. Reflash checksum-verified released neighbor-signal `2.7.26.0b65f2e` without rebuild/reset/key replacement. [Image/profile/evidence](../docs/operations/r004-client-bench.md).

Planned configuration/preservation criteria **pass** through independent full readback and explicit reboot: CLIENT, device/environment 900 seconds, previously enabled power measurements now disabled, power display disabled, battery INA address unconfigured and neighbor transmission enabled. Identity/keys/channel/radio profile and Fahrenheit display preference preserved; account for role-dependent API sleep readback. Other boards/live portal metadata unchanged.

Local environment request plus 45-second observation returns **no temperature/environment metrics**. API device metrics with uptime 3,065 seconds are excluded as cached pre-reboot evidence. Sensor operation, fresh RF/MQTT/portal delivery, calibration, sustained cadence/utilization reduction, runtime and field coverage remain unverified. No physical INA219 removal or resolution of its historical discrepancy claimed. Raw evidence stays ignored under `private/bench/R004-client-20261019/`. [Issue #29](https://github.com/lfg-seth/snorr-meshlink/issues/29) retains sensor verification.

## TEST-017 — R003 CLIENT temperature-only bench reflash

2026-10-19 Pacific; owner connects R003 RAK4631 `!05237743` for the same authorized CLIENT/temperature-only rollout. Match USB identity on COM14/DFU COM16 and D: RAK4631 bootloader; fresh complete private backup saved. Upgrade AHT image `2.7.26.cc5907b` to checksum-verified released neighbor-signal `2.7.26.0b65f2e`, retaining AHT support, without rebuild/reset/key replacement. [Image/profile/evidence](../docs/operations/r003-client-bench.md).

Planned configuration/preservation criteria **pass** through independent full readback and explicit reboot: CLIENT, device/environment 900 seconds, power measurements/display disabled, battery INA address unconfigured and neighbor transmission enabled; identity/keys/channel/radio profile preserved, accounting for role-dependent API sleep readback. Other boards and live portal metadata unchanged.

Local environment request plus 45-second observation returns **no temperature/environment metrics**. Historical temperature success is separate; cached device values with uptime 167,566 seconds are excluded as fresh post-reboot evidence. Sensor operation, fresh RF/MQTT/portal delivery, calibration, sustained cadence/utilization reduction, runtime and field coverage remain unverified. Raw evidence stays ignored under `private/bench/R003-client-20261019/`. [Issue #28](https://github.com/lfg-seth/snorr-meshlink/issues/28) retains sensor verification.

## TEST-016 — R002 CLIENT temperature-only bench reflash

2026-10-19 Pacific; owner connects R002 RAK4631 `!b456f760` and authorizes same CLIENT/temperature profile as R001. Fresh complete private backup saved; USB serial matched between COM9/DFU COM11 and F: bootloader. Reflash checksum-verified pinned neighbor-signal release `2.7.26.0b65f2e` without rebuild/reset/key replacement. [Image/profile/evidence](../docs/operations/r002-client-bench.md).

Planned configuration/preservation criteria **pass** through independent readback and explicit reboot: CLIENT, device/environment measurements 900 seconds, power measurements/display disabled, battery INA address unconfigured, neighbor transmission enabled; identity/keys/channel and other settings preserved, accounting for role-dependent API sleep readback. Other boards untouched.

Local environment request and 45-second observation yield **no temperature/environment metrics**. Local API device metrics show 4.069 V, level 91 and uptime 65 seconds, without proving RF/MQTT/portal reception. Sensor operation, calibration, sustained cadence/utilization reduction, runtime and field coverage remain unverified. Raw evidence stays ignored under `private/bench/R002-client-20261019/`. [Issue #27](https://github.com/lfg-seth/snorr-meshlink/issues/27) retains sensor verification; live portal metadata unchanged.

## TEST-015 — R001 CLIENT temperature-only bench reflash

2026-10-19 Pacific; owner authorizes reflash of connected R001 and requests CLIENT roles with temperature sensors only/no INA219 configuration for the bench rollout. RAK4631 `!a65601b3`, USB identity matched between COM8 and DFU COM10, receives checksum-verified pinned release `2.7.26.0b65f2e` by UF2. No rebuild/reset/key replacement. [Exact image, profile and evidence](../docs/operations/r001-client-bench.md).

Planned criteria: preserve identity/keys/channel/radio profile, save CLIENT, enable device/environment telemetry at 900 seconds, disable power telemetry, verify independent full readback through reboot, then request local temperature. Profile and reboot checks **pass**, including security/channel preservation and enabled NeighborInfo over LoRa. The API's sleep value changes from ROUTER 86,400 to CLIENT 300 seconds by its role-dependent readback implementation.

Local environment request plus 45-second observation returns **no temperature/environment reading**. Sensor operation is unverified; cached device metrics are excluded from fresh post-reboot evidence. No RF/MQTT/portal delivery, sustained telemetry/utilization improvement, runtime, calibration or field-coverage result claimed. Only R001 updated. Raw backups/readbacks are ignored under `private/bench/R001-client-20261019/`; [issue #26](https://github.com/lfg-seth/snorr-meshlink/issues/26) retains fresh sensor verification as the next action.

## TEST-014 — Dedicated Heltec V3 airtime sniffer

2026-10-16 Pacific; owner authorizes conversion/flash of connected V3 MC00 `!9ea0432c`, separate from G001/G002. Original full flash/configuration/keys are privately backed up. Dedicated app `2.7.26.f95a443` / source `f95a443bb`, SHA256 `b2291f0fb3e350ef35a25365c06dc5b709f6823384e931239e8df8cc16e26e7b`, flashes only at 0x10000 with vendor hash verification. Independent post-boot identity/key/channel/RF readback passes; CLIENT_MUTE, TX/Wi-Fi/Bluetooth/MQTT off, US channel 35 / 910.625 MHz / BW250 / SF11 / CR4/5.

Planned criteria: retain every exported receive/repeat, reconstruct exact raw bytes, show known-channel useful data and unknown-key ciphertext, create fresh per-run logs, preserve identity/profile and avoid RF transmit. This is a bench diagnostic test, not field-coverage acceptance.

Measured over 180.118 seconds: **10 receptions, seven duplicates**, seven B002 POSITION_APP copies and three R005 PRIVATE_APP/SNNS copies. All ten reconstruct/decode with **zero reported stream gaps**, and final observed receive airtime is 10.27%. Keyless replay retains/prints the same ten raw frames as opaque; keyed/GUI replay preserves all raw frames/annotations and complete decoded fields. Automatic UART status observes TX0/RX3/bad0; no Packet TX log appears. An optional later local-stat request times out and is not counted as a fresh final counter. No external RF-silence measurement, real read-error event, 58% recurrence or sustained high-load completeness claim.

Twelve Windows checks (including Tk interaction), eleven Linux checks (GUI explicitly skipped for missing Tk/display), Linux launcher syntax and portable C++ address/undefined-behavior sanitizer checks pass. No native Linux USB/GUI or field/runtime validation. [Operation/limits](../docs/operations/airtime-sniffer.md), [run the tool](../scripts/airtime-sniffer/README.md). Raw traffic/configuration remains ignored; all serial handles close after verification.

## TEST-013 — RAK neighbor and sensor power portal integration

2026-10-16 Pacific; owner requests database/portal support for the flashed RAK firmware and sensors. Application source `bed40dd` is deployed; hardware and radio profiles are unchanged.

- Strict SNNS wire/provenance/signal validation, transactional report/link deduplication, signed/zero/absent power fields, separate channel/source clocks, delayed/future reports and authorization checks pass in 57 backend tests. All 45 frontend checks, TypeScript and production build pass. An isolated live copy accepts 11 reports and nine power packets; repeat replay adds zero records.
- Verified backup precedes additive migration of live/separate demo schemas. Live bounded archive recovery accepts 12 reports/ten power supplements; subsequent fresh R005 power and neighbor traffic normalizes through G001. Final backup contains 13 reports, 21 directional link rows and 736 telemetry observations, with R002/R004/R005 neighbor rows. Existing nine identities/configurations and every original protected/history/archive record are preserved.
- Fresh R005 channel 3 reports 4.044 V / +1,034.6 mA at 03:34:46 UTC October 17 (October 16 Pacific); separate environment sensor data remains separate. Hearing ages/counts and report identities are visible without inventing absolute hearing times. Missing/partial neighbors do not delete links. INA219 sign/channel are reported values, with battery/solar interpretation and calibration unverified.
- All nine public assets, authenticated live state/feed, six services, HTTPS/protected routes/authentication throttling and live/demo isolation pass. Complete post-release backup recovery verifies exact link/power metadata and 22 duplicate replay outcomes with zero new records. Browser demo navigation/table/empty power state and populated component DOM tests pass.

Limits: no fresh G002/two-gateway field result, sustained reporting/runtime, calibration, installation/coverage or authenticated native/mobile visual acceptance. [Exact contract, backup hashes and evidence](../docs/operations/radio-report-ingestion.md). Private raw packets/configuration remain off Git.

## TEST-012 — R005 one-off dummy-load build and registration

2026-10-16 Pacific; owner authorizes custom firmware, connected-board flashing and live database registration.

- Build published source `8dd4dacef1cd7a6545983e3dc000ad533101113f` with explicit `rak4631-r005-load`. UF2/OTA creation passes; GPIO31 HIGH/output calls and startup invocation independently verified in linked disassembly. Ordinary RAK target leaves the load option off.
- Identify RAK4631 `!f95b5501` and matched normal/bootloader USB serial; privately snapshot original configuration/keys, then flash one-off `2.7.26.8dd4dac` without factory reset. Independent intended pilot-profile/security-key readback passes before and after reboot. Device/environment/power telemetry enabled at 900 seconds; neighbor transmission enabled. Original US region retained; saved pilot channel/profile applied at 10 dBm.
- Isolated database-copy invalid-identity rejection, registration, idempotence and preservation of existing device rows pass. Live authenticated state confirms nine devices and R005 sharing R001's planned coordinates. Fresh G001 battery ingestion and archived SNNS reception pass. Public HTTPS/proxy/authentication and isolated nine-device backup recovery pass.

Startup opens INA219/AHT drivers. Local and fresh G001 environmental reports carry temperature/humidity; portal weather normalization passes. With batteries connected, INA219 reports roughly −1.1 A; after owner disconnects batteries, fresh local measurements are −0.4 / −0.3 mA at 4.180 / 4.188 V. Owner confirms R100 and expects roughly 50 mA from the dummy load; that load draw is not verified. Normalized current ingestion remains unsupported. Exact samples/checksums: [R005 preparation](../docs/operations/r005-preparation.md). Sustained cadence/runtime, fresh G002 delivery, field placement and calibration remain unverified. Raw data/keys remain private.

Follow-up: owner installs one reportedly fully charged cell and observes 0.08 A on a USB input meter. A new post-request INA219 PowerMetrics sample reports −323.1 mA at 4.200 V. These are separate measurement paths without verified sign/calibration or simultaneous common-path power accounting; the expected 50 mA dummy-load draw remains unverified. No firmware/configuration change; serial time refreshed for valid measurement timestamps.

## TEST-011 — R002 released firmware update without external sensors

2026-10-16 Pacific; owner authorizes R002 update and confirms no external sensors.

- Identify RAK4631 `!b456f760` on COM9, privately snapshot complete profile/keys, verify cached UF2 and bootloader board/USB identity, flash released `2.7.26.0b65f2e` without rebuild/reset/key replacement. Original local configuration, channels, owner and hardware identity match exactly before/after explicit reboot.
- Device/battery telemetry remains enabled at 900 seconds; environment, power, air-quality and health measurement flags are off. NeighborInfo enabled with LoRa transmission and standard 21,600-second interval. Other module settings remain unchanged.
- Live portal firmware/no-external-sensor metadata and private manifest updated; location/equipment and other device configurations preserved. Eight-device authenticated state, public/proxy/authentication checks and final isolated backup recovery pass. [Details/checksums](../docs/operations/r002-release-update.md).
- Fresh post-reboot device packet `2575628823` reaches G001/MQTT at 02:43:29.464 UTC October 17 (October 16 Pacific), measurement 02:43:26 UTC: 4.202 V, level 101, uptime 66. It normalizes into live R002 battery telemetry. Fresh `926194200` reaches G001 at 02:43:36.491 UTC: 40-byte SNNS v1 report archived; normalized custom-neighbor decoding unsupported.

Limits: no fresh G002/two-gateway result, calibrated battery voltage, sustained cadence/runtime, forced relay, native browser review or field/site acceptance. No external sensor data expected or enabled. Raw captures/settings/keys remain private.

## TEST-010 — R004 released firmware and live registration

2026-10-16 Pacific, USB bench plus live portal. Owner authorizes R004 flashing/configuration and registration at R001's location with temperature sensor and INA219.

- Identify RAK4631 `!77fdb9f1`, privately back up its older MR03 profile/keys, verify released UF2 checksum, match its DFU board/USB identity and flash `2.7.26.0b65f2e` without reset or rebuild. Independent profile readback before/after explicit reboot verifies preserved keys, pilot channel/radio at 10 dBm, ROUTER/local-only, 900-second device/environment/power telemetry, enabled neighbor transmission, debug API off and cleared old fixed position.
- Local sensor packets include 4.087 V device voltage, 26.567078°C / 21.399498% RH and INA219 legacy 0.008 V / 1.6 mA. Power report encodes channel 3 at 0.008 V / 1.7 mA; the legacy writer/PowerMetrics union mapping and USB/wiring path require investigation before interpreting these as battery current. No calibrated accuracy, charge direction or solar reading claimed.
- Guarded manual migration passes isolated invalid-identity rejection, idempotence and existing-device preservation. Live registration/mapping preserves prior seven devices/history and adds R004 at R001's private planned coordinates. Authenticated state verifies identity, fitted-weather/INA219 metadata, unknown R004-specific equipment and disabled planned-site warnings.
- Fresh automatic device packet `56599808` reaches G001/MQTT at 02:35:35.802 UTC October 17 (October 16 Pacific), with valid measurement clock, 4.143 V and uptime 66. Environment packet `104352002` reaches G001 at 02:36:00.451 UTC: 26.510239°C / 21.435547% RH. Both normalize into live R004 observations; current remains unsupported. New port-256 packet `2408390913` reaches G001/MQTT: 40-byte `SNNS` v1 companion archived, custom-neighbor decoding unsupported.
- G002's last recorded receipt remains October 15 at 14:38:41.170 UTC. No fresh second-gateway receipt, two-gateway dedup result or gateway reconfiguration claimed. Buffered/pre-registration packets excluded from successful-ingestion evidence.
- Pre/post-registration backup recovery, eight-device restored state/history, proxy authentication/throttling, public HTTPS/certificates and live-mode checks pass. [Operation details/checksums](../docs/operations/r004-preparation.md).

Limits: INA219 wiring/calibration/power-channel mapping, fresh G002 delivery, portal current/neighbor decoding, native browser visuals, sustained cadence, runtime, forced relaying, site installation and field coverage remain unverified. Private raw/configuration evidence stays outside Git.

2026-10-14 TEST-009 correction — Owner's browser check caught standalone demo after successful live API/telemetry checks: frontend build omitted live mode. Records remained intact. Fresh public browser reproduces demo; corrected production default/mode marker/deployment guard restore sign-in. Ten frontend tests/typecheck/build pass; public boundaries and isolated restore pass. API success did not establish correct browser entry. [Root cause](../docs/operations/repeater-telemetry.md#frontend-mode-correction).

## TEST-009 — Live repeater provisioning and telemetry

2026-10-14 Pacific; hosted PocketBase/portal and powered bench radios. Owner confirms R003 powered/in range. Planned sites/equipment are configuration evidence, not measured placements.

- Three repeater records and explicit node mappings added, preserving two existing trackers, two gateways, five accounts and histories. Authenticated state matches exact private planned coordinates/equipment/identities. R002/R003 share one grouped map marker with separate cards. No raw coordinates/tracks published.
- Genuine battery reports: R001 4.115 V at 21:34:29, R002 4.159 V at 21:38:15, R003 3.634 V at 21:37:54. R003 environmental measurement at 21:38:19: 19.8942°C, 36.7484% RH. Each arrives through G001/G002 and yields one accepted observation plus a duplicate receipt: four observations/eight receipts. Actual clocks are valid; calibrated accuracy and charge state are unverified.
- Staged 39 backend tests, 8 frontend tests, TypeScript/build and isolated invalid-third-record transactional rollback/preservation pass. Unknown-time readings remain visibly unknown and cannot replace known measurements; zero values and invalid humidity/voltage are covered. No synthetic production injection.
- Public Cloudflare HTTPS/certificate/protected routes, proxy auth/throttling and isolated backup restore pass. Final backup includes seven devices, four telemetry observations and preserved existing records/private configuration; matching checksum in [operations](../docs/operations/repeater-telemetry.md).

Limits: short bench sample only; no installed-site proof, forced relay/coverage, sustained 15-minute cadence, solar input, battery runtime, sensor calibration, authenticated browser visual review or off-host backup. Planned-site warnings remain disabled pending activation and thresholds; ingestion/display is active.

Updated: 2026-10-14. Software broker, firmware provisioning, local radio and actual two-gateway MQTT fixture tests are recorded below. A short GPS delivery/freshness observation is now recorded; sustained delivery, battery-runtime and field results remain unmeasured. Agree numerical acceptance criteria before using those tests to claim success.

## Test index

### TEST-008 — R003 custom AHT build and radio telemetry

- 2026-10-14: owner explicitly authorizes porting the identified AHT fix, building and flashing R003. Firmware submodule initialized at pinned `54e0d8d`, existing project branch advanced/published to `cc5907b1fc7b4c200e23f43e10baa54c39aeaf25`. Only the RAK `HAS_NCP5623` definition/explanation differs from the release; no forced environmental cadence or wider old-fork defaults. Native PlatformIO `rak4631` build succeeds, version `2.7.26.cc5907b`. [Build details/hashes](../docs/operations/r003-aht-build.md).
- Identity-verified R003 enters DFU and accepts the checksum-verified UF2. No reset or bootloader update. Independent post-flash API confirms version/identity and exact equality of entire local/module/channel settings with the private pre-flash snapshot, preserving keys, private pilot profile, 900-second enabled device/environment telemetry and debug API off.
- Local response now contains 22.90535°C/35.01892% RH. New automatic device packet `1993071474` reaches both V3s (4.267 V, charging/no-battery level 101, uptime 66 seconds). New automatic environment packet `2012857203` reaches both (22.97821°C/34.962845% RH). **4/4 new device/environment gateway receipts pass**; queued older packets observed during gateway connection are excluded. No gateway settings changed. This replaces TEST-007's stock-only environmental limitation for R003.
- Telemetry time fields 66/91 are not Unix wall-clock times; future infrastructure ingestion needs explicit clock-validity/receipt-time handling. Short startup sample only: no calibration, sustained cadence, runtime, forced relay or field result. Portal remains GPS-only. Scope remains R003; R001/R002 stock images unchanged.
- Scoped clang-format 16.0.3 and Git whitespace checks pass; Trunk unavailable on Windows. Vendor-library compiler warnings retained; full native/MCP suite not run. All firmware artifacts, config/key snapshots and raw telemetry receipts remain ignored/private.

### TEST-007 — R003 stock setup and environmental sensor limit

- 2026-10-14: owner connects another on-hand RAK and requests R003 with the same stock pilot setup plus temperature/humidity if available; confirms antenna connected and tentatively identifies AHT21 at 0x38. API identifies RAK4631 `!05237743` on COM14, previously `2.7.17.36133d29d`. Private backup/reset and matching official Nordic serial stock install complete; no bootloader change. Full profile verification passes after configuration reboots, including shared private channel/radio, ROUTER/local-only, 10 dBm, device telemetry enabled at 900 seconds and environmental measurements enabled at 900 seconds.
- During approximately four minutes of gateway observation spanning configuration changes, both independently identified transmit-disabled V3s receive two distinct automatic R003 device-metric packets (4/4 receipts). Reported voltages are 4.259 V and 4.278 V; battery level 101 indicates charging/no-battery status. No meter calibration, steady-state cadence or battery endurance measurement.
- No environmental packet received at either gateway, and a roughly 65-second local environmental request/observation returns device metrics but no temperature/humidity. A brief private debug collection adds no useful detection evidence; debug API restored off. Clean final telemetry profile clears unrelated sensor options; independent complete readback passes again.
- A final explicit reboot disconnects USB and the complete profile passes after reconnect, including environmental/device enable flags, both 900-second intervals, debug API off and unrelated telemetry modules off. The previously observed Python close/disconnect race occurs again after the reboot request; the successful subsequent device readback verifies persistence.
- Pinned standard RAK target defines `HAS_NCP5623`; its I2C scanner compiles out the AHT detection case under that definition. This is a concrete stock-target limitation for the reported sensor, not proof of physical wiring or AHT21 compatibility. [Exact sources and setup](../docs/operations/rak-pilot-setup.md#r003-environmental-sensor-follow-up--2026-10-14). Keep environmental reporting marked unavailable/unverified despite saved enable flags. Owner's stock-firmware constraint preserved; no custom build or hardware replacement.
- R001/R002 disconnected during this run; neither reconfigured. Portal remains GPS-only; these battery/environment settings do not integrate infrastructure telemetry. Forced relaying, field coverage, 15-minute steady-state reporting and solar/battery runtime remain untested.

### TEST-006 — Stock RAK pilot repeater preparation

- 2026-10-14: owner authorizes stock firmware/reset/configuration on two connected RAKs and confirms suitable 915 MHz antennas attached. Identify R001 `!a65601b3` on COM8 and R002 `!b456f760` on COM9, both firmware-reported RAK4631. Private before-state exports preserve previous profiles; stock `2.7.26.54e0d8d` target/package hashes and the post-reset serial recovery are recorded in [setup](../docs/operations/rak-pilot-setup.md). Recovery succeeds through the matching official Nordic serial firmware package; the timeout's precise cause remains unresolved.
- Configure visible `ROUTER` roles, `LOCAL_ONLY` rebroadcast, the existing private pilot channel/key, US/LONG_FAST, slot 35, hop limit 3 and 10 dBm transmit. MQTT/Wi-Fi off; no channel downlinks/uplinks on the RAKs. Clear old fixed positions/admin keys, create fresh device keypairs, disable GPS pending hardware/location identification, and set device telemetry to 900 seconds. Role-change defaults require a second profile application; independent readback on each board verifies the explicit values.
- Predetermine reception criterion: one distinct harmless encrypted zero-hop text fixture from each RAK must reach the other RAK and both V3s, identified by matching packet IDs. All six of six checks pass. Both existing gateways are independently identified and still report transmit disabled; no gateway configuration written. Raw fixture events/readbacks remain ignored under `private/bench/`.
- Explicit reboot requests disconnect both USB APIs; independent reconnection/readback then passes the complete profile on each board. The Python client's close routine reports an already-disconnected-stream error after each reboot request; subsequent device readbacks succeed. This is not a battery power-cycle or endurance test.
- Follow-up: owner completes an earlier double-reset request after setup, exposing two RAK4631 UF2 drives. Reinstall the same checksum-verified stock UF2 without configuration erase. Both normal serial APIs return and complete pilot-profile readbacks pass again; direct reception was not rerun for this unchanged-image recovery.
- Battery-reporting correction: owner asks about battery voltage. Pinned stock `DeviceTelemetry.cpp` requires `device_telemetry_enabled`; the initial profile only set its 900-second interval, leaving broadcasts disabled. Enable the flag on both RAKs, retain the interval and independently verify the complete profiles after configuration reboot. Update private provisioning/verification helpers to require the flag. Stock metrics contain voltage and level (101 means charging/no battery); no actual battery calibration, timed automatic RF-report observation or portal battery ingestion is claimed.
- Limits: this is direct close-bench transmit/receive evidence, not a forced relay-path test, coverage result, measured RF-silence result or sustained delivery rate. V4s are not connected during this run; no new GPS/portal/outage/runtime test. Battery/solar assemblies, exact antenna models, fitted sensors and site permission remain unverified. Existing portal provisioning remains unchanged; RAK telemetry is not integrated into the portal.

## Software MQTT public-endpoint access test — 2026-10-14

Owner-supplied PASS output from [public MQTT check](../scripts/server/check-mqtt-public.py), using MQTT 5 software clients with existing pilot accounts and certificate/hostname validation for `mqtt.snorr.org:8883`. A temporary loopback-only reverse SSH relay routed encrypted TLS through the external test host to the public endpoint, avoiding the broker-origin direct-route timeout. Both V3 accounts published non-retained synthetic audit messages received by the worker. Anonymous/invalid logins, worker writes, gateway reads, and JSON/unrelated-topic writes were denied. No configuration change or retained message was created by this test. Relay closed afterward; independent SSH confirms no port-18884 listener and active Mosquitto. This verifies broker transport/authentication/topic permissions, not physical gateway, GPS, radio, runtime, reconnect or live portal ingestion behavior.

## Heltec bench readiness review — 2026-10-14

[Staged checklist](../docs/operations/heltec-bench-checklist.md) and [current primary-source check](../docs/research/heltec-bench-source-check.md) prepared. Stock firmware supports starting a small local V4 GPS / V3 receiver evaluation after revision, image, wiring, power, antenna and radio configuration checks. Public broker transport has recorded TLS/rejection evidence; subsequent owner-run valid-account synthetic delivery and ACL checks through public TLS pass. Live portal ingestion and custom survey implementation remain unfinished. No radio connected to the agent environment was identified, and no firmware flash, GPS/radio/MQTT hardware run or battery measurement occurred. This is a readiness review, not a measured test result.

## Planned direct-link repeater survey — 2026-10-13

Owner requests a firmware ping/pong responder on solar RAKs, with a GPS-equipped Heltec V4 testing node and Dell log storage; compare repeater and testing-node antennas separately. [Draft procedure and metrics](../docs/research/repeater-operations-survey.md), under [Define repeater operations and direct-link placement testing](../.scratch/pilot/issues/14-repeater-operations-survey.md).

Record repeater-measured ping RSSI/SNR and V4-measured pong RSSI/SNR, direct-path evidence, every attempt/timeout, GPS fix time/age, antenna mounting/feedline, firmware/radio settings and transport discontinuities. Proposed repeated checkpoint sampling is exploratory, not an agreed acceptance criterion. Round-trip success cannot separately establish directional delivery rates. Later GPS relay/outage tests remain separate. Owner mentions previous testing but has not supplied evidence; no measured results, preferred site, antenna winner or completed test is recorded here. Raw GPS logs remain ignored/private.

## Agreed pilot criteria — 2026-10-12

Source: owner responses in [Define useful tracking for the first field pilot](../.scratch/pilot/issues/02-pilot-needs.md). These are planned criteria; no measured results exist.

- Dispatch visibly distinguishes stale locations and displays position age; stale threshold is 15 minutes since GPS measurement. Backfilled positions retain their original measurement age.
- Member nodes track for at least 4 hours on battery; 12 hours is the target. Record runtime under the tested GPS/reporting configuration.
- Power-on starts passive GPS broadcasting without phone use or repeated member interaction. SOS is deferred beyond this MVP.
- Evaluate aggressive reporting and dial back using measured congestion; plugged-in/battery modes and movement thresholds remain candidate options. Numerical settings and congestion criteria are not yet agreed.
- Planned trial count: 6 Heltec V4s only, with GPS and 3000mAh batteries; 2 are on hand, 2 purchases and 2 recoveries are pending. T-Decks are excluded. Routes, trial duration, acceptable stale/missing-position frequency, and backhaul outage acceptance criteria remain open. A 15-minute display threshold alone does not define a network delivery pass rate.
- Infrastructure: RAK repeaters (count/builds to select) and 2 Heltec V3 internet backhauls. Portal-planning amendment permits one designated V3 to transmit shared-channel replies; the other stays receive-only. Verify V4-to-RAK-to-V3-to-dispatch delivery, designated-gateway command behavior, and the receive-only V3's radio silence while internet forwarding is active. Record both backhauls' receipt times separately from GPS measurement times; duplicate handling and outage/recovery checks need a defined procedure. No relay/backhaul measurements exist yet.
- Disconnect internet backhaul and verify local field command-post viewing plus other-member locations on connected companion apps. Distinguish radio delivery, app connection, available offline map data, and position age; do not treat an internet outage as a radio outage. Phone-free tracking must continue. No offline viewing or map tests performed.
- Start relay evaluation with 2 undamaged on-hand RAKs after core identification/operation checks. The Meshtastic app is acceptable for first local-viewing MVP; both app and laptop/portal viewing are intended. The owned rugged Linux Dell is a field-computing candidate, not a verified offline viewer. Record actual viewer platform, version, connection, map preparation, and measurement-age behavior during testing.
- Multi-backhaul evaluation: establish the 2-V3 private-MQTT baseline first, then add 1 companion-app/cellular uplink and increase only if measured behavior is acceptable. Permit portal-message downlink only on the designated V3; keep other tracking gateways from accepting internet-to-LoRa commands. Measure duplicate deliveries, unique position completeness/age, gateway identities, broker/client load, reconnect bursts, phone battery/background behavior, and radio airtime. Confirm delayed duplicates do not reset freshness or replace newer fixes. No acceptable gateway count, saturation limit, or app-proxy reliability established.

## Planned infrastructure-portal verification — 2026-10-12

Source: [Define the dispatch portal MVP](../.scratch/pilot/issues/06-dispatch-portal.md). No results recorded.

- Identify fitted sensors and actual readings on selected RAK/V3 builds; verify battery level/voltage, charging/discharging and solar measurements where available, with correct units and labelled measurement points. Distinguish direct readings from calculated trends.
- Check environmental/detection reports only where equipped. Verify recording, duplicate handling, per-reading timestamps/freshness, historical charts and event logs. Unavailable/stale intrusion data must not show an all-clear.
- Exercise configurable low-battery/missing-telemetry/intrusion warnings after thresholds and acknowledgment/clearing rules are agreed. Keep infrastructure telemetry cadence separate from member-GPS freshness; measure any added radio traffic against passive-tracking priorities.
- Apply the [agreed infrastructure warning policy](../.scratch/pilot/issues/10-infrastructure-warning-rules.md): verify silent persistent badges, audited permissions, capability-specific timeouts, fresh-data recovery, latched/grouped intrusion incidents, replay/duplicate handling and feed-outage/reconnect grace. Check battery configuration distinguishes type, count, capacity scope and pack arrangement from measured health. These checks are planned; none passed yet.

## Test records

| Test ID | Date | Bench / field | Objective / route | Configuration / firmware commit | Evidence reference | Outcome |
| --- | --- | --- | --- | --- | --- | --- |
| TEST-001 | 2026-10-14 | Bench | Stock Heltec firmware/configuration preparation | `v2.7.26.54e0d8d`, commit `54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb` | Ignored `private/bench/`; sanitized details below | Follow-up completes four stock installs and full profile/role reboot checks |
| TEST-002 | 2026-10-14 | Bench | Each V4 fixture received by both V3s | Same release; private channel, US LONG_FAST, slot 35, configured 10dBm, hop limit 3 | Ignored `private/bench/radio-smoke-20261014T180221Z.json` | All four reception checks pass; no GPS or MQTT claim |
| TEST-003 | 2026-10-14 | Bench / software | Hotspot association, broker subscriber, MQTT fixture delivery | Same stock firmware and private channel | Ignored `private/bench/connection-status.json`, `mqtt-saved/`, `mqtt-radio-smoke-20261014T183218Z.json` | Initial 0/4 before password correction; subsequent actual encrypted gateway MQTT delivery 4/4 PASS |
| TEST-004 | 2026-10-14 | Bench | Automatic GPS positions from both V4s through both V3s | Same stock build/channel; replacement hotspot | Ignored `private/bench/gps-mqtt-20261015T002434Z.json`, `gps-herrera/`, `herrera-saved/` | 4/4 GPS member/gateway paths PASS; fix ages about 21–35 seconds |
| TEST-006 | 2026-10-24 | Bench | Saved SNNS intervals, B002 PKI admin and gateway local behavior | R006/G001/G002 `2.7.26.4c96b9b`; B002 unchanged stock `2.7.26.54e0d8d` | [Images, measurements, restoration and limits](../docs/operations/repeater-update.md#r006-and-gateway-admin-bench---2026-10-24); ignored `private/bench/local-3-admin-20261024/` | Cadence, preservation and interrupted-edit recovery pass; rebooting-write ACK ambiguity and forced-relay acceptance remain explicit |

### TEST-001 — Stock Heltec provisioning

- Owner authorizes formatting/flashing 2 V4 and 2 V3 units. USB initially shows four units; V4 with USB serial ending `A878` disappears before serial inspection and is not flashed.
- Remaining chips identified: original V4 `!699c2ed8`, 16MB flash / 2MB embedded PSRAM; V3 `!9ea13cc0` and V3 `!849ad7a0`, each 8MB flash. Exact frequency variants, attached antennas and current US test location still await confirmation before RF enablement.
- Full original flash/configuration backups remain private. All three receive clean stock installs from the official ESP32-S3 release archive; SHA256 matches GitHub (`339650ced8b8c859751f04be69c6af845fea96baca1327518f199afd2595a9d4`). Target image sizes/hashes match manifests. Factory, recovery/OTA and filesystem images are written at target-manifest offsets and independently verified against flash.
- Both V3s boot stock `2.7.26.54e0d8d`. Private bench profile uses a shared random-key `SNORRbench` primary channel, full position precision, uplink on/downlink off, `config_ok_to_mqtt` on, MQTT-originated radio traffic ignored, slot 35 and proposed 10dBm power. Region UNSET, transmit disabled, GPS not present, Wi-Fi/MQTT disabled. Endpoint `mqtt.snorr.org:8883`, TLS, root `snorr/pilot` and encrypted protobuf mode are staged without credentials; no hardware MQTT delivery claimed.
- Bulk serial writes initially fail to persist parts of the profiles. A single transmit-disable write succeeds; longer post-commit hold improves persistence, but complete validation still detects a missed MQTT config. Private logs show UART0 buffer-full errors. Spacing config/channel writes by 0.4 seconds and holding serial open 3 seconds after commit produces no buffer-full errors and processes MQTT config. Saved-profile checks and independent reboot/readbacks distinguish actual state from successful host sends.
- V4 flash verification passes, but bounded API probes time out after RTS reset while the flasher remains reachable. Watchdog reset re-enumerates it as ACM0 and removes the temporary owner-granted ACL. V4 post-boot API/GPS/profile verification awaits restored access. [Runtime access helper](../scripts/bench/grant-heltec-serial-access.sh) prepared/syntax checked; no agent-root execution.
- Final independent reboot checks both bench short names (G001/G002) and every specified saved-profile field; both pass, including staged MQTT endpoint/root/TLS and matching private channel keys. Result: three image installs verified and both V3 profiles pass; overall four-board provisioning incomplete. No fresh GPS fixes, RF delivery/silence measurements, hardware MQTT/reconnect, battery runtime or offline viewing tests collected. Raw backups/configurations/logs and channel key remain ignored/private.

2026-10-14 follow-up — Owner runs runtime access helper, reconnects the second V4, reports selecting US on the three flashed devices and confirms attached antennas. Runtime ACLs survive native USB reset. Newly reconnected V4 `!699ca878` is confirmed original V4, 16MB flash/2MB PSRAM, running old `2.7.15.567b8ea`; 1200-baud touch enters its bootloader. Private full-flash/configuration backup, clean stock install and independent factory/recovery/filesystem verification pass. All four devices now boot the same release. First US initialization regenerates PKI keys and enables transmit; receive-only V3 settings are restored and each final role is explicitly checked. Initial second-V4 profile readback catches missing settings; reapplying after initialization succeeds. No internal cause beyond incomplete first application is established.

Final independent reboot/readback verifies every specified profile field and these bench labels/roles:

| Bench label | Hardware node ID | Board | Region / preset / slot / configured power | LoRa transmit | GPS |
| --- | --- | --- | --- | --- | --- |
| B001 | `!699c2ed8` | Original V4, 16MB / 2MB PSRAM | US / LONG_FAST / 35 / 10dBm | Enabled | Enabled, RX39/TX38/enable34 |
| B002 | `!699ca878` | Original V4, 16MB / 2MB PSRAM | US / LONG_FAST / 35 / 10dBm | Enabled | Enabled, RX39/TX38/enable34 |
| G001 | `!9ea13cc0` | V3, 8MB | US / LONG_FAST / 35 / 10dBm | Disabled | Not present |
| G002 | `!849ad7a0` | V3, 8MB | US / LONG_FAST / 35 / 10dBm | Disabled | Not present |

All use only one enabled primary channel (`SNORRbench`) with a shared private random key and full position precision. V4 profiles use 60-second GPS acquisition, 120-second periodic reports, smart broadcasting off, fixed position off and GPS-solution timestamp flag on; phone-free fresh-fix behavior remains to measure. V3 channel uplink is on; all downlinks are off and MQTT-originated radio traffic ignored. Both V3s remain transmit-disabled through reboot. Wi-Fi/MQTT stay disabled on all four; current broker endpoint, TLS, root and encrypted protobuf settings are staged. Bench labels identify devices, not member assignments. Result: stock firmware/local-radio preparation complete; GPS acquisition/freshness and gateway networking remain unverified. Broker accounts/Wi-Fi access require private provisioning; owner asked for private file paths, not secrets in chat.

### TEST-002 — Local encrypted radio fixture reception

- Started 2026-10-14 18:02:21 UTC (11:02:21 Pacific). Two V4s and two V3s; firmware and settings as above. No RAK relays or internet gateway connections active.
- Criterion set before the run: a distinct harmless encrypted bench text fixture from each V4 must arrive at each V3. Both V4 fixtures reach both receive-only V3s: four of four checks pass. Private event records retain origin/packet ID, receiver, host receipt time and available radio metrics. V4s use normal configured hop limit 3; this does not prove direct-only paths or resume the deferred survey module.
- Available SNRs: 7.0 / 6.5dB for B001 at G002/G001; 6.25 / 6.0dB for B002 at G001/G002. RSSI is recorded as -9dBm for B001 at G001 and -16dBm for B002 at G002; absent on the other two events, not invented. These close-bench measurements do not establish range, field coverage or sustained delivery rates.
- No position events collected during this short fixture test, and no GPS fix is claimed. V3 transmit-disabled configuration is verified, not measured RF silence. MQTT software checks remain separately confirmed; no real gateway MQTT, portal ingestion, reconnect, runtime or offline-map result.

### TEST-003 — First real MQTT gateway provisioning attempt

- Owner supplies credentials and resets hotspot in compatibility mode. Laptop NetworkManager confirms actual SSID rather than its interface-labelled connection name. Both V3s associate and obtain IPs; saved credential equality is checked privately. LoRa transmit remains disabled. Credentials/captures stay ignored/private; no passwords published.
- Existing read-only worker subscriber authenticates through public certificate/hostname-validated TLS and subscribes to `snorr/pilot/2/e/#`. Two harmless encrypted V4 fixtures yield zero of four expected member/gateway MQTT receipts; V3 readback shows MQTT still disabled and account settings unapplied.
- Prerequisite failure: generated gateway passwords are 48 UTF-8 bytes; pinned NanoPB MQTT password storage is 32 bytes including termination (31 usable). That config cannot fit stock V3s despite valid software-client authentication. This is not a broker transport/ACL defect. [Source/prepared fix](../docs/operations/mqtt-nginx-handoff.md#heltec-connection-settings).
- Two gateway password replacements are prepared, not applied. Isolated real-broker tests verify 30-byte replacements authenticate, old values fail, worker password/hash and ACL are preserved, rerun is idempotent, and injected verification failure restores original files/authentication. Owner sudo execution of the guarded fix remains required before private export retrieval and device provisioning.
- Result: hotspot/subscriber pass; actual gateway MQTT remains blocked/unverified. No GPS freshness, portal ingestion, runtime or reconnect claim.


2026-10-14 successful follow-up — Owner runs the guarded compatibility fix. Retrieved owner-private export has two 30-byte gateway passwords and the unchanged 48-byte worker credential. Both V3s persist endpoint/account/root/TLS/encrypted-protobuf settings; password and Wi-Fi equality checks pass privately. Both connect to Wi-Fi and MQTT. At 18:54:46 UTC (11:54:46 Pacific), each V4 sends a distinct harmless bench text fixture. The certificate/hostname-validating read-only subscriber receives and decrypts both fixtures from both gateway identities: all four member/gateway checks pass, all four payloads encrypted, no parser errors. Evidence: ignored `private/bench/mqtt-compatible/` and `mqtt-radio-smoke-20261014T185446Z.json`. No position events collected; no GPS freshness or portal ingestion claim. Settings retain uplink-only channels and disabled V3 LoRa transmit; configured silence is not a measured RF-silence test.

Independent gateway reboot follow-up — Both saved profiles, including exact private credentials, pass readback after reboot. Initial status checks precede MQTT connection; subsequent checks show both Wi-Fi/MQTT connections restored. Fresh encrypted V4 fixtures again reach both restarted gateways and the worker subscriber (4/4 PASS). Evidence: ignored `private/bench/mqtt-reboot/`, `connection-status.json` and `mqtt-radio-smoke-20261014T185601Z.json`. This tests gateway reboot recovery, not hotspot/proxy/broker outages or sustained reliability.

### TEST-004 — Automatic GPS positions through both MQTT gateways

- Owner reports satellites after reconnecting the nodes, then supplies replacement hotspot credentials. Restore owner-granted serial access; apply new Wi-Fi to both V3s. Private readback verifies exact Wi-Fi equality and unchanged MQTT configurations/credentials, with LoRa transmit still disabled. Both gateways reconnect to Wi-Fi/MQTT after initial transitional disconnected states.
- Observation starts 2026-10-15 00:24:34 UTC (2026-10-14 17:24:34 Pacific), with a certificate/hostname-validating read-only MQTT subscriber. No synthetic position, manual send-position command, phone app or firmware change is used. Watch automatic reports for at most 260 seconds, stopping after all four member/gateway paths contain recent GPS measurement timestamps. This is an exploratory bench check, not an agreed field delivery-rate threshold.
- B001 `!699c2ed8`: one unique encrypted GPS report received through both G001/G002; 9 satellites, original GPS measurement age 21.13 seconds at each subscriber receipt.
- B002 `!699ca878`: one unique encrypted GPS report received through both G001/G002; 8 satellites, original GPS measurement age 35.40/35.41 seconds at subscriber receipt. Four source/gateway paths pass, no decoding errors. Duplicate gateway receipts are not four independent fixes or a sustained reliability rate.
- Private evidence: `private/bench/gps-mqtt-20261015T002434Z.json`; direct V4 snapshots in `gps-herrera/` show internal-GPS positions, and `herrera-saved/` verifies gateway settings. An earlier capture `gps-mqtt-20261015T002003Z.json` spans the hotspot transition and contains only B001 through both gateways (11 satellites, ages 50.81/58.76 seconds); superseded by the complete observation, not hidden as a successful four-path run. Raw coordinates stay ignored/private.
- Result: both real GPS sources automatically reach MQTT through both gateways on the replacement hotspot. The temporary subscriber saves test evidence and then exits; no continuous recorder or real portal ingestion worker is installed. Startup without a phone, sustained freshness/completeness, outage handling, runtime and field coverage remain to test. Heltec direct-TLS identity caveat remains unchanged.

### TEST-005 — Live portal GPS ingestion

- Date: 2026-10-14, America/Los_Angeles. Native Windows development and the existing Ubuntu LXC; two original V4s B001/B002 and two receive-only V3 gateways G001/G002 on stock `2.7.26.54e0d8d`. No RAK, additional hardware, firmware patch or outbound radio command.
- Owner replaces gateway Wi-Fi; both V3 saved network settings match privately and MQTT/LoRa configurations remain byte-for-byte unchanged, including transmit disabled. Owner restores B001 reporting after a quiet period. Initial 150-second no-traffic/partial windows and a failed all-tracker window are retained as failures, not counted as all-path passes. No live cutover occurs while those checks fail.
- Timestamp correction: the early adapter used `Position.time`, which source review establishes is a device/transmit clock. Those early small ages are **not** GPS freshness evidence. The final adapter uses `Position.timestamp` plus bounded millisecond adjustment and never substitutes device/receipt clocks. A regression test proves a recent transmit clock cannot refresh an old GPS solution.
- Final strict five-minute preflight: two reports from each tracker observed through each gateway, eight receipts across all four source/gateway paths, zero decoder rejections. Actual GPS-solution ages at receipt: 22.62/22.63, 6.31/6.31, 36.40/36.40 and 74.82/74.82 seconds. Source transmit-attempt denominator is unmeasured, so this is not a packet-delivery percentage or sustained freshness guarantee.
- Before cutover, private backup `meshlink-20261015T023712Z.tar.gz` passes checksum/integrity and isolated API recovery. The expected fictional dataset is transactionally archived/replaced by four verified devices; demo member accounts are disabled, real members/assignments remain empty and admin credentials are preserved. Simulation is explicitly disabled. The hosted service runs `mqtt_worker.py`, under `meshlink-worker`, with TLS hostname/certificate verification and a private durable receipt queue.
- Live portal API/storage verification: initially two positions and four receipts (two accepted/two duplicate), with one receipt for each source/gateway pair and one displayed observation per original packet. Latest stored GPS measurement ages at that check: B001 58.26 seconds, B002 155.26 seconds. After worker restart, three positions/six receipts remain available (three accepted/three duplicate); both trackers retain two-gateway deduplication and the authenticated feed returns online. No raw coordinates/keys appear in tracked evidence.
- New live backup `meshlink-20261015T024051Z.tar.gz` passes checksum, SQLite integrity and isolated API recovery: four accounts, four devices, zero members/assignments/messages/infrastructure observations/incidents/events, three positions and six packet receipts. Expanded backups include private worker configuration, queue and service definitions. Local API/proxy authentication boundaries, per-client throttling and credential-free public HTTPS/certificate/protected-route checks pass. The public browser entry renders the new sign-in-only page; authenticated live map/history browser review is still outstanding.
- Software checks: 36 backend tests pass on the LXC's Python 3.12 runtime with the isolated pinned MQTT dependencies, including encrypted-wire decoding, API retries, durable queue restart, subscription/outage state, transactional cutover rollback and stale timestamp behavior. Eight frontend tests, TypeScript and production build pass on pinned Node 22.23.1; existing MapLibre bundle-size warning remains. Shell/service/Python syntax and Git whitespace checks pass.
- Limits: no sustained field reliability, runtime, RF coverage, broker/Wi-Fi outage hardware test, phone-free cold start, full browser/device matrix or off-host backup demonstrated. Radio messaging, remote naming, member battery and infrastructure telemetry remain unintegrated. This completes receive-only bench GPS integration, not operational deployment readiness.

### TEST-006 — Saved SNNS interval and selected-controller admin bench

- Owner authorizes application-only flashing of R006 and G001/G002, with B002
  as the existing transmitting controller; preserve individual keys/profiles,
  keep both V3s receive-only and restore intended settings. One worker owns
  serial/admin access. No member GPS test, placement or server mutation.
- Reviewed firmware source `4c96b9ba0`; exact image/partition/hash checks and
  complete saved owner/security/channel/local/module comparisons pass through
  reboot. Full private gateway recovery images and concealed original/final
  profiles in 1Password Pilot are retained. B002 firmware/profile is unchanged.
- Seven actual R006 SNNS source gaps are **195 / 315 / 315 / 195 / 915 / 195 /
  195 seconds**, covering 180/300/900, lengthening, outstanding cooldown after
  shortening, saved reboot and return to 180. Matching serial/MQTT copies pass
  through both gateways. Each gateway supplies 39 local reports; consecutive
  source gaps within each observed boot are 75–76 seconds despite their
  different saved device-telemetry settings.
- Unauthorized PKI read is explicitly rejected; temporary B002 authorization
  permits encrypted read/change/readback. A 15-second remote reboot discards an
  uncommitted 300-second edit and recovers saved 180. Short rebooting commands
  can return `ADMIN_BAD_SESSION_KEY`; a 900-second save nevertheless executes
  and survives a distinct boot. Require independent result/boot checks rather
  than blindly repeating the write. The underlying transport cause and general
  app/CLI compatibility are unproven.
- Final all-board original-profile comparisons pass. R006 returns to
  device/power 180, environment off and its original empty admin allowlist;
  B002 is rejected again afterward. V3 TX remains disabled/local-only. All
  serial/subscriber sessions close. Exact clocks, paired receipts, capture
  fingerprints and failed/restored attempts are in the linked operation record.
- Result: selected cadence/profile/recovery checks pass with the admin ACK
  caveat. No forced relay excluding direct reception, authenticated portal
  acceptance, outage-age bound, calibrated current, battery-only duration,
  delivery percentage, independent RF silence or field coverage established.
  Next: forced-relay admin/interrupted-command test with a transmitting
  intermediate and robust operator-tool result handling.

## Copy for each test

### TEST-NNN — title

- Date and time zone:
- Question being tested:
- Acceptance criteria agreed before the run:
- Location/route and relevant weather:
- Member-node count and hardware IDs:
- Repeater and backhaul IDs:
- Firmware versions/commits and configuration reference:
- Test duration; who collected measurements:
- Positions expected / measured at source / received by dispatch:
- Position age at dispatch (distribution and worst observed; use measurement timestamps):
- Missing/duplicate positions and time windows without updates:
- Phone-free operation result:
- Communication attempts and acknowledgments, if tested:
- Internet outage and recovery observations, if tested:
- Battery start/end and power measurements:
- Raw evidence reference and sanitized summary:
- Result: pass / fail / inconclusive, with limits:
- Follow-up decision or corrective action:

## Reporting measures

Track member-device participation, coverage along tested routes, position age, delivery completeness, message delivery, mission runtime, repeater uptime during observed periods, and supported expenses. State the sample size and test conditions with each claim. An untested route or unobserved period has no measured result.
