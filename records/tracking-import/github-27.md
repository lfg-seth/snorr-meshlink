# GitHub issue #27: Reflash R002 for CLIENT bench operation with temperature telemetry only

Immutable import evidence dated **2026-10-21 (America/Los_Angeles)**, retrieved 2026-10-22T01:33:06Z. This snapshot preserves the GitHub record at migration; it is not an active task queue. Historical instructions and claims below describe their original context. Use the repository's current tracker for later status and authorization.

- Source: [Reflash R002 for CLIENT bench operation with temperature telemetry only](https://github.com/lfg-seth/snorr-meshlink/issues/27)
- GitHub state: open; state reason: not supplied.
- Tracking label at import: `status:verify`.
- Labels: `task`, `area:hardware`, `status:verify`, `area:firmware`.
- Assignees: none.
- Author: lfg-seth.
- Created (UTC): 2026-10-20T01:49:42Z.
- Updated (UTC): 2026-10-20T02:20:51Z.
- Closed (UTC): not closed.
- Milestone: none.
- Comments preserved: 3 of 3 reported by GitHub.

## Original issue body

<!-- BEGIN ORIGINAL ISSUE BODY -->
Owner connects R002 and authorizes same configuration as R001 on 2026-10-19: released neighbor-signal firmware, CLIENT, device/environment telemetry at 900 seconds, no INA219/power configuration.

Acceptance: identify R002, fresh complete private backup, verify pinned release and flash without reset/rebuild; preserve identity/keys/channel/radio profile; configure CLIENT, temperature telemetry and power disabled; verify independent reboot readback; request local temperature and record evidence/limits. Prior no-external-sensor record is superseded by this requested profile; actual sensor operation must be measured.

Claim: Codex Windows desktop session 2026-10-19. Only connected R002 scoped. R001 sensor follow-up #26 remains separate.
<!-- END ORIGINAL ISSUE BODY -->

## Original comments

### Comment 6281473377

- Source: [comment 6281473377](https://github.com/lfg-seth/snorr-meshlink/issues/27#issuecomment-6281473377)
- Author: lfg-seth.
- Created (UTC): 2026-10-20T01:52:38Z.
- Updated (UTC): 2026-10-20T01:52:38Z.

<!-- BEGIN ORIGINAL COMMENT 6281473377 -->
Reflash/configuration complete: R002 !b456f760, verified pinned 2.7.26.0b65f2e with neighbor-signal/SNNS firmware; CLIENT, device/environment 900s, power measurements/display disabled, battery INA address unconfigured, NeighborInfo enabled over LoRa. Fresh full private backup and independent exact identity/key/channel/profile checks pass through explicit reboot (role-dependent API sleep default accounted for).

Moving to Verify and releasing claim: local environment request plus 45s yielded no temperature/environment metrics. Confirm fitted sensor/wiring/detection and obtain a fresh reading. RF/MQTT/portal delivery, sustained cadence/utilization reduction, runtime and calibration unverified; other boards/live portal unchanged. Evidence: docs/operations/r002-client-bench.md and TEST-016 in records/field-results.md.
<!-- END ORIGINAL COMMENT 6281473377 -->

### Comment 6281479001

- Source: [comment 6281479001](https://github.com/lfg-seth/snorr-meshlink/issues/27#issuecomment-6281479001)
- Author: lfg-seth.
- Created (UTC): 2026-10-20T01:53:07Z.
- Updated (UTC): 2026-10-20T01:53:07Z.

<!-- BEGIN ORIGINAL COMMENT 6281479001 -->
Evidence published: https://github.com/lfg-seth/snorr-meshlink/commit/0e80e18 . Documentation local-link and whitespace checks pass; origin/main is synchronized. Firmware pin and unrelated untracked battery-box model preserved. Sensor verification remains outstanding.
<!-- END ORIGINAL COMMENT 6281479001 -->

### Comment 6281826272

- Source: [comment 6281826272](https://github.com/lfg-seth/snorr-meshlink/issues/27#issuecomment-6281826272)
- Author: lfg-seth.
- Created (UTC): 2026-10-20T02:20:51Z.
- Updated (UTC): 2026-10-20T02:20:51Z.

<!-- BEGIN ORIGINAL COMMENT 6281826272 -->
R002 confirmed reaching G001 and normalized portal after reflash: latest normalized receipt 2026-10-19 19:15:22 Pacific, matching fresh non-retained envelope/gateway receipt. Temperature still unverified; issue remains Verify.

Published evidence: https://github.com/lfg-seth/snorr-meshlink/commit/0669ede ; docs/operations/repeater-gateway-check-20261019.md / TEST-020. All five reach G001; no recent G002 copies. No DNS/radio/worker change performed by agent.
<!-- END ORIGINAL COMMENT 6281826272 -->
