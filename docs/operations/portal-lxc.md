# Portal LXC deployment

Initial deployment: 2026-10-13. Owner authorized the Ubuntu LXC and Cloudflare Tunnel at **https://meshlink.spp.lol**. Updated 2026-10-14: the portal now runs **real bench GPS data**, with fictional operational records privately archived and replaced by B001/B002 trackers and G001/G002 gateways. The receive-only MQTT worker, deduplication, restart and live-backup recovery are verified. [Live MQTT configuration, cutover and recovery](live-mqtt.md). Earlier simulation evidence below describes the original rollout.

## Deployed environment

- Ubuntu 24.04.5 LTS, amd64, 4 logical CPUs, 8192 MiB RAM, 512 MiB swap allowance and a 64 GiB SSD-backed root filesystem. These allocations were inspected inside the LXC; Proxmox settings and physical-host capacity were not inspected.
- Source at `/opt/meshlink`, static production frontend at `/var/www/meshlink`, and owner-only persistent state at `/var/lib/meshlink`. The checkout's `local-data/backend` symlink points to that state. Binaries, database, credentials and raw records stay outside Git.
- Node 22.23.1 is installed under `/opt` from the official archive with its SHA-256 checked. Node is used for builds; it is not a production web server. The Ubuntu Python 3.12 runtime passes the existing backend suite here; the earlier development documentation's Python 3.14.3 environment was not recreated on this server. PocketBase 0.40.5 is installed through the repository's verified release manifest.
- `meshlink-api.service` runs PocketBase as the unprivileged `meshlink` account on loopback 8090. `meshlink-worker.service` uses a separate `meshlink-worker` account and reads only its own root-owned, group-readable `/etc/meshlink/worker.json`, selected by `MESHLINK_WORKER_CREDENTIALS`. Its access to admin credentials and the database is denied and was checked. Both start at boot and restart on failure. Source is read-only to these services; only the API can write persistent state.
- Nginx serves the build on loopback 8080 and proxies the portal API/authentication routes. Raw collections, superuser administration and worker ingestion are unavailable through that proxy. Application roles remain enforced by PocketBase. Nginx trusts the connector's `CF-Connecting-IP`, overwrites forwarded IP headers, and PocketBase trusts only the resulting `X-Real-IP`; sign-in throttling stays enabled and was tested for separate client IPs. Request access logging and PocketBase IP logging are disabled.
- Owner installed/configured the existing remotely managed `cloudflared.service`; its four edge connections and route `meshlink.spp.lol` → `http://localhost:8080` were inspected. The deployment preserves that connector. No additional tunnel, router forwarding, Cloudflare Access policy or TLS bypass was added. Cloudflare credentials remain private on the LXC.
- Ubuntu unattended security updates are enabled. Automatic container reboot is disabled; Proxmox host/kernel updates remain outside this setup.

## Owner access

Open the portal and sign in on the landing page. **View demo** opens fictional browser-only devices without an account; **Exit demo** returns to sign-in. View generated admin/member credentials privately in your own terminal:

```sh
ssh root@meshlink.int.spp.lol
cd /opt/meshlink
python3 backend/manage.py credentials
```

Do not paste credential output into chat, logs or Git. Account administration commands in `backend/README.md` work from this checkout. The superuser dashboard remains private: use an owner SSH forward to loopback 8090 if database administration is required, rather than exposing it through the tunnel.

For service status and private diagnostics:

```sh
systemctl status meshlink-api meshlink-worker nginx cloudflared
journalctl -u meshlink-api -u meshlink-worker
```

## Backups and verification

`meshlink-backup.timer` runs daily at **02:30 America/Los_Angeles** and catches a missed window at startup. The root-only backup briefly stops the worker, then the API, archives the entire private state plus matching backend/deployment source and static frontend, and restarts whichever services were running. Archives and SHA-256 manifests are stored in `/var/backups/meshlink`; retain 14 complete archives. No pilot records are pruned. Backup failure retains prior archives and attempts to restart services.

