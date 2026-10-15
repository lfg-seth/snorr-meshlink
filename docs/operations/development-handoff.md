# Development handoff: Dell Linux and Windows/WSL

Updated 2026-10-14. The owner regularly switches between the **Dell laptop running Linux** and the **Windows desktop running WSL**. Treat both as active development machines. GitHub `origin` (`git@github.com:lfg-seth/snorr-meshlink.git`) is the shared source and project record. The hosted Ubuntu LXC is a separate deployment.

## Each time you switch machines

Before leaving, record completed work, open questions and the next step in `records/sessions.md`, commit explicit publishable paths and push the current branch. Keep `main` tracking `origin/main`. On the receiving machine, first check `git status`; preserve any local work before pulling. With a clean checkout on main:

```sh
git pull --ff-only origin main
git submodule update --init --recursive
```

If histories diverge, inspect and reconcile them; do not force-push or discard local changes. Use a separate branch when both machines have unfinished work. Read `AGENTS.md`, `PROJECT.md`, the newest session entries and `.scratch/pilot/map.md` at session start.

Keep the WSL clone in its Linux filesystem, for example `~/repos/snorr-meshlink`. Reinstall dependencies locally from the pinned versions/lockfiles; do not copy `.venv`, `node_modules` or built binaries between machines. Frontend checks are `npm ci` then `npm run check` inside `portal/`. Backend setup/check commands are in [backend/README.md](../../backend/README.md). Native local development uses fictional data; do not reinitialize the hosted database.

## Current state

- Hosted authenticated portal: `https://meshlink.spp.lol`, still running **simulation data**. Deployment, service and backup instructions: [portal LXC](portal-lxc.md). Source synchronization does not deploy the portal.
- Broker: `mqtt.snorr.org:8883`, validating TLS through Nginx to source-restricted private Mosquitto. Synthetic authentication/ACL checks pass. Gateway passwords were fitted to stock firmware; the worker account is read-only. See [MQTT handoff](mqtt-nginx-handoff.md).
- Bench: B001/B002 are original GPS-equipped Heltec V4s; G001/G002 are Heltec V3 uplinks, currently receive-only with downlink disabled. All four run stock `2.7.26.54e0d8d`. Saved roles/configurations survive reboot. Both V4s deliver encrypted fixtures and automatic GPS through both gateways. The short GPS sample has original measurement ages around 21–35 seconds; it does not establish sustained reliability, runtime or field coverage. [Measured results](../../records/field-results.md).
- `backend/worker.py` only ingests normalized simulation/replay data. There is **no persistent MQTT subscriber/decoder feeding the portal** and no real portal radio-send/name-update implementation.

## Resume: connect MQTT to the portal

The owner explicitly brought this forward immediately before the handoff. First settle whether the hosted view should switch to real devices only (recommended, unanswered) or keep a separately labelled demo. Preserve existing data with a verified backup before hosted changes.

Implement a persistent worker using the existing normalized ingestion boundary, verified physical-device mappings and the read-only broker account. Decode the pinned-build encrypted protobuf envelopes using the private channel key. Preserve GPS measurement timestamps and gateway receipts, deduplicate observations across gateways, reject unknown identities and maintain outage/stale behavior. Add meaningful adapter and ingestion tests, then deploy under the existing worker service and verify automatic real GPS end to end. Keep the V4s powered with sky view and V3s on working Wi-Fi during live verification. Portal downlink, survey work and wishlist features remain separate.

## Private state stays outside Git

Credentials, channel keys, raw tracks/captures, flash backups, databases and runtime environments are deliberately excluded. A Git pull does not transfer them. On the Dell, bench credentials/key/evidence and exploratory helpers are under ignored `private/bench/` (including `mqtt-credentials.json`, `channel.key` and `gps_mqtt_watch.py`); backend state is under ignored `local-data/backend/`. The private observer is a temporary bench tool, not a production worker. Reusable sanitized scripts are tracked under `scripts/bench/` and `scripts/server/`.

Desktop private provisioning and SSH access are not verified. Obtain necessary secrets through an owner-controlled private transfer or the authorized servers; never paste them into project records or commit them. Transfer only the needed secrets, not raw GPS history. Hosted worker credentials are `/etc/meshlink/worker.json`; the existing service has intentionally limited access. Broker canonical credentials are root-private `/root/meshlink-private/mqtt-credentials.json`; the private export path is documented in the bench scripts. Do not rotate/reset working accounts merely to switch development machines.

No live ingestion, additional RF test or hosted deployment was performed during this handoff. Dell USB permissions/port names do not establish Windows/WSL serial access. Firmware direct-TLS verification and other operational limits remain recorded in the bench source review; do not turn the short bench result into an operational-readiness claim.
