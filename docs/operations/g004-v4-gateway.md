# G004 replacement Heltec V4 gateway - 2026-10-24

Owner retires the failed V3 G004 **`!849ae664`** and selects a Heltec V4 with
its default GPS and an INA219 wired to **SDA17/SCL18** as replacement G004.
The connected V4 independently identifies as **`!699c2ed8`**, previously
**B001**, hardware device ID **`d4d91213c6f862de7a81383bc8843e59`**, USB
**`90:70:69:9C:2E:D8`**, COM5, original **heltec-v4 / 2.7.26.54e0d8d**.
This reassigns existing hardware; it does not add a V4 or preserve B001 as a
second simultaneous device. Historical B001 measurements retain their identity.
The [V3 failure/commissioning record](g004-gps-time.md) remains historical.

## Planned power hardware

Owner specifies **4 × 18650 cells** and **2 × 100 × 60 mm solar panels** for
G004 on 2026-10-24. Record this as the intended assembly; installation and
operation have not been verified. G004-specific cell model/capacity, pack
wiring, panel electrical ratings/wiring and charging hardware remain unknown.
Do not infer pack capacity, solar wattage or runtime from these quantities.
Confirm the actual parts and power path before a battery/solar acceptance run.

## Selected firmware and profile

Published fork target **`heltec-v4-gateway`** inherits ordinary **heltec-v4**,
including OLED, 16 MB flash/2 MB PSRAM, I2C SDA17/SCL18 and default GPS support.
Its only added flags enable the existing passive SNNS collector and select a
180-second fallback. Source **`a56466d8c`** is published on `snorr/develop`;
no collector, sensor, GPS or RF implementation is changed. Ordinary V4 and
V4 TFT/R8 targets remain distinct. Source publication is not a release asset.

Reboot-verified saved profile:

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
No brownout marker is observed in this run's captured console; hard-power
cycling remains untested.

An independent validating-TLS subscriber receives **two fresh automatic
reports of each device/power/SNNS type through all four gateways**, including
G004's own MQTT uplink and RF reception by G001/G002/G003. Retained packets,
MQTT-origin packets, unsupported sources and per-gateway duplicates are
excluded. These are short bench delivery observations, not portal acceptance.

| G004 own-uplink report | First receipt UTC | Second receipt UTC | Receipt gap | Source gap |
| --- | --- | --- | --- | --- |
| Device | 18:04:35.486 | 18:07:35.543 | 180.057 s | 180 s measurement clock |
| INA219 power | 18:05:00.488 | 18:08:00.532 | 180.044 s | 180 s measurement clock |
| SNNS | 18:04:40.414 | 18:07:55.448 | 195.034 s | 195 s uptime |

All other gateways also carry **180-second device/power measurement gaps** and
the same SNNS boot/sequence pair: sequence **1/2**, source uptime **72/267 s**.
The **195-second** SNNS gap includes jitter/scheduler delay above the saved
180-second baseline. Device voltage reports **4.372–4.373 V**; INA219 channel
1 reports **4.192–4.196 V / -0.1–0.0 mA**. These are literal reported values,
not calibrated physical voltage/current or a charging interpretation. No
environmental measurement is enabled. No position packet/fix is observed.

GPS clock propagation needs a receiver without a competing clock source;
MQTT or local GPS receipt alone
does not establish mesh time adoption. INA219 detection/reports do not establish
physical calibration, shunt/polarity, battery-only behavior or runtime.

Serial and MQTT handles close after the second complete cycle. Raw capture,
configuration summary and `delivery-summary.json` remain in the private evidence
directory in the original shared checkout. Firmware source is published and
pinned through this repository; no new firmware release, broker account,
server/portal migration or other-board change is performed.

Concurrent work changes the shared checkout's branch during this run. Copy the
six G004 record files into the attached **g004-v4** worktree, preserving the
other chat's committed fleet summary. Automatic approval rejects restoring or
deleting the shared copies because concurrent edits could be lost; leave them
intact and finish records on **`codex/g004-v4`** in the isolated worktree.

