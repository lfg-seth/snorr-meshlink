# Define the dispatch portal MVP

Type: grilling
Label: wayfinder:grilling
Status: resolved
Assignee: codex-dispatch-portal-2026-10-12
Parent: ../map.md
Blocked by: none

## Question

What is the smallest useful dispatch portal specification for passive tracking first and shared-channel messaging second, including account access, member/device identity, freshness, history, storage, and operation during backhaul outages?

## Comments

### 2026-10-12 — Owner proposal and interview started

- Plan a responsive portal for mobile, tablet, and computer with Map, Users, and Messages pages. Show current member locations by default, pin details and explicit position age, slower breathing as positions age, and grey stale positions after 15 minutes. History is opt-in and must distinguish measured points from inferred connecting lines.
- Owner has a Proxmox VM available for a broker and portal, proposes Cloudflare Tunnel for online access, and wants simple local username/password account administration using an existing auth engine; PocketBase is a candidate, not a selection.
- Owner intends MQTT on V3 gateways and potentially some V4s. Actual firmware/configuration behavior remains unverified.
- Record all incoming data for possible future use. Owner reports member consent before device issue and instructions for disabling tracking outside use. Retention duration, access, backup, and deletion behavior remain to clarify; raw tracks and member identities stay outside Git.
- Assume one shared channel and no member direct-message workflow. Owner wants inbound messages surfaced and dispatch replies, potentially through one designated V3 internet-to-LoRa gateway. This proposes changing the earlier two-receive-only-backhaul decision; transmit permissions and local/offline behavior need an explicit answer.
- Research underway: [Check portal MQTT hosting and backend options](07-portal-transport-research.md) and [Check dispatch map sources and nonprofit access](08-portal-map-research.md).
- Planning only; no service provisioned, backend chosen, account created, or content published. Interview awaits owner decisions.

### 2026-10-12 — Proposed distinctions for the interview

- Separate a tracked member, their physical member node, and a portal login account. Device lending/reassignment must not silently attribute historical tracks to the device's latest holder. The Users page naming and fields depend on this distinction.
- Position age means measurement age, not time since broker receipt or last radio contact. Unknown/invalid GPS timestamps must be explicit; a replayed older observation must not move the current pin backward in time or make it fresh. Proposed details show measured time, received time, and last contact separately.
- Breathing is an optional freshness cue, backed by visible age and a legend; avoid implying heartbeat proves movement or safety. Propose reduced-motion support and distinct never-seen/unknown-position states. Exact fresh/aging ranges remain undecided; the existing stale threshold is 15 minutes.
- Connecting known history points is interpolation/visual connection, not proof of the route walked. Propose visible recorded points, dashed connections, time-gap labels, and a warning for sparse data. Do not invent additional recorded measurements or snap the member to a trail without a separate justified feature.
- “Record everything incoming” can cover every broker receipt, including duplicates and unrecognized packet types, while normalized member observations drive the UI. It cannot reconstruct packets no gateway/broker ever received. Queue/reconnect limits require testing; proposed delivery statuses distinguish queued, submitted to gateway, radio evidence when available, and unconfirmed human receipt.
- Round-one questions sent: offline portal versus local-app fallback; account access/admin registration; one designated transmit gateway; retention intent; device reassignment.

### 2026-10-12 — Transport research returned

- [Transport/backend findings](../../../docs/research/dispatch-portal-transport.md) establish that Cloudflare HTTPS Tunnel suits the browser portal, but ordinary embedded MQTT TCP cannot directly use a public TCP Tunnel route requiring client-side cloudflared. Broker access needs a separately selected path.
- PocketBase is a plausible pilot candidate for built-in accounts/admin, records, and realtime; MQTT ingestion still requires a worker. Its documented pre-1.0 production-critical limitation means operational dependency and maintenance tolerance must inform selection.
- The documented JSON text-command mechanism needs a technical `mqtt` channel on the designated gateway, though broadcasts can target the single operational primary channel. This does not require user-facing channel selection; release-specific configuration still needs verification.
- [Map-source findings](../../../docs/research/dispatch-portal-maps.md) recommend evaluating MapLibre with USGS topo/aerial services. Nonprofit programs are application-based rather than presumed entitlements; actual AO imagery age, close zoom, and offline availability remain to test.

