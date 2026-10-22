# Current work

Local-tracking trial, 2026-10-21, on `trial/local-tracking`. This file owns current status on this branch; [workflow and rollback](../docs/operations/local-tracking.md). GitHub issues/Project remain unchanged. Linked `GH-N` files preserve the one-time import; open only the selected task's details. Priority stays passive member GPS, communications, then law-enforcement expansion. Listing work is not authorization to execute it.

## Current

| Task | Handoff / next action |
| --- | --- |
| [GH-4 — INA219 same-path diagnosis](../records/tracking-import/github-4.md) | Retain the existing bounded Codex Windows/R004 diagnostic claim awaiting the owner's bridge-state reply; serial is closed. Confirm whether VIN+→VIN− was bridged, then compare bridge-on/off with battery disconnected under the existing diagnostic scope. Accuracy and full wiring remain unresolved; preserve image/profile. [Audit](../docs/operations/ina219-audit.md#r004-reinvestigation--2026-10-21). |

## Next

Ready follow-ups and items needing scope/prerequisites; select with the owner before starting. Imported Triage stays unresolved rather than becoming Ready by migration.

| Task | Next action / prerequisite |
| --- | --- |
| [GH-2 — Phone-free GPS freshness/runtime](../records/tracking-import/github-2.md) | Ready: agree run plan and available B001/B002 hardware, then measure measurement age, two-gateway delivery and battery runtime. Preserve 15-minute stale threshold, four-hour minimum and 12-hour target. |
| [GH-3 — Forced relay and outage/local viewing](../records/tracking-import/github-3.md) | Ready: define a test excluding direct reception; verify relay, backhaul recovery and useful offline viewing without silently changing radio profiles. |
| [GH-39 — Bounded demo battery-history recovery](../records/tracking-import/github-39.md) | Ready: reproduce bounded-history verifier failure; correct/check the verifier without truncating demo history or changing production data. |
| [GH-7 — Off-host backup recovery](../records/tracking-import/github-7.md) | Triage: choose an authorized private destination/retention plan, then verify separate live/demo recovery beyond the current host. |
| [GH-8 — Recurring high channel utilization](../records/tracking-import/github-8.md) | Triage: capture the recurrence with the existing receive-only tools before identifying cause or changing radio settings. |
| [GH-13 — Deployment branch/staging policy](../records/tracking-import/github-13.md) | Triage: agree policy before release automation; this tracking branch does not choose production deployment policy. |
| [GH-18 — Measured field-pilot plan](../records/tracking-import/github-18.md) | Triage, blocked on bench/relay/power evidence: agree available devices, access, route and acceptance thresholds before a field run. |
| [GH-51 — Gateway neighbor timing](../records/tracking-import/github-51.md) | Triage: GH-47 selects application current state with installed relative ages. Select and verify gateway stale-queue/source expiry or another delivery-age contract before a strict outage-safe hearing limit; absolute timestamps remain optional. No firmware work or rollout selected. [Decision](pilot/issues/24-neighbor-current-state.md). |
| [GH-52 — Repeater neighbor timing](../records/tracking-import/github-52.md) | Triage: coordinate radio/relay/backhaul residence bounds with GH-51; relative current-state expiry alone excludes unseen upstream delay. Preserve R004's separate diagnostics. Firmware/board scope remains unselected. [Decision](pilot/issues/24-neighbor-current-state.md). |

## Verify

Keep implementation, release, native presentation, live delivery and field acceptance separate. Imported open criteria remain pending unless later evidence is recorded.

| Task | Remaining check / evidence |
| --- | --- |
| [GH-5 — Fresh G002 neighbor/power delivery](../records/tracking-import/github-5.md) | Fresh G002 neighbor delivery/deduplication passed. Sensor-power receipt remains unverified under the deliberately power-disabled RAK profile; agree a configured source/test scope before observing fresh power. |
| [GH-9 — Expanded demo release](../records/tracking-import/github-9.md) | Preserve completed release evidence; finish native review of battery/power/humidity/neighbor examples and remaining imported acceptance. [Release](../docs/operations/portal-lxc.md#demo-feature-examples-and-minimap-navigation--2026-10-20). |
| [GH-21 — Neighbor minimap navigation](../records/tracking-import/github-21.md) | Deployed; verify native desktop/mobile endpoint interaction and retained relationship/viewport behavior. [Release](../docs/operations/portal-lxc.md#demo-feature-examples-and-minimap-navigation--2026-10-20). |
| [GH-23 — MeshMonitor acceptance](../records/tracking-import/github-23.md) | Native views, two-gateway behavior, storage growth and off-host recovery remain; retain read-only/isolation boundaries. [Operations](../docs/operations/meshmonitor-lxc.md). |
| [GH-26 — R001 CLIENT/temperature acceptance](../records/tracking-import/github-26.md) | Firmware/profile preparation exists; verify actual configured temperature receipt and remaining sustained/two-gateway checks. [Bench evidence](../docs/operations/repeater-gateway-check-20261019.md). |
| [GH-27 — R002 CLIENT/temperature acceptance](../records/tracking-import/github-27.md) | Firmware/profile preparation exists; verify actual configured temperature receipt and remaining sustained/two-gateway checks. [Bench evidence](../docs/operations/repeater-gateway-check-20261019.md). |
| [GH-40 — Missing production updates/reconnect](../records/tracking-import/github-40.md) | Observe sustained per-gateway delivery; capture Wi-Fi/MQTT state before resetting during recurrence. G002 Wi-Fi replacement alone does not resolve the trigger. [G002 record](../docs/operations/g002-neighbor-gateway.md). |
| [GH-42 — Gateway battery graphs](../records/tracking-import/github-42.md) | Deployed; confirm native graph presentation. G001 fresh telemetry remains separate from G002's verified graph/cadence. [Evidence](../docs/operations/gateway-battery-graphs.md). |
| [GH-47 — Stale neighbor signal visibility](../records/tracking-import/github-47.md) | Deployed **443ba03**; server 74 backend/55 portal checks, migrated live/demo recovery, fresh SNNS through both gateways and actual-component calculated expiry pass. Next: native desktop/mobile and sustained freshness/outage acceptance. Strict unseen upstream-delay hearing limit remains GH-51/GH-52 work. PR #50 stays undeployed. [Release evidence](../docs/operations/neighbor-signal-visibility.md#deployment---2026-10-21). |
| [GH-53 — Telemetry clock-loss fallback](../records/tracking-import/github-53.md) | Deployed; verify native owner/mobile presentation and sustained telemetry/outage behavior. Fresh R002/R004 selection/history pass; receipt fallback is approximate for delayed unknown-clock reports. [Evidence](../docs/operations/battery-contact-freshness-20261021.md#deployment---2026-10-21). |

## Deferred

Owner activation is required before research, design, implementation or testing. Details live in the linked import or [wishlist](../records/wishlist.md); migration and mentioning an idea keep it parked.

| Task | Hold / future outcome |
| --- | --- |
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

Completed work belongs in [the session log](../records/sessions.md), with decisions/measurements in existing records. [Import index](../records/tracking-import/index.md) preserves all 36 open issues and their historical labels/discussion; it is not another queue.