The manufacturer's [V4 pin reference](https://resource.heltec.cn/download/WiFi_LoRa_32_V4/datasheet/WiFi_LoRa_32_V4.2.0.pdf)
and the selected fork's V4 variant define the board wiring; the existing saved
MCU UART settings agree with `GPS::createGps()`'s RX/TX defaults. Model label,
cold boot, fresh fix/time and field/runtime acceptance remain distinct checks.

## Live portal and MQTT registration - 2026-10-24

Owner requests checking and completing G004's portal/MQTT registration.
Inspection finds live MQTT delivery already working with the existing shared
uplink account, but the portal worker still maps **`!699c2ed8`** to member B001
and has no G004 source/gateway entry. No dedicated G004 broker account is
required to repair that missing registration; broker credentials/ACLs and the
radio's verified profile remain unchanged. Separate account isolation remains
a future provisioning follow-up; broker SSH works, but unattended sudo does not.

At **18:18:45 UTC / 11:18:45 Pacific**, create backhaul **G004**, with the
verified V4 hardware ID, installed version/target, INA219 and GPS metadata,
180-second telemetry/SNNS baseline, and the planned **4 × 18650 / 2 × 100 ×
60 mm panels**. Capacity and panel electrical ratings remain unknown; solar
equipment/warnings are not activated from a plan alone. No coordinates are
invented: the gateway remains an unplaced bench device, with GPS fix/site
placement pending.

Move the active radio mapping from `members` to `infrastructure`, add the
gateway mapping and G004 identity, and remove B001's active worker identity.
Retain B001's existing device row, number, positions, assignments, readings,
receipts and events; mark its configuration retired/superseded by G004 and
move its former radio/hardware IDs into `retiredIdentity`. There is no active
B001 assignment. Exact historical row fingerprints pass before/after the
change, and every other device configuration/identity is preserved. B001
remains visible as a historical offline tracker in the current portal; new
packets update G004. The failed V3's ID is not registered as a working gateway.

The standard private backup **`meshlink-20261024T181646Z.tar.gz`**, SHA256
`b2219ae44675a00e5e128ed6ebbfdd2a10fb306dafdf8b23eed6141b7c17aea2`,
passes isolated database/API/history/credential recovery before the change.
The worker alone restarts for the root-owned MQTT configuration update;
application source, schemas, demo state, broker configuration and other radios
are not changed. Root-private preview/apply evidence is under
`/root/g004-registration-20261024/`; no credentials or full portal state are
published.

Fresh post-registration evidence passes through the production worker and
authenticated portal state. G004's own MQTT uplink supplies the accepted
device/power/SNNS packets; the same packets through G001/G002/G003 deduplicate
without losing their receipts. By **18:21:50 UTC / 11:21:50 Pacific**, the
portal shows device voltage **4.373 V** and INA219 channel 1 **4.192 V /
-0.1 mA**, measured at **18:21:37 UTC**, with valid device timestamps.
These remain uncalibrated reported values. G004 also transports normalized
R002/R003/R004/R006 traffic. B001's historical fingerprints remain exactly
unchanged after fresh G004 ingestion. The authenticated public HTTPS portal
independently returns G004 with those readings and the planned power metadata.

Python's default HTTP user agent receives Cloudflare 1010; use the existing
ordinary curl verification path with credentials on private stdin/files,
retaining certificate validation and edge protections. This does not require
an application/authentication/Cloudflare change.

Post-change backup **`meshlink-20261024T182314Z.tar.gz`**, SHA256
`97017c993cbbc7c7d745e760ce67d385c2134f2d1b9db34cd81aa0727fb27e11`,
passes isolated live database/API/history/credential recovery with **12 device
records** and all **3,370 historical positions** retained. The installed
verifier passes protected routes, public HTTPS/certificates and per-client
authentication throttling. Its first rate-limit assertion fails transiently;
the retry passes after the test window clears, without a configuration change.
The MQTT archive checker validates the latest **200 records**, observes four
new deliveries during its check, and all four live API/worker/Nginx/Tunnel
services are active. Native/mobile rendering, GPS fix/time sharing, a confirmed
map location, sensor calibration, cold boot and field/runtime remain separate.
