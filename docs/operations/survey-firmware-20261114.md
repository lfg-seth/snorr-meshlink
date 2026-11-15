# Direct-hop survey firmware handoff, 2026-11-14

**Installed on three RAK4631s and the original GPS Heltec V4.** Both survey targets were built from `bcb22e037293df5531da391bb88d46b6969633b0` on `snorr/develop`. The project submodule pins that version. The dedicated targets leave the existing production target names available. [Prerelease and checksums](https://github.com/lfg-seth/firmware/releases/tag/snorr-direct-survey-2.7.26.bcb22e0-pre.1) · [Firmware source](https://github.com/lfg-seth/firmware/tree/bcb22e037293df5531da391bb88d46b6969633b0) · [USB, authenticated RF and CLI reference](survey-usb-v1.md).

## Numbered repeater handoff

The owner selected US LongFast, slot 35 for member-free survey testing. These three physical RAKs already had the survey application and had passed an explicit reboot. At handoff, each reported the expected image and matched its own saved owner, security keys, channels, local configuration and module configuration. The Heltec then sent an authenticated direct PING to each. Each RAK independently recorded receiving the request and transmitting the PONG that the Heltec matched.

| Current repeater label | Radio ID | USB port at handoff | Confirmed round trip |
| --- | --- | --- | ---: |
| R004 | `!49ac6d7f` | COM32 | 3,697 ms |
| R005 | `!a65601b3` | COM8 | 2,026 ms |
| R007 | `!b456f760` | COM9 | 2,069 ms |

These are individual exchanges at the bench. Private run evidence is in `private/bench/survey-rollout-20261114/pilot-1794722937458177100/` in the survey worktree. The tested Heltec image stores eight enrolled peers in total. G002 and these three RAKs account for four. R003 remains on its previously recorded RF hold.

## Artifacts

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `firmware-rak4631-survey-2.7.26.bcb22e0.uf2` | 1,530,368 | `581d36007d572252c5668ebaa79428649cd7c148f7ef39e51851bbb89381a9cb` |
| `firmware-rak4631-survey-2.7.26.bcb22e0-ota.zip` | 765,940 | `394d5e3a531e2b48b21ac4cc6f16d70a5da158a4c6a0443291e1e142e8080776` |
| `firmware-heltec-v4-survey-2.7.26.bcb22e0.bin` | 2,052,688 | `d182611030f638cc87f5fd23c659bd2fcfa16016bbe900ce17f05a948244ef4a` |
| `manifest.json` | 1,046 | `4b95e7a50a8b6517bfdc8dd9a800b89b5e67b612a07b033100e5b4db81be7d50` |
| `SHA256SUMS` | 417 | `766d86fc824ca5484de9b88705007ee8e5008361dd9aa26c67f6d11760badb4a` |

The binaries matched their PlatformIO metadata and the uploaded GitHub asset digests. RAK uses 111,196 bytes RAM and 764,940 bytes program flash. V4 uses 110,080 bytes RAM and 2,052,265 bytes program flash. The V4 BIN is application-only. The partition binary SHA-256 is `bd0f7954aca2ef7d925ee21aaa1f3dc8822d1d6ce5cbbd26a135e5886bfff6ce`. On installation, compare the saved flash partition table and active partition with the candidate before writing the V4. Use the RAK UF2 for guarded USB installation on the matching RAK4631.

## What the bench established

Each physical USB serial number, node ID, hardware model and original firmware was matched before making changes. Private originals contain the individual device identity and keys, complete config and all eight channel slots. All four started as CLIENT, US, LongFast, slot 35, 10 dBm with the same primary channel key. Readbacks verified `tx_enabled=false` on the four original images and preserved the individual keys, channels and intended profile. The V4 was staged for one-second GNSS updates with smart position, fixed position and Wi-Fi disabled.

| Port | Physical board and node ID | Previous build | Installed target and reboot readback |
| --- | --- | --- | --- |
| COM8 | RAK4631 `!a65601b3` | `2.7.26.4c96b9b` | `rak4631-survey` / `2.7.26.bcb22e0` |
| COM9 | RAK4631 `!b456f760` | `2.7.26.4c96b9b` | `rak4631-survey` / `2.7.26.bcb22e0` |
| COM32 | RAK4631 `!49ac6d7f` | `2.7.26.4c96b9b` | `rak4631-survey` / `2.7.26.bcb22e0` |
| COM5 | Original GPS Heltec V4 `!699c2ed8` | `2.7.26.6fea6aa` | `heltec-v4-survey` / `2.7.26.bcb22e0` |

Private worktree evidence is under `private/bench/20261114T213913Z/`. The `COM*.json` originals predate staging. The individually timestamped profile files capture the intended readbacks. The V4 recovery image is 16,777,216 bytes, SHA-256 `f2df51b7b777d04f1caa77018353117d3c999da33248ee8337c579e877217188`. The first continuous flash read stalled. Sixteen position-checked 1 MiB reads completed the backup. The original RAK recovery release is retained in the shared checkout at `private/bench/releases/weekend-rak-4c96b9b/`. Keep all four devices' private profiles separate when recovering.

The owner confirmed all four antennas or loads and explicitly approved overwriting the four identified boards. With the watcher stopped and the station lease held, the installer flashed one board at a time. Each UF2 matched its RAK bootloader identity. The V4 partition table matched its backup, and esptool independently verified all 2,052,688 application bytes at `0x10000`. The pre- and post-reboot checks matched the original identities, individual keys, eight channel slots and intended complete configurations.

Physical USB enrollment and both modem profile transitions succeeded on all four with transmit disabled. The client correctly rejected a bench start while TX was disabled. All four returned to the production profile before TX was enabled. The next boot read back one enrolled client and three enrolled responders. Their Meshtastic role was CLIENT throughout.

## Baseline, cadence and interlocks

During 205 idle seconds, other boards decoded ordinary telemetry and a private application broadcast from each RAK. The V4 delivered 199 USB position samples, including 185 distinct valid fixes. Median reported age among valid fixes was 586 ms and the maximum was 1,087 ms. Raw coordinates remain private.

| Production LongFast trial | Seconds | Successful / timed out | Round trips/min | Median RTT | Client / responder median channel utilization | Acceptance |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Fixed 2 s, COM8 only | 75 | 28 / 1 | 22.40 | 2,030 ms | 41% / 41% | Passed |
| Fixed 3 s, three targets | 80 | 11 / 10 | 8.24 | 2,031 ms | 25% / 40% | Passed |
| Fixed 5 s, three targets | 80 | 4 / 12 | 3.00 | 1,836 ms | 33% / 18.5% | Missing all-observer evidence for COM8 and COM9 |
| Adaptive 2 s minimum, three targets | 150 | 39 / 9 | 15.59 | 2,124 ms | 49% / 49% | Passed |

The measured request and response each occupied 70 bytes on air, including 47 application payload bytes. The median request TX-start to TX-done interval was 764 ms in all four trials, against 763 ms predicted. The short trials used a 4,500 ms response timeout and each ended with one cancelled in-flight attempt. Delayed replies reached the client up to 7,344 ms after enqueue. The long bench uses an 8,000 ms timeout, a 2,000 ms minimum and the production PHY. The short trial results include changes in reception and target mix as well as cadence.

In the single-target trial the three RAKs directly decoded 29, 29 and 10 requests respectively. Every observed request renewed quiet. Only COM8 enqueued a response. The three-target adaptive trial produced 44, 42 and 44 direct receipts respectively, all matched to renewals. All 39 successful round trips matched the independent signal measurements in both directions.

Survey start with an unavailable fresh fix returned an interlock error. With a temporary 500 ms maximum fix age, a real fix started survey mode, a subsequent stale interval paused it, and later heartbeat alone left it paused. The client was restored to a 2,000 ms maximum age. Withholding host heartbeats for ten seconds paused bench mode. A returning heartbeat left it paused until an explicit resume. COM9 retained identity, profile and enrollment through an explicit quiet-window restart. Quiet had 614,625 ms remaining before restart and 893,625 ms remaining at post-boot readback.

## Owner-stopped adaptive soak

The client ran in explicit bench mode on 2026-11-14 from approximately 18:05 to 18:55 Pacific. The owner requested stop at **3,013.484 of 7,200 seconds**. The host created the recorder's STOP file. The Heltec acknowledged the stop and emitted an idle snapshot. The recorder finalized the logs with reason `cancelled`, released all four handles and released the station lease. The watcher was stopped. The separate post-run quiet-expiry observation was not started.

The recorder counted 744 successes, 118 timeouts and one in-flight cancellation. That is **86.3% of 862 completed attempts**, or **14.81 confirmed round trips/minute**. All four observers stayed on one boot each and no firmware drop counter increased during this recording. There were no logged stream gaps. The transmitter reported 862 on-air PINGs and the responders reported 761 on-air PONGs. Client channel utilization was 43% median and 54% at the 95th percentile. At responders it was 43% and 55%. Across matched attempts, RTT was 2,086 ms median, 2,964 ms at the 95th percentile and 6,736 ms maximum.

| Target | Successful / timed out | Success share | Longest gap between successes | Median uplink / downlink RSSI | Successful exchanges corroborated by all four observers |
| --- | ---: | ---: | ---: | ---: | ---: |
| COM8 `!a65601b3` | 253 / 35 | 87.8% | 115.1 s | −54 / −35 dBm | 218 |
| COM9 `!b456f760` | 246 / 41 | 85.7% | 154.5 s | −51 / −31 dBm | 223 |
| COM32 `!49ac6d7f` | 245 / 42 | 85.4% | 107.5 s | −58 / −39 dBm | 221 |

Outcomes varied over time. Minutes 15–20 had 27 successes and 28 timeouts. Minutes 45–50 had 93 successes and four timeouts. All 744 successes had matching independent uplink and downlink RSSI/SNR observations, and 662 had complete four-observer corroboration. No captured survey transmission was forwarded or requested a routing ACK. Each of 761 recognized requests addressed to its receiving RAK generated exactly one responder TX. No nontarget replies or owned autonomous transmissions during observed quiet were found. The firmware suppression counters increased by 93 across the four boards.

**Timeout attribution** used the request and reply mesh IDs to join hardware TX starts with independent decoded RX events.

| Last available evidence for the 118 timed-out attempts | Count |
| --- | ---: |
| Client transmitted, selected RAK recorded no decoded request | 99 |
| RAK transmitted the reply, client recorded no decoded reply | 10 |
| Client decoded the reply but did not accept it as a successful match | 6 |
| Selected RAK decoded the request without a quiet renewal or reply | 2 |
| Client recorded no request TX start | 1 |

Five of the six unmatched decoded replies reached the client after the 8,000 ms timeout. One arrived at 7,439 ms. The available RF observations cannot distinguish interference, receiver availability or other physical causes for a missing decode.

**Freshness boundary.** The RAKs logged 2,335 direct decodes of client requests and 2,325 matching quiet renewals. Ten decodes across five distinct requests had no renewal. These five requests waited 5,717–7,051 ms between enqueue and physical TX. The firmware stamps each request at enqueue and checks a seven-second freshness window at reception. The pattern is consistent with that limit interacting with queue and on-air delays, but the current logs do not identify the exact reject branch. The receiving RAKs were already in quiet. The missing renewal is still an acceptance gap for the all-hearer requirement. The next firmware decision is how to align the timestamp, freshness guard and eight-second response window and expose a private rejection reason before repeating the duration gate.

**GNSS.** The window-positioned Heltec supplied 3,004 USB samples. Of those, 2,383 were valid and represented 2,375 distinct fix timestamps. Among valid samples median reported age was 599 ms and the maximum was 1,744 ms. The median interval between distinct fixes was 1,000 ms and the longest was 122 s. Explicit bench mode completed 150 round trips without a valid TX-location sample and retained null coordinates. Peers recorded no decoded V4 position broadcasts.

**Handoff.** All four boards have the published survey image and their verified CLIENT / US LongFast, slot 35, 10 dBm profiles with TX enabled. The final client snapshot was idle. The last RAK snapshots showed 883–900 seconds of quiet remaining. Natural expiry and resumption were not observed after the requested stop. The Heltec reported new boot IDs between some USB sessions. During the separate RAK restart check the generic Meshtastic SDK also printed protobuf decode warnings when handling the survey stream. The explicit restart and profile readback still succeeded. Outdoor moving coverage, relay-only geometry and an uninterrupted two-hour soak remain open.

## Independent fixed-diff review

Two independent read-only subagents inspected the fixed firmware diffs across the published baseline `5bd492399`, candidate `35f3f771a`, hardening `899b217f4` and evidence/replay fixes `cd646c9a4`. One also inspected the final rollback fix at `bcb22e037`. The reviews covered the early router interception, direct receive provenance, address and authorization checks, queue-to-transmit suppression, credential storage and physical USB commands, clockless replay, GPS/heartbeat interlocks and radio profile recovery.

- Routing consumes recognized survey traffic ahead of normal forwarding and reply handling. Requests and responses have independent mesh IDs and a 47-byte versioned payload. Recognition uses the cohort tag, and the selected RAK requires a separate tester tag to respond. Locally originated survey traffic suppresses routing ACKs, retries and MQTT.
- Fixed credential access, clockless replay across reboot, interference between senders' replay windows, and packet-pool pressure in the routing guard. The authorized sender has reserved capacity. Seven additional cohort senders fit the bounded replay cache. Clockless reboot recovery can delay a fresh request up to 60 seconds. Reboot during quiet conservatively restarts the 900-second quiet period.
- Fixed queued autonomous reports, stale GPS at transmit time and pending attempts after heartbeat loss. A failed experimental preset rollback emits `radio_profile_unknown` and inhibits survey TX until successful profile reapplication. Existing lower-level SX126x standby and receive-start paths can still assert on a hardware error. Physical driver fault recovery remains unverified.

The native controller suite compiled both production survey roles with fake hardware boundaries under ASan and UBSan. Both passed directness/authorization, renewal and expiry, queue pressure, replay, timing, GPS, host-loss and result-correlation cases relevant to their role. Windows and Linux adapter tests use a framed serial peer. They cover partial frames, identity checks, command ACK/idempotence across reconnect, directional metrics, null fixes and evidence summaries. These checks do not measure propagation or receiver performance. [Native suite at the pin](https://github.com/lfg-seth/firmware/tree/bcb22e037293df5531da391bb88d46b6969633b0/test/test_direct_survey) · [Host tests](../../scripts/survey/test_adapter.py).

The host review of fixed project diff `7ad7494..4415be7` identified stalled-session, aggregate-metric, quiet-classification and Linux port ownership gaps. The recorder now verifies continued results in the same run, reports each target’s longest gap between successes, requires matching independent evidence per observed target, and checks peer decodes of transmissions during quiet. Linux PTY contention exercises the exclusive open. The GUI bridge and serial adapter also passed a synthetic end-to-end start, duplicate ACK and stop check.

## Evidence and remaining field work

The private worktree run directory `private/bench/20261114T213913Z/soak-2h-adaptive-production/` contains the four board logs and final `summary.json` (SHA-256 `dcb71f70fe16ee980353c72707a6b16e13c78c908c27d5caace2823db84fa823`). Sibling directories contain the baseline, interlock, fixed-rate, adaptive and restart evidence. The [four-observer CLI](survey-usb-v1.md#cancellable-cli) writes append-only board evidence and a summary with matching packet IDs. A live four-board collocated survey can establish direct receptions and detect unexpected onward transmissions. A forced relay-only layout, moving outdoor GNSS accuracy, external power removal and physical driver fault recovery remain separate field checks.
