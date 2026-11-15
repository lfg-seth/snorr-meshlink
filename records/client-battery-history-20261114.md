# B002/B003 battery and GPS history - November 14, 2026

Read-only production snapshot at **18:03:15 Pacific, November 14**
(`2026-11-15T02:03:15.929Z`). All times below are Pacific. No radio,
configuration, service or portal assignment was changed by this analysis.

## Battery results

| Member node | Observed discharge interval | Duration | Battery reports at endpoints | Result |
| --- | --- | --- | --- | --- |
| B002, `!699ca878` | Nov. 13 16:12:12 to Nov. 14 16:48:48 | **24 h 36 min 36 s** | 4.194 V / 100% initially; 3.089 V / 0% at 16:47:27, followed by the last GPS packet at 16:48:48 | First substantial silence follows a near-empty report. Depletion is a strong inference; exact electrical cutoff and cause were not measured. |
| B003, `!699c2ed8` | Nov. 13 17:09:28 to Nov. 14 12:53:11 | **19 h 43 min 43 s** | 4.197 V / 100% to 3.586 V / 35% | Trial ended through owner-confirmed reassignment around 12:55. Voltage rises to 3.638 V / 40% at 12:56:07 and continues upward. Full-discharge runtime is unmeasured. |

Start times are the first ordinary battery-level samples after firmware status
101, supported by a sustained voltage decline. They are conservative observed
discharge spans, not independently logged USB-disconnection times. The preceding
101 samples are at 16:08:17 for B002 and 17:01:37 for B003 on November 13.
Status 101 means charging/external-power or no detected battery; it does not
prove the exact supply state. Percentages and voltages are firmware estimates,
not calibrated capacity or current measurements. Do not extrapolate B003's 35%
reserve linearly into remaining hours.

Both observed spans exceed the four-hour minimum and twelve-hour runtime target
in the [project brief](../PROJECT.md). These bench observations do not close the
phone-free startup, representative outdoor conditions, actual pack-capacity,
forced-relay or field acceptance gates.

## GPS during those discharge intervals

Counts are unique received position packets with coordinates and a GPS
measurement timestamp. Coordinates themselves were not exported.

| Member node | Positions | Median receipt interval | Longest receipt gap | Gaps over 5 minutes | GPS measurement age at receipt: median / maximum |
| --- | --- | --- | --- | --- | --- |
| B002 | 591 | 149.6 s | **5 min 21.2 s** | 5 | 36.0 / 104.6 s |
| B003 | 464 | 152.0 s | **5 min 9.9 s** | 1 | 36.6 / 129.2 s |

Neither discharge interval contains a 15-minute position gap, an unknown GPS
measurement time or a received fix older than 15 minutes. Typical arrivals are
about 2.5 minutes apart against the saved two-minute position setting. B002's
largest gap is November 13 20:37:36 to 20:42:57. B003's is November 14
03:50:03 to 03:55:13. These are observed receipt gaps; independent RF attempts
were not counted, so this is not a packet-loss-rate measurement.

## Stops, returns and later GPS gaps

### B002

- Last GPS before the initial stop: **November 14 16:48:48**. There is no
  intervening selected-source radio packet until NodeInfo at **17:29:13**:
  **40 min 25.5 s** of observed radio silence.
- GPS resumes at **17:29:42**, giving a **40 min 54.9 s GPS gap**. A new
  SNNS boot ID and uptime of 67 seconds at 17:30:04 confirm a restart.
  Battery still reports 3.076 V / 0%.
- Last GPS in that brief return is **17:31:44**. Radio returns again at
  **17:59:55**, and GPS at **18:00:25**, a second **28 min 41.4 s GPS gap**.
  Device telemetry at 18:00:49 again reports uptime 67 seconds, with voltage
  now 3.352 V / 14%. The matching uptime number does not imply the same boot:
  these reports are more than 30 minutes apart.
- Last position and selected-source packet in the snapshot: **18:02:35**.
  Consequently, the evidence shows intermittent returns after the first stop,
  rather than a permanently silent device as of this snapshot. Low voltage
  strongly supports a power-related initial interruption, but later handling,
  charge recovery and restart triggers are unverified.

### B003

