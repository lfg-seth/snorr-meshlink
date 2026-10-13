# Define a future device-only SOS workflow

Type: grilling
Label: wayfinder:grilling
Status: resolved
Assignee: sos-workflow-session-2026-10-12
Parent: ../map.md
Blocked by: 02, 04

## Question

After passive tracking is established, what device-only distress action and dispatch response would be useful and testable?

## Completion evidence

Owner-agreed activation, accidental-trigger handling, cancellation, delivery/acknowledgment indication, dispatch workflow, and behavior during radio/backhaul outages. Verify feasibility for selected hardware and firmware before implementation.

## Comments

2026-10-12: Owner suggested a button combination or press-and-hold distress action, and explicitly requested SOS as a future issue. Deferred beyond the passive-tracking MVP; no gesture, delivery guarantee, or operational readiness established.

2026-10-12: Claimed as the next open, unblocked ticket at the owner's request. This interview defines future requirements only; passive tracking remains the implementation priority. Start with intended recipients and response ownership, then specify activation, cancellation, acknowledgment, and outage behavior. Awaiting owner input; no hardware feasibility or delivery guarantee established.

2026-10-12 — Owner requirements for recipients, alerts, and location:

- Send SOS to both dispatch and nearby members. Response coordination/ownership has not yet been explicitly agreed.
- Show an SOS popup on the Heltec OLED and flash it. Exact flashing behavior, persistence, dismissal, and which devices alert remain to specify and verify.
- Consider fitting a buzzer or similar audible alert to the board. This is an optional hardware idea, not confirmed stock, a selected part, wiring plan, or purchase.
- SOS should identify who needs help, a friendly area name, and latitude/longitude. Example owner-defined areas: Upper/Lower Champion Road, Lee Canyon, Kyle Canyon, and Deer Creek. These are naming examples, not verified geographic boundaries or an approved gazetteer; operational member identity mappings remain outside Git.
- Owner proposes drawing named polygons in Google Earth and exporting them. No area file or boundaries supplied yet.

