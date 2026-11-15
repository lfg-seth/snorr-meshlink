# Live node terminal dashboard

From the repository root on Windows or Linux:

```sh
python scripts/watch-nodes.py
```

Requires Python 3.10+ and OpenSSH on the local computer, plus the existing
key-based access to `root@meshlink.int.spp.lol`. Use Windows Terminal or another
ANSI terminal, ideally at least 100 columns and 40 rows. No local Python packages
need installing. Stop with **Q** or **Ctrl+C**; the cursor and original screen return.

The table updates in place every three seconds. Each cell is colored by its
own stream's expected cadence: green while on schedule, yellow after one missed
due time, red after two missed due times, and gray when unknown. A new sample briefly
highlights its cell, including a new report of the same value. Values continue
aging while the connection is interrupted; SSH reconnects automatically with
a bounded backoff. The header distinguishes SSH snapshot age from the MQTT
worker's connected state and twenty-second heartbeat timeout.

Press **W** for the packet/telemetry watchdog matrix, **A** for all readings,
**P** for power/environment or **R** for radio/GPS. Each watchdog has its own
timer; SNNS cannot reset device, environment or power deadlines. Standard
NeighborInfo is tracked separately from passive SNNS. The header summarizes
on-time, late, two-or-more-missed, waiting and event-driven streams.

All table views keep the same order: repeaters, gateways, legacy gateway, then
member nodes, with labels ordered within each group. Nodes with no packet
activity in the last four hours, including never-heard nodes, are hidden from
the tables, summaries and details. Activity uses receipt time rather than GPS
or sensor measurement time. The exact four-hour boundary is hidden; a new
report makes the node reappear automatically. `--show-inactive` includes all
nodes for troubleshooting. Filtering does not reset watchdog history.

## Reporting cadence

The [cadence file](../../scripts/node-cadence.json) records saved profiles by
physical radio ID. It is a monitoring baseline; reverify it after changing
roles or report settings. A report's embedded interval updates its own
watchdog where supplied (gateway health, Wi-Fi and SD).

| Report | Expected interval |
| --- | --- |
| R001-R010 device, environment and INA219 power | 180 seconds / 3 minutes each |
| RAK passive SNNS | 180-second baseline; scheduling/jitter/airtime can defer |
| B002/B003 device and SNNS | 180 seconds / 3 minutes |
| B002/B003 GPS position packets | 120 seconds / 2 minutes |
| G001 screenless device, INA219 power, SNNS, backhaul and Wi-Fi | 300-second / 5-minute baseline |
| Other inventoried V3 gateways' device, SNNS and backhaul | 180-second / 3-minute baseline |
| R009 GPS position packets | 3,600 seconds / 1 hour; smart reports can occur earlier |
| Standard NeighborInfo on enabled ordinary boards | 21,600 seconds / 6 hours |
| NodeInfo | 10,800 seconds / 3 hours |
| G001 SD health | 86,400 seconds / 24 hours |

