# Dispatch portal transport and backend

Checked 2026-10-12 against primary sources. This supports the open portal interview; it does not select firmware, deploy services, or establish operational reliability. Meshtastic documentation identifies itself as version 2.8; PocketBase documentation currently identifies v0.40.5. Firmware `master` links are moving references, not evidence about the owner's installed release. Pin and bench-test the selected release before configuration work.

## Recommendation for the interview

The owner's Proxmox VM can plausibly host Mosquitto, a small ingestion/command service, PocketBase, and a responsive browser portal. Expose the portal's HTTPS service through Cloudflare Tunnel. Give radio gateways a separate, proven route to the MQTT broker: local LAN for the bench, then a site/router VPN or an actual reachable MQTT TCP/TLS endpoint for remote sites. Stock Heltec MQTT should not be assumed to work through a Cloudflare public TCP hostname.

PocketBase is a good pilot candidate when built-in account administration, storage, and browser updates save work. The material tradeoff is its explicit production-critical warning and upgrade/migration maintenance. Treat backend selection as open until dispatch outage tolerance and maintenance ownership are agreed.

## Verified Meshtastic behavior

- Native MQTT uplink carries `MeshPacket` inside `ServiceEnvelope` on `<root>/2/e/<channel>/<gateway>`. JSON is an additional convenience representation for supported packet types, not a full replacement. Multiple gateways can report the same mesh packet. JSON's `from` identifies the originating node, while `sender` identifies the gateway; its outer `timestamp` is reception time. [MQTT integration](https://meshtastic.org/docs/software/integrations/mqtt/)
- The documented JSON downlink types are `sendtext` and `sendposition`. Text uses a string payload; `from` must identify the transmitting gateway; omitting `to` broadcasts; `channel: 0` selects the primary channel. It requires a downlink-enabled channel named `mqtt` and a reboot after creating it. [MQTT integration, JSON downlink](https://meshtastic.org/docs/software/integrations/mqtt/#json-downlink-to-instruct-a-node-to-send-a-message)
- Consequently, one operational channel remains feasible, but the documented JSON command mechanism can require a second technical channel on the designated gateway. This is an implementation detail to resolve, not a reason to add user-facing channel switching. Native protobuf downlink is another mechanism; it should not be treated as an interchangeable JSON command API. [MQTT integration](https://meshtastic.org/docs/software/integrations/mqtt/)
- Uplink/downlink are per-channel settings. Internet forwarding can use device networking or a client proxy. JSON is documented as unsupported on nRF52; a phone proxy does not satisfy the no-phone requirement for a gateway. JSON is unencrypted application data; MQTT payload encryption and MQTT connection TLS are different settings. Public map reports have a one-hour minimum interval and reduced position precision, so they do not meet the portal's 15-minute freshness requirement. [MQTT configuration](https://meshtastic.org/docs/configuration/module/mqtt/)
- Heltec LoRa32 V3/V3.1 and V4 have Wi-Fi-capable ESP32-S3 processors. V3 has no built-in GPS. V4-R8 is a distinct pinout/firmware variant. Exact boards, external GPS modules, and installed firmware still need identification. [Official device documentation](https://meshtastic.org/docs/hardware/devices/heltec-automation/lora32/)

Source-code checks, rather than installed-device guarantees: the JSON handler accepts commands only for its own numeric node ID; `sendtext` allocates a local text packet and sends it to the mesh. The MQTT code subscribes using topic wildcards, so validate the exact command topic on the selected release rather than relying on a shortened documentation example. The reviewed TLS path calls `setInsecure()`; enabling TLS does not establish verified server identity in that path. Its offline queue discards the oldest item when full. [MQTT implementation](https://github.com/meshtastic/firmware/blob/master/src/mqtt/MQTT.cpp) The reviewed header sets `MAX_MQTT_QUEUE` to 16 and uses `WiFiClient`/`WiFiClientSecure` with `PubSubClient`; it supplies no documented WebSocket MQTT transport. [MQTT header](https://raw.githubusercontent.com/meshtastic/firmware/master/src/mqtt/MQTT.h)

## Recording, freshness, and dispatch commands

The protobuf schema distinguishes GPS-solution `Position.timestamp` from packet `rx_time`. Packet IDs are unique per sender for a limited interval, not global identifiers for an indefinite archive. [Mesh schema](https://raw.githubusercontent.com/meshtastic/protobufs/master/meshtastic/mesh.proto)

Recommended application behavior (inference/design):

- Preserve every broker observation received, including raw envelope, gateway, topic, receive time, decode status, and firmware/schema version. Derive unique logical positions/messages separately; deduplicate with sender, packet ID, and a bounded time window plus payload checks. Do not discard gateway evidence or deduplicate an unlimited archive on packet ID alone.
- Store GPS measurement time, gateway reception time, and server ingestion time separately. Age the pin from a credible measurement time. Missing/invalid measurement time should display unknown age, not silently become fresh on arrival. Confirm the actual GPS timestamp fields emitted by the selected firmware; do not assume JSON preserves the entire Position protobuf.
- Record latest contact independently from latest position. A recent message or telemetry packet proves contact, not a recent fix. Delayed packets must not roll a node's current location backward.
- All data arriving at the collector can be recorded; this cannot promise every radio transmission survives RF loss, broker disconnects, or finite gateway buffers. Persistent broker sessions and collector recovery need testing.
- Allow only the designated gateway to consume dispatch commands; other internet-connected nodes remain uplink-only for that workflow. Enforce broker credentials and topic ACLs as well as device settings. `from` is a routing selector, not authorization. Mosquitto supplies password/authentication, listener, ACL, and persistence configuration. [Mosquitto configuration](https://mosquitto.org/man/mosquitto-conf-5.html)
- Create a dispatch command record before publishing. Show separately: accepted by portal, published to broker, gateway/radio evidence, and human response. Broker acceptance is not proof all members received a broadcast. Use finite expiry, avoid retained send commands, and prevent a reconnect from replaying old dispatch instructions.
- The proposed transmitting gateway changes the earlier receive-only requirement. Its RF transmission and other gateways' radio silence need explicit scope agreement and bench verification; MQTT switches alone do not prove radio silence.

## Cloudflare exposure

Cloudflare public application routes support HTTP/HTTPS directly. Its TCP route carries TCP over WebSocket and requires `cloudflared access tcp` on the client; the docs recommend Client-to-Tunnel for long-lived connections. [Tunnel routing](https://developers.cloudflare.com/tunnel/concepts/routing/) That is not an ordinary public port accepting an embedded node's raw MQTT connection.

Mosquitto can separately listen for MQTT over WebSockets. [Mosquitto listeners](https://mosquitto.org/man/mosquitto-conf-5.html) Cloudflare supports WebSockets, but connections can terminate during edge updates or inactivity and require reconnection/keepalive. [Cloudflare WebSockets](https://developers.cloudflare.com/network/websockets/)

Inference: a capable software bridge could use MQTT over WSS through an HTTPS Tunnel route. This does not add WSS support to stock Meshtastic. A site computer/router could bridge or provide VPN routing without requiring cloudflared on the Heltec. Establish what infrastructure exists at each gateway before choosing that option. Browser clients should normally consume the portal's authorized API/realtime stream, not receive broker credentials and publish arbitrary radio commands.

### Owner hostname example: `mqtt.spp.lol`

Clarified 2026-10-12: the hostname itself is usable. A published TCP Tunnel route is not a transparent public MQTT listener: Cloudflare wraps TCP in WebSockets and requires the connecting client to use `cloudflared access tcp`. Installing the Tunnel connector only on the broker VM does not supply the client-side adapter to a Heltec. [Current published-application protocols](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/routing-to-tunnel/protocols/).

An alternative is a DNS-only record pointing to a reachable broker, with direct MQTT TLS and router port forwarding where available. Cloudflare documents that DNS-only records return the origin address rather than sending traffic through its proxy. This is a proposed path conditional on the owner's actual network/public-address/router capabilities, not confirmation of reachability. [DNS proxy status](https://developers.cloudflare.com/dns/proxy-status/).

A different candidate is an HTTP/WebSocket Tunnel route to a broker's MQTT-over-WebSockets listener, paired with firmware support or a local adapter. Mosquitto supports a `websockets` listener and Cloudflare supports WebSockets; those server capabilities do not add a WebSocket client to the current Heltec firmware. This is an implementation inference to test, not the same wire protocol as Cloudflare's arbitrary-TCP adapter. [Mosquitto listeners](https://mosquitto.org/man/mosquitto-conf-5.html), [Cloudflare WebSockets](https://developers.cloudflare.com/network/websockets/), [Meshtastic MQTT header](https://github.com/meshtastic/firmware/blob/master/src/mqtt/MQTT.h).

## PocketBase fit and limits

PocketBase bundles SQLite, REST-style records, auth, an administrative dashboard, and realtime subscriptions in a self-hosted executable. It can serve static portal assets. Its documentation explicitly says backward compatibility is not guaranteed before 1.0 and does not recommend production-critical applications unless the owner accepts changelog review and occasional manual migration. [Introduction](https://pocketbase.io/docs/)

Username/password is supported by configuring a unique username identity field. Normal auth accounts differ from superusers, which bypass collection rules. [Authentication](https://pocketbase.io/docs/authentication/) Collections/records can be administered in the dashboard, including auth records; email can be optional. Roles and a Manage rule support delegated account administration. [Collections](https://pocketbase.io/docs/collections/) It does not ship the portal's login/registration frontend, and scales on a single server. [FAQ](https://pocketbase.io/faq/)

Realtime uses Server-Sent Events for record creates, updates, and deletes, with collection access rules governing subscriptions. [Realtime API](https://pocketbase.io/docs/api-realtime/) Production guidance includes rate limiting, durable backups, and protection of superuser access. [Going to production](https://pocketbase.io/docs/going-to-production/)

Inference: use administrator-created portal accounts initially, separate from tracked members/devices. A tracker need not have a login, and replacing a device need not replace a member. Keep map/history/message reads behind ordinary authenticated rules and dispatch publishing behind a dispatcher role; never place superuser credentials in the browser. Disable an account through an enforced application rule rather than assuming that hiding it in the UI revokes a previously issued token.

PocketBase does not remove the MQTT ingestion problem. Its built-in JavaScript runtime is embedded ES5, not a Node.js runtime. [JavaScript extension overview](https://pocketbase.io/docs/js-overview/) The simple proposed arrangement is a separate long-running MQTT worker writing validated records via local backend access and consuming authorized command records; a Go extension is possible if later justified. Avoid introducing another full backend solely for authentication unless it reduces the total maintenance burden.

## Next evidence needed

Agree whether the first portal is an evaluation aid or relied-on operational dispatch; identify where each gateway reaches the VM; identify one transmitting V3 and its installed release; capture representative position/text/envelope data; bench-test duplicates, stale GPS, broker loss/recovery, unauthorized publishing, reconnect behavior, and downlink evidence. These are proposed checks, not completed tests. Raw tracks and credentials belong in ignored `private/` or `local-data/`, not Git.
