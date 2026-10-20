# Private MeshMonitor deployment

2026-10-17. Owner authorizes internal-only MeshMonitor, reusing existing Grafana/Prometheus, 30-day metrics and no automatic packet/history pruning. Searchable logs remain deferred. [Scope decision](../../.scratch/pilot/issues/20-monitoring-scope-stack.md), [deployment issue](https://github.com/lfg-seth/snorr-meshlink/issues/22), [verification follow-up](https://github.com/lfg-seth/snorr-meshlink/issues/23).

## Access and services

| Component | Internal address | Role |
| --- | --- | --- |
| MeshMonitor | <http://meshmonitor.int.spp.lol:3001> | Authenticated exploratory radio UI; standalone read-only MQTT source |
| Grafana | <https://grafana.int.spp.lol/d/snorr-meshmonitor/snorr-meshmonitor> | **SNORR MeshLink → SNORR MeshMonitor** dashboard, existing Prometheus data source |
| Prometheus | <http://prometheus.int.spp.lol:9090> | Existing server; new `snorr-meshmonitor` job, authenticated 30-second scrape |

SSH uses `root@meshmonitor.int.spp.lol`, `root@grafana.int.spp.lol` and `root@prometheus.int.spp.lol`. MeshMonitor binds only its private IPv4 address, port 3001; initial provisioning used loopback. Browser access is HTTP on the internal network. MQTT uses certificate/hostname-verified TLS to the existing broker. No Cloudflare route, inbound forwarding or radio/broker reconfiguration was added.

MeshMonitor login: `admin`, with a random password stored root-only in `/etc/meshmonitor/admin-login.json`. The owner can retrieve that file over SSH; do not paste it into issues, Git or shared logs. Existing Grafana login is unchanged. Anonymous mode and the default anonymous account are disabled. Public health/authentication metadata may remain available; anonymous node enumeration returns `[]`, and the metrics API returns 401.

Separate non-admin `prometheus` user/token has read grants for nodes/messages/packet monitoring on this source, private-channel map visibility, and slot-0 map visibility for upstream telemetry-only rows whose channel is NULL. No configuration/key-read/write privileges are granted. The bearer token lives root-only on MeshMonitor and at `/etc/prometheus/meshmonitor-secrets/metrics-token` (root:prometheus 0640) on Prometheus. MQTT reuses the existing read-only `pilot-worker` account with a distinct generated client ID; a dedicated broker account can be provisioned later through its administration path. Sharing the account does not share client IDs or disconnect the portal worker.

## Pinned release and local overlay

Native systemd deployment on the existing Ubuntu 24.04.5 LXC: four logical CPUs, 8 GiB RAM, 512 MiB swap, 64 GiB filesystem. Initial free disk was approximately 64 GiB. Existing Grafana has 8 GiB RAM/15 GiB free disk; Prometheus has 4 GiB RAM/16 GiB free disk and approximately 164 MiB TSDB use at inspection. Physical-host load and long-term growth are separate checks.

- Upstream [v4.17.0 release](https://github.com/Yeraze/meshmonitor/releases/tag/v4.17.0), LXC asset `meshmonitor-4.17.0-amd64.tar.gz`, 541,711,965 bytes.
- Verified release-API SHA-256: `697797ce1aab702eca1a070c878f5c801a82fbd5a2fc9efb6e203cc8282bd03a`.
- Application inspection asset `meshmonitor-v4.17.0.tar.gz`, SHA-256 `1a0705bd9466c874ae73d82f84fe7cd6aae3eb7f98f0e40a1bf6f2d96ed4c91b`.
- Bundled Node `v24.21.0`, installed separately as `/opt/meshmonitor-runtime/node`; packaged native SQLite dependencies load successfully.

Only `/opt/meshmonitor` and the Node executable were extracted from the verified template. The template OS, SSH configuration, root accounts and `/etc` were not unpacked over the existing host. `/opt/meshmonitor` is root-owned; unprivileged `meshmonitor.service` writes only `/data`, with private devices, strict filesystem protection, no capabilities and a 4 GiB memory ceiling. Service starts at boot and restarts on failure. Automatic release updates are not configured.

Upstream 4.17.0 hardcodes several automatic history cleanup paths. The tracked [policy overlay](../../deploy/meshmonitor/patch-release.py) adds an explicit bind-address option and `MESHLINK_RETAIN_HISTORY=true` guards at five cleanup seams: telemetry, TCP packet log, MQTT packet/violation log, coverage/cross-source history, and MeshCore position history. The active MQTT source's position history is telemetry. Distance/aircraft automatic deletion is not enabled. Explicit owner/admin deletions remain separate actions. This is a local build overlay, not an upstream release claim; review/reapply it before any upgrade. Version/seam checks fail rather than silently patching a different build. [Service and provisioning sources](../../deploy/meshmonitor/).

The source is a standalone `mqtt_bridge`, `mode=subscribe_only`, subscribed only to the project's encrypted channel subtree. No embedded broker, attached parent broker, physical radio connection or outbound publish path is enabled. The default TCP placeholder is disabled. MQTT packet monitoring is enabled. App logging is `warn`, with access logging disabled; logs and database remain private.

## Monitoring integration and retention

The existing Prometheus configuration is preserved with one appended scrape job and a separate token file. `promtool check config` validates all configuration and the existing 40 rules before applying it. A systemd drop-in `/etc/systemd/system/prometheus.service.d/30-snorr-retention.conf` preserves the original command and sets `--storage.tsdb.retention.time=30d`.

Prometheus retention is server-wide: this extends **all** existing series from the previous default 15 days to 30 days. No per-job retention setting exists in this setup. The 30-day duration is configured and read back; a full 30-day observation period has not elapsed. Disk growth remains to measure. The existing 21 scrape targets and three rule files remain; four pre-existing down targets remain down, with no new existing-target failure in the final check. The added MeshMonitor target is up, and its MQTT-connection metric equals 1.

Grafana retains its existing `prometheus` data source. New file provider `snorr-meshmonitor.yml` reads `/var/lib/grafana/dashboards/snorr-meshmonitor/dashboard.json`, under a separate **SNORR MeshLink** folder. All three original dashboard specifications compare equal before/after; one dashboard is added. Grafana 13 stores these in its `resource` table; an empty legacy `dashboard` table is not evidence that dashboards were lost. All ten dashboard expressions query successfully from the Grafana host. Native browser layout is a follow-up.

The dashboard shows scrape/MQTT state, active nodes, contact age, battery voltage, channel utilization, transmit airtime, last-reception SNR/RSSI when reported, and rolling message counts. Missing series stay absent. Private-channel data is visible only through the existing authenticated Grafana access policy. The token does not expose channel secrets.

## Measurements and interpretation limits

- Live encrypted packets are received, decrypted and stored. Final recovery checkpoint has four node rows (including the inferred gateway placeholder), 21 telemetry rows and six MQTT packet-log rows. All six logged outcomes are `ingested`; one gateway is represented. Observed telemetry includes two devices' voltage/airtime, one device's temperature/humidity, and GPS history. Counts will grow after this checkpoint.
- Four matching voltage/weather values compare equal against both the existing portal adapter's decoding of exact archived envelopes and persisted portal observations. No live data was changed for this comparison.
- The read-only metrics token exports two voltage series and utilization/airtime series. Environment temperature/humidity are stored in MeshMonitor but not exposed by this upstream metrics endpoint. Upstream protocol-count metrics currently query the TCP packet log, so the unpopulated MQTT protocol-count panel was omitted. Custom MeshLink exporter/health metrics are separate work.
- MeshMonitor's position-observed time and last-heard time are not the portal's GPS measurement age. Its position-history dedup uses a bounded `(source,sender,packet ID)` cache, unlike the portal's content-aware identity. Do not use these charts to certify the 15-minute GPS freshness requirement or complete reception history. Unknown/zero scalar and source/final-hop interpretations remain upstream semantics until separately verified.
- No historical import was performed. Fresh G002 delivery, two-gateway behavior, native desktop/mobile views, outage/replay behavior and measured storage growth remain [verification work](https://github.com/lfg-seth/snorr-meshlink/issues/23). Existing exact PocketBase archive, gateway receipts and silent infrastructure badges remain authoritative. Existing GPS API/worker are healthy after deployment.

## Backup, recovery and rollback

`meshmonitor-backup.timer` runs daily at **02:45 America/Los_Angeles**, with a persistent missed-run catch-up. [Backup helper](../../deploy/meshmonitor/backup.py) uses SQLite online backup plus integrity checking and archives the DB, private `/etc/meshmonitor` configuration/credentials, service and deployment scripts under `/var/backups/meshmonitor`. Keep 14 backup archives; this rotation never deletes application observations. No packet/history expiry is active. Backups currently share the LXC disk; [off-host recovery](https://github.com/lfg-seth/snorr-meshlink/issues/7) remains open.

Measured checks: all five real patched cleanup bodies return before database access; patched JavaScript syntax and installer shell syntax pass. An explicit service restart preserves all retained row IDs, users/permissions/channel keys/token and reconnects MQTT, with upstream-publish and local-republish counters both zero. A fresh backup extracts byte-identically, passes SQLite integrity, and boots an isolated app on loopback:3002 after disabling all sources **in that disposable copy only**. Node, telemetry, packet, user, grant, channel and token row counts match. No live data is replayed or replaced during verification.

Operational checks (SSH to MeshMonitor first):

```sh
systemctl status meshmonitor meshmonitor-backup.timer
python3 /root/meshmonitor-install/config/verify-host.py meshmonitor
systemctl start meshmonitor-backup
python3 /root/meshmonitor-install/config/verify-recovery.py
```

Prometheus pre-change configuration is root-private under `/root/meshmonitor-integration-<UTC>/prometheus.yml`; Grafana pre-change consistent DB is `/root/meshmonitor-integration/grafana-before.db`. Avoid restoring the entire shared Grafana DB for a dashboard-only rollback. Stop MeshMonitor if needed, remove only its provider/dashboard files (Grafana's `disableDeletion` deliberately retains the UI resource until explicitly removed), remove only the `snorr-meshmonitor` scrape/token and retention drop-in if rolling back that change, validate the Prometheus config and reload/restart affected services. Preserve other targets/dashboards and any later owner edits.

For a full MeshMonitor restore: stop its service; preserve current `/data` and `/etc/meshmonitor` privately; extract a verified selected archive into staging; inspect it and compare counts; restore its DB/config/service with original owner/modes, leaving live sources disabled until inspection succeeds; verify the exact pinned runtime/overlay, then start the service and verify MQTT/token access. Never copy a live SQLite main file without its WAL or an online snapshot. The original verified asset and staged application remain under `/root/meshmonitor-install` for exact-version recovery. No destructive live restore was performed.

Source references: [MQTT bridge modes](https://meshmonitor.org/features/mqtt-broker), [upstream LXC guide](https://meshmonitor.org/deployment/PROXMOX_LXC_GUIDE.html), [pinned metrics implementation](https://github.com/Yeraze/meshmonitor/blob/v4.17.0/src/server/routes/v1/metrics.ts), [Prometheus storage/retention](https://prometheus.io/docs/prometheus/latest/storage/).
