# Define an owned-hardware field pilot

Label: wayfinder:map

## Destination

A concise, evidence-backed pilot plan for passive SNORR member GPS tracking on Mount Charleston: participating owned hardware, a justified network/firmware choice, a dispatch data path, and agreed test criteria. This first checkpoint is provisional pending owner feedback.

## Notes

- 2026-10-14 owner resumes stock RAK preparation: R001/R002 are identified RAK4631s, flashed to stock `2.7.26.54e0d8d`, configured on the private pilot channel and verified through explicit reboot. Direct encrypted reception reaches the other RAK and both V3s (6/6); forced GPS relaying, field coverage and battery/solar endurance remain untested. [Setup](../../docs/operations/rak-pilot-setup.md), [evidence](../../records/field-results.md#test-006--stock-rak-pilot-repeater-preparation). Custom survey work remains deferred.

- 2026-10-14 live GPS integration: work alternates between Dell Linux and Windows/WSL through GitHub. [Resume here](../../docs/operations/development-handoff.md). The LXC portal now displays only real bench devices through a persistent read-only MQTT GPS worker; two-gateway receipts/display deduplication, worker restart and isolated live-backup recovery pass. Secrets are in the owner-authorized 1Password Environment with separate private service provisioning. [Measured evidence](../../records/field-results.md#test-005--live-portal-gps-ingestion), [operations](../../docs/operations/live-mqtt.md). Survey and other deferred work stay parked.

- Owner put project work on hold on 2026-10-13 for desktop handoff, then resumed portal hosting, MQTT endpoint testing and live GPS integration on 2026-10-14. [Ubuntu LXC deployment](../../docs/operations/portal-lxc.md) records the running portal, Cloudflare route and backup recovery evidence. Survey and other held work remain deferred. The repeater survey claim remains released; no pilot decision is falsely completed.

- Full mission and standing priorities: [Project brief](../../PROJECT.md).
- Keep it simple. Chart decisions now; implementation and installation follow when their prerequisites are settled.
- Use Wayfinder with the local tracker in [Tracker conventions](../TRACKER.md). For live design questions use grilling/domain-modeling lightly; avoid exhaustive interviews at this stage.
- For research, use primary sources and capture a linked report. Firmware changes are a possibility to investigate, not a settled requirement.
- Owned hardware comes first; no speculative purchase list.
- Future ideas are parked in the [deferred feature wishlist](../../records/wishlist.md), outside the active ticket frontier. Do not begin work on them until the owner explicitly brings them forward.
- Child tickets live in `issues/`; find the frontier using the tracker conventions rather than duplicating open questions here.
- Owner resumed endpoint testing under [Check Heltec MQTT over WebSockets for Tunnel hosting](issues/09-heltec-websocket-research.md) on 2026-10-14. Public TLS 8883 through Nginx to source-restricted private Mosquitto 1883 passes authentication/delivery checks; Mike handles certificates. The persistent portal worker now decodes actual encrypted GPS through both V3 gateways and saves deduplicated positions. No WebSockets implementation or research-ticket resolution is claimed; that ticket stays open/unassigned.

## Decisions so far

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
