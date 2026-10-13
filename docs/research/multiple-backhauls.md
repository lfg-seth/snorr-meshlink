# Multiple MQTT backhauls for the tracking pilot

Checked 2026-10-12 against official Meshtastic documentation and firmware source. This is a capability baseline and proposed test sequence, not a measured capacity result.

## Supported path and client limits

Meshtastic documents `mqtt.proxy_to_client_enabled` for using a connected phone's internet connection, including Android and Apple setup instructions. Android also documents a phone-side proxy toggle that can stop forwarding without changing the radio configuration. The Web Client's visible proxy setting is explicitly documented as nonfunctional. Do not infer support in another companion app from the presence of the radio setting; verify its exact app/version. [Module configuration](https://meshtastic.org/docs/configuration/module/mqtt/), [Android proxy controls](https://meshtastic.org/docs/software/android/user/mqtt/).

Optional member uplinks should require the member's explicit participation, the radio's MQTT/proxy configuration, and any app-side privacy/relay opt-in. Radio configuration is not proof that an app is forwarding. Record app/version, OS, background/locked-screen behavior, radio connection and cellular availability during the test. These sources do not guarantee continuous phone forwarding when an app is suspended or disconnected.

## Duplicates, direction and outages

Official integration documentation warns that multiple gateways can publish duplicate packets and directs subscribers to deduplicate by packet ID. Preserve the originating node (`MeshPacket.from`) separately from the gateway ID/topic suffix. **Implementation proposal:** deduplicate within a bounded window using origin node plus packet ID (and channel/network context), while retaining which gateways heard the report and their receipt times; gateway ID is not the member's identity. [MQTT integrations and gateway notes](https://meshtastic.org/docs/software/integrations/mqtt/).

Enable only the required private-channel uplinks. Keep per-channel downlink disabled on both fixed V3 receivers and optional member gateways: downlink forwards internet packets into LoRa and consumes airtime. MQTT uplink itself is a network publication, not an additional member position transmission over LoRa. Do not copy the general bidirectional quick-start settings into this ingestion-only pilot. [Integration direction settings](https://meshtastic.org/docs/software/integrations/mqtt/), [channel configuration](https://meshtastic.org/docs/configuration/radio/channels/).

Current firmware `MQTT::onSend()` excludes packets already marked `via_mqtt`, checks channel uplink permission, and uses direct connectivity or client proxy to publish. This reduces one feedback path; it does not justify enabling internet-to-LoRa downlink. Its disconnected queue drops the oldest entry when full, so outage recovery is not guaranteed complete. [Official MQTT source](https://github.com/meshtastic/firmware/blob/master/src/mqtt/MQTT.cpp).

## Staged evaluation

1. Establish the two fixed V3 receive-only backhauls first, forwarding to the private broker with LoRa TX disabled and downlink disabled. Verify one report becomes one dispatch update even when both gateways receive it.
2. Add one explicitly participating member phone uplink, then a small additional group only after checking duplicate volume, receipt delay/position age, missing reports, reconnect behavior, phone/radio stability and broker/dispatch load against the baseline.
3. Interrupt each internet path separately; test phone lock/background operation and restored connectivity. Ensure local member-app and command-post viewing continue independently of internet ingestion.

These are proposed checks, not field results or a promise that all member phones can uplink concurrently. Extra receive/uplink gateways can improve ingestion opportunities, but duplicate network traffic and processing still grow. Radio airtime, firmware throttling, regional duty-cycle limits and unchanged GPS broadcast behavior remain separate constraints. [Mesh broadcast/throttling](https://meshtastic.org/docs/overview/mesh-algo/), [LoRa duty-cycle behavior](https://meshtastic.org/docs/configuration/radio/lora/).

## Verification limits

No device, app or broker was tested. Live documentation and `master` source are moving references; record exact firmware/app versions and pin the matching source before implementation. A source commit could not be resolved in this lookup because shell access to GitHub's API failed DNS resolution.

Current official app guides say firmware JSON output was removed, while the module/integration docs and inspected `master` MQTT source still describe or implement JSON. Treat serialization support as release-dependent until verified; protobuf ServiceEnvelope ingestion avoids relying on that disputed documentation claim. [Android format caveat](https://meshtastic.org/docs/software/android/user/mqtt/), [Apple format caveat](https://meshtastic.org/docs/software/apple/user/mqtt/), [module configuration](https://meshtastic.org/docs/configuration/module/mqtt/), [MQTT source](https://github.com/meshtastic/firmware/blob/master/src/mqtt/MQTT.cpp).
