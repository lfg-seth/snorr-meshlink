# GitHub issue #26: Reflash R001 for CLIENT bench operation with temperature telemetry only

Immutable import evidence dated **2026-10-21 (America/Los_Angeles)**, retrieved 2026-10-22T01:33:06Z. This snapshot preserves the GitHub record at migration; it is not an active task queue. Historical instructions and claims below describe their original context. Use the repository's current tracker for later status and authorization.

- Source: [Reflash R001 for CLIENT bench operation with temperature telemetry only](https://github.com/lfg-seth/snorr-meshlink/issues/26)
- GitHub state: open; state reason: not supplied.
- Tracking label at import: `status:verify`.
- Labels: `task`, `area:hardware`, `status:verify`, `area:firmware`.
- Assignees: none.
- Author: lfg-seth.
- Created (UTC): 2026-10-20T01:42:05Z.
- Updated (UTC): 2026-10-20T02:20:49Z.
- Closed (UTC): not closed.
- Milestone: none.
- Comments preserved: 3 of 3 reported by GitHub.

## Original issue body

<!-- BEGIN ORIGINAL ISSUE BODY -->
Owner authorized R001 flash on 2026-10-19 and requests repeaters use CLIENT for bench testing, temperature sensors only, no INA219 configuration. This issue scopes the connected R001.

Acceptance: identify R001 and privately back up complete profile/keys; verify and flash pinned RAK4631 release without reset/rebuild; preserve identity/channel/radio profile; configure CLIENT, environment telemetry and disabled power telemetry; independently verify reboot persistence; record measured sensor evidence and limits.

Claim: Codex Windows desktop session, 2026-10-19. Related utilization investigation #8 remains separate.
<!-- END ORIGINAL ISSUE BODY -->

## Original comments

### Comment 6281422203

- Source: [comment 6281422203](https://github.com/lfg-seth/snorr-meshlink/issues/26#issuecomment-6281422203)
- Author: lfg-seth.
- Created (UTC): 2026-10-20T01:48:25Z.
- Updated (UTC): 2026-10-20T01:48:25Z.

<!-- BEGIN ORIGINAL COMMENT 6281422203 -->
R001 flash/configuration complete: verified UF2 release 2.7.26.0b65f2e, CLIENT, device/environment 900s, power disabled, NeighborInfo enabled. Fresh private backup and independent identity/key/channel/profile comparison pass through explicit reboot. CLIENT sleep readback 300s is an API role-default override.

Verify / session claim released: local environment request plus 45s observation yielded no temperature; cached device metrics excluded. Next: confirm fitted sensor/wiring/detection and obtain fresh temperature. RF/MQTT/portal delivery and utilization reduction remain unverified. Other repeaters unchanged. Durable evidence: docs/operations/r001-client-bench.md and TEST-015 in records/field-results.md.
<!-- END ORIGINAL COMMENT 6281422203 -->

### Comment 6281423768

- Source: [comment 6281423768](https://github.com/lfg-seth/snorr-meshlink/issues/26#issuecomment-6281423768)
- Author: lfg-seth.
- Created (UTC): 2026-10-20T01:48:33Z.
- Updated (UTC): 2026-10-20T01:48:33Z.

<!-- BEGIN ORIGINAL COMMENT 6281423768 -->
Published sanitized hardware evidence and handoff in commit https://github.com/lfg-seth/snorr-meshlink/commit/b3fa109 . Documentation link and whitespace checks pass. Only the pre-existing unrelated battery-box model remains untracked; firmware pin unchanged. Native GitHub CLI Project reconciliation remains pending the authenticated management host.
<!-- END ORIGINAL COMMENT 6281423768 -->

### Comment 6281825744

- Source: [comment 6281825744](https://github.com/lfg-seth/snorr-meshlink/issues/26#issuecomment-6281825744)
- Author: lfg-seth.
- Created (UTC): 2026-10-20T02:20:49Z.
- Updated (UTC): 2026-10-20T02:20:49Z.

<!-- BEGIN ORIGINAL COMMENT 6281825744 -->
R001 confirmed reaching G001 and normalized portal after reflash: latest normalized receipt 2026-10-19 19:15:37 Pacific, matching fresh non-retained envelope/gateway receipt. Temperature still unverified; issue remains Verify.

Published evidence: https://github.com/lfg-seth/snorr-meshlink/commit/0669ede ; docs/operations/repeater-gateway-check-20261019.md / TEST-020. All five reach G001; no recent G002 copies. No DNS/radio/worker change performed by agent.
<!-- END ORIGINAL COMMENT 6281825744 -->
