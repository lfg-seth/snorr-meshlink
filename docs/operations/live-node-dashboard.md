# Live node terminal dashboard

From the repository root on Windows or Linux:

```sh
python scripts/watch-nodes.py
```

Requires Python 3.10+ and OpenSSH on the local computer, plus the existing
key-based access to `root@meshlink.int.spp.lol`. Use Windows Terminal or another
ANSI terminal, ideally at least 100 columns and 40 rows. No local Python packages
need installing. Stop with **Ctrl+C**; the cursor and original screen return.

The table updates in place every three seconds. Each cell is colored by its
own reading age: green below five minutes, yellow from five to fifteen minutes,
red at fifteen minutes or older, and gray when unknown. A new sample briefly
highlights its cell, including a new report of the same value. Values continue
aging while the connection is interrupted; SSH reconnects automatically with
a bounded backoff. The header distinguishes SSH snapshot age from the MQTT
worker's connected state and twenty-second heartbeat timeout.

The columns show device voltage, firmware charge status, INA219 channel-1
voltage/current, temperature, humidity, channel utilization, transmit airtime,
reported uptime, neighbor count and GPS measurement age. Positive current is
charging, negative discharging, matching the portal's single sign inversion.
`USB*` is firmware status 101 (charging or no detected battery), not 101% charge.
These are device reports, not calibrated measurements or runtime estimates.

Telemetry uses measurement time where known, otherwise receipt age. GPS age
always requires the GPS solution timestamp; a recent packet without that clock
shows `?`, even when it includes satellites and PDOP. Neighbor age is the report
receipt age, not a guarantee that every neighbor was just heard. Gateway Wi-Fi,
MQTT, Wi-Fi signal, daily SD usage/drop counters and GPS quality appear below
the table with their own report ages. A daily SD report is not expected every
three seconds. Gateway up/down text describes the last report; `STALE` means
its three-report-interval freshness window has expired.

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
python scripts/watch-nodes.py --interval 5
python scripts/watch-nodes.py --host my-meshlink-ssh-alias
python scripts/watch-nodes.py --no-color
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
everything. `--demo` previews colors and changing cells with synthetic data and
never connects to SSH.

Use `--fresh` and `--stale` for alternate age thresholds in seconds.
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
timestamps cannot replace newer clocked readings.

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

These cover independent freshness, delayed/duplicate reports, unknown GPS time,
stale connection behavior, current polarity, identity mapping, privacy and
terminal formatting. Live acceptance uses `--once` followed by continuous
snapshots against the selected server; synthetic tests do not establish radio
coverage, sensor calibration, runtime or field readiness.

Verified on Windows, 2026-11-12: all 18 offline regressions and changed-document
checks pass. Eight live snapshots from 23:25:16 through 23:25:30 Pacific contain
actual new gateway/R009 samples and zero skipped decoder rows; a second SSH
session also returns a valid snapshot. ANSI in-place redraw, narrow rendering
and cursor restoration pass in the terminal preview. Linux native rendering and
prolonged outage recovery remain unmeasured.
