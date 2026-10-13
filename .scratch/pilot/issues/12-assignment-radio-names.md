# Choose assignment-driven radio names and identity

Type: grilling
Label: wayfinder:grilling
Status: resolved
Assignee: device-naming-session-2026-10-12
Parent: ../map.md
Blocked by: none

## Question

When a member claims or is assigned a numbered tracker, which radio names should change, and how should the portal preserve physical-device identity and communicate pending/confirmed/failed remote updates?

## Comments

2026-10-12 — Owner asks about OTA admin renaming and hardware-specific permanent IDs versus reserving short names as identifiers. The [capability investigation](11-device-identity-research.md) supports this conversation; no device/admin keys or radio settings changed. MQTT connectivity remains parked.

Proposed policy for owner input: stable physical label #004 and short name S004, long name Seth [004] on claim/assignment rather than merely opening device details. Portal assignment takes effect independently of OTA success, with remote name status shown separately. Internal device record/verified hardware identifier preserve history; neither mutable name is the database key. Asked the owner to choose this policy, both names reflecting the carrier, or radio names fixed with portal-only member labels.

Initial primary-source facts: the current schema exposes hardware `MyNodeInfo.device_id`; current ESP32-S3 NodeDB reads it from eFuse. Capture and verify it during local provisioning, rather than assuming it arrives in ordinary MQTT position traffic. The mesh node number/`!nodeID` is separate and can be reselected; long/short names are editable labels. Remote admin needs target trust provisioning and a working admin-capable gateway path; stock MQTT text commands do not establish that path. See the capability investigation for completed evidence/limits.

Completed [identity/admin research](../../../docs/research/device-identity-admin.md): Python `Node.setOwner` provides PKI/session-aware targeted updates through a connected trusted controller; read-back is proposed confirmation. Decoded MQTT admin messages are rejected; native encrypted PKI has conditional forwarding, so a custom admin integration is not ruled out but remains unverified. The owner's naming policy is still pending; neither the portal baseline nor any radio was renamed.

2026-10-12 — Owner confirms: “We can keep shortname static to device number.” Resolved the naming direction below. No actual device names or assignments changed.

## Answer

Owner-agreed naming direction, 2026-10-12:

- Keep each tracker’s radio short name permanently tied to its device number across member claims/reassignments. `S004` for Device #004 is the discussed example; exact prefix/padding conventions are not a new hardware identifier requirement.
- The short name is a human-readable device label, not the database's unique key. Preserve a stable portal device record and capture/verify hardware identity during provisioning; keep the current Meshtastic node ID separate. Names do not determine historical attribution.
- Retain the assignment workflow discussed with the owner: the portal records the carrier immediately and can update the long name to identify that carrier (example `Seth [004]`). A radio-name job is separate from assignment success, with pending/confirmed/failed status and read-back confirmation. Trigger on claim/assignment, not simply viewing a pin/device page. Do not change the short name when changing carriers.
- Preserve dated assignments and prevent a delayed old rename job from overwriting the name for a newer assignment. Release/unassigned long-name wording can be chosen during UI detail work; it must not imply a departed carrier still holds the tracker.
- Remote-name execution requires initial controller-key authorization, a supported admin-capable integration and selected-build tests. The [source research](../../../docs/research/device-identity-admin.md) establishes supported mechanisms, not a functioning portal-to-radio path. Do not treat MQTT text publication as rename success.

Planning decision only; no physical label/name/key changes, provisioning, firmware/UI implementation, hardware test or deployment performed. MQTT connectivity remains parked under the owner's prior planning assumption.
