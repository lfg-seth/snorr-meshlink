# G007 screenless V4 logging gateway

**Current rollout identity, 2026-11-12.** This screenless board is now G001.
The names below record the earlier bench test. [Production rollout](g001-screenless-rollout.md).

## Installation on 2026-11-12

The owner identifies the selected board as Heltec V4.3 with KCT8103L. USB and
esptool independently identify MAC **F8:5B:1B:BF:06:38**, ESP32-S3 v0.2,
embedded 2 MB PSRAM and 16 MB quad flash. Both external antennas are attached.
The screenless board routes 2.4 GHz to IPEX by default according to
[Heltec's board description](https://heltec.org/project/wifi-lora-32-v4/).
G007 uses node **!1bbf0638** and its own first-install PKI. The project pin
is [firmware 898c113b5](https://github.com/lfg-seth/firmware/commit/898c113b51975a92fbb3cdc7c441f0224c3bd88f).

The original diagnostic recovery image is 16,777,216 bytes, SHA-256
`1af5e2dc5b1de0d88b7e11f0458ae401f5288743f9d1101c85377f7c75559014`.
A second complete pre-install backup has SHA-256
`171542b772b785031aaad0d4ae8801a9fbfe3babe9ad4615d24352161c22543f`.
A serial read at 460800 baud lost a block. The retry compared every 128 KiB
block against the original backup plus the installed diagnostic, read differences
at low speed and matched the final 16 MB reconstruction to the chip's whole-flash
digest. Both recovery files are private.

The original 0x140000 application partition is too small. The checked 16 MB
table retains NVS and OTA-data offsets, selects app0 and allocates 0x640000
bytes for it. Both the former filesystem and the new filesystem area were
blank in the verified current backup. This installation wrote the three
ranges below with the same identified esptool handle. Independent chip
digests passed for each range, the preserved NVS and OTA selection.

| Address | Image | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| 0x0 | Bootloader | 15,104 | `2a71d69b471e20c2bac7fb469f3c6a807b3ebee780e348e5889db0da849ca363` |
| 0x8000 | Partitions | 3,072 | `bd0f7954aca2ef7d925ee21aaa1f3dc8822d1d6ce5cbbd26a135e5886bfff6ce` |
| 0x10000 | heltec-v4-sd-gateway 2.7.26.898c113 | 1,901,968 | `10774ff8a4116bf79a1b61d47c4e3cb1a3fa76280bc1a26c980fee9716514bf5` |

The ESP32 build used 103,296 bytes static RAM and 1,901,537 / 6,553,600 bytes
of app flash. Windows required the documented short PlatformIO package path.
The private recovery directory is `private/bench/v4-gateway-20261112/`.
Following repartitioning, restoration of the old diagnostic requires the
original partition layout and boot state, or this board's complete backup.
The earlier app-only restoration procedure applied to its earlier layout.

## Profile and source verification

First installation began with region UNSET and no PKI. The board generated
its own keys when the pilot region was applied. The full intended protobuf
configuration, channels, owner, hardware identity and keys matched through
an explicit reboot. G007 uses CLIENT, rebroadcast NONE, private encrypted
uplink, TLS, NTP, no downlinks, no sleep and a 300-second baseline for device,
power, passive SNNS and SNGH. The verified V4.3 setting enables the FEM LNA.
The runtime selected the KCT8103L gain curve at the requested 10 dBm.
The firmware's dedicated HSPI uses 47/48/6/4 for SCK/MOSI/MISO/CS at 1 MHz.
INA219 uses SDA17/SCL18. The gateway disables active NodeInfo solicitation,
standard NeighborInfo and both relay paths in the target build.

The independent reviewer checked the pinned firmware and application diffs.
Review fixes covered broadcast duplicates, TX queue eviction, active discovery,
spliced or oversized segments, readable position/telemetry, and unknown-clock
receipt age. The disposable FAT fixture retained six-month-old data with free
space and reclaimed the oldest closed file under pressure. It also exercised
foreign files, mixed-boot corruption, missing cards and failed writes. The
native encoder and encrypted adapter agreed on the 52-byte SNSD v1 vector,
including byte counts beyond JavaScript's safe integer range. The daily
scheduler fixture exercised reboot, unknown time, NTP acquisition and forward
clock corrections. [Firmware contract and card format](../../firmware/SNORR_SD_GATEWAY.md).

Open [the offline reader](../../scripts/sd-reader/index.html) in desktop
Edge or Chrome and select physically copied SML files. Read and export remain
local. Tests processed 182,000 synthetic radio events across 182 segments.
A headless Edge test opened the actual reader from disk and verified
reconstructed time labels, text escaping, pagination, filtering and CSV/JSON
output using a test destination for the streaming file picker. Archive raw
member and packet evidence only in private storage.

[MeshLink 0.2.0](https://github.com/lfg-seth/snorr-meshlink/tree/meshlink-v0.2.0)
includes the adapter, PocketBase observations/receipts and state API, device
card and demo states. The clean release built from 205b1909 with 64 portal
tests and 92 backend cases (seven POSIX launcher cases skipped on Windows).
[Tag portal CI](https://github.com/lfg-seth/snorr-meshlink/actions/runs/43348217162) passed.
[Tag backend setup](https://github.com/lfg-seth/snorr-meshlink/actions/runs/43348217221) failed because Ubuntu 26.04 lacks
the pinned Python 3.14.3 binary. The subsequent main-branch CI-only change
selects Ubuntu 24.04 and [hosted backend checks passed](https://github.com/lfg-seth/snorr-meshlink/actions/runs/43348447576).
The records workflow uses the same supported Ubuntu runner. [Hosted records checks](https://github.com/lfg-seth/snorr-meshlink/actions/runs/43350096644).
Local checks passed for 81 bench tests, 10 firmware-release tests, three
offline-reader tests and both native firmware fixtures. PocketBase and portal
release checks ran against the tagged application source.

Production remains on its prior release. Deploying 0.2.0 requires selecting
the production rollout, registering G007 as a backhaul device and adding its
radio identity to both the MQTT gateway and infrastructure mappings. Verify
its current device card and receipt provenance after deployment.

## Live bench evidence

The first automatic SNSD v1 report reached G007's own encrypted MQTT uplink
at 69 seconds uptime with NTP source, 86,400-second interval, healthy mounted
storage, **393,216 / 31,902,400,512 bytes used** and zero discarded records
that boot. The early serial log showed unknown UTC before NTP acquisition over
Wi-Fi. The INA219 driver found 0x40, and power telemetry included 4.220 V
and -0.2 mA in an observed sample. Shunt calibration and whole-battery
current require separate measurements.

During a 1,014-second continuous observation after reboot, the TLS subscriber
received four distinct automatic packets per stream through G007 and through
G001. Each row below spans three consecutive receipt intervals in seconds.

| G007 report | Via G007 | By radio via G001 |
| --- | --- | --- |
| Device | 300.1, 300.1, 300.1 | 300.4, 300.1, 299.7 |
| INA219 power | 300.1, 300.1, 300.1 | 300.1, 300.1, 300.1 |
| Passive SNNS | 315.1, 315.1, 315.1 | 314.2, 315.1, 315.0 |
| Backhaul SNGH | 315.1, 315.1, 315.1 | 315.0, 315.3, 314.9 |

All 22 intact paired radio counter samples showed zero relays. The last
reported 92 good receptions. G001 independently uplinked G007's own radio
reports, while G007 uplinked incoming RF during the same window.

The first daily generation preceded G001 power-up. After the cadence test,
G007 transmitted the identical 52-byte report once from USB with a new mesh
packet ID. The subscriber decrypted matching source time, boot, sequence and
storage data through both G007 and G001. No second automatic daily generation
occurred across the observed reboots. The daily interval stayed at 86,400 s.
A local MQTT proxy input was explicitly rejected on USB. All channel downlinks
and the client proxy were disabled in the verified profile. The target also
returns immediately at its broker-receive entry point.

A disposable, loopback-only MeshLink 0.2.0 backend ingested the actual three
receipts (original direct, repeat direct, repeat through G001) and stored one
SD observation. The authenticated state API returned the exact used and total
byte counts with zero dropped records. Both gateway IDs were retained on the
receipts. Production deployment and authenticated production verification
remain separate.

The bench matched five distinct incoming packet IDs and two locally generated
packet IDs from SD sync diagnostics to encrypted MQTT receipts in that window.
G007 uplinked 38 unique incoming packets. Intact sync counters reached 371
frames and reported zero drops. A physical retrieval of those SML files for
independent examination remains open.
The disposable storage fixture exercised rotation and faults without filling
the owner's card.

For the outage test only, G007 used an unavailable Wi-Fi network name. G001
received its RF backhaul report 93 seconds after the test began, at 73 seconds
of device uptime, with Wi-Fi and MQTT both disconnected and source time
unknown. Restoring the saved network configuration rebooted G007. Its complete
profile and own identity matched the saved intent. An NTP-timed online report
at 71 seconds uptime arrived on G007's TLS uplink 96 seconds after starting
restoration and on G001's uplink at 97 seconds. The serial handles and MQTT
observer were closed after recovery.

Bench limits include full physical card integrity, day-long retention under
traffic, field coverage and solar endurance. The existing direct MQTT client
uses TLS without verifying the broker certificate. The private observation
client used certificate validation. The power pack, charger and panels were
outside this installation.
