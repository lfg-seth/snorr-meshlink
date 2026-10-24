# Project brief

SNORR MeshLink supports Search and Rescue on Mount Charleston, Nevada.

## Mission and priorities

1. Passive member GPS tracking for dispatch.
2. Member communications.
3. Later law-enforcement expansion.

Reuse inventoried hardware before proposing purchases. The first destination is
an evidence-backed field pilot, followed by broader deployment when its gates
pass. The [tracker](.scratch/TRACKER.md) owns current work; the
[latest session](records/sessions.md) records the last handoff.

## Confirmed direction

- Passive tracking means power on and automatically report GPS without a phone
  or repeated member interaction. Show position age from the GPS measurement;
  stale at **15 minutes**. Member runtime is **four hours minimum, twelve hours
  target**. These are requirements, not accepted field results.
- Initial scale is roughly 20 members. The planned first trial uses six
  GPS-equipped Heltec V4 member trackers, two selected RAK relays and two Heltec
  V3 backhauls. B001/B002 were the established member bench pair; on 2026-10-24
  the owner reassigns B001 to [replacement gateway G004](docs/operations/g004-v4-gateway.md),
  leaving B002 in the member role. Planned
  purchases/recoveries and 3000 mAh allocations require confirmation in
  [inventory](records/inventory.md). T-Decks are outside the first trial.
- Meshtastic is selected for pilot evaluation; firmware/protocol suitability
  remains subject to measured hardware and field evidence. LoRaWAN, Meshtastic
  and MeshCore are distinct systems. The [decision map](.scratch/pilot/map.md)
  retains selection history and later amendments.
- The pilot data path is member radio → optional RAK relay → Heltec V3 gateway
  → private MQTT → Python ingestion worker → PocketBase → dispatch portal. Preserve GPS
  measurement times, per-gateway receipts and deduplication. Current G001/G002
  are receive-only. The earlier designated-gateway message-downlink design is
  future communications scope; implementing it requires a selected assignment.
- The portal uses React, approachable TypeScript, Vite and MapLibre/USGS layers
  on an Ubuntu Proxmox LXC, with HTTPS through Cloudflare Tunnel. Demo and live
  data stay isolated. [Live MQTT](docs/operations/live-mqtt.md) and
  [portal operations](docs/operations/portal-lxc.md) own deployment details.
- Local command-post and companion-app location viewing must be useful without
  internet. Phone use is optional for tracking; offline maps and stale/missing
  behavior remain acceptance gates. Repeaters/gateways need measured power,
  solar, enclosure and environmental performance before unattended placement.
- Device numbers and assignment history remain independent of mutable radio
  names. [Identity](.scratch/pilot/issues/12-assignment-radio-names.md) and
  [infrastructure warnings](.scratch/pilot/issues/10-infrastructure-warning-rules.md)
  retain their detailed requirements; capability, battery, solar and antenna
  metadata must distinguish known, planned and unknown equipment.

## Releases and project records

[MeshLink application releases](docs/operations/meshlink-releases.md) and
[SNORR Firmware releases](records/firmware-releases/README.md) have independent
versions. The application release JSON owns its version. Firmware development
uses `snorr/develop`; this repository pins published source through `firmware`.
A source pin or product baseline does not establish a device's installed bytes.

Keep `snorr-meshlink` as the repository name. Reviewed source goes to main;
production deployments are manual and explicitly selected. No staging site now.
[Local tracking](docs/operations/local-tracking.md) owns task dispatch, concurrent
work and handoff. GitHub hosts source, CI and useful PRs; historical issues and
the Project board remain unchanged unless requested.

## Boundaries and evidence

Keep secrets, identifiable rosters and raw tracks in ignored `private/` or
`local-data/`; publish sanitized evidence. Member consent and a private network
do not settle operational access, retention, radio compliance or publication
permission. Verify actual radio/antenna settings and site permission before use.
Candidate locations are not installation permission. Track spending and measured
outcomes for potential grants; no funding is promised.

Most public project material should be human-readable and owner-copyedited.
[Content policy](records/content.md#public-documentation-direction---2026-10-23)
owns editorial boundaries; agent internals stay outside site rendering and issue
pages are provisionally excluded. Existing GitHub source publication is
authorized; other publishing and outreach require authorization.

## Deferred wishlist

[Wishlist](records/wishlist.md) work starts only when the owner brings it forward.
Communications/SOS, public-site implementation and UI improvements retain their
existing holds in the tracker. Mentioning or decomposing work does not activate it.

## Possible backhaul

Vehicle Starlink/cellular, fire-department locations and member homes remain
candidates. [Sites](records/sites.md) owns availability, permission and evidence.

## Open choices

The tracker and parent acceptance records own remaining GPS/runtime, relay,
outage, power, release and field gates. Exact devices/routes, acceptable missing
rates, access/retention, operational maintenance and budgets require evidence or
owner decisions. Use the [roadmap](docs/roadmap.md) for acceptance checkpoints.

## First planning destination

Pass the measured pilot gates with owned hardware before expanding deployment.
Implementation, release, native presentation, live delivery, sustained operation
and field acceptance are separate evidence stages.

Dated development details were moved intact to the
[historical brief](records/project-brief-history-20261023.md). Consult it only for
an earlier decision or evidence reference; current status belongs in the tracker.
