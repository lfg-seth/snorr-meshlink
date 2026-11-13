# RAK batch identification and preparation

Owner selects batches of **4-8 connected RAKs**, fresh labels and **CLIENT on
the bench**. Sensor fit is mixed: record INA219/AHT21 separately for each !ID.
The selected repeaters switch to ROUTER during Sunday's final installation,
followed by complete role/cadence/profile readback. A role change can install
firmware defaults; confirm the 180-second reporting settings again afterward.

## Label station

From the repository root, use the existing Python environment:

```powershell
.\.venv\Scripts\python.exe scripts/bench/watch-raks.py --exclude-usb 70DF102F58D2A034
```

Plug boards in one at a time to attach their initial **!nodeid** labels. Several
boards may remain connected; the watcher reads new RAKs sequentially and closes
each port immediately after identification. It skips Heltec USB devices and
the selected **REF1** reference. Example:

```text
!f95b5501  |  R001  |  CLIENT  |  COM19  |  USB E93C5FF0F97DD76B  |  2.7.26.4c96b9b
```

The !ID comes first; names are current readback, not an old assignment. A unit
without a responding Meshtastic API shows WAIT and its USB identity rather
than an invented !ID. This watcher never flashes, renames, resets or writes
configuration. Ctrl+C stops it; `--once` scans connected RAKs once and exits.
SDK output stays in ignored `private/bench/rak-label-station/`; the console
prints identity/name/role/firmware only. `nodes.json` is a discovery cache,
not a task-status queue or permission to copy another board's identity.

## Port handoff for batch preparation

Before flashing/configuration/radio tests:

```powershell
.\.venv\Scripts\python.exe scripts/bench/watch-raks.py --pause
```

Wait for **PAUSED** in the console, or `status.json` with `paused: true` and
`busyPort: null`. Then the worker may open selected boards. After closing all
worker serial handles:

```powershell
.\.venv\Scripts\python.exe scripts/bench/watch-raks.py --resume
```

Resume rereads connected boards and shows **!ID + final R00N name + CLIENT +
firmware**, ready for updating physical labels. An OS-owned station lock
prevents two watchers; closing/crashing releases it.

## Efficient preparation order

1. Inventory all USB/!IDs and receive the owner's per-board sensor list. Use
   the [fresh roster](../../records/deployment-nodes.md), not old R/G labels.
2. Pause the watcher. Back up each deployment unit's own complete profile and
   identify its image. Retain matching 4c96b9b; flash only units that need the
   selected verified ordinary image. Reference wipe authority does not waive
   deployment-node backups or allow copying another unit's keys.
3. Apply fresh names, CLIENT, fitted-sensor reporting and agreed cadence.
   Clear stale sites; leave case/battery/solar/location selection until Sunday.
   Stage several units before waiting for reboots/sensors, then independently
   verify each complete saved profile. CLIENT's sleep-interval field can
   normalize to 300 seconds with power saving off.
4. Collect sensor startup data across the batch; serialize paced RF checks
   against REF1. R001's six-packet check measured **44.4 seconds**; whole-batch
   throughput has not yet been measured. Preserve failures.
5. Report each verified **!ID -> R00N / CLIENT / firmware / sensor fit**, resume
   the station and update labels. Sunday's ROUTER/site step and forced-relay/
   end-to-end acceptance remain explicit.

Implementation: [watch-raks.py](../../scripts/bench/watch-raks.py). This CLI
implements discovery/label refresh and port handoff. The preparation steps
remain the worker's procedure, not an automatic flashing mode in this CLI.
