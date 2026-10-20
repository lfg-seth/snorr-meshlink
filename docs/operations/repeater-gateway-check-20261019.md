# Repeater gateway receipt check — 2026-10-19

## Portal archive confirmation after owner DNS repair

Owner fixes DNS; SSH access then succeeds. Read-only live database inspection at **19:19 Pacific** confirms **all five repeaters reach G001 and have normalized portal receipts** after reflashing. Actual `meshlink-worker.service` and API are active; the initial probe used nonexistent `meshlink-mqtt-worker` and its inactive result is not a service-failure finding.

| Node | Latest normalized G001 receipt, Pacific | Recent normalized receipt count since 18:35 |
| --- | --- | --- |
| R001 | 19:15:37 | 4 |
| R002 | 19:15:22 | 3 |
| R003 | 19:17:04 | 5 |
| R004 | 19:15:28 | 3 |
| R005 | 19:15:08 | 3 |

Latest raw receipts have matching topic/envelope gateway identities, `retained=false` and recent gateway radio-receipt clocks. Archive parsing since 18:35 finds R001 8, R002 5, R003 8, R004 7 and R005 6 raw G001 deliveries, including unsupported/rejected kinds; normalized counts are separate. No recent G002 copies occur in this range. R005's newest raw packet at 19:15:12 is rejected; it does not negate its earlier normalized receipts, and no rejection cause is established here.

Fresh normalized environment observations also establish post-flash temperature operation for **R003 24.769783°C (19:17:04), R004 27.470970°C (19:15:28), R005 26.064301°C (19:07:12)**. Their `measuredAt` remains empty: fresh arrival does not create a known measurement clock. No fresh temperature observation found for R001/R002 in the queried range. Calibration, sustained cadence, direct-versus-relayed path and both-gateway behavior remain unverified. Read-only query helper: ignored `private/bench/check-repeater-archive.py`.

## Earlier direct MQTT observation

Owner asks whether the reflashed R001–R005 are reaching a gateway, then changes desktop networks and requests retry. Read-only TLS MQTT subscription uses existing private worker credentials with a distinct client ID; no radio/configuration changes or broker publications.

Two observation windows: October 19 Pacific **19:14:39–19:15:35** and **19:16:18–19:17:13** (UTC October 20 02:14:39–02:15:35 and 02:16:18–02:17:13). Broker connection/subscription succeeds in both. Decode channel-encrypted envelopes privately; summarize only known repeater identities and non-location measurements. Seven matching deliveries are non-retained; topic/envelope gateway identities match **G001 `!9ea13cc0`**, and gateway `rx_time` is roughly 1–2 seconds before desktop receipt.

| Node | Latest observed Pacific receipt | Result |
| --- | --- | --- |
| R001 | None in these windows | Unconfirmed, not evidence of failure |
| R002 | None in these windows | Unconfirmed, not evidence of failure |
| R003 | 19:17:04 | Environment packet `2671727265`: **24.769783°C**; SNNS `3328318112` at 19:16:20 |
| R004 | 19:15:19 | SNNS `3628480489`; device telemetry `911223782` at 19:15:02, plus node/position application packets whose payloads are not published |
| R005 | 19:15:08 | SNNS `2501594642` |

This confirms RF-to-G001-to-MQTT delivery for R003/R004/R005 and live R003 temperature operation after its reflash. It does not prove direct rather than relayed reception, sensor calibration, both-gateway behavior or portal normalization. R003's telemetry `time=151` is not a valid wall-clock measurement timestamp; preserve it separately from fresh gateway/desktop receipt times. R004's device telemetry time is likewise 246. No sustained cadence, utilization or runtime conclusion.

No G002 copies observed. R001/R002 have configured 900-second telemetry and firmware-controlled neighbor cadence, so these short windows cannot establish offline state. First window has one decode error of unclassified source; completeness is not claimed. Full private summaries remain ignored at `private/bench/repeater-gateway-check-20261019-first.json` and `private/bench/repeater-gateway-check-20261019.json`.

Portal archive initially unavailable: recorded `meshlink.int.spp.lol` returns NXDOMAIN through system resolution and both configured local DNS servers after the network change. Existing alternate SSH host times out. Owner subsequently repairs DNS; successful archive checks above supersede this access limit. Agent changes no DNS/network settings.

Next: observe a full configured reporting cycle with all five powered, check R001/R002 fitted temperature sensing if expected, and separately verify G002. Preserve distinction between RF/MQTT delivery, normalized portal state and valid measurement clocks.