Source readbacks: [RAK batch](rak-batch-20261112.md),
[R009 GPS](r009-gps-20261112.md), [B003 profile](b003-v4-client.md),
[gateway rollout](gateway-backhaul-health.md), and
[screenless gateway profile and measured cadence](https://github.com/lfg-seth/snorr-meshlink/blob/0692833c9f5dcd8e0a20c44b2258f1914adb4446/docs/operations/g007-screenless-gateway.md#profile-and-source-verification).
B002's saved 2026-10-24 readback supplies its device/position/NodeInfo baseline.
Ordinary RAK environmental packets can contain INA219 voltage/current even
without temperature/humidity. Member environment/power and the screenless
target's suppressed standard NeighborInfo have no expected periodic watchdog.

For cadence **T**, the thresholds are **T + grace** for yellow and **2T + grace**
for red. Grace defaults to one polling interval (three seconds); `--grace 0`
gives exact boundaries. A three-minute stream becomes yellow at 183 seconds and
red at 363 seconds with the defaults. An on-time daily SD report stays green
through its 24-hour deadline. Yellow/red identify an overdue report; they do
not establish congestion, RF loss, reboot or power failure as the cause.

Watchdog cells show `cadence:time left`, for example `3m:2:45`. `3m:+20s` means
20 seconds overdue. `?` marks a stream awaiting its first report; its timer
starts when monitoring begins and becomes yellow/red at the same one/two-cycle
boundaries. That initial deadline survives SSH reconnects. `E:age` tracks an
observed event-only packet without inventing a periodic deadline. Text, routing
and other unconfigured packet types therefore never become overdue merely
because no event occurred. Extra telemetry variants get separate event timers.

The columns show device voltage, firmware charge status, INA219 channel-1
voltage/current, temperature, humidity, channel utilization, transmit airtime,
reported uptime, neighbor count and GPS measurement age. Positive current is
charging, negative discharging, matching the portal's single sign inversion.
`USB*` is firmware status 101 (charging or no detected battery), not 101% charge.
These are device reports, not calibrated measurements or runtime estimates.

Telemetry uses measurement time where known, otherwise receipt age. GPS age
always requires the GPS solution timestamp; a recent packet without that clock
shows `?`, even when it includes satellites and PDOP. A GPS packet watchdog can
be green while its solution time remains unknown or old; GPS measurement age
keeps the pilot's fifteen-minute upper limit. Neighbor age is the report
receipt age, not a guarantee that every neighbor was just heard. Gateway Wi-Fi,
MQTT, Wi-Fi signal, daily SD usage/drop counters and GPS quality appear below
the table with their own report ages. A daily SD report is not expected every
three seconds. Gateway up/down text describes the last report, with `LATE`
or `MISSED 2+` when its cadence deadline has expired.

The [physical roster](../../records/deployment-nodes.md) supplies fresh repeater
labels by radio ID. Member and gateway identities come from the server's
existing private MQTT configuration. Radios missing from portal registration
are explicitly listed as **Archive only**, and their valid archived telemetry
is decoded in memory. This does not register them or change portal assignments.
Restart after changing the roster or server mappings.

## Options

```sh
python scripts/watch-nodes.py --once
python scripts/watch-nodes.py --view power
python scripts/watch-nodes.py --view radio
python scripts/watch-nodes.py --view watchdogs
python scripts/watch-nodes.py --view watchdogs --packet device --packet environment --packet power
python scripts/watch-nodes.py --interval 5
python scripts/watch-nodes.py --host my-meshlink-ssh-alias
python scripts/watch-nodes.py --no-color
python scripts/watch-nodes.py --show-inactive
python scripts/watch-nodes.py --json
python scripts/watch-nodes.py --demo
```

`--once` prints one snapshot and exits. `--json` streams sanitized snapshots
without terminal control. `--plain` prints successive tables instead of moving
the cursor. Piped output and POSIX `TERM=dumb` also avoid cursor control. On
Windows, native console capabilities determine cursor support. `NO_COLOR`
disables automatic colors; monochrome values use `~` for aging, `!` for stale
and `?` for unknown. `--color always` forces ANSI colors when desired.

Below 100 columns the default table shows power/environment; choose
`--view radio` for the radio columns. Short terminals clip supplementary details
and indicate that they are hidden; enlarge the terminal or use `--once` to see
everything. The watchdog matrix fits as many stream columns as the terminal
allows and lists hidden types; use repeatable `--packet` filters to inspect
them. `--json` includes per-type cadence, last receipt, remaining time, missed
cycle count and state. `--demo` previews colors and changing cells with synthetic data and
never connects to SSH.

Use `--cadence-file` for alternate saved per-radio baselines and `--grace` for
the polling allowance. This replaces the initial fixed `--fresh`/`--stale` options.
`--roster` selects another file in the same physical-roster Markdown format.
Nonstandard SSH ports/keys belong in the user's SSH config. Advanced server
path overrides are listed by `--help`.

## Data access and checks

The client sends [the sampler](../../scripts/server/node_readings.py) to the
existing MQTT virtual environment through one SSH connection. It reads the
private configuration and opens SQLite with `mode=ro` and `query_only=ON`.
The initial scan covers 24 hours (`--hours` changes this); older stored readings
remain visible with their original timestamps. Later polls read only new
archive row IDs plus the small current-device/feed tables. Two-gateway copies
of the same encrypted radio packet cannot renew a reading. Out-of-order source
timestamps cannot replace newer clocked readings. Repeated generations of a
custom SD/health report do not pet its watchdog, even with a new mesh packet ID.
Each packet watchdog uses unique arrivals; each value retains its own source/
receipt time so a new environmental report cannot refresh an omitted humidity
field. Packet receipt does not itself establish a fresh GPS measurement.

No server script is installed, no service is restarted, no MQTT or radio command
is sent, and no serial port is opened. Credentials, channel keys, packet bytes,
member names and coordinates stay on the server. JSON exports contain only
sanitized measurements, radio IDs, timestamps and packet fingerprints; keep
operational exports under ignored `private/` or `local-data/`.

Offline regression checks:

```sh
python -m unittest discover -s scripts/tests -p test_node_watch.py -v
python scripts/check-project.py
```

These cover independent cadence deadlines, delayed/duplicate reports, unknown GPS time,
stale connection behavior, current polarity, identity mapping, privacy and
terminal formatting. Live acceptance uses `--once` followed by continuous
snapshots against the selected server; synthetic tests do not establish radio
coverage, sensor calibration, runtime or field readiness.

Verified on Windows, 2026-11-12: all 34 offline regressions and changed-document
checks pass. Eight watchdog-enabled live snapshots from 23:49:45 through
23:49:59 Pacific contain actual new B002/R007/R009 samples and zero skipped
decoder rows; a second SSH session also returns a valid snapshot. The live
matrix shows independently late/missing streams and the daily SD deadline.
ANSI in-place redraw, W switching to watchdog timers, Q exiting with status 0,
narrow rendering and cursor restoration pass in the terminal preview. Linux native rendering and
prolonged outage recovery remain unmeasured.

2026-11-13 follow-up: 37 offline tests pass, including consistent ordering
across A/W/P/R, the exact four-hour cutoff, never-heard nodes, optional inactive
display and reappearance based on a new receipt despite an old GPS fix.
A live 00:18 Pacific snapshot shows 13 active nodes in the same grouped order
and hides five inactive/never-heard nodes.
