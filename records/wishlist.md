# Deferred feature wishlist

These are owner-requested future ideas, first recorded on 2026-10-12 and extended on the dates below. They are outside the current pilot scope and active ticket frontier. Do not start research, design, implementation, or testing for them until the owner explicitly brings them forward. Passive member GPS tracking remains the first priority.

Current status is maintained in the linked GitHub issues under the [tracking workflow](../docs/operations/github-tracking.md). This file preserves the owner's requested ideas and deferral decisions.

Keep these ideas available as context: mention a parked item when it is relevant and useful in a future conversation. Mentioning it does not activate it or authorize work.

## Known Wi-Fi networks with automatic MQTT backhaul

GitHub: [track this deferred idea](https://github.com/lfg-seth/snorr-meshlink/issues/15).

Status: deferred by owner.

Desired behavior: a compatible node stores a table of known Wi-Fi networks. When it detects a listed network, it automatically attempts to connect and then attempts MQTT backhaul to the project's private broker.

Exact supported devices, network selection/retry behavior, credential provisioning/storage, and effects on tracking and battery runtime remain unspecified and unverified. Keep actual Wi-Fi and MQTT credentials out of Git. The existing MQTT connectivity investigation remains separately parked.

## Browser-based firmware flashing for member-owned devices

GitHub: [track this deferred idea](https://github.com/lfg-seth/snorr-meshlink/issues/16).

Status: deferred by owner.

Desired behavior: a member who purchases a supported device can flash the project's own firmware from a web browser. Support a small, preselected subset of devices; exact models and revisions remain to be selected later.

The owner cites Meshtastic's website flashing experience as the reference. Browser/device compatibility, firmware delivery, and any initial configuration or enrollment steps remain unspecified and unverified. No flasher technology, supported-device list, or onboarding process is selected now.

## Slack integration

GitHub: [track this deferred idea](https://github.com/lfg-seth/snorr-meshlink/issues/17).

Status: deferred by owner. Added 2026-10-12.

Desired direction: integrate SnorrMesh with Slack, which the owner reports SNORR uses heavily. The owner suggests a dedicated channel or an app/plugin as possible forms and is unfamiliar with Slack's API; these are ideas, not selected approaches.

Exact use cases, information shared, message direction, channel creation behavior, access permissions, and integration mechanism remain unspecified. Capture only for now; investigate Slack capabilities when the owner explicitly brings this item forward.

## Overlapping map nodes

GitHub: [Keep overlapping map nodes separately visible and selectable](https://github.com/lfg-seth/snorr-meshlink/issues/34).

Status: deferred by owner. Added 2026-10-19.

Owner reports that nodes at the same location stack on the map, preventing access to both. Keep their markers side by side until zoom provides enough separation; exactly co-located nodes must still each be accessible. Display separation must preserve stored coordinates. Report captured without independent reproduction or browser/build details; implementation and verification wait for activation.

## Selected-node neighbor signals on desktop

GitHub: [Show only the selected node's neighbor signals on the desktop main map](https://github.com/lfg-seth/snorr-meshlink/issues/35).

Status: deferred by owner. Added 2026-10-19.

Desired behavior: clicking a node on desktop shows only its neighbor signal connections on the main map, including when Show signal is off. Selecting another node switches the connections to that node. Behavior after deselection remains to define when activated; mobile changes are outside this request.

## Map default centered on all nodes

GitHub: [Default the map to the center of all node locations](https://github.com/lfg-seth/snorr-meshlink/issues/36).

Status: deferred by owner. Added 2026-10-19.

Desired behavior: stop defaulting to Mount Charleston and instead default to the center of mass of all nodes with usable locations. Exact calculation, initial zoom, empty-location fallback and saved-view interaction remain to define when activated.

## Member GPS tracking session controls

GitHub: [Allow starting, stopping and restarting member GPS tracking sessions while devices stay on](https://github.com/lfg-seth/snorr-meshlink/issues/37).

Status: deferred by owner. Added 2026-10-19.

Desired behavior: provide a way to start, stop and restart member-node (client) GPS tracking sessions even when a device remains powered on throughout. Session boundaries must be independent of device uptime or reboot boundaries. Control location, authorized roles, whether restart resumes a session or creates a new one, and treatment of reports outside active sessions remain to define when activated. No radio-broadcasting or raw-data-retention changes are selected by this request.
