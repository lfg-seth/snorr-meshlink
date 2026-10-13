# Device identity and remote name updates

Primary-source review: 2026-10-12. Sources describe current documentation and moving `master` branches, not the installed pilot firmware. No radio rename, key provisioning, implementation, or hardware test performed. Broker exposure remains deferred.

## Result

Short names need not be unique database keys. A portal can identify physical devices independently of names, associate a device with a member, and request an over-the-air name change through Meshtastic remote administration. Stock MQTT text commands do not provide that administration API. Keep the portal assignment and the confirmed radio-name state separate until the target responds and its owner data is read back.

## Identity layers

| Layer | Evidence and intended use |
| --- | --- |
| Portal device ID and sticker | Recommendation: generate a permanent portal UUID and human-readable asset sticker. This remains the inventory/assignment key even when firmware or radio identifiers change. |
| Hardware identity | Current `MyNodeInfo.device_id` is a local hardware identifier. On ESP32-S3, reviewed firmware reads 16 bytes from `ESP_EFUSE_OPTIONAL_UNIQUE_ID`. Capture and verify it during provisioning; it is not part of every MQTT position packet. |
| Factory MAC | Espressif provides a factory eFuse base MAC read API; a full MAC-48 is 6 bytes. Capture the factory value rather than assuming an interface MAC cannot be overridden. This is a fallback provisioning identity, not authentication. |
| Mesh transport ID | `!xxxxxxxx` represents the 32-bit node number. Initially derived from the last four MAC bytes; saved state and conflict/reserved-number handling matter. Track it as the device's current radio address and retain old mappings. |
| Public key | Cryptographic credential used for authenticated/encrypted exchanges. It can be regenerated when key material is absent or replaced, so it is not a permanent asset serial. |
| Long/short names | Mutable display labels. Reassignment can change both without replacing the device or its historical identity. |

