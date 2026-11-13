# G001 power reduction estimates

Research date: 2026-11-13. Scope: screenless Heltec V4.3 G001 / !1bbf0638,
firmware 2.7.26.898c113. Research only; no configuration, firmware, serial,
service or deployment changes. [Installed-board evidence](../operations/g001-screenless-rollout.md).

## Baseline and confidence

The owner reports about 160 mA constantly from the portal/INA219 and confirms
that its measurement path is uncertain. Treat this as an owner-reported reading,
not a calibrated whole-gateway input-current measurement. The existing
[peripheral evidence](../operations/heltec-v4-peripherals.md) and
[installation evidence](../operations/g007-screenless-gateway.md) leave shunt
calibration, polarity and whole-battery current unverified. USB input can include
battery charging; a battery-lead shunt can show net charging/discharging rather
than total system load. Establish voltage and shunt location before converting
to battery runtime or solar energy. Current at 5 V cannot be compared directly
with current at 3.7 V; compare power and include conversion losses.

## Published component and board figures

- Heltec's [V4.2 datasheet, table 3.4](https://resource.heltec.cn/download/WiFi_LoRa_32_V4/datasheet/WiFi_LoRa_32_V4.2.0.pdf)
  lists sleep as 20 microamps (0.020 mA) from battery/3.3 V and 2 mA from USB.
  It lists ordinary RX as 75 mA, without identifying it as an optimized
  light-sleep logger. The newer [V4.3.1 datasheet](https://resource.heltec.cn/download/WiFi_LoRa_32_V4/datasheet/WiFi_LoRa_32_V4.3.1_Datasheet.pdf)
  repeats these numbers. These are family references, not a measurement of our
  exact screenless V4.3 plus SD card and INA219. The table calls the low-current
  state Sleep; it does not specify an application-level test procedure.
- The [ESP32-S3 datasheet, low-power table](https://documentation.espressif.com/esp32_s3_datasheet_en.pdf)
  gives approximately 240 microamps (0.24 mA) for chip-only light sleep under its
  specified conditions. That does not include external flash/PSRAM retention,
  LoRa, FEM, SD, INA219, regulators or processing time.
- [Semtech SX1261/2 rev 2.2, table 3-5](https://resource.heltec.cn/download/WiFi_LoRa_32_V4/datasheet/SX1261_2%20V2-2.pdf)
  gives 4.6 mA LoRa 125 kHz RX and 5.3 mA boosted RX with DC-DC regulation;
  corresponding LDO values are 8.8 and 10.1 mA. These are chip figures under
  specified conditions, not our LONG_FAST whole-board measurement.
- The FEM maker's [product catalog](https://kxcomtech.com/en/product) lists
  KCT8103L RX current as 9 mA at 3.3 V and 18 mA at 5 V. Its
  [product page](https://kxcomtech.com/en/product/info/1774) describes the LNA
  and bypass path. The [exact V4.3 schematic](https://resource.heltec.cn/download/WiFi_LoRa_32_V4/Schematic/HTIT-WB32LAF_V4.3.pdf)
  and installed-board evidence establish the relevant FEM; G001 has LNA enabled.
  Bypassing it changes RF reception and requires coverage testing.
- [TI INA219 datasheet](https://www.ti.com/lit/ds/symlink/ina219.pdf) specifies
  0.7 mA typical operating supply current, 1 mA maximum; the module can add
  other loads. The exact reused SD card's idle/write current is unknown.

A plausible engineering target for continuous LoRa reception plus SD logging
with Wi-Fi off and the CPU light-sleeping between events is **20-40 mA average**
at a battery-like supply, under modest traffic with the LNA retained. This is an
inference and development target, not a vendor specification, guaranteed range
or bench result. Chip RX plus FEM and INA219 already accounts for roughly
15-20 mA on their local supplies before the card, CPU wakeups and other loads.
Frequent receptions, SD activity, regulator behavior, own RF reports or a poor
card idle state can push the total above this target. Simply switching Wi-Fi
off while leaving the CPU awake may leave tens of mA more; Heltec's ordinary
75 mA RX figure must not be relabeled as light-sleep performance.

## Sleep and recording behavior

In the low-current whole-node sleep arrangement, radio reception and recording
stop. Retaining an external LoRa receiver during CPU deep sleep is a different
architecture with receiver current and boot-per-event costs; it cannot deliver
the 20-microamp whole-board figure while listening continuously.

For the proposed light-sleep logger, the separate SX1262 remains receiving.
A packet IRQ wakes the CPU, which reads/processes the packet and writes or
buffers it for SD; the CPU cannot execute SD writes while asleep. It also wakes
for flushes, telemetry and upload timers. [Espressif sleep documentation](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/sleep_modes.html)
explains CPU/peripheral suspension and loss of Wi-Fi connections during explicit
light/deep sleep. This must be engineered and measured around recording and
radio deadlines rather than enabled as a blind toggle.

## Conditional upload estimates

Model all currents at the same supply point and voltage. Assume 25 mA average
between uploads (including reception, SD, wakeups and own RF reports), 160 mA
average while online, and successful sessions taking 30 or 60 seconds in total.
Session time includes Wi-Fi association, address/DNS setup, TLS/MQTT connection,
backlog transfer and delivery confirmation. The 160 mA online input is a
scenario parameter drawn from the owner's provisional reading, not a verified
input current. Firmware changes can also change online current.

Average = offline current + (online current - offline current) * online seconds / interval seconds.

| Schedule | 30 seconds online/session | 60 seconds online/session | Nominal reporting delay before upload |
| --- | ---: | ---: | --- |
| Continuously online, reported baseline | 160 mA | 160 mA | Live uplink |
| Every 15 minutes | 29.5 mA | 34.0 mA | Up to about 15 minutes plus transfer |
| Every hour | 26.1 mA | 27.3 mA | Up to about 60 minutes plus transfer |

These worked examples imply approximately 79-84% lower average current than
the assumed 160 mA baseline. They do not establish actual savings or runtime.
With a 20-40 mA offline baseline instead, those same 30-60-second scenarios span
about 25-48 mA for 15-minute uploads and 21-42 mA for hourly uploads.

The same amount of data per hour still has to move. Hourly uploads have four
times the per-session backlog at constant traffic, so equal session lengths
are sensitivity cases, not a prediction. Much of the interval benefit is fewer
reconnections. Poor signal or unavailable backhaul can dominate unless retry
attempts have bounded on-time/backoff. Keep logging during unsuccessful uploads.

## Existing implementation and required work

Read-only source inspection found:

- [Wi-Fi setup](../../firmware/src/mesh/wifi/WiFiAPClient.cpp) explicitly calls
  WiFi.setSleep(false) and esp_wifi_set_ps(WIFI_PS_NONE).
- [Power FSM](../../firmware/src/PowerFSM.cpp) omits normal light-sleep
  transitions while isWifiAvailable() is true. The Wi-Fi helper returns true
  for an enabled, configured SSID even when disconnected.
- [MQTT header](../../firmware/src/mqtt/MQTT.h) sets MAX_MQTT_QUEUE to 16.
  [MQTT source](../../firmware/src/mqtt/MQTT.cpp) discards the oldest queued
  entry on overflow. This RAM queue is not a durable hourly upload backlog.
- [Recorder](../../firmware/src/mesh/SnorrRecorder.cpp) has a separate writer
  task, 32-slot event queue and five-second sync target. The
  [SD contract](../../firmware/SNORR_SD_GATEWAY.md) and existing offline reader
  provide an archive, not automatic historical delivery to MeshLink.

A batch-uplink implementation needs persistent upload progress, restart/retry
recovery, reliable delivery confirmation, duplicate handling, bounded reconnect
attempts and concurrent reception/logging. Retain original GPS measurement and
receipt times; delayed history must never become a fresh position. The existing
15-minute stale criterion means a 15-minute upload cycle has no freshness margin;
hourly batches intentionally sacrifice live dispatch visibility when no other
awake gateway uplinks those packets. Health/watchdog logic must also understand
the intended schedule before deployment. Historical replay and freshness
presentation require coordinated backend work.

## Next useful measurements

1. Verify shunt placement, shunt value/calibration, polarity and supply voltage;
   compare with a meter at the entire gateway input, accounting for charging.
2. Establish the unchanged G001 average and peaks with its actual card, LNA,
   telemetry and representative traffic. Compare normal live operation with a
   selected Wi-Fi modem-sleep build that retains live uplink.
3. Benchmark a selected Wi-Fi-off light-sleep recorder prototype under quiet and
   busy traffic; correlate known packets with SD to detect losses. Measure the
   actual card's idle/write contribution and retained-memory overhead.
4. Measure reconnect plus upload energy for known 15-minute and hourly backlogs,
   including unavailable-Wi-Fi retry behavior, then substitute into the formula.

[Espressif Wi-Fi power saving](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/wifi-driver/wifi-performance-and-power-save.html#esp32-s3-wi-fi-power-saving-mode)
supports modem sleep while maintaining the AP connection. Investigating that
first may preserve live tracking with less development than batch replay; its
savings and compatibility with our gateway remain unmeasured. Research does not
select a new operating policy or authorize a hardware change.
