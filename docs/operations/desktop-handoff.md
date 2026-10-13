# Desktop handoff — 2026-10-13

Owner has put project work and the repeater survey issue on hold. This handoff preserves the workspace; resume implementation or investigations only when the owner brings them forward. Read `AGENTS.md`, `PROJECT.md`, `CONTEXT.md`, `records/sessions.md`, `.scratch/TRACKER.md` and `.scratch/pilot/map.md` first, then run `git status` before editing.

## Get the workspace

On the new desktop, with GitHub SSH access configured:

```sh
git clone --recurse-submodules git@github.com:lfg-seth/snorr-meshlink.git
cd snorr-meshlink
git branch --set-upstream-to=origin/main main
git status --short --branch
git submodule status --recursive
```

For an existing clean checkout, fetch/pull `main` using `git pull --ff-only`, then run `git submodule update --init --recursive`. Inspect/preserve local edits first; do not reset or force-pull over them.

The firmware submodule is pinned to `54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb`, public release `v2.7.26.54e0d8d`. The fork branch is `snorr/rak-survey`; fresh clones normally start detached at the recorded commit. See [firmware setup](../research/firmware-workspace.md) before switching branches or updating the baseline. The firmware tree has no new survey implementation. Both repositories require their own commits/pushes when firmware changes resume.

## Preserved progress

- Portal: React/TypeScript/Vite prototype with Map, Users, Messages and Infrastructure; authenticated local PocketBase backend and Python simulation/replay worker already implemented. Added one-terminal `python3 backend/launch.py` supervision and launcher tests. Live MQTT/firmware adapters, physical sends and deployment remain unimplemented/unverified.
- Broker: fresh Mosquitto installed and auth/ACL checks passed locally on `127.0.0.1:1883`. Mike handles DNS/Nginx/certificates for intended `mqtt.snorr.org:8883`. Separate-host proxy access requires a restricted private listener; external TLS/auth/topic and real-device integration remain unverified. Broker issue remains held. Maintenance/reset scripts and [Nginx handoff](mqtt-nginx-handoff.md) are recorded; do not rerun the reset over the existing fresh broker.
- Hardware: owner confirms RAK4631 cores. Counts/condition and radio variants remain distinguished in [inventory](../../records/inventory.md); no new hardware readiness or measured coverage claimed.
- Survey: [Define repeater operations and direct-link placement testing](../../.scratch/pilot/issues/14-repeater-operations-survey.md) is open/deferred with claim released. [Requirements and draft](../research/repeater-operations-survey.md) preserve all discussion.

## Agreed survey prototype

- Always-available RAK responder on a dedicated survey application port, direct addressed zero-hop/no-ACK ping/pong, no autonomous survey pings or repeater survey logging.
- Native PKI with a separate survey public-key allowlist. Private key resides on the V4 and may transfer to replacement tester hardware; node/key discovery remains necessary. No survey admin privileges implied.
- Dell drives a USB-tethered GPS V4. Touchscreen GUI has large controls and entry pads, one-or-more repeater selection, sequential round-robin with one outstanding ping, minimum spacing between attempts, reply timeout, continuous/fixed attempts per repeater, start/pause/stop and explicit resume after disconnect.
- Automatic private attempt logging includes failures, optional site/antenna/notes and configuration segments. Readouts show directional RSSI/SNR, round-trip counts/timeouts, host response time and GPS age.
- Live map shows recorded GPS and success/timeout locations for revisiting dead spots. Independent GPS stream, stale/no-fix indication, per-repeater inspection and offline basemap preparation are design directions, not tested functionality.

No responder or survey GUI has been implemented, built, flashed or hardware-tested. Exact payload/configuration/UI/defaults and offline map behavior remain to verify. Field routes, coverage acceptance, power endurance, complete solar/cell build and permissions remain separate open questions.

## Local development when resumed

Use the repository pins in `.python-version` and `.nvmrc`; Linux or WSL is appropriate for the launcher, which does not support native Windows. Install dependencies in the new checkout using the documented [backend setup](../../backend/README.md) and [portal setup](../../portal/README.md). Run initialization only for a new local demo database; do not overwrite existing project data.

```sh
python3 backend/manage.py install
python3 backend/manage.py init-demo
cd portal
npm ci
cd ..
python3 backend/launch.py
```

Private databases, credentials, raw GPS tracks, logs, binaries and dependencies are ignored and are **not transferred through GitHub**. New initialization creates new fictional demo records/accounts. Moving existing private data requires a separate private backup/transfer; backup/restore has not been validated. GitHub carries source, planning records and sanitized evidence only.

Checks: `python3 backend/manage.py check` and `npm run check` from `portal/`. Server scripts can be syntax-checked locally; their privileged behavior should not be rerun merely for desktop setup.

When the owner resumes survey work, implement the minimal responder and touchscreen tester against the pinned release, then bench-check PKI authorization/key replacement, direct-only behavior with a third node, GPS freshness, losses and reconnect logging. Verify offline map preparation before field use. Preserve passive member GPS tracking as the first project priority.
