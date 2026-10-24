# Define an owned-hardware field pilot

**Permanent local tracking - accepted 2026-10-23:** The [local tracker](../TRACKER.md) owns current task status on `main` under the [local workflow](../../docs/operations/local-tracking.md). This map preserves decision history; historical open/claimed fields are not the current queue. GitHub imports remain reference evidence, with no routine board synchronization.

Formerly open questions: [private monitoring scope](https://github.com/lfg-seth/snorr-meshlink/issues/10), [held repeater survey](https://github.com/lfg-seth/snorr-meshlink/issues/11), and [deferred WebSockets alternative](https://github.com/lfg-seth/snorr-meshlink/issues/12). Their original questions remain below and in the linked decision files.

2026-10-16 R004 follow-up — Owner-authorized fourth RAK preparation completes on released `2.7.26.0b65f2e`, preserving device keys and verifying pilot/sensor/neighbor configuration through reboot. Live R004 registration shares R001's private planned site. Fresh G001 battery/weather ingestion and archived SNNS reception pass; INA219 interpretation, normalized current/neighbor decoding and fresh G002 delivery remain limited. [Evidence](../../docs/operations/r004-preparation.md). No tracker decision or field installation is implied.

2026-10-14 owner expands provisioning to R001/R002/R003 at two private planned sites. All three equipment/location records and live voltage reports now reach PocketBase/portal; R003 also delivers actual temperature/humidity. Four reports × two gateways deduplicate correctly. Planned sites/assemblies remain unverified and warnings disabled pending activation. [Operations](../../docs/operations/repeater-telemetry.md), [TEST-009](../../records/field-results.md#test-009--live-repeater-provisioning-and-telemetry). Survey/wishlist work remains deferred.

Label: wayfinder:map

## Destination

A concise, evidence-backed pilot plan for passive SNORR member GPS tracking on Mount Charleston: participating owned hardware, a justified network/firmware choice, a dispatch data path, and agreed test criteria. This first checkpoint is provisional pending owner feedback.

## Notes

- 2026-10-17 — Owner resolves [private monitoring scope](issues/20-monitoring-scope-stack.md): internal-only MeshMonitor, existing Grafana/Prometheus, 30-day metrics and no automatic packet/history pruning; searchable logs deferred. [Deployment](../../docs/operations/meshmonitor-lxc.md) verifies live values, private access, restart persistence and isolated recovery. [Remaining verification](https://github.com/lfg-seth/snorr-meshlink/issues/23) covers native views, two-gateway behavior and growth; portal freshness/archive remain authoritative.

- 2026-10-16 — [Build a dedicated Heltec V3 airtime sniffer](issues/23-airtime-sniffer.md) completes: MC00 runs receive-only `2.7.26.f95a443`; Windows/Linux GUI/CLI logs raw/decoded packets, repeats and airtime. Ten live receptions/seven duplicates, byte-identical opaque/keyed replay, Windows GUI and portable framing pass; Linux GUI/USB and high-load completeness remain unverified. Gateway/repeater roles are unchanged.

- 2026-10-16 — [RAK neighbor and sensor power integration](../../docs/operations/radio-report-ingestion.md) deploys SNNS/standard neighbor decoding and signed, channel-preserving voltage/current display in application `bed40dd`. Archive recovery, fresh R005/G001 normalization and isolated live/demo restore pass; G002 freshness and sensor calibration remain unverified. No new pilot decision or hardware configuration change.

- 2026-10-16 — [Show neighbor signal connections on the map](issues/18-map-neighbor-signals.md) adds the local signal-strength toggle and colored lines without labels, independent legend info disclosure, node-card relationship/pill rows and two endpoint buttons on relationship cards for returning to node cards. Known relationships remain accessible without mapped locations; missing identities stay unknown. Deployed in application release `3ca3a94`; native visual review remains outstanding.

- 2026-10-16 — [Show plain-language GPS quality in tracker cards](issues/15-gps-quality-pill.md) is implemented locally: shared Map/Users Good/Limited/Poor/Unknown pill, same-fix quality storage and plain-language expandable help. All 48 backend checks and frontend checks/default/live builds pass; deployment now passes with application release `3ca3a94`; native browser review and field validation remain outstanding. Existing member flags are unchanged; no metre-accuracy guarantee implied.

- 2026-10-14 owner authorizes port/build/flash of the prior AHT detection fix to R003. Custom `2.7.26.cc5907b` succeeds: actual temperature/humidity and device battery reports reach both V3s (4/4 new receipts), with exact pilot-profile/key preservation. This supersedes R003's stock-only sensor limitation below; R001/R002 remain stock and survey work remains deferred. [Build record](../../docs/operations/r003-aht-build.md), [TEST-008](../../records/field-results.md#test-008--r003-custom-aht-build-and-radio-telemetry).

- 2026-10-14 R003 follow-up: third on-hand RAK4631 receives matching stock pilot profile with device/environment telemetry enabled. Battery packets reach both V3s; reported AHT21 temperature/humidity does not work on the pinned stock RAK target because AHT detection is compiled out with HAS_NCP5623. Stock firmware retained; no two-repeater field-scope change. [Evidence](../../records/field-results.md#test-007--r003-stock-setup-and-environmental-sensor-limit), [source explanation](../../docs/operations/rak-pilot-setup.md#r003-environmental-sensor-follow-up--2026-10-14).

- 2026-10-14 owner resumes stock RAK preparation: R001/R002 are identified RAK4631s, flashed to stock `2.7.26.54e0d8d`, configured on the private pilot channel and verified through explicit reboot. Direct encrypted reception reaches the other RAK and both V3s (6/6); forced GPS relaying, field coverage and battery/solar endurance remain untested. [Setup](../../docs/operations/rak-pilot-setup.md), [evidence](../../records/field-results.md#test-006--stock-rak-pilot-repeater-preparation). Custom survey work remains deferred.

- 2026-10-14 live GPS integration: work alternates between Dell Linux and Windows/WSL through GitHub. [Resume here](../../docs/operations/development-handoff.md). The LXC portal now displays only real bench devices through a persistent read-only MQTT GPS worker; two-gateway receipts/display deduplication, worker restart and isolated live-backup recovery pass. Secrets are in the owner-authorized 1Password Environment with separate private service provisioning. [Measured evidence](../../records/field-results.md#test-005--live-portal-gps-ingestion), [operations](../../docs/operations/live-mqtt.md). Survey and other deferred work stay parked.

- Owner put project work on hold on 2026-10-13 for desktop handoff, then resumed portal hosting, MQTT endpoint testing and live GPS integration on 2026-10-14. [Ubuntu LXC deployment](../../docs/operations/portal-lxc.md) records the running portal, Cloudflare route and backup recovery evidence. Survey and other held work remain deferred. The repeater survey claim remains released; no pilot decision is falsely completed.

- Full mission and standing priorities: [Project brief](../../PROJECT.md).
- Keep it simple. Chart decisions now; implementation and installation follow when their prerequisites are settled.
- Use Wayfinder with the [local tracker](../TRACKER.md) and [tracking workflow](../../docs/operations/local-tracking.md). For live design questions use grilling/domain-modeling lightly; avoid exhaustive interviews at this stage.
- For research, use primary sources and capture a linked report. Firmware changes are a possibility to investigate, not a settled requirement.
- Owned hardware comes first; no speculative purchase list.
- Future ideas are parked in the [deferred feature wishlist](../../records/wishlist.md), outside the active ticket frontier. Do not begin work on them until the owner explicitly brings them forward.
- Historical child tickets live in `issues/`; use the local tracker for the current work queue during the branch trial.
- Owner resumed endpoint testing under [Check Heltec MQTT over WebSockets for Tunnel hosting](issues/09-heltec-websocket-research.md) on 2026-10-14. Public TLS 8883 through Nginx to source-restricted private Mosquitto 1883 passes authentication/delivery checks; Mike handles certificates. The persistent portal worker now decodes actual encrypted GPS through both V3 gateways and saves deduplicated positions. No WebSockets implementation or research-ticket resolution is claimed; that ticket stays open/unassigned.

## Decisions so far

- [Publish the cached RAK build as a fork prerelease](issues/22-rak-prerelease.md) — Exact cached UF2/OTA binaries are published with checksums; routine flashing downloads verified assets, and fork release checks skip all upstream publishing jobs.

- [Improve passive neighbor signal reporting in the RAK fork](issues/21-rak-neighbor-signals.md) — Published firmware adds bounded direct-neighbor RSSI/SNR, hearing age and background companion reports; RAK build and portable checks pass, with flashing and portal ingestion still to verify.

- [Check Meshtastic monitoring and recording stacks for the pilot](issues/19-meshtastic-monitoring-research.md) — Current projects/templates compared; a private read-only MeshMonitor trial leads the shortlist, with stack choice and compatibility checks still open.

- [Serve the demo and neighbor table from a separate PocketBase](issues/17-database-demo-neighbor-table.md) — Local demo pages now read a separate inspectable database with a Git-tracked synthetic checkpoint and ten sample directional signal rows. Production remains on the VM; fork work stays parked. Checks and public deployment pass with application release `3ca3a94`; real signal ingestion remains outstanding.

- [Check node telemetry and directional neighbor signal reporting](issues/16-node-neighbor-telemetry.md) — Gateway receipts can provide final-hop SNR/RSSI; optional NeighborInfo provides directional SNR with slow reporting and configuration limits. Table/storage proposal recorded; implementation and live verification remain outstanding.

- [Establish the portal development and CI baseline](issues/13-portal-build-environment.md) — Accepted stack scaffolded with approachable TypeScript, native Dell commands and GitHub-hosted tests/build artifacts; optional desktop integration and VM deployment follow later.

- [Inventory owned hardware for the pilot](issues/01-inventory.md) — First-pass on-hand stock confirmed; four devices have GPS modules. Plan from current stock, with deployed/uncertain hardware excluded and build/runtime checks carried into pilot selection.

- [Define useful tracking for the first field pilot](issues/02-pilot-needs.md) — 6 GPS-equipped V4 member trackers, RAK repeaters, and 2 V3 internet backhauls (one later permitted to transmit portal replies); stale at 15 minutes with visible age; battery minimum 4 hours, target 12; power-on tracking, SOS deferred.

- [Distinguish LoRaWAN and the candidate mesh firmware](issues/03-protocol-baseline.md) — Separate architectures; existing timing settings warrant a configuration-first evaluation, while hardware compatibility and passive behavior still need bench evidence.

- [Choose the pilot network and firmware approach](issues/04-pilot-approach.md) — Meshtastic evaluation with 6 planned V4 trackers, 2 RAK relays, 2 V3 private-MQTT uplinks, local app viewing first, and optional phone backhauls subject to staged testing; later portal amendment permits one designated V3 to transmit replies.

- [Define a future device-only SOS workflow](issues/05-sos-workflow.md) — Five-second user-button activation/cancellation, readable SOS reminders plus faster normal tracking, OLED alerts, GPS-age fallback, reboot persistence, and originator-only cancellation; implementation follows passive tracking, with power detection pinned.

- [Check portal MQTT hosting and backend options](issues/07-portal-transport-research.md) — HTTPS Tunnel suits the portal; stock MQTT needs a separate broker route; PocketBase and one-gateway downlink are candidates with explicit implementation limits.

- [Check dispatch map sources and nonprofit access](issues/08-portal-map-research.md) — MapLibre with free USGS topo/aerial layers is an evaluation shortlist; nonprofit programs are conditional, and imagery age/zoom and offline behavior need verification.

- [Define the dispatch portal MVP](issues/06-dispatch-portal.md) — Four responsive pages for tracking, assignments, shared messages and recorded infrastructure health; configurable warnings, local-app outage fallback, pilot stack evaluation and owner-deferred MQTT connectivity assumption.

- [Check persistent device identity and remote name updates](issues/11-device-identity-research.md) — Capture verified local hardware identity independently of mutable names/node IDs; PKI admin supports set-owner updates, while portal execution needs a trusted controller/admin integration.

- [Choose assignment-driven radio names and identity](issues/12-assignment-radio-names.md) — Short names stay tied to device numbers across carrier changes; portal identity/history and pending radio-name updates remain separate.

- [Define infrastructure warning and intrusion handling](issues/10-infrastructure-warning-rules.md) — Silent persistent badges, capability-specific cadence rules, automatic health recovery, admin-resolved intrusion incidents, feed-outage handling and battery configuration metadata.

## Not yet specified

- Monitoring rollout detail beyond the initial scope/collector decision: measured storage budgets, access/role configuration, retention, maintenance ownership and whether an independent outage observer is useful. No service deployment or monitoring integration is accepted yet.

- Owner brought [Define repeater operations and direct-link placement testing](issues/14-repeater-operations-survey.md) forward on 2026-10-13: solar RAKs with 2–4 18650 cells and Muzi/fiberglass antennas; firmware pong responder, GPS-equipped V4 testing node and Dell logging. Draft procedure recorded; candidate locations, endurance target, exact builds and survey acceptance criteria remain open. Portal work is set aside for this discussion; MQTT hold remains.

- Owner brought portal design/building forward on 2026-10-13 while nodes are unavailable. The [portal build plan](portal-build-plan.md) now has a reviewed four-page prototype and a local authenticated PocketBase/Python simulation backend. Deployment/backup/restore and selected-build hardware integration remain to verify.

- Exact V4 builds, compatibility, and readiness for the planned six-device pilot after purchases/recoveries and bench checks.
- How much firmware customization is actually needed for the agreed reporting behavior.
- Optional member backhaul capacity remains to measure. Portal requirements and transport/map-source questions are now explicit child tickets; ingestion implementation follows the agreed specification.
- Required local command-post and companion-app location viewing without internet backhaul: Meshtastic app first, with laptop/portal viewing also intended and an owned rugged Linux Dell available. Verify connections, offline maps, and stale data behavior.
- Test routes, acceptance thresholds, and a repeatable build/configuration for the pilot.
- Solar/18650 power and enclosure design matched to measured consumption and environmental requirements.
- Site surveys, permission, installation, maintenance, and member rollout after pilot evidence.
- Evidence needed for a supported expansion budget and stakeholder presentation.

## Out of scope

- Full mountain deployment and production portal implementation during this planning checkpoint.
- Law enforcement rollout; it remains a later project goal.
- Purchases, public publishing, external outreach, and grant submissions in this setup session.