The owner confirms this unit was tasked elsewhere around the 12:55 voltage
reversal. Later restarts and silences are part of the changed-use period and
must not be labelled battery exhaustion or an unexplained endurance failure.

- GPS gap **13:57:49 to 14:15:21**, **17 min 31.7 s**.
- Last GPS in the snapshot: **14:21:48**; no later position is retained through
  18:03:15, a trailing absence of **3 h 41 min 27 s**.
- Radio silence **14:23:10 to 17:50:45**, **3 h 27 min 34.2 s**. Subsequent
  battery reports arrive at 17:50:45, 17:58:15 and **18:01:16**. Latest battery
  report is 3.882 V / 69%.
- Uptime falls confirm multiple restarts after reassignment. They do not
  establish a hardware fault or flat battery.

The production archive continues receiving other nodes in every minute bucket
across the completed long silences above. A general archive/ingestion stoppage
does not explain these client gaps. This does not isolate local power, handling,
RF reception or receiver scheduling as the cause.

## Full retained history and identity

The complete retained MQTT archive contains **117,583 receipts**, from
October 15 13:27:25 through November 14 18:02:45. Decoding and deduplication
select **6,231 B002** and **5,403 B003-physical-radio** packets, including
battery/device telemetry, GPS and custom reports.

Normalized positions predate the raw archive and extend the GPS history to
**October 14 19:37:27 for B002** and **19:39:20 for B003's physical radio**.
Combining those older positions with the raw-archive positions produces
**4,153 B002 positions** and **2,531 positions for B003's physical radio**.
Every normalized position after the archive start is represented in the raw
position export; no post-start normalized positions are missing from it.

B003's hardware previously served as B001 and G004. Those earlier logical
identities remain distinguished in the private normalized export; their history
is not treated as a continuous B003 member trial. Older multi-day gaps, including
the late-October to November 12 inactivity, likewise cannot establish continuous
battery runtime or an operational outage. The complete position-gap catalog
contains 19 B002 and 24 B003-physical-radio completed gaps longer than 15 minutes
across the entire retained history; it preserves dates rather than attributing
all historical inactivity to battery failure.

## Method, private evidence and validation

The existing server MQTT Python runtime opens SQLite with `mode=ro`,
`PRAGMA query_only=ON` and a read transaction. Channel keys and decryption remain
on the server. Historical uplink IDs are accepted only when envelope/topic
identity and the pilot channel match. Gateway copies are deduplicated by
physical sender, packet ID and encrypted payload digest. Position measurement
time remains separate from packet source/transmit and receipt times.

Sanitized exports are ignored at `private/client-history-20261114/`:

- `full-history.json`: all selected decoded packet observations, gateway receipt
  copies, archive activity counts and older normalized records. No coordinates,
  member identities, credentials, keys or raw encrypted payloads are exported.
- `analysis.json`: discharge windows, GPS age/gap measurements and full-history
  summary; `gps-gaps-over5m.csv`: complete retained position-gap catalog.
- `analyze-full.py` and `inspect-history.py`: local calculation and inspection.
  Collector: `private/overnight-analysis-20261113/pull-client-full.py`.

The current custom-report validator rejects 322 historical custom messages,
principally from the radio's earlier role. Their radio receipt times are retained
as undecoded custom events rather than dropped. They do not supply battery/GPS
values. This analysis covers retained pilot telemetry and GPS, not the contents
of encrypted administrative messages.

Validation recomputes counts, duration arithmetic, unique position receipts,
measurement ages, both completed B002 GPS gaps and pre-archive position
coverage. A recursive privacy check rejects coordinate, credential and raw
payload fields in the local export. These checks and the four changed-document
link/whitespace checks pass. The full-history export SHA-256 is
`b3cbbdc9d5ee92529e611124f260504134c7f704ff11a32895bc5a0298ce6382`;
`validation.json` retains the other evidence hashes. No synthetic samples are
added. The final snapshot is fixed; it does not predict subsequent reporting.

Next: confirm any B002 power intervention after 16:48, and repeat a controlled,
logged battery-only trial with known packs and cutoff/phone-free startup
observations if formal runtime acceptance is required. B003's full-discharge
result remains open because the owner ended this run for another task.