```sh
systemctl start meshlink-backup.service
systemctl list-timers meshlink-backup.timer
python3 /opt/meshlink/deploy/portal/verify.py --public
```

The check signs in only through loopback, confirms proxy boundaries and per-client sign-in limits, validates the archive checksum, restores into a root-private temporary directory, checks SQLite integrity and starts a separate API on loopback 18090. Restored credentials, members, assignments, messages, incidents and events are compared; history/receipt collections remain populated. The isolated instance is stopped and removed afterward. The live database is never replaced by this check.

Public probes use curl without credentials and retain HTTPS certificate/hostname verification. Cloudflare currently returns 403 to Python's default HTTP user-agent; no edge protection was changed. An attempted public authenticated check was rejected by automatic approval review because it would transmit generated admin credentials through Cloudflare. That check was replaced with credential-free public probes. Owner browser sign-in through the public tunnel remains to verify.

**These backups share the container's disk.** They cover application recovery, not loss of the container/Proxmox storage. Configure Proxmox backups or copy encrypted/private archives to a separate owner-selected destination; no destination or Proxmox administrative access was supplied. Do not publish these archives because they include passwords and future operational records. A live replacement restore must stop both services, preserve the current state separately, restore the matching archived backend and state with `meshlink` ownership, regenerate the worker-only credential via `configure.py` once the API is running, and recheck before reopening service. Isolated recovery is verified; a destructive live restore has not been exercised.

## Reproduction and updates

