# Define useful tracking for the first field pilot

Type: grilling
Label: wayfinder:grilling
Status: resolved
Assignee: pilot-needs-session-2026-10-12
Parent: ../map.md
Blocked by: none

## Question

For a small first pilot, what member count, acceptable position age, mission duration, and device-only workflow would demonstrate useful passive tracking to dispatch?

## Completion evidence

Owner-agreed requirements and explicit remaining unknowns. Start with member count and acceptable position age; discuss duration and the standalone workflow next. Do not settle targets on the owner's behalf.

## Comments

2026-10-12 — Pilot requirements session: owner requested work on this ticket. Claimed for a short requirements interview, starting with pilot size and maximum dispatch position age. Current inventory records four GPS-equipped on-hand devices; five trackers remain a possible target with hardware readiness unresolved. Awaiting owner decisions; no acceptance thresholds settled on the owner's behalf.

2026-10-12: Requested rough pilot member count and maximum useful GPS position age. No numerical requirements agreed yet.

2026-10-12 — Owner response: “20ish client device trackers. as little as 5 to start. GPS: 5-15min?” Record 5 as a possible first-trial size, roughly 20 as the initial rollout scale, and 5–15 minutes as a tentative GPS range. Clarify broadcast interval versus dispatch position age when defining field acceptance criteria. Mission duration and routes remain open; this ticket is not resolved.

2026-10-12 — Owner pilot direction:

- Plan to order 2 more Heltec V4s and recover 2 member-held Heltec V4s, all with GPS and 3000mAh batteries. Together with the 2 V4s on hand, this is a planned pool of 6 V4s; whether the 2 T-Decks join the same trial remains open. Planned units are not confirmed available stock, and no purchase was reported.
- The earlier GPS range concerns stale position age at dispatch, not broadcast interval. An exact stale cutoff within/beyond that tentative range still needs explicit agreement.
- Begin with aggressive reporting and dial back when network saturation is observed. Initial interval and measurable congestion criteria remain for configuration/bench evaluation; this is not evidence that saturation has occurred or a requirement to degrade operational traffic.
- Consider plugged-in versus battery reporting modes and movement-based rebroadcast thresholds. These are evaluation options, not verified firmware features or settled algorithms. A stationary node still needs a way to demonstrate fresh tracking; heartbeat cadence and GPS measurement cadence remain open.

Next interview round: exact stale cutoff, unplugged runtime target, and minimum device-only workflow. Confirm final participating device count before resolving. Firmware choice remains in its separate ticket.

2026-10-12 — Owner-agreed requirements:

- Dispatch must make stale locations easy to distinguish and show how stale they are. Agreed stale threshold: 15 minutes of position age, measured from the GPS measurement time rather than dispatch receipt time.
- Battery runtime: minimum 4 hours; target 12 hours. Larger batteries may be purchased if testing supports that need; no size, quantity, price, or purchase agreed.
- MVP workflow: power on and begin automatic GPS broadcasting, without a phone or repeated member interaction.
- A single-button/combination or press-and-hold distress action is a future possibility, explicitly deferred to [Define a future device-only SOS workflow](05-sos-workflow.md); SOS is not an MVP requirement.

Pending final shared-understanding check: whether the intended first trial is the 6 planned V4s alone or also includes the 2 T-Decks. Routes, exact reporting/movement settings, congestion criteria, and acceptable stale/missing-position frequency remain explicit implementation/test-planning unknowns. No requirement for uninterrupted remote dispatch during loss of all backhaul has been agreed.

2026-10-12 — Final owner confirmation: use only Heltec V4s for this trial. Exclude T-Decks to avoid added complexity from a different firmware/device path. This confirms the participant scope and closes the requirements interview.

## Answer

2026-10-12 — Later portal-interview amendment: one designated V3 is now permitted to transmit portal-originated shared-channel replies, while the other stays receive-only. The original two-receive-only requirement below is historical. V1 portal internet-outage viewing uses the previously accepted local Meshtastic fallback; a locally running copy of the same portal is not required for v1. See [Define the dispatch portal MVP](06-dispatch-portal.md).

Agreed first-pilot requirements, confirmed by the owner on 2026-10-12:

- **Member-node set:** 6 Heltec V4s, each intended to have dedicated GPS and a 3000mAh battery: 2 on hand, 2 planned purchases, and 2 planned recoveries. T-Decks are excluded to keep the device/firmware scope simple. This is a planned trial count, not a claim that all 6 are available or working.
- **Pilot infrastructure:** include owned RAK repeaters (count and exact builds to select) and 2 owned Heltec V3s intended as receive-only internet backhauls. V4-only refers to member trackers, not the entire network. The V3s are intended to receive radio traffic and forward it to dispatch over internet, without radio transmissions or RF relaying; verify that the selected firmware/configuration satisfies this requirement.
- **Dispatch freshness:** stale threshold of 15 minutes since the GPS position was measured. Dispatch must clearly distinguish stale locations and show their age; newly received old positions do not become fresh.
- **Reporting direction:** start aggressively and dial back based on measured network congestion. Evaluate plugged-in versus battery modes and movement-based rebroadcasting. Exact settings, stationary refresh behavior, and congestion criteria remain to be established against selected firmware and bench evidence.
- **Battery runtime:** at least 4 hours, with a 12-hour target under the selected tracking configuration. Larger batteries are an option if testing supports them; no extra battery purchase selected.
- **Phone-free MVP:** power on and automatically begin GPS broadcasting, without repeated member interaction. SOS is deferred to its separate future ticket.
- **Local viewing without internet backhaul:** field command-post viewing is required. Members using the companion app must be able to view other members' received locations in the field without internet backhaul. This does not require every member to use a phone, nor establish delivery when the radio path is unavailable. Offline maps, local connection arrangements, and stale/missing-position behavior remain to verify.

Remaining unknowns: exact hardware/radio/GPS builds and compatibility; receipt/recovery and readiness of planned units; firmware/network choice; reporting settings; routes and field-test duration; acceptable stale/missing-position frequency; dispatch ingestion and behavior through backhaul outages. The runtime minimum does not itself settle field-test duration. These belong to approach selection and subsequent bench/field planning; no measured success or operational readiness is claimed.

2026-10-12 — Owner scope clarification: include RAK repeaters and 2 Heltec V3 receive-only internet backhauls. The six V4s describe member trackers only. Infrastructure count/build selection and verification continue in the approach ticket; this clarification does not resolve the firmware/network decision.

2026-10-12 — Owner confirmed local viewing during internet backhaul outages, including field command-post viewing and other-member locations in the companion app for members who choose to use it. Added this requirement to the answer; specific offline implementation and acceptance procedure remain open in approach/test planning.
