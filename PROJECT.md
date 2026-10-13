# Project brief

Project name: **SNORR MeshLink** — Search and Rescue Tracking & Communications. Repository: [lfg-seth/snorr-meshlink](https://github.com/lfg-seth/snorr-meshlink). The owner authorized GitHub publication and pushing every completed commit on 2026-10-12.

Recorded from the project owner's instructions on 2026-10-12.

## Mission and priorities

Support SNORR Search and Rescue operations on Mount Charleston, Nevada.

1. Attach a passive GPS tracker to every member so their location can be available to dispatch.
2. Provide a device that helps members communicate.
3. Explore later expansion to law enforcement communications.

## Confirmed direction

- Design and install repeaters; design and distribute member client nodes.
- Inventory the owner's significant existing hardware supply and use it before buying more.
- Repeaters are intended to use solar power and 18650 batteries. Specific pack, charging, protection, and weather designs remain open.
- Every member node is intended to have dedicated GPS.
- Initial scale: roughly 20 member trackers. First-trial plan: 6 Heltec V4s only (2 on hand, 2 planned purchases, 2 planned recoveries), each intended to have GPS and a 3000mAh battery. T-Decks are excluded to reduce device/firmware complexity. Planned additions are not yet confirmed available or working.
- Pilot infrastructure also includes 2 owned RAK repeaters (exact units/builds to select) and 2 owned Heltec V3 internet backhauls. Initially both were receive-only; the portal interview now authorizes one designated V3 to transmit portal-originated replies, with the other remaining receive-only. V4-only applies to member trackers. Verify forwarding and the required transmit/silence behavior under the selected firmware/configuration.
- Initial relay evaluation will use 2 undamaged, on-hand RAKs, subject to core identification and bench verification. Both app and laptop/portal viewing are intended; the Meshtastic app is acceptable for the first local-viewing MVP. An owned rugged Dell laptop/tablet running Linux is available for field use, with compatibility unverified.
- Dispatch stale-position threshold: 15 minutes since GPS measurement, with an obvious stale indication and visible position age. Prefer aggressive broadcasting initially and tune based on measured congestion; exact intervals and movement/power-based modes remain for evaluation. These are requirements and preferences, not tested guarantees.
- Member battery runtime: minimum 4 hours, target 12 hours. Consider larger batteries if runtime tests justify them; no additional battery purchase specified.
- Passive-tracking MVP: power on and automatically broadcast GPS without a phone or repeated member interaction. Device-only SOS is deferred to a future issue.
- Support members who use companion apps and members who operate entirely from the device. Some may use a keyboard-equipped, BlackBerry-style node.
- Provide a web portal/dashboard for dispatch and members to see nodes and status.
- Member tracker radio short names stay tied to device numbers across carrier changes. Keep portal device identity/assignment history separate from names and remote-update success; [naming decision](.scratch/pilot/issues/12-assignment-radio-names.md). Remote admin integration is planned, not implemented/tested.
- Portal baseline has Map, Users, Messages, and Infrastructure pages. Repeaters/backhaul devices are viewable by role with an optional map layer, recorded battery charge/discharge and solar information, weather/intrusion readings where equipped, and configurable health/intrusion warnings. Actual sensors, measurable values, telemetry cadence and warning thresholds remain to verify/define; retain all received infrastructure observations under the pilot-data policy.
- Infrastructure warning behavior is [agreed](.scratch/pilot/issues/10-infrastructure-warning-rules.md): silent persistent badges, sensor-capability-specific rules, default missing timeout of three expected reporting intervals, automatic health recovery and admin-resolved intrusion incidents. Device setup records battery type/chemistry, cell count, nominal mAh capacity and per-cell/pack scope, plus pack arrangement where applicable. Actual battery thresholds and fitted sensors/readings remain to verify.
- Device setup also records solar-panel configuration (options to be determined later) and antenna configuration, including Muzi whip or fiberglass, with unknown/unconfigured values explicit. These are configuration records; panel output and antenna performance remain unverified.
- Portal pilot evaluation: PocketBase with a separate MQTT worker and MapLibre/USGS topo/aerial layers; host on the owner's local Proxmox VM with no inbound router port forwarding. Cloudflare Tunnel is intended for portal HTTPS. Owner has deferred MQTT connectivity investigation; for portal planning assume stock MQTT clients can reach the local broker through Cloudflare. This is a working assumption, not verified compatibility.
- Pilot remote dispatch path: both V3 backhauls forward received member position packets to one private MQTT broker for dispatch ingestion, preserving measurement times and handling duplicates. Permit dispatch-message downlink only through one designated V3; keep other tracking uplinks from accepting internet-to-LoRa commands. Companion-app/cellular member backhauls are an optional extension only after compatibility and multi-gateway testing show acceptable behavior.
- Pilot viewing must remain available locally at the field command post without internet backhaul. Members who use the companion app must also be able to see other members' received locations in the field without internet backhaul; phone use remains optional for passive tracking. Offline map availability and missing/stale-position behavior need verification.
- Use a closed private network. The owner reports all participating members consent to tracking and its privacy implications; operational access, retention, and public-content permissions still need definition.
- Evaluate a fork or modification of Meshtastic or MeshCore, especially configurable update frequency. The actual need for code changes remains to be established.
- Document planning, execution, and results; create social media content.
- Track spending and tangible outcomes to support possible grant requests to Clark County / Mount Charleston stakeholders. No funding is awarded or promised.

## Deferred wishlist

The [feature wishlist](records/wishlist.md) records known-Wi-Fi automatic MQTT backhaul and browser-based flashing of project firmware for a small supported subset of member-owned devices. Both are parked until the owner explicitly brings them forward; no research or implementation is scheduled.

## Possible backhaul

Some vehicles may provide internet through Starlink or cellular service. One or two repeaters may have internet through the Kyle Canyon and Lee Canyon fire department locations. Member homes in Las Vegas may also connect to a mountain repeater and contribute internet access. These are candidates, with availability, RF paths, and permission unverified.

## Open choices

- Network architecture: the owner said “LoRaWAN” while also naming Meshtastic and MeshCore. Establish whether the intended system is a LoRa mesh, LoRaWAN, or a combination before choosing firmware.
- Pilot terrain/routes, field-test duration, acceptable stale/missing-position rate, and exact reporting settings. Trial scope is 6 GPS-equipped Heltec V4s after 2 purchases and 2 recoveries, each intended to use a 3000mAh battery. Stale threshold is 15 minutes; runtime minimum is 4 hours with a 12-hour target.
- Current hardware counts, condition, radio variants, and GPS capabilities. A 32-row historical purchase list is imported in [Inventory](records/inventory.md); the owner reports most items are retained, but quantities are not yet confirmed.
- Message workflow, display/button needs, and behavior without a phone or internet.
- Site permission, radio configuration/compliance, link coverage, and service access.
- Dispatch data access, track retention, and handling of delayed/stale positions.
- Power sizing, environmental limits, and maintainability.
- Budget ceiling, ownership of equipment, grant applicant, and partners.

The initial [protocol baseline](docs/research/protocol-baseline.md) records official-source findings and configuration options. It supports a bench evaluation after inventory; it does not settle firmware selection or prove that a fork is required.

## First planning destination

Prepare a small, measurable field pilot using owned hardware: define the participating node set, choose a justified firmware/network approach, sketch how positions reach dispatch, and agree on success criteria. Keep values undecided until evidence or owner input settles them.

The field pilot is a checkpoint toward the full mission, not a claim that the system is ready for operational deployment.
