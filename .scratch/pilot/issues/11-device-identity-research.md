# Check persistent device identity and remote name updates

Type: research
Label: wayfinder:research
Status: resolved
Assignee: device-identity-research-2026-10-12
Parent: ../map.md
Blocked by: none

## Question

Which Meshtastic identifiers persist independently of long/short names on Heltec V3/V4, and what supported remote-admin mechanism can let portal device assignment update radio names without assuming that MQTT text downlink is an admin interface?

## Comments

2026-10-12 — Owner asks whether selecting/claiming a device can update its long/short names over the air, and whether a hardware-specific persistent identifier means the short name need not serve as the unique key. Verify current primary docs/schema/source; preserve the owner-deferred Cloudflare reachability assumption and do not reopen broker networking. No rename, credential provisioning, flashing, or portal implementation authorized/performed by this research.

## Answer

2026-10-12 — See [Device identity and remote name updates](../../../docs/research/device-identity-admin.md) for primary sources and verification limits.

- Short/long names are mutable display fields. Use a portal UUID/sticker and provisioned hardware identity independently of the current mesh transport address and person assignment.
- Current Meshtastic ESP32-S3 source exposes an eFuse-derived 16-byte `MyNodeInfo.device_id`; verify populated values on the installed V3/V4 release during provisioning. The full factory MAC is another capturable hardware identifier. Deprecated broadcast macaddr, truncated MAC-derived node numbers, and regenerable public keys should not be treated as permanent asset serials.
- Current Python Node.setOwner supports target-node AdminMessage updates with PKI/session handling. Firmware 2.5+ remote admin requires the controller key provisioned on each target. Recommend portal rename jobs executed by a trusted local radio API agent (USB/local TCP), followed by confirmed read-back.
- JSON MQTT sendtext cannot rename; decoded native ADMIN_APP is rejected. Encrypted native PKI forwarding exists conditionally, so a full custom encrypted admin integration is not ruled out, but is not verified or plug-and-play. Current AdminModule has no blanket via_mqtt rejection; do not invent one.
- Keep assignment success and radio rename confirmation separate. Pin firmware/SDK, enforce release-specific byte limits, preserve other owner flags, and test offline/unauthorized/expired-session/reassignment behavior.

Documentation/source research only; no naming, key provisioning, deployment, code implementation, hardware test, or commit. Parent session will update the map/session record.
