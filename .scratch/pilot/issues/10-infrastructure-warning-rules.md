# Define infrastructure warning and intrusion handling

Type: grilling
Label: wayfinder:grilling
Status: resolved
Assignee: infrastructure-warning-session-2026-10-12
Parent: ../map.md
Blocked by: 06

## Question

How should low-battery, missing-telemetry and intrusion warnings be configured, acknowledged, cleared and repeated, including who may change thresholds and how absent/stale data is distinguished from a reported normal condition?

## Comments

2026-10-12 — Created after the owner accepted the Infrastructure page, optional map layer, full telemetry/event history and configurable warnings. Baseline: [Define the dispatch portal MVP](06-dispatch-portal.md). Thresholds should reflect fitted sensors, verified units and expected cadence; do not reuse member GPS's 15-minute cutoff automatically. No alarm policy or numeric thresholds selected. Created unclaimed; prerequisite wired after creation.

2026-10-12 — Owner brought this decision forward. Interview started with configuration/acknowledgment permissions, notification scope, intrusion clearing and threshold policy. Recommendations are proposals awaiting owner answers; no alert behavior selected or implemented. MQTT connectivity investigation remains deferred.

### 2026-10-12 — First round answered

- Admins configure thresholds/disable rules; all registered users may acknowledge. Audit actor/time for changes and acknowledgments. Acknowledgment means seen, not fixed.
- Persistent badges/cards and cross-page portal toasts; no sound for infrastructure alerts, including intrusion. Existing shared-message sound preference is separate.
- Intrusion incidents latch until an admin resolves them with a note. Later normal sensor readings update sensor state without resolving the incident; silence/missing data never clears it.
- Shared rule defaults with per-device overrides. Missing telemetry follows configured reporting cadence; battery thresholds await verified readings/builds, with unconfigured rules explicit.
- Owner emphasizes not all devices have sensors. Apply sensor rules only to configured, supported capabilities; absent sensors are not missing reports or normal readings. Sensor fitment remains to verify.
- Next round covers repeat notifications, health-warning recovery, feed-outage handling and cadence-based missing-telemetry defaults. No numeric battery threshold, incident grouping policy or implementation selected yet.

### 2026-10-12 — Second round answered; consolidated policy awaiting confirmation

- Owner replaced infrastructure toast notifications with persistent badges only: no toasts, sounds, reminders or repeat notifications. Log every event. This supersedes the first-round infrastructure toast choice; shared-message notifications remain separate.
- Low-battery warnings clear automatically on fresh readings meeting a separate recovery threshold; missing-telemetry warnings clear on fresh reports, not old replayed observations. Preserve warning/recovery history.
- On loss of the incoming portal feed, show a prominent feed-outage warning and aging readings; suppress new device-missing notifications and preserve existing warnings/incidents. With badge-only policy, use the feed warning to explain unknown device health rather than generating new device-missing incidents solely from a known feed outage.
- Missing-telemetry default: three expected reporting intervals, configurable per device/report type. An equipped, enabled sensor awaiting its first report starts the timeout when monitoring is enabled. Unsupported sensors show not equipped and do not alert.
- Consolidated summary sent for confirmation. Proposed reconnect rule: allow three expected reporting intervals (or the configured override) after feed restoration before raising a new missing-report warning; require fresh evidence to clear existing warnings. This reconnect rule remains a proposal pending confirmation.
- Intrusion remains a latched incident, distinct from current sensor state. Log all reports; proposed grouping keeps subsequent intrusion reports on the open incident, with the next report after resolution opening a new incident. Grouping remains a proposal pending confirmation.

### 2026-10-12 — Owner confirmed

Owner accepted the consolidated policy, including reconnect grace and intrusion grouping. Added device-configuration battery metadata: type, capacity in mAh and cell count (for example an 18650 pack or a 3000mAh LiPo). Record pack arrangement and whether capacity refers to a cell or the complete pack so the value is unambiguous. This adds a configuration requirement, not confirmed hardware quantities or a runtime estimate.

## Answer

Owner-confirmed policy, 2026-10-12. Requirements only; no warning engine, portal or sensor behavior implemented/tested.

- **Presentation:** persistent infrastructure warning badges/cards only. No infrastructure toasts, sounds, reminders or repeat notifications. Log every incoming event under the pilot retention policy, keeping duplicate receipt evidence distinct from incident counts. Shared-message notifications retain their separate policy.
- **Permissions/audit:** admins configure thresholds, enable/disable rules and resolve intrusion incidents. All registered users may acknowledge alerts. Record actor/time, configuration changes, acknowledgments and resolution notes. Acknowledgment means seen, not recovered or resolved; disabling a rule preserves its history.
- **Capabilities:** apply rules only to configured, supported device/report capabilities. Distinguish not equipped, unconfigured rule, awaiting first reading, current reading and stale reading. Missing or unsupported intrusion data is not an all-clear. Verify sensor fitment before enabling monitoring.
- **Configuration:** shared rule defaults with per-device/report-type overrides and expected reporting cadence. Low-battery trigger and separate recovery thresholds await verified metrics/units and battery builds; no numeric battery values selected. Unconfigured rules are visible.
- **Missing telemetry:** default timeout is three expected reporting intervals, configurable per device/report type. For an enabled capability that has never reported, start the timeout when monitoring is enabled. Fresh reports clear the warning; old replayed reports do not reset freshness or clear it.
- **Health recovery:** low battery clears automatically when fresh evidence reaches its configured recovery threshold. Preserve trigger, acknowledgment and recovery history. No data does not demonstrate recovery.
- **Intrusion:** a reported event opens a latched incident. Further intrusion reports belong to the open incident and every event remains logged. Current sensor state is separate; later normal readings or silence do not resolve the incident. An admin resolves it explicitly with a note. A subsequent intrusion report opens a new incident.
- **Feed outages:** show a prominent feed-outage warning and aging readings; preserve existing device warnings/incidents. Do not create new device-missing incidents solely from a known feed outage. After restoration, allow the configured missing-report timeout (default three expected intervals) before raising new missing warnings. Existing warnings require fresh recovery evidence to clear.
- **Battery metadata addition:** device setup records battery type/chemistry, cell count, nominal capacity in mAh with per-cell versus whole-pack scope, and pack arrangement where applicable (unknown allowed). Examples are illustrative, not installed configurations. Keep declared/rated capacity separate from measured capacity; do not infer remaining charge, charge/discharge current or runtime from metadata alone. Actual device builds, readings, units and cadence remain verification prerequisites.

Implementation checks follow this policy: unsupported/never-reported/stale sensors, trigger/recovery thresholds, acknowledgment versus resolution, repeated intrusion reports and new incidents, replayed/duplicate observations, feed outage/reconnect grace and event/audit preservation. Connectivity investigation remains owner-deferred.
