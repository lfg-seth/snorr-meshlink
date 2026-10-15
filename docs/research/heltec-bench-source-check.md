# Heltec V3/V4 bench source check

Checked 2026-10-14 against official documentation and upstream source. This is a prerequisite review, not evidence that owned boards have passed tests. The local baseline is `v2.7.26.54e0d8d`, commit `54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb`, as inspected in the accompanying bench review. Current documentation describes additional newer capabilities; installed hardware/build behavior still needs verification.

## Board and image identification

| Physical board | Meshtastic image target | Check before flashing |
| --- | --- | --- |
| LoRa32 V3 or V3.1 | `heltec-v3` | Exact board and frequency variant |
| Original LoRa32 V4, ESP32-S3R2 | `heltec-v4` | Chip marking and connector/wiring identification |
| LoRa32 V4-R8, ESP32-S3R8, OLED | `heltec-v4-r8-oled` | R8 chip and OLED display |
| LoRa32 V4-R8, ESP32-S3R8, TFT | `heltec-v4-r8-tft` | R8 chip and TFT display |

V4-R8 has a different pinout and requires its own image; original V4 firmware must not be flashed onto R8. Documentation specifies 2.7.25 or newer for R8 support. V3/V3.1 share an image, have no built-in GPS, and have a documented USB-C charging caveat: use USB-A to USB-C. The V3 USB/UART bridge lacks ESD protection. These are documented capabilities/cautions, not identification of the owner's units. [Meshtastic Heltec support](https://meshtastic.org/docs/hardware/devices/heltec-automation/lora32/).

Heltec lists V4's eight-pin GNSS connector as an addition over V3. A connector does not establish that a functioning GNSS module is installed. Use the actual revision's pin map and module electrical specification before powering wiring; V4-R8 must not inherit an original-V4 wiring assumption. [Heltec board comparison and resources](https://docs.heltec.org/en/node/esp32/wifi_lora_32/index.html).

## GPS and private-channel prerequisites

Stock firmware exposes GPS mode, acquisition interval, periodic broadcast interval, smart broadcasting, external GPS RX/TX/enable GPIOs and a position flag for the GPS-solution timestamp. Acquisition and transmission are separate settings. Fixed position repeats saved coordinates, so disable it for moving member nodes. Check source measurement time in actual packets, not just arrival time. A phone-free cold boot, stationary fresh fixes, movement and loss of fix remain bench tests. [Position configuration](https://meshtastic.org/docs/configuration/radio/position/).

The official V3 external-GPS example connects GPS TX to board RX GPIO48 and GPS RX to board TX GPIO47, with optional switched-power control GPIO46. These are example pins, not verified owned wiring or a V4 prescription. The guide distinguishes no GPS, disabled GPS and no lock; a sky view is required for lock testing. Check voltage, polarity and installed pin configuration first. [Heltec peripherals](https://meshtastic.org/docs/hardware/devices/heltec-automation/lora32/peripherals/).

Use a shared private channel key kept outside Git. Default/simple keys are public. Check channel position precision explicitly: zero suppresses position; 32 sends full precision; public-key channels are capped at 15 bits in current documentation. [Channel configuration](https://meshtastic.org/docs/configuration/radio/channels/).

## Radio prerequisites

For the Nevada bench, confirm 902–928 MHz hardware and select `US`; match modem settings and frequency slot across nodes. `UNSET` prevents transmission; transmit enable defaults true and can be disabled. Save/read back the intended V3 silence setting and measure silence across reboot/reconnect. The later designated reply gateway needs its separate transmit-enabled test. Avoid frequency/duty-cycle overrides. [LoRa configuration](https://meshtastic.org/docs/configuration/radio/lora/).

Attach the correct LoRa antenna before power/flashing; official Heltec device guidance warns against possible radio damage without one. [Heltec hardware guidance](https://meshtastic.org/docs/hardware/devices/heltec-automation/lora32/). Region selection is a software prerequisite, not an equipment authorization finding. Actual board authorization, antenna and power configuration remain to check against the applicable FCC conditions; private channels/consent do not resolve them. [47 CFR 15.247](https://www.ecfr.gov/current/title-47/section-15.247).

## V3 MQTT prerequisites and limits

Hardware provisioning finding, 2026-10-14: the pinned release's NanoPB option allocates 32 bytes for `MQTTConfig.password`, including termination; only 31 UTF-8 bytes fit. Generated 48-character broker passwords authenticate in software but cannot be applied to these stock radios. Use compatible gateway credentials rather than truncating a password only on the client. The guarded broker fix was subsequently applied by the owner; both gateways now use compatible 30-byte passwords and pass real MQTT delivery/reboot checks (see TEST-003 in records/field-results.md). [Pinned option](https://github.com/meshtastic/firmware/blob/54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb/protobufs/meshtastic/module_config.options), [generated field](https://github.com/meshtastic/firmware/blob/54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb/src/mesh/generated/meshtastic/module_config.pb.h#L141).

The project endpoint is `mqtt.snorr.org:8883`; transport verification is recorded separately in [hosting evidence](../../records/sites.md#broker-hosting-record--mike-rollins). Configure device Wi-Fi, MQTT enabled, TLS enabled, client proxy disabled, the agreed private root and per-gateway credentials privately. Enable uplink on the tracking channel; leave all downlinks disabled for initial passive tests. Map reporting should be disabled. Decide payload encryption/JSON deliberately: JSON is plaintext at the MQTT payload layer, and disabling MQTT encryption sends decoded data even when the radio channel uses a key. TLS protects transport separately. [MQTT configuration](https://meshtastic.org/docs/configuration/module/mqtt/).

Current upstream `MQTT.cpp` parses `host:port` and defaults to 8883 for TLS, 1883 otherwise. Uplink gating for other nodes checks the packet's OK-to-MQTT bit when the broker's connected IP is public. A privately owned broker behind a public IP does not qualify for the private-IP bypass. Set/check member `lora.config_ok_to_mqtt` for the authorized private uplink and test actual forwarding. All-disabled channel downlinks avoid MQTT subscriptions; test alongside broker ACLs. Queuing is bounded and can discard oldest packets, so outage recovery cannot be assumed lossless. Recheck these moving-source observations on the pinned build. [Upstream MQTT implementation](https://github.com/meshtastic/firmware/blob/master/src/mqtt/MQTT.cpp).

The local pinned-build review confirms its direct TLS path calls `setInsecure()` at line 549 and its connection log includes username/password at line 328. Encrypted transport alone therefore does not demonstrate device certificate/hostname verification. Sanitize serial logs and keep originals private. Its `onSend` lines 780–787 also confirm packet-bitfield gating on public broker IPs, so the member OK-to-MQTT prerequisite applies to this baseline. [Pinned MQTT TLS path](https://github.com/meshtastic/firmware/blob/54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb/src/mqtt/MQTT.cpp#L549), [pinned connection logging](https://github.com/meshtastic/firmware/blob/54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb/src/mqtt/MQTT.cpp#L328), [pinned uplink gate](https://github.com/meshtastic/firmware/blob/54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb/src/mqtt/MQTT.cpp#L780).

## Readiness implication

Official sources support a stock-firmware configuration-first bench. They do not identify a mandatory source patch before initial GPS/radio/MQTT tests. Owned revision/frequency/GPS/power/antenna identification, matching built images, saved configuration and authenticated external broker delivery/ACL tests remain prerequisites to a reproducible connected bench. A local GPS/radio bench can proceed independently of portal ingestion once its hardware/configuration checks pass. Full dispatch end-to-end verification still requires a real packet adapter and selected-build packet evidence.
