# R002 ordinary firmware and three-minute INA219 reporting - 2026-10-24

Owner reconnects R002, requests the same latest firmware/three-minute update
as R004 and explicitly confirms **R002 also has an INA219**. This supersedes
its earlier no-INA219 sensor selection, preserving existing environment
telemetry. Fitment does not establish calibrated current or its physical path.

## Image and preservation

Identify **RAK4631 `!b456f760`**, USB serial **`BADB1E79E9739FC4`**, COM9.
Privately back up the full original owner/identity/keys/channel/local/module
profile from ordinary **2.7.26.0b65f2e** before any write.

Published `snorr/develop` and the project pin both select source
**`4c96b9ba0360f01752892a41d09ccacda82747bb`**. Reuse the same reviewed ordinary
**rak4631 / 2.7.26.4c96b9b** application as the
[R006 bench](repeater-update.md#r006-and-gateway-admin-bench---2026-10-24) and
[R004 update](r004-three-minute.md), without rebuilding. UF2 **1,519,104 bytes**,
SHA256 **`f83039d32c8637beff30f1a8d06e8addd106ad817f611dbc440b9bac04c65206`**.

Image hash, nRF52840 application bounds and matching RAK USB volume pass.
Application-only flashing retains bootloader and saved configuration; a fresh
independent API read verifies the ordinary target/version and complete
original-profile equality at **17:44:03 UTC / 10:44:03 Pacific**. This explicitly
selected local build does not change the public release/download pointer.

## Saved profile and verification

Complete intended-profile/identity/key comparison passes through explicit
reboot at **17:45:48 UTC / 10:45:48 Pacific**. The first verifier reaches a
successful pre-reboot profile read, then the SDK's serial-close double-flush
races with USB disconnection during the requested reboot. A fresh independent
API connection verifies the complete intended state without repeating flash
or configuration writes. Set device time locally after this final comparison.

| Setting | Verified value |
| --- | --- |
| Role | CLIENT |
| Device/battery telemetry | Enabled, 180 seconds |
| Existing temperature/environment telemetry | Enabled, 180 seconds |
| INA219 power telemetry | Enabled, 180 seconds |
| Passive SNNS | Enabled over LoRa, saved device interval supplies 180-second baseline |
| Standard NeighborInfo | Separate 21,600-second interval |

Preserve original names, keys, private channel, radio profile, other
local/module settings, display preferences and unset battery-INA address.
The only intended changes are telemetry cadence and enabling power
measurement; neighbor settings already match. R002's tracked updater sensor
profile now retains both environment and INA219 power, with the existing
offline sensor-exception check updated accordingly.

SNNS retains jitter/cooldown/airtime deferral and requires
changed passive direct receptions; it does not send empty/unchanged tables.
The 180-second setting is its baseline rather than exact reception timing.

## Evidence and remaining gates

Validating-TLS MQTT subscription receives fresh, non-retained, encrypted
R002 device/environment/power/SNNS reports through **both G001 and G002**.
The live wire adapter independently decrypts/validates source and transport
gateway; duplicate packet IDs are excluded per gateway. Acceptance excludes
reports received before the final check at **17:45:48.633 UTC**.

First device telemetry measures **4.093 V** at **17:46:09 UTC**. Environment
at **17:46:34 UTC** contains INA219 **4.068 V / -227.8 mA**, with **no
temperature or humidity fields**. PowerTelemetry independently reports
**channel 1, 4.068 V / -229.2 mA**. Preserve the signed values without claiming
calibrated current, net charging or a confirmed physical measurement path.
Both gateways receive the new SNNS boot's sequence **1**, source uptime
**66 seconds**, at approximately **17:46:11.93 UTC**.

Two distinct automatic reports of each type reach each gateway after the
final reboot/profile check, without manual telemetry requests:

| Report | Measurement gap | G001 receipt gap | G002 receipt gap |
| --- | --- | --- | --- |
| Device/battery | 180 s | 179.929 s | 179.925 s |
| Environment / INA219 | 180 s | 179.734 s | 179.743 s |
| INA219 channel-1 power | 180 s | 180.018 s | 180.010 s |

Same-boot SNNS sequence **2**, source uptime **261 seconds**, follows sequence
1 by **195 source-uptime seconds**, consistent with the 180-second baseline
plus jitter/scheduling. G001/G002 receipt gaps are **194.870 / 194.867 seconds**.
Earlier boot/history packets are excluded. Serial and MQTT handles close.

The environment enablement does not establish a fitted/working temperature
sensor; its observed payload here is INA219 voltage/current. All **34 offline
updater checks** and changed-document link/whitespace checks pass with R002's
confirmed power-sensor exception.

Private immutable original/intended/final profiles, image provenance, serial
logs and validating-TLS MQTT captures remain under ignored
`private/bench/r002-update-20261024/`. Exclude earlier boots/history and duplicate
packets from cadence evidence. Authenticated portal receipt/cadence metadata,
physical sensor path/calibration, battery-only behavior, runtime, sustained
operation and field coverage remain separate gates. Other radios, server
mapping and portal metadata are unchanged; no stock/purchase/site change is
inferred.
