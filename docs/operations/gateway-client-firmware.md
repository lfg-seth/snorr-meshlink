# Screenless V4 SD client gateway

[Download the 2.7.26.14c35c8 prerelease and SHA256SUMS](https://github.com/lfg-seth/firmware/releases/tag/snorr-v4-sd-client-2.7.26.14c35c8-pre.1).
Select the ordinary `.bin` for an existing screenless Heltec V4 SD gateway
with the matching 16 MB layout and active app0 at 0x10000. The separate
`.factory.bin` is a full installation image. Before updating, save a private
recovery backup and compare the installed partition table with the release's
`partitions.bin`. Verify the downloaded files with `sha256sum -c SHA256SUMS`.
The application is 1,921,120 bytes. Its SHA-256 is
`eabb4e83b2ee846980036de6cac506b303f468df74a2259416276d1d0cd58051`.

The target is `heltec-v4-sd-gateway-client`, for ESP32-S3 with 2 MB QSPI
PSRAM. It retains SD recording, INA219 telemetry and the authenticated survey
responder. CLIENT schedules eligible relays and cancels a pending relay when
it hears another node relay the packet. The MQTT receive path honors channel
downlink settings. [Firmware source](https://github.com/lfg-seth/firmware/commit/14c35c8ff4d9864ad91fbf3ea3f6e09b62daa21c).

## Configure the selected gateway

The application update preserves the saved profile. The earlier screenless
profiles used rebroadcast mode NONE and disabled MQTT downlink. Apply these
settings on the selected gateway and read them back after reboot.

| Setting | Value |
| --- | --- |
| Device role / rebroadcast mode | `CLIENT` / `ALL` |
| LoRa transmit / ignore MQTT | `lora.tx_enabled=true`, `lora.ignore_mqtt=false` |
| Network | Working Wi-Fi and the selected private broker, credentials and topic root |
| MQTT module | Enabled, direct TLS connection, encryption enabled, JSON disabled for the encrypted path |
| Private mesh channel | Enable downlink on the intended channel. Retain its existing key, uplink setting and radio profile. |

## Send a message through MQTT

For encrypted text, publish a Meshtastic `ServiceEnvelope` containing a
channel-encrypted `TEXT_MESSAGE_APP` packet on
`<root>/2/e/<channel-id>/<publishing-gateway-id>`. An uplink from another
Meshtastic gateway can supply this envelope. Use the same private channel,
a fresh nonzero packet ID and at least one hop remaining. The receiving
gateway suppresses its own echoes. The receiving radio must also accept
MQTT-marked packets.

For an application that sends text as JSON, configure a separate channel
named `mqtt` with downlink enabled and enable `mqtt.json_enabled`. Publish
without retain on `<root>/2/json/mqtt/<gateway-id>`. In the example, replace
`123456789` with the receiving gateway's **decimal** node number and `0`
with the intended outgoing mesh channel index.

```json
{"from":123456789,"type":"sendtext","channel":0,"payload":"Gateway bench check"}
```

JSON mode also publishes decoded copies of eligible uplinks to JSON topics.
Limit broker access accordingly. The gateway needs read access to the
selected downlink topic and the sender needs publish access. The documented
pilot gateway accounts have uplink-only permissions. Confirm the selected
account's ACL before the bench test.
[Pilot broker permissions](https://github.com/lfg-seth/snorr-meshlink/blob/323640a9b6e85055b0bb06a7f0b5dcb67fb1c5a2/docs/operations/mqtt-nginx-handoff.md).

## Acceptance

Offline checks exercised CLIENT relay eligibility, duplicate-cancellation
policy and MQTT handler dispatch, plus SD recording, survey and neighbor
report fixtures. Hardware acceptance needs an identified V4 and RF peer.
Send one fresh MQTT text to an RF-only receiver and match the text at that
receiver. Separately, observe a packet across a path requiring the client
relay and confirm it suppresses a duplicate when another relay wins.
