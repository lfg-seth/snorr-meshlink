# G003 gateway preparation - 2026-10-24

Owner requests flashing the attached Heltec V3 with INA219 as **G003**, with
telemetry enabled every **three minutes**, and supplies/corrects its private
Wi-Fi credentials. Only this board is written.

## Identification and first installation

- Independently identify COM6 as ESP32-S3 revision v0.2, 8 MB flash, MAC
  `9c:13:9e:9f:16:7c`. The original Heltec factory demo logs radio TX/RX activity
  and does not answer Meshtastic configuration requests. There is no original
  Meshtastic profile or PKI identity to preserve.
- Save all **8,388,608 original flash bytes** privately, SHA256
  `cd1be3b84921c22e7442ba3ceb0469a89b734416a28cd3d93f6ed8f03d08b1d9`.
  This is the board-specific recovery image; retain it before any future reset.
- Install dedicated **heltec-v3-gateway / 2.7.26.4c96b9b** from reviewed,
  published source `4c96b9ba0360f01752892a41d09ccacda82747bb`. Reuse the
  existing local build, validating its manifest and exact application SHA256
  `1fbe3acf8f91d8d9ae563cbeef8b412c17b58e830ebc79f96ee60767612e8cfe`.
  This remains an unpublished local build, not a new firmware release.
- First installation needs the bootloader/partition/application image rather
  than the existing-gateway application-only procedure. Write and independently
  verify these three images; no full-chip erase or Meshtastic factory-reset
  command is used:

| Offset | Image / bytes | SHA256 |
| --- | --- | --- |
| `0x0` | Gateway factory image / 2,176,528 | `b20363d20d8c8f371a4874ff4fbfd538bc655f5ff606049fa5821cc6d43d4810` |
| `0x340000` | Official ESP32-S3 unified OTA v1.0.1 / 636,544 | `3e62c5451afda604bac372444f058fc689dd588a87772ad4be90c228e04c1995` |
| `0x670000` | Matching gateway LittleFS / 1,572,864 | `6c59f5c30abd1a76cdb55ce25a0a65d7a7a4afdef49d627d824b88e560078800` |

The recovery image comes from the
[official release](https://github.com/meshtastic/esp32-unified-ota/releases/tag/v1.0.1)
and matches GitHub's published SHA256 asset digest. The factory image's embedded
application exactly matches the reviewed application above; its initial OTA
selection is app0. The recovery UI itself is not exercised.

## Saved profile and sensor

New Meshtastic identity is **`!9e9f167c`**, hardware device ID
`4393827189e95c03021dd7b37007a6a0`, short name **G003**, long name
**SNORR Pilot Gateway G003**. Initial US-region provisioning generates a new
32-byte PKI pair. Keys remain private and stable through subsequent changes and
explicit reboot.

- CLIENT, existing private pilot channel, US/LONG_FAST/slot 35/hop limit 3,
  **LoRa TX disabled**, channel uplink enabled and downlink disabled.
- Enabled Wi-Fi with the owner's corrected SSID/password. Enabled encrypted,
  TLS MQTT on the existing private endpoint/root. Reuse G002's existing uplink
  account; no separate broker account is provisioned and G002 is not changed.
- **Device telemetry enabled, 180 seconds. INA219 power telemetry enabled,
  180 seconds.** Environmental measurement remains disabled; no temperature
  sensor is reported by the owner.
- Neighbor collector enabled, local-only; standard NeighborInfo interval
  21,600 seconds. Custom gateway SNNS retains its separate 60-second minimum
  plus jitter; it does not inherit the three-minute telemetry interval.
- Boot scan detects **INA219 at 0x40 on the external I2C bus**; power telemetry
  initializes and opens it. This establishes sensor detection, not calibrated
  accuracy, polarity, battery-only behavior or the physical measurement path.

Complete intended owner/hardware/key/channel/local/module profile comparison
passes after configuration and through explicit reboot. The initial verifier
catches firmware's first-region initialization forcing `tx_enabled=true`
despite the requested false value. A second saved LoRa write disables TX, then
full profile and reboot comparisons pass. No continuous RF-silence claim is made
for that intermediate provisioning period. The corrected Wi-Fi is independently
verified with every other profile field preserved.

## Delivery and remaining acceptance

An independent subscriber verifies broker TLS and accepts fresh, non-retained,
channel-encrypted telemetry with G003 as both source and transport gateway.
Initial device report is **4.069 V** at **16:14:26 UTC**, received
**16:14:25.945 UTC**. Initial INA219 PowerMetrics channel 1 reports
**3.920 V / -489.4 mA** at **16:14:51 UTC**, received **16:14:51.397 UTC**.
These are literal reported values, not independently calibrated measurements;
the current sign is not assigned a charging/discharging interpretation.

The **275-second observation** receives two device and two power reports.
Second device report is **4.073 V** at **16:17:26 UTC**, received
**16:17:26.298 UTC**; second power report is **3.924 V / -489.3 mA** at
**16:17:52 UTC**, received **16:17:51.573 UTC**. Device/power receipt gaps are
**180.353 / 180.176 seconds**; their respective device-clock measurement gaps
are **180 / 181 seconds**. Both saved intervals are 180 seconds. Five own-source
telemetry packets are also captured through the local API; phone delivery has
its own cadence and is not the MQTT reporting-interval measurement.

Serial and MQTT handles close after observation. These two-report samples
verify the short bench cadence, not sustained delivery or clock accuracy.
Portal registration and authenticated portal acceptance are separate: this run
does not change production gateway/source mappings or create a portal record.
Battery allocation/capacity, antenna, site, shunt/polarity/calibration, sustained
delivery, runtime and field coverage remain unknown or unverified.

Full flash, private profiles, supplied Wi-Fi input, logs, manifests and raw
observations remain ignored under
`private/bench/G003-preparation-20261024/`. Do not publish those files.
