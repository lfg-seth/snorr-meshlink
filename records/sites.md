# Candidate sites and backhaul

Updated: 2026-10-12. Candidate entries below are owner-described possibilities. None has verified coverage, permission, or internet availability recorded. Existing deployments are recorded separately.

| ID | Candidate | Possible role | Internet possibility | Permission / feasibility | Next evidence |
| --- | --- | --- | --- | --- | --- |
| SITE-001 | Mountain repeater locations; exact sites TBD | Solar repeater | Unknown | Unverified | Candidate locations and field measurements |
| SITE-002 | Kyle Canyon fire department location | Repeater and backhaul | Possible fixed internet | Unverified | Confirm site, contact, permission, and connection |
| SITE-003 | Lee Canyon fire department location | Repeater and backhaul | Possible fixed internet | Unverified | Confirm site, contact, permission, and connection |
| SITE-004 | Member vehicles | Mobile node and backhaul | Starlink or cellular | Availability unconfirmed | Equipment, power, and representative routes |
| SITE-005 | Member homes in Las Vegas | Fixed node and backhaul | Home internet | RF reach and participation unconfirmed | Identify willing hosts and test mountain link |

Create a separate entry when a specific site is identified. Record hardware IDs, installation/access permission, survey/test IDs, power source, internet availability, and maintenance responsibility. Keep exact private home addresses and sensitive site access details in ignored local records.

## Existing deployments reported by owner

2026-10-12 — Portal hosting constraint: owner confirms the available Proxmox VM is on the local network and wants no inbound router port forwarding. Portal HTTPS remains a Cloudflare Tunnel candidate; remote MQTT transport remains unselected. Evaluate a compatible WebSocket firmware/bridge path or a separate reachable broker with an outbound home connection. No remote endpoint, paid service, gateway-site adapter, or network change approved/deployed.

2026-10-12 — Owner subsequently deferred connectivity investigation. Portal design should assume the local broker works through Cloudflare with stock MQTT clients. This records an explicit planning assumption, not measured reachability or verified compatibility; no network configuration or site permission changed.

2026-10-12 — Owner reports an available Proxmox VM for hosting the private MQTT broker and dispatch portal, with Cloudflare Tunnel proposed for online exposure. This is a hosting candidate, not a deployed service; host resources, network reachability, maintenance/backups, and broker transport remain unverified. Owner proposes one designated V3 for internet-to-LoRa dispatch replies, potentially with V4 MQTT uplinks too; this changes the prior receive-only direction only if agreed in the [portal interview](../.scratch/pilot/issues/06-dispatch-portal.md). No public endpoint or new installation permission recorded.

2026-10-12 — Owner subsequently confirmed the designated-V3 transmit exception in the portal interview. The other V3 stays receive-only. V1 portal outage fallback is local Meshtastic viewing, not a requirement to run the same portal with local ingestion while offline. Source research distinguishes portal HTTPS Tunnel from embedded MQTT TCP reachability; the broker route and gateway-site networking remain unselected.

2026-10-12 — Pilot scope includes owned RAK repeaters and 2 Heltec V3 receive-only internet backhauls. Repeater count, placement, backhaul hosts, internet availability, and installation permissions remain unconfirmed. Inclusion in the pilot does not establish use or readiness of the existing remote RAK deployments.

2026-10-12 — Owner selected 2 undamaged on-hand RAKs for initial relay evaluation; individual units/builds and placement remain unselected. Remote dispatch ingestion will use one private MQTT broker with the 2 receive-only V3 uplinks. Optional member-phone/cellular backhauls are conditional on compatible app proxy behavior and measured multi-gateway results; no member availability, cellular coverage, or additional site permission established. Local app viewing must work without internet backhaul.

- 2026-10-12: 2 RAK units associated with HW-001 remain deployed in remote areas at Mount Charleston. Exact sites, builds, operating status, power configuration, backhaul, and permissions are not recorded. These are separate from the updated 8 RAK units on hand (1 damaged).
- Owner plans recovery when replacement nodes are ready, rather than an immediate remote recovery trip. Replacement readiness and recovery dates remain unset.
- Owner subsequently reports a possible third mountain RAK repeater, or a destroyed unit, as explanations for the unresolved source-list difference. Neither is confirmed; no third deployed unit is counted in planning stock.
- Later inventory update: an additional RAK was found on hand with a broken carrier board. This closes the numerical source-list difference; the earlier third-repeater/destroyed-unit possibility remains unverified. Owner estimates perhaps 4 × 18650 cells per deployed repeater (about 8 total across the 2 reported deployments), separate from 88 cells on hand; deployed counts and condition are unconfirmed.
