# Direct-hop survey interface v1

Owner-approved assignment boundary, 2026-11-14. The
[firmware assignment](../../.scratch/tasks/direct-hop-survey-firmware.md) and
[GUI assignment](../../.scratch/tasks/direct-hop-survey-gui.md) implement this
interface in parallel. This is a proposed software contract, not installed
firmware or live acceptance. The tracker owns task status.

## Ownership and architecture

Heltec client firmware owns the radio polling loop, one outstanding attempt,
target selection, deadlines, GPS interlock and adaptive cadence. A laptop
process owns USB, host heartbeats, durable logs and browser connections. The
browser issues explicit commands and displays state. Closing Safari, folding
the phone, changing orientation or losing the browser socket does not stop a
run. Losing the laptop-to-Heltec heartbeat does stop it.

Firmware worker owns the actual USB framing and a small Python adapter/bench
harness in `scripts/survey/`. Use existing Meshtastic framing where appropriate;
keep debug text separate from machine messages. Produce a usable, versioned
connection document and reusable adapter. The GUI worker owns `survey-app/`
and its host process, and initially uses a simulator implementing the normalized
contract below. This document defines the host-facing semantics, not a promise
that ordinary Meshtastic USB already supports them. Live adapter integration
can follow without waiting to build/test the mobile GUI. GUI worker never
opens a physical serial port during the firmware worker's bench ownership.

Each implementation uses an isolated checkout/branch. Read the latest owner
records in the original checkout when identifying hardware; the planning branch
does not supersede newer physical assignments. Firmware worker is the sole
editor of this contract after dispatch. Maintain v1 names/required semantics;
add optional fields/capabilities compatibly and publish actual wire details.
GUI worker can maintain its adapter mapping without editing firmware/schema.

## Normalized command and event envelopes

Commands are JSON objects:

```json
{"v":1,"kind":"command","id":"cmd-17","name":"start","params":{"mode":"survey","target_id":"!00000001"}}
```

Events are JSON objects:

```json
{"v":1,"kind":"event","seq":41,"boot_id":"example-boot","name":"ack","data_source":"simulation","data":{"command_id":"cmd-17","ok":true,"applied":{},"error":null}}
```

Require v/kind/name and command id/params or event seq/boot_id/data_source/data.
Unknown optional fields are tolerated; unsupported versions/commands/settings
receive an explicit error. Every command receives an ACK/error, including the
actual applied values. ACK means applied/accepted as described, not RF delivery.
Use idempotent command IDs, prevent duplicate starts and reject ambiguous
changes during an active attempt. Resume/start never happens implicitly after
a fault, reboot, adapter reconnect or browser resubmission.

Commands: `hello`, `get_state`, `configure`, `start`, `pause`, `resume`, `stop`,
`set_target`, `heartbeat`. `configure` and `set_target` may be rejected while
running unless the implementation safely segments the change. Stop must remain
available. `start` selects explicit `survey` or `bench` mode. Default is survey.

Events: `hello`, `ack`, `state`, `gps`, `attempt`, `result`, `fault`, `quiet`,
`statistics`. Stable event identity is boot_id + seq; preserve session_id and
attempt_id across the pipeline. On reconnect, obtain an authoritative snapshot
and host-stored history; show a gap when replay is unavailable. Publish queue
pressure/overflow and dropped counts instead of silently claiming full capture.

`hello` exposes build/protocol, hardware identity, supported commands, settings
and their ranges/defaults, units, capabilities and actual radio profile. `state`
exposes run state, mode, session/segment/target, applied settings, GPS health,
host-heartbeat health, queue state, quiet deadline and cumulative counts.

## Settings and measurements

Expose through configure/capabilities: target(s), production/experimental radio
profile, minimum attempt interval, response timeout, adaptive pacing enable and
limits, channel-utilization target/backdown thresholds, GPS update/freshness
thresholds, and host heartbeat interval/timeout. Firmware enforces feasible
ranges. Initial GPS target is one fresh fix/second with maximum age 2,000 ms;
verify feasibility on the actual receiver. Default quiet duration is 900 seconds
after the most recent recognizable direct survey ping; document any tuning.
Never let the GUI promise unsupported settings. Record profile/configuration
changes as new segments; mark experimental settings visibly.

For every attempt/result preserve session_id, segment_id, attempt_id, sequence,
target_id, mode, status, radio/build/profile and provenance. Status distinguishes
`success`, `timeout`, `cancelled`, `late`, `rejected`, `deferred` and
`transport_lost`; repeated/late replies do not create a new successful attempt.
Preserve the underlying reason and duplicate relation where applicable.

Successful results include `uplink` and `downlink`, each containing nullable
`rssi_dbm` and `snr_db`. Uplink is measured at the repeater on that exact ping;
downlink is measured at the client on the matching pong. Unknown is null, never
zero. Include `rtt_ms`, monotonic timing and separate host receipt time; distinguish
enqueue/TX/receive times and label estimates. Include available local/remote
channel utilization, predicted/measured airtime and direct-path evidence.

