# Portal LXC deployment

Initial deployment: 2026-10-13. Owner authorized the Ubuntu LXC and Cloudflare Tunnel at **https://meshlink.spp.lol**. Updated 2026-10-14: the portal now runs **real bench GPS data**, with fictional operational records privately archived and replaced by B001/B002 trackers and G001/G002 gateways. The receive-only MQTT worker, deduplication, restart and live-backup recovery are verified. [Live MQTT configuration, cutover and recovery](live-mqtt.md). Earlier simulation evidence below describes the original rollout.

## INA219 current graphs / MeshLink 0.1.4 - 2026-10-24

Current deployment: owner-selected [PR #64](https://github.com/lfg-seth/snorr-meshlink/pull/64)
is merged and deployed as **MeshLink 0.1.4 / `91d0ced` /
`meshlink-v0.1.4`**. INA219-equipped cards show current history and a separate
30-minute mean; both graphs offer 30min/6hr ranges. Same-commit 89 backend/63
portal checks, public asset hashes, protected-state preservation, pre/post
live/demo recovery and authenticated live average comparisons pass.
[Deployment, backups and remaining acceptance](device-card-current-history.md#meshlink-014-deployment---2026-10-24).

## Fleet current polarity / MeshLink 0.1.1 - 2026-10-24

Owner-selected [PR #59](https://github.com/lfg-seth/snorr-meshlink/pull/59) is
merged and deployed as **`a405987dc849acf9f609ed3764c967ceb292a333`**, tagged
**`meshlink-v0.1.1`**. The state API globally inverts environment and all eight
power-channel currents once: positive charging, negative discharging. Existing
caches and new reports share the conversion; raw evidence remains unchanged.
Server 75 backend/56 portal checks and clean live build pass, as do all ten
public asset hashes, protected-state preservation and verified pre/post live
and demo recovery. Root source marker and public `/version.json` agree on the
merged commit. [Exact deployment, current samples and recovery evidence](radio-report-ingestion.md#meshlink-011-deployment---2026-10-24).

## Recovery verifier maintenance - 2026-10-24

Installed live/demo recovery now compares exact provisioned/restored device
identities and the exact newest bounded battery history for all three windows.
The normal verifier commands pass on a fresh backup, including over-cap demo
history; task-local replacement scripts are no longer required. Carry
`recovery_checks.py` with both verifiers during future updates.
[Source, checksum, installation and recovery proof](backup-recovery-verifiers.md).
Application source/version and radio behavior are unchanged by this maintenance.

## Current neighbor signals and relative expiry - 2026-10-21

Owner explicitly authorizes deployment of the trial branch's reviewed GH-47 correction. Application **443ba03** is deployed with explicit additive migrations to both live/demo databases, preserving all pre-existing records, configuration and saved demo work. Server 74 backend/55 portal checks, live build, nine public assets, access/isolation boundaries and migrated backup recovery pass. Fresh SNNS reports produce useful current readings; cached standard tables cannot renew them. Actual-component replay verifies exact two-hour estimated-age expiry. Native/sustained acceptance and unseen upstream delay remain separate. [Release evidence and limits](neighbor-signal-visibility.md#deployment---2026-10-21). `main` and draft PR #50 remain unchanged.

## Telemetry receipt-time fallback - 2026-10-21

Application **8c5350e** from [PR #54](https://github.com/lfg-seth/snorr-meshlink/pull/54) is deployed 2026-10-21. Backend/frontend release, 63 backend/49 portal checks on the server, exact protected-state preservation, public hashes/authentication/services and isolated live/demo recovery pass. [Release evidence and fresh-receipt verification](battery-contact-freshness-20261021.md#deployment---2026-10-21).

## Gateway battery graph release - 2026-10-21

Owner authorizes deployment after restoring connectivity. Merged [PR #46](https://github.com/lfg-seth/snorr-meshlink/pull/46), application **`fa035509dfc2fd1492c8ae01618d99269c9a4f92`**, is deployed. Graphs preserve isolated readings when cadence is unknown; both gateways now have owner-confirmed 1000 mAh LiPo metadata. G002 has verified five-minute battery cadence and actual history rendering; G001 correctly awaits its first battery report. All 47 portal checks on pinned server Node, public assets/boundaries, six services, fresh MQTT ingestion and final isolated live/demo backup recovery pass. Prior frontend rollback is retained. Initial public asset permissions are corrected before final verification. [Exact release/backup evidence and limits](gateway-battery-graphs.md#verification-and-deployment).

## Demo feature examples and minimap navigation — 2026-10-20

Owner authorizes merging and deploying [PR #38](https://github.com/lfg-seth/snorr-meshlink/pull/38). Application source **`5d07d61d916290ea81d5ed98bfdadc6127f407eb`** is deployed at **https://meshlink.spp.lol**. The synthetic demo now includes member pack/voltage profiles, humidity, signed/zero sensor-power channels and three SNNS examples (thirteen directional signal rows total). Neighbor minimap endpoint icons open the corresponding device cards; the separate Open device buttons are removed. Endpoint-location context remains available.

All **59 backend and 46 portal checks**, TypeScript and the live production build pass, including on the pinned LXC runtime in `/opt/meshlink-release-5d07d61`. The isolated stage uses its own lockfile-installed dependencies; the older shared dependency folder lacked test packages. [Portal CI](https://github.com/lfg-seth/snorr-meshlink/actions/runs/39521996510) and [Backend CI](https://github.com/lfg-seth/snorr-meshlink/actions/runs/39521996418) pass on merged main. The previous broad map-test stall was a failed DOM-valued assertion expecting removal of the retained location section; corrected expectations pass the full scenario. No portal behavior was removed to satisfy the test.

Before promotion, all fourteen hook/migration files match the prior application after normalizing existing CRLF line endings; no schema migration is needed. Preserve prior application source/static assets and the **complete old synthetic workspace, including saved edits**, root-private at `/opt/meshlink-rollback-5d07d61` (`demo-state` holds the prior workspace). Promotion verifies exact live database-file and private configuration hashes while services are stopped; both are unchanged. The live nine device identities, owner-provided configuration and existing operational/history/archive rows are preserved. New hashed assets are published before an atomic index replacement; earlier hashed assets remain available for open tabs. `/opt/meshlink/SOURCE_COMMIT` identifies this application release; `RECORDS_COMMIT` identifies the separate evidence commit.

Private backup evidence:

- Pre-release `meshlink-20261021T003040Z.tar.gz`, SHA-256 `98f395065ca5b04a2ddf5049f49e136d83c6e9506d6f687e9145406e3670f700`.
- Post-release `meshlink-20261021T003651Z.tar.gz`, SHA-256 `bfc7889ec56a2b65e4f5762356f3fda8d9dd286251751f407683d5b10c84e417`.

Checksums and isolated live/demo database/API/history recovery pass. The pre-release demo already exceeded the 50,000-sample API history cap in its 7-day/30-day windows; the existing verifier incorrectly assumes untruncated responses. An isolated pre-release recovery check verifies the exact newest bounded samples and truncation flags for all windows. The refreshed checkpoint fits the limit and passes the existing post-release verifier. [Handle bounded battery history in demo recovery verification](https://github.com/lfg-seth/snorr-meshlink/issues/39) tracks the verifier correction; no API expansion or history deletion is part of this release.

All **126 installed application source files** and **nine build files** match the tested release, with build files also matching public HTTPS byte-for-byte. Public index SHA-256: `f3f5e0c6171031a9eefef4c827ff12bd23a8221fb0085fa41d2458abb4d61838`. Demo feature-state checks, proxy/authentication/throttling boundaries, live/demo token and OS isolation, all three demo history windows and all six services pass. Live feed heartbeat is online; the latest 200 archived envelopes validate and the queue is empty. No new MQTT receipt arrives during a 45-second observation, so fresh radio delivery is unverified by this release. No browser surfaces are available for native WebGL/mobile/keyboard visual review; [native verification](https://github.com/lfg-seth/snorr-meshlink/issues/6) remains separate. No hardware changes or field-performance claims.

## Deployed environment

- Ubuntu 24.04.5 LTS, amd64, 4 logical CPUs, 8192 MiB RAM, 512 MiB swap allowance and a 64 GiB SSD-backed root filesystem. These allocations were inspected inside the LXC; Proxmox settings and physical-host capacity were not inspected.
- Source at `/opt/meshlink`, static production frontend at `/var/www/meshlink`, and owner-only persistent state at `/var/lib/meshlink`. The checkout's `local-data/backend` symlink points to that state. Binaries, database, credentials and raw records stay outside Git.
- Node 22.23.1 is installed under `/opt` from the official archive with its SHA-256 checked. Node is used for builds; it is not a production web server. The Ubuntu Python 3.12 runtime passes the existing backend suite here; the earlier development documentation's Python 3.14.3 environment was not recreated on this server. PocketBase 0.40.5 is installed through the repository's verified release manifest.
- `meshlink-api.service` runs PocketBase as the unprivileged `meshlink` account on loopback 8090. `meshlink-worker.service` uses a separate `meshlink-worker` account and reads only its own root-owned, group-readable `/etc/meshlink/worker.json`, selected by `MESHLINK_WORKER_CREDENTIALS`. Its access to admin credentials and the database is denied and was checked. Both start at boot and restart on failure. Source is read-only to these services; only the API can write persistent state.
- Nginx serves the build on loopback 8080 and proxies the portal API/authentication routes. Raw collections, superuser administration and worker ingestion are unavailable through that proxy. Application roles remain enforced by PocketBase. Nginx trusts the connector's `CF-Connecting-IP`, overwrites forwarded IP headers, and PocketBase trusts only the resulting `X-Real-IP`; sign-in throttling stays enabled and was tested for separate client IPs. Request access logging and PocketBase IP logging are disabled.
- Owner installed/configured the existing remotely managed `cloudflared.service`; its four edge connections and route `meshlink.spp.lol` → `http://localhost:8080` were inspected. The deployment preserves that connector. No additional tunnel, router forwarding, Cloudflare Access policy or TLS bypass was added. Cloudflare credentials remain private on the LXC.
- Ubuntu unattended security updates are enabled. Automatic container reboot is disabled; Proxmox host/kernel updates remain outside this setup.

## Owner access

Open the portal to view the separate synthetic database demo automatically. **Sign in** at the top opens the live account form; **View demo** returns to the demo. Saved live sign-ins are validated and restored on refresh. The shared fictional demo workspace has no MQTT connection. View generated live admin/member credentials privately in your own terminal:

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

## RAK neighbor and sensor power ingestion — 2026-10-16

Owner-requested application `bed40dd3204b5ce98ce967468c97d69b5b78d0e5` is deployed. SNNS/standard neighbor reports fill the existing table and map relationships; signed environment/PowerMetrics voltage/current appear with original source/channel and clocks on Infrastructure/node cards. Live archive recovery and fresh R005/G001 normalization pass. All nine identities/configurations and original protected/history/archive records are preserved; demo migration is separate. [Contract, exact backup hashes and release verification](radio-report-ingestion.md).

All 57 backend and 45 frontend checks, TypeScript/live build, nine public assets, authenticated state/feed, six services, proxy/authentication boundaries and complete isolated live/demo backup recovery pass. Post-release backup `meshlink-20261017T033546Z.tar.gz` contains 13 reports/21 link rows; restored API power/link metadata matches stored values exactly, and replay adds zero records (22 duplicates). Current calibration/sign interpretation, fresh G002 delivery, sustained cadence/field performance and authenticated native/mobile visuals remain unverified. Source/static rollback is retained at `/opt/meshlink-rollback-bed40dd-final`; a source rollback does not undo the additive schema.

## Demo-first entry and iPhone login fields — 2026-10-16

Owner requests pushing and deploying both portal changes. Application source `60ea977f8559cdba61dd93f40f2d0f5f4b3d8f42` opens the separate database demo automatically for anonymous visitors, including production builds, with **Sign in** in the top header. Saved live sessions still validate on refresh; opening Sign in cancels any pending demo load. Demo connection failures leave live sign-in available. Username/password inputs use `max(16px, 1rem)` to address iPhone focus zoom while retaining manual zoom and larger font settings.

All 43 frontend checks, TypeScript and the live production build pass in `/opt/meshlink-release-60ea977` on the pinned server Node runtime. Initial staging omitted the tracked synthetic database required by one frontend test; adding that fixture from the same commit makes the full suite pass. Publish only frontend source/static assets, keeping backend code, schemas, live/demo databases and provisioning intact. Retain previous frontend source/assets and release markers root-private at `/opt/meshlink-rollback-60ea977`. Publish hashed assets before atomically replacing the index; previous hashed assets remain available to open tabs.

All nine build files match the tested release over public HTTPS. Index SHA-256: `9bc8a5300de05119f46e14da37d18d6d921faeff0484b118a6cc0db4cd96af74`. The published CSS contains the login font floor; public synthetic authentication/state succeeds. Protected live routes, authentication throttling, live account/state checks, demo-token rejection by live routes, demo OS isolation and all six services pass. The real-application DOM regression covers production startup, header action, demo read/write isolation, unavailable/misdirected demo responses, cancellation during loading and live sign-in refresh. Browser inventory is empty; native browser/WebGL and iPhone focus/keyboard behavior remain unverified.

Pre-release backup `meshlink-20261016T215107Z.tar.gz` (SHA-256 `3df44b9c0d2f54b68b5ba5ca6c8174ae4a641f7264bb266678a8ba4f3d722a8d`) and post-release backup `meshlink-20261016T215210Z.tar.gz` (SHA-256 `1600085d72647ade71866f0c4454f24cec4acb1d2c03a0ffe92d1d587187d1c2`) pass checksum and isolated live/demo database/API/history recovery, preserving the private MQTT archive. No fresh radio reception or field performance claim is added. `/opt/meshlink/SOURCE_COMMIT` identifies this application source; deployment evidence is recorded separately in `RECORDS_COMMIT`.

## GPS, neighbor maps, battery history and database demo release — 2026-10-16

Owner requests pushing and deploying all local changes. Release contains the shared GPS quality pill and same-fix metadata, neighbor table/map connections and endpoint navigation, assignment-aware card mini maps with shared basemap/marker styling, and infrastructure voltage history with 24hr/7day/30day windows. Live neighbor rows remain empty until a separate real-ingestion integration; the synthetic demo supplies ten illustrative rows and 30 days of fictional battery patterns. No radio firmware is flashed or monitoring stack installed.

Two additive migrations create the locked signal collection and index battery history queries. Verify them first against a private consistent copy of the live database; preserve existing operational rows and identities. Take and verify a pre-release backup before replacing backend code, stop the live worker/API for migration and source replacement, and retain matching prior source/static/configuration for rollback. Publish hashed frontend assets before replacing the index; keep old assets for open tabs. Code rollback does not reverse schema changes.

The separate demo API/worker run as `meshlink-demo` with state under `/var/lib/meshlink-demo`, using a root-owned copy of the pinned binary under `/opt/meshlink-demo`. `enable-demo.py` copies only the checked synthetic checkpoint, rebases scenario timestamps once and refuses to overwrite an existing runtime. API binds to loopback 8092. Nginx permits portal/authentication routes through `/demo-api`; dashboard/raw collections and worker ingestion remain local. Live services/configuration stay on their existing independent paths. Public demo credentials must never become live operational credentials. All viewers share the fictional demo workspace and its mutations. [Demo guide](../../backend/demo/README.md).

Backups now quiesce both sets of services and include demo state/binary/service definitions plus Nginx configuration alongside the existing private live state and MQTT queue/configuration. Updates must also run `install -m 0755 deploy/portal/backup.py /usr/local/sbin/meshlink-backup`: the installed backup service executes that helper, not the repository file directly. After release, run `verify.py --public`, `verify-demo.py`, and `verify-mqtt-archive.py`. The demo verifier checks all three history windows, simulation identity, demo-token rejection by live routes, denied OS access to live secrets/state, and isolated synthetic database/API/history recovery. These checks do not establish field performance or native browser/WebGL behavior. Deployment verified for application source `3ca3a9447ee4506ebf17721cd8cd57457b1c7c31`. All 52 backend checks pass locally and on the LXC; the pinned server Node runtime passes all 43 frontend checks, typecheck and the live build. Both migrations pass on a private consistent database copy and on live state with unchanged fingerprints for every pre-existing operational table. Seven live device identities remain intact, and the new live signal collection contains zero synthetic rows.

All nine build files match the tested release through public HTTPS byte-for-byte. Index SHA-256: `39ee9929e8895fe0f3d03b7ab349640c0b2205a85427cc18420476947fba43e0`. Live authenticated state, worker heartbeat, all 15 infrastructure history requests (five devices × three periods), protected proxy routes, per-client sign-in throttling and all six services pass. Public demo sign-in, separate simulation state, all three history periods and blocked dashboard/raw/worker routes pass using only deliberately public synthetic credentials. Demo tokens are rejected by live routes; the demo OS user cannot read live state or MQTT/worker secrets.

Pre-release backup `meshlink-20261016T211551Z.tar.gz`, SHA-256 `d4c53e1ad72ee903dcf40b2d194fee917ac693d8bf8e62ef1a83b297204dc498`, passes isolated live recovery. The first post-release check identified that systemd still used the older installed backup helper; installing the updated helper corrected demo-state inclusion. The demo verifier also replaced an incorrect fixed row-count expectation with exact comparison to saved battery samples. Final post-release backup `meshlink-20261016T211956Z.tar.gz`, SHA-256 `23058d3e28afe3a0e4785e3ae2881de815ca7dcb7d6a2ebb5e99abf28b4a37b2`, passes checksum, isolated live database/API/history/archive recovery and isolated demo database/API/exact-history recovery.

Staged build/source remain at `/opt/meshlink-release-20261016`; prior source, static assets and Nginx configuration are root-private at `/opt/meshlink-rollback-3ca3a94`. Earlier hashed assets remain available to open tabs. `/opt/meshlink/SOURCE_COMMIT` identifies the application release; the follow-up evidence/verifier commit is recorded separately in `RECORDS_COMMIT`. The existing archive's latest 200 deliveries pass envelope/binary-length checks, SQLite integrity is good and the durable queue is empty. No new receipt arrives during the 60-second post-release observation window; fresh radio ingestion/new quality-bearing fixes remain unverified, despite a broker-connected worker heartbeat. Native browser/WebGL/mobile review, real signal ingestion, field validation and off-host backups remain outstanding; no connected browser surfaces are available.

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
