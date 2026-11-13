# Measuring G001 Wi-Fi

The screenless Heltec V4.3 measures the signal **received by its Wi-Fi radio
from the associated 2.4 GHz AP**, in dBm. A less negative number is stronger.
It is separate from LoRa RSSI and does not measure upload quality, loss, latency,
throughput, antenna gain or distance. Board placement, the laptop, a person,
walls, reflections, AP power, channel and roaming can all change the reading.
The implementation uses Espressif’s [associated AP information](https://docs.espressif.com/projects/esp-faq/en/latest/software-framework/wifi.html).
No scan, traffic generator, SSID, BSSID or coordinates are needed. Heltec lists
separate Wi-Fi and LoRa antennas on this board; its default Wi-Fi path uses an
FPC and the optional external 2.4 GHz connector requires selecting its RF path.
Check the [Heltec antenna FAQ](https://github.com/HelTecAutomation/HeltecWiKi/blob/main/docs/devices/open-source-hardware/esp32-series/lora-32/wifi-lora-32-v4/frequently-asked-questions.md) for your revision before comparing antenna types.

**USB walk test:** plug in G001, close other serial clients, open its USB port
at **115200 8N1** with a newline line ending, and enter `WIFI ON`. Lines beginning
with `SNWF` show uptime, dBm, channel and an association number, or explicitly
say disconnected/unavailable. Enter `WIFI OFF` to stop. The mode expires after
30 minutes, stops on a Meshtastic API connection or reboot, and does not
change any saved profile. A USB adapter that resets the board can start a new
boot when opening a terminal. Survey data is also recorded locally on the SD
card as SML1 event 20 while logging is healthy. Starting the survey does not
speed up or initiate radio broadcasts.

For a CSV and per-association min/median/max, run the following from the repo
with its Python environment (replace COM31 if Windows assigns a new port):

```powershell
.venv/Scripts/python.exe scripts/bench/wifi-survey.py --port COM31 --samples 60 --label stock-vertical-20m
```

The helper stores each sample immediately under ignored `local-data/wifi-surveys/`.
Use measured distances and mark obstacles yourself. At each mark, hold board
and laptop height/position steady. Alternate A/B/A, collect 30–60 seconds for
each antenna or orientation, and compare medians, variation and disconnects.
Use the same AP, channel and transmit settings. Split the run on a new
association or reboot; association numbers are observations within a boot,
not persistent AP identities. Repeated directionally consistent differences
are more useful than one peak reading. A usable range needs a separate
two-way traffic/delivery test under the intended installation conditions.

**Bench baseline (2026-11-12):** G001 `!1bbf0638` ran firmware `246ec7285`
(app SHA-256 `29911d7350fafb560fdbd52d891b8a88aac58598a3dc21f3bfe1f2871f015f0c`).
The app-only write matched its on-chip digest and preserved the bootloader,
partition table, NVS, OTA data and complete saved gateway profile. Over about
60 seconds the USB collector accepted 45 samples: two startup disconnects,
then 43 readings on channel 5/association 1, ranging from −44 to −33 dBm
with a median of −38 dBm. Missing serial lines are not Wi-Fi disconnects.
Raw evidence: `private/bench/g001-wifi/bench-fixed.csv`. This was one bench
position; no antenna gain, AP distance or installation range was established.

**Production acceptance:** MeshLink 0.3.0 at `1901aa7552865a525936c80cc5583116e2ce92db`
passed all 93 backend and 65 portal checks on the release host. Both live and
demo backup restores passed before and after deployment; all ten public
assets matched the tagged build. At 20:04:07 Pacific, Nov 12 (04:04:07 UTC,
Nov 13), the gateway's first autonomous SNWF report read **−40 dBm, channel
5, association 1, interval 300 s**. It was stored once with two encrypted
raw receipts, via G001 and via the legacy V3's independent radio uplink.
The live authenticated Infrastructure card showed the reading alongside
**<0.1% used (384 KiB of 29.7 GiB)**, zero dropped on its last SD report.
Evidence: `private/bench/g001-wifi/live-browser-result.json`,
`G001-live-WiFi-card.png`, `wifi-evidence.json` in the same private folder.
Production rollback: `/opt/meshlink-rollback-wifi-1901aa7`; firmware recovery:
verified prior app `private/bench/g001-wifi/rollback-app.bin`. Offline reader
fixtures cover event 20 and SNWF; a physical SD file copy remains a separate
inspection. No field-distance or comparative antenna run was performed.

**Normal operation:** SNWF v1 follows actual periodic device telemetry mesh
sends (G001 configured at 300 s, subject to airtime limits and scheduling).
The 36-byte private payload is little-endian `<4sBBbB7I`: magic, version,
state (0 disconnected, 1 unavailable, 2 measured), signed RSSI, primary channel,
observer, boot, sequence, uptime seconds, source UTC or zero, effective interval
seconds and boot-local association ordinal. The last three measurement fields
(RSSI, channel, association) are zero on wire when no reading is available and
null in normalized data. The gateway never broadcasts the one-second survey.
MeshLink archives each delivered MQTT envelope on its subscribed pilot root,
even for unsupported packets; observations deduplicate a report by source,
boot and sequence and retain each route's receipt. The newest eligible sample
appears on the gateway card; after three expected intervals it is last known.
Loss before reception, SD/queue drops, unavailable storage and offline periods
cannot be recovered from a displayed signal value. SD health remains daily.
