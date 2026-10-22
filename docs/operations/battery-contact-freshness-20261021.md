# R002/R004 contact and battery freshness

Read-only diagnosis, 2026-10-21 Pacific. Tracking: [Diagnose R002/R004 recent-heard status with stale battery telemetry #53](https://github.com/lfg-seth/snorr-meshlink/issues/53). Production application: `fa035509dfc2fd1492c8ae01618d99269c9a4f92`.

Both nodes are actually delivering source packets through G002. Their old displayed battery readings are a separate telemetry-selection problem from [cached neighbor hearing freshness #47](https://github.com/lfg-seth/snorr-meshlink/issues/47).

## Measurements

Authenticated state and read-only SQLite observations at approximately **15:09 Pacific** reproduce the discrepancy:

| Node | Displayed battery / measurement time | Newest battery packet received | New packet voltage | Recent contact |
| --- | --- | --- | --- | --- |
| R002 | 4.193 V / 09:16:17 Pacific | 14:56:52.844 Pacific | 4.058 V | 15:09:18.390 Pacific |
| R004 | 4.090 V / 13:16:20 Pacific | 14:53:51.101 Pacific | 4.195 V | 15:04:09.381 Pacific |

The owner's roughly five-hour metric age is the reported symptom. At inspection, R002's selected measurement is nearly six hours old; R004's is nearly two hours old. These are the actual inspected values, not confirmation of identical five-hour ages.

The last-contact receipts are newly accepted `neighbors:r002:ec2c2099:...` and `neighbors:r004:33937b09:...` packets, sent **by those repeaters**, rather than another node mentioning them in its cached table. Decoded envelopes have `via_mqtt=false`, non-retained/non-duplicate receipt flags, unchanged hop start/limit of 3/3, relay bytes matching each source, and G002 RF metadata: R002 **−42 dBm / 6.5 dB**, R004 **−44 dBm / 6.0 dB**. Gateway packet clocks are roughly one to two seconds before portal receipt. This supports recent direct RF reception of their own reports; it does not establish fresh hearing for every neighbor listed inside them.

Both nodes also deliver distinct battery packets approximately every fifteen minutes. Six consecutive R002 reports from 13:41 through 14:56 Pacific have increasing telemetry times/uptimes **3668, 4568, 5469, 6369, 7270, 8171 seconds**, with changing voltages. Six R004 battery reports from 13:38 through 14:53 have **66, 966, 1866, 2767, 3667, 4568 seconds**. Their telemetry clocks equal uptime, not Unix epoch time. The inspected packets have different IDs, varying RF readings and contemporaneous gateway clocks; this is evidence against an old retained packet explaining the mismatch. Absolute source measurement time remains unknown.

Read-only serial identification finds R002 on COM9, USB serial `BADB1E79E9739FC4`, node `!b456f760`, firmware **2.7.26.0b65f2e**, CLIENT. Device telemetry is enabled at **900 seconds**; environment configuration remains enabled at 900 seconds and neighbor reporting remains enabled over LoRa. Serial logs show an unknown wall clock (`??:??:??`). No saved configuration, time synchronization, forced radio transmission, reboot or flash command is issued. Serial is closed after inspection. R004 is not connected or changed; its diagnostic image/state remains preserved.

## Cause

The [MQTT adapter](../../backend/mqtt_adapter.py) correctly treats telemetry times below 2020 as unknown measurement clocks. New observations are saved with empty `measuredAt` and `timestampQuality=unknown`.

The [ingestion selector](../../backend/pb_hooks/ingest.js) permits an unknown-time reading to replace another unknown-time reading by receipt order, but **never permits it to replace an existing timestamped reading**. Both nodes have an earlier timestamped battery reading. Consequently, new voltages accumulate in observations without replacing the selected reading. The [state endpoint](../../backend/pb_hooks/meshlink.js) exposes that old selected voltage and its measurement time, while `lastContactAt` advances from accepted source packets. Battery history also requires a measurement clock and therefore excludes the newer unknown-time samples.

This is a confirmed selection limitation, not evidence that the radios stopped reporting battery telemetry. It affects other telemetry metrics through the same selection rule. Contact is a receipt clock and must remain separate from GPS or telemetry measurement freshness. Duplicate receipts can also advance contact under the current implementation, so contact alone is not a general guarantee against replay; the independent packet evidence above is what supports actual reception here.

## Reproduction and next action

A private read-only probe compares authenticated `infrastructure[].battery` against the most recently received positive battery observation for each node. Run through SSH with `Get-Content private/bench/recent-heard-probe.py -Raw | ssh root@meshlink.int.spp.lol python3 -`, it reports:

```text
REPRODUCED: r002 display battery differs from latest received battery
REPRODUCED: r004 display battery differs from latest received battery
```

Independent archive decoding confirms the telemetry contents and RF metadata. Production decoder/ingestion files match local source after newline normalization. Credentials, full payloads, raw logs, configuration and locations remain private. An initial broad observation-row probe was rejected by automatic approval review; the successful replacement selects only timing, packet identity and battery fields and decodes privately on the host.

Diagnosis is complete; no application fix or deployment is claimed. Corrective work should retain separately the latest received telemetry and latest trustworthy measured telemetry, expose unknown measurement time explicitly, and avoid presenting receipt as measurement freshness. Verify known-to-unknown clock transitions, reboot, delayed/out-of-order delivery, duplicate receipts and later clock recovery at the real ingestion/state seam. Determine how RAKs regain a valid clock without requiring a phone as a separate firmware/operational check; do not mask the selection issue by simply setting R002's clock once.

## Receipt fallback correction

Owner subsequently authorizes backend/portal implementation with a simpler temporary policy: use valid source calendar time when available, otherwise receipt time for the displayed measurement time and age. Keep absent/invalid measurement clocks null/empty in storage and retain timestamp quality; omit the measurement-time-unknown message in received telemetry views. Owner explicitly declines uptime ordering. This supersedes the earlier proposed presentation above.

The shared backend telemetry selector uses `measuredAt || receivedAt` for each metric. A new report without calendar time can replace an older timestamped reading. A late report with known old calendar time cannot replace a newer effective-time reading. Duplicate gateway deliveries return before selection, retaining the first unique observation's receipt time. Invalid/future source clocks retain their quality and use receipt fallback. GPS selection/age and neighbor hearing clocks remain unchanged.

Infrastructure state preserves actual nullable `readingTimes` and adds `readingReceivedTimes`. `reportedAt` summarizes effective telemetry times. Battery history and snapshot samples merge known-time and receipt-time observations before applying bounds, retaining actual `measuredAt`, `receivedAt` and quality in the API. Cards, infrastructure detail, member battery, power readings, charge freshness and supported telemetry warnings use the same fallback rule. A report about another metric or a neighbor does not refresh battery age. The small chart title correction makes exact-reading tooltips render correctly with React.

No schema or firmware change is required. Existing selected readings advance on the next unique newer telemetry packet after release; historical samples without clocks become eligible immediately. No data rewrite or raw-archive replay is performed by this code. Without trustworthy source time, a delayed unique packet can appear newest by receipt, and its displayed age can understate measurement age; the owner accepts receipt time as a temporary approximation. Uptime and boot inference are not used.

Verification: the real PocketBase integration regression fails before the correction (`4.19 != 4.05`) and passes after it. Tests cover clock loss/recovery, delayed known/unknown reports, duplicate delivery, invalid/future clocks, honest stored clocks, member GPS independence, health recovery and mixed-clock history bounds. Real React component regressions fail before the portal change and pass after it, checking metric-specific fallback, stale valid measurements and stale fallback readings. All 49 portal tests, TypeScript and production build pass on desktop Node 25.6.0. Full Windows backend checks hit connection resets in authorization tests and absent timezone data; final Linux CI verification remains pending at this checkpoint. An attempted isolated LXC source transfer was rejected by automatic approval review; no transfer/deployment occurred, and validation uses the authorized GitHub CI path instead.

Implementation is prepared separately from draft neighbor PR #50. Production remains `fa03550`; device state, production databases and services are unchanged. Release must apply backend and portal together and verify new unique R002/R004 receipts and native presentation through the normal backup/recovery procedure.
