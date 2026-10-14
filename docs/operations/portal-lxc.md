# Portal LXC deployment

2026-10-13. Owner authorized configuring the Ubuntu LXC and publishing the portal through Cloudflare Tunnel at **https://meshlink.spp.lol**. This is the authenticated **simulation pilot**, with fictional members/devices/positions and simulated message/name outcomes. Live MQTT/firmware integration remains held.

## Deployed environment

- Ubuntu 24.04.5 LTS, amd64, 4 logical CPUs, 8192 MiB RAM, 512 MiB swap allowance and a 64 GiB SSD-backed root filesystem. These allocations were inspected inside the LXC; Proxmox settings and physical-host capacity were not inspected.
- Source at `/opt/meshlink`, static production frontend at `/var/www/meshlink`, and owner-only persistent state at `/var/lib/meshlink`. The checkout's `local-data/backend` symlink points to that state. Binaries, database, credentials and raw records stay outside Git.
- Node 22.23.1 is installed under `/opt` from the official archive with its SHA-256 checked. Node is used for builds; it is not a production web server. The Ubuntu Python 3.12 runtime passes the existing backend suite here; the earlier development documentation's Python 3.14.3 environment was not recreated on this server. PocketBase 0.40.5 is installed through the repository's verified release manifest.
- `meshlink-api.service` runs PocketBase as the unprivileged `meshlink` account on loopback 8090. `meshlink-worker.service` uses a separate `meshlink-worker` account and reads only its own root-owned, group-readable `/etc/meshlink/worker.json`, selected by `MESHLINK_WORKER_CREDENTIALS`. Its access to admin credentials and the database is denied and was checked. Both start at boot and restart on failure. Source is read-only to these services; only the API can write persistent state.
- Nginx serves the build on loopback 8080 and proxies the portal API/authentication routes. Raw collections, superuser administration and worker ingestion are unavailable through that proxy. Application roles remain enforced by PocketBase. Nginx trusts the connector's `CF-Connecting-IP`, overwrites forwarded IP headers, and PocketBase trusts only the resulting `X-Real-IP`; sign-in throttling stays enabled and was tested for separate client IPs. Request access logging and PocketBase IP logging are disabled.
- Owner installed/configured the existing remotely managed `cloudflared.service`; its four edge connections and route `meshlink.spp.lol` → `http://localhost:8080` were inspected. The deployment preserves that connector. No additional tunnel, router forwarding, Cloudflare Access policy or TLS bypass was added. Cloudflare credentials remain private on the LXC.
- Ubuntu unattended security updates are enabled. Automatic container reboot is disabled; Proxmox host/kernel updates remain outside this setup.

## Owner access

Open the portal and choose **Backend sign in**. View generated admin/member credentials privately in your own terminal:

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

For updates, take a verified backup first, stop worker/API before replacing backend source, install the reviewed source/build, apply any intentional schema migration separately and restart/check. The services use `--automigrate=false`; code rollback does not undo database migrations. Keep the source commit and previous release identifiable. No unattended application deployment is configured.

## Evidence and limits

- Existing 27 backend tests and 8 frontend tests pass on this LXC; TypeScript checking and production build pass. The existing large MapLibre bundle warning remains.
- Nginx and shell/Python deployment syntax pass. Local admin/member login, protected routes, independent client throttling, service restart persistence and isolated backup recovery pass.
- Public DNS through Cloudflare resolves the hostname; HTTPS frontend/API health return 200, unauthenticated state returns 401 and database administration returns 404. The connector has four active edge connections. Desktop HTTPS also passed with the public DNS answer supplied explicitly.
- LAN DNS retained a negative IPv4 answer during setup, while public DNS was correct; the LXC could see new IPv6 answers but has no usable IPv6 internet route. Normal browser access on the desktop remained blocked by its LAN resolver. Refresh/wait for the LAN DNS cache; do not disable certificate checks or change the portal to an IP address. Public browser UX/sign-in, actual reboot recovery, off-host backups, load/field performance and live MQTT remain unverified.

Primary references: [Cloudflare packages](https://pkg.cloudflare.com/), [Tunnel configuration](https://developers.cloudflare.com/tunnel/features/locally-managed-tunnels/configuration-file/), [PocketBase production guidance](https://pocketbase.io/docs/going-to-production/) and [proxy settings API](https://pocketbase.io/docs/api-settings/).
