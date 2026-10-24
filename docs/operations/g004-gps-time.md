# G004 GPS time support

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
