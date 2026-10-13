# Project brief

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
- Initial scale: roughly 20 member trackers, with as few as 5 for the first trial (owner input on 2026-10-12).
- Tentative GPS target: 5–15 minutes. Whether this means broadcast interval, maximum position age at dispatch, or both remains to be confirmed; this is a starting range, not a tested guarantee.
- Support members who use companion apps and members who operate entirely from the device. Some may use a keyboard-equipped, BlackBerry-style node.
- Provide a web portal/dashboard for dispatch and members to see nodes and status.
- Use a closed private network. The owner reports all participating members consent to tracking and its privacy implications; operational access, retention, and public-content permissions still need definition.
- Evaluate a fork or modification of Meshtastic or MeshCore, especially configurable update frequency. The actual need for code changes remains to be established.
- Document planning, execution, and results; create social media content.
- Track spending and tangible outcomes to support possible grant requests to Clark County / Mount Charleston stakeholders. No funding is awarded or promised.

## Possible backhaul

Some vehicles may provide internet through Starlink or cellular service. One or two repeaters may have internet through the Kyle Canyon and Lee Canyon fire department locations. Member homes in Las Vegas may also connect to a mountain repeater and contribute internet access. These are candidates, with availability, RF paths, and permission unverified.

## Open choices

- Network architecture: the owner said “LoRaWAN” while also naming Meshtastic and MeshCore. Establish whether the intended system is a LoRa mesh, LoRaWAN, or a combination before choosing firmware.
- Pilot terrain/routes, precise dispatch position-age target, mission duration, and acceptable missing-position rate. Initial scale is 5 toward roughly 20 trackers; the owner's GPS starting range is 5–15 minutes.
- Existing hardware models, counts, condition, radio variants, and GPS capabilities.
- Message workflow, display/button needs, and behavior without a phone or internet.
- Site permission, radio configuration/compliance, link coverage, and service access.
- Dispatch data access, track retention, and handling of delayed/stale positions.
- Power sizing, environmental limits, and maintainability.
- Budget ceiling, ownership of equipment, grant applicant, and partners.

## First planning destination

Prepare a small, measurable field pilot using owned hardware: define the participating node set, choose a justified firmware/network approach, sketch how positions reach dispatch, and agree on success criteria. Keep values undecided until evidence or owner input settles them.

The field pilot is a checkpoint toward the full mission, not a claim that the system is ready for operational deployment.
