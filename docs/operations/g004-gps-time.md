# G004 GPS time support

**Replacement selected 2026-10-24:** owner reports this V3 failed hardware and
reassigns **G004** to existing Heltec V4 **`!699c2ed8`** (previously B001), with
default GPS and INA219 on SDA17/SCL18. Follow the
[V4 replacement record](g004-v4-gateway.md) for current work. The V3 evidence
and GPIO45/46 configuration below apply only to retired **`!849ae664`**.

## Commissioning attempt - 2026-10-24

**Owner hold:** on 2026-10-24 the owner disconnects G004 pending hardware
investigation and requests closing the chat. Stop bench work; serial is already
closed. Resume only when the owner brings the board/investigation forward.
The verified firmware installation remains recorded below; commissioning and
mesh time support remain incomplete.

Owner authorizes setting G004 up like G003 with GPS enabled, RF TX on and
normal position packets, then explicitly makes the old configuration disposable.
Only the connected **COM6 / Heltec V3** is written. Independently identify
ESP32-S3 revision v0.2 / embedded 8 MB flash, MAC **`b0:81:84:9a:e6:64`**,
node **`!849ae664`**, hardware device ID **`74bdf87af2ebb4a61d657eb19bf72422`**.

The original application does not complete a Meshtastic API connection. Its
partition table matches the existing gateway layout, with app0 selected. Install
and independently verify the **application only at `0x10000`**, dedicated
**heltec-v3-gateway / 2.7.26.4c96b9b**, SHA256
`1fbe3acf8f91d8d9ae563cbeef8b412c17b58e830ebc79f96ee60767612e8cfe`,
from reviewed source **4c96b9ba0360f01752892a41d09ccacda82747bb**. No build,
full-chip erase or factory-reset command. Bootloader, partition table, existing
**Meshtastic-OTA 0.3.0.47c250a** recovery app and filesystem are not overwritten.
The new application answers and identifies as HELTEC_V3 / heltec-v3-gateway.
No claim of equality with the inaccessible pre-update profile is made.

The original full flash had already been saved before the owner's later
no-backup instruction, SHA256
`42ba359d0f48d8076c3ee4ed79dab5a95d4f09c15d67accc283fb19fa0e40dc9`.
No further preservation work is required. Private evidence and setup helpers
are ignored under `private/bench/G004-preparation-20261024/`.

### Requested profile and failed persistence check

Use G003's **latest reboot-verified** corrected Wi-Fi/pilot/MQTT profile, which
matches the saved default bench Wi-Fi. Do not copy G003's identity or PKI keys.
Requested differences are G004's owner name, enabled GPS (MCU RX45/TX46), RF
TX enabled, GPS refresh **120 seconds** and ordinary position broadcasts every
**300 seconds**, smart/fixed position off. Device and INA219 power telemetry
remain **180 seconds**, environment off, encrypted TLS MQTT/uplink enabled,
MQTT downlink disabled and local-only neighbor collector as on G003. Reuse
the same existing uplink account; no broker/server writes.

**Setup is not complete.** The full-profile readback rejects the attempted
configuration. The captured console shows **five `BROWNOUT_RST` resets**,
also logged as `reset_reason=brownout`; the first interrupts the open settings
transaction after the network write and before commit. The last complete
readback has the owner name G004 but **region UNSET, GPS NOT_PRESENT, RX/TX
GPIO zero, Wi-Fi/MQTT off and device/power telemetry disabled**. A true stored
`tx_enabled` flag with region UNSET does not establish operational RF TX.
No completed PKI provisioning, GPS clock, outgoing position, telemetry cadence
or mesh time transfer is claimed. Serial handles are closed.

Boot repeatedly detects **INA219 at 0x40**. This establishes detection only;
power telemetry/calibration/path remain unverified. Chip identification also
reports flash voltage fixed to **3.3 V by eFuse**, rather than selected by GPIO45
on this chip. A physical cold-power test with the GPS fitted is still required.

When the owner resumes after hardware investigation/reconnect, check the power
path, reliable powered USB/short cable and a charged battery if fitted. Then
rerun configuration and require complete
intended-profile equality through explicit reboot before observing GPS time,
three-minute device/power telemetry and five-minute time-bearing position
packets. The firmware image verification passes; the power/reset and saved
configuration gates remain open. The exact supply/wiring fault is unmeasured;
do not attribute the brownout to the cable, GPS, INA219 or regulator without
further evidence, or disable brownout protection to bypass the failure.

## Initial source review - 2026-10-24

2026-10-24: owner reports another Heltec V3 with an INA219 and a GT-U7 GPS,
assigned **G004**. Purpose is mesh time for telemetry; gateway location is not
an operational requirement. Owner explicitly clarifies the physical wires as
**GT-U7 TX → Heltec GPIO45**, **GT-U7 RX → Heltec GPIO46**. Identity, installed
firmware, GPS output/baud, power wiring and operation have not been inspected.

