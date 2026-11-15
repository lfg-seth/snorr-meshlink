# G004 replacement Heltec V4 gateway - 2026-10-24

Owner retires the failed V3 G004 **`!849ae664`** and selects a Heltec V4 with
its default GPS and an INA219 wired to **SDA17/SCL18** as replacement G004.
The connected V4 independently identifies as **`!699c2ed8`**, previously
**B001**, hardware device ID **`d4d91213c6f862de7a81383bc8843e59`**, USB
**`90:70:69:9C:2E:D8`**, COM5, original **heltec-v4 / 2.7.26.54e0d8d**.
This reassigns existing hardware; it does not add a V4 or preserve B001 as a
second simultaneous device. Historical B001 measurements retain their identity.
The [V3 failure/commissioning record](g004-gps-time.md) remains historical.

## Selected firmware and profile

Published fork target **`heltec-v4-gateway`** inherits ordinary **heltec-v4**,
including OLED, 16 MB flash/2 MB PSRAM, I2C SDA17/SCL18 and default GPS support.
Its only added flags enable the existing passive SNNS collector and select a
180-second fallback. Source **`a56466d8c`** is published on `snorr/develop`;
no collector, sensor, GPS or RF implementation is changed. Ordinary V4 and
V4 TFT/R8 targets remain distinct. Source publication is not a release asset.

Requested saved profile:

- **G004 / SNORR Pilot Gateway G004**, CLIENT, existing private US pilot radio
  profile with RF TX enabled. Preserve this V4's **10 dBm configured radio
  power**, FEM selection and individual security keys.
- Default GPS enabled with the existing **MCU RX39/TX38, enable34** settings;
  refresh 120 seconds, ordinary position broadcasts 300 seconds, smart/fixed
  position off. Do not apply the retired V3's GPIO45/46 overrides.
- Default bench Wi-Fi and the latest reboot-verified G003 encrypted TLS MQTT
  uplink profile; channel downlink off. Reuse the existing uplink account;
  separate broker-account/portal registration is a later acceptance step.
- Enabled **device and INA219 power telemetry at 180 seconds**; environment
  off. The owner's INA219 wiring shares the V4 OLED bus at **SDA17/SCL18**.
- Neighbor collector enabled with **over-LoRa SNNS**, following the saved
  **180-second device interval**, plus jitter, scheduler and airtime admission.
  This selects radio mode to meet the requested three-minute SNNS baseline;
  G003's local-only mode has an independent 60-second baseline. Standard
  NeighborInfo remains separate at 21,600 seconds.

Full original profile/keys and raw flash evidence are private under ignored
`private/bench/G004-v4-20261024/`. No member roster, credentials or GPS tracks
belong in Git. A new logical gateway label does not update the live portal's
historical B001 identity or retired V3 mapping automatically.

## Build and image evidence

Clean published source **`a56466d8c127929c22a959b659296d8ddfb17921`** builds
**heltec-v4-gateway / 2.7.26.a56466d** with Windows PlatformIO 6.1.19,
Espressif platform 6.13.0 and GCC 8.4.0. Full target build passes in **387.84
seconds**, using 107,508 / 2,097,152 RAM bytes and 2,118,541 / 6,553,600 flash
bytes. All four existing sanitizer-backed SNNS module/collector configurations
pass under WSL: 180/300-second fallbacks and 32/10-entry capacities. Existing
dependency warnings remain; this is not a warning-free build claim.

The exact **2,118,976-byte application** has SHA256
`c5d0f0ff9c1f5ec6aad689d5b1744f4a82861c44b1bc71ee9f69035b81969901`.
Build-manifest MD5/size and original partition-table equality pass. The
original **16,777,216-byte full flash backup** has SHA256
`751e35157c10ef6ac0b74857cd5ba27bbc24799b9a950c3a26808789e6b13de6`.
Its active OTA selection is app0, starting at **`0x10000`**, with a 6,553,600-byte
application allocation. Application-only installation and independent esptool
digest verification pass at **`0x10000`**. Bootloader, partition table, recovery
application, filesystem and settings are retained; no erase/factory reset is
used. A fresh API read passes complete original-profile and identity equality.

## Acceptance evidence

Complete intended owner/hardware/key/channel/local/module equality passes
after configuration and again after an explicit reboot, final capture
**2026-10-24T18:03:26Z / 11:03:26 Pacific**. The source/firmware/target read back
as selected. Existing individual PKI keys, 10 dBm power/FEM, default GPS pins,
US region and pilot radio settings are retained. G003's Wi-Fi/MQTT/channel
profile is copied without its security identity; no other board is written.

Serial logs identify **L76K** and show **PowerTelemetry initializing/opening
INA219**. No current GPS lock is observed. Owner confirms the device is
**indoors without clear sky view**; receiver communication passes, while a
fresh satellite fix/clock and time-bearing position transmission remain open.
GPS clock propagation needs
a receiver without a competing clock source; MQTT or local GPS receipt alone
does not establish mesh time adoption. INA219 detection/reports do not establish
physical calibration, shunt/polarity, battery-only behavior or runtime.

The manufacturer's [V4 pin reference](https://resource.heltec.cn/download/WiFi_LoRa_32_V4/datasheet/WiFi_LoRa_32_V4.2.0.pdf)
and the selected fork's V4 variant define the board wiring; the existing saved
MCU UART settings agree with `GPS::createGps()`'s RX/TX defaults. Model label,
cold boot, fresh fix/time and field/runtime acceptance remain distinct checks.
