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

## Connected-gateway follow-up and recovery

Later on October 20, the owner connects both gateways and the dedicated debug receiver. Identify **G001 / !9ea13cc0 / COM21**, **G002 / !849ad7a0 / COM22**, and the dedicated sniffer stream on **COM6**, reporting `2.7.26.f95a443`, 910.625 MHz / BW 250 kHz / SF11 / CR 4/5 / TX disabled. Both gateways independently report expected `2.7.26.9d2fd8f`, enabled Wi-Fi/MQTT/TLS/uplink, expected broker/root, disabled LoRa TX/downlink and credentials matching the last owner-supplied Wi-Fi. Exact profiles remain private.

Initial 12-second passive logs distinguish the gateways:

- G002 is publishing. First resumed production archive receipt is **19:44:44.367 Pacific** (`2026-10-21T02:44:44.367Z`). Its initial console uptime is approximately 57 seconds, consistent with a recent boot; prior power state is not established.
- G001 is receiving and processing mesh reports, but emits **`MQTT not connected, queue packet`** and **`MQTT queue is full, discard oldest`**. Its initial console uptime is approximately **85,723 seconds**, so absence of portal traffic did not mean the radio was powered off. These logs directly establish a failed gateway MQTT uplink and loss of older packets from its bounded queue. They do not establish the underlying Wi-Fi/session failure.

G001 restarts during the ordinary Meshtastic serial API inspection: later passive logs have uptime 46–86 seconds. The stock Python serial constructor opens with default USB control-line states; an incidental serial-open reset is a plausible trigger, not a confirmed reset reason. No reboot command, configuration write, firmware flash or broker change is issued. Do not describe this as spontaneous recovery or proof of a firmware fix. Subsequent API readback uses a serial subclass that sets DTR/RTS inactive **before** opening.

G001's first resumed production archive receipt is **19:47:00.592 Pacific** (`2026-10-21T02:47:00.592Z`). A subsequent 65-second passive G001 capture contains seven MQTT publish log entries and zero disconnected/full-queue messages. Final local connection-status responses confirm **Wi-Fi connected and MQTT connected on both gateways**. Independent local/module/channel byte comparisons match their saved inspection profiles exactly.

The original archive verification command now passes: **3,775** archive records, **two** new deliveries during the check, latest **200** envelopes validated, outcomes **195 normalized / five unsupported**, and **zero** pending queue entries. New B001 and B002 reports have receipts through **both** gateways. Authenticated live state has valid GPS measurement times **19:47:00** and **19:47:29 Pacific**, distinct from the newer receipt times. G001/G002 own reports and R001/R002/R003/R004 delivery also resume; no new R005 report is observed in this short checkpoint, and its cadence/readiness is not established.

The dedicated sniffer's **65.101-second** capture contains **12** reconstructed/decoded receptions, **six** duplicate receptions and no capture-gap events or session error. Observed sources are R001/R003/B001/B002. Peak trailing-window receive-airtime estimate is **16.77%**; this does not measure all RF activity or validate high-load completeness.

Private evidence: `private/bench/outage-20261020/` and `local-data/sniffer/20261020-194716-ab6b72ee/`. All interfaces close after checks. Current delivery is recovered; the original disconnection trigger, automatic reconnect reliability, sustained freshness and outage data loss remain unverified. Keep #40 in Verify for that bounded remaining diagnosis rather than claiming a permanent fix.