### 2026-10-12 — Owner answers, first round

- Internet loss: use local Meshtastic fallback for v1; the same portal need not provide fresh offline/local ingestion in this version. Remote position age and feed-outage status must remain clear.
- Access: all registered users may have full operational access to locations, history, and messages. Separate account/deletion administration remains to clarify; no public registration agreed.
- Messaging gateway: one designated V3 may transmit portal replies. This supersedes the earlier strictly receive-only requirement for that V3; the other V3 remains receive-only/uplink-only. Additional V4 uplinks do not imply additional downlink permission. Installed firmware/configuration and RF behavior remain untested.
- Retention: retain all pilot data and review retention before wider rollout; no automatic rolling deletion or indefinite post-pilot policy selected.
- Assignment: devices can be labelled numerically and assigned to a user in the portal by dispatch/admin or claimed by the signed-in user. Proposed dated assignments preserve historical identity. Conflict handling, release, and member/device cardinality remain open.
- Round two asks: occupied-device transfer rules; initial freshness bands; history window/long gaps; offline message drafts/queues; account/archive administration.

### 2026-10-12 — Owner answers, second round

- Self-claim only unassigned devices; dispatch/admin transfers occupied devices. Keep dated assignment history, allow release, and never silently rewrite old track attribution.
- Initial position-age bands: under 2 minutes fast breathing; 2–5 minutes slow; 5–15 minutes very slow; at 15 minutes grey/no breathing. Always show age, separate last contact, and explicitly show unknown GPS age. No known position means list-only, not an invented map pin.
- History opens at the last 4 hours with a range selector, visible measured points/timestamps, dashed estimated connections, and line breaks across gaps longer than 15 minutes.
- Gateway outage: keep unsent draft, do not automatically queue/resend in v1, and require manual send after reconnect. Broadcast delivery remains unconfirmed without additional evidence; broker publish is not a member acknowledgment.
- Admins manage accounts and archive deletion; all registered users have full operational map/history/message access. Admin-created username/password accounts; no public registration.
- Third round asks: member/device list and unassigned pins; in-portal versus background alerts; author identification over the shared gateway; broker-network reachability; pilot stack evaluation.

### 2026-10-12 — Owner answers, third round

- Users lists members with an unassigned-device section and one active member per tracker/one active tracker per member. Reporting unassigned trackers appear on the default member map under their device numbers; fixed RAK/V3 infrastructure does not appear there by default.
- In-portal shared-message toast/unread badge on any page, optional sound, chronological Messages page; closed-browser background push is not required in v1.
- Outbound shared-channel radio text is prefixed with the sender's short display name; the authenticated author is recorded separately. Exact selected-firmware payload limit remains an implementation check.
- Evaluate PocketBase plus a separate MQTT worker, MapLibre, and free USGS topo/aerial layers for the pilot. This approves evaluation, not an operational backend or provider guarantee.
- Owner asks why a Cloudflare Tunnel on the broker VM plus `mqtt.spp.lol` cannot be entered directly on the Heltec. Broker reachability remains unanswered: explain DNS names versus raw MQTT transport and Cloudflare's client-side adapter requirement before asking for network details.
- Clarified that `mqtt.spp.lol` can be a broker hostname; standard Tunnel TCP requires a client-side cloudflared adapter, which is absent from the reviewed stock MQTT path. Alternatives are a reachable DNS-only MQTT TLS endpoint, site networking/bridge, or evaluated MQTT-over-WebSockets support with an HTTP Tunnel route. Asked whether the VM is local and router port forwarding is available/wanted. No route selected or endpoint created.

