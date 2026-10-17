# Session log

## 2026-10-16 — Add RAK neighbor and sensor power ingestion

- Owner requests database/portal support for flashed RAK neighbor reports and INA219 sensors. Synchronize main, preserve the unrelated untracked battery-box model and retain the firmware pin. Add strict SNNS v1 and bounded standard NeighborInfo decoding, transactional private report/link storage and per-gateway receipt deduplication. Preserve unknown radio IDs, hearing ages/counts, boot/sequence/coverage metadata and unknown absolute hearing clocks.
- Normalize signed PowerMetrics channels 1–8 and legacy environment sensor voltage/current with independent field presence and original clocks. Future measurement checks use original receipt time, including replay. Show sensor/channel readings in Infrastructure and map node cards; extend neighbor tables/relationship cards and prevent delayed lower sequences from replacing newer same-boot reports. Do not map raw current to charging/discharging, battery voltage or solar output.
- Add dry-run-first, cutoff-bounded private archive recovery through normal ingestion. An isolated live database copy preserves all nine identities/configurations, accounts, assignments, positions and raw archive. Its 1,570 archived receipts yield 11 reports/15 directional rows and nine power supplements; second replay adds zero records (20 duplicates). R004/R005 power readings appear with literal channel/sign. Only G001 is represented; G002, calibration and field behavior remain unverified. [Contract and evidence](../docs/operations/radio-report-ingestion.md).
- Final LXC tests pass 57 backend and 45 frontend checks, TypeScript and production build, including final clock/order regressions; local decoder-only checks pass. Windows full checks are limited by missing frontend dependencies and sandbox temp/socket access. No hardware, profile, site or member data change.
- Publish/deploy application `bed40dd` after verified backup. Additive migration preserves all existing records in live and demo databases. Live archive replay accepts 12 reports/ten power supplements; fresh R005 power/neighbor normalization follows through G001. Final backup has 13 reports/21 link rows; all original protected/history/archive rows and device identities/configurations remain intact. Nine public assets, authenticated live state/feed, six services, public boundaries and isolated live/demo recovery pass. Restore verifies exact power/link metadata and zero-addition repeat replay (22 duplicates). [TEST-013](field-results.md#test-013--rak-neighbor-and-sensor-power-portal-integration).
- Initial demo readiness race recovers on bounded retry; private release-helper comparison/readiness errors are corrected without replacing live data. Native browser verifies published demo navigation/table/empty power state; populated fields are covered by DOM tests/live API. Sensor sign/calibration, fresh G002 and authenticated native/mobile visuals remain limited.

Next useful step: inspect the populated live UI on the owner's phone/browser, restore/verify fresh G002 delivery, and establish INA219 wiring/polarity/calibration before interpreting current as battery or solar behavior. Sanitized source/records are committed and pushed; raw captures/credentials remain private.

## 2026-10-16 — Recheck R005 with one full cell and a USB meter

- Owner reports replacing the disconnected batteries with one fully charged cell and observing 0.08 A on an inline USB input meter. Identify R005 on COM19, verify debug API remains off, refresh serial time and request fresh sensor data without a firmware/profile change.
- New PowerMetrics sample at epoch `1792206853` reports 4.200 V / −323.1 mA on the inherited observed channel 3; device voltage is 4.177 V. Preserve raw packet evidence separately from prior battery-disconnected captures. Record the USB reading as owner-observed total input; it does not isolate dummy-load draw or validate INA219 sign/calibration/common-path accounting.

Next useful step: establish the actual charger/INA219/load branch wiring and compare calibrated same-path measurements or a controlled load-on/load-off baseline. Expected 50 mA remains unverified; no charging-rate, endurance or calibration result claimed. Documentation/whitespace checks only; no build, flash or database schema change.

## 2026-10-16 — Build, flash and register R005 with an always-on dummy load

- Owner requests a one-off latest-project RAK build asserting the fitted dummy load while operating, then flashing the connected RAK as R005 and registering it at R001's saved location with INA219/temperature sensors. Read handoff/source instructions, synchronize clean repositories, preserve unrelated battery-box model. Identify RAK4631 `!f95b5501` on COM19; privately back up complete original configuration/keys. Owner confirms 2 kΩ base resistor to 2N2222 on RAK19007 AIN1.
- Publish firmware `8dd4dacef1cd7a6545983e3dc000ad533101113f` on authorized `snorr/rak-survey`: explicit `rak4631-r005-load` target holds P0.31 / GPIO31 HIGH at Arduino variant startup; ordinary RAK builds remain unchanged. Exclude conflicting Dropzone input use. Exact clang-format 16.0.3/whitespace checks, committed-source target build and linked startup/GPIO disassembly pass. Trunk unavailable. New version `2.7.26.8dd4dac`, UF2/OTA hashes and recovery evidence recorded in [R005 preparation](../docs/operations/r005-preparation.md).
- Match bootloader USB serial/RAK4631 board ID, flash verified UF2, apply saved pilot profile/name/900-second device/environment/power telemetry and neighbor transmission. Original US region and device security keys retained. Independent intended-profile/key readbacks pass before/after explicit reboot; final debug API off. A serial-close race after reboot raises an exception; independent post-reboot readback passes. No factory reset, bootloader replacement, other-board change or gateway configuration.
- Isolated database-copy identity rejection, idempotence and all-existing-device preservation pass. Apply identity-pinned manual registration, worker mapping and private recovery manifest; live authenticated state confirms nine devices and exact R001 planned-site equality, with unknown equipment/warnings disabled. G001 battery/weather normalization and SNNS/power archival pass; current/custom-neighbor normalized decoding and G002 delivery remain unverified. Final complete backup/public/authentication/isolated API-history recovery passes.
- Startup opens INA219 and AHT-family drivers. Initial current roughly −1.1 A at 4.184 V exceeds owner's expected 50 mA; owner suggests charging, disconnects batteries and confirms R100 shunt. Fresh post-disconnection local reports are −0.4 mA at 4.180 V and −0.3 mA at 4.188 V, with working temperature/humidity. Record measured reports separately from calibrated physical current; expected dummy-load draw is not verified. R005 database metadata captures this limit while all other device configurations are preserved. Raw data/keys/builds stay private.

Next useful step: establish whether battery removal also removed the dummy-load supply, then compare load voltage/current and INA219 readings with a meter under a known supply path. No field coverage/endurance, sustained cadence, sensor calibration or installed-site acceptance claimed. Source and project records are committed/pushed; see final response for project commit.

## 2026-10-16 — Update sensor-free R002 to released RAK firmware

- Owner connects R002 and requests update, confirming no external sensors. Preserve unrelated battery-box model; repository main is current. Identify COM9 RAK4631 `!b456f760`, snapshot entire current stock profile/keys privately, verify cached pinned UF2, match COM11/F: bootloader identity and install released `2.7.26.0b65f2e`. No rebuild/reset/key replacement, region or other-board change.
- Preserve exact original local configuration, channels, owner and hardware identity. Keep 900-second device telemetry; disable all external-sensor measurements and enable NeighborInfo/LoRa reporting at standard six-hour interval. Independent full readback passes before and after clock synchronization/explicit reboot. [Operation](../docs/operations/r002-release-update.md).
- Back up live portal, update only R002 firmware/no-sensor metadata through the local-only administration API and private provisioning manifest, preserving identity/site/equipment/other records. Authenticated portal and final backup recovery/public/proxy/authentication checks pass. No source/schema/frontend/worker identity change.
- Fresh R002 4.202 V device report reaches G001/MQTT and live normalized battery observation; fresh 40-byte SNNS v1 reaches G001/archive. No external-sensor report expected. G002 fresh delivery and normalized custom-neighbor decoding remain unverified. [TEST-011](field-results.md#test-011--r002-released-firmware-update-without-external-sensors).

Next useful step: verify the second gateway path and sustained reporting, or update the next explicitly requested board. No runtime/field coverage/calibration claim. Publish sanitized records; raw keys/settings/captures stay private.

## 2026-10-16 — Flash, configure and register R004

- Owner requests newly connected RAK as R004, latest firmware per notes, temperature sensor/INA219, and same location as R001. Read session/hardware instructions, preserve the unrelated untracked battery-box model, and fast-forward-check main (already current). Discover COM17 RAK4631 `!77fdb9f1`, formerly MR03/`2.7.17.36133d29d`, and privately back up the complete configuration/keys.
- Verify pinned cached release assets, identity-match COM18/RAK4631 UF2 bootloader and flash released `2.7.26.0b65f2e`; no rebuild/reset/key replacement or other board update. Set R004 naming and matching private pilot channel/radio, ROUTER/local-only, 900-second device/environment/power telemetry and neighbor transmit enable. Clear old fixed position, synchronize clock and independently verify the whole intended profile and original keys before/after explicit reboot. [Exact operation, hashes and evidence](../docs/operations/r004-preparation.md).
- Local temperature/humidity, battery voltage and INA219 legacy/PowerMetrics reports arrive. INA219 reports 0.008 V / about 1.6–1.9 mA while device voltage is about 4.1 V; wiring, calibration and the legacy union/channel mapping must be checked before battery-current/charging interpretation. No solar reading inferred.
- Add the guarded manual R004 migration after isolated invalid-identity/idempotence/preservation checks and backup recovery. Register R004 in live PocketBase/portal, copy only R001's private planned coordinates, record fitted sensors and leave R004-specific battery/antenna/solar unknown. Merge worker identity mapping, extend private provisioning manifest and verify eight-device authenticated state, preserved history, services, public boundaries and backup recovery. No application rebuild, demo change or new ticket decision.
- Fresh post-registration automatic battery packet (4.143 V) and environment packet (26.510239°C / 21.435547% RH) reach G001/MQTT and accepted live R004 observations with valid measurement clocks. A 40-byte SNNS v1 companion reaches G001/MQTT/archive; normalized neighbor/current decoding remains unsupported. G002's last receipt is October 15, so its fresh path and two-gateway deduplication are not verified. [TEST-010](field-results.md#test-010--r004-released-firmware-and-live-registration).

Next useful step: check INA219 wiring and meter readings on the intended power path, then restore/verify G002 delivery. Portal current/custom-neighbor decoding, sustained cadence/runtime, native browser visuals, site permission/installation and field coverage remain outstanding. Raw keys, tracks, exact locations and capture/configuration evidence stay private; stock counts/purchases are unchanged.

## 2026-10-16 — Publish cached RAK prerelease and download-first flashing

- Owner authorizes fixing inherited release automation, publishing the cached RAK build on their firmware fork and making future chats download it. Claim/resolve [Publish the cached RAK build as a fork prerelease](../.scratch/pilot/issues/22-rak-prerelease.md). Verify retained UF2/OTA ZIP against recorded sizes/hashes; reuse the exact tested bytes without rebuilding. Owner signs into GitHub to enable the authorized asset upload; no credentials are exposed or committed.
- Publish firmware release-only commit `8fe47325e38b82c8b2358293484ff845320d1be6` and tag `snorr-rak4631-2.7.26.0b65f2e-pre.1` on `snorr/rak-survey`. Gate all six upstream release jobs to `meshtastic/firmware`; add a read-only SNORR asset verifier, tracked manifest, integrity tests and release notes. Cached binary source remains `0b65f2e8444ea2dd3566f61ba2614d6eb33d3fd2`; the verifier rejects additional firmware/build-input changes between that source and the tag. No history rewritten.
- Publish [the RAK4631 prerelease](https://github.com/lfg-seth/firmware/releases/tag/snorr-rak4631-2.7.26.0b65f2e-pre.1) with UF2, Nordic OTA ZIP, build-manifest.json and SHA256SUMS, explicit bench/hardware-unverified status and source provenance. Public download/byte/hash/manifest checks and repeat-run cache reuse pass. [GitHub run 38994730691](https://github.com/lfg-seth/firmware/actions/runs/38994730691) succeeds: SNORR verification passes; Docker/PPA/OBS/COPR/upstream website/version-bump jobs all skip.
- Update the firmware pin, AGENTS/project/operation/handoff notes and add `scripts/bench/download-rak-release.py`. Routine flashing downloads/checks pinned assets into ignored private cache; it does not rebuild or flash. Six verifier regressions and YAML repository/permission checks pass; use pinned Black 26.5.1 with Trunk unavailable. Verify documentation links/whitespace; preserve the unrelated battery-box file. No binaries, private profiles, raw logs/tracks or credentials enter Git.

Next useful step: use the download helper in a named-board flashing chat, preserve identity/configuration and verify new RF/MQTT/portal evidence separately. No hardware flash, device configuration, sensor calibration, field/runtime test or portal deployment performed.

## 2026-10-16 — Save a reusable board flashing and configuration handoff

- Owner clarifies INA219 placement inline between battery and RAK and asks whether a new chat can recover the flashing/configuration notes. Record that owner-reported wiring in inventory without inventing sensor counts, per-board allocation, charger junction, polarity/calibration or measured current. Treat the sensor as battery/load-path sensing; total battery charging/discharging interpretation awaits the actual charge path, and solar-input measurement is unsupported by this placement.
- Existing RAK source/build evidence and checksums were already published in project commit `3756b0b` and firmware `0b65f2e84`. Add [Board flashing and configuration handoff](../docs/operations/board-flashing-handoff.md) as the single starting point for future chats, linked from AGENTS.md, README and development handoff. Record the owner-authorized firmware fork destination to prevent repeating the resolved publishing question.
- Save the previously chat-only portal-gap assessment: neighbor/current ingestion, INA219 packet channel/sign verification, GPS quality flags, sensor cadence/health clocks, live messaging/admin gaps, intrusion mapping and pinned gateway TLS/logging issue. Separate current support from pending integration; link source and measured evidence. Include a scoped example request for R003 that preserves keys/profile, performs the intended normal update and verifies new gateway traffic without a factory reset.
- Documentation/inventory only: no firmware, configuration, hardware state, source pin, live service, tracker decision or credential changed. Check local documentation links and Git whitespace; preserve the unrelated untracked battery-box model.

Next useful step: in a new chat, request a named board update using the handoff. Rediscover the board, privately snapshot configuration and choose the pinned target before writing; verify RF, MQTT and portal ingestion separately and record measured outcomes.

## 2026-10-16 — Implement passive RAK neighbor signal reports

- Owner asks whether the RAK branch already has richer neighbor signal information and brings implementation forward if missing. Fetch both remotes; firmware `snorr/rak-survey` remains at `cc5907b1f`, containing the AHT fix only. Claim [Improve passive neighbor signal reporting in the RAK fork](../.scratch/pilot/issues/21-rak-neighbor-signals.md). Preserve the unrelated untracked battery-box model.
- Commit firmware source `0b65f2e84`: primary-channel direct-reception RSSI/SNR, monotonic hearing age and accepted observation counts; bounded 32-entry table, least-recently-heard eviction, 30-minute expiry and rotating eight-row/152-byte private-port companion reports. Retain AHT support and standard GPS/NeighborInfo. Existing enable/transmit settings gate the module; no saved radio setting changed. Background priority, jitter, airtime admission and five-minute radio minimum keep diagnostics conditional. [Contract and rollout boundary](../docs/operations/rak-neighbor-signals.md).
- Collector and actual-module harness checks pass with address/undefined-behavior sanitizers, including zero/negative SNR, unknown/relayed/MQTT rejection, encoding, bounded rotation/eviction, expiry, primary-channel/configuration/airtime/role gates and cooldowns across timer rollover. Collector passes capacities 32 and 10. Trunk is unavailable; exact clang-format 16.0.3 repository configuration and whitespace checks pass. Initial target compilation caught an incorrect packet-release API call, fixed before the commit. Final committed-source build succeeds as `2.7.26.0b65f2e`: 759,256 bytes flash, 105,252 bytes static RAM. Preserve artifacts/log/checksums privately and record hashes in operations; runtime allocation peaks remain unmeasured.
- Automatic approval review initially rejects pushing to `git@github.com:lfg-seth/firmware.git` because standing publication authorization names the project repository. Owner first requests keeping the work in this repo, then identifies the firmware fork and explicitly authorizes pushing there. Remove the temporary patch packaging/version-helper change; push succeeds on `snorr/rak-survey`, with a clean firmware checkout and exact local/remote commit match. Pin the published firmware in this repository and resolve the source task. No history rewrite.

Next useful step: separately implement/test portal `SNNS` decoding and arrange an authorized bench flash with both-gateway delivery/GPS-airtime-runtime comparisons. No hardware flash, gateway provisioning, portal deployment, measured RF delivery or field validation performed. The unrelated battery-box model remains outside the commits.

## 2026-10-16 — Deploy demo-first entry and iPhone login fix

- Owner requests push and deployment. Commit/push application source `60ea977` to `origin/main` and deploy its frontend source/static assets to the LXC. Anonymous production entry now opens the separate database demo with Sign in at the top; live session restoration and independent API routes remain intact. Username/password inputs have a minimum 16px font. No backend/schema, radio or provisioning change.
- All 43 frontend checks, typecheck and live build pass on the pinned server runtime after adding the same commit's synthetic test fixture to staging. All nine released files match through public HTTPS; public synthetic sign-in/state and the published input font rule pass. Live state/device identity, worker heartbeat, protected routes, authentication throttling, demo isolation and all six services pass. Pre/post-release backups pass isolated live/demo database/API/history recovery, preserving the MQTT archive. [Release and rollback evidence](../docs/operations/portal-lxc.md#demo-first-entry-and-iphone-login-fields--2026-10-16).
- Native browser inventory is empty; iPhone focus/keyboard and visual behavior remain unverified. Preserve the concurrently added branch-build/automatic-deployment session note outside these commits. Existing bundle-size warning remains; no fresh radio reception or field-performance verification claimed.

Next useful step: open the public site on iPhone, confirm automatic demo entry and top-header sign-in, then focus/dismiss both login fields and verify manual pinch zoom. Publish deployment evidence separately from the application release.

## 2026-10-16 — Default to the database demo in production builds

- Owner requests demo-first startup even in production, retaining Sign in at the top. Remove the live-build restriction from anonymous demo startup and relabel the existing header action **Sign in**. Keep the production build's live account form and independent demo API routing; saved live tokens still undergo server validation before opening the live workspace. Anonymous refresh returns to the demo; sign-out clears the live token and offers the account form/View demo.
- Keep Sign in available while the demo loads; cancel the pending demo attempt when it is selected so a late response cannot replace the account form. Failed or misdirected demo responses expose sign-in without rendering fallback fixtures. Preserve the preceding iPhone input-font fix.
- Update the real-application DOM regression for production demo startup, header placement, refresh, demo read/write isolation, unavailable/misdirected databases, cancellation during loading and live sign-in restoration/rejection. The changed test fails before the application fix and passes after it. `npm run check` passes all 14 reported frontend test files, typecheck and the default live production build. Whitespace checks pass; existing MapLibre size warning remains. Native browser/iPhone visual and keyboard behavior remain unverified.

Next useful step: deploy both portal changes and verify anonymous demo entry, top-header sign-in and iPhone field focus on the public site. Local source/build only; no commit, push or deployment performed.

## 2026-10-16 — Prevent iPhone sign-in field focus zoom

- Owner reports iPhone automatically zooming into the mobile login fields. Those fields inherit the assignment form's `0.77rem` text size (about 12px at the default root size). Add a scoped `.backend-login input` font size of `max(16px, 1rem)` so both fields remain readable without reducing larger user font settings. Preserve the existing viewport and manual pinch zoom.
- `npm run check` passes all 14 reported frontend test files, typecheck and production build; `git diff --check` passes. Existing MapLibre chunk-size warning remains. Native iPhone focus/keyboard behavior is not reproduced or verified here; no artificial CSS-only regression test added for browser behavior. [WebKit focus-zoom implementation](https://github.com/WebKit/WebKit/blob/main/Source/WebKit/UIProcess/ios/WKContentViewInteraction.mm) uses the focused field's font size when revealing it.

Next useful step: deploy the CSS fix and verify username/password focus, keyboard dismissal and manual pinch zoom on an iPhone. Local source/build only; no commit, push or deployment performed.

## 2026-10-16 — Publish and deploy accumulated local changes

- Owner requests pushing and deploying all local changes. Commit/push application release `3ca3a94` to `origin/main`, retaining tracking against `origin/main`. Include GPS quality, separate database demo, neighbor table/signal map, card mini maps/labels, battery history, research/tracker records and the existing clean stock-firmware submodule pointer. No hardware flash or monitoring-stack implementation performed. Use the repository's established author identity for this commit because this machine has no Git identity configured.
- Frontend tests/typecheck/live production build and all 52 backend checks pass locally and on the LXC; its pinned Node runtime reports 43 frontend checks. The initial restricted backend run could not open localhost sockets; the authorized rerun passes. The known MapLibre bundle-size warning remains. Both additive migrations pass on a private live database copy and on the live database, preserving fingerprints of every pre-existing operational table and all seven device identities. Live signal rows remain empty.
- Deploy exactly committed application source to the owner-authorized LXC. Add the separate `meshlink-demo` OS account, loopback API and synthetic worker, independent state/binary and `/demo-api` Nginx proxy. Verify live/demo tokens and OS access boundaries; keep worker/administration/raw collections private. Public synthetic demo sign-in, history and all nine build files pass through HTTPS; live authenticated state, worker heartbeat, all 15 history queries, proxy boundaries, authentication throttling and all six services pass. [Release/backup evidence](../docs/operations/portal-lxc.md#gps-neighbor-maps-battery-history-and-database-demo-release--2026-10-16).
- Retain rollback source/assets/configuration at `/opt/meshlink-rollback-3ca3a94` and the staged tested build at `/opt/meshlink-release-20261016`. Pre-release backup restores successfully. The first post-release demo recovery check catches an older installed backup helper: install the updated `/usr/local/sbin/meshlink-backup` used by systemd and take a corrected complete backup. Replace the verifier's incorrect fixed sample-count expectation with exact comparison to saved samples. Final backup `meshlink-20261016T211956Z.tar.gz` passes checksum and isolated live/demo database/API/history recovery, including the private MQTT archive.
- Existing archive verification checks 200 recent envelopes/binary lengths with SQLite integrity good and no queued receipts. No new MQTT archive receipt arrives during the 60-second post-release observation window, so fresh radio ingestion and new quality-bearing fixes are not revalidated; the broker-connected worker heartbeat passes. Native browser/WebGL/mobile review remains unverified because browser inventory is empty; real neighbor ingestion, field validation and off-host backup remain open. Raw state, credentials and tracks stay outside Git.

Next useful step: visually review the deployed map, node/relationship cards and battery periods on desktop/mobile, then verify new GPS-quality-bearing packets when the bench reports. Real neighbor ingestion remains a separate integration; monitoring choices remain open and parked firmware/wishlist work stays parked.

## 2026-10-16 — Explore private Meshtastic monitoring and recording

- Owner invokes Wayfinder to investigate current Meshtastic monitoring/Grafana projects and setup requirements. Claimed [Check Meshtastic monitoring and recording stacks for the pilot](../.scratch/pilot/issues/19-meshtastic-monitoring-research.md); research completed in an isolated worktree/branch, preserving all unrelated staged and unstaged changes. Resolved the research only; no implementation decision is resolved.
- Primary-source comparison identifies MeshMonitor's standalone subscribe-only MQTT, Prometheus/Grafana assets and Proxmox LXC template as the leading packaged trial; tcivie's encrypted MQTT/TimescaleDB/Grafana bundle is the SQL alternative. MeshView/Malla need TLS adaptation in inspected clients; hacktegic's exporter skips encrypted packets. Source findings are not runtime compatibility tests.
- Record a [proposed private setup](../docs/research/meshtastic-monitoring-setup.md): preserve exact PocketBase archiving and portal GPS semantics, distinguish numeric metrics from logs, evaluate a private read-only collector, and verify dual-gateway receipt/dedup behavior and timestamps. Existing 4-CPU/8-GiB/64-GiB allocations are recorded; current free headroom is unmeasured. Loki/Alloy can follow metrics; retention/access/hosting remain proposals.
- Push the primary-source report on `research/meshtastic-monitoring-20261016`, commit `f69b6a4`; no PR/merge. Create [Choose a private monitoring scope and pilot stack](../.scratch/pilot/issues/20-monitoring-scope-stack.md) as the owner decision after the research. No radio, firmware, MQTT ACL, production service, inventory, expense or notification integration changed; parked wishlist and fork work remain parked.

Next useful step: choose whether to evaluate MeshMonitor plus Prometheus/Grafana first, or a narrow exporter on the existing worker, and whether log search belongs in that initial evaluation. Research-branch publication status is recorded in the research ticket; the main-worktree setup/tracker/session edits remain uncommitted. No application or hardware tests run; documentation/link and whitespace checks only.

## 2026-10-16 — Attempt to inspect legacy MQTT messages

- Owner requested a quick private inspection for the latest old messages and timestamps. SSH to the broker succeeds using the recorded port, but root-only archive inspection stops at `sudo: a password is required`. No archived file metadata, logs or payloads were read; no live broker changes made.
- Network sandbox required an approved external SSH call; the default local SSH configuration also has a permissions error, bypassed with `-F /dev/null`. Archive content and recoverable timestamps remain unknown.
- Owner supplied a privileged listing and latest-log tail: archived `mosquitto.db` is 47 bytes; logs include the current file, `.1`, and six compressed rotations. Mosquitto 2.0.18's [persistence writer](https://github.com/eclipse-mosquitto/mosquitto/blob/v2.0.18/src/persist_write.c) and [fixed structures](https://github.com/eclipse-mosquitto/mosquitto/blob/v2.0.18/src/persist.h) make 47 bytes consistent with header/configuration only, indicating no saved message records (inferred from size, not a binary parse). Supplied tail contains saves, failed connections, restarts and the audit rejection, with no successful message receipts. Final shutdown/save was October 13 at 13:44:08 Pacific; this is not a last-message timestamp. No remote IPs or raw log lines copied into Git.

Next useful step: search all archived log rotations for successful client connections or any PUBLISH logging to establish the latest recorded legitimate activity; ordinary log levels may not establish last-message time or contents. Existing unrelated edits preserved; no commit or push requested/performed.

## 2026-10-16 — Clarify legacy Mosquitto archive and message history

- Confirmed from the recorded October 13 reset and its installer that legacy configuration, data and logs were moved to the broker's private `/root/meshlink-archive/mqtt-legacy-20261013T204408Z` after stopping Mosquitto to flush persistence. Archive contents and recoverable message counts remain uninspected; this review did not access the server.
- Checked the official Mosquitto configuration/MQTT manuals: retained messages and persistent-session queues can preserve limited message state; broker persistence is not a complete traffic history. The fresh broker installer enables persistence. Separate full-payload worker archiving began October 15 and only covers delivered traffic, subject to broker ACLs and delivery gaps.

Next useful step if historical recovery is requested: inspect the legacy archive's file metadata and any persistence database privately, without changing the live broker. Existing unrelated edits preserved; no commit or push requested/performed.

## 2026-10-16 — Minimal battery history on repeater and gateway cards

- Add a compact voltage chart to repeater/gateway map cards and reuse it in Infrastructure battery detail. Provide 24hr/7day/30day buttons, small axis values and a single smooth monotone line without dots, grid, area fill or cursor. Curves stay within adjacent readings and leave battery missing-timeout gaps disconnected. Keep unknown/invalid/future readings out of the plot; preserve current/stale/offline indications and recent exact readings in the detail disclosure.
- Add an authenticated, no-store, on-demand history route and device/time index migration. Admin/member access follows the existing infrastructure snapshot; worker/anonymous access is denied. Bound each period to the latest 50,000 observations with explicit truncation. Refresh selected history once a minute, merge recent snapshots, abort obsolete device/period requests and retain loaded readings on refresh failure. The ordinary two-second state snapshot remains small.
- Rebuild the synthetic checkpoint with 17,283 timed voltage examples covering 30 days: Demo ridge relay recovers daily with sun cycles, Demo canyon relay shows daily charging but a roughly 0.51 V monthly deficit, and Demo dispatch gateway stays nearly steady. Update the simulation worker to continue all three patterns from a persisted/rebased scenario clock. These are fictional examples, not solar sufficiency diagnoses or measured runtime.
- Back up the running local demo privately, refresh only its illustrative voltage history/configuration, and restart its verified launcher so the new route and worker are active at localhost:5173. Through the actual frontend proxy, verify all three periods, separate simulation identity and online feed. Saved members, assignments and neighbor observations exactly match the pre-refresh backup; synthetic checkpoint checksum and SQLite integrity pass.
- Frontend checks/typecheck/default live build and all 52 backend checks pass, including real-database history windows/access, solar cycles/deficit, curved bounds/outage gaps and rapid period/device switches. Native browser visual review remains unavailable (empty browser inventory); existing MapLibre bundle-size warning remains. Preserve prior staged/unstaged edits; no production deployment, hardware change, commit or push requested/performed.

Next useful step: review repeater/gateway cards in the running local demo, comparing 24hr with 7day/30day on the two relays. Deploy the history hook and index migration with the frontend when a release is requested.

## 2026-10-16 — Match mini-map marker styles and states to the main map

- Replace the generic mini-map badge with the main map's shared marker classes/CSS. Share class selection for client GPS age and infrastructure type; tracker and infrastructure node cards retain the matching selected outline. Relationship endpoints use their own current status and update as time or position records change. Preserve assigned member shortnames, map framing, signal lines and button-free mini maps.
- Regression checks compare actual main/mini marker classes and computed colors, dimensions, shape, borders, shadows and selected outlines. Cover Active/Recent/Stale/No Location transitions in relationship and node cards, plus Users and gateway styling. Frontend tests, typecheck, production build and whitespace checks pass; the existing bundle-size warning remains. Native WebGL/visual review remains unverified. Preserve unrelated edits; no deployment, database/radio change, commit or push performed.

Next useful step: visually review matching marker states in local node and relationship cards.

## 2026-10-16 — Assigned member shortnames on card mini maps

- Reproduce the owner's reported mismatch in the actual Map card: the main marker displays the assigned member shortname ALIAS while its mini map displays S001. The tracker mini map directly used the device shortname, and relationship mini maps used device-labeled endpoints. Reuse the existing assignment-aware map-label function for Map/Users tracker cards and client endpoints in relationship mini maps. Device shortnames remain the fallback when no active member shortname exists.
- Add regression checks for assigned clients, relationship endpoint labels, assignment release restoring the device label and Users cards. Observe the ALIAS-versus-S001 assertion fail before the fix. Frontend tests, typecheck and production build pass; whitespace checks pass. DOM adapters verify labels; native visual review remains unverified and the existing bundle-size warning remains. Preserve unrelated edits; no database/radio change, deployment, commit or push performed.

Next useful step: review assigned client markers in the local node and relationship cards.

## 2026-10-16 — Minimal maps in node and relationship cards

- Add a lazy-loaded mini map to tracker/member-client and infrastructure detail sheets, including gateway/router cards and tracker cards opened from Users. Each shows only its node. Relationship cards show just the two endpoints and their existing signal-colored connection, independently of the main signal overlay. Reuse the main map style and worker setup; share Topo/Aerial imagery selection across cards and page navigation for the current app session.
- Center single nodes and fit both relationship endpoints with padding and a zoom cap, including on sheet resize. Keep panning/touch zoom available, omit map buttons, preserve visible USGS attribution and allow card scrolling over maps. Separate labels for co-located endpoints. Unknown/invalid positions remain explicit; missing endpoints never produce invented locations or lines. Existing planned/recorded-location details remain available.
- Frontend tests, typecheck and production build pass, including marker isolation, framing, line geometry/color updates, synchronized basemap changes, gateway cards, Map-to-Users navigation and unknown positions. DOM/MapLibre adapters verify behavior; browser inventory is empty, so native WebGL, tiles and desktop/mobile visual review remain unverified. Existing bundle-size warning remains. Preserve unrelated staged/unstaged work; no deployment, database/firmware change, commit or push performed.

Next useful step: visually review single-node and relationship mini maps in the local demo on desktop/mobile.

## 2026-10-16 — Restore assigned-device map shortnames in the database demo

- Reproduce the S00X fallback against the tracked synthetic database and the actual map-label function: all five saved member shortnames were blank after replacing browser fixtures with database-backed demo state. Assignment lookup and marker rendering still worked; existing UI tests supplied their own member shortnames and missed the checkpoint omission.
- Seed AVERY/JORD/MORG/RILEY/CASEY in the demo generator and rebuild its synthetic checkpoint/manifest. Restore only blank shortnames for matching fictional members through the running local demo API; preserve saved assignments and signal edits. Verify the frontend's `/demo-api` proxy now yields AVERY/JORD/MORG/RILEY for assigned devices and S005/S006 for unassigned ones. No production or radio changes.
- Add a regression test that reads saved members/assignments/devices from the actual checkpoint and runs the map-label function. Observe the exact failure before fixing it. All 41 frontend tests, typecheck/build and three demo-database integration checks pass; whitespace checks pass. Existing MapLibre bundle-size warning remains. Native browser visual review remains unverified. Preserve unrelated staged/unstaged work; no commit or push requested/performed.

Next useful step: review the restored names in the running local map; its normal polling reads the corrected saved records.

## 2026-10-16 — Rename node-card list to Neighbors

- Replace the map node-card heading and accessible section label Relationships with Neighbors, and align the empty-state message, existing test expectation and portal guide. Text-only change; whitespace checks pass. No tests rerun, deployment, commit or push performed; unrelated edits preserved.

Next useful step: review the Neighbors list in the local demo.

## 2026-10-16 — Relationship card endpoint buttons

- Extend [Show neighbor signal connections on the map](../.scratch/pilot/issues/18-map-neighbor-signals.md) with two Open [node] buttons at the top of each relationship card. Each opens its tracker or infrastructure card in place; its relationship row can return to the relationship card. Reuse tracker marker-selection behavior, including parent selection and trail clearing, and retain exactly one open card with the overlay either on or off.
- Frontend tests, typecheck and default live build pass, including navigation through both endpoint buttons and back through relationship rows on desktop/mobile dialog APIs. Whitespace checks pass; native browser visual review remains unverified and the existing MapLibre bundle warning remains. Preserve unrelated edits; no service start, deployment, database/firmware change, commit or push performed.

Next useful step: review node → relationship → either node navigation visually in the local demo.

## 2026-10-16 — Simplify signal lines and add node relationships

- Refine [Show neighbor signal connections on the map](../.scratch/pilot/issues/18-map-neighbor-signals.md) at the owner's request: remove all line labels, retain colored/selectable lines, hide legend explanations behind an accessible info button and place the legend outside toolbar flow so only its own box expands. Align toolbar controls at the top to prevent stretched buttons.
- Preserve tracker/infrastructure marker selection above line targets by stopping marker click propagation and ignoring marker-originated layer clicks. Map node cards now show only a relationship and colored SNR pill per relationship row; selecting the row opens the full relationship sheet. Lists and details work with the overlay off and with known endpoints lacking coordinates. Turning the layer off changes visibility without dismissing cards. No readings or explanatory copy are added to the compact rows.
- Frontend tests, typecheck, default live build and explicit demo build pass, covering no map labels, collapsed/revealed legend help and isolated CSS layout, marker click precedence, compact tracker/infrastructure relationship rows, relationship selection on desktop/mobile, retained offline/live updates and access without GPS or the overlay. Existing grouping/timestamp/unknown-value checks remain passing. Native visual/WebGL review remains unverified; existing MapLibre bundle warning remains. Preserve prior edits; no database/firmware change, service start, deployment, commit or push performed.

Next useful step: review the simplified map and node-to-relationship interaction visually in the database demo.

## 2026-10-16 — Map neighbor signal overlay

- Implement [Show neighbor signal connections on the map](../.scratch/pilot/issues/18-map-neighbor-signals.md): Show/Hide signal strength toggle beside and styled like Fit area, colored geographic lines, directional SNR label buttons and selectable responsive detail sheets. Use the existing authenticated/demo API link records; preserve unrelated edits.
- Group one connection per known mapped pair, retaining both directions/report sources without inventing reverse reception. Color by the weakest finite SNR among latest readings per direction/source (green ≥5 dB, amber 0–<5 dB, red <0 dB, neutral unknown); these are display bands, not receiver limits or delivery guarantees. Known hearing times order delayed reports; a newer missing reading never borrows an older SNR. Unknown final-hop identity never becomes an original-source connection.
- Cards show SNR/RSSI including zero/missing readings, separate hearing and report timestamps with ages, path/original source, loaded observation count and recorded/configured/planned endpoint context. Labels support keyboard activation, lines have wider pointer targets, selection replaces existing cards, feed loss retains observations and basemap changes preserve the overlay. Lines depict displayed endpoint locations, not measured RF paths or historical endpoint positions.
- Full frontend tests, TypeScript/default live build and explicit demo build pass; focused grouping and React interaction checks cover missing identities/coordinates, delayed reception, weaker reverse SNR, live updates, line/label selection, empty state, toggle cleanup and mobile/desktop sheet API behavior. Whitespace checks pass. Native browser/WebGL visual review is unavailable (browser inventory empty); existing MapLibre bundle-size warning remains. No service start, deployment, database/firmware change, commit or push requested/performed.

Next useful step: review the overlay visually with the database demo; existing real signal ingestion remains a separate integration task before live observations can populate it.

## 2026-10-16 — Simple local development README

- Add root `README.local.md` with startup, one-time setup, portal/dashboard URLs, public demo credentials, member sign-in, stop behavior, build/check commands and writable/checkpoint database paths. Link it from the main README. Check local documentation links and whitespace; no source or runtime changes, tests rerun, commit or deployment. Preserve existing edits and keep local services stopped as requested.

Next useful step: follow the short README when local development resumes.

## 2026-10-16 — Stop local demo services

- Owner requests stopping local development. Confirm the demo PocketBase on localhost:8092 and its synthetic worker are running; the frontend on 5173 is already stopped. Stop the identified worker first, then its demo server supervisor, and verify neither 5173 nor 8092 accepts connections. Preserve the demo database and all working-tree edits; no production service, commit or deployment changes.

Next useful step: run `python3 backend/launch.py` when local development resumes.

## 2026-10-16 — Local launch and build commands clarified

- Confirm existing `python3 backend/launch.py` supervises the separate demo PocketBase (8092), simulation worker and Vite (5173), preserving the writable demo database and stopping its children on Ctrl+C. It requires initialized demo state/dependencies and refuses occupied ports.
- Confirm repository-root frontend commands: `npm --prefix portal run build` for the default live production build, `VITE_PORTAL_MODE=demo npm --prefix portal run build` for the explicit database-demo build, and `npm --prefix portal run check` for frontend tests plus build. First-time setup remains in the demo guide. No service, source-code, database, deployment or commit changes performed; existing edits preserved.

Next useful step: use the launcher after stopping existing local services, or run the documented build/check command as needed.

## 2026-10-16 — Database-backed demo and neighbor signal table

- Owner keeps the fork proposal parked and requests a neighbor table populated from a separate inspectable PocketBase with its synthetic database tracked in Git. Complete [Serve the demo and neighbor table from a separate PocketBase](../.scratch/pilot/issues/17-database-demo-neighbor-table.md). [Demo guide and public demo-only credentials](../backend/demo/README.md).
- Generate `backend/demo/data.db` solely from fictional fixtures in a fresh disposable PocketBase; retain a checksum manifest and synthetic marker. Initialize an ignored writable copy at `local-data/demo/pb_data/data.db`, rebasing scenario timestamps once in the DB, preserving later edits and refusing overwrite. Seed six trackers, five members, four infrastructure devices and ten directional link observations alongside saved scenario records. Production stays on the VM with operational data/secrets outside Git.
- Replace application memory-only demo data/mutations with separate PocketBase API reads/writes. Keep live/demo request origins and token persistence separate, reject a non-simulation demo response and remove page-level sample fallbacks. Add Infrastructure receiver-filtered Neighbor signals table and a locked additive `link_observations` collection exposed through authenticated state. Preserve signal zeros, unknown values/relay identities, original-source separation and independent report/hearing times. No sample rows enter ordinary migrations; live signal ingestion and fork firmware remain unimplemented.
- All 51 backend checks pass in the existing `.venv` against real disposable databases, including checkpoint/runtime isolation, record edits reaching state, restart persistence and authorization. Frontend tests, typecheck, default live build and explicit demo build pass, including API separation, unavailable/misdirected demo rejection, table filtering and unknown/zero readings. Verify the actual Vite `/demo-api` response matches all ten SQLite signal records and the synthetic worker is online. Existing MapLibre bundle warning remains; no browser surfaces are available for native desktop/mobile visual review.
- Existing frontend occupies 5173, so do not stop it. Start the new demo API on 8092 and its synthetic worker alongside it; portal is `http://127.0.0.1:5173`, dashboard `http://127.0.0.1:8092/_/`. Preserve prior GPS-quality, firmware, cadence-research and other edits. Add only the synthetic checkpoint/manifest/guide to Git tracking; no commit, push, VM deployment or hardware change requested/performed.

Next useful step: owner opens Infrastructure and the demo dashboard to inspect/edit the same rows. Before public release, provision a separate demo API service/proxy and apply the signal migration with its state hook; native visual review and real signal ingestion remain outstanding.

## 2026-10-16 — Fork neighbor reporting improvements explored

- Owner asks whether our fork can improve NeighborInfo for project needs. Extend [node and neighbor telemetry](../docs/research/node-neighbor-telemetry.md#follow-up-tailoring-our-fork) and the existing [research answer](../.scratch/pilot/issues/16-node-neighbor-telemetry.md#fork-customization-follow-up) with passive infrastructure collection of RSSI/SNR, actual hearing age and optional bounded window summaries. Member trackers can keep ordinary GPS broadcasts; only instrumented observers/export paths need the new feature.
- Propose independent gateway MQTT/repeater LoRa schedules, separate expiry and publication, bounded local capacity covering the planned node set and capped/batched radio summaries. Suggested intervals/capacity remain bench hypotheses. Preserve standard NeighborInfo with a versioned private companion payload, GPS priority, airtime gates and gateway silence. Explain duplicate filtering, relay-identity ambiguity and incomplete snapshots; no delivery-rate or complete-topology claim.
- Read-only source/design research and documentation checks only. Local firmware remains at the upstream pin, two commits behind the locally recorded fork branch; reconcile the latest fork before coding. No fetch, firmware change, setting change, build, flash, deployment or commit requested/performed. Existing working-tree changes preserved.

Next useful step: when implementation is requested, define the first report payload and bench acceptance checks, then implement one infrastructure observer/export path before changing the fleet.

## 2026-10-16 — Node and neighbor signal capture reviewed

- Owner asks what else nodes can report and whether neighbor signal strength from repeaters/gateways can be captured in a table. Complete [Check node telemetry and directional neighbor signal reporting](../.scratch/pilot/issues/16-node-neighbor-telemetry.md), with pinned Meshtastic source and official documentation in [node and neighbor telemetry](../docs/research/node-neighbor-telemetry.md).
- Gateway envelopes can include final-hop RSSI/SNR; optional NeighborInfo provides directional neighbor SNR without RSSI or transmitted per-neighbor hearing time. Keep origin/observer/heard-node identities separate, preserve gateway copies and unknown values, and avoid implying reverse connectivity or delivery reliability. Pinned NeighborInfo defaults to six-hour reports, minimum four hours, with ten neighbors; enabling/exporting it requires configuration/build/path verification.
- Record proposed table columns and directional history storage, plus uptime, airtime/channel use, diagnostic counters, transmitted GPS context and fitted sensors as additional candidates. Recommend receive-only gateway metadata extraction first. Exact raw MQTT receipts are already archived privately, but neighbor/signal normalization and portal display are not implemented.
- Documentation only; no live archive inspection, device setting readback/change, firmware change, implementation, deployment, hardware test or commit requested/performed. Check documentation links/whitespace; preserve all pre-existing working-tree edits, including the local GPS-quality feature.

Next useful step: implement gateway receipt signal capture and an Infrastructure table when requested; verify NeighborInfo module/configuration and actual delivery before adding repeater-reported rows.

## 2026-10-16 — Plain-language GPS quality pill

- Owner requests a visual confidence/quality indication without technical abbreviations or invented metre accuracy. Complete [Show plain-language GPS quality in tracker cards](../.scratch/pilot/issues/15-gps-quality-pill.md): green Good / amber Limited / red Poor / neutral Unknown, with bars and text. Tap/click or keyboard-activate for a plain-language explanation about the recorded fix, environmental limitations and separate Last GPS age. Reported satellite count is secondary context; no raw quality score, probability or accuracy radius is displayed.
- Extend MQTT decoding and validated PocketBase ingestion with optional PDOP/satellite values stored on each historical/latest position in existing JSON fields. Absent/zero remains unknown; newer missing quality clears prior quality, and delayed/duplicate/unknown/future packets retain existing ordering and freshness behavior. No migration, archive replay/backfill or firmware/settings change. Demo-only fixtures illustrate the quality categories. Provisional thresholds and primary-source rationale are recorded in the ticket answer and linked contract.
- All 48 backend tests pass against disposable actual PocketBase instances; the initial sandbox run could not open localhost sockets and the permitted rerun passes. Frontend tests/typecheck/default and live builds pass, including wire scaling, metadata validation, duplicate/delayed/restart association, missing-quality replacement, disclosure interaction and Map/Users rendering independently of age. Whitespace checks pass; existing MapLibre bundle warning remains. Browser inventory is empty, so native visual/mobile/keyboard review is unverified.
- No live deployment, hardware/field test or commit requested/performed; preserve unrelated firmware, GPS cadence research and prior session-log edits.

Next useful step: review the pill visually on desktop/mobile, then release worker, backend hook and frontend together when deployment is authorized. Live historical points without quality remain Unknown until a new quality-bearing position arrives.

## 2026-10-16 — GPS quality in location reports checked

- Owner asks whether nodes report GPS accuracy with location. Stock Meshtastic position packets support optional DOP and satellite count ([official configuration](https://meshtastic.org/docs/configuration/radio/position/#position-flags)); pinned `v2.7.26.54e0d8d` PositionModule includes these when enabled, but does not populate `gps_accuracy` in normal node-originated position broadcasts. DOP is a satellite-geometry quality indicator, not a measured error radius in metres.
- Saved private B001/B002 GPS snapshots have position flags 939 (DOP and satellite count enabled, HVDOP disabled). The retained TEST-004 capture contains PDOP 183/282, corresponding to 1.83/2.82, and satellite counts 9/8, with duplicate gateway receipts. These are historical bench observations, not current device readback or field accuracy measurements. Raw locations and identities stay private.
- The current MQTT adapter normalizes coordinates and GPS measurement time but does not expose DOP/satellite count to the portal. No implementation, configuration change, hardware test or commit performed; preserve unrelated edits.
- Follow-up: owner asks whether all position flags are enabled. Decode saved member value 939 against the pinned schema: enabled ALTITUDE, ALTITUDE_MSL, DOP, SATINVIEW, TIMESTAMP, HEADING and SPEED; disabled GEOIDAL_SEPARATION, HVDOP and SEQ_NO. HVDOP selects separate horizontal/vertical DOP instead of PDOP. Saved configuration only; no live readback or setting change.

Next useful step: if GPS quality display is requested, carry received DOP/satellite values through ingestion and label them as quality indicators; a trustworthy metre-radius estimate needs separate receiver/error-model evidence.

### Portal GPS quality integration discussed

- Owner accepts the existing position flags unchanged and asks how to include reported data, especially quality, in the portal. Inspect the adapter, PocketBase ingestion/snapshot and shared tracker detail card. Recommend extending the normalized position with PDOP and satellite count first, retaining these on each historical position and its matching latest-position object. Existing JSON payload/latest-position fields and snapshot forwarding support an additive change without a new collection.
- Proposed presentation: a GPS quality row showing PDOP and a separate satellite count, with a short explanation that lower DOP indicates better satellite geometry, not metre accuracy. Keep quality attached to the same GPS measurement as the coordinates; missing/zero DOP remains unknown and older points without quality stay valid. Preserve position-age/stale behavior separately. Other already-transmitted altitude, speed and course data can follow the same ingestion path, with pinned-source units checked before use.
- This is an integration recommendation, not implemented or deployed behavior or a newly resolved tracker decision. No firmware/settings change, tests or commit performed; unrelated edits preserved.

Next useful step: when implementing, cover wire scaling (183 → 1.83), missing indicators, matching historical/latest measurements and unchanged two-gateway deduplication, then add the quality fields to the shared Map/Users card.

### Accuracy in metres checked

- Owner asks whether metre accuracy is possible. Current stock broadcasts do not provide a per-fix metre-error estimate; PDOP alone cannot supply one without an additional error model. The pinned V4 target assumes L76K, and [Heltec's compatible module](https://heltec.org/project/l76-gnss-module/) lists 2.5 m CEP as a product specification, not each fix's error. Exact installed GPS modules remain unverified in the inventory.
- A possible receiver-native route merits bench verification before any firmware promise: [GPSD's CASIC driver](https://gitlab.com/gpsd/gpsd/-/blob/master/drivers/driver_casic.c) decodes NAV-PV horizontal/vertical error variances into metre estimates. Its header explicitly notes the L76K public protocol document does not document NAV messages; this does not establish support on our units. Some other receivers explicitly expose horizontal accuracy, e.g. [u-blox NAV-PVT](https://content.u-blox.com/sites/default/files/products/documents/u-blox7-V14_ReceiverDescriptionProtocolSpec_%28GPS.G7-SW-12001%29_Public.pdf).
- Recommend first identifying/probing the existing fitted module for a documented per-fix error estimate, then, if supported, implementing firmware reading/transmission and portal storage/display with explicit estimate/confidence semantics. No hardware purchase, firmware/configuration change, actual probe, implementation or commit performed. Do not substitute the advertised specification or an arbitrary PDOP multiplier for observed metre accuracy.

Next useful step: verify the installed module and supported accuracy messages on one owned V4 before deciding whether metre estimates can be added without hardware changes.

## 2026-10-16 — Deploy sign-in refresh fix

- Owner authorizes deployment. Commit and push source `ee5e57e`; build/test it in an isolated LXC release directory with dependencies from the lockfile. The initial shared dependency folder lacked jsdom; isolated installation resolves that without changing the running services. Frontend tests/typecheck/production build pass locally and on the pinned server Node runtime.
- Take and verify a pre-release backup, then publish frontend assets before atomically replacing the index. All seven files match the staged build through Nginx and public HTTPS. Loopback sign-in, saved-token reuse/current account, invalid-token rejection, real-device counts and live MQTT heartbeat pass. All four services remain healthy. No backend code, schema or provisioning changes; old hashed assets and root-private source/static rollback remain available.
- Post-release backup `meshlink-20261016T161434Z.tar.gz`, SHA-256 `888f4a778e53938dbdf4b158aa06026f8149f3201aa2974b7cc64b81d9b6747a`, passes isolated integrity/API/history recovery including MQTT archive preservation. Public TLS, proxy boundaries and per-client sign-in throttling pass. [Full release evidence and pre-release backup](../docs/operations/portal-lxc.md#sign-in-refresh-fix--2026-10-16).
- No connected browser is available for native sign-in/refresh review; actual React DOM regression tests cover refresh, sign-out, rejected tokens, outage/retry, blocked storage and late responses. Preserve unrelated firmware, GPS cadence research and earlier uncommitted session-log entries.

Next useful step: load the updated site and sign in once, then refresh the same tab to confirm the owner's browser retains sign-in. Closing the tab ends this tab-scoped session; demo refresh still returns to sign-in.

## 2026-10-16 — Preserve portal sign-in through refresh

- Owner reports page refresh signs them out. Reproduce with the real live-mode React app in the DOM harness: sign in, remount, assert the authenticated workspace remains. The original app fails because its account/token exist only in React memory; no backend rejection is needed to reproduce it.
- Save only the account bearer token in tab-scoped `sessionStorage`. Reload validates it through the existing protected snapshot endpoint before showing the workspace, using current server account details. Sign-out and rejected authentication remove the saved token. Temporary connection failure offers retry without discarding the sign-in; blocked browser storage retains working memory-only sign-in. Demo entry remains memory-only. Update backend usage/security documentation.
- Frontend test suite, TypeScript check and production build pass. Regression coverage includes authenticated reload, sign-out across reload, 401/403 rejection, temporary outage/retry, a late restore response after sign-out, blocked storage and separate demo access. DOM tests use actual React with a MapLibre adapter; native browser/live-service verification is still outstanding. Existing MapLibre bundle warning remains.
- Owner authorizes deployment on follow-up. Prepare a source commit with only the sign-in fix and its documentation; preserve unrelated firmware, GPS cadence research and pre-existing session-log edits. Origin fetch succeeds and main matches origin/main. Deployment verification will be recorded separately after release.

Next useful step: deploy this reviewed frontend to `meshlink.spp.lol` with a verified backup and retained rollback assets, then check the public build and protected API boundaries. Native browser verification remains outstanding because no connected browser is available.

## 2026-10-15 — Map release and public demo entry

- Owner authorizes deploying the accumulated map/device-card changes and asks for a View demo button on sign-in without an account. Add explicit browser-only demo entry to the live build, a visible Demo label and Exit demo in the shared mobile/desktop header, and return to sign-in on refresh/sign-out. Extract App from the mounting entry point so the actual live-build sign-in/demo/authentication flow can be tested. No anonymous operational API access is added.
- Deploy and push source commit `3964f46` to the existing LXC/public portal. Local frontend tests/typecheck/live production build and all 46 backend integration tests pass; the staged server runtime also passes all 46 backend tests. The additive shortname migration passes first on a private live-database copy, then on the live database with exact checks that existing operational rows and all seven device identities are preserved.
- Public HTML/assets match the verified live build byte-for-byte; authenticated snapshots contain only B001/B002 and five infrastructure devices, with the correct Heltec V4 type metadata. Worker heartbeat, all four services, anonymous profile/state denial, proxy boundaries, sign-in throttling and public TLS checks pass. No demo accounts or synthetic records are added to PocketBase. Preserve earlier hashed assets for open tabs and retain private rollback source/static files at `/opt/meshlink-rollback-3964f46`.
- Pre-release backup: `meshlink-20261015T222413Z.tar.gz`. Post-release backup `meshlink-20261015T222458Z.tar.gz`, SHA-256 `6873c79a5949cef61ace28916c8f60550c298fb8ce16abcca193e0ec295d516d`, passes isolated integrity/API/history recovery, including MQTT archive preservation. [Release operations](../docs/operations/portal-lxc.md#map-and-demo-release--2026-10-15).
- No connected browser is available for visual review; interaction tests use real React/DOM with a MapLibre adapter. Preserve the unrelated firmware checkout and GPS cadence research.

Next useful step: review View demo and the map sheets in a mobile/desktop browser. Friendly-area boundaries, complete long-session aggregation and measured INA219 current remain separate follow-ups.

## 2026-10-15 — Always-active full-battery demo tracker

- Owner requests one full-battery demo whose GPS never exceeds two minutes old. Set Demo Avery/S001 to 100% and derive its standalone simulated position/contact timestamps from the current minute using the existing app clock. This also recovers immediately on the next clock update after an inactive tab; other fixture ages and authenticated backend observations stay unchanged.
- Frontend tests and typecheck/production build pass, covering fresh GPS/Active status at startup, minute boundaries and after long clock jumps without mutating the original fixtures, plus the rendered solid-green 100% battery. No backend change, deployment or commit requested/performed; preserve unrelated edits.

Next useful step: review Avery's solid green battery and Active pill in the demo card.

## 2026-10-15 — Battery size and digit alignment refinement

- Owner requests slightly smaller battery/digits and vertical/horizontal centering. Reduce the icon to 90% of pill height while retaining the 30:14 aspect ratio; reduce digits from 10 to 9 SVG units. Following visual feedback that digits remain too high, move their middle anchor down to x=13.5/y=8 for optical alignment. Preserve existing colors, values and solid 100% appearance.
- Existing rendered component checks and frontend typecheck/production build pass. No connected browser for visual sizing review; no backend change, hosted deployment or commit requested/performed. Preserve other working-tree changes.

Next useful step: review the refined battery in the tracker card at mobile/desktop sizes.


## 2026-10-15 — Stock member GPS timing options reviewed

- Owner asks whether stock firmware can report faster and whether movement-based reporting is better. Check official position/device documentation and pinned stock `2.7.26.54e0d8d` source; capture findings in [member GPS cadence](../docs/research/member-gps-cadence.md). Private-channel configuration permits explicit 60/30-second periodic intervals; GPS acquisition, periodic broadcasts and movement distance/minimum-time settings are separate controls. Default-channel interval enforcement must not be confused with this private profile.
- Recommend comparing a 60-second periodic / 30-second GPS profile with a hybrid: retain 120-second periodic reports, enable smart broadcasting, explicitly set 30-second minimum and 50-metre displacement with 30-second GPS acquisition. These are proposed bench profiles, not approved/applied device settings or measured delivery/runtime claims. Movement requires both displacement and elapsed time; periodic fallback remains useful for stationary/slow searches. Faster reporting increases offered radio traffic; measure freshness, congestion and battery runtime against the existing four-hour minimum/twelve-hour target.
- Source caveat: GPS publication calls `handleNewPosition()` without the smart-enable check, and that handler tests distance/time independently of the toggle. Thus the recorded smart-off setting does not establish strictly fixed-only transmissions. Current documentation also contains inconsistent defaults; use explicit values and reboot/readback. No bug fix or hardware/configuration change performed.
- No ticket decision, deployment or commit requested/performed. Preserve all unrelated working-tree edits.

Next useful step: compare the proposed profiles using actual source measurement/receipt gaps, transmission counts and battery runtime before selecting an operational cadence.

## 2026-10-15 — Session clock clarity, distance and battery sizing

- Owner questions First Seen 99 minutes ago versus Time Active 1h 27m for Demo Morgan. Clarify that the first is age since the first GPS point and the second is the observed first-to-last span (99 minus 12 minutes since the latest point = 87 minutes). Keep Time Active and change First Seen to clock time only, with Unknown retained when unavailable. Last GPS/Last Heard age behavior remains separate.
- Add Distance Travelled beside Time Active in the latest-session summary, displaying miles to one decimal. Sum great-circle segments only between valid, ordered/deduplicated points in that same session; do not bridge >2-hour gaps or include prior sessions. Single point displays 0.0 mi and no timed points Unknown. This is a GPS-sample estimate, not measured route length; missing data/noise and the existing 500-point/12-hour snapshot cap limit completeness.
- Give battery and status pill one shared full CSS height including pill padding; preserve the icon's 30:14 aspect ratio and existing colors/digit/full-charge rules. This supersedes the earlier font-height icon request.
- Frontend tests/typecheck/build pass, including clock-only First Seen, duration semantics, displayed one-decimal distance placement, multi-leg mileage, prior-session exclusion, stationary/single-point/unknown behavior and dateline crossing. Existing MapLibre bundle warning remains; browser visual sizing/native review is unavailable. No backend/API/schema change, hosted deployment, hardware action or commit requested/performed; pre-existing work preserved.

Next useful step: visually review the larger battery and session summary; full session/distance completeness still needs the deferred backend snapshot aggregation work.


## 2026-10-15 — Current member GPS cadence checked

- Owner asks the currently configured location-reporting cadence. Saved/reboot-verified B001/B002 Heltec V4 profiles in TEST-001 use 120-second periodic position broadcasts, 60-second GPS acquisition and smart broadcasting disabled. No later recorded member cadence change found; TEST-004/005 establish automatic GPS reception/ingestion, not a sustained two-minute delivery guarantee.
- Read-only records review; no device readback, radio configuration, hardware test, ticket change or commit performed. Preserve existing working-tree edits.

Next useful step: if actual delivery cadence is needed, measure GPS measurement/receipt gaps from retained observations and compare with the saved profile.

## 2026-10-15 — Compact battery/copy indicators and latest recorded trail

- Owner requests UI-only refinement: compact battery beside status, icon-based coordinate copy, Area/Coordinates on one row, sheets that shrink to content with an approximately 85% viewport limit, “Show Recorded Trail” for the latest continuous session and always-visible session info below GPS/contact times. Read the supplied Lucide icon references and use small inline outline SVGs without another runtime dependency.
- Battery outline/digits match red for 00–19, amber 20–39, green 40–99; 100 is solid green with no visible digits. Unknown/invalid values stay neutral/unknown. Fractional reports are floored; glyph height matches the pill font. Copy works from either text or symbol, shows a brief animated green check and accessible announcement, and handles clipboard failure with a manual-copy message. Mobile sheets have auto height/max 85dvh, bottom safe-area padding and sticky close controls.
- Replace the history range selector, point buttons/details and expanding explanations with one Show Recorded Trail checkbox. Latest loaded GPS session splits only on gaps greater than two hours; exact two-hour gaps stay connected. Sort/deduplicate valid, nonfuture measurement times without mutating inputs, include a known current position, draw only that session and retain dots after card close. Dots are noninteractive and do not block device pins. Shared page state lets a trail chosen on Users appear on Map; login changes clear it.
- Display First Seen from the latest session's earliest available GPS point, separate stored Last Heard and Time Active as the observed first-to-last GPS span, with a fixed loaded-point note. Silence does not grow activity. Session start/duration are unknown without timed points. No backend/API/schema changes: PocketBase currently returns at most 500 GPS points in 12 hours and no session summary. Complete long-session trails/start/activity values need a later backend snapshot aggregation change using retained observations; a new collection is not necessarily needed. Friendly-area mapping remains unconfigured.
- Frontend tests/typecheck/production build pass, including two-hour boundaries, splits, sorting/deduplication, invalid/unknown/future timestamps, current-position inclusion, duration formatting, battery color/digit/full-charge boundaries, copy success/failure/text tapping, map trail features and unchanged card content on checkbox toggles. Existing MapLibre bundle warning remains. No browser surface is connected for actual layout/animation/native clipboard review. Prior backend, firmware, inventory and other work is preserved; no hosted deployment, hardware action, ticket resolution or commit requested/performed.

Next useful step: review the compact sheet in a connected desktop/mobile browser. When backend work is brought forward, provide complete latest-session points and explicit session metadata beyond the current 12-hour/500-point snapshot window.


## 2026-10-15 — Simplified tracker location card and member map shortnames

- Owner requests Location fields (friendly Area, copyable Coordinates to five decimals, Last GPS and Last Heard), a pill beside the name, device-type/radio-name eyebrow and only reported Battery percent. Implement shared card on Map/Users; remove the detailed member battery estimate/voltage/configuration section, while preserving its existing backend storage/API and location history. Clipboard success/failure is announced; coordinates remain manually selectable. Battery is the final field.
- Last GPS uses source measurement time and Last Heard uses receipt-based contact independently; local clocks omit seconds, age uses whole minutes and displays `+2hrs` after two hours. Missing/invalid/future times remain unknown. Provisional pills use Active <2 min, Recent 2–15 min, Stale 15 min–2h and No Location >2h/unknown/no position, pending the owner's optional threshold answer. The existing 15-minute stale summary rule is unchanged. Last known map pins/coordinates remain visible for No Location; no fresh fix is inferred from receipt time.
- Area displays a supplied friendly name or “Unknown area.” Project notes specify owner-defined Google Earth KML/KMZ boundaries, but no dataset/resolver is configured or found. Actual area lookup remains outstanding; no geographic names or boundaries invented. Device type comes from configuration; demo fixtures/confirmed B001/B002 use Heltec V4, other unknown metadata shows Device.
- Add optional five-character member shortnames with additive migration, authenticated own-profile route, owner account-creation prompt and Users form. Validate 1–5 letters/digits/underscores/dashes on server; derive the target member from authentication and reject unrelated fields/worker/anonymous access. Account creation saves a supplied alias transactionally. Assigned map markers use the saved choice; blank/unassigned falls back to the unchanged radio label. Marker width adapts to five characters. Existing records are not assigned invented aliases; fictional demo aliases are explicitly synthetic.
- All 46 backend tests pass in the existing project virtual environment against disposable PocketBase databases, including profile validation, cross-member/role mutation rejection, persistence, account transaction behavior and unchanged tracker/assignment records. System Python initially lacked cryptography; use the existing `.venv` with the required MQTT dependencies. Frontend tests/typecheck/build pass, including exact age/status boundaries, aliases through assignment/release, old-coordinate retention, copy success/failure, card placement/content, shortname form and existing infrastructure/history interactions. Verify the live-cutover metadata addition separately. Existing MapLibre bundle-size warning remains; no connected browser for visual/native clipboard/gesture review.
- Preserve prior firmware, infrastructure, inventory and other frontend work. No live database/schema change, hosted deployment, hardware action, radio naming command, ticket resolution or commit requested/performed.

Next useful step: provide/configure owner area boundaries, confirm the provisional status thresholds, visually review the tracker sheet, and deploy the additive backend/frontend change together when requested.


## 2026-10-15 — Full-screen map and mobile device sheets

- Owner requests map-only viewing with full-width Apple-style mobile detail sheets for infrastructure/member devices, tracking stats on Users, cleaner battery copy and a remembered infrastructure overlay toggle. Map now fills the available viewport beside navigation; basemap/fit/layer controls overlay it and no detail opens until selection. Infrastructure starts on and persists its preference for one year in a SameSite=Lax cookie (Secure on HTTPS).
- Share one native-dialog device sheet: nearly full-height, independently scrollable and animated upward on mobile through 850px; compact nonmodal overlay on desktop. Close control stays visible; Escape, backdrop and a downward handle swipe dismiss. Preserve GPS versus receipt ages, history/point attribution, member battery configuration, infrastructure weather/last heard and offline/stale indications. Move summary counts and searchable tracker list to Users; even devices without positions retain inspection/configuration access there. History remains visible after map-sheet close so points can still be selected.
- Infrastructure estimate labels now say “Estimated battery percentage” without voltage-estimate warnings. Replace visible trend/rate copy with charging/discharging/steady direction and mA availability. No measured current is present in the live contract: display `— mA` rather than relabelling a voltage slope. Optional frontend signed `batteryCurrentMa` supports a supplied current; backend ingestion/sign mapping remains separate. Record owner's planned INA219 use on repeaters/gateways in inventory without claiming installation, measured data or changed quantities.
- Frontend tests/typecheck/production build pass, including actual React/DOM interactions for exclusive device selection, mobile modal versus desktop panel APIs, close/cancel/Escape, focus restoration, history, cookie remounts, offline status, infrastructure-only maps and never-seen device inspection. Current checks distinguish signed mA readings from missing/invalid current and voltage-only history. Existing MapLibre bundle-size warning remains. Computer-use inventory exposes no apps or browsers, so native modal/gesture behavior, animation, WebGL/tiles and visual layout remain unverified.
- Existing firmware, infrastructure battery/history UI, package/inventory/session and research work preserved. No firmware/backend change, hardware test, hosted deployment, ticket resolution or commit requested/performed.

Logo/layout follow-up: owner supplies the [SNORR logo](https://snorr.vegas/wp-content/uploads/2021/12/cropped-SNORR-Final-Logo.png), requests the same mobile header as the other pages and reduces sheets to about 80% of the screen. Bundle the unchanged PNG locally in shared branding, restore the mobile map logo/navigation plus common topbar/status header, and size all mobile device sheets to `80dvh` with independent scrolling/sticky close controls. Desktop keeps the compact overlay. Frontend checks/typecheck/build pass; no connected browser for visual review and no hosted deployment/commit requested.

Banner cleanup follow-up: owner removes both environment/feed banners from Map on every screen size and the breadcrumb/clock bar from every page. Do not render the two banners on Map; retain their account/demo/feed controls on other pages and keep shared logo/navigation visible. Remove unused breadcrumb/clock styling and the mobile banner override. Map outage notices and 80%-height device sheets remain available. Frontend checks/typecheck/build pass; browser visual review and hosted deployment remain outstanding. No commit requested/performed.

Infrastructure visibility follow-up: owner removes the infrastructure toggle and requires infrastructure always on. Remove visibility state, cookie reads/writes, toggle props/control and unused styling; render infrastructure markers unconditionally and ignore previous off cookies. Update existing DOM coverage to retain infrastructure after page remount with an old off cookie and with zero member trackers. Frontend checks/typecheck/build pass; no hosted deployment or commit requested/performed.

Next useful step: review the map and sheets in a connected browser at desktop/mobile widths, then deploy when requested. INA219 installation and live current telemetry remain unverified.


## 2026-10-15 — Member battery voltage and configurable LiPo estimate

- Owner requests backend/frontend support for end-user voltage broadcasts, battery type/size configuration and similar state-of-charge estimates for the purchase-list 1000/3000 mAh LiPo packs. Preserve the earlier 1100 mAh inventory label for the smaller packs and unchanged stock counts; suggestions include 1000/1100/3000 with other positive whole capacities or unknown accepted. No installed device/pack mapping inferred.
- Normalize member battery telemetry into existing PocketBase observations/receipts with source validation and two-gateway deduplication. Expose separate voltage, measurement/receipt timestamps, timestamp quality and configuration in tracker snapshots. Battery packets preserve GPS measurements/history; old/future/unknown clocks cannot overwrite newer known battery measurements. Member nonbattery telemetry remains outside operational normalization; raw archive remains complete for received traffic.
- Add admin-only battery type/capacity configuration using the existing route and selected-tracker Battery UI. Generic 1S 3.7/4.2 V LiPo lookup uses the pinned Meshtastic nonlinear reference, rounded to 5%, with raw volts and offline/unknown-time/15-minute stale indication. Capacity is metadata, not a runtime estimate or percentage multiplier. [Source/profile details](../docs/research/member-battery-charge.md).
- All 44 backend checks pass locally and on the LXC runtime in disposable databases; full working-tree frontend and isolated staged frontend checks/typecheck/live build pass, including rendered battery state/admin-controls tests. Deploy only the member change after verified backup `meshlink-20261015T203559Z.tar.gz`; no schema migration or radio/telemetry-setting change needed. Post-deployment backup `meshlink-20261015T203735Z.tar.gz` restores in isolation and proxy/auth boundaries pass.
- Check ten actual archived messages through the new decoder: no member battery-voltage packets available, so no backfill performed. B001/B002 keep unknown profile/capacity and voltage absent; do not invent readings or silently assign packs. Real member voltage reception/calibration, installed-pack selection and full browser visual review remain unverified. Preserve unrelated local firmware/infrastructure UI/inventory/session work outside this release; local battery helper now re-exports the shared estimator without changing EVE results.

Next useful step: admin selects the installed LiPo type/capacity for each tracker, then verify the first actual member voltage packet and compare to a multimeter. No firmware/cadence change made.

## 2026-10-15 — Archive all received MQTT traffic in PocketBase

- Owner directs saving all MQTT data now and deciding how to use it later. Add private `mqtt_archive` collection and worker-only archive route: exact payload bytes as base64, topic, arrival time, QoS/retain/duplicate flags, stable receipt UUID and bounded normalization outcome/reason. Unsupported, unknown-source, retained, malformed and duplicate deliveries are preserved; existing operational normalization/contact/freshness rules stay intact.
- Subscribe to the configured project root (`snorr/pilot/#`), archive before normalized ingestion and acknowledge QoS 1 after private SQLite persistence. API retries reuse archive IDs; old normalized queue entries still drain, and backend validation rejection receipts no longer block the queue. No raw data/keys enter Git, no automatic expiry is introduced, and archive access stays behind trusted PocketBase administration.
- Deploy additive migration and worker/hooks to the authorized LXC after verified backup `meshlink-20261015T202515Z.tar.gz`. Verify an actual new live receipt, byte-length preservation, zero pending queue and active services. All 42 backend tests pass locally and on the production runtime against disposable databases. Post-update backup `meshlink-20261015T202742Z.tar.gz` and isolated recovery include the archive; protected proxy and login checks pass.
- Worker requests all root topics, but broker delivery remains ACL-limited: documented read permission is `snorr/pilot/2/e/#`. Broker SSH works as the owner, but ACL inspection/change requires unavailable sudo authentication; root SSH is denied. No broker permissions were changed. Raw ciphertext retains later decoding options with the matching private key; past discarded data and offline/QoS-0 losses are not recovered. [Operations and limits](../docs/operations/live-mqtt.md#raw-mqtt-archive--2026-10-15).
- Preserve the pre-existing firmware, frontend, inventory and session edits outside this change.

Next useful step: let the archive collect real traffic; broker admin can expand the worker read ACL to `snorr/pilot/#` if topics outside the existing encrypted subtree are needed. Review stored packet types when the owner brings interpretation forward.

## 2026-10-15 — Last-heard ingestion semantics reviewed

- Owner asks whether last heard can use the latest MQTT packet from a node. Inspect adapter, worker and ingestion: live worker subscribes to the configured encrypted channel, filters registered sources/gateways, and currently normalizes member positions plus infrastructure voltage/environment telemetry. Other application packets are counted as ignored, not archived. Rejected adapter packets are counted, while backend validation failures retain bounded receipts.
- Accepted/duplicate normalized receipts update the originating device's lastContactAt using original worker receipt time, independently of sensor/GPS measurement clocks. Snapshot and map stats already expose that field; demo infrastructure fixtures currently omit receipt timestamps. Queued API ingestion preserves original arrival time.
- Recommend extending last heard to validated packets originating from a registered node regardless of application kind, retaining only needed contact metadata. Keep gateway latest MQTT uplink activity separate: forwarding another node's packet proves gateway activity, not a fresh packet originating from the gateway or each relay. Keep sensor/GPS measurement ages independent. No catch-all ingestion, raw-payload archive or last-heard behavior change implemented in this review.

Next useful step: choose all-valid-origin-packet contact tracking plus separate gateway uplink age, then implement/test the adapter/receipt contract without refreshing telemetry/GPS timestamps.

## 2026-10-15 — RAK charging and solar specifications checked

- Owner asks about published RAK4631 charge/discharge/cutoff/solar behavior. Inventory identifies RAK19007 base boards; per-unit revision remains unverified. Read the official RAK19007 datasheet and RAK support explanations, and inspect the pinned Meshtastic source without modifying firmware.
- Record charging target 4.2 V, documented 350 mA charge current, nominal 5 V solar input / 5.5 V maximum and 3.3–4.3 V documented battery operating range. Distinguish 2.9 V charger precharge and recharge hysteresis from low-voltage discharge protection. Source has software low-battery sleep near 3.1 V; physical protection and real sleep/restart thresholds remain untested. [Sources and distinctions](../docs/research/battery-charge-estimate.md#rak19007-charging-and-low-voltage-behavior).
- No hardware/protection installation claim, field measurement, threshold/code change, ticket resolution or deployment.

Next useful step: confirm actual base-board revision, battery protection and panel voltage, then bench-test normal low-battery sleep and solar recovery when hardware is available.

## 2026-10-15 — EVE battery profile and approximate charge display

- Owner identifies EVE 26V 18650 2550 mAh / 7.5 A cells, confirms direct battery voltage and supplies 3.6/4.2/2.5 V nominal/full/cutoff. Update inventory without changing counts or claiming assembly/calibration.
- Verify EVE specifications and visually inspect the manufacturer's reference discharge chart using PDF rendering. Document approximate nonlinear lookup from the 0.2C/77°F curve, interpolation, 5% display rounding and limits in [battery charge estimate](../docs/research/battery-charge-estimate.md). This is a loaded reference curve, not measured pack calibration or open-circuit data.
- Add shared estimated charge display to Infrastructure battery detail and map quick stats for R001/R002/R003 and explicitly configured EVE 1S profiles. Other/unknown profiles stay unknown; member percentages and raw backend telemetry remain unchanged. Preserve voltage, unknown/stale/offline indications and charging-bias context. Cell cutoff is separate from unverified node cutoff and runtime; no warning rule changes or hosted deployment.
- Verify nonlinear interpolation, bounds/invalid inputs, profile isolation, monotonicity, 5% rounding and rendered UI through frontend checks. Hardware calibration, actual charge-state verification and browser visual review remain outstanding. Existing unrelated firmware change preserved; no commit requested.

Next useful step: review the approximate percentages locally, then compare telemetry to a multimeter and record a normal-load battery discharge when nodes are available.

## 2026-10-15 — Voltage-derived charge estimate discussion

- Owner asks whether battery chemistry/voltage can provide estimated state of charge and clarifies 2550 mAh 18650 cells in two- or four-cell parallel packs. Record owner-reported wiring and rated arithmetic in inventory without assigning unconfirmed per-device configurations or measured capacities.
- A coarse chemistry-specific voltage lookup is feasible after confirming the cell model/charge profile and that telemetry measures battery terminals. Discuss calibration, charger/load influence, temperature and usable cutoff; capacity/parallel count alone does not define the voltage curve or remaining runtime. TI primary-source reference: https://www.ti.com/document-viewer/lit/html/SSZT786/GUID-5DD8C3D9-BCBE-467B-90E5-FAA672AAC15D .
- No estimate curve, new hardware, backend/frontend implementation, field measurement or ticket resolution in this discussion.

Next useful step: identify cell make/model or nominal/full-charge voltage and confirm per-device parallel packs/measurement path, then choose an explicitly approximate UI profile.

## 2026-10-15 — RAK4631 small dummy-load guidance

- Owner asks about a conservative resistor load and chip GPIO limits. Reviewed [Nordic GPIO specifications](https://docs.nordicsemi.com/r/bundle/ps_nrf52840/page/gpio.html), [Nordic support's package-current guidance](https://devzone.nordicsemi.com/f/nordic-q-a/82106/nrf52840-gpio-drive-capability), and [RAK4631 electrical documentation](https://docs.rakwireless.com/product-categories/wisblock/rak4631/datasheet/).
- Standard-drive logic levels are specified at 0.5 mA; high drive at 5 mA with VDD >= 2.7 V (3 mA at lower supply). Nordic support gives 15 mA total GPIO sink/source ceiling for the package; table values of 14/15 mA are not conservative per-pin design targets. Suggested starting at 10 kOhm GPIO-to-ground (~0.33 mA at 3.3 V), with an unused output verified first. A 2.2 kOhm load (~1.5 mA) requires explicit high-drive configuration for this guidance.
- A power-rail resistor, optionally switched by a MOSFET, better suits a larger battery dummy load; exact rail, baseboard wiring/regulator budget and firmware pin use must be checked before wiring. No hardware connected, firmware changed, load/current measured, ticket resolved or commit requested. Existing working-tree edits preserved.

Next useful step: identify the exact baseboard and whether the intended test is battery drain or processor work, then select the load and connection accordingly.

## 2026-10-15 — Linux infrastructure battery UI

- Owner resumes frontend development without nodes and requests better repeater battery direction/rate/history. Synced main (already current); preserved the pre-existing firmware submodule change.
- Added voltage-derived charging/discharging/steady estimates and mV/hour slope from actual elapsed times over the latest continuous hour. Require three reports over ten minutes, break on configured battery timeout, and label stale/unknown-time/offline estimates as historical. Charger state/current remain unmeasured; no battery capacity/runtime claims.
- Replaced the fixed-axis dots with a full-width time chart, adaptive voltage scale, 1h/6h/24h/all-loaded ranges, keyboard/selectable exact readings, range/change summary and reading table. Expose existing 40-observation snapshot limit; retain unknown-clock handling. Added richer fictional demo histories only; backend, hardware, hosted services and private data unchanged.
- Frontend tests/typecheck/production build pass, including direction, irregular sampling, sparse data, outages and invalid timestamps. Existing MapLibre bundle-size warning remains. Visual browser review could not run: computer-use inventory has no browsers/apps. No hardware or live telemetry validation, hosted deployment, ticket resolution or commit requested/performed.

Follow-up: owner reports repeated backhaul details after switching devices. Reproduced using actual React components in a temporary jsdom harness: switching to the backhaul leaves two battery sections and emits duplicate-key warnings. BatteryHistory and RuleForm shared the selected device ID as sibling keys. Give each component a distinct prefixed key; repeated repeater/backhaul switches now retain exactly one battery section and one rule form. Add a persistent DOM regression test and pinned development-only jsdom dependency to the existing Node test command. Browser visual review remains unavailable; this verifies actual React reconciliation and rendered DOM rather than appearance.

Map follow-up: owner requests named/selectable infrastructure markers with quick power/weather/last-heard stats. Replace generic R/B/site-count pins with individual R001/G001-style labels, preserving separate selection at colocated coordinates using screen offsets. Member pins now show full short names such as S001. Add an on-map quick-stats panel for voltage, inferred direction/rate, available temperature/RH, receipt-based last heard and planned-site/offline/stale/unknown-time indicators. State of charge is explicitly unknown because the current infrastructure contract does not provide a percentage; do not derive one from voltage. Layer-off and close controls clear the panel; no new telemetry or deployment.

DOM interaction tests exercise actual map React components with a minimal MapLibre marker adapter (no WebGL/tiles), covering colocated labels, device switching, sensor availability, offline status, close and layer toggling. Frontend tests/typecheck/build pass; browser visual/hardware checks remain outstanding.

Temperature follow-up: owner requests Fahrenheit throughout the site while preserving Celsius in the backend. Centralize presentation conversion and apply it to both infrastructure details and map quick stats. Update rendered-DOM assertions for both surfaces (8.4°C displays as 47.1°F); preserve unavailable-reading behavior and raw telemetry.

Next useful step: review local Infrastructure detail and infrastructure map quick stats on desktop/mobile, then decide whether to expand backend battery history/state-of-charge telemetry and deploy the reviewed frontend.

## 2026-10-15 — Restore connected gateway Wi-Fi

- Owner requests restoring supplied Wi-Fi credentials on the connected gateway. After USB reconnection, COM6 identifies as G002 (`!849ad7a0`). G001 is unchanged.
- Privately back up settings, apply supplied credentials with Wi-Fi enabled, and reconnect to verify exact saved values. Serialized MQTT and LoRa settings remain unchanged. Credentials and snapshots stay in ignored `private/bench/2026-10-15-gateway-wifi/`.
- Saved configuration passes; hotspot association and subsequent MQTT delivery remain unverified. No firmware, hardware allocation, portal or radio-profile changes.

Next useful step: keep the hotspot available and verify fresh G002 receipts in the live portal.

## 2026-10-14 — Correct standalone-demo frontend on live portal

- Owner reports demo data after repeater deployment. Fresh public browser reproduces six fictional trackers; authenticated loopback confirms live backend/configurations retained. Served bundle matches staged artifact. Cause: build omitted `VITE_PORTAL_MODE=live`, selecting old demo default. Earlier API/restore checks missed browser entry behavior.
- Production now defaults live while retaining local development/explicit standalone demo. Vite validates/records mode in HTML; deployment refuses non-live artifacts and live verifier checks served mode. Two regression tests added; all 10 frontend tests/typecheck/build pass. Deploy hashed assets before atomic HTML replacement after private backup; no database/radio/credential changes.
- Hosted mode assertion changes from failure to pass; fresh public browser shows sign-in. Configuration preservation, public HTTPS/auth boundaries and isolated corrected-build restore pass. Backup/checksum in [operations](../docs/operations/repeater-telemetry.md#frontend-mode-correction). Authenticated browser rendering still needs account-holder review.

Next useful step: owner refreshes/signs in to review live Infrastructure cards; continue sustained telemetry/coverage/power measurements. Publish correction to origin/main, preserving unrelated 3MF.

## 2026-10-14 — Three repeaters provisioned with live telemetry

- Owner authorizes adding R001/R002/R003 at two supplied planned sites with antenna, four 2550 mAh 18650 cells each and 160 mA solar-cell records; explicitly includes live infrastructure telemetry. Exact coordinates remain private. Record planned assemblies without inferring chemistry, wiring, aggregate capacity or panel wattage. Warn monitoring remains disabled pending deployment activation; live readings are enabled.
- Extend encrypted MQTT decoding, PocketBase observations/health and portal humidity/unknown-clock display; group colocated map markers. Add guarded transactional provisioning, isolated rollback/preservation checks and dynamic restore expectations. Fix existing generated-password CLI parsing using `--`. Existing trackers/accounts/history and credentials are preserved.
- Staged 39 backend tests and 8 frontend tests/TypeScript/build pass. First deployment attempt safely stops before provisioning because the old restore verifier assumes four accounts; actual deployment has five. Correct verifier and rerun backup/restore before successful migration. No reset or synthetic live records.
- Live authenticated configuration matches all three exact private plans. R001 4.115 V, R002 4.159 V, R003 3.634 V; R003 19.8942°C/36.7484% RH. Each of four genuine radio reports arrives through both gateways: eight receipts, four observations, accepted/duplicate pairs. Valid wall-clock measurements are preserved; unknown uptime clocks are separately tested.
- Public HTTPS/authentication boundaries, proxy throttling and isolated seven-device restore pass. Matching final private backup/checksum and details: [operations](../docs/operations/repeater-telemetry.md), [TEST-009](field-results.md#test-009--live-repeater-provisioning-and-telemetry). No new hardware purchases, field installation or deferred survey work.

Next useful step: review authenticated rendering on the owner's devices, confirm installed-site status and monitoring thresholds, then measure sustained telemetry/GPS freshness, power endurance and actual relay coverage. Solar-input measurement, sensor calibration and off-host backup remain unverified. Publish this completed source/record checkpoint to origin/main; preserve unrelated 3MF.

## 2026-10-14 — R003 AHT fix ported, built and flashed

- Owner explicitly authorizes bringing the identified changes forward, building and flashing R003. Sync main (already current), initialize pinned firmware/nested submodules and read firmware agent/build instructions. Switch clean firmware to the existing `snorr/rak-survey` project branch and port only the RAK sensor-detection fix; no forced reporting intervals, old defaults or survey implementation. Publish functional commit `b0aa05b41` and concise-comment follow-up `cc5907b1fc7b4c200e23f43e10baa54c39aeaf25`; no history rewritten.
- Native Windows PlatformIO build succeeds as `2.7.26.cc5907b`. Recover a stalled compiler download using the exact registry-checksummed archive; remaining dependencies install normally. Build uses pinned GCC 9.3.1, nordicnrf52 10.11.0 and Arduino framework source `9ddcbc9568b12f102f9e88bd4d1b88ea789213a4`. Trunk is unavailable; changed line passes scoped clang-format 16.0.3 and whitespace checks. Vendor-library warnings remain; no full native/MCP suite claim.
- Snapshot R003's complete private profile/keys. Identity-check it, enter its UF2 bootloader and flash the checksum-verified custom image without reset/bootloader change. Reconnect on COM14; custom version and complete pilot-profile checks pass. Entire local/module/channel configurations equal the pre-flash snapshot, including channel/device keys, role/radio settings, debug off and enabled device/environment reports at 900 seconds.
- AHT-family readings now work: local sample 22.90535°C/35.01892% RH; automatic environmental packet at 22.97821°C/34.962845% RH reaches both V3s. New battery packet (4.267 V, charging/no-battery level 101) also reaches both: 4/4 new receipts pass. Exclude older packets drained from gateway queues. Post-flash telemetry clocks initially report uptime-like 66/91 values; do not treat them as Unix measurement times. No gateway, R001/R002, portal or other hardware changes.
- Keep artifacts, checksums, build logs, configuration/key snapshots and raw receipts ignored/private. Update submodule pointer, inventory, project/map and handoff; [exact source/build/flash evidence](../docs/operations/r003-aht-build.md), [TEST-008](field-results.md#test-008--r003-custom-aht-build-and-radio-telemetry). The stock-only R003 limitation is resolved by this authorized custom image; original two-repeater field allocation and deferred survey scope remain unchanged.

Next useful step: measure sustained 15-minute device/environment delivery and battery/solar runtime, compare sensor/voltage to references, and verify required V4-to-RAK GPS relaying. Portal infrastructure ingestion/display and clock-validity handling are separate work. Publish the parent source pointer and these records after the already-pushed firmware commits.

## 2026-10-14 — Existing fork AHT fix confirmed

- Owner recalls fixing the RAK temperature-sensor issue in the older firmware fork and requests verification. Read the existing fork audit, then independently inspect GitHub's exact commit diff and current develop source. Confirm `e617a4dcfd95500c73f570c583f3ea6d02aa4881` (2025-12-31, “fix AHT10 for RAK4631”) comments out HAS_NCP5623. This survives at current develop `76d5156e72d9d9aaa9722b7bbc1336335b685984` and R003's former reported source revision `36133d29d`.
- The same commit forced environmental enable/15-second reports; later commits revert the forced behavior while retaining the variant fix. Link this existing finding into the R003 setup record. The source change matches the stock scanner exclusion; it does not prove the tentatively identified AHT21's wiring or operation. No firmware/configuration/hardware change, build, flash, ticket resolution or broader fork transplant.

Next useful step, if owner brings custom firmware forward: port only the RAK sensor-detection compatibility change onto the pinned current release, retain configured 900-second device/environment reports, build a traceable image and verify actual temperature/humidity on R003. Stock firmware remains installed pending that scope change.

## 2026-10-14 — R003 prepared; stock AHT sensor limitation identified

- Owner replaces the connected RAKs with another unit, requests R003 with matching stock pilot configuration and temperature/humidity if available, confirms antenna, and tentatively identifies AHT21 at 0x38. Sync main (already current), preserve unrelated untracked 3MF, identify COM14 RAK4631 `!05237743` and privately back up its older profile.
- Full reset, 1200-baud Nordic entry on COM15 and official matching stock package install succeed. Apply shared private profile with device/environment telemetry explicitly enabled at 900 seconds each; reapply after role defaults, clear unrelated telemetry options and verify the complete profile after configuration reboot. Private provisioning/verifier updated; no changes to disconnected R001/R002 or the gateways/portal.
- Both V3s receive two automatic device-metric packets (4/4 receipts) with firmware-reported 4.259/4.278 V and level 101. No temperature/humidity arrives in gateway observation or short local request. Brief private debug logging restored off. Pinned standard RAK variant defines HAS_NCP5623, which compiles out the scanner's AHT detection case; environmental enable alone cannot overcome that stock-target exclusion. Sensor model/wiring and actual voltage calibration remain unverified.
- Record third existing-stock allocation, verification and source explanation in [setup](../docs/operations/rak-pilot-setup.md#r003-environmental-sensor-follow-up--2026-10-14), inventory and [TEST-007](field-results.md#test-007--r003-stock-setup-and-environmental-sensor-limit). Keep the original two-repeater field plan, stock firmware constraint and deferred custom survey scope; no new purchase, site work, custom firmware or tracker status change.
- Final explicit reboot/reconnection passes the complete profile, including debug off and unrelated sensor modules disabled. Local Python close/disconnect race recurs after reboot, with successful subsequent device readback.

Next useful step: owner chooses whether to retain stock with this sensor unavailable or bring forward a targeted firmware/sensor compatibility change. Forced GPS relaying, actual sensor wiring/model verification, calibrated battery voltage and sustained cadence/runtime tests remain outstanding; portal telemetry is separate.

## 2026-10-14 — Enable RAK battery-voltage telemetry

- Owner asks whether R001/R002 track/report battery voltage. Check saved profiles and pinned stock `DeviceTelemetry.cpp`: a 900-second interval alone does not enable broadcasts. Initial setup missed `device_telemetry_enabled`, which remained false. Correct it to true on both identified RAKs and retain the interval.
- Independent complete profile checks pass after configuration reboot on both devices, including the added enable-flag assertion. Private setup/verification helpers are corrected; keys/configuration stay outside Git. Stock device metrics include voltage and battery level, with level 101 for charging/no battery. Actual voltage calibration and timed periodic RF delivery remain unmeasured; the portal's existing GPS worker does not ingest battery telemetry.

Next useful step: connect the verified battery assembly, compare reported voltage to a meter, observe automatic telemetry reception at the V3s, then implement portal infrastructure telemetry separately when brought forward. No radio/channel, inventory quantity, site, battery specification or ticket status change.

## 2026-10-14 — Two stock RAK pilot repeaters prepared

- Owner brings forward setup of two plugged-in RAK repeaters with stock firmware and permits flash/reset; confirms suitable 915 MHz antennas on both. Sync main from origin (already current), preserve the unrelated untracked 3MF, read the pilot/inventory/handoff and identify COM8/COM9 as RAK4631 R001/R002. No purchase, stock-count change, site installation or custom survey work.
- Privately back up previous configurations; verify the official nRF52840 release archive digest and matching RAK4631 UF2. Install stock `2.7.26.54e0d8d`. Both APIs time out after full reset; 1200-baud entry and official matching Nordic serial firmware reinstall restore access without a bootloader update. Cause remains unresolved. Full reset replaces legacy keys, admin configuration and old fixed locations.
- Configure the shared private pilot channel/radio profile, visible ROUTER roles, local-only rebroadcast, US/LONG_FAST slot 35, hop limit 3 and 10 dBm. GPS/fixed location, MQTT/Wi-Fi and channel gateway functions off; device telemetry 900 seconds. Stock role-change defaults override initial values; reapply the explicit profile after role change and verify independently. Complete exports/keys stay private.
- Six of six direct encrypted zero-hop fixture receipts pass: each RAK reaches the other and both independently identified receive-only V3s. Existing gateway/portal configurations unchanged. [Setup and recovery record](../docs/operations/rak-pilot-setup.md), [TEST-006](field-results.md#test-006--stock-rak-pilot-repeater-preparation).
- Final explicit reboot/reconnection checks pass both complete profiles. Local Python cleanup reports an already-disconnected stream after reboot requests; successful subsequent readbacks verify the devices. No battery power cycle performed.
- Owner later completes the earlier requested double-reset gesture, exposing both RAK4631 recovery drives. Recopy the same checksum-verified stock UF2 without erasing configuration; both return to COM8/COM9 and pass the complete independent pilot-profile checks again. No further button action needed.

Next useful step: physically label R001/R002, reconnect a GPS V4, then prove each repeater is required in an isolated V4-to-RAK-to-V3 path with original GPS measurement times retained at dispatch. Sustained freshness, local operation during internet loss, actual battery/solar assembly and runtime remain untested. No decision ticket status changed; custom survey work stays deferred.

## 2026-10-14 — Real MQTT GPS portal deployed; secrets stored in 1Password

- Owner authorizes the recommended receive-only GPS integration, replacement of fake data and project-secret storage in 1Password. Create SNORR MeshLink — Pilot and store the existing channel/broker/gateway/portal provisioning secrets and replacement Wi-Fi without password rotation or values in Git/logs. Windows MCP environment mounts are unavailable; root-owned group-readable LXC JSON config is provisioned separately and does not automatically sync vault edits. Owner corrects broker SSH to `mqtt.snorr.org:64582`; export only the read-only worker credential.
- Apply/read back replacement Wi-Fi on both V3s, preserving MQTT and transmit-disabled LoRa configurations. Independently identify COM4 B002, COM5 B001, COM6 G001, COM7 G002 and confirm four distinct stable hardware identities. No quantities, firmware or RAK changes. Owner restores B001 reporting during live validation.
- Implement encrypted Meshtastic position decoding, verified node/gateway mapping, true GPS-solution timestamps, gateway-independent packet identity, private durable API retry queue, broker-aware heartbeat/reconnect and service supervision. Correct an early `Position.time` clock mistake to `Position.timestamp`; regression coverage prevents receipt/transmit clocks refreshing old fixes. Native simulation remains a development tool; the guarded installer cannot overwrite live provisioning.
- Automatic review rejects broad broker-export disclosure; a scoped worker-only export succeeds. It also rejects a proposed partial-tracker cutover; no partial cutover occurs. After owner reports B001 fixed, the strict five-minute preflight passes all four paths with actual GPS ages about 6–75 seconds. A backup/verified isolated recovery precedes the transactional real-device cutover. The backup verifier now waits for API HTTP readiness after service restart, fixing an observed startup race.
- Hosted API has simulation disabled and four real bench devices, with demo members/accounts retired/disabled and admin access preserved. Publish the sign-in-first live frontend. The live worker saves two observations/four receipts initially; after a verified worker restart, three observations/six receipts are retained, with both trackers deduplicated across both gateways. Latest checked ages after restart are about 143–145 seconds. Inbound/outbound text, name updates and telemetry remain separate/unimplemented. [TEST-005](field-results.md#test-005--live-portal-gps-ingestion).
- Verify the new live backup, isolated restore, proxy authorization/throttling and credential-free public HTTPS boundaries. Public browser sign-in entry renders; authenticated live map/history browser QA remains outstanding. All 36 backend tests and eight frontend tests pass; pinned Node build/TypeScript, Python/shell/service syntax and whitespace checks pass. Existing MapLibre size warning remains. Private raw tracks, credentials, DB/queue and unrelated untracked 3MF stay outside Git.

Next useful step: owner reviews the authenticated live map/history using the unchanged admin login now stored in 1Password, then measure sustained freshness, phone-free startup, Wi-Fi/broker outages and battery runtime. Real member provisioning and off-host backups remain outstanding. Commit/push this coherent integration checkpoint; no ticket status/decision changed, no survey/wishlist expansion or outbound radio feature activated.

## 2026-10-14 — Live portal development prerequisites reviewed

- Owner resumes development and asks what is needed to connect MQTT and replace fictional portal data. Reviewed the handoff, current worker, ingestion validation, physical bench identities and LXC deployment records. Real radio-to-MQTT GPS delivery is already recorded; the missing implementation is the persistent encrypted-protobuf adapter feeding the authenticated normalized ingestion endpoint.
- Interpret the requested replacement as a real-device-only cutover. Plan a verified hosted backup before retiring fictional operational records, preserve portal access, provision the two V4 trackers/two V3 gateways with verified physical mappings, and disable simulation updates and simulated send/name outcomes. No hosted records or services changed.
- Prerequisites: privately provision the existing read-only MQTT account and channel key to the worker host; build/test decoding, timestamp preservation, duplicate receipts and reconnect/outage behavior; keep both V4s powered with sky view and both V3s on working Wi-Fi for end-to-end verification. Desktop serial ports are accessible, but local bench dependencies and per-V3 port mapping still need setup if serial inspection is used.

Next useful step: implement the receive-only GPS adapter and safe real-device provisioning/cutover procedure, then deploy after backup and verify live GPS in the portal. No implementation, new hardware test, ticket resolution, commit or push in this prerequisite review.

## 2026-10-14 — All four Windows serial ports accessible

- After owner reconnects the V3s, both CP2102 bridges report healthy drivers (error code 0), assigned COM6 and COM7. Both V4 ports COM4/COM5 and both V3 ports COM6/COM7 pass brief native open/close with DTR/RTS disabled. No additional Windows driver permissions needed for serial access.
- No firmware/configuration changes, GPS/MQTT delivery test or hosted deployment. V3 label-to-port mapping remains to read through the device protocol.

Next useful step: install local bench dependencies and read device identities, then resume the MQTT ingestion adapter using the accessible LXC. Hosted simulation-data handling remains to settle before changing its database.

## 2026-10-14 — Windows driver installation recheck

- Owner reports driver installed. One CP2102 bridge now has a healthy driver and COM6; native open/close passes on COM4, COM5 and COM6. The second CP2102 bridge still reports missing-driver error 28 and has no COM port. Per-V3 identity remains unverified. No hardware quantity changes.
- Windows hardware rescan via `pnputil /scan-devices` is denied by the current Windows token even outside the sandbox. No radio/configuration changes or application-level packet tests.

Next useful step: unplug/replug both V3s to trigger driver detection; if the second bridge remains unconfigured, use administrator Device Manager to apply the installed CP210x driver to that device.

## 2026-10-14 — Windows desktop access smoke check

- Synced main from origin (already current), preserving the unrelated untracked 3MF file. Firmware submodule is pinned but not initialized in this checkout.
- All four boards enumerate on Windows USB. V4 descriptor identities match B001 on COM4 and B002 on COM5; both ports pass a brief native open/close with DTR/RTS disabled. Both CP2102 bridges have Windows device error 28 (missing drivers), so neither V3 has a COM port. No firmware/configuration write or application-level GPS/radio test performed.
- Initial sandbox CIM/WSL access denials clear with approved outside-sandbox read-only checks. Ubuntu-24.04 WSL starts as the owner, with Python available but no attached USB serial devices. Native Python lacks serial/Meshtastic/MQTT packages. Existing SSH access to root@meshlink.int.spp.lol succeeds; API and simulation worker services are active. No hosted data/service changes.

Next useful step: install the signed [Silicon Labs CP210x Windows VCP driver](https://www.silabs.com/software-and-tools/usb-to-uart-bridge-vcp-drivers) with Windows administrator access, then verify both V3 serial ports and set up local bench dependencies. Native Windows serial plus LXC deployment is available; WSL USB passthrough is unnecessary for that path. Live MQTT adapter and hosted demo-data choice remain pending.

## 2026-10-14 — Dell Linux to Windows/WSL development handoff

- Owner requests committing/pushing all pending publishable work for desktop continuation and confirms regular switching between the Dell Linux laptop and Windows desktop running WSL. Record the ongoing workflow in PROJECT.md, the environment plan, inventory and the linked handoff; GitHub is the sync point for both machines.
- Handoff includes broker setup/testing/password-compatibility scripts, serial access/export helpers, source review, bench checklist and sanitized four-device radio/MQTT/GPS evidence. Private credentials, channel key, flash backups, raw GPS captures, local databases and private bench helpers remain ignored on the Dell; they are not transferred through GitHub.
- Portal is still the hosted simulation. Live MQTT ingestion was explicitly brought forward but no adapter/deployment has started. The next developer must settle demo-data handling, provision stable physical identities and build/test the persistent worker before claiming live portal tracking. No additional hardware or radio changes in this handoff.

Next useful step on Windows/WSL: pull main (including submodules), read docs/operations/development-handoff.md, then resume the live ingestion adapter. Python compilation, shell syntax, Git whitespace and unchanged pinned firmware-submodule checks pass. The isolated broker test cannot be rerun on this Dell because `mosquitto_passwd` is absent; the earlier recorded remote test pass is retained without claiming a new pass. Publication follows this checkpoint commit.

## 2026-10-14 — Live portal MQTT integration brought forward

- Owner asks to connect MQTT to the portal and identify prerequisites. Reviewed existing deployment, normalized ingestion boundary and private bench subscriber code. Broker worker credentials and channel key already exist privately; the remaining software is a persistent decoder/identity adapter and hosted worker integration, replacing synthetic updates.
- Recommend first connecting the two verified V4 trackers and two V3 gateways for read-only GPS ingestion, preserving measurement timestamps and per-gateway receipts while deduplicating displayed observations. Confirm handling of existing fictional portal records before changing hosted data. Keep live devices powered with GPS sky view for end-to-end verification. No deployment, credential transfer, database change, radio transmission, ticket resolution, commit or push performed; existing edits preserved.

Next useful step: confirm whether the hosted portal should show only real bench devices or retain a separately labelled simulation, then implement/test and deploy the ingestion worker with a backup and live GPS verification.

## 2026-10-14 — Replacement hotspot and real GPS delivery verified

- Owner reconnects nodes, reports satellites and supplies new hotspot credentials. USB permissions changed; owner restores scoped ACL access after interactive sudo is required. Initial automatic permission-review timeout succeeds on its permitted retry. Save new Wi-Fi privately, apply to both V3s and verify private equality with MQTT config unchanged and LoRa transmit disabled. Both gateways reconnect to Wi-Fi/MQTT.
- Direct snapshots show internal GPS positions on both V4s. First observation spanning the hotspot transition sees B001 only; subsequent clean automatic observation sees one real GPS report per V4 through both gateways (4/4 paths). B001 reports 9 satellites and 21.13-second fix age; B002 reports 8 satellites and 35.40/35.41-second fix age at subscriber receipt. Original GPS measurement timestamps survive encrypted radio/MQTT delivery. No forced/synthetic position used. [TEST-004](field-results.md#test-004--automatic-gps-positions-through-both-mqtt-gateways).
- Raw coordinates, Wi-Fi/broker credentials and evidence stay ignored/private. Temporary observer exits after collection; no continuous recorder or live portal adapter installed. Short sample does not establish sustained delivery, phone-free startup, outage behavior, battery runtime or field performance. No firmware source change, inventory quantity change, ticket decision, commit or push; unrelated edits preserved.

Next useful step: connect a persistent MQTT ingestion worker to the existing portal database, then measure sustained GPS freshness/duplicate handling, power-on behavior and battery runtime separately.

## 2026-10-14 — Actual Heltec MQTT delivery and reboot recovery pass

- Owner completes the guarded broker password compatibility fix. Retrieve its private export, confirm both gateway credentials are 30 bytes, then provision both V3s. Exact saved credentials, TLS endpoint/root/encrypted-protobuf settings, uplink-only channels and disabled LoRa transmit pass private readback. Both gateways connect to the hotspot and public broker; worker credential remains usable.
- Each V4 encrypted fixture reaches the read-only worker subscriber through both V3s: 4/4 member/gateway checks pass. Independently reboot both V3s, verify every networking/receive-only setting persists, then confirm reconnection and repeat fresh fixtures: 4/4 pass again. Subscriber verifies broker certificate/hostname; stock Heltec direct TLS uses `setInsecure()`, so its server identity validation is not established. Serial debug logging is suppressed; credentials/configs/captures stay ignored/private.
- Update sanitized readiness, inventory and TEST-003 records. All four boards are stock-flashed/profile-verified and ready for passive GPS/runtime testing. No fresh GPS positions collected, portal adapter integrated, battery runtime measured, broker/hotspot outage test or sustained delivery claim. No hardware count changes, firmware source patch, ticket decision, commit or push; unrelated edits preserved.

Next useful step: give both GPS-equipped V4s sky view and verify fresh GPS measurement timestamps through both gateways, then measure phone-free restart/reporting and battery runtime. Portal ingestion remains a separate unfinished adapter.

## 2026-10-14 — Hotspot connected; stock MQTT password limit found

- Owner supplies hotspot/broker credentials and reports a hotspot reset in compatibility mode. Native NetworkManager confirms actual SSID is the original hotspot name; the parenthesized string is its Wi-Fi interface label. Both V3s associate and obtain IPs after recovery. Saved SSID/password matches are checked privately; credentials remain mode-0600 under ignored `private/bench/`, never copied into project records.
- Broker SSH recovers after network blip; reading its root-private credential file requires interactive sudo. Prepared/uploaded a private export helper, but owner supplies credential JSON instead. Permission-review timeout recovers on the single permitted retry; no ongoing approval rejection.
- Certificate/hostname-validating read-only subscriber authenticates to public broker. Gateway provisioning still leaves MQTT off and account settings unchanged: supplied gateway passwords are 48 bytes, whereas pinned NanoPB MQTT password field allows 31 bytes plus terminator. Actual two-V4/two-V3 MQTT fixture test receives zero of four expected deliveries; this is a failed client-provisioning test, not proof of a broker transport/ACL defect. No GPS/portal claim.
- Correct future fresh-installer gateway generation to 30 characters, retaining 48-character worker credentials. Prepare/upload [guarded live compatibility fix](../scripts/server/fit-v3-mqtt-passwords.py) that replaces only the two gateway passwords, preserves worker/ACL/listeners, backs up privately, reloads, verifies and exports privately. [Isolated real-Mosquitto tests](../scripts/server/test-fit-v3-mqtt-passwords.py) pass new/old authentication, worker/hash/ACL preservation, rerun idempotency and injected-failure rollback. Syntax and local/remote SHA256 match; no production account changes performed.
- Owner sudo execution requested as the remaining privileged step; new values will be retrieved privately, not pasted. All radios retain their verified roles; no firmware source patch/flash, ticket resolution, commit or push. Other in-progress changes preserved.

Next useful step: owner runs the uploaded compatibility fix, retrieve its owner-private export, provision/read back both V3 accounts, then verify live radio-to-MQTT delivery and reconnect. Fresh GPS and portal ingestion remain separate.

## 2026-10-14 — Four Heltecs prepared; local radio smoke passes

- Owner runs runtime serial helper, reconnects missing V4, selects US on the three flashed nodes and confirms attached antennas. Runtime rules preserve access through USB re-enumeration. Newly reconnected V4 `!699ca878` is original 16MB/2MB PSRAM hardware on old `2.7.15.567b8ea`; 1200-baud touch reaches bootloader. Privately back up its configuration/full flash, then clean-install and independently verify stock factory/recovery/filesystem images. All four now run `v2.7.26.54e0d8d`; firmware source/submodule unchanged.
- Finish shared private channel and full saved profiles. Bench B001/B002 V4s have GPS enabled, 60-second acquisition, 120-second reporting, smart/fixed position off and measurement timestamp flag; G001/G002 V3s have no GPS and remain transmit-disabled. US initialization re-enables TX/generates keys; restore each intended role explicitly. First second-V4 readback catches partial setup; reapplication after initialization passes. Final independent reboot checks every specified field and all four bench labels/roles.
- Local encrypted text fixture smoke: each V4 reaches both V3s, four of four reception checks pass. No RAK, actual MQTT connection or fresh position event in this short run. Normal hop limit 3 does not establish direct-only paths. [Sanitized TEST-001/TEST-002 evidence](field-results.md#test-001--stock-heltec-provisioning); raw backups/configs/packets/key remain ignored/private.
- Wi-Fi/MQTT remain disabled while current endpoint/root/TLS/encrypted protobuf settings are staged. Bench host cannot reach authorized broker SSH via public or recorded private address from its current connection; no broker fault/configuration change inferred. Requested local private credential paths and Wi-Fi choice; no secrets requested in chat. Existing software MQTT confirmation remains valid; actual gateway delivery/portal adapter and GPS freshness/runtime remain to test.
- All four firmware/profile/role checks and local fixture reception pass. No ticket decisions, purchases, survey/SOS implementation, firmware patch, commit or push. Preserve unrelated in-progress broker records/scripts.

Next useful step: privately provision both V3s' selected Wi-Fi and fresh broker accounts; obtain/measure phone-free fresh GPS fixes with sky view, then verify their original measurement timestamps through actual MQTT packets. Portal ingestion and field/runtime tests remain separate.

## 2026-10-14 — Three Heltecs flashed; V3 profiles prepared

- Owner grants temporary serial access. Privately export configs/full original flash for original V4 `!699c2ed8` and V3s `!9ea13cc0` / `!849ad7a0`. Second V4 with USB serial ending `A878` is absent before inspection. Confirmed 16MB/2MB PSRAM V4 and 8MB V3 chips; frequency/antenna/current-location confirmation requested before RF enablement.
- Clean-install stock `v2.7.26.54e0d8d` on all three accessible boards from checksum-verified release archive and target-manifest partition offsets. Esptool independently verifies factory, recovery/OTA and filesystem images. First V3 no-reset connection attempt fails before erase; CP2102 default reset succeeds. Firmware submodule/source unchanged.
- Both V3s boot stock release and receive shared private-key uplink-only profiles. Region UNSET, transmit disabled, GPS not present, Wi-Fi/MQTT disabled; endpoint/root/TLS/encryption staged without credentials. Bulk config writes initially drop settings; single-write probe succeeds, private logs show UART0 buffer overflow, and 0.4-second pacing plus 3-second commit hold removes overflows and processes MQTT settings. Check saved fields and reboot rather than trusting host command success.
- Applied diagnosing-bugs skill to V4 serial failure: bounded probes time out, RTS reset leaves flasher accessible, watchdog reset re-enumerates as ACM0 and loses temporary ACL. Image verification passes; post-boot API/GPS/profile verification still awaits owner-local access. Prepared [runtime serial ACL helper](../scripts/bench/grant-heltec-serial-access.sh), limited to three observed hub sockets and missing V4 serial and expiring at reboot; owner root execution requested, not performed by agent.
- Final independent reboot verifies both V3 bench short names and complete profiles, including staged MQTT endpoint/root/TLS and shared private channel; all assertions pass. Shell/Python syntax and documentation whitespace pass, firmware checkout stays clean. Recorded inventory and [TEST-001](field-results.md#test-001--stock-heltec-provisioning). No RF/GPS/runtime/actual MQTT results, ticket decisions, firmware code changes, commit or push. Unrelated MQTT records/scripts preserved.

Next useful step: owner runs runtime access helper, reconnects missing V4 and confirms 915MHz/antennas/US location; finish V4 identification/setup, privately provision V3 Wi-Fi/current broker accounts, then begin phone-free GPS/RF/MQTT measurements.

## 2026-10-14 — Four Heltecs connected; bench flashing preparation

- Owner confirms MQTT tested and connects 2 V4 / 2 V3 boards, authorizing formatting/flashing as needed. Authenticated MQTT delivery/ACL evidence is already recorded in the following completed broker session; no broker re-test needed for initial preparation.
- Escalated read-only USB discovery confirms two native Espressif ports and two CP2102 ports. Sandbox hides the device nodes, and host serial opens fail with OS permissions: current user is not in dialout and noninteractive sudo requires a password. Requested owner-run temporary user ACL on exactly the four connected ports; physical frequency/antenna/location confirmation requested before enabling transmission.
- Installed esptool 5.5.0 / Meshtastic Python 2.7.11 in ignored project `.venv`; downloaded the official pinned `v2.7.26.54e0d8d` ESP32-S3 archive into ignored private storage. GitHub release SHA256 `339650ced8b8c859751f04be69c6af845fea96baca1327518f199afd2595a9d4` matches; V3/V4 factory image headers/checksums validate and specify 8MB/16MB respectively. Prepared private configuration inspection/backup helper; exact board identification precedes image selection.
- No serial configuration read, flash/erase, device configuration write or RF test yet. Existing project edits and clean firmware submodule preserved; no commit requested/made.

Next useful step: owner grants temporary serial access and confirms antenna/frequency/location; inspect/back up each board, flash matching pinned stock images only where needed, then save/read back a shared private bench configuration.

## 2026-10-14 — Authenticated public MQTT delivery and ACL checks pass

- Owner runs the uploaded public-check script with sudo and supplies all PASS lines. Existing V3 accounts publish non-retained synthetic messages through certificate-validated public TLS and the worker receives them. Anonymous/invalid logins, worker writes, gateway reads and JSON/unrelated-topic writes are denied. Credentials remain server-private and no broker configuration changes occur during the check.
- Closed the temporary SSH relay; independent SSH confirms no 18884 listener and active Mosquitto. Updated current broker/project/bench records to reflect successful authenticated software testing, preserving historical pending observations. No radio/GPS/reconnect/runtime or live portal ingestion claim.
- Documentation whitespace checked. No commit requested/made; other in-progress bench work preserved.

Next useful step: begin selected-build V4 GPS/V3 MQTT hardware bench using the recorded checklist, verify actual packet delivery and reconnect, and implement live portal ingestion when brought forward. Broker-side initial-uplink readiness is verified.

## 2026-10-14 — Authenticated public MQTT test prepared

- Owner asks how to verify valid-account delivery. Added/uploaded a read-only configuration check script reusing the established MQTT 5 protocol/ACL test helpers; reset entry point is never invoked. Reads server-private credentials only under owner-interactive sudo, sends non-retained synthetic fixtures and validates gateway publish/worker receipt and denied permissions over certificate-validated TLS.
- Broker-origin direct public endpoint probe times out, potentially due to router hairpin routing; cause unconfirmed. Opened a temporary reverse SSH relay bound to broker loopback 18884, routing through this external test host to public TLS 8883. SSH independently confirms loopback binding and the credential-free public TLS/anonymous-rejection check passes. Initial relay connection timed out; retry succeeds. No credentials read/transmitted yet, permanent service change or authenticated PASS claimed.
- Python syntax/upload checks and documentation whitespace checks pass. Preserved other in-progress bench records. No commit requested/made.

Next useful step: owner runs uploaded check script with sudo and relay options, shares status only; investigate any failure, then close the temporary relay. Record authenticated result before declaring external account/topic testing complete.

## 2026-10-14 — Heltec V3/V4 bench readiness verified against records and sources

- Owner requests bench readiness verification. Reviewed project/tracker, inventory, planned test criteria, MQTT handoff, worker and clean release-pinned firmware submodule. Prepared [bench checklist](../docs/operations/heltec-bench-checklist.md) and delegated [primary-source review](../docs/research/heltec-bench-source-check.md).
- Stock configuration supports a small V4 GPS / V3 receiver evaluation after exact revision/image, GPS wiring, power/antenna, radio settings and viewer checks. Two GPS-equipped V4s and nine GPS-less V3s are owner-reported stock; condition and availability at this session remain unverified. No mandatory GPS patch identified. The six-member field pilot still needs planned additions and later relay/runtime/outage evidence.
- Public TLS/broker rejection and local ACL evidence exist, but valid-account external delivery remains to test. Confirmed pinned MQTT source logs credentials, disables TLS certificate verification and gates other-node uplink at public-IP brokers by the packet's OK-to-MQTT flag. Recorded private-log/isolated-credential precautions and explicit member forwarding configuration.
- Full live portal bench requires MQTT/protobuf adapter work; worker remains simulation/replay-only. Initial broker ACLs still prevent portal downlink; survey responder/GUI remain deferred/unimplemented. No ticket claimed/resolved, hardware/inventory quantities changed, server changes, credentials read, firmware build/flash or measured bench results. No visible USB serial radios in the agent environment. Preserved existing unrelated edits; no commit requested/made.

Next useful step: identify one V4 revision/GPS connection and one V3 radio variant, select matching stock images and save/read back a private bench profile, then run phone-free GPS to local receiver before adding authenticated MQTT uplink.

## 2026-10-14 — Nginx-to-Mosquitto access restored and publicly verified

- Owner runs the guarded backend installer successfully. It retains loopback/accounts, adds broker LAN 1883, privately backs up configuration/firewall, and allows only Nginx's `192.168.12.254` source before blanket IPv4/IPv6 1883 deny. Owner supplies active UFW output and local anonymous-rejection PASS; SSH independently confirms active Mosquitto and both listeners.
- External `mqtt.snorr.org:8883` verifies TLS 1.3 and the matching certificate. Anonymous and invalid-account MQTT CONNECT requests receive not-authorized CONNACK in 0.11/0.12 seconds, replacing the earlier 10-second closes and confirming proxy-to-broker MQTT reachability. Public 1883 times out from the test origin.
- Valid-account publish/subscribe, external ACLs, unrelated-LAN denial, actual firmware/reconnect and certificate renewal remain untested. No credentials read/transmitted or operational packets published. Script syntax/checksum and documentation whitespace checks pass; no commit requested/made.

Next useful step: privately run authenticated synthetic publish/subscribe and ACL tests through public TLS, then integrate the selected gateway/worker when brought forward. Survey and other held work remain deferred.

Bench-readiness guidance — Owner asks whether more Mosquitto configuration is needed. Reviewed installed-template account/ACL design and current official Mosquitto/Meshtastic documentation. No additional broker configuration identified for initial passive-tracking uplink bench; authenticated public delivery/permission checks remain the next verification. Recorded V3 endpoint/root/settings and corrected legacy hostname in the handoff. Current ACLs intentionally block portal downlink and the existing portal worker remains simulation-only; those later integrations are separate from broker transport readiness. No account/ACL/device/server change or additional ticket resolution. Documentation whitespace checked; no commit requested/made.

## 2026-10-14 — Public MQTT endpoint tested after DNS/Nginx rollout

- Owner resumes endpoint testing and supplies root SSH on `mqtt.snorr.org:64582`. DNS resolves, TCP 8883 connects, and TLS 1.3 verifies a matching Let's Encrypt certificate expiring 2027-01-11.
- Two anonymous MQTT 3.1.1 CONNECT probes each close after about 10 seconds without CONNACK; initial 8-second probe times out. Public 1883 times out from this origin. TLS rollout is verified; Mosquitto forwarding/authentication/ACLs are not.
- Root SSH rejects available key/configured 1Password agent. Requested existing key/account information without secrets. No server changes, credentials read, authenticated traffic, real packets or hardware tests. Prior loopback-only listener is a possible separate-proxy obstacle, not a newly confirmed cause.
- Recorded sanitized results in sites and the connectivity ticket. No commit requested or made.

Next useful step: restore authorized SSH access, inspect current Mosquitto listener/firewall and Nginx stream upstream/error logs, then verify authenticated publish/subscribe and topic ACLs through public TLS. Survey and broader integration remain deferred.

Follow-up — Owner corrects SSH account to `setheth`; SSH succeeds. Active Mosquitto is reverified on loopback 1883 only, with anonymous local CONNECT returning not authorized immediately; Nginx is inactive on this host, which has no 8883 listener. A separate edge cannot reach the loopback backend. Sudo requires a password, so requested owner-run UFW status and Nginx private source/upstream details before configuring restricted LAN access. No remote changes or credentials read. Next useful step is the restricted backend listener/firewall configuration, followed by external MQTT auth/ACL verification.

Backend preparation — Owner supplies firewall rules and Nginx source `192.168.12.254`; broker LAN address is inspected as `192.168.12.51`. Added/uploaded guarded private-backend installer without resetting accounts; local/remote Python syntax and upload checksum match pass. Installer awaits owner-interactive sudo, checks active/default-deny UFW and expected configuration, backs up privately, restricts 1883 to proxy, preserves loopback and rolls configuration back on broker verification failure. No privileged changes executed. Next owner runs the uploaded installer, shares sanitized status and confirms Nginx upstream `192.168.12.51:1883`; then repeat external MQTT tests. No commit requested/made.

## 2026-10-13 — Portal LXC deployed through Cloudflare

- Owner confirms LXC creation, authorizes root SSH setup and chooses `meshlink.spp.lol`. Inspected Ubuntu 24.04.5 amd64 with 4 CPUs, 8 GiB RAM, 512 MiB swap and 64 GiB SSD-backed root filesystem; recorded virtual resources without altering radio counts or inventing costs. Portal hosting resumes; MQTT/survey holds remain.
- Added reproducible deployment source for static Nginx/PocketBase/Python simulation services, private persistent state, restricted public API routes, per-client proxy IP/throttling and Ubuntu security updates. Owner installed/configured the existing remotely managed Cloudflare connector; preserved it and verified four connections plus the loopback-8080 route. No second tunnel, router forwarding, MQTT adapter or Cloudflare protection change.
- Isolated the hosted worker under a separate OS account with only its own credential JSON; verified ingestion succeeds while admin credentials/database reads are denied. Native development retains its original credential path. Backend checks rerun after this worker-source change.
- Daily 02:30 Pacific root-private backups retain 14 local archives, quiescing the worker/API for consistent state and including matching source/build. Verified checksum, SQLite integrity, restored credentials/assignments/messages/incidents/events and retained history via a separate loopback API; live state was not replaced. Off-host/Proxmox backups remain pending owner-selected storage/access.
- Verification: existing 27 backend and 8 frontend tests, TypeScript/production build, Nginx/shell/Python syntax, loopback sign-in/role boundaries, independent client throttling, restart persistence, isolated restore and credential-free public HTTPS/certificate/API boundaries pass. Existing MapLibre bundle warning remains. Public DNS is correct; LAN DNS retains an older negative IPv4 result, blocking desktop browser review during setup. Cloudflare blocks Python's default user-agent; curl probes pass without altering protection.
- Automatic approval review rejected transmitting generated admin credentials through Cloudflare for a public sign-in test. Replaced that test with credential-free HTTPS probes and retained loopback authenticated checks; no credentials/tokens published. Owner public browser sign-in and actual reboot recovery remain unverified. Preserved unrelated battery-box model. Completed source/records checkpoint is committed/pushed to main; final response reports result.

Next useful step: owner opens the portal and signs in using privately viewed generated credentials after LAN DNS catches up; configure off-host Proxmox backups, then resume live MQTT integration only when the owner brings it forward.

## 2026-10-13 — Ubuntu LXC portal sizing

- Owner resumes portal hosting setup and selects Ubuntu LXC on Proxmox. Reviewed the current PocketBase/Python/static React stack and primary Proxmox/Ubuntu documentation; recommended 2 cores, 2 GiB RAM, 512 MiB swap allowance and 32 GiB SSD-backed storage in an unprivileged Ubuntu 24.04 LTS container, with direct services, a stable LAN address and start at boot. Recorded the proposed hosting configuration in sites; these are estimates, not confirmed allocations or measured capacity.
- No container created, service deployed, broker integration resumed or hardware count changed. MQTT and other held work remain held. Documentation whitespace checked; unrelated storage-box file preserved. No commit requested or made.

Next useful step: owner creates the container and supplies its Ubuntu version and LAN address privately as appropriate; then configure access, pinned runtimes, persistent services and a tested backup/restore before HTTPS rollout.

## 2026-10-13 — Project held and desktop handoff checkpoint

- Owner requests holding the survey issue, wrapping all current project progress and pushing it to GitHub for another desktop. Released the survey claim, left it open/deferred, recorded the project-wide hold in the map/project brief and added [desktop handoff](../docs/operations/desktop-handoff.md). Resume only at owner direction; no planning decision falsely marked complete.
- Checkpoint includes accumulated portal launcher/test/documentation work, broker maintenance/reset scripts and sanitized hosting/handoff research, hardware/field planning records and accepted RAK/Dell survey requirements. Firmware submodule remains clean at the published release pin; no survey firmware/GUI built or hardware-tested.
- Verification: all 27 backend tests pass with localhost sockets enabled (initial sandbox run could not create sockets). Portal tests, TypeScript checking and production build pass; existing large-map-bundle warning remains. Both server shell scripts pass `bash -n`; reset script passes Python compilation. Publication candidate secret-pattern scan finds no matches; Git excludes private credentials/databases/raw tracks, binaries, dependencies and generated output. Documentation diff check passes. Privileged server scripts were not rerun; external broker path and firmware/hardware behavior remain unverified.
- Owner-authorized commit/push checkpoint targets `main` on `origin`; final response reports commit and push result. GitHub contains reproducible source/planning, not the current ignored local database or credentials. New-desktop setup and private-data transfer limits are documented in the handoff.

Next useful step: clone/update recursively on the other desktop and read the handoff. Keep work held until owner resumes the selected task.

## 2026-10-13 — Survey GUI behavior accepted and live map added

- Owner accepts proposed scheduling, run controls, disconnect handling and automatic logging with optional labels/configuration segments. Added live GPS/signal map to active tester scope to help revisit dead spots during a run.
- Recorded success/timeout attempt markers, per-repeater inspection and an independent timestamped GPS stream as the map design direction. Distinguish failed round trips from directional loss and stale/no-fix locations from precise measurements. Offline basemap preparation remains to verify; map availability must not block logs/readouts.
- Survey draft/ticket updated; broad operations ticket remains claimed pending field/power requirements. No GUI/firmware implementation or hardware test. Documentation diff checked; unrelated edits preserved, no commit requested or made.

Next useful step: implement the touchscreen survey prototype and RAK responder, verifying selected-build GPS availability, PKI and direct-only exchanges; verify offline map preparation before field use.

## 2026-10-13 — Touchscreen multi-repeater survey GUI requirements

- Owner requires a simple touchscreen Dell GUI with large buttons, touch input pads, one-or-more repeater selection and interval/other parameters. Recorded accepted requirements in the survey draft/ticket.
- Proposed sequential round-robin scheduling with one outstanding ping and interval between individual attempts, configurable timeout/continuous or finite runs, automatic private logging with configuration labels, and pause/explicit resume after tester disconnection. These behavior choices await owner input; no UI built, firmware changed or hardware tested.
- Broader operations ticket remains claimed. Documentation diff checked; unrelated edits preserved, no commit requested or made.

Next useful step: settle scheduling, disconnect behavior and run labels, then implement the simple touchscreen tester alongside the pinned-release responder.

## 2026-10-13 — Always-available survey responder accepted

- Owner selects always-available response to authorized survey pings because RAK nodes will be placed in hard-to-reach locations. Recorded rationale and behavior in the repeater ticket and survey draft: no physical visit/per-survey enable step, Dell drives attempts, and RAK responds only to valid requests authorized by the separate survey public-key allowlist.
- First-prototype direction now includes RAK4631, Dell GUI and transferable V4 native-PKI keys. Broader field/power decisions remain open; operations ticket stays claimed. No implementation, provisioning, build, flash or RF test. Documentation diff check passed; unrelated edits preserved. No commit requested or made.

Next useful step: specify the minimal GUI/logging controls and implement the pinned-release responder/tester prototype, followed by direct-only and authorized/unauthorized bench checks when hardware is available.

## 2026-10-13 — Portable survey key accepted

- Owner accepts transferring the tester private key to the V4. Recorded native PKI with a separate survey public-key allowlist as the chosen authentication approach in the existing repeater ticket and survey draft. Replacement tester hardware requires keypair restoration and node/key discovery; no admin rights implied.
- RAK4631 target and Dell-driven GUI remain confirmed. Survey enablement and GUI defaults remain open; broader operations ticket not resolved. No secrets generated/read, provisioning, firmware changes, build or flash performed. Documentation diff check passed; unrelated edits preserved, no commit requested or made.

Next useful step: settle whether the authorized responder is always available or explicitly enabled, then prepare the minimal responder and Dell GUI bench prototype.

## 2026-10-13 — RAK target and GUI tester clarified

- Owner confirms RAK4631 cores and Dell-driven V4 testing with a GUI/readout; updated inventory without changing counts or claiming verified frequency variants/condition.
- Checked pinned firmware routing/admin key handling and primary cryptographic documentation, with a delegated read-only source check. Native survey public-key authorization is feasible; keys live on tester radios, can migrate to replacement hardware, and still need node/key discovery. Proposed a survey-only allowlist separate from admin privileges. Dell-held payload signatures are an alternative requiring additional implementation/replay design.
- Recorded accepted hardware/test-control direction and proposed authentication/GUI scope in the existing survey ticket/draft. No full operations decision resolved, key generated, firmware changed, build, flash or hardware test performed. Existing edits preserved; no commit requested or made.

Next useful step: owner chooses radio-held native PKI versus Dell-held signing key; then specify survey enablement and GUI controls before implementing the first bench prototype.

## 2026-10-13 — RAK survey firmware pre-build readiness

- Used owner-invoked Wayfinder and its grilling/domain-modeling guidance to review the existing repeater survey ticket, inventory, proposed exchange/logging contract and firmware workspace. Confirmed clean firmware checkout at the recorded release commit; preserved unrelated working-tree edits.
- Identified immediate prerequisites: exact RAK core/radio variant, owner choice of tethered versus autonomous tester, and survey enable/access policy. Recommended Dell-controlled V4 testing first and explicitly enabled responder access for a configured tester; these remain proposals. Site selection, solar endurance and field acceptance thresholds can follow the first bench prototype.
- Added the readiness review to [Define repeater operations and direct-link placement testing](../.scratch/pilot/issues/14-repeater-operations-survey.md). No decision resolved, firmware implementation, build, flash or RF test performed. No commit requested or made.

Next useful step: identify the selected RAK core and settle tester control/access, then verify the direct-only module/API paths against the pinned release before implementation.

## 2026-10-13 — Firmware fork added and RAK release branch published

- Owner requested adding `lfg-seth/firmware` as a submodule and creating a current-public-release RAK branch. Added `firmware/`, configured its tracked branch as `snorr/rak-survey`, and published that branch to the fork.
- Verified GitHub latest public release is `v2.7.26.54e0d8d` (title Beta, GitHub prerelease=false), commit `54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb`. New branch matches that release exactly; existing fork develop remains `76d5156e72d9d9aaa9722b7bbc1336335b685984`. No old customizations merged or history rewritten.
- Initialized the release-pinned protobufs and meshtestic submodules; verified clean firmware tree and remote branch SHAs. Added [workspace/setup notes](../docs/research/firmware-workspace.md). Exact owned RAK core remains unknown; no firmware build, flash, RF transmission or hardware test performed.
- Commit scope is submodule configuration/pointer, setup notes and this session entry. Existing portal/broker/repeater-planning working-tree changes are preserved outside this commit. No tracker decision resolved.

Next useful step: identify the RAK core, then check the dedicated direct-only ping/pong module design against this pinned release before implementing and building it.

## 2026-10-13 — Dedicated direct-link survey module reviewed

- Owner asks about firmware modifications/plugins, a dedicated packet type, addressed zero-hop exchanges and adjustable usage restrictions. Reviewed upstream primary module/port/routing/airtime/radio/API sources and appended [implementation findings](../docs/research/repeater-operations-survey.md#dedicated-firmware-module--follow-up-source-review) to the existing survey draft/ticket discussion.
- Recommended compiled-in RAK responder module on a private application port, explicit PING/PONG payload, zero-hop/no-ACK requests and replies, and client-controlled attempts. Noted generic reply/ACK hop rewriting, MQTT exclusion, duplicate handling and queue/actual-TX distinctions. Stock V4 with Dell API control is a candidate minimal prototype; autonomous V4 testing and precise radio-time logging may need client firmware.
- Distinguished configurable survey scheduling/congestion policies from regional radio constraints and hardware queue/half-duplex operation. No unrestricted RF operation, global restriction removal, final port number or implementation approved/inferred. Reviewed moving upstream sources only; revision lookup failed, so release/commit pinning remains before implementation.
- No firmware cloned, built/flashed, hardware tested, portal/MQTT work resumed or new decision resolved. Existing edits preserved. Documentation checks only; no commit requested or made.

Next useful step: identify target RAK core and V4 firmware/API versions, pin a firmware revision, and verify a minimal private-port responder plus Dell-controlled direct-only exchange on three nodes.

## 2026-10-13 — Repeater operations and placement survey opened

- Owner steps back from portal work and brings solar RAK repeater operations forward: 2–4 18650 cells, Muzi whip or fiberglass antenna, firmware ping/pong responder and GPS-equipped V4 testing node tethered to Dell log storage. Captured intended builds without changing stock counts or assuming installation permission.
- No installed `$wayfind` skill found after local search; used repository-defined Wayfinder tracker conventions. Created/claimed [Define repeater operations and direct-link placement testing](../.scratch/pilot/issues/14-repeater-operations-survey.md), retaining claim pending owner input. No non-research decision resolved; MQTT remains held.
- Reviewed primary RAK electrical documentation, Meshtastic range-test/role documentation and packet schema. Recorded [draft operations/survey plan](../docs/research/repeater-operations-survey.md): per-packet metrics in both directions, verified direct-only paths, timeout/GPS-age logging, controlled antenna comparisons and separate later GPS relay validation. Recorded power autonomy, cell/charger/cold-charge protection, recovery, mounting and service-access questions. No firmware built, hardware tested or coverage measured.
- Asked owner for prior-test candidate landmarks/routes and coverage gaps. Outstanding: exact RAK/core/cell/panel builds, no-sun endurance target, survey cadence/sample size and route acceptance thresholds. Existing unrelated working-tree edits preserved. Documentation checks only; no commit requested or made.

Next useful step: capture candidate sites and required routes, agree no-sun endurance, then identify one representative RAK power build and bench-check the direct-link responder/logging contract before a field survey.

## 2026-10-13 — Worker readiness review

- Owner asked what comes next and whether DNS completion makes the worker ready for Mosquitto. Inspected worker code, backend contract/tests and current broker handoff. The Python worker supports authenticated synthetic ingestion and normalized JSONL replay only; it has no MQTT connection/subscription, TLS/broker credential configuration or selected-firmware decoder. DNS completion alone will not enable live tracking.
- Fresh Mosquitto local authentication/ACL readiness is recorded, but its last verified listener is loopback-only. Separate-host Nginx requires restricted private access, followed by external TLS/auth/topic verification. No remote probes, broker changes, implementation or tests performed in this review; existing edits preserved.

Next useful step: implement a receive-only MQTT-to-normalized-ingestion adapter with explicit simulation/live modes, reconnect/outage handling and decoder tests using sanitized selected-build packets; verify the external broker path with Mike when ready. No commit requested or made.

## 2026-10-13 — Fresh pilot Mosquitto installed

- Owner ran adapted reset and supplied successful live authentication/ACL test output. Old broker configuration/accounts/data/logs and broker-specific renewal state archived privately at `/root/meshlink-archive/mqtt-legacy-20261013T204408Z`; fresh account credentials stored root-private on server, not read/published.
- SSH follow-up confirms active Mosquitto under its own account, loopback `127.0.0.1:1883` only, no VM 8883 listener, config/data/log directories mode 0750 and enabled scheduled-maintenance reboot timer. Updated current server/project/handoff records from prepared to installed. Unrelated backend/portal launcher edits preserved.
- Local broker accounts/ACLs are ready for tracking ingestion; no command publishing/downlink yet. Restricted separate-host Nginx access needs its private source IP. External TLS/DNS/proxy path, actual V3/worker adapters and SSH password hardening remain pending. No credentials, raw messages/tracks or archive contents accessed during verification.

Next useful step: Mike supplies Nginx private source IP, then enable only that proxy's private 1883 access and test public `mqtt.snorr.org:8883` when Mike is ready. Documentation diff checked; no commit requested or made.

## 2026-10-13 — Broker-only setup resumed and adapted

- Owner authorized making the fresh Mosquitto updates while Mike's external infrastructure remains pending. Inspected live service/private interface; no fresh marker found and sudo still requires local password. Preserved unrelated backend launcher/README/test edits visible in Git.
- Adapted/uploaded reset installer to private 1883, no broker certificates/hooks, intended client hostname `mqtt.snorr.org`, old MQTT archive plus broker-specific old renewal configuration archive, fresh per-gateway and worker credentials/ACLs. Default loopback-only because proxy source IP is unknown; LAN mode requires explicit addresses and active source-restricted UFW preflight.
- Private-backend isolated auth/ACL tests passed. Temporary-filesystem full-flow archive/credential and injected-startup-failure rollback tests use actual isolated Mosquitto with mocked privilege/service operations; real privileged execution remains pending. [Details](../docs/research/mqtt-server-maintenance.md#2026-10-13--private-backend-reset-adapted).

Next useful step: owner runs updated script with sudo, then verify live fresh broker/archive without exposing credentials. Enable restricted LAN listener once Mike supplies Nginx source IP; external infrastructure remains deferred. No live broker reset, firewall change, commit or push performed.

## 2026-10-13 — Combined local launcher

- Owner confirms no Proxmox VM or nodes are available and brought local launch cleanup forward. Added `python3 backend/launch.py` to supervise PocketBase, the synthetic Python worker and Vite in one foreground terminal on Linux/macOS/WSL. Updated backend/portal startup instructions; individual commands remain available for debugging.
- Launcher checks installed dependencies/initialized storage and Node version, refuses duplicate launches and occupied ports, waits for API/portal readiness, binds services to localhost and keeps per-process logs in ignored private storage. Ctrl+C/termination or a child exit shuts down its process groups, stopping the worker before the API; bounded escalation handles unresponsive children. It does not install/reset data or print credentials. Synthetic observations continue to be saved while running.
- Verification: existing twenty backend/installer tests passed. Seven launcher tests passed, including occupied-port preservation, duplicate refusal, startup failure, real child cleanup and forced termination. A disposable real PocketBase/worker/Vite run on temporary ports verified API proxying, ingestion, duplicate refusal, Ctrl+C cleanup, restart with saved data and worker-failure cleanup. Existing port-8090 service was left untouched. Linux verified; macOS/WSL runtimes remain untested. Documentation diff check passed; no commit requested or made, unrelated edits preserved.

Next useful step: stop the existing individual development terminals, run the combined launcher on the Dell and review the saved portal workflows. VM deployment and hardware integration await availability; MQTT remains on hold pending Mike and owner resumption.

## 2026-10-13 — Hypothetical SNORR companion-app forks

- Owner asked whether SNORR could fork the Meshtastic iOS/Android apps and what features would suit the project. Reviewed current primary [Apple source/README](https://github.com/meshtastic/Meshtastic-Apple), [Android source/README](https://github.com/meshtastic/Meshtastic-Android), [Android fork/rebrand guidance](https://github.com/meshtastic/Meshtastic-Android/blob/main/CONTRIBUTING.md#forks-and-rebrands) and [position configuration](https://meshtastic.org/docs/configuration/radio/position/). Both apps use GPLv3-family licenses; distribution requires applicable source/notices and distinct branding under the upstream conditions.
- Suggested hypothetical priorities: GPS measurement age and explicit stale/unknown states, prepared offline field maps, cached device/member assignments, simple member controls, clear local-radio versus dispatch-feed status, and later concise messaging with honest delivery/acknowledgment states. Keep phone-free GPS and device-only SOS in node firmware; an app cannot establish radio coverage or dispatch receipt without evidence.
- Recommended a small customization that preserves the Meshtastic protocol and upstream improvements, after stock-app pilot checks identify actual gaps. Apple/Android have separate UI stacks and ongoing maintenance needs. No app cloned, built or tested; feasibility is source/documentation review only. No active ticket, wishlist activation, firmware selection change, broker work, commit or push. Existing edits preserved.

Next useful step if the owner brings app work forward: compare stock apps on the pilot devices against freshness, offline map and reconnect requirements, then select one platform and a minimal scope. Passive GPS bench testing remains the first hardware priority.

## 2026-10-13 — Next-work review

- Reviewed project records, tracker and portal build checkpoints. Recommended tested backend backup/restore as the next independent software task, followed by VM service supervision and HTTPS deployment. Live MQTT integration remains on hold pending Mike and owner resumption.
- Passive GPS bench testing remains the first hardware priority when nodes are available. No implementation, ticket change, remote check or deployment performed; existing uncommitted work preserved. No commit requested or made.

Next useful step: implement private backend backup/restore and demonstrate recovery into a separate local instance, preserving accounts, assignments, observations and history.

## 2026-10-13 — MQTT issue held pending Mike

- Owner explicitly instructed holding the broker issue until Mike completes infrastructure work. Recorded `mqtt.snorr.org` as intended endpoint, with Mike updating DNS and placing the VM behind Nginx; certificate management belongs to Mike. Completion is unverified.
- Released the connectivity ticket claim and left it open/deferred; updated map, project brief, hosting record and handoff. No broker/proxy probes, implementation, hardening or reset performed after the hold. Earlier update/maintenance verification remains recorded.
- Fresh broker reset is prepared but not executed and needs adaptation for Nginx TLS termination/private port 1883. Firewall activation, SSH-password hardening, live ACL provisioning, actual firmware/client configuration and one-gateway dispatch downlink remain unverified. Documentation diff checked; no commit requested or made.

Resume only when owner brings this issue back after Mike's work is complete. First confirm `mqtt.snorr.org` TLS/proxy reachability, then adapt/archive/reset the broker and test gateway/worker access.

## 2026-10-13 — Nginx MQTT handoff prepared

- Owner reports Mike wants Nginx to own certificates and says certificate management is handled. Prepared [consolidated handoff](../docs/operations/mqtt-nginx-handoff.md) for TLS termination on public 8883, private broker TCP 1883 restricted to Nginx, DNS/client settings, existing SSH preservation and verification. No certificate-provisioning instructions or outreach.
- Recorded current direction over earlier passthrough proposal. Actual proxy/VM addresses, separate/same-host layout and deployed configuration remain unknown. Marked existing fresh-reset installer unsuitable unchanged because it provisions broker-side TLS/certificate handling; adaptation remains before running it for this topology.
- No live broker reset, proxy/firewall/DNS change, template runtime verification or completed security hardening claimed. Documentation diff checked; no commit requested or made.

Next useful step: Mike supplies private upstream/source addresses and validates Nginx configuration; adapt the archived fresh-broker setup for the chosen private 1883 listener, then test external TLS/auth/topic access and reconnects.

## 2026-10-13 — Nginx TCP proxy proposal documented

- Owner asked about fronting the VM with Nginx. Verified primary Nginx TCP stream/HTTP routing and Cloudflare proxy-port documentation. Prepared [configuration proposal](../docs/research/mqtt-nginx-proxy.md): separate Nginx edge forwards TLS 8883 and HTTP-01 challenges to the broker VM, keeping certificates/auth/ACLs at Mosquitto.
- Asked whether proxy is on a separate host or the broker VM. Same-VM option requires different backend listener and Certbot validation configuration; no topology/installation assumed. No Nginx, router, DNS or broker change made. Existing fresh reset remains prepared, not executed.

Next useful step: confirm proxy location/management interface and private upstream address, then adapt and validate configuration with Mike's existing routing. Examples are templates and not syntax-tested on an actual proxy. Documentation diff check passed; no commit requested or made.

## 2026-10-13 — Fresh MQTT reset prepared

- Owner authorized archiving all old MQTT state and setting up the host fresh for the new pilot. Prepared/uploaded a root installer that stops/flushed broker, moves old configuration/accounts/cert copies/persistence/logs to a root-private timestamped archive and creates an empty TLS-only broker with separate V3 uplink credentials and read-only worker credential. Initial root `snorr/pilot`; commands denied until designated gateway integration. Secrets/raw data remain on server.
- Installer creates private credentials, guards against accidental repeat reset, restores old trees on reset/startup/test failure, and installs a certificate copy/reload deploy hook scoped to the current hostname. Known expired cert still blocks external validating TLS; renewal pending port-80 routing.
- Python syntax checks and isolated installed-Mosquitto tests passed for valid/invalid/anonymous credentials, gateway publish/no-delivery, worker read/no-publish and command/unrelated-topic denial. Adjusted test to verify actual delivery because SUBACK may precede ACL filtering. Full root reset/rollback/hook not exercised; live old broker unchanged. [Details](../docs/research/mqtt-server-maintenance.md#2026-10-13--fresh-pilot-reset-authorized-and-prepared).

Next useful step: owner runs uploaded reset via local sudo and shares status without credentials; verify archive/fresh service, then renew TLS and configure actual gateways/worker. Firewall/SSH hardening remains pending. Documentation diff checked; no commit requested or made.

## 2026-10-13 — Privileged broker security audit received

- Owner output confirms inactive UFW and effective SSH password authentication enabled, correcting earlier inference from the readable main config. Root login is disabled and public-key login enabled. Eleven MQTT accounts exist; secrets/hashes not read.
- AppArmor loaded/enforcing selected profiles but no Mosquitto profile listed; no broker confinement claimed. Existing generic profiles do not establish installed apps.
- Prepared firewall rules preserving local SSH 22, MQTT TLS 8883 and HTTP-01 80; dormant rules need inspection. Asked whether Mike uses SSH keys before disabling passwords. No firewall/SSH/account changes performed, and update-policy dry-run remains pending.

Next useful step: inspect/activate UFW rules and verify a fresh SSH connection; confirm Mike's key access, then fix effective SSH password policy and design topic ACLs. Documentation diff checked; no commit requested or made.

## 2026-10-13 — Security checks while port-80 routing is pending

- Rechecked active SSH/Mosquitto, enabled maintenance timer and effective apt policy. Confirmed security/stable updates plus timer-controlled reboots. Running broker uses the mosquitto account; private-key/password-file modes are restrictive. UFW enabled state and installed AppArmor tool do not establish effective rules/profiles. Broker data-directory mode is 0755; local-user visibility needs file-permission review without reading tracks.
- Credential-free diagnostic TLS negotiated 1.3 and anonymous MQTT CONNECT was rejected with code 5. Expired certificate verification bypass was confined to this probe; no credentials, topic operations or payloads accessed. This is not validating TLS or ACL verification.
- Prepared next local-sudo audit commands for firewall, effective SSH, account names, AppArmor and update-policy dry-run. No server changes. [Evidence](../docs/research/mqtt-server-maintenance.md#2026-10-13--checks-while-http-01-routing-is-pending).

Next useful step: owner supplies privileged audit output, then define/install tested per-client topic restrictions while awaiting certificate repair. Documentation diff checked; no commit requested or made.

## 2026-10-13 — Enabled broker maintenance documented

- Owner supplied successful automation installer/timer output. Recorded enabled daily security/stable updates at 03:00 Pacific (up to ten minutes jitter) and required-only reboots at 04:00 Pacific with timezone/DST handling, busy-apt skip and no missed-window reboot catch-up in the server hosting and maintenance records. Logged-in users do not block scheduled reboots. No major release upgrades enabled.
- Recorded the server-local root-only configuration archive path without copying its sensitive contents. First shown next upgrade/reboot-check dates agree with the intended Pacific window. Updated project summary.
- Activation confirmed from owner output; no future automated run/reboot/reconnection or full backup restore observed. Certificate repair, MQTT topic permissions, firewall audit, unattended-upgrade dry-run and failure response remain outstanding. Documentation diff check passed; no commit requested or made.

Next useful step: complete the privileged update-policy dry-run and certificate renewal after Mike's port-80 routing change; then finish topic/firewall checks and observe the first maintenance run.

## 2026-10-13 — Broker updated/rebooted; scheduled maintenance prepared

- Owner supplied completed OS update output and rebooted the server. Reconnected and confirmed kernel 6.8.0-146, active SSH/Mosquitto and no remaining reboot-required flag. fwupd failed during update-time restart; after boot its unit reports inactive/success, but the prior failure cause is unverified.
- Owner requested automatic updates and scheduled reboots, reporting no active maintainer. Existing automation covers security updates. Prepared/uploaded a sudo installer adding same-release Ubuntu updates, a Pacific-time upgrade window and required-only reboot timer. Proposed 03:00 updates/04:00 reboot pending owner preference; timezone expression verified and shell syntax checks passed. [Details](../docs/research/mqtt-server-maintenance.md#2026-10-13--updatesreboot-completed-automation-prepared).
- Installer is not yet run as root or enabled. TLS certificate renewal, topic ACLs and privileged firewall/effective SSH audit remain outstanding. No claim of completed security hardening or verified future automatic reboot.

Next useful step: owner enables the maintenance schedule via local sudo and shares timer/dry-run output, then continue certificate and access-control repairs. No commit requested or made.

## 2026-10-13 — Broker update/security work started

- Owner authorized server updates and security work. Read-only checks found pending Ubuntu packages and an existing reboot-required flag. Readable SSH settings disable root/password/keyboard-interactive login; apt security automation is enabled. Effective SSH/firewall/topic-account checks remain privileged.
- Sudo still requires an interactive password. Prepared, syntax-checked and uploaded an OS update script to the owner's server home directory, with root-only configuration backup, no-removal package upgrade, health checks and no automatic reboot. [Maintenance record](../docs/research/mqtt-server-maintenance.md). Script has not been run as root; no packages updated or security settings changed.
- Requested privileged audit output without secrets; certificate repair, topic ACLs, firewall review, post-update validation and coordinated reboot remain. No non-research decision resolved or commit requested.

Next useful step: owner runs the uploaded script with sudo and supplies audit results; continue TLS/ACL changes from verified settings. Shell syntax check and upload passed; runtime untested until privileged execution.

## 2026-10-13 — Broker host and domain plans recorded

- Owner confirms Mike Rollins hosts the old-pilot broker, and the owner owns its current `mqtt.spp.lol` domain. Documented the hosted service in sites/inventory and the current project brief; physical host resources, costs, backup and maintenance details remain unknown.
- Mike plans to open/route port 80 shortly; completion and renewal success remain unverified. Recorded `mqtt.snorr.vegas` and `mqtt.snorr.org` as possible future hostnames, not selected or configured.
- Verified official Certbot/Let's Encrypt guidance: a new hostname needs certificate coverage and domain validation; a transition certificate can cover old plus chosen new hostname. Recorded DNS, HTTP-01 routing, certificate deployment/reload and client-address cutover prerequisites in the transport report. No DNS, certificate, server or radio changes, outreach, expense or non-research decision resolution.

Next useful step: once Mike's routing change is ready, verify renewal dry-run and repair broker certificate deployment/reload; choose a replacement hostname separately if desired. Documentation diff checked; no commit requested or made.

## 2026-10-13 — Old pilot MQTT server investigated

- Owner provided `mqtt.spp.lol` and authorized SSH inspection. Connected and performed read-only service/configuration/renewal-status checks plus external TCP/TLS probes; no credentials, password hashes, keys, member data or broker payloads read.
- Found enabled/active Mosquitto 2.0.18 with password-required TLS on 8883. External 8883 reachable; 1883 refused and has no local listener. Public certificate expired 2026-03-24; validating TLS rejected it. Latest Certbot run failed, standalone renewal configured, no renewal-hook files found; privileged logs unavailable and cause remains unknown. No topic ACL directive found in inspected configuration.
- Recorded [findings and reuse recommendation](../docs/research/dispatch-portal-transport.md#2026-10-13--existing-pilot-broker-inspected) and existing endpoint in site records. No server changes, service restart, broker publish/subscribe, hardware test, spending or hosting decision made.

Next useful step: inspect privileged certificate-renewal failure evidence and repair/verify renewal plus broker certificate installation/reload; then verify topic access and stock V3 integration. Noninteractive sudo was unavailable. Documentation diff checked; no commit requested or made.

## 2026-10-13 — MQTT broker discussion reopened

- Owner asked to revisit the broker issue. Claimed [Check Heltec MQTT over WebSockets for Tunnel hosting](../.scratch/pilot/issues/09-heltec-websocket-research.md) and lifted the connectivity-research deferral in current project/map notes; separate wishlist features remain parked.
- Rechecked official Cloudflare, Meshtastic source/configuration and Mosquitto documentation. Stock direct MQTT transport and published Tunnel TCP still need an adapter between them. Recorded home site VPN/bridge, separate reachable private broker and custom WSS candidates in the [transport report](../docs/research/dispatch-portal-transport.md#2026-10-13--broker-issue-revisited). Recommended Mosquitto for evaluation without recording owner acceptance.
- Hosting preference remains open: all-home requirement versus acceptable external private broker. Existing no-inbound-home-port-forwarding preference and one designated V3 downlink remain intact. No broker/VM deployed, firmware changed, external service purchased, real packets tested or non-research decision resolved.

Next useful step: settle hosting preference; for a home broker, inventory available site routers/computers before choosing an adapter. Then prepare a LAN broker test on identified/pinned gateway firmware and implement the real worker adapter. Documentation/source review only; no commit requested or made.

## 2026-10-13 — PocketBase installer running-file fix

- Owner reported `Errno 26: Text file busy` from installing over the running PocketBase executable. Replaced in-place truncating writes with same-directory staging and atomic replacement. Matching binaries stay untouched; a private verification receipt allows subsequent matching installs without another download. Older installs receive one archive/binary comparison without rewriting the executable.
- Locked replacements now preserve the existing binary, clean staged files and report how to stop/retry/restart the backend. Updated native setup instructions. No database/credential replacement or service restart is required for a matching reinstall.
- Verification: all twenty backend/installer tests passed, including a real running PocketBase reinstall, offline reuse, legacy installs without receipts, checksum rejection, tampered-binary replacement and locked-file preservation. Frontend is unchanged; Windows runtime/locking behavior remains untested (the error branch is exercised with a simulated lock).

Next useful step: repeat `python3 backend/manage.py install`, then continue backend sign-in/review. Keep existing local data and credentials; initialization remains a one-time command.

## 2026-10-13 — Local authenticated backend and connected portal built

- Owner approved backend development after reviewing the portal. Implemented PocketBase 0.40.5 migrations/hooks, the normalized [backend contract](../docs/research/portal-backend-contract.md), and a standard-library Python simulation/replay worker. Pinned official release checksums and Python 3.14.3; added native install/initialization/startup/account commands and GitHub-hosted backend CI. No VM, broker or hosted service provisioned.
- Added username/password admin/member accounts, a separate restricted worker account, locked direct collection writes and server-enforced permissions. Admin account creation/password reset/deactivation preserve earlier records. Transactional assignment/release/transfer and partial unique indexes protect one active member per tracker and one active tracker per member; dated attribution and separate latest-only simulated name jobs remain intact.
- Portal contact detail also remains visible for a device that has reported messages without a GPS fix; no location pin is invented.
- Persisted original GPS/sample timestamps and quality, first receipt time, separate contact time, every normalized receipt (including duplicates/rejections), position/history records, infrastructure observations, shared messages/send attempts and audited warnings/incidents. Older/unknown/future GPS data does not replace a newer known measurement. Simulated sends require a healthy feed and exactly one designated gateway; no radio receipt, publish or rename is claimed.
- Implemented supported-capability warning evaluation with device/per-report cadence, three-interval defaults/timeout overrides, shared battery defaults/device overrides, separate fresh recovery thresholds, acknowledgment, disabled-rule history, feed-loss suppression/reconnect grace and admin-resolved latched intrusion. Demo feed loss pauses synthetic observation production and retains prior readings/warnings.
- Connected all four portal pages to authenticated persisted snapshots/mutations, retaining standalone demo mode. Browser tokens remain in memory; reload requires login, while records persist. API failure retains the last snapshot and disables sending. Fixed pending sends so successful completion does not clear newly edited drafts, and converted PocketBase query slices to ordinary arrays before reversing histories to prevent repeated/misordered entries. History queries and point controls are bounded; storage retains all received pilot data.
- Verification: fourteen integration tests passed against the actual pinned binary in temporary databases, including authorization/bypass, accounts, concurrent claims, duplicate/delayed/invalid/future ingestion, ordered unique histories, outage/manual-send evidence, rules/incident lifecycle, stale name jobs and restart persistence. Fresh setup command passed in a disposable directory. Frontend tests (eight domain tests also run in single-process mode), strict types and production build passed. Connected browser checks cover login, saved assignments after reload, messages/drafts, rules/incidents, member permissions, mobile layout and API outage; the same connected flow passed against the production preview, including a deliberately delayed-send regression check and visual review. Private data/credentials/binaries remain ignored; Vite's existing map bundle-size warning remains.

Next useful step: owner tries backend sign-in on the Dell using the private generated credentials and reviews saved workflows. Then prepare backup/restore and deployment/supervision, or integrate sanitized packets from identified/pinned hardware builds when available. Live MQTT/firmware adapters, actual radio send/name execution, field/GPU performance, backup/restore and VM/HTTPS remain unverified. MQTT transport research and wishlist features stay deferred. No hardware/inventory, expense, site permission or field measurement changed.

## 2026-10-13 — Four-page synthetic portal and map built

- Owner requested continuing portal development with the remaining pages and map. Replaced the starter with responsive Map, Users, Messages and Infrastructure pages, using six fictional trackers, five fictional members and four illustrative infrastructure devices. No actual sites, member records, hardware changes or live packets are represented.
- Added MapLibre/USGS topo and aerial layers, selectable/searchable tracker list, measurement/receipt/contact times, aging and stale/unknown/never-seen states, optional infrastructure layer and opt-in recorded history. History shows measurement-time carriers, inspected points and dashed estimated connections broken across gaps over 15 minutes. Reduced motion and map/WebGL failure keep the tracking list usable. Rechecked official map/bundler guidance and explicitly bundled the MapLibre worker for Vite production builds.
- Added browser-memory assignment claim/release/admin transfer with dated history and stable short names, separate simulated long-name jobs and latest-job outcome controls. Shared messages include manual simulated sending, author prefixes, unread notifications and drafts preserved through page changes/outages without reconnect resend. Role previews are illustrative, not authentication.
- Added infrastructure role filtering, capability-specific readings, voltage history, declared hardware configuration, event/audit history, silent persistent badges and latched intrusion acknowledgment/admin resolution with a note. Battery rule configuration is a preview; automatic warning/recovery/missing-report/reconnect evaluation awaits ingestion. Demo sensor/voltage/configuration values do not establish hardware fitment or approved thresholds.
- Verification: npm checks, strict TypeScript and production build passed; all eight domain tests also passed with Node's single-process test mode. Browser checks passed against development and production at 1440px/390px, including topo/aerial tiles, layers/history, assignment/name jobs, outage draft/manual sending, notifications, incidents/rules and role previews. Additional checks passed for blocked tiles, unavailable WebGL, reduced motion, keyboard skip navigation, browser back and narrow layout overflow. Visually reviewed page captures. Map renderer size still produces Vite's default bundle-size warning (about 286 kB compressed plus a 508 kB uncompressed worker).

Next useful step: owner reviews the prototype on the Dell, then define the normalized persistence/ingestion contract and implement authenticated PocketBase operations with a Python simulation path. No backend, VM, live radio integration, offline-map readiness, field/GPU performance or automatic warning engine is verified. MQTT connectivity and wishlist features remain deferred.

## 2026-10-13 — Owner confirms Dell development works

- Owner confirms the frontend works and can be built on the Dell. This verifies the owner's development experience for the current starter; it does not establish full-stack, MapLibre or field-device performance.
- Reviewed the existing portal build plan. Next deliverable is the synthetic tracking screen: MapLibre/USGS map, six fictional trackers, searchable list and selectable device detail, with measurement age separate from last contact, stale/unknown/never-seen states and a simulated feed outage. Follow with opt-in history, then the remaining portal pages and backend integration.

Next useful step: implement and review the tracking screen on the Dell at desktop and narrow widths. Existing CI remains the automated check; no VM or live nodes are required. No new implementation or ticket decision in this status review.

## 2026-10-13 — Accepted portal stack and development/CI baseline

- Owner accepted React + TypeScript + Vite, PocketBase and Python worker, requesting simple TypeScript and explanations. Owner reports a desktop with WSL/Docker potentially available and no Proxmox VM yet; recorded development resources without assuming desktop access or readiness.
- Added the local frontend baseline, exact npm dependency lockfile, Node version, synthetic GPS freshness examples and developer instructions. Added GitHub-hosted CI for tests/type checking/build and seven-day main build artifacts; no deployment workflow or service credentials.
- Documented native Dell development now, optional desktop integration later and VM deployment after persistence/backup/rollback preparation. Checked official Vite, GitHub Actions, Microsoft WSL and PocketBase guidance. MQTT connectivity investigation stays deferred.
- Resolved [Establish the portal development and CI baseline](../.scratch/pilot/issues/13-portal-build-environment.md). Local lockfile install, four direct measurement-age tests, strict type checking, production build and whitespace checks passed. Dependencies/build output are ignored. No browser QA, desktop/Docker verification, backend or hosted portal; first remote CI execution awaits publication/verification.

Next useful step: build/review the four-page synthetic portal, starting with MapLibre map, tracker list and device detail. No VM needed for this step. Later pin backend/worker dependencies when their interfaces are implemented.

Publication/CI evidence: pushed baseline commit `cae58e5` to `origin/main`. The first [GitHub-hosted Portal CI job](https://github.com/lfg-seth/snorr-meshlink/actions/runs/38422409410) completed successfully, including lockfile installation, checks/build and artifact upload. No deployment occurred.

## 2026-10-13 — Portal work brought forward without nodes

- Owner has no nodes available for bench testing and requested moving forward with portal design and building. Reviewed the agreed portal, naming and infrastructure warning requirements; hardware testing is not a prerequisite for a synthetic prototype.
- Prepared the [portal build plan](../.scratch/pilot/portal-build-plan.md), including first-review screen behavior, build sequence, normalized data needs, meaningful verification and owner inputs needed now versus later.
- Asked whether to adopt the previously recommended React + TypeScript + Vite frontend with the planned PocketBase/Python backend. No stack acceptance inferred. MQTT connectivity investigation and wishlist features remain deferred.

Next useful step: confirm frontend direction and build the local responsive Map/Users/Messages/Infrastructure prototype with clearly labelled synthetic data. No app implementation, deployment, packet integration or hardware tests performed in this planning step.

## 2026-10-13 — Project status review

- Reviewed the project brief, session history, pilot map, tracker, inventory, wishlist and planned field criteria. Pilot approach and portal requirements are agreed; no bench/field results or deployed portal are recorded.
- Reconfirmed the planned six-V4 pilot includes only two on-hand V4s, with two purchases and two recoveries pending. Hardware identification, firmware/configuration pinning, passive GPS freshness, runtime and outage checks remain next.
- Recommended starting with the owned-hardware passive-tracking bench baseline; the next software step remains a synthetic-data four-page portal mockup. MQTT connectivity investigation and wishlist items stay deferred. No new decision, ticket claim, implementation or hardware test.

Next useful step: identify the two on-hand V4 revisions/GPS wiring, two undamaged RAK cores and two V3 variants, then prepare a repeatable stock-firmware bench configuration and test procedure.

## 2026-10-12 — Project setup

- Captured the owner's mission, priorities, existing-hardware preference, intended member devices, solar/18650 repeaters, backhaul possibilities, dashboard, content, and grant-reporting goals.
- Initialized local Git on `main` and established the project brief, agent instructions, glossary, local Wayfinder tracker, and record templates.
- Proposed the first planning checkpoint: a measurable field pilot using owned hardware. This checkpoint is provisional pending owner input.
- Requested rough hardware models/counts and pilot member count/acceptable position age.
- Owner supplied an initial scale of roughly 20 trackers, starting with as few as 5, and a tentative GPS target of 5–15 minutes. Recorded these without treating them as verified performance or final acceptance criteria.
- Completed a [primary-source protocol comparison](../docs/research/protocol-baseline.md) on `research/protocol-baseline` for incorporation into `main`; resolved the research ticket. Existing Meshtastic timing settings warrant evaluation before a fork; MeshCore passive GPS behavior requires build-specific verification. Firmware selection remains open.
- Verified local Markdown links, Git whitespace checks, and ignore rules for local secrets/operational data. The local issue tracker is tracked. No firmware or hardware tests performed.

Next: confirm a usable subset of owned radio boards, GPS hardware, and 18650 cells, then agree pilot requirements. No current equipment quantities, verified expenses, field outcomes, or installation permissions have been invented.

## 2026-10-12 — Purchase-list import

- Owner added `Mesh Purchase List - Purchase List.csv` and reports retaining most, but potentially not all, listed items.
- Preserved the source CSV unchanged and imported all 32 rows with stable hardware IDs and source row numbers. Listed quantities are distinct from unknown current counts.
- Used the bundled Python CSV reader and exact decimal arithmetic to check source structure and costs. All rows have 22 fields; all 32 item rows were accounted for.
- Reconciled listed extended costs to $1,989.79; $129.00 is explicitly outside the mesh project, leaving a $1,860.79 listed mesh subtotal. These are not booked cash transactions or current stock valuations.
- Prioritized confirming radio/core variants, GPS hardware, and cells. Kept inventory and firmware-choice tickets open pending that evidence.

## 2026-10-12 — High-value inventory reconciliation shortlist

- Owner requested a reconciliation pass focused on higher-dollar hardware, excluding the full kit and consumables.
- Selected the six mesh purchase-list lines above $100 in listed extended cost: fiberglass antennas, RAK WisBlock assemblies, Heltec V4 boards, whip antennas, the devices labelled “Tdfeck,” and Heltec V3 boards. Costs are historical source references, not current valuations.
- Current counts and condition remain unconfirmed; no stock quantities were changed. The $129 camera card is separately outside the mesh project.

Next: owner confirms remaining counts and known condition for those six groups, then exact radio/core models and fitted GPS for the board/device groups.

## 2026-10-12 — Owner-confirmed higher-value inventory

- Recorded 10 fiberglass antennas, 7 RAK units on hand, 9 Heltec V3, 2 Heltec V4 with GPS modules, 11 Muzi whip antennas, and 2 brand-new LILYGO T-Decks with GPS modules.
- Recorded 2 additional RAK units deployed remotely at Mount Charleston, with recovery deferred until replacement nodes are ready. Possible member-held Heltec V4s remain uncounted pending confirmation/reclamation.
- Preserved historical source quantities. RAK has 9 units accounted for against 10 listed; V3 has 5 more on hand than listed; whip antennas have 5 fewer on hand than listed. V4 has 2 on hand against 6 listed, with member-held stock uncertain. Differences do not establish losses or new expenses.
- GPS modules are owner-confirmed on 4 on-hand devices. Exact hardware variants, GPS on V3/RAK, most condition details, and working passive tracking remain unverified. No purchase or spending was recorded.

Next: identify RAK core modules/radio variants and whether V3 units have GPS, then bench-check a five-device pilot subset. Confirm member-held V4s before deciding any additional quantity to order.

## 2026-10-12 — First-pass inventory closed

- Owner confirms all 9 V3 units lack GPS, with 6 × 1100mAh batteries available for them; 2 × 3000mAh batteries are for V4 units. Both T-Decks have included batteries, capacity unconfirmed.
- Recorded proposed V3 silent internet/backhaul and possible repeater roles without treating them as verified capabilities or a firmware choice. Recorded the owner's concern about larger V4 batteries for later runtime evaluation.
- Owner directed planning from confirmed current stock only. The unresolved RAK may be a third mountain repeater or destroyed; it remains uncertain and excluded, alongside deployed RAKs and unconfirmed member-held V4s.
- Resolved “Inventory owned hardware for the pilot” with first-pass counts, explicit unknowns, and follow-up inspections. Updated the map; did not close other decisions or record purchases.

Next: agree pilot duration and position-age criteria, then identify exact builds and bench-check GPS reporting/runtime. Current stock includes four GPS-equipped devices; a five-member GPS pilot needs one more GPS-equipped device or a revised initial size. No runtime, firmware compatibility, or field tests performed.

## 2026-10-12 — Additional RAK and 18650 count

- Owner found 1 more RAK with a broken carrier board requiring replacement: now 8 on hand (1 damaged) plus 2 deployed, numerically reconciling the source-listed 10. Damaged unit excluded from ready-to-use stock; the other 7 remain untested.
- Recorded 88 × 18650 cells on hand. Owner estimates perhaps 4 cells per mountain repeater, about 8 across the 2 reported deployments; these are separate estimates and excluded from available stock. Cell identity, condition, and capacity remain unverified.
- Updated inventory, deployment notes, and the resolved inventory ticket without reopening it. No replacement purchase or expense recorded. Left the newly added storage-box 3MF file untouched.

Next: identify the damaged carrier board and compatible replacement, inspect cell labels/condition, and continue pilot build/runtime planning. No hardware tests performed.

## 2026-10-12 — Pilot requirements interview started

- Claimed “Define useful tracking for the first field pilot” at the owner's request.
- Read project context, tracker, and current inventory/session decisions; preserved existing uncommitted inventory work and the storage-box file.
- Started clarification of pilot size and maximum dispatch position age, distinguishing position measurement time from receipt time and broadcast frequency.

Outstanding: owner agreement on pilot size and position-age target, followed by duration and device-only workflow. Ticket remains claimed while awaiting input. No hardware tests or firmware decisions made.

## 2026-10-12 — Pilot hardware and reporting direction

- Owner plans 2 Heltec V4 purchases and 2 V4 recoveries, all with GPS and 3000mAh batteries. Recorded these separately from current stock and actual cash transactions; potential pool is 6 V4s plus the 2 existing T-Decks if included.
- Clarified that the tentative 5–15-minute range concerns stale position age. Recorded aggressive reporting followed by congestion-based tuning, with power-based modes and movement thresholds as options to evaluate.
- Kept exact stale cutoff, runtime, device-only workflow, and trial participant count open. No prices, orders, recoveries, performance results, or firmware capabilities assumed.

Next: agree stale cutoff and unplugged runtime, then minimum phone-free member workflow and final trial count. “Define useful tracking for the first field pilot” remains claimed awaiting owner input.

## 2026-10-12 — Tracking MVP requirements agreed

- Owner agreed a 15-minute stale-position threshold, clear stale indication and visible age at dispatch, a 4-hour minimum battery runtime with a 12-hour target, and automatic tracking after power-on for the MVP.
- Recorded larger batteries as an option subject to runtime evaluation; no capacity, cost, or purchase recorded.
- Created “Define a future device-only SOS workflow” at the owner's request and deferred it beyond passive tracking. No SOS implementation or gesture selected.
- Updated the project brief and planned field criteria. No field/bench results recorded. Whitespace checks passed.

Next: confirm whether the first trial uses 6 planned V4s alone or includes 2 T-Decks, then close the shared requirements summary and proceed to firmware/network selection. “Define useful tracking for the first field pilot” remains claimed for that final confirmation. No commit requested or made.

## 2026-10-12 — First-pilot requirements closed

- Owner confirmed V4-only scope to avoid T-Deck device/firmware complexity: 6 planned GPS-equipped V4s with 3000mAh batteries, comprising 2 on hand, 2 planned purchases, and 2 planned recoveries. Current stock counts are unchanged.
- Resolved “Define useful tracking for the first field pilot” with the agreed stale-display, battery-runtime, reporting direction, and power-on workflow requirements plus explicit remaining unknowns. Added its decision link to the map and updated the project, inventory, and planned field criteria.
- “Choose the pilot network and firmware approach” is now unblocked. SOS remains a future open ticket. No other non-research decision resolved in this session.
- Git whitespace checks passed; no hardware/firmware, runtime, or field validation performed. Changes remain uncommitted; no commit requested.

Next: choose a V4-compatible firmware/network approach and identify the exact hardware builds, then define bench checks and reporting settings against these requirements.

## 2026-10-12 — Pilot infrastructure clarified

- Owner clarified that the pilot includes RAK repeaters and 2 Heltec V3 receive-only internet backhauls alongside the 6 planned V4 member trackers. T-Decks remain excluded; V4-only was member-device scope, not total network scope.
- Updated the resolved requirements answer, approach-ticket comments, project brief, map, inventory allocation, planned field criteria, and site notes. Preserved the existing claimed approach ticket and its research; no additional decision resolved.
- RAK quantity/builds and locations remain open. V3 radio silence while forwarding to internet is a requirement to verify, not a demonstrated firmware capability. No stock counts, expenses, or deployment permissions changed.
- Git whitespace checks passed. No hardware, RF, internet forwarding, or field tests performed; changes remain uncommitted.

Next: select the pilot RAK count/builds and verify the chosen firmware supports V4 tracking, RAK relaying, and radio-silent V3 backhaul, then specify ingestion and bench checks.

## 2026-10-12 — Pilot approach interview started

- Claimed “Choose the pilot network and firmware approach” at the owner's request to continue to the next issue; inventory, requirements, and protocol research prerequisites are resolved.
- Read project context and tracker, preserved existing uncommitted work, and started current official-source verification of V4 support and passive GPS behavior for the firmware choice.
- Firmware selection, dispatch ingestion, and bench configuration remain open. No hardware tests, purchases, deployment, or commit performed.

Next: owner chooses a firmware to evaluate first, then agree the minimal dispatch data path and assumptions to verify on the bench. Ticket remains claimed while awaiting those decisions.

## 2026-10-12 — Meshtastic evaluation accepted; requirements refreshed

- Owner accepted Meshtastic as the first evaluation path and expects firmware modifications will likely be needed; stock sufficiency remains unproven.
- Reread the updated “Define useful tracking for the first field pilot”: 6 V4 member trackers plus owned RAK repeaters and 2 strictly receive-only V3 internet backhauls.
- Started checking V3 transmit-disable and uplink behavior against primary sources. The approach ticket remains claimed; no decision closed, hardware tested, or commit made.

Next: clarify anticipated modifications and local dispatch needs during internet outages, then choose a minimal ingestion path and RAK subset with explicit bench verification gates.

## 2026-10-12 — GPS fork review and offline viewing requirements

- Owner identified GPS behavior as the expected firmware-modification area and requested inspection of commits ahead in `lfg-seth/firmware`; started a primary-source commit/diff review.
- Owner confirmed local field command-post viewing and other-member location viewing in companion apps without internet backhaul. Updated the resolved requirements answer, project brief, map, approach discussion, and planned field criteria. Passive tracking remains phone-free.
- Source review supports evaluating V3 LoRa TX disable alongside MQTT uplink; exact build behavior and radio silence still require bench evidence. RAK cores remain unidentified.

Outstanding: finish the fork review, identify GPS changes worth evaluating against current upstream, and select local/remote ingestion arrangements plus a RAK subset. No firmware flashed, hardware tested, expenses changed, or commit made.

### Fork review completed

- Saved the [old firmware fork audit](../docs/research/old-firmware-fork.md), covering all 17 ahead commits (2 merges), net surviving changes, and a targeted comparison against pinned current upstream; fork is 1,887 behind.
- Found GPS timing preferences rather than a new GPS/position algorithm, a 30-minute periodic broadcast requiring revision for stationary freshness, and a source-level coordinate-shift defect in the full-precision MQTT map override. Do not transplant the old fork unchanged.
- Recorded offline app/map considerations and LoRa-silent gateway checks in the approach ticket. Public-history secret values were omitted from the report; do not reuse them for the private pilot.
- Git whitespace checks passed. No firmware builds, hardware/field tests, deployment, or commit performed.

Next: choose the command-post viewing device/connection and RAK subset, then define the current-release bench configuration and concrete GPS behavior gaps. “Choose the pilot network and firmware approach” remains claimed; no additional decision resolved.

## 2026-10-12 — Local viewer and RAK subset selected

- Owner selected both app and laptop/portal viewing, with the Meshtastic app acceptable for the first local-viewing MVP. Recorded 1 owned rugged Dell laptop/tablet running Linux as field equipment (HW-033); model/compatibility and runtime are unknown.
- Owner accepted 2 undamaged on-hand RAKs for initial relay evaluation, subject to core identification and operation checks; individual units remain unassigned. No radio stock counts changed.
- Prepared an approach summary in the claimed firmware/network ticket, including proposed private MQTT position-packet ingestion, local app viewing, and explicit bench prerequisites. Remote ingestion choice/final shared understanding remain pending; no decision resolved.
- Whitespace verification passed; no firmware builds, hardware tests, spending, installation, or commit performed.

Next: agree the approach summary/private MQTT path, then identify exact builds and prepare bench configuration and tests. Changes remain uncommitted; no commit requested.

## 2026-10-12 — Pilot network/firmware approach closed

- Owner accepted one private MQTT broker for both receive-only V3 uplinks and proposed compatible companion-app/cellular member uplinks only if multiple-backhaul behavior is acceptable.
- Completed [multiple-backhaul research](../docs/research/multiple-backhauls.md): documented phone proxy support, duplicate handling, downlink isolation, outage limits, and app/version caveats. No maximum gateway count or capacity result invented.
- Resolved “Choose the pilot network and firmware approach” with the agreed Meshtastic evaluation, hardware subset, local app-first/laptop viewing, private position-packet ingestion, and conditional staged member-phone backhauls. Added its decision link to the map and updated project/backhaul/test records. Only this non-research decision was resolved in this session.
- Exact builds, GPS settings, ingestion implementation, and hardware/field success remain open. Whitespace checks passed; no firmware build/flash, broker deployment, hardware tests, purchases, or commit performed.

Next useful step: identify the V4 revisions/GPS wiring, 2 RAK cores, and 2 V3 variants, then pin a current firmware release and prepare the bench configuration/test procedure. Keep SOS deferred until passive tracking is established. Changes remain uncommitted; no commit requested.

## 2026-10-12 — Future SOS requirements interview started

- Claimed “Define a future device-only SOS workflow” as the next open, unblocked tracker issue at the owner's request.
- Started a requirements-only interview with intended recipients and dispatch response ownership. SOS implementation remains deferred beyond passive tracking.
- Preserved existing uncommitted work. No decision resolved, firmware changed, hardware tested, or commit made.

Outstanding: agree recipients and response ownership, then activation, accidental-trigger handling, cancellation, acknowledgment, and outage behavior. Passive-tracking hardware identification and bench preparation remain the next implementation step.

## 2026-10-12 — Future SOS alerts and friendly areas

- Owner chose both dispatch and nearby-member SOS recipients, requested a Heltec OLED popup/flashing alert, and suggested an optional fitted buzzer. Recorded the hardware idea without assuming parts, compatibility, or spending.
- Recorded desired SOS content: member identity, friendly area name, and latitude/longitude. Owner proposes defining named Mount Charleston AO polygons in Google Earth; no boundaries supplied or inferred.
- Verified Google primary documentation for KML/KMZ export and named polygon geometry. Proposed an offline area lookup for discussion; device firmware/memory feasibility and boundary, overlap, unmatched, and stale/missing-GPS rules remain open.
- No SOS decision resolved, hardware/code changed, tests performed, or commit made. Whitespace verification passed.

Next: agree activation, then alert/cancellation/acknowledgment and response/outage behavior. “Define a future device-only SOS workflow” remains claimed; passive tracking remains the implementation priority.

## 2026-10-12 — Existing V4 button preferred for SOS

- Owner prefers a 5-second hold of the existing Heltec V4 button to activate SOS, replacing long-hold shutdown; no dedicated SOS button selected.
- Checked upstream user-button mapping and hold-event code. Shutdown conflicts warrant a firmware remap investigation; the owned board/button and installed-build behavior remain unverified.
- Proposed visible countdown, early-release abort, and one activation at the threshold for owner agreement. Cancellation and a replacement shutdown workflow remain open alongside acknowledgment/outage/area-lookup details.
- No decision resolved, code/firmware changed, hardware tested, or commit made. Whitespace verification passed.

Next: agree countdown/trigger behavior and how to cancel a sent SOS. Passive tracking remains the implementation priority; the SOS ticket remains claimed.

## 2026-10-12 — Active SOS interaction and GPS requirements

- Owner agreed the 5-second countdown/early-release activation and chose a separate subsequent 5-second hold to cancel/send cancellation. Recorded the need for release between holds and superseded the proposed menu cancellation.
- Recorded an obvious flashing/active SOS indication while incoming messages remain viewable, a new location attempt, a warning when no current fix is available, and last-known coordinates with their original age.
- Owner requested immediate new SOS transmissions when a location becomes available during SOS. Proposed grouping transmissions into one incident with ordered updates; every-fix versus recovery-only scope and no-new-fix repetitions remain for agreement.
- Proposed an explicit location-unavailable SOS when no fix has ever existed. No coordinates, timing guarantees, firmware support, or measured results assumed.
- No decision resolved, firmware/hardware changed, tests performed, or commit made. Whitespace verification passed.

Next: clarify SOS location-update scope and repetition, then acknowledgment/response, cancellation/outages, and remaining area/display rules. The SOS ticket remains claimed; implementation remains after passive tracking.

## 2026-10-12 — SOS text and position traffic separated

- Owner assumes a specially formatted Meshtastic text SOS and rejected an SOS message for every new GPS fix. Recorded faster ordinary position broadcasts during active SOS; exact rate and first-recovered-fix text behavior remain open.
- Recorded the need for retransmission without flooding even when recipients cannot acknowledge. OLED-only rescue followed by cancellation on the originating device is an intended workflow.
- Checked official Meshtastic acknowledgment/retransmission documentation and distinguished transport evidence from human response. Proposed spaced, bounded reminders that slow down independently of human acknowledgment, with optional human acknowledgment stopping text reminders but not active tracking; not yet agreed.
- No final retry policy, packet format, code change, hardware result, or decision resolution established. Whitespace verification passed; no commit made.

Next: agree reminder/acknowledgment behavior, then remaining receiver/cancellation/GPS/area rules. Passive tracking remains the implementation priority.

## 2026-10-12 — SOS acknowledgment deferred

- Owner removed human acknowledgment from the first SOS design and left cancellation to the originating member's separate 5-second hold.
- Superseded the proposal that human acknowledgment stops reminders. Active indication, faster ordinary tracking, and bounded text reminders continue until originating-device cancellation; numerical rates remain unselected.
- Preserved OLED-only response without acknowledgment. Underlying transport acknowledgment is not a condition for clearing SOS; recipient cancellation delivery is still unverified.
- No ticket resolved, firmware/hardware changed, tests performed, or commit made. Whitespace verification passed.

Next: agree behavior when no position has ever been acquired and after an unexpected reboot, then finish remaining requirements/prerequisites. “Define a future device-only SOS workflow” remains claimed; passive tracking remains the implementation priority.

## 2026-10-12 — SOS persistence and power-aware cadence

- Owner agreed SOS sends without any known position and active SOS survives an unexpected reboot until originating-member cancellation.
- Added requested battery status on the SOS screen and power-source-aware effort: maximum configured effort on external power even with low battery, taper on low battery only when battery-powered. Exact thresholds/rates remain open.
- Saved a primary-source [V4 power-detection check](../docs/research/v4-power-detection.md). Battery sensing is supported; reliable external-power detection for a low-battery V4 on a charger/power bank remains unverified and needs exact-board/build investigation plus bench tests.
- No ticket resolved, hardware/firmware changed, spending recorded, or hardware tests performed. Whitespace verification passed; no commit made.

Next: establish external-power detection and unknown-source behavior, then summarize the SOS requirements and remaining implementation prerequisites. Passive tracking remains the implementation priority.

## 2026-10-12 — Power detection pinned for follow-up

- Owner deferred the power-source investigation and proposed sustained battery-level trend over a configurable window, perhaps 1 minute, as an inferred-charging heuristic.
- Recorded the idea in the SOS ticket and power-detection research note without selecting an algorithm or treating trend as proof of external power. Unknown/flat behavior and exact cadence policy remain open.
- No tests, firmware/hardware changes, spending, ticket resolution, or commit. Whitespace verification passed.

Next: resume the remaining SOS workflow requirements and shared summary; keep power detection as a deferred implementation prerequisite. Passive tracking remains the implementation priority.

## 2026-10-12 — Future SOS workflow closed

- Owner accepted receiver short-press silencing with the incident retained, immediate local cancellation with bounded cancellation-delivery attempts through outages, and dispatch coordination when reachable with direct nearby-member response otherwise.
- Resolved “Define a future device-only SOS workflow” with a consolidated owner-agreed answer and linked it from the map. Recorded activation/cancellation, formatted text/ordinary position traffic, GPS age/unavailable fallback, OLED/battery status, reboot persistence, no human acknowledgment, and bounded reminders.
- Kept power detection/battery-trend evaluation pinned and message/rate/area/shutdown/firmware details as explicit implementation prerequisites. SOS implementation remains after passive tracking. Only this non-research decision resolved in this session.
- Whitespace verification passed. No firmware/hardware tests, purchases, deployment, or commit made; existing unrelated edits preserved.

Next useful step: identify the V4 revisions/GPS wiring, 2 undamaged RAK cores, and 2 V3 variants, then pin firmware and prepare the passive-tracking bench procedure. No open tickets remain in the current pilot tracker; create a focused bench-preparation follow-up when continuing implementation planning.

## 2026-10-12 — Charging display option captured

- Added the owner's configurable “keep display always on while charging” idea beside the battery-charge heuristic in the [power-detection note](../docs/research/v4-power-detection.md).
- No default, algorithm, or firmware change selected. The resolved SOS workflow remains closed; power detection stays deferred.
- Whitespace verification passed; no hardware tests or commit made.

Next useful step remains pilot hardware identification and passive-tracking bench preparation.

## 2026-10-12 — Dispatch portal interview started

- Owner redirected planning to a responsive Map/Users/Messages portal, MQTT-equipped V3s and possible V4s, an available Proxmox VM, Cloudflare Tunnel, simple locally managed accounts, and topo/aerial maps. Captured the proposal in the claimed [Define the dispatch portal MVP](../.scratch/pilot/issues/06-dispatch-portal.md) without choosing a stack or provisioning services.
- Recorded current-pin defaults, 15-minute stale display with measurement age, optional history showing measured points and uncertain connecting lines, all-incoming-data storage, shared-channel messages, and the proposed single dispatch transmit gateway. The prior receive-only approach remains recorded; the gateway change awaits agreement.
- Completed and resolved two primary-source research investigations: [broker/portal transport and backend options](../docs/research/dispatch-portal-transport.md), and [map sources/nonprofit access](../docs/research/dispatch-portal-maps.md). Cloudflare portal HTTPS is distinct from stock-device MQTT reachability; PocketBase is a pilot candidate with production-critical caveats and still needs ingestion. MapLibre plus USGS topo/aerial is a shortlist; coverage/age/zoom and offline use need verification. Preserved existing unrelated edits and hardware records; no purchase, publication, hardware test, service deployment, or commit performed.
- Asked the first independent design round: internet-outage workflow, account permissions, dispatch transmit gateway, retention, and dated device/member assignments. No non-research decision resolved.
- Git whitespace verification passed. Research is source-based, with moving firmware documentation/code; no selected release or hardware/backend/browser behavior tested.

Next useful step: owner answers the first round, then refine the map/user/message behavior and broker access path against the research findings. Hardware identification and passive-tracking bench preparation remain outstanding.

### First portal round answered

- Owner selected local Meshtastic fallback for v1, full operational access for registered users, one designated V3 transmitting portal replies, and retention of all pilot data with review before wider rollout.
- Owner proposed numeric device labels and portal member assignment by dispatch/admin or signed-in self-claim. Added device-number/assignment terminology; conflict/transfer/time-history rules remain under discussion.
- Amended current project, inventory allocation, planned field checks, sites, and the earlier approach answer to make the one-V3 transmit exception explicit. This does not select a hardware unit or establish transmission/forwarding success.
- Sent the next design round: assignment collisions; freshness bands; history window and gaps; sending during gateway outages; admin versus operational permissions. The portal ticket remains claimed pending these answers and eventual shared-summary agreement.

Next useful step: finish the portal behavior interview, then choose the broker connection/backend path and map evaluation prerequisites. No services deployed, hardware tests, spending, or commit.

### Second portal round answered

- Owner agreed unassigned-only self-claim with dispatch/admin transfers, preserved dated history, measurement-age breathing bands (under 2, 2–5, 5–15 minutes; stale at 15), separate last contact/unknown GPS, and no invented positions.
- Owner selected 4-hour initial history, measured points with dashed estimated connections and breaks over 15-minute gaps; manual send after outages with an unsent draft; and admin-only account/archive management with full operational access for registered users.
- Third round covers member/device list and unassigned pins, alert scope, shared-gateway author attribution, broker reachability, and pilot backend/map evaluation. Portal ticket remains claimed; no non-research ticket resolved or implementation performed.

Next useful step: answer that round and review a consolidated portal specification with any explicitly deferred infrastructure questions.

## 2026-10-12 — Portal list, alerts, author and evaluation stack agreed

- Owner selected the member/unassigned-device list and default tracker map, one-to-one active assignments, in-portal message toast/unread badges with optional sound, and author-name prefixes for outbound radio text.
- Owner approved a PocketBase/MQTT-worker/MapLibre/USGS pilot evaluation. No backend deployed or operational performance established.
- Owner requested clarification of why a broker VM's Cloudflare Tunnel hostname cannot directly serve stock Heltec MQTT. Rechecked official Cloudflare protocol documentation and current Meshtastic MQTT source; raw MQTT TCP/TLS is distinct from the Tunnel's WebSocket-wrapped TCP path requiring a client-side adapter. Domain use remains possible with a separately reachable broker.
- Portal ticket stays claimed pending the broker clarification and consolidated requirements review. Existing edits preserved; no purchase, publication, deployment, hardware test, or commit.
- Explained the hostname/Tunnel distinction using `mqtt.spp.lol`; documented DNS-only direct MQTT TLS and a WebSocket firmware/bridge candidate. Asked a simpler network question about VM location and router port forwarding. No actual domain, port, or firmware change performed. Git whitespace verification passed.

Next useful step: explain the `mqtt.spp.lol` example, identify a feasible broker connection path or explicitly defer it, and confirm the portal requirements summary.

## 2026-10-12 — No inbound forwarding; portal summary drafted

- Owner confirms the Proxmox VM is local and wants no inbound router port forwarding. Recorded this in the project/site notes and portal ticket; excluded the direct home-broker port-forward proposal.
- Started [Check Heltec MQTT over WebSockets for Tunnel hosting](../.scratch/pilot/issues/09-heltec-websocket-research.md). Compare a home WebSocket firmware/bridge route with a separate reachable private broker using outbound home connections; no route/provider/cost or firmware modification selected.
- Drafted a consolidated requirements summary in [Define the dispatch portal MVP](../.scratch/pilot/issues/06-dispatch-portal.md) for owner review. Asked whether home broker hosting is preferred or a separate broker is acceptable. The portal ticket stays claimed; no non-research decision resolved.
- No deployment, publishing, purchase, hardware tests, or commit. Preserve existing unrelated edits and raw-data ignore policy.

Next useful step: review the narrow transport findings, establish the hosting preference, and confirm the consolidated portal requirements with explicit implementation prerequisites.

### Connectivity investigation deferred by owner

- Owner explicitly stopped further connectivity investigation for now and asked us to assume a local MQTT broker reachable through Cloudflare with stock clients. Recorded that as an unverified planning assumption, without revising primary-source evidence or asserting operational support.
- Interrupted the research agent and released the WebSocket ticket claim. Do not resume connectivity investigation until requested. Updated the project, sites, map notes, and draft requirements accordingly.
- Portal requirements are ready for consolidated owner review. No service deployment, firmware change, field test, spending, or commit; unrelated edits preserved.

Next useful step: confirm the portal summary, then evaluate its map/user/message interface. Networking remains parked for the owner's later investigation.

## 2026-10-12 — Infrastructure monitoring added; portal baseline resolved

- Owner added repeaters/backhaul visibility by role, recorded battery charge/discharge, solar measurements, weather where equipped and intrusion detection where equipped.
- Owner selected a fourth Infrastructure page with device cards/details, telemetry charts and event log, optional infrastructure map layer, and configurable low-battery/missing-telemetry warnings and intrusion alerts.
- Resolved [Define the dispatch portal MVP](../.scratch/pilot/issues/06-dispatch-portal.md) with the consolidated interview answers and accepted addition; linked the answer from the map. Only this non-research decision resolved in this session. MQTT connectivity stays deferred under the owner's explicit planning assumption.
- Added infrastructure terminology, project direction and planned verification. Meshtastic docs establish capability categories, not sensor fitment, measured charging/solar behavior or alert reliability on owned builds. No stock counts or purchases changed.
- Created [Define infrastructure warning and intrusion handling](../.scratch/pilot/issues/10-infrastructure-warning-rules.md) for exact thresholds, permissions, acknowledgment/clearing and repeat behavior. This is separate from UI baseline selection and remains unclaimed.

Next useful step: choose infrastructure warning/event behavior or evaluate a map/infrastructure interface mockup. No firmware/UI implementation, deployment, hardware/sensor tests, spending or commit; existing unrelated edits preserved.

## 2026-10-12 — Device identity and remote naming interview

- Owner asks whether device selection/assignment can trigger OTA long/short-name changes, and whether a persistent device-specific identifier avoids using short names as unique database IDs.
- Completed/resolved [Check persistent device identity and remote name updates](../.scratch/pilot/issues/11-device-identity-research.md) with a [primary-source report](../docs/research/device-identity-admin.md), and claimed [Choose assignment-driven radio names and identity](../.scratch/pilot/issues/12-assignment-radio-names.md) for the owner policy.
- Current schema/source exposes a local hardware `device_id` on ESP32-S3, distinct from the mesh node number and editable names; actual boards/releases need provisioning checks. Remote admin requires authorized keys and a command-capable gateway integration; do not equate it with MQTT text downlink.
- Proposed stable short name S004 and carrier long name Seth [004] on assignment, with portal assignment independent of pending/confirmed/failed OTA naming. Owner choice is pending; no naming policy added to the resolved portal baseline yet.
- MQTT/Cloudflare connectivity stays parked under the owner's assumption. No actual name/admin key changes, device provisioning, flashing, implementation, hardware tests or commit.
- Verified source-level caveat: MQTT JSON text cannot rename and decoded admin payloads are rejected; encrypted PKI transport has a conditional path, so do not claim all MQTT admin is impossible. Recommend a trusted local radio API agent for the supported SDK route; portal execution/read-back remains to test. Git whitespace verification passed.

Next useful step: finish the capability check and owner naming choice, then record the assignment-name behavior and admin integration prerequisite.

## 2026-10-12 — Static device short names agreed

- Owner confirmed tracker short names remain static to device numbers. Resolved [Choose assignment-driven radio names and identity](../.scratch/pilot/issues/12-assignment-radio-names.md), linked it from the map, and amended the portal baseline/project/glossary.
- Recorded the separation of stable device identity, dated assignments and radio-name updates. Short names do not serve as database identity; long-name carrier updates are separate jobs with pending/confirmed/failed state and read-back. Exact formatting/release wording and the admin execution path remain implementation details to settle/verify.
- Only this non-research decision resolved in this session. Existing edits preserved; no actual names/admin keys changed, devices provisioned, UI/firmware implemented, hardware tested or deployment performed. MQTT connectivity stays parked.

Next useful step: define infrastructure warning/event behavior or review a map/infrastructure interface mockup. No commit requested or made.

## 2026-10-12 — Future feature wishlist captured

- Recorded the owner's [deferred feature wishlist](wishlist.md): a known-Wi-Fi table with automatic connection and MQTT-backhaul attempts, and browser-based flashing of project firmware for a small preselected subset of member-owned devices.
- Linked the wishlist from the project brief and pilot map, outside the active ticket frontier. Both ideas remain parked until the owner explicitly brings them forward; no research, design, implementation, or testing started.
- Supported devices, connection behavior and provisioning details remain future questions. Existing MQTT connectivity deferral and passive-tracking priority are preserved. Existing unrelated edits remain intact; no commit requested or made.

Next useful step: continue current pilot/portal planning when requested. Revisit these wishlist items only at the owner's direction.

## 2026-10-12 — Wishlist convention made persistent

- Owner clarified that future requests to “wishlist” an idea or feature refer to the deferred list in `records/wishlist.md`.
- Added the standing routing instruction to `AGENTS.md`: capture the idea outside the active ticket frontier and wait for explicit owner direction before starting work on it.

Next useful step: apply this convention to future wishlist requests. No feature work or commit performed.

## 2026-10-12 — Slack integration wishlisted

- Added Slack integration to the [deferred wishlist](wishlist.md), noting the owner's report that SNORR uses Slack heavily and possible dedicated-channel or app/plugin forms.
- Left use cases and integration mechanism open. No research, active ticket, Slack connection, channel creation, or implementation started; no commit made.

Next useful step: continue current project work when requested; revisit Slack integration only when the owner explicitly brings it forward.

## 2026-10-12 — Wishlist relevance clarified

- Owner clarified that deferred ideas should still be mentioned when relevant to future conversations. Updated `AGENTS.md` and the wishlist introduction to retain that context while keeping work deferred until explicit owner direction.
- Mentioning a wishlist item does not activate it. No feature work or commit performed.

Next useful step: consult the wishlist during related discussions and surface useful connections without starting deferred work.

## 2026-10-12 — Infrastructure warning interview started

- Owner requested work on infrastructure warnings and intrusion handling. Claimed [Define infrastructure warning and intrusion handling](../.scratch/pilot/issues/10-infrastructure-warning-rules.md).
- Started the policy interview covering permissions, notification scope, intrusion clearing and threshold configuration. Existing portal baseline and connectivity deferral remain in force.

Next useful step: collect owner answers, settle dependent repeat/outage/recovery behavior, and confirm the consolidated rules. No implementation, hardware tests, deployment or commit performed.

### First infrastructure round answered

- Owner accepted admin-only rule configuration, acknowledgment by all registered users, audited actions, and admin resolution of latched intrusion incidents with a note.
- Accepted persistent portal badges/cards and toasts, explicitly with no sound. Accepted shared defaults/per-device overrides and emphasized uneven sensor fitment; sensor rules apply only where configured/supported.

Next useful step: settle repeats, recovery, feed outages and missing-report timing, then confirm the consolidated decision. Ticket remains claimed; no implementation or tests performed.

### Second infrastructure round answered

- Owner selected persistent infrastructure badges only and logging of all events, superseding infrastructure toasts; no sound or repeat notifications.
- Accepted automatic health-warning recovery on fresh evidence, separate battery recovery thresholds, feed-outage visibility and preservation of existing alerts, and configurable missing-report timeouts starting at three expected reporting intervals.
- Consolidated policy awaits owner confirmation, including explicit proposals for reconnect grace and intrusion-event grouping. Battery values and sensor/cadence verification remain implementation prerequisites.

Next useful step: confirm the summary and resolve the infrastructure policy ticket. No implementation, hardware tests, deployment or commit performed.

## 2026-10-12 — Infrastructure warning policy resolved

- Owner confirmed the consolidated [infrastructure warning and intrusion policy](../.scratch/pilot/issues/10-infrastructure-warning-rules.md), including reconnect grace and intrusion-event grouping. Resolved this one non-research decision and linked it from the map and portal baseline.
- Added owner-requested device battery configuration metadata: type/chemistry, cell count and nominal mAh capacity with explicit per-cell/pack scope and arrangement where applicable. Unknowns remain explicit; no installed battery types, stock counts, measured capacity or runtime inferred.
- Updated project direction and planned verification. Silent badges replace infrastructure toasts; shared-message notification policy remains separate. Exact battery thresholds, sensor fitment/units and reporting cadence require verification. MQTT connectivity remains deferred; wishlist items remain parked.

Next useful step: review a portal interface mockup or identify and bench-check the owned pilot builds for passive tracking. No implementation, hardware/sensor tests, deployment, spending or commit performed; existing unrelated edits preserved.

## 2026-10-12 — Solar and antenna configuration added

- Owner added solar-panel configuration to device setup, explicitly leaving options for later definition.
- Added antenna configuration including Muzi whip and fiberglass choices, with unknown/unconfigured values explicit. Recorded both additions in the portal baseline and project brief; no installed hardware assignments, inventory counts, purchases or performance claims changed.

Next useful step: review the portal interface or bench-check owned pilot hardware. Solar configuration options remain open. No implementation, tests, deployment or commit performed.

## 2026-10-12 — Next-step review

- Reviewed project decisions, session history and tracker state. Portal requirements, naming and infrastructure warning policy are resolved; the remaining open connectivity research is explicitly deferred.
- Recommended identifying the owned pilot hardware and preparing a small passive-tracking bench test as the next step toward the primary GPS mission. A portal interface mockup remains the next software planning option.

Next useful step: identify the 2 on-hand V4 revisions/GPS wiring, 2 undamaged RAK cores and 2 V3 variants, then prepare firmware/configuration and a bench procedure. No new ticket claimed, implementation, hardware test or commit performed; existing edits preserved.

## 2026-10-12 — Portal development handoff for the night

- Owner requested a brief portal-development next-step review, then stopping for the night. Reviewed the resolved portal baseline; no additional requirements interview or implementation started.
- Recommended a local four-page mockup with synthetic data, emphasizing the tracking map, position age, stale/unknown states and feed outages. Next define the records and worker interface for device identity, dated assignments, observations, packet receipts, messages and infrastructure events, then implement a simulated ingestion-to-map slice before live hardware integration.
- Real integration still needs sanitized packet samples/pinned firmware, verified telemetry capabilities and units, message limits/delivery evidence, and VM/backup setup. MQTT connectivity research remains explicitly parked; it need not block a simulated local prototype.

Next useful portal step: build a local Map/Users/Messages/Infrastructure mockup using synthetic data, then review it before wiring the backend. No new ticket, deployment, publishing, hardware test or commit; existing edits preserved. Session ended at the owner's request.

### Portal stack recommendation

- Owner favors Python for the MQTT worker and is most familiar with React. Recommended React + TypeScript + Vite for the browser portal, retaining PocketBase and MapLibre. React's current official documentation includes a Vite-based setup; frontend choice remains a recommendation pending owner acceptance.
- Python worker preference recorded; no worker library, dependency versions or broker software selected. No implementation or deployment started.

Next useful step: confirm the frontend direction when resuming, then build the local synthetic-data mockup. No commit made.

### Hosting comparison

- Compared current official Vercel Hobby/function limits and PocketBase deployment guidance. Recommended retaining the owned Proxmox VM for the pilot: static React build, persistent PocketBase data, Python MQTT worker and private broker together.
- Vercel is a possible frontend-only host, but that split retains the VM/backend dependency and adds hosting configuration. Hobby functions are duration-limited and do not fit the intended continuous MQTT worker; plan eligibility remains to check if Vercel is considered.
- Home power/internet availability, service restarts and backups remain deployment checks. No hosting decision changed, service deployed or connectivity research resumed; no commit made.

### Portal bandwidth and client performance

- Owner reports a 100Mbps home uplink. Expected pilot bandwidth is manageable if browsers fetch USGS basemap tiles directly and receive small incremental operational updates; this is an architectural estimate, not a measured load test.
- Verified official Cloudflare caching guidance, USGS cached basemap services and MapLibre performance guidance. Recommend caching public versioned frontend assets, leaving authenticated operational responses uncached, and keeping map tiles off the home-origin path.
- Client checks should cover slow cellular connections, tile-provider latency, GPU/WebGL support on the rugged Dell and mobile devices, marker animation, bounded history queries and reconnect behavior. Concurrent viewers, actual payload sizes, VM resources and observed latency remain unmeasured.
- No deployment/configuration change, hosting decision or connectivity investigation performed. Next prototype should measure cold/repeat loading and live updates on actual field devices; no commit made.

## 2026-10-12 — Pre-bench firmware readiness review

- Owner asked whether firmware changes are needed before bench testing. Reviewed the agreed pilot approach, old-fork audit, future SOS requirements and deferred power/wishlist work. Recommend a stock Meshtastic baseline with deliberate configuration; no mandatory source patch identified for the initial passive-tracking tests. Stock sufficiency remains unproven until hardware tests.
- Rechecked official [position configuration](https://meshtastic.org/docs/configuration/radio/position/): acquisition cadence, periodic broadcasts, movement thresholds, configurable GPS pins and GPS-solution timestamp flags exist. Proposed an initial diagnostic profile of 60-second acquisition, 120-second periodic broadcasts and smart broadcasting off to isolate stationary reporting; these are unapproved/unmeasured trial suggestions, not operational settings or a freshness guarantee. Verify saved settings after reboot and measure actual fresh-fix transmissions.
- Official [Heltec support](https://meshtastic.org/docs/hardware/devices/heltec-automation/lora32/) distinguishes original V4 from V4-R8 firmware targets. Identify owned revisions/GPS wiring and RAK cores before pinning a release and matching per-board images. Do not reuse the old fork's 30-minute member broadcast preference.
- Existing [LoRa transmit disable](https://meshtastic.org/docs/configuration/radio/lora/#transmit-enabled) and [MQTT configuration](https://meshtastic.org/docs/configuration/module/mqtt/) warrant configuration-first gateway tests. Preserve the later amendment: one V3 may transmit portal replies; the other remains receive-only. Test continued uplink and silence through reboot/reconnect on the pinned build. No broker-connectivity investigation resumed.
- Portal measurement-age/stale display, assignments, deduplication and warnings are application/integration work. The agreed custom SOS button/countdown, incident persistence/cancellation, reminders, OLED handling and area lookup need later firmware implementation/evaluation; deferred charging heuristics and wishlist items remain parked.

Next useful step: identify boards and GPS connections, pin supported stock images, save a bench configuration, then test phone-free boot, stationary/moving GPS freshness, reboot persistence, relay/backhaul behavior and battery runtime. No firmware changed/flashed, hardware tests, ticket status changes or commit performed; prior unrelated edits preserved.

## 2026-10-12 — Project naming suggestions

- Owner requested a short umbrella name connecting SNORR, mesh networking and communications, understandable at a county meeting and suitable for a GitHub repository.
- Recommended SNORR Link, with the descriptor "Search and Rescue Tracking & Communications" and suggested repository name `snorr-link`. Alternatives: SNORR MeshLink, SNORR Connect and SNORR RescueNet. These are suggestions awaiting owner selection; the existing project/repository name remains in place.

Next useful step: owner selects a name. No repository rename, availability check, publishing or commit performed; existing edits preserved.

## 2026-10-12 — SNORR MeshLink GitHub publication

- Owner created `lfg-seth/snorr-meshlink`, supplied its SSH URL, authorized pushing the project there and requested a push after every commit. Adopted SNORR MeshLink in the project overview and saved the publication/push policy in AGENTS.md.
- Confirmed the remote is empty and SSH access works using Windows OpenSSH. Prepared the accumulated inventory, pilot decisions, portal/SOS requirements, research, wishlist and session records for a coherent publication checkpoint. The local Markdown tracker is mirrored with the repository; no GitHub Issues migration requested.
- Refreshed the README's outdated pilot summary. Kept the unrelated untracked battery-box 3MF model outside the commit. No hardware tests, implementation or operational deployment performed.

Next useful step: identify pilot boards/GPS wiring and prepare passive-tracking bench tests, or resume the synthetic-data portal mockup. Push each completed commit to origin and report failures; keep private operational data outside Git.

### Broker renewal diagnosis follow-up

- Owner asked whether closed inbound 443 explains renewal failure. Official [Certbot standalone documentation](https://eff-certbot.readthedocs.io/en/stable/using.html#standalone) confirms the configured standalone HTTP-01 method requires public inbound TCP 80; inbound 443 is not required for that method. Outbound HTTPS to the ACME service is separately required. Closed 80 is a possible cause, not confirmed without logs.
- Requested root-visible Certbot journal and the latest Let's Encrypt log error block. Renewal cause remains pending; no firewall change or renewal attempted. After renewal, separately verify deployment of the renewed certificate into Mosquitto's configured certificate files and reload behavior.

### HTTP-01 failure located

- Owner supplied root-visible Certbot failure evidence. Active HTTP-01 challenge request received 404 on public port 80; outbound ACME HTTPS succeeded. Read-only follow-up HTTP probe returned an nginx 404. A routing/proxy/challenge-serving mismatch is suspected; the precise destination remains to inspect. Closed inbound 443 is not the cause of this configured HTTP-01 failure.
- Recorded sanitized evidence in the transport report. Next inspect public port-80 forwarding/nginx routing, correct the selected challenge path and run a renewal dry-run before production renewal and broker certificate deployment. No remote changes or commit performed.

### Heltec port explanation

- Owner asked whether Heltecs specify a port and what 1883/8883 do. Verified current Meshtastic source parses `hostname:port`, choosing default 8883 with TLS and 1883 otherwise. Documented gateway settings `mqtt.spp.lol:8883` with TLS enabled and private proxy-to-broker 1883 role. Actual firmware remains unpinned/unverified; member LoRa trackers do not all need MQTT.
- Captured source-level credential-logging/certificate-verification checks for later provisioning without reading or publishing actual credentials. No device/server changes or commit performed. Next step remains adapting the fresh broker for Mike's TLS-termination layout and verifying actual endpoints/builds.
