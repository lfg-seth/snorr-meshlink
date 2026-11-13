# RAK batch identification and preparation

Owner selects batches of **4-8 connected RAKs**, fresh labels and **CLIENT on
the bench**. All deployment RAKs have **INA219**, confirmed by the owner.
Auto-detect AHT21 using actual returned **temperature and relative humidity**;
no per-board sensor list is required. Record both sensor results by !ID.
The selected repeaters switch to ROUTER during Sunday's final installation,
followed by complete role/cadence/profile readback. A role change can install
firmware defaults; confirm the 180-second reporting settings again afterward.

## Label station

From the repository root, use the existing Python environment:

```powershell
.\.venv\Scripts\python.exe scripts/bench/watch-raks.py --reference-usb 70DF102F58D2A034
```

Plug boards in one at a time to attach their initial **!nodeid** labels. Several
boards may remain connected; the watcher reads new RAKs sequentially and closes
each port immediately after identification. All RAKs are shown by default;
Heltec USB devices are skipped. **REF1** (!8737c2c9, USB ending A034) is shown
with a **REFERENCE** annotation and excluded from deployment numbering. Example:

```text
!f95b5501  |  R001  |  CLIENT  |  COM19  |  USB E93C5FF0F97DD76B  |  2.7.26.4c96b9b
```

The !ID comes first; names are current readback, not an old assignment. A unit
without a responding Meshtastic API shows WAIT and its USB identity rather
than an invented !ID. This watcher never flashes, renames, resets or writes
configuration. Ctrl+C stops it; `--once` scans connected RAKs once and exits.
SDK output stays in ignored `private/bench/rak-label-station/`; the console
prints identity/name/role/firmware only. `nodes.json` is a discovery cache,
with a `connected` flag on each cached board. Unplugged boards print
**DISCONNECTED** and remain in the cache with `connected: false`; cached rows
are not a count of attached boards, readiness, or permission to copy identities.

Windows enumeration alone does not establish usable serial access: batch
checks have encountered listed COM ports that would not open. On WAIT or an
incomplete identity/profile, leave the board unmodified, check for a competing
port owner, refresh the present-device list and reseat that identified board.
Retry once, then keep a failing unit pending and continue the batch. Preserve
the error and USB identity; a failed open does not establish a Windows, hub,
cable or board fault.

## Port handoff for batch preparation

Before flashing/configuration/radio tests:

```powershell
.\.venv\Scripts\python.exe scripts/bench/watch-raks.py --pause
.\.venv\Scripts\python.exe scripts/bench/watch-raks.py --status
```

Wait for **PAUSED**, then require validated `--status` output with
`running: true`, `stale: false`, `paused: true` and `busyPort: null` before the
worker opens selected boards. Status verifies the process creation identity
and a heartbeat no older than 30 seconds; heartbeat refreshes before and after
each port read. A raw `status.json` file or stale pause acknowledgement is not
a safe handoff. If the watcher has stopped, the worker must acquire the
station's OS lease before opening boards. After closing all worker handles:

```powershell
.\.venv\Scripts\python.exe scripts/bench/watch-raks.py --resume
```

Resume rereads connected boards and shows **!ID + final R00N name + CLIENT +
firmware**, ready for updating physical labels. An OS-owned station lock
prevents two watchers; closing/crashing releases it.

Use `--stop` to request exit after the current read closes, then check
`--status`. Stop requests target the verified running instance; an orphan
request cannot stop the next launch. Ctrl+C also stops the watcher.
Workers that acquire the station OS lease themselves must stop the watcher
and wait for exit before acquiring it; a paused watcher retains that lease.

## Efficient preparation order

1. Inventory USB/!IDs with the [fresh roster](../../records/deployment-nodes.md),
   ignoring old R/G labels. INA219 is expected on every deployment board;
   detect AHT21 from measured temperature and humidity during preparation.
2. Pause and validate the handoff. Back up each unit's own complete profile and
   identify its image. Retain matching 4c96b9b; flash only units that need the
   selected verified ordinary image. Reference wipe authority does not waive
   deployment-node backups or allow copying another unit's keys.
3. Apply fresh names, CLIENT, sensor reporting and agreed cadence.
   Clear stale sites; leave case/battery/solar/location selection until Sunday.
   Stage several units before waiting for reboots/sensors, then independently
   verify each complete saved profile. CLIENT's sleep-interval field can
   normalize to 300 seconds with power saving off.
4. Collect INA219 and temperature/humidity startup data across the batch. If
   AHT21 does not return both measurements, mark it **not detected/unverified**;
   silence alone does not prove absence or failure. Serialize paced RF checks
   against REF1. R001's six-packet check measured **44.4 seconds**; whole-batch
   throughput has not yet been measured. Preserve failures.
5. Report each verified **!ID -> R00N / CLIENT / firmware / sensor fit**, resume
   the station and update labels. Sunday's ROUTER/site step and forced-relay/
   end-to-end acceptance remain explicit.

Implementation: [watch-raks.py](../../scripts/bench/watch-raks.py). This CLI
implements discovery/label refresh and port handoff. The preparation steps
remain the worker's procedure, not an automatic flashing mode in this CLI.
