# Deferred feature wishlist

These are owner-requested future ideas, first recorded on 2026-10-12 and extended on the dates below. They are outside the current pilot scope and active ticket frontier. Do not start research, design, implementation, or testing for them until the owner explicitly brings them forward. Passive member GPS tracking remains the first priority.

During the `trial/local-tracking` branch trial, current status is maintained in the [local tracker](../.scratch/TRACKER.md) under the [local workflow](../docs/operations/local-tracking.md). Capture each new requested idea here and add one deferred tracker line linked to its section. This file preserves the owner's requested ideas and deferral decisions. Existing GitHub links below are historical references; issues and the Project board stay untouched during the trial, while `main` retains the prior workflow.

Keep these ideas available as context: mention a parked item when it is relevant and useful in a future conversation. Mentioning it does not activate it or authorize work.

## Known Wi-Fi networks with automatic MQTT backhaul

Original issue: [Known Wi-Fi networks with automatic MQTT backhaul](https://github.com/lfg-seth/snorr-meshlink/issues/15).

Status: deferred by owner.

Desired behavior: a compatible node stores a table of known Wi-Fi networks. When it detects a listed network, it automatically attempts to connect and then attempts MQTT backhaul to the project's private broker.

Exact supported devices, network selection/retry behavior, credential provisioning/storage, and effects on tracking and battery runtime remain unspecified and unverified. Keep actual Wi-Fi and MQTT credentials out of Git. The existing MQTT connectivity investigation remains separately parked.

## Browser-based firmware flashing for member-owned devices

Original issue: [Browser-based firmware flashing for member-owned devices](https://github.com/lfg-seth/snorr-meshlink/issues/16).

Status: deferred by owner.

Desired behavior: a member who purchases a supported device can flash the project's own firmware from a web browser. Support a small, preselected subset of devices; exact models and revisions remain to be selected later.

The owner cites Meshtastic's website flashing experience as the reference. Browser/device compatibility, firmware delivery, and any initial configuration or enrollment steps remain unspecified and unverified. No flasher technology, supported-device list, or onboarding process is selected now.

## Slack integration

Original issue: [Slack integration](https://github.com/lfg-seth/snorr-meshlink/issues/17).

Status: deferred by owner. Added 2026-10-12.

Desired direction: integrate SnorrMesh with Slack, which the owner reports SNORR uses heavily. The owner suggests a dedicated channel or an app/plugin as possible forms and is unfamiliar with Slack's API; these are ideas, not selected approaches.

Exact use cases, information shared, message direction, channel creation behavior, access permissions, and integration mechanism remain unspecified. Capture only for now; investigate Slack capabilities when the owner explicitly brings this item forward.

## Overlapping map nodes

Original issue: [Keep overlapping map nodes separately visible and selectable](https://github.com/lfg-seth/snorr-meshlink/issues/34).

Status: deferred by owner. Added 2026-10-19.

Owner reports that nodes at the same location stack on the map, preventing access to both. Keep their markers side by side until zoom provides enough separation; exactly co-located nodes must still each be accessible. Display separation must preserve stored coordinates. Report captured without independent reproduction or browser/build details; implementation and verification wait for activation.

## Selected-node neighbor signals on desktop

Original issue: [Show only the selected node's neighbor signals on the desktop main map](https://github.com/lfg-seth/snorr-meshlink/issues/35).

Status: deferred by owner. Added 2026-10-19.

Desired behavior: clicking a node on desktop shows only its neighbor signal connections on the main map, including when Show signal is off. Selecting another node switches the connections to that node. Behavior after deselection remains to define when activated; mobile changes are outside this request.

## Map default centered on all nodes

Original issue: [Default the map to the center of all node locations](https://github.com/lfg-seth/snorr-meshlink/issues/36).

Status: deferred by owner. Added 2026-10-19.

Desired behavior: stop defaulting to Mount Charleston and instead default to the center of mass of all nodes with usable locations. Exact calculation, initial zoom, empty-location fallback and saved-view interaction remain to define when activated.

## Member GPS tracking session controls

Original issue: [Allow starting, stopping and restarting member GPS tracking sessions while devices stay on](https://github.com/lfg-seth/snorr-meshlink/issues/37).

Status: deferred by owner. Added 2026-10-19.

Desired behavior: provide a way to start, stop and restart member-node (client) GPS tracking sessions even when a device remains powered on throughout. Session boundaries must be independent of device uptime or reboot boundaries. Control location, authorized roles, whether restart resumes a session or creates a new one, and treatment of reports outside active sessions remain to define when activated. No radio-broadcasting or raw-data-retention changes are selected by this request.

## Node-card neighbor details and inactivity cutoff

Original issue: [Simplify node-card neighbors and hide links after two hours of inactivity](https://github.com/lfg-seth/snorr-meshlink/issues/43).

Status: deferred; portal fix-list capture only. Added 2026-10-21.

Desired behavior: node-card neighbor entries show just the neighbor name, signal strength and distance in miles. Neighbors fall off the card after two or more hours without activity. Exact strength presentation, activity timestamp semantics and missing-location handling remain to define when activated. Card visibility does not request deletion of stored neighbor history. No independent reproduction or browser/build details captured.

## Hide sensor power section when no sensors are present

Original issue: [Hide node-card sensor voltage and current when no sensors are present](https://github.com/lfg-seth/snorr-meshlink/issues/44).

Status: deferred; portal fix-list capture only. Added 2026-10-21.

Desired behavior: hide the sensor voltage/current section on node cards when no sensors are present; retain it for nodes with relevant sensors. Sensor-presence detection remains to define when activated; missing or stale readings alone do not establish absent hardware. No independent reproduction or browser/build details captured.

## Member-node battery percentage and GPS layout

Original issue: [Add member-node battery percentage beside GPS quality on node cards](https://github.com/lfg-seth/snorr-meshlink/issues/45).

Status: deferred; portal fix-list capture only. Added 2026-10-21.

Desired behavior: on client/member-node cards, add battery percentage where GPS quality is now and move GPS quality to the right. Keep the battery logo/icon at the top. Missing-percentage presentation and responsive layout details remain to define when activated; no new battery-estimation method is selected.

## Remove endpoint locations from neighbor signal cards

Original issue: [Remove "Endpoint locations" from neighbor signal cards](https://github.com/lfg-seth/snorr-meshlink/issues/48).

Status: deferred; portal fix-list capture only. Added 2026-10-21.

Desired behavior: remove the "Endpoint locations" heading and its section contents from neighbor signal cards. The owner finds this section unnecessary. This is separate from the earlier minimap navigation change.

## Improve sign-in persistence

Original issue: [Improve portal sign-in persistence to avoid roughly hourly reauthentication](https://github.com/lfg-seth/snorr-meshlink/issues/49).

Status: deferred; portal fix-list capture only. Added 2026-10-21.

Owner reports needing to sign back in every hour or so. Desired behavior: retain a valid sign-in through ordinary use without roughly hourly credential prompts. This interval is approximate owner-reported behavior, not a measured token lifetime or established cause. Browser/device, application version, idle/active use and tab/reload behavior remain uncaptured. Exact longer duration and cross-tab/browser-restart expectations remain to define when activated; preserve deliberate sign-out, rejected/revoked-session handling and live/demo isolation. Diagnosis and verification wait for activation.
