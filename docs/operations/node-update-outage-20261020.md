# Missing production node updates — 2026-10-20

Owner-requested diagnosis: [Diagnose missing production node updates](https://github.com/lfg-seth/snorr-meshlink/issues/40). Read-only observations around 19:37–19:43 Pacific on October 20. No service, broker, radio or configuration changes.

## Supported finding

Both gateway streams stopped delivering to **both independent receivers** at approximately **20:19:33 Pacific on October 19** (`2026-10-20T03:19:33Z`). The first failing observed boundary is upstream of portal ingestion. Gateway power, Wi-Fi, MQTT connection and publishing remain to inspect; the evidence does not distinguish those causes or prove a hardware failure.

The outage predates the October 20 demo/minimap application deployment. Production source is `5d07d61d916290ea81d5ed98bfdadc6127f407eb`; no application rollback is supported by these observations.

## Reproduction and boundary checks

Run on production:

```sh
python3 /opt/meshlink/deploy/portal/verify-mqtt-archive.py --wait 15
```

Observed failure: `RuntimeError: No new MQTT archive receipts during verification window.` This is a fresh-delivery check, not proof of the outage's physical cause or a sustained reporting acceptance threshold.

Ranked hypotheses were worker subscription failure, queued/API ingestion failure, and gateways no longer publishing. Subsequent checks found:

- API, worker, Nginx and Cloudflare services active. Worker running since 17:37:02 Pacific October 20, zero systemd restarts. Its latest half-hour of logs repeatedly reports `MQTT subscribed: True`, with queued/unsupported/rejected/saved counters all zero for this process.
- Production archive has **3,746** deliveries. G001's latest arrival is `2026-10-20T03:19:33.625Z`; G002's is `2026-10-20T03:19:33.631Z`. Last normalized device contacts also fall in the preceding few minutes. Durable queue contains **zero** entries; database `quick_check` returns `ok`; filesystem has approximately **61 GiB** available.
- A separate temporary read-only subscriber, using existing private production credentials and a unique client ID, passes normal hostname/certificate-validating TLS, MQTT authentication and a granted QoS-1 subscription to the configured project root. It receives **zero** messages in 22 seconds after subscription. It disconnects cleanly; it neither publishes nor replaces the production client.
- Authenticated live state reports `simulation: false`, all **nine** devices, and `feedOnline: true`, while their last-contact timestamps remain old. This feed indicator describes worker/broker connectivity; it does not establish fresh node reports.
- Separate MeshMonitor service is active. Its **1,127** MQTT packet-log entries end at timestamp **1792466373631** (`2026-10-20T03:19:33.631Z`). Its G001 stream ends at `.626Z` and G002 at `.631Z`, independently matching the portal cutoff to milliseconds. This argues against a portal-specific ingestion or display fault.
- Broker's Mosquitto service is active. An unprivileged socket snapshot shows two established private MQTT connections, but does not identify their MQTT clients. Do not infer gateway connection identities from that snapshot.

## Limits and next action

The broker SSH account cannot read the Mosquitto log and passwordless sudo is unavailable; root SSH authentication is unavailable. No password was requested or copied. Windows currently enumerates only COM1, so neither gateway is locally available for direct readback. No power, Wi-Fi or gateway-session diagnosis can be established from this access.

Confirm both gateways' power and Wi-Fi, then inspect gateway MQTT status or obtain a broker-admin connection-log summary around the cutoff and current connections for G001/G002. Preserve existing settings and keys. After correcting the actual cause, repeat the archive check and independently verify new per-gateway normalized receipts and GPS measurement ages. No recovery or fix is claimed in this session.

Secrets, packet bodies, coordinates and raw tracks were not included in the public evidence. The startup shell emits a missing Node-version warning, but the Python services and diagnostic commands run; that warning is not evidence of the delivery cause.