## Configuration-first finding

No firmware source change is expected for an ordinary NMEA GPS on the pinned
**heltec-v3-gateway / 2.7.26.4c96b9b** source. The ESP32 architecture enables GPS,
the gateway target does not exclude it, and `GPS::createGps()` reads saved GPIO
overrides. For the owner's wiring the MCU-side settings are:

| Setting | Intended value |
| --- | --- |
| `position.gps_mode` | `ENABLED` |
| `position.rx_gpio` | `45` |
| `position.tx_gpio` | `46` |

These are proposed values, not applied/read-back configuration. GT-U7 is the
owner-reported module label; compatibility with this actual receiver's output
still needs a bench check. GPS and INA219 use separate UART/I2C interfaces.

`GPS::lookForTime()` can set `RTCQualityGPS` from valid NMEA date/time separately
from acquiring a location. Device and periodic INA219 power telemetry already
stamp measurements from the shared clock. This provides G004's own timestamps
once valid satellite time is acquired, including without internet or a phone.
It does not correct another node's already-generated telemetry timestamps.

## Sharing time over the mesh

Existing firmware shares usable wall-clock time in **position packets on the
primary channel**. A receiver without its own quality time source can adopt it.
The sender needs RF transmission enabled and a valid position; disabling
position sharing with precision zero also suppresses this time-carrying packet.
The current G001/G002/G003 receive-only profile therefore cannot simply be
copied unchanged to a G004 intended to supply mesh time.

The owner does not need G004's location for the application. If ordinary GPS
position packets on the private pilot channel are acceptable, mesh time support
is a configuration/verification outcome with no new protocol or firmware
feature expected. If the requirement becomes **transmit time with no coordinates**,
the pinned sender needs a bounded firmware change: it currently rejects empty
coordinates. A manual fixed location is not an equivalent workaround: the
current receive path rejects remote time marked with a manual/unknown location
source. No such firmware requirement or radio change is selected here.

## Remaining bench checks

Use the [board handoff](board-flashing-handoff.md) when a G004 bench run is
selected. Independently identify the board and back up its existing complete
profile before writes. Verify GPS serial output, valid current date/time and
`RTCQualityGPS`, then verify device/INA219 timestamps. Include cold boot with
the GPS powered: GPIO45/46 are ESP32-S3 strapping pins; an external signal on
GPIO45 can affect flash supply selection depending on the chip's eFuses.
Firmware cannot repair an incompatible reset-time strap level.

For mesh acceptance, use a selected transmitter profile and a second node
without a competing GPS/RTC/phone/NTP source. Demonstrate its clock becoming
`RTCQualityFromNet` from G004's primary-channel position packet, then verify
its subsequent telemetry timestamps. Remove internet/phone time during this
test to distinguish satellite/mesh time from NTP or API provisioning. Include
loss/recovery and relay checks separately before claiming sustained coverage.
No board, firmware, radio setting or server state was changed in this review.

## Evidence

- Pinned fork source **4c96b9ba0360f01752892a41d09ccacda82747bb**:
  [gateway target](https://github.com/lfg-seth/firmware/blob/4c96b9ba0360f01752892a41d09ccacda82747bb/variants/esp32s3/heltec_v3/platformio.ini),
  [ESP32 GPS support](https://github.com/lfg-seth/firmware/blob/4c96b9ba0360f01752892a41d09ccacda82747bb/src/platform/esp32/architecture.h),
  [GPS pin/time handling](https://github.com/lfg-seth/firmware/blob/4c96b9ba0360f01752892a41d09ccacda82747bb/src/gps/GPS.cpp),
  [position send/receive gates](https://github.com/lfg-seth/firmware/blob/4c96b9ba0360f01752892a41d09ccacda82747bb/src/modules/PositionModule.cpp),
  [device telemetry](https://github.com/lfg-seth/firmware/blob/4c96b9ba0360f01752892a41d09ccacda82747bb/src/modules/Telemetry/DeviceTelemetry.cpp),
  [power telemetry](https://github.com/lfg-seth/firmware/blob/4c96b9ba0360f01752892a41d09ccacda82747bb/src/modules/Telemetry/PowerTelemetry.cpp).
- [Meshtastic position configuration](https://meshtastic.org/docs/configuration/radio/position/),
  accessed 2026-10-24. The live documentation is version 2.8; behavior above is
  checked against this project's pinned 2.7 source rather than inferred from
  that documentation alone.
- [Espressif ESP32-S3 schematic/strapping guidance](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/schematic-checklist.html),
  [GPIO capabilities](https://docs.espressif.com/projects/esp-idf/en/v5.1.1/esp32s3/api-reference/peripherals/gpio.html)
  and [boot mode selection](https://docs.espressif.com/projects/esptool/en/latest/esp32s3/advanced-topics/boot-mode-selection.html),
  accessed 2026-10-24. GPIO46 supports output on ESP32-S3; its boot-strapping
  function still applies.
