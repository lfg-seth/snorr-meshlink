# GH-11: mobile survey GUI and laptop server

Execute with GPT-6 Astra, reasoning ultra. Owner approved this scope through
grilling on 2026-11-14. Build a separate application in this repository and run
in parallel with the firmware chat. First priority is actual iPhone Duo / iPad
mini access to a working simulated survey through the desktop's Tailscale.

## Outcome and inputs

Deliver `survey-app/`: a self-hosted laptop/desktop webserver, durable recording,
responsive touch GUI, contract simulator, replaceable firmware adapter boundary
and connection/run instructions. Read the authoritative
[v1 interface](../../docs/operations/survey-interface-v1.md) in full. The
[firmware chat](direct-hop-survey-firmware.md) owns actual USB framing and a
reusable scripts/survey adapter; you can complete the GUI against synthetic
events while that dependency is unmet. Mock success is not live acceptance.

Start with git status and required repository startup/context reads. Owner wants
this in the same repo but separate from the existing dispatch portal. Reuse
suitable project components/patterns without modifying production services.
Consult applicable Sites skill as local-only laptop software; there is no
authorization for public website hosting or Funnel publication.

## Scope, parallel ownership and source publication

Create an isolated checkout under ignored private/worktrees on a short-lived
codex/ branch starting from `codex/survey-assignments`. Preserve the root dirty
checkout, firmware submodule and other chat work. Own survey-app and its own
docs/tests. Firmware chat owns firmware, scripts/survey, USB protocol changes
and the four attached radios. Do not enumerate/open/flash/configure those
serial ports or contend with its test runner. Reconcile shared record edits
minimally. Read the shared v1 contract without editing it; implement a replaceable
adapter and tolerate compatible capability additions. No work depends on an
unreported implementation detail in another chat.

Owner authorizes desktop hosting accessible privately over Tailscale for phone
testing, then Linux laptop headless operation. Choose free ports and preserve
existing app/network configurations. Verified private host is
setheth-desktop.tail5dfe78.ts.net / 100.100.20.119. Existing Tailscale Serve HTTPS
8443 -> localhost:5180 belongs to another service; preserve it. Prefer a separate
private HTTPS Serve port when already enabled and feasible. Use current CLI
docs/status, add only your mapping, do not reset Serve or enable Funnel. If an
unmet tailnet-wide consent/admin permission blocks HTTPS, keep building and use
a private HTTP fallback if workable, accurately reporting secure-context limits.
Do not promise a placeholder URL. Keep host runtime local/private, no external
account integration or public deployment. Use Windows hidden background helpers
per workspace rules; provide clean start/stop and later Linux commands.

## Build and first mobile milestone