### 2026-10-12 — Hosting constraint clarified

- Owner confirms the Proxmox VM is on the local network and does not want inbound router port forwarding. Exclude the direct home-broker port-forward proposal.
- Keep portal HTTPS exposure through Cloudflare Tunnel. For remote MQTT, compare a WebSocket-capable firmware/client path through an HTTP Tunnel route, a gateway-site bridge/network adapter, or a separate reachable private broker to which the home worker/broker connects outbound. The last option adds an external service and does not meet a strict all-home-hosting requirement; do not presume budget or provider approval.
- Native Heltec firmware WebSocket suitability is a research prerequisite, not a promised small change: [Check Heltec MQTT over WebSockets for Tunnel hosting](09-heltec-websocket-research.md).

### 2026-10-12 — Owner defers networking

- Owner does not want more connectivity investigation now. For portal planning assume the locally hosted MQTT broker works through Cloudflare with stock MQTT clients.
- This is an owner-requested working assumption, not verified technical support. Preserve the source findings and revisit the route before real gateway connectivity/deployment validation; do not reopen it during the current portal interview.
- Stopped the transport research agent and released the deferred WebSocket research claim. Portal behavior can be specified against a reachable broker interface independently of the eventual connection mechanism.

### 2026-10-12 — Infrastructure addition agreed

- Owner accepted the baseline with repeaters/backhaul devices viewable by role, recorded battery charge/discharge and solar information, and weather/intrusion readings where equipped.
- Owner selected a fourth Infrastructure page with device cards/details, telemetry charts/event log, plus an optional infrastructure map layer.
- Owner selected configurable low-battery/missing-telemetry warnings and reported-intrusion alerts. Infrastructure freshness follows expected telemetry cadence rather than the member-GPS cutoff. Unsupported, never-reported and stale readings remain distinct; no report is not an all-clear.
- All incoming infrastructure telemetry/events follow the agreed pilot retention policy. Sensor fitment, firmware support and exact thresholds remain implementation/evidence prerequisites, not confirmed hardware capabilities.
- Resolved the consolidated portal requirements direction below. MQTT connectivity remains parked by the owner. Detailed thresholds, acknowledgment/clearing and repeat-alert policy are a [follow-up decision](10-infrastructure-warning-rules.md).

## Answer

2026-10-12 — Device-setup addition requested by owner: record solar-panel configuration, with its fields/options to be determined later; record antenna configuration, including Muzi whip and fiberglass choices and an explicit unknown/unconfigured state. These fields describe each device's configured hardware, not new stock, verified solar output or measured antenna performance.

2026-10-12 — Owner-confirmed [infrastructure warning policy](10-infrastructure-warning-rules.md) completes the warning follow-up below: badges only, no infrastructure toasts/sounds/repeats, capability-specific timing, recovery and intrusion resolution. Device setup also records battery type/chemistry, cell count and nominal mAh capacity with per-cell/pack scope and pack arrangement where applicable; unknown values remain explicit. These are configuration metadata, not verified remaining charge/runtime.

Owner-agreed portal baseline, 2026-10-12, consolidated from the interview and accepted infrastructure addition. This resolves requirements direction, not implementation readiness. Connectivity investigation is explicitly deferred by the owner.

