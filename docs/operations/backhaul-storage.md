# Backhaul storage snapshot

Read-only SSH inspection on **2026-11-13, 00:34–00:37 Pacific** (08:34–08:37
UTC). Values change as traffic and synthetic demo generation continue. No
services, radios, retention settings or stored observations were changed.

## Where the data goes

Gateway MQTT deliveries enter the portal worker's SQLite queue at
`/var/lib/meshlink-worker/receipts.sqlite`. The worker saves each receipt's
exact payload bytes (base64), topic, receipt time and decoding outcome in
PocketBase's private `mqtt_archive` collection before normalizing supported
reports. PocketBase uses SQLite at `/var/lib/meshlink/pb_data/data.db`.
Positions, observations, neighbor/link reports and per-gateway receipts share
that database. Separate MQTT deliveries remain separate archive entries;
normalization deduplicates displayed reports. This archives what the worker
receives, not traffic lost before delivery. [Ingestion contract](live-mqtt.md).

PocketBase's adjacent `auxiliary.db` holds internal logs. Demo data uses its
own database under `/var/lib/meshlink-demo/pb_data`, with no MQTT archive
entries at inspection. [Portal deployment](portal-lxc.md).

[MeshMonitor](meshmonitor-lxc.md) independently subscribes to MQTT and stores
its decoded observations and packet log in `/data/meshmonitor.db` on its own
LXC. Prometheus stores time-series metrics in `/var/lib/prometheus`; Grafana
stores dashboard/application state in `/var/lib/grafana`, not the primary
radio archive. The MQTT broker is transport, not the project's history store.

