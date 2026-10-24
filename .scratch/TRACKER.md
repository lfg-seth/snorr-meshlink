# Current work

Permanent local tracking accepted 2026-10-23. This file owns current status on
`main`; [workflow](../docs/operations/local-tracking.md). GitHub issues/Project
remain historical references, without automatic synchronization. Linked GH-N
imports retain original requirements. Priority stays passive member GPS,
communications, then law-enforcement expansion. Listing work is not authorization.

## Current

| Task | Lane | Handoff / next action |
| --- | --- | --- |
| R006 portal cadence acceptance | Software / live verification | Latest owner instruction replaces the unapplied point request with a labelled random Las Vegas placeholder; authenticated map readback passes. Next: reconcile saved three-minute firmware/cadence metadata and verify authenticated R006 receipts without changing the new placeholder. [Map acceptance](../docs/operations/g003-portal.md), [bench evidence](../docs/operations/repeater-update.md#r006-and-gateway-admin-bench---2026-10-24); release/other-board work belongs to LOCAL-3. |
| [GH-4 — INA219 same-path diagnosis](../records/tracking-import/github-4.md) | Bench | R006 profile/reboot and three signed power cycles pass; physical accuracy and battery-only behavior remain unresolved. Next: confirm shunt/polarity and compare simultaneous shunt mV/series battery current. Serial closed; R004 diagnostics/bridge-state question unchanged. [Hardware](../docs/operations/repeater-update.md#r006-installed-verification), [audit](../docs/operations/ina219-audit.md#r006-production-preparation--2026-10-23). |

## Next

Ready follow-ups and items needing scope/prerequisites; select with the owner before starting. Imported Triage stays unresolved rather than becoming Ready by migration.

Select one Software outcome; keep a Bench plan/run available when inputs permit.
Linked briefs and parent assignment tables own scope, not status. [Dispatch and
handoff rules](../docs/operations/local-tracking.md#task-dispatch-and-context).

| Task | Lane | Next action / prerequisite |
| --- | --- | --- |
| [LOCAL-3 - Production firmware readiness](pilot/issues/25-production-firmware-readiness.md) | Bench / Software follow-ups | Reviewed/pinned `4c96b9ba0` installed on R006/G001/G002; B002 PKI, 180/300/900 SNNS, interrupted edit and full-profile restoration verified through both gateways. Serial closed; original admin allowlist restored; secrets in 1Password Pilot. Next bench: forced-relay admin/lost-command handling excluding direct reception; resolve rebooting-write ACK ambiguity before inaccessible use. Continue independent software freshness contract. [Measurements/limits](../docs/operations/repeater-update.md#r006-and-gateway-admin-bench---2026-10-24). Release, portal, soak and GH-4/GH-8/LOCAL-4/field gates remain open. |
| [GH-2 — Phone-free GPS freshness/runtime](../records/tracking-import/github-2.md) | Bench preparation → run | Next: [prepare the B001/B002 run plan](tasks/gh-2-run-plan.md), then agree hardware, sampling and missing/stale criteria before measuring. Preserve 15-minute stale, four-hour minimum/12-hour target. |
| [LOCAL-6 - SNORR firmware releases](pilot/issues/28-snorr-firmware-releases.md) | Software | Next: [version/manifest foundation](tasks/local-6-release-foundation.md); coordinate shared firmware writes with LOCAL-3. [0.1.0](../records/firmware-releases/0.1.0.md) remains the mixed-fleet development baseline, production 1.0.0. Artifact publication and rollout follow separately. |
| [LOCAL-4 - Heltec V3 gateway readiness](pilot/issues/26-gateway-production-readiness.md) | Bench preparation / Software | Next: [power plan and exact-parts checklist](tasks/local-4-power-plan.md). Parent assignment boundaries separate measurements, enclosure, TLS/reconnect, sensor, release and soak work; shared SNNS contract stays LOCAL-3. |
| [GH-3 — Forced relay and outage/local viewing](../records/tracking-import/github-3.md) | Bench | Ready: define a test excluding direct reception, then verify relay, backhaul recovery and useful offline viewing with agreed devices/criteria. Preserve radio permissions/profiles. |
| [GH-39 — Bounded demo battery-history recovery](../records/tracking-import/github-39.md) | Software / live verification | Ready: correct/check the installed verifier's untruncated-history assertion. Independent exact bounded-history/full-database recovery passes; installed verifier remains unchanged. [Evidence](../docs/operations/ina219-audit.md#recovery-evidence). |
| [GH-7 — Off-host backup recovery](../records/tracking-import/github-7.md) | Software / decision | Triage: choose an authorized private destination/retention plan, then verify separate live/demo recovery beyond the current host. |
| [GH-8 — Recurring high channel utilization](../records/tracking-import/github-8.md) | Bench | Triage: capture recurrence with existing receive-only tools before diagnosis or radio changes. |
| [GH-18 — Measured field-pilot plan](../records/tracking-import/github-18.md) | Bench | Triage; needs bench/relay/power evidence, agreed devices/access/route and acceptance thresholds before a field run. |

## Verify

Keep implementation, release, native presentation, live delivery and field acceptance separate. Imported open criteria remain pending unless later evidence is recorded.

| Task | Remaining check / evidence |
| --- | --- |
| G003 dedicated-account radio cutover | Dedicated broker account/public TLS and concealed 1Password save pass; live portal registration, mappings, labelled random placement and seven normalized receipts pass. Next: owner reconnects G003 after G004, then change only MQTT credentials, verify full profile through reboot and fresh delivery using its own account. Current radio still uses G002's credentials; Wi-Fi API unavailable from desktop. [Acceptance and private inputs](../docs/operations/g003-portal.md). |
| Gateway-aware portal recovery verifier | Staged update uses registered gateway mappings instead of hard-coded G001/G002; two regression checks and full 11-device post-change restore pass. Automatic approval review rejects persistent live-tool replacement as outside the initial scope; explicit owner approval is pending. Installed verifier remains unchanged. [Evidence](../docs/operations/g003-portal.md#backups-and-recovery). |
| MeshLink 0.1.0 release validation | Version metadata, changelog/tag/package validation and 56 portal checks/build pass. Windows backend cutover test connection leak fixed; full-suite runs still show intermittent connection resets and skip seven POSIX-only tests. Next: confirm Linux CI before tagging/publishing the combined release; source merge is not server deployment. [Release procedure](../docs/operations/meshlink-releases.md). |
| [GH-9 — Expanded demo release](../records/tracking-import/github-9.md) | Preserve completed release evidence; finish native review of battery/power/humidity/neighbor examples and remaining imported acceptance. [Release](../docs/operations/portal-lxc.md#demo-feature-examples-and-minimap-navigation--2026-10-20). |
| [GH-21 — Neighbor minimap navigation](../records/tracking-import/github-21.md) | Deployed; verify native desktop/mobile endpoint interaction and retained relationship/viewport behavior. [Release](../docs/operations/portal-lxc.md#demo-feature-examples-and-minimap-navigation--2026-10-20). |
| [GH-23 — MeshMonitor acceptance](../records/tracking-import/github-23.md) | Native views, two-gateway behavior, storage growth and off-host recovery remain; retain read-only/isolation boundaries. [Operations](../docs/operations/meshmonitor-lxc.md). |
| [GH-42 — Gateway battery graphs](../records/tracking-import/github-42.md) | Deployed; confirm native graph presentation. G001 fresh telemetry remains separate from G002's verified graph/cadence. [Evidence](../docs/operations/gateway-battery-graphs.md). |
| [GH-47 — Stale neighbor signal visibility](../records/tracking-import/github-47.md) | Deployed **443ba03**; server 74 backend/55 portal checks, migrated live/demo recovery, fresh SNNS through both gateways and actual-component calculated expiry pass. Next: native desktop/mobile and sustained freshness/outage acceptance. Strict unseen upstream-delay hearing limit now belongs to LOCAL-3 (consumed GH-51/GH-52). PR #50 stays undeployed. [Release evidence](../docs/operations/neighbor-signal-visibility.md#deployment---2026-10-21). |
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
| [GH-43 — Neighbor card cleanup/two-hour expiry](../records/tracking-import/github-43.md) | Presentation wishlist remains deferred; GH-47's corrective freshness work is a separate scope. |
| [GH-44 — Hide absent sensor values](../records/tracking-import/github-44.md) | Wishlist: omit sensor voltage/current when sensors are absent. |
| [GH-45 — Member battery percentage](../records/tracking-import/github-45.md) | Wishlist: percentage beside GPS quality on node cards. |
| [GH-48 — Remove Endpoint locations](../records/tracking-import/github-48.md) | Wishlist: remove the neighbor-card section. |
| [GH-49 — Longer sign-in persistence](../records/tracking-import/github-49.md) | Wishlist: reproduce roughly hourly reauthentication when activated; cause/lifetime remain unknown. |
| [LOCAL-1 — Infrastructure page overhaul](../records/wishlist.md#infrastructure-page-overhaul) | Wishlist: richer clickable device summary cards including member devices; readable current-neighbor overview; optional collapsed, sortable, paginated debug table with timestamps; move useful unique detail into full cards. Await owner activation. |
| [LOCAL-2 — Member node/battery reports without GPS](../records/wishlist.md#member-node-and-battery-reports-without-a-gps-fix) | Owner reports missing member battery data. Target node/status and battery broadcasts every five minutes (300 seconds), including without a fix or phone, with truthful contact/signal freshness. Await activation; verify actual member settings and end-to-end delivery before choosing a fix. |

| [LOCAL-5 - Public Markdown blog/wiki](pilot/issues/27-public-markdown-blog-wiki.md) | Broad public project docs, human-readable and owner-copyedited, with illustrated node setup pages. Agent internals excluded; issue pages provisionally excluded. Approved content ships through manual deployment. Hardware source section now exists; implementation/publication remain deferred. [Wishlist](../records/wishlist.md#public-markdown-blog-and-hardware-wiki). |

Completed work belongs in [the session log](../records/sessions.md), with decisions/measurements in existing records. [Import index](../records/tracking-import/index.md) preserves all 36 open issues and their historical labels/discussion; it is not another queue.