Primary-source feasibility check, 2026-10-12: [Google Earth export help](https://support.google.com/earth/answer/148150?hl=en) documents KML export and KMZ containing KML; the [KML reference](https://developers.google.com/kml/documentation/kmlreference) supports named placemarks and polygon geometry, with coordinates in longitude, latitude, altitude order. This supports a proposed import/conversion pipeline for owner-defined areas; it does not demonstrate Heltec firmware support.

Proposed design for owner agreement: convert the area export into a versioned offline lookup, use a point-in-polygon test on the SOS position, and preserve coordinates plus measurement time in the alert. On-device lookup would allow a friendly name without internet; memory, polygon complexity, and firmware feasibility need evaluation. Define overlap/boundary rules, unmatched-area fallback, missing/stale GPS behavior, and matching area versions before implementation. Never invent a fresh fix or silently substitute an old location. No exact message format or code change selected.

Next interview round: choose the activation method. Accidental-trigger protection, cancellation, recipient alert dismissal, human acknowledgment versus transport delivery, response ownership, and outage/retry behavior remain open. Ticket stays claimed; no decision resolved or SOS implementation authorized by this requirements discussion.

2026-10-12 — Existing-button activation preference:

- Owner prefers holding the existing Heltec V4 button for 5 seconds to trigger SOS, replacing its long-hold shutdown behavior. This supersedes the proposed dedicated/recessed 3-second SOS button; no additional activation button requested.
- Owner believes the existing hold currently shuts down the device. Current upstream [InputBroker.cpp](https://github.com/meshtastic/firmware/blob/develop/src/input/InputBroker.cpp) maps the screen-equipped user button's extended hold to shutdown, with shorter holds used for selection. [ButtonThread.cpp](https://github.com/meshtastic/firmware/blob/develop/src/input/ButtonThread.cpp) handles hold timing/events. This supports investigating a firmware remap; the owned V4 revision, installed firmware, precise threshold, and physical button identity remain unverified. Distinguish the firmware-controlled user button from reset.
- Proposed interaction for agreement: display an SOS countdown during the hold, release before 5 seconds to abort, and trigger once at 5 seconds without requiring release or a second confirmation. Suppress conflicting menu/select/shutdown actions during the SOS hold, including when the screen starts asleep; prevent a continued hold from retriggering. These are proposed behavior and bench checks, not implemented features.
- Still open: post-send cancellation gesture and cancellation message, replacement normal-shutdown workflow, accidental sustained pressure, alert dismissal versus human acknowledgment, response ownership, retries/outages, and friendly-area/GPS fallback rules. Ticket remains claimed.

2026-10-12 — Owner agreed activation/cancellation and expanded active-SOS behavior:

- Agreed activation: visible countdown during a 5-second user-button hold, early release aborts, and trigger once when 5 seconds is reached while still held.
- Agreed cancellation: while SOS is active, release the button after activation and make a separate 5-second hold to cancel. Send cancellation to recipients. This replaces the proposed menu-based cancellation action; whether the cancellation countdown is the entire confirmation remains to clarify. A continuously held button must not activate and then cancel in the same press.
- Originating device must show rapid flashing or another obvious active/sending-SOS OLED indication while continuing to display incoming messages. Exact presentation remains open; outgoing attempt, transport delivery, and human acknowledgment must remain distinguishable.
- SOS should attempt another location broadcast/acquisition and warn the user if no current location is available. Clarify whether this means waking/requesting GPS acquisition as well as broadcasting the existing fix; do not wait indefinitely for GPS before alerting recipients.
- Send the last known location and its actual staleness when a current fix is unavailable. Preserve measurement time rather than stamping an old fix as fresh. Proposed never-had-a-fix fallback: send SOS with explicit “location unavailable” and no invented coordinates; awaiting agreement.
- During active SOS, when a new location becomes available, immediately send a new SOS transmission containing it. Owner has not yet specified whether this means every subsequent GPS fix or only recovery from missing/stale GPS. Transmission scheduling/airtime feasibility remains to verify; “immediate” is a requested behavior, not a demonstrated delivery latency.

Proposed incident handling for agreement: initial SOS, subsequent location updates, and cancellation share one incident identity with ordered updates. Fresh updates still alert recipients as SOS updates; they do not create unrelated emergencies. Preserve the fix time/age and recompute the friendly area from that same fix. Prevent delayed/duplicate updates from reopening a canceled incident or replacing a newer position. These are design proposals, not implemented packet semantics.

Next questions: whether each newer GPS fix should trigger an SOS update, whether to group these as one incident, and repetition when no new fix arrives. Also outstanding: never-had-a-fix behavior, human acknowledgment/response ownership, recipient alert dismissal, cancellation confirmation/delivery during outages, reboot state, replacement shutdown access, area boundary/version rules, and exact alert UI. No ticket resolution or firmware implementation yet.

2026-10-12 — Owner clarified message architecture and retry intent:

- Working assumption: SOS is a normal Meshtastic text message using a special recognizable format. Exact format/parser and compatibility are not selected. A readable text fallback is desired so a member can act from the OLED alone; automatic flashing/incident handling would still require compatible receiver behavior to be verified or implemented.
- Owner rejected sending a new SOS for every GPS fix. Use ordinary position broadcasts at an increased frequency while SOS is active. This supersedes the earlier general immediate-new-SOS-on-location requirement; whether the first recovered fix warrants a one-time SOS text refresh is not separately settled. Exact position interval remains a measured configuration/design choice.
- Owner wants SOS retransmission when nobody appears to receive it, without flooding the network when acknowledgment is impossible. Retry policy is not yet agreed. A member may see only the OLED message, navigate using the coordinates/friendly area, and reach the originating member without sending acknowledgment; local cancellation must remain sufficient to end that member's active SOS.
- Technical distinction: [Meshtastic broadcast algorithm](https://meshtastic.org/docs/overview/mesh-algo/) documents implicit acknowledgment from overhearing a rebroadcast and bounded transport retransmissions. Such evidence does not establish that dispatch or a person saw the SOS or accepted responsibility. Absence of acknowledgment likewise does not prove nobody received it. Application reminders must account for the transport's own retries rather than layering rapid duplicate sends on top. Release-specific behavior still needs verification.

Proposed retry/state policy for agreement:

- Send the initial readable SOS promptly, then send occasional refreshed SOS reminders while active. Each reminder includes the latest available location, area label, and original fix timestamp/age; normal faster position packets continue separately.
- Space reminders progressively farther apart up to a maximum interval, add small randomized timing, and bound total SOS/position airtime. Keep reminders slow even without any acknowledgment, so an OLED-only recipient does not have to acknowledge to prevent flooding. Exact intervals/budgets require bench testing, including simultaneous incidents.
- Treat transport receipt, human acknowledgment, and cancellation as distinct states. A transport acknowledgment alone must not report “help is coming.” Proposed explicit human acknowledgment stops repeated SOS text while keeping the local SOS indicator and faster tracking active until cancellation; awaiting agreement.
- A fresh, separate 5-second hold on the originating device ends local SOS and restores ordinary tracking even if cancellation delivery cannot be confirmed. Cancellation dissemination/retries and remote stale-active indications still need agreement; no guaranteed recipient clearance implied.

Remaining decisions: retry/acknowledgment policy, response ownership and receiver controls, fresh-fix recovery exception, missing-fix fallback, cancellation/reboot/shutdown details, area lookup rules, and display presentation. Hardware/firmware and exact rates remain feasibility/test work; ticket stays claimed.

2026-10-12 — Human acknowledgment deferred; originator controls cancellation:

- Owner explicitly deferred acknowledgment for this initial SOS design. Do not add a human-acknowledgment interaction or use acknowledgment to stop SOS reminders, clear alerts, or change active-SOS tracking. This supersedes the proposed human-acknowledgment state and its reminder-stop behavior.
- The originating member cancels the alert with a separate 5-second hold after releasing the activation press. An OLED-only recipient can act on the readable alert without acknowledging; recipient dismissal/silencing, if provided, must not cancel the originating incident.
- Keep reminder traffic bounded even without acknowledgment. Exact retry spacing/airtime budget remains a bench-design choice; owner has not selected numerical intervals. Transport acknowledgment may remain part of underlying Meshtastic delivery mechanics, but is not an SOS completion condition.
- First-version scope now excludes human acknowledgment UI/workflow. Keep SOS active indication, faster ordinary position updates, and bounded SOS text reminders until originating-device cancellation. Cancellation delivery and reboot behavior remain to specify; no claim that all recipients will clear simultaneously.

Next interview round: agree the never-had-a-GPS-fix fallback and whether active SOS survives an unexpected reboot. Remaining area boundaries/fallbacks, receiver dismissal/display, replacement shutdown access, cancellation dissemination, and response coordination can then be summarized or carried as explicit implementation prerequisites. Ticket remains claimed; no implementation or final resolution.

2026-10-12 — Missing GPS, reboot persistence, and power-aware effort:

- Owner agreed: send SOS even if no position has ever been acquired, explicitly showing location unavailable, warning the member, and continuing GPS acquisition.
- Owner agreed: persist active SOS through an unexpected reboot and restore indication, reminders, and faster tracking until originating-member cancellation. Persistence implementation and cancellation/reboot ordering need tests.
- Include battery status on the originating SOS screen alongside the active indication and incoming messages. Battery status in the transmitted text is not yet requested.
- Owner proposes reducing rebroadcast aggressiveness as battery gets low only while running on battery; wants maximum effort when externally powered even with low battery. Interpret effort as SOS text reminder and ordinary position cadence, with exact scope/rates to confirm. Do not equate maximum effort with unlimited transmissions or automatically changing RF power.
- Completed a preliminary [V4 power-detection check](../../../docs/research/v4-power-detection.md). Battery ADC support is present; reliable charger/power-bank detection with a low battery is not established. Exact board/build and a dependable external-power signal are bench prerequisites. A battery-voltage estimate or USB data-host connection alone is insufficient for the requested distinction.
- Numerical battery thresholds/cadences, unknown-source fallback, and whether non-USB input counts as external power remain open. No new parts, quantities, spending, firmware changes, or measurements established. Ticket stays claimed.

2026-10-12 — Power-source investigation pinned for later:

- Owner directed setting aside reliable power-source detection for now. Preserve the external-power versus battery-only effort requirement; do not settle the unknown-source policy or block the SOS requirements interview on this research.
- Owner suggests sustained battery-level direction as inferred charging status, observed over a configurable prolonged window, perhaps 1 minute. Added this candidate to the [power-detection follow-up](../../../docs/research/v4-power-detection.md); no algorithm/window selected or tested.
- Distinguish inferred charging from confirmed external power. Trend thresholds, smoothing/hysteresis, flat/ambiguous behavior, full-battery external power, load effects, and exact source-mode policy remain later verification/design work.
- SOS ticket remains claimed and human acknowledgment remains deferred. Next useful planning step is a consolidated requirements summary and the remaining receiver/area/cancellation choices; power detection is an explicit implementation prerequisite.

2026-10-12 — Final workflow agreement: owner accepted short-press receiver silencing with the alert retained, immediate originating-device cancellation with bounded cancellation-delivery attempts during outages, and dispatch coordination when reachable with nearby-member response otherwise. Owner accepted deferring the named implementation details and feasibility checks. Resolved the future workflow requirements only; implementation remains after passive tracking.

## Answer

Owner-agreed future device-only SOS workflow, 2026-10-12:

### Activation and cancellation

- Hold the existing Heltec V4 user button for 5 seconds, with a visible countdown. Releasing early aborts; reaching the threshold activates SOS once without a second confirmation. Replace the extended-hold shutdown action for this workflow.
- Require release before a separate subsequent 5-second hold cancels SOS. One continuous hold cannot both activate and cancel.
- Only the originating member cancels the incident. Cancellation exits local SOS immediately and restores ordinary tracking, even without radio/internet connectivity. Make bounded attempts to send cancellation; simultaneous clearance at all receivers is not guaranteed.
- Persist active SOS across unexpected reboot and resume the indication, reminders, and faster tracking until explicitly canceled. Verify persistence and cancellation ordering before implementation is accepted.

### Message, location, and effort

- Initial SOS is a readable Meshtastic text message following a recognizable special format, sent to both dispatch and nearby members. Include member identity, friendly area, coordinates when available, and position measurement age. Exact format and compatible parser behavior remain implementation work; keep operational identity mappings outside Git.
- Attempt a fresh GPS fix/report without indefinitely delaying SOS. If no current fix exists, warn the member and send last-known coordinates with their actual age. If no fix has ever existed, send explicit “location unavailable” and continue seeking GPS.
- During SOS, use ordinary position broadcasts at an increased frequency. Do not create an SOS text message for every GPS fix. Bounded recurring SOS reminders carry the latest available position/area and its original measurement time/age; never refresh old coordinates merely by retransmitting them.
- No human acknowledgment workflow in this version. Reminders and active tracking continue until originating-device cancellation. Underlying transport acknowledgment does not clear the SOS or assert that a person is responding.
- Bound retry traffic and overall airtime even without acknowledgment. Exact intervals, backoff, and position cadence need bench evaluation, including multiple simultaneous incidents and outages.
- Show battery status on the originating SOS screen. Use maximum configured effort on external power even with a low battery; taper low-battery effort only when running on battery. Maximum effort remains subject to the airtime budget. Reliable source detection is deferred; the proposed configurable battery-trend window (perhaps 1 minute) is an untested inferred-charging heuristic, not confirmed external power. See the [pinned follow-up](../../../docs/research/v4-power-detection.md).

### Display, recipients, and response

- Originating device shows an obvious flashing/active SOS indication and battery status while incoming messages remain viewable. Do not imply successful delivery merely because the device is attempting transmission.
- Receiving Heltecs show an SOS OLED popup/flashing alert. A short press silences flashing and any fitted buzzer locally while retaining the visible, active incident; it does not acknowledge or cancel the originator's SOS. Buzzer fitting remains optional and unverified.
- Retain last-heard age at receivers. Silence/outage alone never means canceled. Handle cancellation when received; remote indicators may remain active if cancellation cannot be delivered.
- Dispatch coordinates response when reachable. Nearby members can respond directly without internet or acknowledgment, including navigating from OLED coordinates/friendly area and helping the originating member cancel on that device.
- Friendly areas come from owner-defined Google Earth polygons exported as KML/KMZ. An offline lookup is a proposed implementation path; no boundaries supplied or inferred. Keep coordinates/age available alongside the area name.

### Deferred implementation and verification

- Pin exact V4 revision, user-button behavior, firmware/app builds, and compatible receiving devices; confirm button remapping, screen behavior, GPS acquisition, reboot persistence, and cancellation behavior on hardware.
- Define compact message/parser semantics, incident identity/order, duplicate handling, and protection against delayed SOS reopening a canceled incident. Verify the private dispatch ingestion path and local radio-only viewing; no delivery guarantee established.
- Select measured retry/position rates, battery thresholds, and source-state policy after bench tests. Reliable external-power detection and the battery-trend candidate remain pinned; no parts purchase or sensing circuit selected.
- Define polygon overlap/boundary/unmatched behavior, area-data versioning and device memory feasibility; finalize display layout and replacement normal-shutdown access. Optional buzzer GPIO/driver/power/enclosure compatibility remains to inspect.

This closes the future workflow requirements with owner agreement, not SOS implementation or operational readiness. Passive tracking remains first. No firmware built/flashed, broker/portal changed, hardware tested, purchases recorded, or commit requested.