1. Read latest primary WebKit guidance, especially
   [Safari 27.1 / Duo](https://webkit.org/blog/18486/webkit-features-for-safari-27-1/).
   This is a real dual-display phone, not an ordinary fixed-size iPhone viewport.
   Build responsive from the start: outer portrait/landscape, inner portrait/
   landscape and narrow Split View, plus iPad mini and desktop. Preserve app
   state/commands across folding/rotation; measure container sizes and resize
   maps. Keep functionality available without experimental posture/segment
   feature flags or UA sniffing. Handle four-edge safe areas, browser toolbars,
   dynamic viewport height, keyboards, zoom and touch; keep controls reachable.
2. Implement the shared command/event adapter and a deterministic simulator with
   synthetic IDs/locations, including strong/weak/asymmetric links, timeouts,
   quiet/backdown, survey GPS fault, bench without GPS, USB/heartbeat loss,
   reconnect/replay, map outage and long-session event load. Use clear simulation
   labeling, isolated runtime storage and explicit source selection; never
   silently fall back from real hardware to mock success.
3. Launch a recognizable, usable simulated interface early. Verify it locally
   and privately through the owner's actual Tailscale FQDN/IP and chosen port.
   Return that working link in commentary as soon as ready so the owner can
   test Duo/iPad while you finish other work. Do not wait on firmware. Avoid
   changing global firewall/tailnet policy; request only a concrete unavoidable
   permission with a working local result ready for review. Keep working on
   independent functionality if external phone feedback has not arrived.

## Required product behavior

Map plus compact live instrument panel. Always make selected repeater, both
direction RSSI/SNR, round-trip success counts/rate, fresh GPS age/health, actual
cadence/backdown, connection and recording health and pause/stop easy to find.
Narrow screens can switch map/readout; larger screens show both. Use large
semantic touch controls and numeric fields appropriate for mobile keyboard
input. Expose firmware capabilities/settings, including GPS sample/age limits,
survey/bench mode, target lock, experimental profiles, timing and adaptation;
validate ranges and display actual applied settings/errors. Do not create
controls that pretend unsupported firmware features exist.

Server owns USB adapter connection, independent heartbeat, append-only durable
logs and browser subscriptions. Heltec owns the RF loop/GPS gate. One device
controls the run; no multi-user management or parallel-control feature is needed.
Browser lock/background/socket loss must not stop polling/recording. Reconnect
loads authoritative state/history and shows gaps. Laptop-to-client loss stops
RF and requires explicit resume. Avoid duplicate commands on reconnect. A
long-lived headless process must not depend on the browser tab to do work.

Preserve every attempt, independent GPS stream, timeout/late/duplicate/transport
events, actual profile, target fixed location and configuration-change segments.
Private append-only JSONL is appropriate; provide useful CSV export and session
replay without rewriting raw evidence. Clear log/queue/disk failure reporting is
required. Bound memory/display history while retaining durable evidence; dense
points must not freeze a phone. Raw tracks/locations/credentials stay ignored.
Use Heltec GPS exclusively for survey positions; browser GPS is not a fallback.

Default map coloring is vehicle-to-repeater SNR, with explicit direction and
RSSI/SNR selectors. Preserve both readings in point details/readout. Timeouts
need distinct symbols/text and never assert a specific failed direction. Show
GPS fix age and gaps; null locations remain unmapped. Support target filtering,
follow/current-position toggle, manual pan/zoom and past-attempt inspection,
plus fixed repeater markers from entered/imported records. A drawn line is an
estimate between measured positions. Avoid invented universal RSSI pass/fail
thresholds; make legend/scales intelligible and radio-context aware.

Starlink supports online use. Owner can pre-cache Mount Charleston AO on fast
home internet and prefers that if modest. Verify current primary map-source
terms before downloading; do not bulk-prefetch public tile services that forbid
it. Prefer a lawful laptop-served bounded offline package/cache with area/zoom/
size limits, progress/cancel, disk-budget accounting and readiness indication.
Reuse the private AO boundary when available; keep it out of Git. If a sound
offline mechanism is disproportionate, deliver Starlink/online plus permitted
bounded opportunistic caching and document the limit. No map-cache complexity
may block the first phone test or core survey controls/logging. Keep required
frontend assets local so a tile-provider outage does not disable the application.

## Acceptance and handoff

Test adapter/schema behavior, idempotent controls and truthful simulated vs live
states, persistence/replay, browser disconnect without run interruption, GPS
mode distinctions, errors/backpressure, session segmentation and map failure.
Verify responsive layouts at WebKit's Duo viewport sizes and narrow iPad
multitasking sizes, portrait/landscape, onscreen keyboard and long event lists.
Use browser QA where available; be explicit that desktop/Chromium emulation
does not prove native Safari, folding or physical device acceptance. Seek owner
feedback through the early link without blocking autonomous implementation.

When the firmware adapter is available, integrate its documented API without
opening boards until firmware chat has handed off ownership. If it is still
unavailable, complete all simulator/UI/backend work and report exactly the
pending adapter/live tests. Do not wait idle or substitute synthetic receipts
for hardware acceptance. Preserve the normalized contract and show capabilities.

Run appropriate project/app checks. Update sanitized GUI operations/evidence and
the tracker/session handoff once, stage explicit paths, commit and push every
completed commit to its authorized origin branch. Final handoff includes the
verified Tailscale phone-test link and service ownership/start/stop, mobile QA
results and limits, cache implementation or fallback, real-adapter status,
commit/branch/push and the next physical-device check. Leave the preview running
and private for the owner unless stopped/otherwise directed.
