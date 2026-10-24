# Current work

Permanent local tracking accepted 2026-10-23. This file owns current status on
`main`; [workflow](../docs/operations/local-tracking.md). GitHub issues/Project
remain historical references, without automatic synchronization. Linked GH-N
imports retain original requirements. Priority stays passive member GPS,
communications, then law-enforcement expansion. Listing work is not authorization.

## Current

| Task | Lane | Handoff / next action |
| --- | --- | --- |
| R006 map placement / portal acceptance | Software / live verification | Selected `2.7.26.4c96b9b` admin/cadence bench reaches both gateways; full profiles restored. Portal acceptance still needs server access. Next: apply private map/cadence metadata and verify authenticated receipts. [Current bench evidence](../docs/operations/repeater-update.md#r006-and-gateway-admin-bench---2026-10-24); release/other-board work belongs to LOCAL-3. |
| [GH-4 — INA219 same-path diagnosis](../records/tracking-import/github-4.md) | Bench | Owner confirms common wiring and charging R002/R004/R006 versus discharging G003; [global API polarity correction](../docs/operations/radio-report-ingestion.md#meshlink-011-deployment---2026-10-24) is deployed in MeshLink 0.1.1 with fresh current/raw pairs verified. Physical accuracy and battery-only behavior remain unresolved. Next: confirm shunt and compare simultaneous shunt mV/series battery current. Serial closed; R004 bridge-state question unchanged. [Hardware](../docs/operations/repeater-update.md#r006-installed-verification), [audit](../docs/operations/ina219-audit.md#r006-production-preparation--2026-10-23). |

## Next

Ready follow-ups and items needing scope/prerequisites; select with the owner before starting. Imported Triage stays unresolved rather than becoming Ready by migration.

Select one Software outcome; keep a Bench plan/run available when inputs permit.
Linked briefs and parent assignment tables own scope, not status. [Dispatch and
handoff rules](../docs/operations/local-tracking.md#task-dispatch-and-context).

| Task | Lane | Next action / prerequisite |
| --- | --- | --- |
| G004 GPS mesh time commissioning | Bench | Failed V3 `!849ae664` is retired; replacement OLED V4 `!699c2ed8` now passes `2.7.26.6fea6aa`, original GPS/pin preservation and 180-second gateway reporting. Fresh outdoor GPS fix and autonomous mesh-clock propagation remain unverified; the outage bench supplied time once over serial after its deliberate reboot. Next: agreed sky-view/time test. [Current gateway evidence](../docs/operations/gateway-backhaul-health.md#completed-bench-and-deployment---2026-10-24). |
| [LOCAL-3 - Production firmware readiness](pilot/issues/25-production-firmware-readiness.md) | Bench / Software follow-ups | Reviewed `4c96b9ba0` installed on R002/R004/R006/G001/G002; [R002](../docs/operations/r002-three-minute.md) and [R004](../docs/operations/r004-three-minute.md) full profile/reboot and 180-second device/environment/power plus 195-second SNNS source gaps pass through both gateways. R006 B002 PKI, 180/300/900 SNNS and interrupted edit/restoration pass; serial closed, original admin allowlist restored. Next bench: forced-relay admin/lost-command handling excluding direct reception; resolve rebooting-write ACK ambiguity before inaccessible use. New `6fea6aa68` pin and all-four gateway health/outage rollout pass separately; continue software freshness contract. [Admin measurements/limits](../docs/operations/repeater-update.md#r006-and-gateway-admin-bench---2026-10-24). Release, portal, soak and GH-4/GH-8/LOCAL-4/field gates remain open. |
| [GH-2 — Phone-free GPS freshness/runtime](../records/tracking-import/github-2.md) | Bench preparation → run | Next: [prepare the B001/B002 run plan](tasks/gh-2-run-plan.md), then agree hardware, sampling and missing/stale criteria before measuring. Preserve 15-minute stale, four-hour minimum/12-hour target. |
| [LOCAL-6 - SNORR firmware releases](pilot/issues/28-snorr-firmware-releases.md) | Software | Next: [version/manifest foundation](tasks/local-6-release-foundation.md); coordinate shared firmware writes with LOCAL-3. [0.1.0](../records/firmware-releases/0.1.0.md) remains the mixed-fleet development baseline, production 1.0.0. Artifact publication and rollout follow separately. |
| [LOCAL-4 - Heltec V3 gateway readiness](pilot/issues/26-gateway-production-readiness.md) | Bench preparation / Software | Four-board reporting and G001 Wi-Fi outage/recovery pass ([evidence](../docs/operations/gateway-backhaul-health.md#completed-bench-and-deployment---2026-10-24)); next: [power plan and exact-parts checklist](tasks/local-4-power-plan.md). Parent assignment boundaries separate measurements, enclosure, TLS/reconnect, sensor, release and soak work; shared SNNS contract stays LOCAL-3. |
| [GH-3 — Forced relay and outage/local viewing](../records/tracking-import/github-3.md) | Bench | Ready: define a test excluding direct reception, then verify relay, backhaul recovery and useful offline viewing with agreed devices/criteria. Preserve radio permissions/profiles. |
| [GH-7 — Off-host backup recovery](../records/tracking-import/github-7.md) | Software / decision | Triage: choose an authorized private destination/retention plan, then verify separate live/demo recovery beyond the current host. |
| [GH-8 — Recurring high channel utilization](../records/tracking-import/github-8.md) | Bench | Triage: capture recurrence with existing receive-only tools before diagnosis or radio changes. |
| [GH-18 — Measured field-pilot plan](../records/tracking-import/github-18.md) | Bench | Triage; needs bench/relay/power evidence, agreed devices/access/route and acceptance thresholds before a field run. |

## Verify

Keep implementation, release, native presentation, live delivery and field acceptance separate. Imported open criteria remain pending unless later evidence is recorded.

| Task | Remaining check / evidence |
| --- | --- |
| Gateway backhaul health / MeshLink 0.1.3 | All four `2.7.26.6fea6aa` profiles, peer receipts, G001 real Wi-Fi outage/recovery, public authenticated state, source/tag/build metadata and isolated backups pass; serial/MQTT closed. Next: native owner-phone check and agreed sustained outage/airtime/power run. Unknown-clock bootstrap, forced relay, calibration/runtime and field gates remain open. [Evidence](../docs/operations/gateway-backhaul-health.md#completed-bench-and-deployment---2026-10-24). |
| B002 member GPS/runtime acceptance | Owner-requested `2.7.26.a56466d`, complete profile/reboot, device telemetry at 180 seconds and saved-baseline radio SNNS pass; two fresh battery/SNNS cycles reach G001/G002/G003 and authenticated portal/database checks pass. GPS remains 60/120 seconds; no fresh fix observed. One boot after serial close has unverified cause. Next: GH-2 phone-free run preparation, including power/boot stability and agreed GPS/runtime sampling criteria. [Evidence](../docs/operations/b002-three-minute.md). |
| R002 portal cadence acceptance | Ordinary `2.7.26.4c96b9b`, full profile/reboot and two fresh device/environment/INA219 power/SNNS reports through each gateway pass; owner confirms INA219. Next: with authenticated server/portal access, reconcile private cadence/sensor metadata to 180 seconds and verify portal receipts/freshness. No temperature/humidity received; physical INA219 path/calibration remains unverified. [Evidence](../docs/operations/r002-three-minute.md). |
| R004 portal cadence acceptance | Ordinary `2.7.26.4c96b9b`, full profile/reboot and two fresh device/environment/power/SNNS reports through each gateway pass. Next: with authenticated server/portal access, reconcile R004's private cadence metadata to 180 seconds and verify portal receipts/freshness. Calibration remains GH-4. [Evidence](../docs/operations/r004-three-minute.md). |
| Gateway account separation | G001–G004 are registered and deliver fresh telemetry/SNNS/health through peers on MeshLink 0.1.3. G003/G004 still use the existing uplink account; separate accounts remain an authorized follow-up to select. Current profiles/credentials are preserved. [Four-board acceptance](../docs/operations/gateway-backhaul-health.md#completed-bench-and-deployment---2026-10-24). |
| [LOCAL-8 — Device-card battery summary](../records/wishlist.md#device-card-battery-summary-without-duplicate-sensor-readings) | PR #60 merged; MeshLink 0.1.2 / `359e6ba` deployed. 75 backend/60 portal tests, public hashes, protected state, live/demo recovery, all-device live-data rendering and native desktop/mobile demo cards pass. Next: owner-phone authenticated acceptance; physical accounting stays separate. Installed verifier maintenance is [complete](../docs/operations/backup-recovery-verifiers.md). [Release evidence](../docs/operations/device-card-battery-summary.md#meshlink-012-deployment---2026-10-24). |
| [GH-9 — Expanded demo release](../records/tracking-import/github-9.md) | Preserve completed release evidence; finish native review of battery/power/humidity/neighbor examples and remaining imported acceptance. [Release](../docs/operations/portal-lxc.md#demo-feature-examples-and-minimap-navigation--2026-10-20). |
| [GH-21 — Neighbor minimap navigation](../records/tracking-import/github-21.md) | Deployed; verify native desktop/mobile endpoint interaction and retained relationship/viewport behavior. [Release](../docs/operations/portal-lxc.md#demo-feature-examples-and-minimap-navigation--2026-10-20). |
| [GH-23 — MeshMonitor acceptance](../records/tracking-import/github-23.md) | Native views, two-gateway behavior, storage growth and off-host recovery remain; retain read-only/isolation boundaries. [Operations](../docs/operations/meshmonitor-lxc.md). |
| [GH-53 — Telemetry clock-loss fallback](../records/tracking-import/github-53.md) | Deployed; verify native owner/mobile presentation and sustained telemetry/outage behavior. Fresh R002/R004 selection/history pass; receipt fallback is approximate for delayed unknown-clock reports. [Evidence](../docs/operations/battery-contact-freshness-20261021.md#deployment---2026-10-21). |

## Deferred

Owner activation is required before research, design, implementation or testing. Details live in the linked import or [wishlist](../records/wishlist.md); migration and mentioning an idea keep it parked.

| Task | Hold / future outcome |
| --- | --- |
| [GH-13 - Future deployment automation/staging](../records/wishlist.md#future-staging-or-automatic-deployments) | Policy resolved 2026-10-23: main, manual production updates, no staging now. Remaining automation/connection/staging work deferred; revisit only on owner activation. |
| [GH-11 — Repeater operations/site survey](../records/tracking-import/github-11.md) | Owner-held survey; define direct-link placement procedure when resumed. |
| [GH-12 — Heltec MQTT over WebSockets](../records/tracking-import/github-12.md) | Revisit only if the deployed transport needs an alternative. |
| [GH-14 — Messaging/remote administration](../records/tracking-import/github-14.md) | Later communications scope after passive tracking. |
| [GH-15 — Known Wi-Fi/MQTT backhaul](../records/tracking-import/github-15.md) | Wishlist: automatic connection using known networks. |
| [GH-16 — Browser firmware flashing](../records/tracking-import/github-16.md) | Wishlist: member-owned supported devices. |
| [GH-17 — Slack integration](../records/tracking-import/github-17.md) | Wishlist: exact purpose and data flow remain unspecified. |
| [GH-20 — Repeatable member rollout](../records/tracking-import/github-20.md) | Wait for accepted field-pilot evidence. |
| [GH-34 — Overlapping map nodes](../records/tracking-import/github-34.md) | Wishlist: separately visible/selectable markers, preserving stored coordinates. |
| [GH-35 — Selected-node desktop signals](../records/tracking-import/github-35.md) | Wishlist: limit the main-map signals to the selected node. |
| [GH-36 — Default map center](../records/tracking-import/github-36.md) | Wishlist: center on all node locations. |
| [GH-37 — Tracking session controls](../records/tracking-import/github-37.md) | Wishlist: start/stop/restart sessions while the radio stays powered. |
| [LOCAL-9 — Router/gateway card eyebrow model](../records/wishlist.md#router-and-gateway-card-eyebrow-device-model) | Show hardware model at the top like client cards, retaining Backhaul/Router role text. Await owner activation. |
| [LOCAL-7 — Large-map router/gateway health colors](../records/wishlist.md#large-map-router-and-gateway-health-colors) | Match client last-heard colors; low battery overrides with yellow/red. Battery thresholds and stale/missing handling await activation. |
| [LOCAL-1 — Infrastructure page overhaul](../records/wishlist.md#infrastructure-page-overhaul) | Wishlist: richer clickable device summary cards including member devices; readable current-neighbor overview; optional collapsed, sortable, paginated debug table with timestamps; move useful unique detail into full cards. Await owner activation. |
| [LOCAL-2 — Member node/battery reports without GPS](../records/wishlist.md#member-node-and-battery-reports-without-a-gps-fix) | Owner reports missing member battery data. Target node/status and battery broadcasts every five minutes (300 seconds), including without a fix or phone, with truthful contact/signal freshness. Await activation; verify actual member settings and end-to-end delivery before choosing a fix. |

| [LOCAL-5 - Public Markdown blog/wiki](pilot/issues/27-public-markdown-blog-wiki.md) | Broad public project docs, human-readable and owner-copyedited, with illustrated node setup pages. Agent internals excluded; issue pages provisionally excluded. Approved content ships through manual deployment. Hardware source section now exists; implementation/publication remain deferred. [Wishlist](../records/wishlist.md#public-markdown-blog-and-hardware-wiki). |

Completed work belongs in [the session log](../records/sessions.md), with decisions/measurements in existing records. [Import index](../records/tracking-import/index.md) preserves all 36 open issues and their historical labels/discussion; it is not another queue.
