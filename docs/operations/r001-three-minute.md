# R001 ordinary firmware and three-minute reporting - 2026-10-25

Owner reconnects R001 and requests latest firmware with three-minute telemetry.
Independently identify **RAK4631 `!a65601b3`**, USB serial
**`AA474A4710B85C2C`**, COM8, previously ordinary **2.7.26.0b65f2e**.

## Image and saved configuration

Select the latest already verified ordinary RAK image used by R002/R004/R006:
**rak4631 / 2.7.26.4c96b9b**, published source
**`4c96b9ba0360f01752892a41d09ccacda82747bb`**. The current published and
project-pinned source is `6fea6aa68842c43be261f2aa3ca0565e2e48db10`;
changes since `4c96b9b` add Wi-Fi gateway health and a Heltec V4 target,
with gateway implementation guarded by `HAS_WIFI`. Reuse the exact reviewed
RAK binary without rebuilding. This selects a verified local image; no public
release asset or download pointer changes.

Application-only UF2: **1,519,104 bytes**, SHA256
**`f83039d32c8637beff30f1a8d06e8addd106ad817f611dbc440b9bac04c65206`**.
Verify hash, nRF52840 application bounds, matching USB serial and RAK UF2
Board-ID before writing. Preserve bootloader and saved configuration.

Fresh complete private owner/security/channel/local/module backup succeeds.
Independent post-flash readback verifies the target/version and exact original
profile equality. Complete intended profile passes again through explicit reboot
at **17:23:38 UTC / 10:23:38 Pacific**; only intended interval settings differ:

| Setting | Verified value |
| --- | --- |
| Role | CLIENT |
| Device/battery telemetry | Enabled, 180 seconds |
| Existing temperature/humidity telemetry | Enabled, 180 seconds |
| Power telemetry | Disabled; stored interval 180 seconds |
| Passive SNNS | Enabled over LoRa; saved device interval supplies 180-second baseline |
| Standard NeighborInfo | Separate 21,600-second interval |

Preserve keys, private channel, radio settings, names, battery-INA address,
debug API and all other saved settings. No additional sensor is inferred or
configured. Set time over the local API after final reboot verification.
SNNS retains jitter, changed-table gating and airtime deferral; its baseline
does not guarantee an exact three-minute reception.

## Delivery and remaining gates

Validating-TLS MQTT subscription observes non-retained, encrypted R001 reports
through G001/G002 using the existing live adapter. Source, gateway, metric units
and measurement/receipt clocks are independently validated. Deduplicate by
gateway/packet ID and exclude receipts before final configuration completion
at **17:23:43.145860 UTC**. No manual telemetry requests are used.

The enabled temperature/humidity setting does **not** establish sensor operation.
No fresh environment packet or sensor initialization/open evidence is observed
during this run. The exact fitted sensor/wiring/presence is unknown; do not copy
R003's successful AHT result onto R001. Confirm hardware and obtain a fresh
reading before accepting environmental reporting.

Two distinct automatic device packets and two same-boot SNNS reports reach
each gateway:

| Report | Source gap | G001 receipt gap | G002 receipt gap |
| --- | --- | --- | --- |
| Device/battery | 240 s measurement | 239.478 s | 239.478 s |
| SNNS | 195 s uptime | 195.398 s | 195.396 s |

Battery measurements are **4.174 and 4.181 V**. SNNS sequences **1/2** advance
source uptime **74 to 269 seconds**. An additional independent serial connection
at 17:28 verifies exact intended-profile equality, including the stored
**180-second** device interval. It observes the second automatic device send at
**17:28:29 UTC**, source uptime **306 seconds**; the same packet arrives through
both gateways. The device remains on the same boot; no extra configuration write
or manual report request is used. The longer device gap is measured evidence,
not three-minute delivery acceptance. Airtime admission/scheduling may defer
telemetry in the source, but the cause of this specific delay is **unknown**.
Capture ends without a fresh environment packet. Serial/MQTT handles close.

The documented `scripts/check-project.py docs` scope passes local inline links
and whitespace checks. No firmware or repository tool source changes, rebuild,
factory reset, key rotation or bootloader update.

Authenticated portal ingestion/cadence metadata, calibrated sensor accuracy,
sustained operation, runtime, forced relay and field coverage remain separate
gates. No other radio or server metadata is changed.

Private full profiles, serial logs, image provenance and validating-TLS MQTT
capture remain under ignored `private/bench/r001-update-20261025/`.
