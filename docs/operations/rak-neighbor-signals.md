# RAK passive neighbor signal firmware

Portal follow-up (2026-10-16): [application `bed40dd`](radio-report-ingestion.md) now decodes these reports, recovers the newly supported archive data and displays directional signals/hearing ages/counts. Fresh R005/G001 normalization and isolated backup recovery pass; G002 and field/calibration limits remain. The original implementation/rollout history below is retained.

2026-10-16. Owner brings the previously parked richer-neighbor-report proposal forward and requests updating the existing RAK branch if absent. Fetch confirms `snorr/rak-survey` was still at `cc5907b1f`, with only its targeted AHT compatibility change beyond pinned Meshtastic `2.7.26.54e0d8d`.

## Source and behavior

For flashing, download [prerelease `snorr-rak4631-2.7.26.0b65f2e-pre.1`](https://github.com/lfg-seth/firmware/releases/tag/snorr-rak4631-2.7.26.0b65f2e-pre.1), not a new local build. Run `python scripts/bench/download-rak-release.py` from the project root to download/check the four assets and cache them privately. [Complete flashing handoff](board-flashing-handoff.md).

Firmware commit [`0b65f2e84`](https://github.com/lfg-seth/firmware/commit/0b65f2e84), branch `snorr/rak-survey`, adds a separate passive collector compiled into the `rak4631` target. The AHT fix remains. [Full implementation, byte contract and reproducible tests](../../firmware/SNORR_NEIGHBORS.md).

- Store up to 32 direct neighbors, configurable at build time, with full node ID, latest RSSI/SNR, monotonic hearing age and accepted observation count. Accept zero dB SNR; reject self/zero senders, MQTT origin, relayed/unknown hops, other channels and invalid signal values. Collector sees decoded primary-channel packets that survive normal duplicate filtering; it does not count every RF reception.
- Expire after 30 minutes without hearing; evict the least recently heard when full. Export eight rows per bounded 152-byte companion payload. Larger tables rotate, with subset and capacity-eviction flags. Missing rows never delete links or imply failure.
- Keep standard NeighborInfo port/schema/cadence and GPS unchanged. Extra fields use the project-local `SNNS` v1 payload on shared private port 256. Hearing age is measured at encoding; receipt time does not establish hearing time or remove transport delay.
- Existing NeighborInfo enable/transmit settings gate activation; firmware source does not alter saved configuration. Local mode uses a minimum 60 seconds plus jitter. Radio mode uses a minimum five minutes plus jitter, BACKGROUND priority, no requested ACK/reply, private-channel/transmit/role checks and existing airtime admission. No active probes.

The five-minute schedule is a conservative **bench starting setting**, not a measured safe operating cadence or GPS-freshness guarantee. Large-table full rotation takes multiple report intervals. Standard NeighborInfo's four-hour minimum remains intact; custom settings do not silently bypass it.

## Verification

- Build with the existing Windows PlatformIO 6.1.19 / Nordic nRF52 10.11.0 toolchain and pinned dependencies described in [R003's AHT build](r003-aht-build.md). No protobuf regeneration or dependency revision change.
- Portable C++17 collector checks pass under WSL GCC with `-Wall -Wextra -Werror` and address/undefined-behavior sanitizers, at capacities 32 and 10. Cover signal wire values/presence, counts, packet bounds/rotation, least-recently-heard eviction and monotonic expiry across rollover.
- A second sanitizer-backed harness compiles the **actual module implementation** against mocked services/settings. It passes primary-channel filtering, enable/default-channel/transmit/CLIENT_MUTE/both-airtime gates, local-only destination, background/no-ACK/no-response behavior, mode-change cooldown, timer-rollover cooldown and silent expiry.
- `trunk fmt` is unavailable on this Windows host. New C++ files pass the repository's exact clang-format 16.0.3 configuration (`.trunk/configs/.clang-format`), with whitespace checks. No full upstream native/MCP test-suite result claimed. The initial target build caught an unqualified packet-release API call, corrected before the source commit.

The exact committed source builds successfully as **2.7.26.0b65f2e** in 123.48 seconds. Flash: **759,256/815,104 bytes (93.1%)**; static RAM: **105,252/248,832 bytes (42.3%)**. The collector also allocates its bounded table at runtime; these static totals are not peak heap/stack measurements. Existing upstream sensor/library warnings remain. No warnings are repaired outside this feature.

Artifacts, full log and `checksums.json` are retained under ignored `private/bench/rak-neighbors-0b65f2e/`:

| Artifact | Bytes | SHA256 |
| --- | --- | --- |
| `firmware-rak4631-2.7.26.0b65f2e.uf2` | 1,518,592 | `59fff11dad4b8c83bfe1fd1b8a13438bf0147dd734db6e2821585b9710791f47` |
| `firmware-rak4631-2.7.26.0b65f2e.zip` | 760,213 | `2658def06a179c49ea77e872f7815a7794d8ca54768d0b9208e964c49842867f` |

Owner explicitly authorizes publication to their `lfg-seth/firmware` fork after an initial automatic-review rejection. Push succeeds on `snorr/rak-survey`, and the SNORR MeshLink submodule pins the published source. No keys, profiles or raw tracks are committed. No history rewritten; temporary alternative patch packaging was removed before publication.

## Published cached prerelease — 2026-10-16

The two binary files above are now published unchanged with `build-manifest.json` and `SHA256SUMS`. The binary source remains **0b65f2e8444ea2dd3566f61ba2614d6eb33d3fd2**. Release tag/tooling commit **8fe47325e38b82c8b2358293484ff845320d1be6** adds only workflow guards, the manifest, verification tests/tooling and release documentation; no firmware/build input changed and no rebuild was performed. This project's submodule now pins that release-tooling commit. The prerelease is not a stable/latest release or a claim of hardware verification.

Fresh public download, exact size/SHA256 comparison, manifest/checksum comparison and repeat-run cache reuse all pass. Six integrity regressions cover valid files, same-length corruption, missing/unexpected assets and altered manifest/checksum files. YAML policy checks verify repository guards and the fork job's read-only permissions. Black 26.5.1 formats the new Python scripts; Trunk remains unavailable. No firmware/hardware tests are rerun for these release-only changes.

[GitHub release workflow run 38994730691](https://github.com/lfg-seth/firmware/actions/runs/38994730691) succeeds: `verify-snorr-rak` passes, and all six upstream Docker/PPA/OBS/COPR/website/version-bump jobs are skipped. Fork prereleases perform read-only asset verification and no firmware rebuild, upstream publishing or inherited-secret work.

## Rollout boundary and next step

Subsequent R002 update: [sensor-free R002](r002-release-update.md) also runs the released build with preserved profile/keys, neighbor transmission enabled through reboot and a fresh 40-byte SNNS report through G001/MQTT/archive. Portal battery telemetry works; normalized custom-neighbor decoding and fresh G002 delivery remain unverified.

2026-10-16 follow-up: [R004](r004-preparation.md) now runs this released build with neighbor transmission enabled/read back through reboot. A fresh 40-byte SNNS v1 report reaches G001/MQTT and is archived; normalized portal decoding and fresh G002 delivery remain unverified. R003's AHT build and R001/R002's stock builds are unchanged. The source-implementation session itself did not flash hardware.

The current portal worker archives unsupported MQTT payloads but does not decode `SNNS`; live neighbor rows do not become available just by building this source. Before rollout, separately implement/test ingestion against the byte contract, preserve gateway receipt provenance and reject malformed/version/provenance mismatches. Then identity-check and snapshot a bench RAK, flash with owner authorization, explicitly enable/read back reporting and verify both stock gateway paths. Private-port forwarding and broker delivery depend on normal configuration; `CORE_PORTNUMS_ONLY` rejects this traffic.

Measure receipt delay/gaps, correct direct identities, expiry/capacity behavior, GPS freshness under diagnostic traffic, channel use and battery runtime. Report omissions, counts or signal values cannot establish link reliability, an entire route, placement suitability or field readiness.

Primary-source baseline: [official NeighborInfo configuration](https://meshtastic.org/docs/configuration/module/neighbor-info/), pinned local receive/filter/MQTT implementations, and [the original research](../research/node-neighbor-telemetry.md). This firmware work implements the owner-authorized first passive phase; survey ping/pong and other parked wishlist items remain deferred.
