# Deferred feature wishlist

These are owner-requested future ideas, recorded on 2026-10-12. They are outside the current pilot scope and active ticket frontier. Do not start research, design, implementation, or testing for them until the owner explicitly brings them forward. Passive member GPS tracking remains the first priority.

Keep these ideas available as context: mention a parked item when it is relevant and useful in a future conversation. Mentioning it does not activate it or authorize work.

## Known Wi-Fi networks with automatic MQTT backhaul

Status: deferred by owner.

Desired behavior: a compatible node stores a table of known Wi-Fi networks. When it detects a listed network, it automatically attempts to connect and then attempts MQTT backhaul to the project's private broker.

Exact supported devices, network selection/retry behavior, credential provisioning/storage, and effects on tracking and battery runtime remain unspecified and unverified. Keep actual Wi-Fi and MQTT credentials out of Git. The existing MQTT connectivity investigation remains separately parked.

## Browser-based firmware flashing for member-owned devices

Status: deferred by owner.

Desired behavior: a member who purchases a supported device can flash the project's own firmware from a web browser. Support a small, preselected subset of devices; exact models and revisions remain to be selected later.

The owner cites Meshtastic's website flashing experience as the reference. Browser/device compatibility, firmware delivery, and any initial configuration or enrollment steps remain unspecified and unverified. No flasher technology, supported-device list, or onboarding process is selected now.

## Slack integration

Status: deferred by owner. Added 2026-10-12.

Desired direction: integrate SnorrMesh with Slack, which the owner reports SNORR uses heavily. The owner suggests a dedicated channel or an app/plugin as possible forms and is unfamiliar with Slack's API; these are ideas, not selected approaches.

Exact use cases, information shared, message direction, channel creation behavior, access permissions, and integration mechanism remain unspecified. Capture only for now; investigate Slack capabilities when the owner explicitly brings this item forward.
