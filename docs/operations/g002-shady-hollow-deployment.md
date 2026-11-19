# G002 Shady Hollow offline SD recorder - 2026-11-15

**Publication update, 2026-11-15:** owner approves publishing the exact fixed
location in the [deployment table](../../records/sites.md#2026-11-15---published-deployment-setup-and-fixed-locations). Earlier privacy wording below describes the original evidence handling;
complete profiles and raw logs remain ignored.

Owner selects **G002 / Case 7 / eight cells / Muzi** for **Shady Hollow**, with
exact supplied coordinates. Purpose is local SD recording without Wi-Fi;
CLIENT or ROUTER is authorized. Keep existing **CLIENT / rebroadcast NONE**,
which supports recording without introducing a new routing role. Identity
and label remain G002; no portal reassignment is requested. Exact coordinates,
raw packet logs and full profiles stay private.

## Configuration

Fresh USB backup independently identifies **F8:5B:1B:BF:0A:B8**, radio
**!1bbf0ab8**, hardware **bfd67fc07c1161ce8fae291933705196**, HELTEC_V4 and
installed **2.7.26.f6cdbeb / heltec-v4-sd-gateway-survey**. The installed
recorder supports offline logging; no firmware flash, factory reset or rebuild.
[Original commissioning](g002-screenless-gateway.md) remains historical.

Disable **Wi-Fi and MQTT**; retain saved credentials privately for future use.
Save the owner-supplied fixed coordinates as integer degrees × 10^7, retaining
existing altitude or leaving it unspecified. Preserve own keys/admin list,
channels/names, CLIENT/NONE, radio/power/Bluetooth, enabled device/INA219 power
**300 seconds**, saved-baseline SNNS, standard NeighborInfo **21,600 seconds**,
GPS NOT_PRESENT and own **3,600-second smart-position** settings. Leave the
recorder's card, files, rotation policy and private survey pairing intact.

Station lease/full fresh-profile guard precede writes. Complete intended
local/module/channel bytes, owner/identity, hardware/firmware metadata and exact
fixed coordinates pass before and after the one explicit reboot. Temporary
structured USB logging is restored to its original setting; the final
independent full-profile read verifies that restoration. Serial closes.
Private commands and evidence:
`private/bench/G002-shady-hollow-20261115/`.

## SD writes verified with networking disabled

Two successful local sync diagnostics show segment **23**, frames **123 → 151**, **zero drops**, **4,208 / 31,149,056 KiB** used/total.
The first 135-second observation obtains one healthy sync but no proven frame
growth. A second observation retains every sync and requests one telemetry
read addressed only to G002 itself over USB; newly generated local records
are included in the successful growth check. This is not an RF ping or field
reception/coverage trial. The full offline profile and connection-status replies confirm Wi-Fi
and MQTT disabled throughout this observation. SD writes continue without an
internet uplink. No card erase, destructive diagnostic or file rotation-policy
change. Physical copied-file integrity/endurance remain separate checks.
Observation timestamps and raw diagnostic references remain private.

## Offline recording and monitoring

Pinned `f6cdbeb` `SnorrRecorder.cpp` starts the writer independently of Wi-Fi
and MQTT. Incoming raw RF, decoded/local packets and recorder events feed its
queue; successful diagnostics follow `f_sync` and capacity refresh. Recording
uses boot/sequence/monotonic values and records clock quality, including unknown
UTC. USB-set time does not prove clock acquisition on a field cold start.

The same firmware gates SNSD/SNGH on Wi-Fi/MQTT enablement. With both disabled,
absence of those remote health reports is expected and is not a card-failure
verdict. CLI baseline disables gateway/Wi-Fi/SD-report deadlines for this
selected offline use, retaining ordinary radio/position baselines. No production
portal/server/gateway service changes or downlinks are made.

## Assembly and remaining checks

Case 7 intake is **v4 PETG, one SMA, two 200 mA panels, one four-cell parallel
holder/four-cell capacity**. Owner now explicitly allocates **eight cells**;
that newer count supersedes the earlier count, without inferring a second
holder, wiring or physical fit. No purchase, stock recount, capacity/runtime,
antenna-gain or solar-output claim.

Physical copied-card file inspection, sustained recording/power-loss recovery,
calibration, completed installation, field reception/coverage and battery/solar
runtime remain separate checks. No ping or relay acceptance is implied.

## Copied-card analysis - 2026-11-16

Owner supplies `/home/setheth/Desktop/SN1BBF0AB8/` for read-only analysis.
All headers identify **G002 !1bbf0ab8**. The **25 consecutive segments
00000001–00000019 (hex)** contain **6,612,854 bytes / 69,772 event frames /
20 boot IDs**. They include commissioning history, an earlier **7 h 18 min**
networked boot and the latest offline boot; do not combine them as one field run.
Boot payloads identify **2.7.26.f6cdbeb** throughout.

### Integrity and scope

The existing [SML1 reader](../../scripts/sd-reader/reader.js) and an independent
Python `struct`/`zlib.crc32` walk agree on every header, frame CRC, frame length,
boot ownership and closed-segment frame count. **Zero corrupt bytes or missing
segment numbers; all event sequence numbers present exactly once within each
boot.** One older boot has an append-order inversion, without a missing event;
the latest boot's sequence and monotonic time increase throughout.

**24 segments have valid close markers.** The last, `00000019.SML`, ends exactly
after a valid event, with no `END1` marker or partial frame. This is an open
recording tail, not detected corruption. It does not prove deliberate clean
shutdown or exclude queued/unflushed events lost after the last saved frame.
There are **no Record loss or Eviction events** in the supplied copy. This is
bounded evidence of preserved recording, not an end-to-end packet-loss verdict
or a destructive power-loss/recovery test.

Private evidence: `private/analysis/G002-offline-20261116/` contains a per-file
SHA-256/size/header manifest, decoded event JSONL, independent audit and analysis
scripts, protobuf decoding and derived summaries. Original files remain unchanged.
Raw packets, GPS coordinates, message payloads and individual tracks are not
published. No board, serial port, server, portal or radio configuration changed.

### Latest offline boot and clock limitation

Segments **00000017–00000019** share boot **9b841cdf**. They contain **29,334
consecutive events**, starting at uptime **7.728 s** and ending at
**104,109.000 s (28 h 55 min 9 s)**. No intervening boot is recorded.
Configuration in the boot event is CLIENT/NONE, LongFast, 10 dBm, hop limit 3
and 300-second telemetry. The single connectivity event reports disconnected;
there are **zero MQTT intent/envelope/queue/publish events** in this boot.
Together with the saved configuration, this supports recording without backhaul.
It is not a Wi-Fi configuration readback from the card.

**Every event has UTC absent and clock quality 0**, including the sole clock
anchor. Thus the offline run never records valid UTC. Earlier networked boots
acquire quality 3/NTP; their clock must not be carried across a reboot. FAT
file dates include 1980 and future dates and are not an observation timeline.
Own telemetry's nonzero `time` fields are small epoch-relative values, not valid
2026 UTC; treating nonzero as valid would misdate this run.

As a separately labelled estimate, **5,509 decoded telemetry/position packets**
with plausible source UTC yield a median `source time − recorder uptime` of
**2026-11-16 00:57:03 UTC**, suggesting approximately **November 15 16:57 to
November 16 21:52 Pacific**. Per-source medians agree within about six seconds;
individual offsets span roughly 96 seconds. This alignment assumes reasonably
correct sender clocks and bounded transmission delay. It is **reconstructed
from sender times**, not G002's measured receive UTC or a certified error bound.
Do not use it to claim exact fix age at reception or a passed cold-start clock gate.

### Radio reception and sustained sources

The latest boot contains **13,158 Raw RX events**, **7,010 decoded observations**
and **4,993 duplicate decisions**. Of the raw reads, **12,006 return success**
and **1,152 (8.76%) return −7**, RadioLib's
[received-packet CRC mismatch](https://jgromes.github.io/RadioLib/group__status__codes.html).
This is corruption on the radio path, separate from the valid on-card frame CRCs.
The percentage describes observed radio read events, not the fraction of all
attempted transmissions lost. Headers from failed reads are untrusted and produce
many spurious near-matching node IDs; they are excluded from source/link analysis.

Successful reads with a complete radio header represent **nine source IDs**,
including G002's own packets heard after relaying. Eight other origins decode:
R001, R008, R005, R011, B002, B003, G003 and legacy **!b03d6790**. The longest
gap between all Raw RX observations is **91.42 seconds**; this includes failed
reads and does not guarantee useful data from every source at that cadence.

| Source / current assignment | Decoded observations, whole boot | Direct-indicated successful RX after first hour | Median direct RSSI / SNR after first hour | Largest received device-telemetry gap |
| --- | ---: | ---: | --- | ---: |
| R001 !f95b5501 / Cathedral Rock | 2,272 | 2,192 | −86 dBm / +4.0 dB | 6.0 min |
| R008 !120b04fd / Kyle Junction | 2,125 | 1,920 | −97 dBm / −4.5 dB | 12.0 min |
| R005 !a65601b3 / Angel Vegas | 1,656 | 1,595 | −103 dBm / −10.0 dB | 18.0 min |
| R011 !8737c2c9 / Angel Mountain | 881 | 844 | −105 dBm / −12.5 dB | 72.1 min |

“Direct-indicated” uses valid read status, source ID and the radio header's
unchanged **hop start/limit 3/3**. RSSI/SNR are measured at G002 for those
receptions. Relayed copies are excluded from these medians. This establishes
one-way reception evidence; it is not bidirectional survey/pong acceptance,
proof of installation at the selected sites or a complete path measurement.
The first hour is excluded from link medians to reduce commissioning/handling
influence, without assuming a known stationary start. All four sources remain
present in the last six hours.

R011 is the weakest of these received direct signals and has substantially
sparser device telemetry. Its largest environment and INA219 power gaps are
**108.1 and 81.0 minutes**, respectively. Sender scheduling, RF loss and path
changes are not isolated by this copy. R002/R003/R004/R006/R007/R009/R010/G001
have no successfully decoded observations in this latest boot; their absence
cannot establish whether they were powered, installed, transmitting or reachable.

The final received device estimates are **R001 45% / 3.682 V**, **R008 58% /
3.791 V**, **R005 68% / 3.872 V**, and **R011 96% / 4.141 V**. These are
reported estimates at different receipt times, not measured pack capacities.

### Member GPS evidence

**B002 !699ca878** supplies **ten decoded positions**, all with internal-GPS
measurement timestamps and distinct coordinates, between uptime **96.215 and
1,784.572 seconds**. Source packet time minus GPS measurement time is **10–56 s**;
that is a sender-side age, not receiver-observed age. The largest received
position gap within this window is **726.175 s / 12.1 min**. No further B002
position appears during the remaining **28 h 25 min** of the copy. This records
a short successful GPS-reception window, not sustained member tracking or proof
that a member continued moving/transmitting afterward.

**B003 !699c2ed8** supplies eleven device reports and no position in this boot.
Its current [survey-tester use](../../records/bench-overnight-20261115.md)
suppresses ordinary position broadcasts, so this is not a new GPS-fault finding.
Other decoded positions are fixed R001/R008/R005 infrastructure pins without
GPS measurement timestamps; do not count them as member GPS fixes.

### G002 power, cadence and earlier reset

G002 generates **347 INA219 power samples**, with median spacing **300.353 s**
and maximum **300.959 s**. It also records **348 populated own device samples**
plus one empty device-metrics request; excluding that request avoids interpreting
it as a zero battery reading. These are local generation records, not proof
that another node received every telemetry packet.

The last populated device sample is **85% / 4.022 V**; the first is **4.285 V /
101**, where >100 is the protocol's externally-powered sentinel, not 101% charge.
INA219 CH1 is a separate measurement: **4.200 → 3.944 V**, median current
**114.6 mA**, sampled range **−243.1 to +497.8 mA**. Negative readings and voltage
recoveries occur, but wiring/polarity, sensor calibration and external charging
are not established by these logs. Do not extrapolate eight-cell capacity,
remaining runtime or a solar energy balance from sparse current samples.

Own populated device telemetry reports median channel utilization **6.59%**,
maximum **21.045%**, and median transmit-airtime utilization **0.730%**. There
are **1,034 TX-start events / 1,032 TX-complete events**; two starts have no
matching completion, at uptime **2 h 1 min** and **19 h 37 min**. Later TX and
recording continue. Their cause is not recorded; this is not proof that either
packet reached another node or of a boot reset.

The earlier `00000016.SML` boot reports reset reason **4**, corresponding to
[ESP_RST_PANIC](https://raw.githubusercontent.com/espressif/esp-idf/v5.4.1/components/esp_system/include/esp_system.h).
No exception backtrace or trigger is present, so no root cause is assigned.
That short boot precedes the latest offline boot, whose reason is **3 / software
reset**. Do not describe the 29-hour run as a repeated-crash run or treat the
older panic as resolved merely because the later run is stable.

### Remaining acceptance

Copied-card structural integrity and sustained recording now have positive
evidence. Prioritize **cold-start UTC acquisition without USB/phone/NTP**, then
an owner-selected matched placement/link comparison for R011 and a sustained
member GPS test with agreed powered/transmitting intervals. Controlled power-loss
recovery, recorder/INA219 calibration, exact power/charging topology, installation,
coverage, bidirectional/forced-relay tests and battery/solar endurance remain open.
No firmware fix, flash, new RF test or deployment is performed by this analysis.