Verified implementation: `NodeDB::pickNewNodeNum()` starts from the saved number, derives one from MAC when zero, and picks a random alternative if a known node with a different MAC already uses it or the number is reserved. It formats `owner.id` from that number. NodeDB also populates the S3 eFuse hardware ID and generates/regenerates keys according to stored private-key state. Therefore, a reset can restore the MAC-derived address, but it is wrong to claim every reset necessarily changes the address or that the address can never change. The reviewed code establishes actual selection behavior; old schema collision prose is not used as proof of a particular live collision protocol. [NodeDB source](https://raw.githubusercontent.com/meshtastic/firmware/master/src/mesh/NodeDB.cpp)

The schema marks `User.macaddr` deprecated and distinguishes `MyNodeInfo.device_id` from `my_node_num`. It documents long names as 24 UTF-8 bytes on current firmware. [Mesh schema](https://raw.githubusercontent.com/meshtastic/protobufs/master/meshtastic/mesh.proto) The current decode options retain a larger compatibility buffer for old senders but reserve 5 bytes for short names including the terminator: use a conservative four ASCII characters for portal-generated short names and enforce the deployed release's long-name limit. [Nanopb options](https://raw.githubusercontent.com/meshtastic/protobufs/master/meshtastic/mesh.options)

Espressif documents `esp_efuse_mac_get_default()` for the factory base MAC and separate APIs for custom base/interface MACs. Names and flash preference resets do not rewrite that factory MAC. Replacing the MCU/board changes which physical hardware is identified. [ESP32-S3 system APIs](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/misc_system_api.html)

Recommendation: store UUID, sticker, populated hardware `device_id`, factory MAC when captured, current transport node ID, key fingerprint, and observed names as separate fields. Verify identifiers on the actual V3/V4 release and reject missing/all-zero hardware values. Ordinary MQTT discovery can map a provisioned transport ID to an asset; an unfamiliar ID/key after reset should require reconciliation rather than automatically merging on a reused short name. Member-to-device assignment should have effective dates so past locations remain associated with the person carrying the device at that time.

## Supported remote rename mechanism

For firmware 2.5+, official remote-admin instructions require the controlling radio's public key in the target's Security `admin_key` list, with up to three authorized controllers. Default administration is local USB/Bluetooth/TCP; remote administration carries authenticated Admin Messages over the mesh. [Remote administration documentation](https://meshtastic.org/docs/configuration/remote-admin/)

Current Python `Node.setOwner(long_name, short_name, ...)` constructs `AdminMessage.set_owner`, obtains a session key, and sends to the target node with PKI encryption and response/ACK handling. `MeshInterface.getNode(nodeId, ...)` creates a remote Node, so a backend can call `getNode(target, requestChannels=False).setOwner(...)` through a locally connected controller. This is source-level support, not a tested portal integration; pin SDK and firmware together. [Python Node](https://raw.githubusercontent.com/meshtastic/python/master/meshtastic/node.py), [Mesh interface](https://raw.githubusercontent.com/meshtastic/python/master/meshtastic/mesh_interface.py)

The firmware admin handler validates the sender against authorized admin keys, requires a valid session passkey for remote mutations, handles `set_owner`, and saves/broadcasts changed names. Session passkeys expire; the application must handle request/response ordering, expiry, retry, and read-back. Preserve non-name flags such as licensed/unmessageable state when using a User/setOwner update. [Admin implementation](https://raw.githubusercontent.com/meshtastic/firmware/master/src/modules/AdminModule.cpp)

Recommended path: an authorized portal action creates a narrow rename job; a trusted agent with USB or local TCP access to the designated controlling radio uses the supported Python/radio API; the controller performs PKI remote administration over LoRa. Initial admin-key provisioning happens while devices are locally accessible. Keep credentials and controller keys server-side. Radio reachability and authorization are required even if the portal assignment itself succeeds.

## MQTT limits and nuance

The reviewed MQTT implementation supports JSON `sendtext`/`sendposition`; neither issues a `set_owner` admin request. It explicitly rejects decoded `ADMIN_APP` downlink packets. Publishing a plaintext AdminMessage protobuf is therefore not a supported shortcut. However, the same implementation has a conditional forwarding path for encrypted `PKI` envelopes when downlink is enabled and endpoint knowledge permits. [MQTT implementation](https://raw.githubusercontent.com/meshtastic/firmware/master/src/mqtt/MQTT.cpp)

The reviewed AdminModule has no blanket `via_mqtt` rejection; its checks concern authentication, encryption, and session state. [Admin implementation](https://raw.githubusercontent.com/meshtastic/firmware/master/src/modules/AdminModule.cpp) The router can reject MQTT-origin packets through `ignore_mqtt`. [Router implementation](https://raw.githubusercontent.com/meshtastic/firmware/master/src/mesh/Router.cpp)

Inference: a separately implemented encrypted native-MQTT admin client might carry a complete PKI/session exchange in a compatible configuration, but this research does not demonstrate it. It requires cryptographic identity, the target's key, correctly constructed encrypted packets/envelopes, return traffic, passkey handling, and release-specific forwarding checks. Do not describe all MQTT administration as impossible, or describe native injection as a plug-and-play portal rename mechanism.

A custom gateway firmware command could instead accept a narrowly authorized rename request and originate the proper local-radio admin exchange. That is a custom integration to evaluate if a local API agent is unsuitable; it must preserve remote-admin authorization, job expiry/idempotency, and confirmation. No complexity or delivery guarantee has been established.

## Acceptance checks before implementing assignment automation

Provision two test radios; record hardware/transport/key identities; authorize the controller; rename long/short names remotely and read back; prove those names do not change hardware identity; test target offline, wrong controller key, expired session, retry, reassignment while an old job is pending, and a reset/reprovisioning reconciliation. Use job states such as pending, confirmed, and failed. A portal save or an implicit radio ACK alone should not label the rename confirmed. These checks are proposed, not measured results.
