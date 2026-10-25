# R003 ordinary firmware and three-minute reporting - 2026-10-25

Owner reconnects R003 and requests latest firmware with three-minute telemetry.
Independently identify **RAK4631 `!05237743`**, USB serial
**`397EBE4F36E1F126`**, COM14, previously ordinary **2.7.26.0b65f2e**.

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
at **17:15:42 UTC / 10:15:42 Pacific**; only intended interval settings differ:

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

Validating-TLS MQTT subscription receives fresh, non-retained encrypted reports
through **G001 and G002**. The existing live adapter independently validates
source, transport gateway, metric units, measurement and receipt clocks.
Deduplicate by gateway/packet ID; exclude everything received before final
configuration completion at **17:15:46.816590 UTC**. No manual telemetry requests
are used for this observation.

Two distinct automatic reports of each type reach each gateway:

| Report | Source measurement gap | G001 receipt gap | G002 receipt gap |
| --- | --- | --- | --- |
| Device/battery | 180 s | 180.185 s | 180.185 s |
| Temperature/humidity | 180 s | 176.856 s | 176.854 s |
| SNNS | 195 s source uptime | 195.440 s | 195.442 s |

Device measurements report **4.249-4.260 V**. Temperature reports are
**23.218-23.227 degrees C**, humidity **34.704-35.063% RH**. AHT10-compatible
sensor initialization/open succeeds; this does not independently identify its
exact fitted part or establish calibration. Same-boot SNNS sequences **1/2**
advance uptime **78 to 273 seconds**. Source measurement cadence and gateway
receipt cadence remain distinct, as the environment timing demonstrates.
Serial and MQTT handles close after observation.

The documented `scripts/check-project.py docs` scope passes local inline links
and whitespace checks. Initial sandbox serial/DNS/submodule restrictions are
resolved with ordinary host access. No repository tool or firmware source code
changes, rebuild, factory reset, key rotation or bootloader update.

Authenticated portal ingestion/cadence metadata, calibrated sensor accuracy,
sustained operation, runtime, forced relay and field coverage remain separate
gates. No other radio or server metadata is changed.

Private full profiles, serial logs, image provenance and validating-TLS MQTT
capture remain under ignored `private/bench/r003-update-20261025/`.
