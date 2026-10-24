# Board flashing and configuration handoff

2026-10-24 **G001/G002/G003/G004** now run checked **2.7.26.6fea6aa**
from published **6fea6aa68**: V3 target for G001–G003, OLED V4 target for
replacement G004 **`!699c2ed8`**. CLIENT, **LoRa TX enabled**, over-LoRa SNNS,
device telemetry **180 seconds**, and retained G003/G004 INA219 power **180
seconds** pass full intended-profile comparison through reboot. Preserve
individual keys, channel/radio power, Wi-Fi/MQTT and GPS pins/settings; MQTT
downlinks remain disabled. Real G001 Wi-Fi outage delivers health, telemetry
and SNNS through peers, raises a public portal warning and recovers after
exact network restoration. [Current hashes, acceptance and limits](gateway-backhaul-health.md#completed-bench-and-deployment---2026-10-24).
This **supersedes earlier receive-only/local-only gateway entries below**.
SNNS/health timing remains subject to jitter/scheduling and airtime admission.

2026-10-24 **B002 `!699ca878`** now runs selected original OLED V4 target
**heltec-v4-gateway / 2.7.26.a56466d**, published source **`a56466d8c`**.
The target enables SNNS while B002 retains its **CLIENT member profile**,
disabled Wi-Fi/MQTT, individual keys/private channel, 10 dBm configured RF
power/FEM and GPS **60-second acquisition / 120-second reporting**.
Device telemetry enabled at **180 seconds** and over-LoRa SNNS using the same
saved baseline pass complete intended-profile comparison through explicit
reboot; environment/power telemetry remain disabled. This supersedes all
historical B002 stock-image entries below. [Exact image, preserved profile and delivery evidence](b002-three-minute.md).

2026-10-24 **R002 `!b456f760`** now runs ordinary **rak4631 /
2.7.26.4c96b9b**, with complete original-profile preservation and intended
profile verification through explicit reboot. Owner confirms fitted INA219;
CLIENT, enabled device/environment/**INA219 power** telemetry at **180 seconds**
and private over-LoRa SNNS using the saved 180-second baseline are verified.
Preserve original keys/channel/radio settings and unset battery-INA address.
[Exact image, fresh delivery and limits](r002-three-minute.md). This supersedes
its earlier no-INA219 bench selection; physical path/calibration remains unknown.

2026-10-24 **R004 `!77fdb9f1`** now runs ordinary **rak4631 /
2.7.26.4c96b9b**, replacing its INA219 diagnostic image at the owner's request.
Application hash and complete original-profile preservation pass. CLIENT,
device/environment/**INA219 power** telemetry enabled at **180 seconds**, and
over-LoRa SNNS using that saved 180-second baseline pass full intended-profile
comparison through explicit reboot. Existing keys/channel/radio settings are
preserved. [Exact image, delivery evidence and limits](r004-three-minute.md).
Earlier diagnostic captures remain retained; physical calibration, bridge-state
confirmation and battery-only behavior remain unresolved.

2026-10-24 **G003 `!9e9f167c`** is commissioned from the Heltec factory demo
with dedicated **heltec-v3-gateway / 2.7.26.4c96b9b**, a complete original
flash backup and verified first-install images. CLIENT/receive-only private
pilot profile, supplied Wi-Fi, device/power telemetry enabled at **180 seconds**,
INA219 detected at 0x40, environment off and local-only collector pass complete
profile comparison through explicit reboot. Initial region setup automatically
enables TX; save TX disabled again after initial provisioning and verify it.
[Exact images, sensor/delivery evidence and remaining registration gates](g003-gateway-preparation.md).
G001/G002 retain their separate profiles below.

LOCAL-3 saved-interval source/build verification is recorded in
[repeater operations](repeater-update.md#saved-snns-interval-software-verification).
On that source, radio SNNS follows saved `telemetry.device_update_interval`
with RAK 180-second fallback/minimum, retained jitter/cooldown and explicit
long-interval saturation. Gateway local reporting remains 60 seconds plus
jitter with RF TX disabled. The source pin does not select a new image for
flashing; release artifacts, updater integration and selected-board/admin
acceptance remain separate. Historical entries retain their original image
and compiled-interval evidence.

2026-10-24 selected saved-interval bench: **R006 `!da581e5f`**, **G001
`!9ea13cc0`** and **G002 `!849ad7a0`** now run **`2.7.26.4c96b9b`** from
reviewed source `4c96b9ba0`, using ordinary `rak4631` and dedicated
`heltec-v3-gateway` respectively. Application-only image verification and
complete original profile/identity/key comparison pass through reboot. Both
V3s retain CLIENT, disabled LoRa TX, local-only SNNS and individual network
profiles. B002's existing stock V4 identity is the temporary radio admin
controller. [Exact images, measured behavior, recovery and limits](repeater-update.md#r006-and-gateway-admin-bench---2026-10-24)
supersede the older installed versions below for these three boards. This does
not publish release assets or change the production download pointer.

2026-10-23 owner-requested three-minute rollout: the new
[repeater updater and acceptance procedure](repeater-update.md) covers
R001–R006, preserving their identities/private profiles and fitted-sensor
exceptions. Ordinary source `0634b775f` is built; published release/download
verification and R006's private map placement remain pending. **R006
`!da581e5f` now passes the native Windows updater on ordinary
`rak4631 / 2.7.26.0634b77`**, UF2 SHA256
`0734127c43d85ef846caff0f161590183aea964268fcf8fdf1649142970cc9ba`.
CLIENT/device/power **180 seconds**, environment off, compiled private SNNS
180 seconds and standard NeighborInfo 21,600 seconds pass full intended
profile/identity/key verification through explicit reboot at
2026-10-24T00:51:19Z. Serial closed; first serial-only DFU failure is recovered
and the corrected API-driven UF2 path passes. Three automatic device/power/SNNS
cycles reach both gateways: device/power measurement gaps 180/180 s, private
SNNS 195/195 s including jitter. Portal acceptance and map write remain
pending server access. Only R006 is connected;
**R001–R005 remain unchanged**. The production release pointer remains unset
until publication passes; an explicitly selected,
checksum-verified [unpublished local bundle](repeater-update.md#explicit-local-bundle-while-public-publication-is-pending)
supports the remaining authorized board updates. This supersedes R006's
900-second installed profile below; [acceptance and limits](repeater-update.md#r006-installed-verification).

2026-10-23 R006 production exception supersedes its diagnostic-only profile
below: **R006 `!da581e5f`** now runs ordinary **`rak4631` / 2.7.26.09d8a9d**,
UF2 SHA256 `8429d164a70d9b3d7ef3d0f58d28c568dbe2cff51aa32ac6363071427314784e`.
This is a new ordinary build from the published pinned source, with INA219
fixes and no diagnostic/dummy-load flags; it is distinct from both the older
published prerelease and R004's same-version diagnostic target. Owner selects
**INA219 only, no temperature sensor**. CLIENT pilot profile, device and power
telemetry enabled at **900 seconds**, environmental measurement disabled;
private channel and newly initialized PKI pair persist through reboot. Local
fresh power replies verify **channel 1**. [Image, profile and acceptance](ina219-audit.md#r006-production-preparation--2026-10-23).
Other repeaters retain their separate current profiles.

2026-10-23 fresh-board diagnostic: owner-authorized new RAK19003/4631
`!da581e5f` / default `1e5f` now runs checksum-verified existing
**`rak4631-ina219-debug` / 2.7.26.09d8a9d**. **R006 remains provisional**.
Environmental measurement is enabled; region remains UNSET and no pilot
radio profile is applied. Identity/keys/channels are preserved; five automatic
upgrade-setting differences are explicitly recorded. Five fresh USB-charging
responses report **−270.7 to −279.4 mA / 3.844–3.848 V**; six initialized held
triples are stable and mathematically consistent. Physical calibration,
polarity and battery-only behavior remain unverified. Serial closed; retain
the diagnostic image for the next controlled comparison. [Image, profile,
measurements and limits](ina219-audit.md#fresh-rak190034631-comparison--2026-10-23).
R004 and all other boards are unchanged.

2026-10-21 R004 exception: owner activates the INA219 investigation and authorizes diagnostic flashing. R004 now runs **`rak4631-ina219-debug` / 2.7.26.09d8a9d**, with its complete original owner/keys/channel/local/module profile independently preserved. It logs continuous and held single-shot register snapshots, restoring sensor configuration before normal telemetry. Device/environment stay 900 seconds; power telemetry remains disabled and battery INA address unset. Correct R100 calibration is captured, but physical accuracy/current variation remain unresolved. Diagnostic image is retained for the next measurement; restore ordinary released firmware when collection is complete. [Audit, hashes and measurements](ina219-audit.md#r004-reinvestigation--2026-10-21). Other boards retain their prior state.

2026-10-19 gateway collector: **G001/G002** now run dedicated **`heltec-v3-gateway` / 2.7.26.9d2fd8f**, with enabled/local-only neighbor collection, CLIENT and LoRa TX disabled. Individual full identity/keys/intended profiles persist through reboot. Fresh own-observer measurements pass MQTT/archive/normalized and authenticated portal state for each gateway. Both gateway source IDs are registered in the live worker. [G001 image/profile/evidence](g001-neighbor-gateway.md), [G002 exact build/source/hash and evidence](g002-neighbor-gateway.md). This is separate from MC00 and the RAK prerelease.

2026-10-19 owner override for the current bench rollout: program repeaters as **CLIENT**, with temperature/environment telemetry and **power telemetry disabled; no INA219 configuration**. [R001 reflash](r001-client-bench.md), [R002 reflash](r002-client-bench.md), [R003 reflash](r003-client-bench.md), [R004 reflash](r004-client-bench.md) and [R005 reflash](r005-client-bench.md) are completed locally with reboot/profile verification. All five use ordinary released `2.7.26.0b65f2e`; R005's earlier GPIO31 HIGH dummy-load override is removed. Preserve individual keys/channel/radio profiles. Historical ROUTER, INA219 and R005 special-image settings below describe earlier runs; they are not the current bench profile.

Dedicated debug receiver (2026-10-16): [Heltec V3 MC00 airtime sniffer](airtime-sniffer.md), `!9ea0432c` / last COM6, runs custom **`2.7.26.f95a443`** / `heltec-v3-sniffer`, separate from G001/G002. It exports every handled raw receive before routing/duplicate filtering and inhibits RF TX at compile time. Keep its receive-only profile and keys; stop the Windows/Linux sniffer before API/flashing operations. An ordinary V3 image removes that dedicated capture behavior. This image precedes the later INA219 source commit pinned by the shared submodule; preserve that newer project pin.

Updated 2026-10-16. Start here when a new chat is asked to flash boards, configure radios or verify their portal data. Read the repository's session-start instructions first. This document records the current handoff; a request to prepare notes does not itself authorize a hardware update.

INA219 audit: [R100 calibration, source defects and measurement evidence](ina219-audit.md). RAK calibration matches 0.1 Ω; the source fix corrects the environment/power union and multiplier consistency. Existing released/flashed images still write power channel 3. R004's historical +0.94–1.07 A versus owner-metered battery-only 8–16 mA remains unresolved; fresh USB readings near −5.8 mA do not validate the battery-only path. No corrective scaling or flash is implied.

R005 exception: [one-off dummy-load build](r005-preparation.md), `2.7.26.8dd4dac`, uses explicit target `rak4631-r005-load` to hold AIN1/GPIO31 HIGH during normal operation. It is flashed only on R005; ordinary released-image flashing remains unchanged. The latest source submodule includes the optional target, but the cached release's source/hash remain unchanged. INA219 reports near-zero current after battery removal, so the expected 50 mA load remains unverified.

Latest hardware evidence: [R004 preparation](r004-preparation.md) flashes the released prerelease, preserves device keys, enables/readbacks neighbor and 900-second device/environment/power telemetry, and verifies fresh G001 battery/weather portal ingestion plus archived SNNS delivery. INA219 local reports need wiring/calibration/channel interpretation; normalized current/neighbor decoding and fresh G002 delivery remain unverified. R001/R002/R003 are unchanged.

Subsequent [R002 update](r002-release-update.md): released prerelease installed with original local/channel/identity preservation verified through reboot. Owner confirms no external sensors; only device telemetry remains enabled at 900 seconds, with neighbor transmission enabled. Fresh G001 battery normalization/SNNS archive delivery and portal metadata/backup checks pass. R001/R003 are unchanged.

Portal follow-up: [RAK neighbor and sensor power ingestion](radio-report-ingestion.md) is deployed in `bed40dd`, with SNNS/standard neighbor normalization and signed, channel-preserving INA219 data. Archive recovery, fresh R005/G001 normalization and isolated backup recovery pass. Historical gap statements below describe the earlier flashing sessions; current polarity/calibration and fresh G002 delivery still need verification.

## Default bench Wi-Fi

Owner selects the corrected, G003-verified network as the default bench Wi-Fi
on **2026-10-24**. Read its exact case-sensitive SSID and password from ignored
`private/bench/default-wifi.json` (`ssid` / `password`). Use this default when
provisioning a bench device or when the owner requests the default bench Wi-Fi;
an owner-supplied network override takes precedence. Ordinary updates preserve
the device's existing network unless reconfiguration is part of the request.

The same default is saved as concealed variables **MESHLINK_BENCH_WIFI_SSID**
and **MESHLINK_BENCH_WIFI_PASSWORD** in the **SNORR MeshLink — Pilot**
1Password Developer Environment. Use these named values when provisioning
another machine's private local copy. Existing gateway-specific settings remain
separate; saving the default does not update them automatically.

The local file matches G003's final profile through reboot and its successful
MQTT observation. Keep credentials out of Git and command output. This saved
preference does not change any currently configured board.

## Identify the requested board

1. Check project and firmware Git status, preserving unrelated edits. With clean checkouts, pull the project with `--ff-only` and initialize its pinned submodules. Use the pinned commit rather than `git submodule update --remote`.
2. Discover connected hardware and read node/USB identities. Match the requested device number, actual board revision, firmware target and fitted sensors. Old COM/tty names are hints only. Finish identification before selecting an image or opening a writer.
3. Privately back up its complete configuration, channel keys, security identity and current firmware/version. Record the image checksum and recovery method. Keep backups and raw observations under ignored `private/bench/`; another machine needs its own private material or an authorized transfer.
4. State the selected board/image and intended configuration changes. Carry out a user-requested normal firmware update and necessary reboot within that request; do not ask again solely because the operation was already authorized. A factory reset, identity/key replacement, changed regulatory region, changed target or additional board needs its own explicit scope. Never start flashing merely because this handoff exists.

For firmware tooling, read [firmware agent instructions](../../firmware/AGENTS.md) and their canonical `.github/copilot-instructions.md` before hardware work. Prefer the documented MCP tools when available; sequence all serial operations on each port. Older setup records containing factory resets describe recovery history, not the default update procedure.

## Select source and profile

| Board/function | Source and last verified hardware state | Configuration reference |
| --- | --- | --- |
| RAK4631 repeater, including R001/R002/R003/R004 | Download **2.7.26.0b65f2e** from the [pinned prerelease](https://github.com/lfg-seth/firmware/releases/tag/snorr-rak4631-2.7.26.0b65f2e-pre.1). Includes AHT detection fix, INA219 driver and passive neighbor reporting. **R002/R004 flashed/verified**; R001 remains stock 2.7.26.54e0d8d; R003 remains AHT build 2.7.26.cc5907b. | [Build/checksums](rak-neighbor-signals.md); [saved profile](rak-pilot-setup.md); [R002 update](r002-release-update.md); [R004 preparation](r004-preparation.md); [R003 evidence](r003-aht-build.md). |
| Original Heltec V4 member trackers B001/B002 | Last verified stock 2.7.26.54e0d8d. Identify original V4 versus V4-R8/display variants; a RAK UF2 is never a Heltec image. | [Heltec bench evidence](heltec-bench-checklist.md), [field results](../../records/field-results.md), [live GPS behavior](live-mqtt.md). |
| R006 selected interval bench | Ordinary `rak4631` 2.7.26.4c96b9b; intended device/power 180 seconds, INA219-only, saved-interval radio SNNS. | [Exact images, admin/cadence and limits](repeater-update.md#r006-and-gateway-admin-bench---2026-10-24). |
| Heltec gateways G001–G004 | G001–G003: `heltec-v3-gateway`; replacement G004: `heltec-v4-gateway`; all `2.7.26.6fea6aa`, CLIENT/private TX and over-LoRa SNNS, 180-second device/active power telemetry. Preserve individual profiles; no MQTT downlink. | [Current four-board evidence](gateway-backhaul-health.md#completed-bench-and-deployment---2026-10-24). |

For routine RAK flashing on any machine, **download and verify the published binaries; do not rebuild them**. After initializing the pinned submodule, run from the project root:

```sh
python scripts/bench/download-rak-release.py
```

The helper downloads the exact tagged UF2, Nordic OTA ZIP, manifest and checksums into ignored `private/bench/releases/snorr-rak4631-2.7.26.0b65f2e-pre.1/`. It checks the complete asset set, sizes and SHA256 against the Git-tracked manifest before reporting success. A subsequent run verifies and reuses that cache. A partial/corrupt cache fails closed; inspect it rather than flashing or silently rebuilding. Choose UF2 or OTA only after identifying the board and matching its update procedure; the helper never builds, flashes or resets devices. Use the verified image directly with its appropriate update procedure; avoid build-first upload wrappers for routine released-image flashing.

The binary source is `0b65f2e8444ea2dd3566f61ba2614d6eb33d3fd2`; the release tag/submodule tooling commit `8fe47325e38b82c8b2358293484ff845320d1be6` adds release automation/verification only. Do not rebuild at that later commit and call it the cached `0b65f2e` binary. Source development or a new target/build is a separate task, producing a new verified release. Original build logs remain desktop-local under `private/bench/rak-neighbors-0b65f2e/`. Neither asset verification nor build success establishes successful flashing or live data delivery.

### RAK neighbor update

Preserve the private channel/key, security identity, radio profile and visible ROUTER role. Existing bench profile is recorded in the RAK setup reference; reread actual settings rather than applying historical defaults wholesale.

- Explicitly enable `neighbor_info.enabled` for the companion collector. An isolated RAK requires `neighbor_info.transmit_over_lora=true` to send its observations through a gateway. Read both back after the configuration reboot.
- The new companion reports use private port 256 (`SNNS` v1), minimum five-minute radio cadence plus jitter/airtime deferral; local mode uses a one-minute minimum. They collect passive direct receptions, not active ping/pong. Standard NeighborInfo remains separate, with its six-hour default/four-hour minimum.
- Verify gateway handling of private-port packets; `CORE_PORTNUMS_ONLY` prevents their delivery. Stock gateways need no custom collector merely to forward a RAK report. Do not enable gateway radio transmission to solve an uplink-only task.
- The live worker still needs custom-report decoding. Radio/MQTT receipt can pass while the portal neighbor table remains empty. Use [the wire contract](../../firmware/SNORR_NEIGHBORS.md) and preserve hearing age separately from receipt time.

### Sensors and battery interpretation

The [inventory's INA219 wiring record](../../records/inventory.md) is authoritative for owner-reported placement: **battery → INA219 → RAK**. Treat it as battery/load-path sensing, not solar-input measurement. Exact board allocation, charger junction, shunt polarity and calibration still need identification. A series sensor measures current through that branch; do not claim whole-battery net charging current until the charge path is established. USB power can change the observed path.

INA219 detection/driver inclusion is confirmed by the RAK build. Actual voltage/current readings and the PowerMetrics channel mapping remain unverified. Inspect both the legacy EnvironmentMetrics writer and PowerTelemetry caller before assuming which channel carries the readings. Enable the appropriate fitted-sensor telemetry deliberately and verify the received packet's units/sign/channel against measurements. Do not derive current from voltage slope or label battery watts as solar watts.

Device battery-voltage reporting uses `telemetry.device_telemetry_enabled` and its interval. AHT reporting uses `telemetry.environment_measurement_enabled` and its interval; R003's last verified device/environment settings are 900 seconds. Power reporting has its own enable/interval options. Use fitted sensors only and preserve valid measurement timestamps; match portal health timeouts to verified cadence. The portal's battery type/capacity fields are metadata, not radio settings or measured remaining runtime.

## Portal gaps to carry into a new chat

This is an assessment from source inspection, not an instruction to implement every item during a flash:

| Feature | Current boundary / follow-up |
| --- | --- |
| Neighbor table/map | Add/test live custom-report decoding and gateway reception observations; current normalized adapter does not ingest them. Keep unknown identities/readings explicit. |
| INA219 mA / charging display | Adapter, ingestion validation and snapshot need current support. Current sign/channel and timestamps need bench evidence; displaying current is not enabled merely by compiling its driver. |
| Solar display | The reported INA219 placement does not measure solar input. Leave solar unavailable unless a verified measurement path exists. |
| GPS quality | Adapter supports PDOP and satellite count. Verify actual V4 position flags include the required fields and GPS measurement timestamp. HVDOP selects separate HDOP/VDOP instead of PDOP in the pinned build. Existing flags were deliberately preserved; configuration changes require the current task's scope. |
| Battery/weather health | Voltage and temperature/humidity ingestion exist. Verify fitted capabilities, calibration, valid/unknown clocks, saved intervals and corresponding missing-report/recovery rules. |
| Messages / remote names | Live worker remains receive-only; radio text and remote-admin execution are not integrated. Gateways now transmit their own radio reports; preserve disabled MQTT downlinks unless separately authorized. Portal assignment labels remain independent of radio names. |
| Intrusion | Needs fitted input hardware, selected device configuration and an event-to-portal mapping; UI capability alone does not supply events. |
| Gateway MQTT | Pinned gateway source logs credentials and uses `setInsecure()` for direct TLS. Keep logs private and address that gateway firmware issue before field rollout; the RAK neighbor build does not fix the stock V3 images. |

Source references: [MQTT adapter](../../backend/mqtt_adapter.py), [ingestion validation](../../backend/pb_hooks/ingest.js), [current display](../../portal/src/battery.ts), and the pinned firmware's INA219/PowerTelemetry/Position/MQTT implementations. Current source governs behavior; older operational notes may describe superseded integration stages.

## Finish the requested hardware task

1. After update/reboot, independently read back node identity, firmware version, complete intended profile and keys privately. Confirm preserved fields match the backup and only intended configuration differs. Keep debug API/logging in its intended final state.
2. Observe **new** packets after the update through each required gateway; exclude buffered startup/history packets. Verify values, source/observer/gateway identity and measurement/report/receipt clocks. Check the live portal separately from RF/MQTT receipt; unsupported data cannot pass a portal test.
3. Report actual results and limits: flashed/configured, local sensor read, direct RF receipt, MQTT receipt and portal ingestion are separate evidence. Short bench success does not measure runtime, solar sufficiency, field coverage or sustained GPS freshness.
4. Update [inventory](../../records/inventory.md), [field results](../../records/field-results.md), affected operation notes and [session log](../../records/sessions.md). Record exact source/image hashes, saved profile changes, verification and next step; publish coherent records while keeping raw data private.

## Suggested new-chat request

> Read `docs/operations/board-flashing-handoff.md` and the normal session-start files. Download and verify the pinned RAK prerelease without rebuilding. Identify connected R003, back up its profile/keys, then flash and configure that released image while preserving its identity, private channel and existing AHT telemetry. Enable neighbor reporting over LoRa and verify new packets through both gateways. Record any portal-ingestion limits separately. Do not factory-reset it or change other boards.

Replace R003 with the actual requested device. Starting a separate chat does not transfer ignored artifacts, credentials or serial access. Keep one active hardware writer per physical board.
