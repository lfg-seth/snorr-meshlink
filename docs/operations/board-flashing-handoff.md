# Board flashing and configuration handoff

2026-10-19 owner override for the current bench rollout: program repeaters as **CLIENT**, with temperature/environment telemetry and **power telemetry disabled; no INA219 configuration**. [R001 reflash](r001-client-bench.md), [R002 reflash](r002-client-bench.md), [R003 reflash](r003-client-bench.md) and [R004 reflash](r004-client-bench.md) are completed locally with reboot/profile verification; other boards have not yet been updated. Apply this request when each subsequent board is identified, preserving its keys/channel/radio profile. Historical ROUTER and INA219 settings below describe earlier runs.

Dedicated debug receiver (2026-10-16): [Heltec V3 MC00 airtime sniffer](airtime-sniffer.md), `!9ea0432c` / last COM6, runs custom **`2.7.26.f95a443`** / `heltec-v3-sniffer`, separate from G001/G002. It exports every handled raw receive before routing/duplicate filtering and inhibits RF TX at compile time. Keep its receive-only profile and keys; stop the Windows/Linux sniffer before API/flashing operations. An ordinary V3 image removes that dedicated capture behavior. This image precedes the later INA219 source commit pinned by the shared submodule; preserve that newer project pin.

Updated 2026-10-16. Start here when a new chat is asked to flash boards, configure radios or verify their portal data. Read the repository's session-start instructions first. This document records the current handoff; a request to prepare notes does not itself authorize a hardware update.

INA219 audit: [R100 calibration, source defects and measurement evidence](ina219-audit.md). RAK calibration matches 0.1 Ω; the source fix corrects the environment/power union and multiplier consistency. Existing released/flashed images still write power channel 3. R004's historical +0.94–1.07 A versus owner-metered battery-only 8–16 mA remains unresolved; fresh USB readings near −5.8 mA do not validate the battery-only path. No corrective scaling or flash is implied.

R005 exception: [one-off dummy-load build](r005-preparation.md), `2.7.26.8dd4dac`, uses explicit target `rak4631-r005-load` to hold AIN1/GPIO31 HIGH during normal operation. It is flashed only on R005; ordinary released-image flashing remains unchanged. The latest source submodule includes the optional target, but the cached release's source/hash remain unchanged. INA219 reports near-zero current after battery removal, so the expected 50 mA load remains unverified.

Latest hardware evidence: [R004 preparation](r004-preparation.md) flashes the released prerelease, preserves device keys, enables/readbacks neighbor and 900-second device/environment/power telemetry, and verifies fresh G001 battery/weather portal ingestion plus archived SNNS delivery. INA219 local reports need wiring/calibration/channel interpretation; normalized current/neighbor decoding and fresh G002 delivery remain unverified. R001/R002/R003 are unchanged.

Subsequent [R002 update](r002-release-update.md): released prerelease installed with original local/channel/identity preservation verified through reboot. Owner confirms no external sensors; only device telemetry remains enabled at 900 seconds, with neighbor transmission enabled. Fresh G001 battery normalization/SNNS archive delivery and portal metadata/backup checks pass. R001/R003 are unchanged.

Portal follow-up: [RAK neighbor and sensor power ingestion](radio-report-ingestion.md) is deployed in `bed40dd`, with SNNS/standard neighbor normalization and signed, channel-preserving INA219 data. Archive recovery, fresh R005/G001 normalization and isolated backup recovery pass. Historical gap statements below describe the earlier flashing sessions; current polarity/calibration and fresh G002 delivery still need verification.

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
| Heltec V3 gateways G001/G002 | Last verified stock 2.7.26.54e0d8d. Both currently receive-only. One future transmitting gateway is authorized in the design, not yet provisioned for live portal downlink. | [Live MQTT configuration and limits](live-mqtt.md); [gateway Wi-Fi helper](../../scripts/bench/set-gateway-wifi.py). |

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
| Messages / remote names | Live worker remains receive-only; radio text and remote-admin execution are not integrated. Preserve receive-only gateways unless explicitly bringing downlink forward. Portal assignment labels remain independent of radio names. |
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