G001 also records binary SML segments on its SD card. These are an independent
on-device archive; the current firmware does not upload/replay those files to
the portal automatically. The portal receives an SD usage/health report.
[Card format and retrieval](https://github.com/lfg-seth/firmware/blob/898c113b51975a92fbb3cdc7c441f0224c3bd88f/SNORR_SD_GATEWAY.md),
[gateway installation](g007-screenless-gateway.md).

## Measured sizes

Directory allocation below is `du -s -B1`, divided by binary units and rounded.
SQLite logical file lengths can be larger than disk allocation on these hosts;
do not add the logical and allocated columns together. WAL files fluctuate.

| Store | Logical main database | Allocated directory size |
| --- | ---: | ---: |
| Live PocketBase `pb_data` | `data.db`: 174.3 MiB; `auxiliary.db`: 107.3 MiB | 84.4 MiB including WAL and metadata |
| All `/var/lib/meshlink` | Includes binaries and old private snapshots | 155.3 MiB, including the live `pb_data` above |
| Synthetic demo state | `data.db`: 2.70 GiB | 1.08 GiB including auxiliary DB and WAL |
| Worker receipt queue | 24 KiB | 5 KiB directory; 2 pending rows at sampling |
| Portal backups | 14 compressed archives; 11,100,939,257 bytes total | 10.33 GiB |
| MeshMonitor `/data` | `meshmonitor.db`: 87.8 MiB | 21.5 MiB including WAL |
| MeshMonitor backups | 14 compressed archives | 183.3 MiB |
| Prometheus metrics, all jobs | Time-series files | 980.9 MiB |
| Grafana application state | Database and supporting files | 491.0 MiB |

These non-overlapping top-level stores total approximately **13.21 GiB**
(exclude the live `pb_data` subtotal). This is selected application storage
across hosts, not their combined filesystem use. Prometheus and Grafana
include other monitoring workloads. OS files, application installations,
release/rollback copies and system logs are outside that sum.

The portal LXC filesystem reports **16.48 GiB used / 64 GiB**, **47.52 GiB
available**, 26% used. Its `/var/log` occupies 79.2 MiB. MeshMonitor's LXC
reports 2.29 GiB used / 64 GiB. Broker inspection as the existing non-root
owner shows a 48 GiB filesystem with 7.6 GiB used; broker state/log directories
report 4 KiB each, but privileged completeness was not established.

## Counts and SD report

The live main DB has **68,118 MQTT archive entries**, from
2026-10-15 20:27:25 UTC through 2026-11-13 08:34:57 UTC; 5,243 receipts arrived
since 00:00 UTC that day. It also has 4,695 position rows, 22,440 observations,
66,170 packet receipts, 15,129 neighbor reports and 80,121 link observations.
These are overlapping representations, not independent packet totals, and
were sampled moments apart. `dbstat` attributes about 40.9 MiB of logical
pages to the raw archive table, excluding its indexes.

The synthetic demo has 1,192,728 position rows and zero MQTT archive rows.
MeshMonitor has 79,940 telemetry rows and 65,654 MQTT packet-log rows.

G001's latest stored SD report was measured at **00:31:21 Pacific**:
**3,080,192 / 31,902,400,512 bytes** (2.94 MiB / 29.71 GiB), with zero drops
reported for that boot. Its reported interval is 300 seconds at this snapshot,
unlike the earlier daily deployment baseline. This audit neither changes nor
establishes the reason for that interval. It is a radio-reported measurement,
not a direct card-file inventory.

## Retention and remaining checks

Portal/MeshMonitor packet history has no automatic pruning configured in the
recorded deployment. Both backup jobs keep 14 local archives; the portal timer
is active with the next run at 02:30 Pacific. Prometheus's running command
confirms 30-day metrics retention. Backups are on each application's own host;
off-host recovery remains open. No backup or restore was triggered here.

This is one capacity baseline, not a measured growth rate. Compare a later
snapshot before projecting retention capacity; the demo generator and backup
contents materially affect growth. No direct SD retrieval, sustained
collection-completeness test, physical-host/snapshot accounting or off-host
recovery acceptance was performed.

## Structured data coverage - November 13 follow-up

Read-only deployed-code/schema and aggregate inspection at approximately
00:40–00:43 Pacific. The server's `SOURCE_COMMIT` is
`62dcc0bfe70984332a9ffe5646238d8224320e7c`; it includes Wi-Fi signal ingestion
and variable SD cadence validation beyond the original 0.2.0 source in this
audit branch. Inspect deployed behavior rather than assuming this checkout is
the live release. No payload contents, coordinates, names or credentials were
exported. Schema presence alone is not evidence of populated measurements.

| Information | Portal database | Separate MeshMonitor database |
| --- | --- | --- |
| Member GPS latitude/longitude, measurement/receipt clocks and timestamp quality | Structured `positions`; PDOP and satellite count when supplied | Structured latitude/longitude/altitude telemetry; timestamp semantics differ |
| Device battery voltage | Structured observation history | Structured telemetry |
| Battery percentage, channel utilization, transmit airtime and general device uptime | Retained in raw MQTT envelopes, not ordinary normalized device telemetry; gateway-health and SNNS carry their own uptime | Actual typed telemetry rows exist for all four |
| Infrastructure temperature/humidity and sensor voltage/current | Structured observations, with environment versus power-channel identity; channels 1–8 supported, observed channels 1 and 3 | Actual environment and channel-1 telemetry rows exist; do not assume support for every portal channel |
| SNNS and standard NeighborInfo | `neighbor_reports`, `link_observations`, current-neighbor state; SNNS includes RSSI/SNR, hearing age/count and boot/sequence | Custom PRIVATE_APP reports are logged as unsupported; no equivalent custom SNNS/SNGH/SNSD/SNWI normalization was observed |
| Gateway Wi-Fi/MQTT health, boot/sequence, uptime/interval | Structured observation history and latest state | Custom report packet metadata/preview only |
| Gateway Wi-Fi signal/state/channel/association | Structured observation history and latest state; 50 accepted generations at sample | Custom report packet metadata/preview only |
| Gateway SD mounted/write flags, used/total bytes, drop counter and clocks | Structured observation history and latest state; 4 accepted generations at sample | Custom report packet metadata/preview only |
| Per-gateway receipts, accepted/duplicate/rejected ingestion results | `packet_receipts` with source/gateway/time/outcome and normalized JSON | Separate MQTT packet log with source/destination/gateway/channel, application type, receive metadata and outcome |
| RF packet RSSI/SNR and hop metadata | Exact envelope retains fields, but no general normalized packet-level table | Populated `mqtt_packet_log` fields; a field's presence/default does not establish a valid physical measurement |
| NodeInfo identity/hardware/role announcements | Raw archive; portal identity/configuration remains provisioned separately | Structured node records and NodeInfo packet log |
| Received radio text | Raw archive; operational MQTT text adapter absent and live `messages` has zero rows | 50 stored message rows; 97 received text packets logged at sample |
| Routing/ACK packets | Raw archive, not operational delivery/route history | 116 routing packets logged as unsupported; `traceroutes` has zero rows |

Structured does not mean every metric is a dedicated SQL column. Portal
device/time/identity fields are columns with relevant indexes; coordinates
and metrics live in structured JSON `payload` fields. They are directly
queryable with SQLite JSON functions, without decrypting/reparsing protobuf.
For example, SQL can select `json_extract(payload,'$.power1CurrentMa')` from
`observations`, filtered by `deviceId`, `measuredAt` or `receivedAt`. Some
sensor metrics/history have portal APIs; arbitrary cross-stream analytics
still require private SQL/tooling. There is no single unified history/query
schema across PocketBase, MeshMonitor, Prometheus and SD files.

The raw archive's receipt ID, topic, received/ingested times are SQL fields.
QoS, retained/duplicate flags, byte length, decode outcome/reason and base64
payload are JSON metadata. At sampling it held 65,017 normalized, 1,663 rejected
and 1,618 unsupported deliveries. Thus rejected/unsupported does not mean
discarded: the original MQTT bytes remain, including unregistered-source
traffic received within the worker's subscribed/authorized topics. Those
payloads require envelope/protobuf parsing and sometimes decryption before
their unnormalized contents become analytical fields. The terminal dashboard
does this on read for additional metrics; it does not persist a new metric table.

The archive's `normalized` outcome means the adapter produced a supported
normalized packet; backend acceptance/duplicate/rejection is a separate
`packet_receipts` result. Radio duplicates across MQTT deliveries are kept in
the archive and receipt history while supported observations deduplicate.

### Files, logs and collection gaps

- G001 SD segments hold raw RF receive bytes/status/airtime and RSSI/SNR,
  decode/duplicate references, retained application protobuf bytes, local
  publish results, encrypted RF TX-start frames, TX-complete interrupts,
  Wi-Fi/MQTT link events, boot/reset and clock anchors, gap/eviction records.
  These are binary files with a local reader/exporter, not centrally imported
  queryable event rows. Decoded admin contents are intentionally excluded.
- Server service/system logs, PocketBase internal logs and selected bench
  captures exist separately. Nginx portal access logging is explicitly off.
  A continuous central radio serial/debug-console archive or cross-host log
  search has not been deployed. MeshMonitor has its own populated audit log;
  this audit does not assert all services omit IPs or authentication metadata.
- No receiver records RF it never detects/reads, collisions/noise as a full
  waveform, or transmissions suppressed before a packet is created. No
  complete every-hop path, proven human delivery/read receipt, or exact
  network-wide loss history can be reconstructed from these stores alone.
- MQTT disconnect/buffering limits can leave server gaps. SD may retain local
  RF evidence but there is no automatic SD upload/replay to fill those gaps.
  SD queue overflow, unsynced power-loss tails and capacity eviction remain
  recorded/possible loss boundaries, not guarantees of complete capture.
- Supported solar/intrusion ingestion fields do not establish live sensors:
  neither key appears in current live observation history. Whole-system energy,
  calibrated battery capacity and runtime are not directly measured merely
  because voltage/current history exists. Member environment/power and
  infrastructure GPS are not normalized by the portal MQTT adapter.

No retention policy or implementation change was made. These coverage gaps
are findings; addressing them requires an owner-selected scope.
