# G003 mobile Heltec V3 gateway - 2026-11-14

Owner requests a full wipe without backup of the connected V3, fresh label
G003, supplied vehicle Wi-Fi, no association test while that network is absent,
and no portal registration. This is mobile vehicle backhaul, without a fixed
site or position. The saved default bench Wi-Fi is unchanged.

## Physical identity and image

COM6 independently identifies **HELTEC_V3 / ESP32-S3 / 8 MB**, radio
**!849ad7a0**, hardware **47af7bdcb7950e6e07f8ef108ef19fab**, CP210x USB
serial **0001**. This is the former G002 V3, not the new screenless G002.
Historical G002 records remain historical; this physical unit now bears G003.
No stock addition, purchase, sensor allocation or battery capacity is inferred.

Full-chip erase, factory image at **0x0**, filesystem at **0x670000**, and
independent esptool digest verification pass. No old configuration or flash
backup was made. Selected existing **heltec-v3-gateway / 2.7.26.6fea6aa**,
published source **6fea6aa68842c43be261f2aa3ca0565e2e48db10**; no rebuild.
Manifest target, sizes/MD5, partition table and factory-embedded application
match the previously verified V3 application SHA256.

| Image | SHA256 |
| --- | --- |
| Application | `c26a61e96b4553958c4632bb4074e89bbea0a214dbed15289cc2bbf54f5263f7` |
| Factory | `aa5fde22d0bc4e23be18dadeb9aa8c82d3ccbd9b9472ec903b547653be4ab4cb` |
| Filesystem | `1edd1dc3ae6f691567ada95eba5cae9009f85e9640c35319b95eef5009ed6cc7` |

## Installed profile and verification

- **SNORR Gateway G003 / G003**, CLIENT; US/LONG_FAST, private pilot channel,
  slot 35, 10 dBm configured power, hop limit 3, LoRa TX enabled.
- Newly generated own PKI pair; mathematical public/private consistency and
  separation from the template gateway's keys pass. No prior keys restored.
- Supplied vehicle Wi-Fi enabled; exact stored SSID/password verified privately.
  Existing private MQTT uplink account/root retained from the pilot template;
  encrypted TLS enabled, channel downlinks and JSON/map/client proxy disabled.
- Device telemetry **180 seconds**; neighbor collector enabled over LoRa,
  standard NeighborInfo **21600 seconds**. Custom SNNS/health use the saved
  baseline subject to scheduling, jitter and airtime admission.
- No fixed position, GPS disabled, power saving disabled; external environment
  and power telemetry disabled because fitted sensors are unconfirmed.

Complete intended owner/key/channel/local/module profile comparison passes
after configuration and again after an explicit reboot, with the exact target
and version read back. Serial handles are closed. Debug API logging remains
disabled. Private intended/final profiles, credentials and logs remain
ignored under `private/bench/g003-mobile-20261114/`.

Wi-Fi association/direct MQTT, paired RF, portal delivery, vehicle power/runtime
and field coverage were not tested. No portal record, registry, mapping, history
or server setting was changed; existing historical mappings may still label
this hardware with its old identity. When the vehicle network is available,
verify association and direct uplink if the owner selects that check.