- **Scope:** responsive Map, Users, Messages, and Infrastructure pages for mobile/tablet/computer. Passive tracking is the first priority; future SOS-specific/device workflow remains a separate effort.
- **Access:** admin-created local username/password accounts. Every registered user can view current locations/history/shared messages/infrastructure health and send. Admins manage accounts and archive deletion. No public registration or member direct messages in v1.
- **Map:** latest known measured position per member tracker by default. Click/tap opens member/device detail, explicit measurement age, and separate last contact. Under 2 minutes fast breathing; 2–5 minutes slow; 5–15 minutes very slow; at 15 minutes grey/no breathing. Unknown measurement age is explicit; never-seen positions stay in the list. Unassigned trackers with known positions appear by device number. Fixed RAK/V3 infrastructure is omitted from the default member map.
- **History:** opt-in per member, initially last 4 hours with a time-range selector. Recorded points and timestamps remain inspectable; dashed connections are estimates, not proven routes. Break connections across gaps longer than 15 minutes. Late/duplicate packets do not freshen the latest pin or overwrite a newer measurement.
- **Users/devices:** stable numeric labels, one active member per tracker and one active tracker per member. Users may claim an unassigned device or release their own. Dispatch/admin transfers occupied devices. Preserve dated assignments so reassignment does not silently relabel historical tracks.
- **Radio naming amendment:** owner subsequently chose static short names tied to device numbers. See [Choose assignment-driven radio names and identity](12-assignment-radio-names.md) for the assignment/long-name workflow and remote-update confirmation requirements.
- **Infrastructure:** repeaters/backhaul devices remain viewable by role on a dedicated page with cards, detail/history charts and event log, plus an optional map layer where location is known. Show battery level/voltage, charging/discharging information, solar measurements, weather and intrusion events as available from installed hardware and verified firmware. Label reported values versus calculated/inferred trends, units, measurement/receipt times and data age. Solar electrical output and light intensity are separate readings. A battery-percent trend is not confirmed charge current or external-power state. Distinguish unsupported sensors, no reading yet, stale readings and current readings.
- **Infrastructure warnings:** configurable low-battery and missing-telemetry warnings plus reported-intrusion alerts in the portal. Freshness thresholds follow each device's expected telemetry cadence, not the member-GPS cutoff. Missing intrusion reports are not “no intrusion.” Exact thresholds, acknowledgment/clearing and repeat-notification rules remain a follow-up decision.
- **Messages:** one shared operational channel, chronological log, in-portal toast/unread badge across pages, optional sound. Closed-browser push is deferred. All portal users send through one designated V3, prefixing radio text with their short display names and recording authenticated authors. Other gateways remain uplink-only for this workflow. No automatic outage queue/resend: retain drafts and require deliberate sending after reconnection. Broker publication is not member receipt.
- **Data:** retain all incoming pilot data, including infrastructure telemetry/sensor/intrusion events and duplicate receipt evidence, with deduplicated member positions/messages and infrastructure observations for display. Infrastructure histories remain inspectable rather than storing only the latest readings. Review retention before wider rollout. Raw tracks, member identities, credentials, and backups remain outside Git. Packets never received cannot be reconstructed.
- **Hosting/evaluation:** local Proxmox VM, no inbound router port forwarding, portal HTTPS through Cloudflare Tunnel. Evaluate PocketBase plus a separate MQTT worker and MapLibre with USGS topo/aerial layers. At the owner's request, assume a working Cloudflare connection from stock MQTT clients to the local broker for portal design; actual compatibility and transport selection are explicitly deferred and unverified.
- **Outages:** local Meshtastic command-post/member viewing is the v1 fallback; a locally running copy of the same portal is not required. Display aging data/feed outages clearly.
- **Before implementation:** confirm transport and pinned firmware/packet formats, evaluate map coverage/imagery age/zoom and mobile browser behavior, establish message length/evidence/expiry controls and backup/recovery procedures. Inventory fitted infrastructure sensors and verify available metrics/units, power/solar measurement points and intrusion report format. These are verification prerequisites, not passed tests or additional purchases.

Primary-source capability check: Meshtastic documents device/environment/power telemetry and GPIO detection messages, but does not establish sensor fitment or reliable charging/solar/intrusion behavior on the owner's builds. [Telemetry](https://meshtastic.org/docs/configuration/module/telemetry/), [Detection sensor](https://meshtastic.org/docs/configuration/module/detection-sensor/). No hardware, telemetry ingestion, alert rules or UI implemented/tested; no commit or deployment.
