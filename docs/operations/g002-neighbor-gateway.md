# Heltec V3 gateway neighbor collector — 2026-10-19

## Wi-Fi replacement ? 2026-10-21

Owner requests replacement Wi-Fi on connected G002. COM6 independently identifies HELTEC_V3 `!849ad7a0`, still running **2.7.26.9d2fd8f**. Complete profile backed up privately before changing only owner-supplied SSID/password and Wi-Fi enablement. Credentials remain ignored under `private/bench/G002-wifi-20261021/`; network name/password are omitted here.

Independent readback after the network-setting restart matches complete saved user, channels, metadata, local and module configuration with only requested Wi-Fi fields changed. Identity/security keys, CLIENT role, disabled LoRa TX, neighbor collector and MQTT settings are preserved. Console observes Wi-Fi association/IP acquisition, `MQTT connected` and a queued publish. Initial verifier completes profile assertions but fails saving an unsupported optional status attribute; corrected independent rerun passes. Initial console connection evidence was observed during that first run; its raw log was overwritten by the rerun. No firmware flash, factory reset, other-device write or server change. Serial closes after checks. Short local success does not verify production ingestion, sustained delivery or resolution of [the earlier gateway outage](https://github.com/lfg-seth/snorr-meshlink/issues/40).

Subsequent same-day rollout: [G001 now runs the same verified image](g001-neighbor-gateway.md), with its own profile/keys preserved through reboot and fresh own-observer measurements accepted by the authenticated portal. Both gateway collector rollout checks pass. The G002 build and initial deployment evidence below remain unchanged.

Owner activates the same richer passive neighbor measurements on the gateways, with G002 connected. [Enable richer passive neighbor measurements on Heltec V3 gateways](https://github.com/lfg-seth/snorr-meshlink/issues/31) tracks rollout; [firmware PR](https://github.com/lfg-seth/firmware/pull/1) is merged into the existing `snorr/rak-survey` branch. G001 was still stock during this initial G002 run; the subsequent update is linked above.

## Source, image and preservation

Dedicated target `heltec-v3-gateway` enables the existing `USERPREFS_SNORR_NEIGHBOR_SIGNALS=1` collector. Ordinary V3 and dedicated sniffer targets are unchanged. Collector filtering, bounded storage, wire contract and RAK behavior are unchanged; see [SNNS contract](../../firmware/SNORR_NEIGHBORS.md).

- Binary source: `9d2fd8fd0025ccd658e383eaf6548c342a96e70d`; version **2.7.26.9d2fd8f**. Published branch/project pin `473a9ed41137f16a51c4962ffb5c186f53d046ae` adds only the pinned Markdown formatter correction.
- Application: `firmware-heltec-v3-gateway-2.7.26.9d2fd8f.bin`, **2,111,152 bytes**, SHA256 **`fe28db2e11a090c535e40003764038a0dc349430c753062906771b56b2ef7777`**. Build succeeds in 471.87 seconds with Espressif32 6.13.0 / Arduino ESP32 3.20017. Static RAM 132,096/327,680 bytes (40.3%); reported flash 2,110,725/3,342,336 bytes (63.2%). These are not peak-memory/runtime measurements.
- G002 independently identifies as **HELTEC_V3 `!849ad7a0`**, COM6, ESP32-S3 revision v0.2 / 8 MB flash. Original stock firmware `2.7.26.54e0d8d`, complete profile/keys and all 8,388,608 flash bytes are privately backed up. Original flash SHA256 `0a2ef6ab86cf846132d1115af4e1a3939342cec96cd0f181e670f2a92d8649cb`.
- Generated partition table exactly matches original partition bytes; OTA sequence 1 selects app0 at **0x10000**, size **0x330000**. Only the application is flashed, with esptool hash verification. Bootloader, partition table, NVS, filesystem and recovery application are retained. No reset of identity/keys or factory erase.
- Configure `neighbor_info.enabled=true`, `neighbor_info.transmit_over_lora=false`. Firmware persists standard NeighborInfo's six-hour default (`update_interval=21600`); custom local SNNS opportunities have their separate 60-second minimum plus jitter/scheduler delay. Preserve **CLIENT**, **LoRa TX disabled**, existing RF/region/channel/uplink/downlink/security/MQTT settings. Owner supplies replacement Wi-Fi after the prior saved access point is unavailable. Full independent user/channel/local/module comparison, including that deliberate Wi-Fi change, passes through explicit reboot.

The existing collector and actual-module C++17 harnesses pass under WSL GCC with address/undefined-behavior sanitizers, including capacities 32/10, local-only operation with TX disabled/CLIENT_MUTE, radio admission/cooldowns, bounds and rollover. Full gateway build succeeds; upstream library warnings remain. Trunk is unavailable locally; pinned Prettier 3.8.4 fixes the initial Markdown-only CI failure. Final PR Trunk, label and Semgrep checks pass. No full native/MCP hardware-suite result is claimed.

## Live delivery

Initial validating-TLS MQTT observation has zero G002 deliveries. Private console confirms RF reception/collector filtering, repeated Wi-Fi reason **201 (`WIFI_REASON_NO_AP_FOUND`)**, and no obtained IP. That code is verified against the installed ESP32 SDK header. Owner-authorized replacement Wi-Fi saves/readbacks with MQTT/LoRa settings preserved, restoring delivery.

The live worker previously accepted gateways only as transport identities, rejecting their original-source packets as `unknown source`. After the standard private backup, add the two existing verified node mappings (`!9ea13cc0` → `g001`, `!849ad7a0` → `g002`) to `/etc/meshlink/mqtt.json`'s infrastructure source mapping. Preserve every other config field and restart only `meshlink-worker`. No application source/schema/frontend deployment, raw archive replay or radio downlink is needed. Prior rejected envelopes remain archived unchanged.

At **19:42:36 Pacific**, a new non-retained encrypted SNNS packet **b92f2bfd**, sequence **1**, boot ID **1500438677**, reporter uptime **70 seconds**, identifies G002 as both original observer and transport gateway. Topic/envelope gateway IDs match. Live portal archive outcome is **normalized**, and its receipt is **accepted**, with a single report containing:

| Heard device | RSSI dBm | SNR dB | Hearing age at encoding, seconds | Observations |
| --- | --- | --- | --- | --- |
| R002 | -45 | 6.25 | 62 | 1 |
| R004 | -69 | 6.50 | 59 | 1 |
| R001 | -50 | 6.75 | 49 | 1 |
| B002 | -49 | 5.75 | 30 | 1 |
| R005 | -45 | 6.00 | 28 | 1 |

These are reported bench readings, not calibrated signal measurements or delivery percentages. Hearing age excludes transport delay and does not establish an absolute last-heard time. All five directional rows retain G002 as observer; no inferred relay route is claimed.

The 180.3-second validating-TLS observation contains **eight G002 deliveries**, including that self-originated SNNS report, with no decoder errors. Independent authenticated live snapshot checks find exactly the same five G002 direct SNNS rows, correct observer/transport provenance, null absolute hearing clocks and all nine configured devices retained. Database checks confirm both G001/G002 receipts for each of the three repeater packets below.

Fresh R005 **19:40:38**, R002 **19:41:39** and R001 **19:41:47** neighbor packets also arrive through G002. Their portal receipts are correctly marked duplicates of previously received packets, retaining per-gateway evidence without adding duplicate reports. A fresh B002 position packet is seen at MQTT but no member-location details are published here. Power telemetry remains disabled on the current repeater bench profile, so this does not complete the historical sensor-power acceptance in [Verify fresh G002 neighbor and sensor-power delivery end to end](https://github.com/lfg-seth/snorr-meshlink/issues/5).

## Recovery, limits and next step

Pre-change private backup: `meshlink-20261020T024151Z.tar.gz`, SHA256 `5f884a058ae86ac1a1081f5331016387e833c2b834ad8a28af9b4938ce688f44`. Post-change backup: `meshlink-20261020T024320Z.tar.gz`, SHA256 `49daf7d0b1a646e792c8939eecbc978677fb1a7672b08dce72e5db30c6051759`. Standard isolated database/API restore, integrity/credential/history preservation, all nine devices, public HTTPS/certificate/protected routes and authentication throttling pass. The restored backup includes 228 link observations and 3,532 exact MQTT archive entries. No live data is replaced by the recovery check.

Private build/image/manifest, original full flash/profile, replacement Wi-Fi, console, exact MQTT envelopes and portal evidence remain ignored under `private/bench/G002-neighbors-20261019/`. Remote original worker config is root-private under `/root/gateway-neighbors-20261019/`. The V3 image is cached locally, not published as a binary release; the RAK prerelease is not a V3 image. On another machine, use the exact binary source and gateway target with a new verified build, or an explicitly transferred matching image.

G001 was unchanged at the end of this initial run; its subsequent board-specific backup/update is linked above. Preserve each gateway's own identity/profile and check its Wi-Fi rather than cloning the other board's full configuration. Sustained cadence/freshness, outage recovery, radio-silence instrumentation, native authenticated visuals, runtime, calibration and field coverage remain unmeasured. A short console sample contains no Packet TX entries; saved TX-disable readback is not an independent RF-silence measurement.