The tracked `deploy/portal/install.sh` supports an amd64 Ubuntu source tree at `/opt/meshlink`. It installs dependencies, builds/tests the frontend, prepares state/services and initializes fictional records only when both database and credentials are absent. It does not authorize or replace a Cloudflare connector. For a new host, configure a remotely managed tunnel route to loopback 8080 after installation using [Cloudflare's setup instructions](https://developers.cloudflare.com/tunnel/get-started/).

For updates, take a verified backup first, stop worker/API before replacing backend source, install the reviewed source/build, apply any intentional schema migration separately and restart/check. The services use `--automigrate=false`; code rollback does not undo database migrations. Keep the source commit and previous release identifiable. No unattended application deployment is configured. The simulation installer now refuses existing live MQTT provisioning; use the live operations guide for this instance.

## Sign-in refresh fix — 2026-10-16

Owner authorizes deploying source commit `ee5e57e8c8993a75313fc5032826a0559c3e924e`. Previously, refreshing discarded the React-memory account token. The portal now saves only that token in tab-scoped `sessionStorage` and validates it through the protected state endpoint before restoring the workspace with current account details. Sign-out/rejected authentication clear it, temporary outages offer retry, and blocked storage falls back to memory-only sign-in. Demo entry still resets on refresh.

Frontend tests, TypeScript and production build pass locally and in an isolated release directory on the pinned LXC Node runtime. The staged dependency install uses the lockfile; the older shared server dependency folder lacked jsdom. All seven release files match the tested build on disk, through Nginx and over public HTTPS. Index SHA-256: `8d4609f7d4a2ae67f1edf80580da09a5ed1af2525629fcc553f0564fc709eb03`. Loopback sign-in/token reuse, current server account, real-device counts, live worker heartbeat and rejected-token checks pass. All four services are active. Native browser sign-in/refresh remains unverified because no browser is connected.

The release replaces frontend source/static files only; no backend code, schema or provisioning changes. Assets are installed before an atomic index replacement, and prior hashed assets remain available to open tabs. `/opt/meshlink/SOURCE_COMMIT` identifies this source. Previous frontend source, available changed documentation and all static assets are retained root-private at `/opt/meshlink-rollback-ee5e57e`. The staged tested source/build remains at `/opt/meshlink-release-ee5e57e`.

Pre-release backup `meshlink-20261016T161141Z.tar.gz`, SHA-256 `36ab7b4493fcba9453a049aa9224cb19f33bf24acc6c4b4f1aef194b298ceb4d`, passes checksum, isolated database/API/history recovery and public proxy/authentication checks.

Post-release backup `meshlink-20261016T161434Z.tar.gz`, SHA-256 `888f4a778e53938dbdf4b158aa06026f8149f3201aa2974b7cc64b81d9b6747a`, passes the same isolated integrity/API/history recovery, including MQTT archive preservation. Proxy boundaries, per-client sign-in throttling and public TLS/protected-route checks also pass after release. All four services are active after the backup restart.

## Map and demo release — 2026-10-15

Owner authorizes deploying source commit `3964f46b877791bcd4ce737a35a5f18838010a27`. Map fills the available screen, infrastructure is always visible, and device selection opens a content-sized mobile bottom sheet up to 85% of the viewport. Tracker cards use the revised location/session, copy and battery indicators; summary counts live on Users. Shared branding uses the supplied SNORR logo.

Production remains a live-mode build with sign-in as the initial page. **View demo** explicitly opens only fictional browser state, labelled Demo in the shared header; **Exit demo** returns to sign-in and refresh resets the choice. Demo viewing makes no operational API requests. Avery/S001 has a full battery and a simulated GPS fix each minute. The backend remains live; no demo database/account initialization is performed.

The additive `1792110000_member_shortnames.js` migration adds optional member map shortnames and known Heltec V4 type metadata for B001/B002. It passes against a private live-database copy and then the live database, preserving all existing operational rows and seven device identities. Both local and staged LXC runtimes pass 46 backend tests; frontend tests, TypeScript and production build pass. The verified build is installed with its index published after assets; previous hashed assets remain available for open tabs. `/opt/meshlink/SOURCE_COMMIT` records the deployed source. Previous source/static files are root-private at `/opt/meshlink-rollback-3964f46`; the schema change is additive, and restoring old source does not undo it.

Public HTML and referenced assets match the staged build byte-for-byte. Authenticated real-device state/type metadata, worker heartbeat, all four services, anonymous state/profile denial, proxy boundaries, authentication throttling and public TLS checks pass. Post-release backup `meshlink-20261015T222458Z.tar.gz` has SHA-256 `6873c79a5949cef61ace28916c8f60550c298fb8ce16abcca193e0ec295d516d` and passes isolated API/database/history recovery, including the MQTT archive. Pre-release backup is `meshlink-20261015T222413Z.tar.gz`.

No browser is connected for native visual/mobile/clipboard review. Friendly-area boundaries, complete session aggregation beyond the existing snapshot cap, and measured INA219 ingestion remain follow-ups; this release does not fabricate those values.

## Evidence and limits

- Existing 27 backend tests and 8 frontend tests pass on this LXC; TypeScript checking and production build pass. The existing large MapLibre bundle warning remains.
- Nginx and shell/Python deployment syntax pass. Local admin/member login, protected routes, independent client throttling, service restart persistence and isolated backup recovery pass.
- Public DNS through Cloudflare resolves the hostname; HTTPS frontend/API health return 200, unauthenticated state returns 401 and database administration returns 404. The connector has four active edge connections. Desktop HTTPS also passed with the public DNS answer supplied explicitly.
- LAN DNS retained a negative IPv4 answer during setup, while public DNS was correct; the LXC could see new IPv6 answers but has no usable IPv6 internet route. Normal browser access on the desktop remained blocked by its LAN resolver. Refresh/wait for the LAN DNS cache; do not disable certificate checks or change the portal to an IP address. Public browser UX/sign-in, actual reboot recovery, off-host backups, load/field performance and live MQTT remain unverified.

Primary references: [Cloudflare packages](https://pkg.cloudflare.com/), [Tunnel configuration](https://developers.cloudflare.com/tunnel/features/locally-managed-tunnels/configuration-file/), [PocketBase production guidance](https://pocketbase.io/docs/going-to-production/) and [proxy settings API](https://pocketbase.io/docs/api-settings/).
