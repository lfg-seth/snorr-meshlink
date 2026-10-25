# R005 ordinary firmware and three-minute reporting - 2026-10-25

Owner reconnects R005 and requests latest firmware with three-minute telemetry.
Independently identify **RAK4631 `!f95b5501`**, USB serial
**`E93C5FF0F97DD76B`**, COM19, previously ordinary **2.7.26.0b65f2e**.

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
at **17:31:56 UTC / 10:31:56 Pacific**; only intended interval settings differ:

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

The reboot disconnects the serial stream before the helper finishes closing,
raising an `AttributeError` during cleanup after the settings write and explicit
reboot. A fresh independent connection verifies the complete intended profile,
target and version; no repeat flash or settings write is needed. Preserve the
existing Fahrenheit preference and disabled power reporting.

Validating-TLS MQTT receives fresh, non-retained encrypted R005 packets using
the existing live adapter with a temporary local observation mapping. This
mapping does not update the server. Validate source/gateway identity and clocks,
deduplicate gateway/packet IDs and exclude receipts before final configuration
verification completes at **2026-10-25T17:32:00.774307+00:00**. No manual telemetry requests are used.

Two distinct automatic device packets and two same-boot SNNS reports reach
each gateway. One fresh environment packet reaches each gateway:

| Report | Source gap | G001 receipt gap | G002 receipt gap |
| --- | --- | --- | --- |
| Device/battery, two packets | 240 s measurement | 240.535 s | 240.543 s |
| SNNS, two packets | 195 s uptime | 196.762 s | 196.759 s |
| Temperature/humidity, one packet | Not established | Not established | Not established |

Battery values are **4.241 and 4.259 V**. Same-boot SNNS sequences **1/2**
advance source uptime **101 to 296 seconds**. The fresh environment packet
reports **23.173 degrees C / 35.313% RH**, plus legacy sensor fields
**0.888 V / -0.1 mA**. Do not interpret those legacy sensor fields as calibrated
battery-path measurements; the distinct power module remains disabled.

An independent live connection again verifies complete intended-profile equality
at 17:36, including the saved **180-second** telemetry settings. It observes the
second automatic device send at **17:36:46 UTC**, uptime **306 seconds**.
At **17:37:12 UTC**, the log explicitly reports **Ch. util >25%. Skip send**
for environment telemetry, then reads AHT10-compatible metrics and sends a local
phone packet only (**23.190 degrees C / 35.265% RH**). This establishes an
actual environment RF airtime deferral, not a second gateway-delivered report.
The cause of the particular 240-second device gap remains unknown. Saved
three-minute intervals are verified; sustained three-minute radio delivery is
not accepted by this run. Serial and MQTT handles close after observation.

The documented `scripts/check-project.py docs` scope passes local inline links
and whitespace checks. No firmware/repository tool source change, rebuild,
factory reset, key rotation or bootloader update.

Authenticated portal ingestion/cadence metadata, calibrated sensor accuracy,
sustained operation, runtime, forced relay and field coverage remain separate
gates. R005 was removed from active portal inventory on 2026-10-24; this
firmware/configuration request does not recreate its server record. No other
radio or server metadata is changed. The ordinary target retains the prior
removal of the historical GPIO31 HIGH dummy-load override; physical circuit
state and current draw remain unverified.

Private full profiles, serial logs, image provenance and validating-TLS MQTT
capture remain under ignored `private/bench/r005-update-20261025/`.
