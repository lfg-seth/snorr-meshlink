# Direct-hop survey firmware handoff, 2026-11-14

**Build and publication passed. Installation and RF acceptance are open.** Both survey targets were built from `bcb22e037293df5531da391bb88d46b6969633b0` on `snorr/develop`. The project submodule pins that version. The dedicated targets leave the existing production target names available. [Prerelease and checksums](https://github.com/lfg-seth/firmware/releases/tag/snorr-direct-survey-2.7.26.bcb22e0-pre.1) · [Firmware source](https://github.com/lfg-seth/firmware/tree/bcb22e037293df5531da391bb88d46b6969633b0) · [USB, authenticated RF and CLI reference](survey-usb-v1.md).

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

| Station port | Matched identity | Last installed firmware | Last radio readback |
| --- | --- | --- | --- |
| COM8 | RAK4631 `!a65601b3` | `2.7.26.4c96b9b` | CLIENT, TX disabled |
| COM9 | RAK4631 `!b456f760` | `2.7.26.4c96b9b` | CLIENT, TX disabled |
| COM32 | RAK4631 `!49ac6d7f` | `2.7.26.4c96b9b` | CLIENT, TX disabled |
| COM5 | Original GPS Heltec V4 `!699c2ed8` | `2.7.26.6fea6aa` | CLIENT, TX disabled |

Private worktree evidence is under `private/bench/20261114T213913Z/`. The `COM*.json` originals predate staging. The individually timestamped profile files capture the intended readbacks. The V4 recovery image is 16,777,216 bytes, SHA-256 `f2df51b7b777d04f1caa77018353117d3c999da33248ee8337c579e877217188`. The first continuous flash read stalled. Sixteen position-checked 1 MiB reads completed the backup. The original RAK recovery release is retained in the shared checkout at `private/bench/releases/weekend-rak-4c96b9b/`. Keep all four devices' private profiles separate when recovering.

The station watcher was stopped with no busy port. The staging process released its lease and closed its serial handles. Automatic approval review rejected the four-board installation before execution because overwriting physical boards changes persistent operational state. **Zero boards received survey firmware. Soak duration was 0 of 7,200 seconds.** There are no hardware measurements of delivery rate, channel utilization, packet airtime, quiet suppression, signal metrics or GPS freshness for this release.

## Independent fixed-diff review

Two independent read-only subagents inspected the fixed firmware diffs across the published baseline `5bd492399`, candidate `35f3f771a`, hardening `899b217f4` and evidence/replay fixes `cd646c9a4`. One also inspected the final rollback fix at `bcb22e037`. The reviews covered the early router interception, direct receive provenance, address and authorization checks, queue-to-transmit suppression, credential storage and physical USB commands, clockless replay, GPS/heartbeat interlocks and radio profile recovery.

- Routing consumes recognized survey traffic ahead of normal forwarding and reply handling. Requests and responses have independent mesh IDs and a 47-byte versioned payload. Recognition uses the cohort tag, and the selected RAK requires a separate tester tag to respond. Locally originated survey traffic suppresses routing ACKs, retries and MQTT.
- Fixed credential access, clockless replay across reboot, interference between senders' replay windows, and packet-pool pressure in the routing guard. The authorized sender has reserved capacity. Seven additional cohort senders fit the bounded replay cache. Clockless reboot recovery can delay a fresh request up to 60 seconds. Reboot during quiet conservatively restarts the 900-second quiet period.
- Fixed queued autonomous reports, stale GPS at transmit time and pending attempts after heartbeat loss. A failed experimental preset rollback emits `radio_profile_unknown` and inhibits survey TX until successful profile reapplication. Existing lower-level SX126x standby and receive-start paths can still assert on a hardware error. Physical driver fault recovery remains unverified.

The native controller suite compiled both production survey roles with fake hardware boundaries under ASan and UBSan. Both passed directness/authorization, renewal and expiry, queue pressure, replay, timing, GPS, host-loss and result-correlation cases relevant to their role. Windows and Linux adapter tests use a framed serial peer. They cover partial frames, identity checks, command ACK/idempotence across reconnect, directional metrics, null fixes and evidence summaries. These checks do not measure propagation or receiver performance. [Native suite at the pin](https://github.com/lfg-seth/firmware/tree/bcb22e037293df5531da391bb88d46b6969633b0/test/test_direct_survey) · [Host tests](../../scripts/survey/test_adapter.py).

## Resume on the station

1. Obtain explicit four-board install approval following the execution review. Recheck the watcher, exclusive station lease, current USB identities, retained profiles and release digests. Leave TX disabled during installation.
2. Install one board at a time. Read back model, target/build, complete private profile and keys after an explicit reboot. Enroll the actual V4 public key on each RAK, and the three RAK public keys on the V4, using a separately generated private cohort key. Confirm persistence. Verify live USB hello, settings and stop on each applicable role.
3. Confirm suitable 915 MHz antennas or RF loads are connected before enabling transmit. Verify original production PHY settings and collect baseline traffic. Exercise target and nontarget quiet, expiry/recovery, authenticated selected-only replies, independent packet observations, missing/stale GPS and heartbeat loss/explicit resume. Compare fixed and adaptive polling at multiple intervals using actual TX/RX timings.
4. Run the [cancellable four-device CLI](survey-usb-v1.md#cancellable-cli) for 7,200 seconds and inspect its per-target and observer evidence. An indoor missing fix is permitted in explicit bench mode. Outdoor fresh fixes, moving vehicle data, a forced relay-only geometry and physical power cycles require their own evidence. Add measured results and close the station lease at handoff.
