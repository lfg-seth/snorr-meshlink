# Choose the pilot network and firmware approach

Type: grilling
Label: wayfinder:grilling
Status: resolved
Assignee: pilot-approach-session-2026-10-12
Parent: ../map.md
Blocked by: 01, 02, 03

## Question

Given the owned hardware, agreed pilot needs, and protocol comparison, which network and firmware should the pilot use, and can configuration satisfy the required GPS behavior before a fork is necessary?

## Completion evidence

An owner-agreed approach that names usable hardware, identifies configuration versus code changes, and records the assumptions to verify on the bench. Sketch how dispatch receives positions without designing the whole portal yet.

## Comments

2026-10-12: Blocked by the first-pass inventory, pilot requirements, and protocol research. Dependencies wired after initial ticket creation.

2026-10-12: Claimed after all three prerequisites resolved. Scope is 6 planned GPS-equipped Heltec V4s only, 15-minute stale indication with visible measurement age, 4-hour minimum runtime / 12-hour target, and passive tracking after power-on. Checking current official firmware/hardware documentation before asking the owner to choose the pilot approach. Firmware choice and dispatch path remain undecided; no bench tests performed.

2026-10-12 — Current primary-source check for the first interview round:

- Meshtastic documents [Heltec V4 support](https://meshtastic.org/docs/hardware/devices/heltec-automation/lora32/); original V4 and V4-R8 require different build targets. Exact owned revision and GPS wiring remain unverified.
- Existing [position settings](https://meshtastic.org/docs/configuration/radio/position/) separate GPS acquisition, periodic transmission, movement-based broadcasts, and GPS solution timestamps. This supports a configuration-first bench evaluation, not a guarantee of achieved freshness or runtime.
- A [custom MQTT broker](https://meshtastic.org/docs/configuration/module/mqtt/) and [position-packet ingestion](https://meshtastic.org/docs/software/integrations/mqtt/) provide a possible dispatch path. One-hour-minimum map reports are distinct from tracking packets; measurement time must remain distinct from gateway receipt time.
- MeshCore's [FAQ](https://docs.meshcore.io/faq/#24-q-how-often-do-adverts-get-sent) describes user-initiated companion advertisements. Autonomous member GPS reporting remains build-specific and unverified.

Recommendation awaiting owner decision: evaluate stock Meshtastic on the V4 pilot first, using configuration before considering a fork. Ask the firmware choice first; dispatch-path decisions follow once that prerequisite is settled.

2026-10-12 — Owner clarified infrastructure scope: the 6 V4s are member trackers, not the complete pilot network. Include owned RAK repeaters (quantity and exact builds open) and 2 owned Heltec V3s as receive-only internet backhauls. Verify compatibility across all three hardware groups, RAK relay behavior, and V3 radio silence while forwarding received positions to dispatch. Radio silence includes any automatic advertisements, acknowledgments, telemetry, rebroadcasts, and internet-to-radio traffic; do not assume a role name proves silence. Select on-hand RAKs for inspection; exclude the damaged unit until repaired and verified, and do not assume the 2 remote deployments are available or working. Sites, internet transport, and multi-backhaul ingestion remain open.

2026-10-12 — Owner accepted Meshtastic as the initial firmware evaluation path (Q1), while expecting modifications will likely be needed. This is not agreement that stock firmware will meet every requirement. Refreshed the resolved requirements ticket: evaluate V4 tracking, owned RAK relays, and 2 strictly receive-only V3 internet backhauls together. Checking transmit-disable behavior and internet uplink compatibility before proposing that configuration. Next decisions: the owner's anticipated modification needs and whether the pilot requires local dispatch viewing during loss of all internet backhaul. Exact RAK count/build selection remains open.

2026-10-12 — Owner expects GPS-related modifications and requested review of ahead commits in the [old firmware fork](https://github.com/lfg-seth/firmware). Review in progress; no old change selected for reuse yet. Owner confirmed local command-post viewing and other-member location viewing through companion apps without internet backhaul. Updated the requirements answer and planned field criteria; phones remain optional for automatic member tracking. Local connection architecture and offline map behavior remain open.

Primary-source follow-up: [LoRa TX disable](https://meshtastic.org/docs/configuration/radio/lora/#transmit-enabled) is distinct from CLIENT_MUTE forwarding behavior. Upstream [radio code](https://github.com/meshtastic/firmware/blob/master/src/mesh/RadioLibInterface.cpp), [received-packet handling](https://github.com/meshtastic/firmware/blob/master/src/mesh/Router.cpp), and [MQTT code](https://github.com/meshtastic/firmware/blob/master/src/mqtt/MQTT.cpp) support evaluating receive-only V3 MQTT uplinks with `tx_enabled=false`; this is a source inference on moving upstream code, not tested compatibility. Valid region, matching channel/key, uplink settings, continued Wi-Fi availability, reboot/reconnect silence, and outage queue limits need pinned-build checks. RAK support depends on the actual [core modules](https://meshtastic.org/docs/hardware/devices/rak-wireless/wisblock/core-module/), which remain unidentified.

Offline viewing source check: official [Android maps](https://meshtastic.org/docs/software/android/user/map-and-waypoints/) and [Apple maps](https://meshtastic.org/docs/software/apple/user/map/) document received node locations and offline map downloads. Use the matching private primary channel/key and explicitly verify [position precision settings](https://meshtastic.org/docs/configuration/radio/channels/). App presence/online indicators are not the agreed 15-minute measurement-age indication. The [web client](https://meshtastic.org/docs/software/web-client/) supports local radio connections, but offline page loading and basemap rendering are not established by that overview. Bench/field checks must include internet-disabled app startup, map availability, fresh positions, and stale data behavior on the chosen app versions. No command-post app or transport selected yet.

2026-10-12 — Completed [old firmware fork audit](../../../docs/research/old-firmware-fork.md): reviewed all 17 ahead commits (including 2 merges), against pinned fork/upstream heads; fork is 1,887 behind. No ahead commit changes the GPS driver or position algorithm. Active preferences configure 600-second acquisition and 1,800-second position broadcasts; stationary reporting needs revision for the freshness goal. Surviving source changes mainly concern MQTT map precision/defaults and RAK RGB hardware. Precision 32 leaves an invalid coordinate shift expression, so that override should not be transplanted unchanged. Removed provisioning scripts and reverted forced environmental telemetry are historical, not active head behavior. No ahead change implements the required V3 silence, local viewer, or offline member viewing. Recommendation: recover specific behavior goals on a selected current release and evaluate received position-packet ingestion; source/build/bench work remains necessary before selecting code changes. Local viewer platform/connection and RAK subset remain owner decisions; ticket stays claimed.

2026-10-12 — Owner chose both app and laptop/portal viewing, with the Meshtastic app acceptable for the first local-viewing MVP. Owner has a rugged Dell laptop/tablet running Linux available in the field (HW-033); exact compatibility remains to verify. Owner accepted 2 undamaged, on-hand RAKs for initial relay evaluation, subject to identifying cores and verifying operation. No stock counts or equipment readiness inferred from allocation.

## Approach summary for final agreement

- Meshtastic is the initial mesh/firmware evaluation path for 6 planned GPS V4 member trackers, 2 undamaged on-hand RAK relays, and 2 owned V3 LoRa receive-only internet backhauls. Use an identified current release/build, then isolate GPS behavior gaps; the old fork is a behavior reference, not a selected deployment image.
- Members track automatically after power-on. Companion apps provide optional local member-position viewing; local command-post viewing starts with the Meshtastic app. Prepare offline maps and verify freshness indication. Laptop/portal viewing follows, using the owned rugged Linux Dell where compatible.
- Proposed remote dispatch path, awaiting owner agreement: received position packets from either V3 uplink to one private MQTT broker and dispatch ingestion/viewer. Preserve GPS measurement time and gateway receipt time, deduplicate packets, and show stale data during outages. Keep internet-to-LoRa traffic disabled for the receive-only V3s. Do not use the gateway's own MQTT map reports as member tracking ingestion.
- Bench prerequisites: identify V4 revision/GPS wiring, RAK cores/radio variants, V3 variants, app platform/connection and effective radio settings. Verify LoRa silence through reboot/reconnect, local offline viewing, stationary/moving fresh reporting, duplicates/outage recovery, and 4-hour minimum/12-hour target runtime. Exact settings, routes, acceptance rates, site permissions, and any needed code changes remain subsequent implementation/test work.

Awaiting final agreement on this summary and the proposed private MQTT ingestion path; ticket remains claimed. No implementation, hardware tests, or deployment performed.

2026-10-12 — Owner accepted the private MQTT position-packet ingestion path from both V3s. Owner also proposed advanced members' paired companion apps with cellular service as optional additional backhauls, conditional on avoiding problems from too many uplinks. Evaluate this as a staged extension after the 2-V3 baseline, not a requirement that every member backhaul. Checking current client-proxy, duplicate, and downlink behavior before finalizing the approach answer.

2026-10-12 — Completed [multi-backhaul capability check](../../../docs/research/multiple-backhauls.md). Android/Apple proxy paths are documented, but exact app/version and phone background behavior need testing. Additional uplinks create duplicate internet deliveries; use origin-node/packet identity with bounded deduplication and preserve gateway evidence. Keep downlink disabled on all tracking gateways. No safe maximum gateway count established. Owner's conditional option is retained: two-V3 baseline, one phone trial, then a small group only if measured behavior remains acceptable. Resolved the approach decision after owner agreement; this does not establish bench success or operational readiness.

## Answer

2026-10-12 — Portal-interview amendment: the owner subsequently authorized one designated V3 to transmit portal-originated shared-channel replies; the other remains receive-only. This supersedes the strictly receive-only requirement for that designated V3 in the original answer below. Follow the [dispatch portal interview](06-dispatch-portal.md) for command workflow and access rules; hardware/configuration verification remains required. Preserve the original answer as the historical baseline.

Owner-agreed pilot approach, 2026-10-12:

- **Network/firmware:** evaluate a Meshtastic LoRa mesh using an identified current release/build. Start from supported configuration and identify specific GPS gaps requiring code changes. The owner expects GPS modifications may be needed; stock sufficiency is not presumed. The [old fork audit](../../../docs/research/old-firmware-fork.md) informs behavior goals, not a wholesale old-fork deployment.
- **Hardware:** 6 planned GPS-equipped V4 member trackers with intended 3000mAh batteries (2 on hand, 2 purchases and 2 recoveries pending); 2 undamaged on-hand RAKs selected for relay evaluation after core/operation checks; 2 of the owned V3s as LoRa receive-only internet backhauls. Exact units/builds are unassigned and unverified. T-Decks, damaged RAK, and deployed remote RAKs are excluded from this initial set.
- **Local viewing:** automatic phone-free member tracking; optional companion-app viewing of other members' radio-received positions without internet. Meshtastic app is acceptable for the first command-post viewing MVP. Both app and laptop/portal viewing are intended; the owned rugged Linux Dell (HW-033) is available, compatibility unknown. Verify offline maps and measurement-age/stale behavior rather than relying on app online indicators.
- **Remote dispatch:** either V3 forwards received member position packets to one private MQTT broker feeding dispatch ingestion/viewing. Preserve GPS measurement and per-gateway receipt times; deduplicate by origin/packet identity within a bounded window, retain gateway evidence, and never refresh old positions merely because they arrived again. Gateway map reports are not the tracking feed. Use a verified packet format; current docs conflict on JSON availability, so protobuf ingestion is a candidate for release-specific evaluation.
- **Optional member backhaul:** advanced members with a compatible paired app and cellular service may contribute uplinks after the 2-V3 baseline, conditional on successful multi-gateway evaluation. Start with one phone, then expand only after measuring freshness, completeness, duplicates, load, stability, and reconnect/background behavior. Keep internet-to-LoRa downlink disabled across tracking gateways. No supported maximum gateway count or guaranteed phone forwarding established; see [multiple-backhaul findings](../../../docs/research/multiple-backhauls.md).
- **Bench gates:** identify exact V4/GPS, RAK core/radio and V3 builds; pin firmware/app versions; test passive fresh stationary/moving reporting, both V3s' LoRa silence through reboot/reconnect, duplicate/outage handling, internet-independent local viewing, 15-minute stale indication, and 4-hour minimum/12-hour target runtime. Verify radio configuration/compliance before transmission and permissions before installation. Exact GPS intervals/movement/power modes, local connections, field routes, delivery acceptance rates, and code changes remain implementation/test-planning work.

This resolves the approach selection only. No broker/portal deployed, firmware built/flashed, hardware tested, purchase made, radio settings approved, or site permission established. No commit requested or made.