`gps` and the GPS snapshots on attempts/results contain `valid`, `lat_deg`,
`lon_deg`, `altitude_m`, `fix_utc_ms`, `fix_age_ms`, and nullable quality/satellites
where measured. Retain the send-time fix and optionally reply-time fix separately.
Absent/invalid location fields are null. Never invent/interpolate measurements
or reassign a newer fix to an older attempt. Use monotonic ages for gating;
retain original GPS fix time plus host receipt rather than conflating clocks.
Stream fresh local GPS independently of RF attempts, without GPS LoRa broadcasts.

## RF behavior and GPS modes

New versioned PING/PONG application packet types remain inside Meshtastic;
select a noncolliding private port/encoding. Broadcast PING carries the selected
responder; all hearing nodes enter quiet, only selected responder pongs. Both
directions use zero hops, no ACK/retries and no MQTT path. Explicitly prevent
forwarding of survey packet types even if presented with a positive hop budget.
Suppress unwanted generic replies from nontargets. Any recognizable, decoded
direct-RF survey PING triggers quiet regardless of target or survey authorization;
do not treat unrelated RF energy/malformed bytes as a recognizable survey ping.
The earlier PKI-only quiet-trigger proposal is superseded. Define responder
authentication separately; preserve existing survey authorization where feasible
without gating the any-ping quiet trigger. Native PKI cannot broadcast to all.

Quiet suppresses own periodic/unsolicited telemetry, positions (including smart
movement sends), node-info, neighbor/SNNS and other autonomous RF. Preserve GPS
acquisition, USB control/local reporting and intended pongs. Audit queued reports,
repeated pings, expiry, reboot and restoration without a catch-up flood. Global
TX disable cannot implement this because pongs must transmit. Keep ordinary
non-survey relay/explicit admin semantics documented; this is not authorization
to silence unrelated remote devices or change the live portal/gateways.

Survey mode pauses and emits fault on stale/missing GPS, defaults to explicit
resume after recovery. Bench mode continues RF checks with missing GPS, labels
it everywhere, and never fabricates map coordinates or claims coverage acceptance.
The window-positioned Heltec may obtain fixes; bench GPS failure does not block
testing the rest of the firmware. Laptop heartbeat loss pauses in either mode.

## Data and GUI contract

Desktop first, later a Linux laptop; server can run headless. Windows and Linux
host support must be explicit. Raw tracks, locations, device exports, pairing
secrets and runtime data stay in ignored private/local-data storage. Simulation
is unmistakable, uses synthetic IDs/positions and never mixes with live records.
Browser is not a serial client and its own GPS is not the survey location source.

Map defaults to vehicle-to-repeater SNR with direction and RSSI/SNR selectors.
Timeouts have a distinct symbol and mean failed round trips, not proven uplink
failure. Preserve map points, independent GPS trail, target sites, sample counts,
fix age, both signal directions, actual rate/backdown and recording health.
Repeater fixed locations may be entered/imported; unknown remains unknown.

Starlink is available. Prefer a bounded, explicit pre-cache of the Mount
Charleston AO at home when a provider permits it and implementation is modest.
Show bounds, zooms, estimated bytes, progress/cancel and readiness. If a sound
offline package is disproportionate, deliver online tiles plus legal bounded
opportunistic caching and document the limitation; do not block mobile testing.
Map failure must not stop controls/logging. Keep AO source coordinates private.

## Mobile hosting and acceptance

Desktop Tailscale IP supplied by owner: 100.100.20.119. Read-only verification on
2026-11-14 found `setheth-desktop.tail5dfe78.ts.net` online and existing Serve
HTTPS port 8443 proxying localhost:5180. Those endpoints are already in use;
preserve them. GUI worker selects free ports, verifies its private test service,
and returns an actual Tailscale FQDN/IP link. No public Funnel publication.
HTTPS Serve is preferable when already enabled, preserving existing mappings.
HTTP over Tailscale is a fallback with secure-context limitations disclosed.
Do not promise an unverified URL or disable browser certificate checks.

iPhone Duo outer/inner displays, both orientations and Split View must preserve
session state. Use actual container/viewport sizes, safe insets on every edge,
appropriate dynamic/small viewport heights and keyboard-aware controls. Keep
touch targets readable, support zoom, avoid hover-only controls and resize the
map renderer with its container. Baseline requires no experimental browser flags.
In Safari 27.1, Duo posture/segments APIs are previews behind flags; feature-detect
enhancements only. WebKit lists 382/594/669/951 CSS-pixel widths and 385-pixel
split windows. iPad mini also needs rotation and narrower multitasking layouts.
Emulation/Chromium screenshots do not establish physical Safari/fold acceptance.

First GUI milestone: simulated survey reachable on owner's actual Duo/iPad via
Tailscale, before live integration. Test running, weak/asymmetric links, timeouts,
quiet/backdown, stale GPS pause, bench-without-GPS, USB loss, backend reconnect,
map outage, keyboard, resize and long logs. One controlling device; no
multi-user roles/management work. Browser disconnection never stops host logging.

## Primary references

- [Pinned firmware readiness and timing](../research/direct-hop-upstream-research-20261113.md).
- [WebKit Safari 27.1 / Duo](https://webkit.org/blog/18486/webkit-features-for-safari-27-1/).
- [WebKit safe areas](https://webkit.org/blog/7929/designing-websites-for-iphone-x/).
- [Tailscale Serve](https://tailscale.com/docs/features/tailscale-serve).
- [HTTPS and Tailscale browser limitations](https://tailscale.com/docs/how-to/set-up-https-certificates).
