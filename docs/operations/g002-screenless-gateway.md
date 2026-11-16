# G002 screenless SD gateway - 2026-11-14

**Deployment update, 2026-11-15:** owner selects G002 / Case 7 / eight cells /
Muzi for [Shady Hollow offline SD recording](g002-shady-hollow-deployment.md).
CLIENT/NONE retained, fixed coordinates saved, Wi-Fi/MQTT disabled; successful
SD sync/frame growth verified without networking. Identity/firmware retained.
The uplink/assembly state below records original commissioning.

The owner selects the newly connected Heltec V4 with SD and INA219 as fresh
**G002 / SNORR Pilot Gateway G002**, matching the current screenless
[G001 profile](g001-sd-cadence.md). USB identity is
**F8:5B:1B:BF:0A:B8**, radio **!1bbf0ab8**, initially COM39. Esptool confirms
ESP32-S3, embedded 2 MB PSRAM and 16 MB flash. Exact PCB subrevision, battery,
case, solar assembly and site are unconfirmed. Both antennas are owner-confirmed.

## Firmware and recovery

Installed **heltec-v4-sd-gateway-survey / 2.7.26.f6cdbeb**, published source
[f6cdbeb3f390f6dcf31c8e909cb4fcd1b24a9cdc](https://github.com/lfg-seth/firmware/commit/f6cdbeb3f390f6dcf31c8e909cb4fcd1b24a9cdc).
This adds an inherited SD-gateway target with the existing authenticated
direct-hop responder, based on published survey source bcb22e037. G001 itself
and the existing target remain unchanged. This is a responder, not the GPS tester.
[Exact prerelease and checksums](https://github.com/lfg-seth/firmware/releases/tag/snorr-sd-survey-2.7.26.f6cdbeb-pre.1).

| Image | Address | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Bootloader | 0x0 | 15,104 | `2a71d69b471e20c2bac7fb469f3c6a807b3ebee780e348e5889db0da849ca363` |
| Partitions | 0x8000 | 3,072 | `bd0f7954aca2ef7d925ee21aaa1f3dc8822d1d6ce5cbbd26a135e5886bfff6ce` |
| Gateway application | 0x10000 | 1,911,920 | `904ebe249d75d5a332dacffc1fa4f254e747f96b5ea3447daf0a0b80e9b26c55` |

The original factory program did not complete a Meshtastic handshake. A complete
16,777,216-byte recovery backup passed per-block and whole-chip digests, SHA-256
`0b9b157d62f92f8e36ffb54c2e6785e8a1d2ad3807028d03d9d8395bc76a5bc5`.
The original app0 was 0x140000 bytes. Installation uses the same larger app0
layout as G001, with independently verified image digests and preserved NVS and
OTA-data. Returning to the original program requires this board's full backup
or its original layout/boot state; an app-only rollback is insufficient.

The clean target builds in 518.61 seconds, with 109,000 bytes static RAM and
1,911,489 / 6,553,600 bytes program flash. Native survey client/responder,
SD scheduling/wire/rotation, and actual SNNS/SNGH/Throttle fixtures pass.
Trunk is unavailable on this host; no C++ implementation changed in this target
addition. Existing library/compiler warnings remain.

## Saved profile and peripherals

Full intended owner, hardware identity, local/module protobufs and all channel
slots match after explicit reboot. G002 generated its own distinct PKI keys;
G001's keys were not copied. The private channel, US LongFast, slot 35, configured
10 dBm, FEM setting, Wi-Fi/NTP and encrypted TLS MQTT settings match the saved
G001 profile. CLIENT, rebroadcast NONE, no sleep, disabled GPS, disabled MQTT
downlinks/JSON/client proxy, and disabled active discovery/standard NeighborInfo
are retained. Device, INA219 power, passive SNNS, SNGH, SD and Wi-Fi baselines
follow the saved 300-second profile, subject to admission and scheduling.

INA219 responds at **0x40**, SDA17/SCL18. SD uses SCK47/MOSI48/MISO6/CS4 at
1 MHz. The existing radio-silent peripheral diagnostic reports
`SUMMARY ina=PASS sd=PASS`; 16,384 bytes compare after close/unmount/remount,
and its new test file is removed. The initial serial capture missed the earlier
INA_RESULT line; the captured combined firmware verdict and independent gateway
I2C detection are the evidence. The latest gateway application was restored and
digest-verified, preserving boot/partitions/NVS/OTA/internal filesystem.

Live SNSD reports have flags **15**, **31,896,633,344 filesystem bytes total**,
valid NTP time and zero dropped records in the observed boot. Initial used bytes
are 245,760, then 262,144. This is mounted-filesystem capacity, not a full physical
card-capacity test. One power report is **4.208 V / 0.0 mA**; calibration,
polarity and whole-input current remain unverified. Serial sync records can
interleave with other task logs; missing intact labels alone are not a card fault.

## Production identity

MeshLink remains on **0.3.1 / 62dcc0b**; no application deployment. The guarded
registration was rehearsed on an isolated database copy, then applied under the
deployment lock with backups, queue drain, and service recovery. System Python
first lacked paho; that attempt made no registry/mapping change and recovered
both services. The installed MQTT-worker runtime completed the transaction.

The historical V3 **!849ad7a0** moves to **legacy-v3-849ad7a0** with its own
row and history. The transaction preserves **5,412 source receipts**, **18,626
transport receipts**, all original raw MQTT envelopes, other devices and member
records. The new board receives a separate G002 row and both gateway/source
mappings. Battery capacity, fixed coordinates, solar and other V3 hardware
details are not copied. Authenticated public HTTPS state verifies the new G002
identity, INA219, Wi-Fi, 300-second healthy SD readings and direct receipts;
all six services pass. No second gateway route was observed in this bench.

## Automatic reporting and RF acceptance

Three distinct automatic generations per stream arrived on G002's own encrypted
uplink during the uninterrupted baseline. Receipt gaps in seconds:

| Stream | Consecutive receipt gaps |
| --- | --- |
| Device | 300.2, 300.2 |
| INA219 power | 300.1, 300.1 |
| SD health | 300.1, 300.1 |
| Wi-Fi signal | 300.2, 300.2 |
| SNGH | 345.2, 315.1 |
| Passive SNNS | 345.2, 315.1 |

SD generations 1/2/3 share one boot, advertise 300 seconds, have valid NTP
source times and healthy flags, and report zero dropped records. G002 also
uplinked at least 59 distinct incoming packet IDs. The first intact SD diagnostic
labels were interleaved; live SNSD data establishes healthy mounted storage.

The existing GPS tester **!699c2ed8** is enrolled with G002 using each board's
own public key and the existing private survey cohort. Enrollment survives the
G002 reboot. After another bench owner released the shared station lease, a
54.367-second, unchanged US LongFast/slot-35/10 dBm test completed **five matched
round trips and four initial timeouts**. Median successful RTT is **1,806 ms**
(range 1,667-1,902 ms). All five successful pairs have independent physical
request/reply TX/RX witnesses and matching uplink/downlink signal metrics.
No survey forwarding, hop/ACK violation or owned autonomous RF during observed
quiet is found. One initial USB handshake event gap is recorded; it precedes
the trial. Timeout causes are unisolated; this is functional acceptance, not
a loss-free link or a coverage measurement. Tester persistent profile and
previous RAM settings/targets are restored; handles and lease are released.

The responder deliberately suppresses autonomous RF for **900 seconds from the
latest accepted authenticated PING**, including a cohort PING for another target.
Logging and incoming uplink continue. Ordinary telemetry is expected to resume
after that quiet window; full quiet-expiry/recovery observation remains separate.

Post-registration archive `meshlink-20261115T060501Z.tar.gz`, SHA-256
`2bcf8cf3e0f2f72aa14aa09bb841fe45dae46ac282467888cdaa017a0c60a805`,
passes whole-archive hashing and an isolated SQLite restore with integrity,
current/legacy identities, both private mappings, healthy SD and preserved legacy
receipt counts. The authenticated live API was verified separately. This is not
an off-host or full restored-service recovery claim.

## Evidence and remaining acceptance

Private backups, complete profiles, build/flash/diagnostic logs, encrypted MQTT
observations and RF-test records are under
`private/bench/g002-gateway-20261114/`. Registration, public-state checks and
pre/post recovery archives remain private under `/root/g002-rollout-20261114`
on the production host. Raw location/packet records and enrollment keys stay
outside Git.

Physical copied-card inspection, full survey quiet expiry, peer-gateway receipts, Wi-Fi-outage recovery,
long operation, calibration, field coverage and solar/runtime acceptance remain
separate. G001 and the other gateways are not flashed. The selected tester is
used only for enrollment and the bounded RF check; its persistent profile and
previous RAM settings/target selection are restored.
