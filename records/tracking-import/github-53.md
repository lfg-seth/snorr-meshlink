# GitHub issue #53: Prevent battery display freezing when telemetry loses its measurement clock

Immutable import evidence dated **2026-10-21 (America/Los_Angeles)**, retrieved 2026-10-22T01:33:06Z. This snapshot preserves the GitHub record at migration; it is not an active task queue. Historical instructions and claims below describe their original context. Use the repository's current tracker for later status and authorization.

- Source: [Prevent battery display freezing when telemetry loses its measurement clock](https://github.com/lfg-seth/snorr-meshlink/issues/53)
- GitHub state: open; state reason: not supplied.
- Tracking label at import: `status:verify`.
- Labels: `bug`, `status:verify`, `area:portal`.
- Assignees: none.
- Author: lfg-seth.
- Created (UTC): 2026-10-21T22:07:58Z.
- Updated (UTC): 2026-10-22T01:29:36Z.
- Closed (UTC): not closed.
- Milestone: none.
- Comments preserved: 0 of 0 reported by GitHub.

## Original issue body

<!-- BEGIN ORIGINAL ISSUE BODY -->
## Deployed — 2026-10-21

Owner explicitly authorizes deployment. [Use receipt time when telemetry lacks a valid calendar clock — PR #54](https://github.com/lfg-seth/snorr-meshlink/pull/54) is merged as **8c5350e8834a771781d594414bd6b7c812a5f136** and deployed to https://meshlink.spp.lol at approximately 18:17 Pacific. Published deployment/evidence records **0713f7e** are on main and pinned in the LXC. Separate from draft neighbor PR #50.

Telemetry selection, displayed measurement time/age, battery history and supported telemetry health prefer valid source calendar time; otherwise original receipt time. Absent/invalid/future source clocks remain null/empty with quality retained. Uptime is unused. Duplicate gateway deliveries cannot refresh a selected reading's fallback age. GPS/neighbor freshness remains separate.

## Passed verification

- Final PR CI and actual LXC isolated checks: **63 backend tests, 49 portal tests, TypeScript and live build**. Deployment verifier fc24573 also supports receipt-fallback history provenance and older backups.
- Pre-release, post-release and final fresh-telemetry backup checksums plus isolated live database/API and separate demo database/API/history recovery.
- Exact live/demo database, credentials and worker-configuration hashes unchanged during quiesced promotion; all nine devices and histories retained. No schema migration, firmware or device configuration/clock change.
- Nine public HTTPS asset hashes, live/demo token/OS isolation, protected routes, per-client authentication throttling and all six services. Fresh MQTT archive traffic, 200 envelopes and zero pending queue.
- Fresh normal-cadence battery packets: **R004 4.091 V**, measured **18:24:16 Pacific**, received **18:24:19.842**, replaces its selected five-hour-old reading; **R002 4.110 V**, measured **18:26:54**, received **18:26:59.318**, advances selected timestamp/history. Both packets have valid calendar clocks, which are correctly preferred. Historical unknown-time observations immediately appear with receipt fallback in battery history; isolated regressions verify unknown-time selection.
- Actual React node-card and battery-detail renders using sanitized authenticated data show R002 4.110 V / 28s ago and R004 4.091 V / 3m 6s ago, with 78/77 samples in their 24-hour histories and no measurement-time-unknown message.

[Durable diagnosis, behavior, exact backup hashes, release and limits](https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/battery-contact-freshness-20261021.md#deployment---2026-10-21).

## Remaining acceptance

Native owner browser/mobile presentation and sustained telemetry/outage behavior remain unverified. Refresh the portal for the new build. Receipt time remains the owner-approved temporary approximation and can understate age for delayed unknown-clock packets. Hardware calendar-clock recovery remains separate from this backend correction.

Codex Windows deployment claim released to Verify; no retained session claim. Rollback/source are retained privately. The user-authorized deployment resolves the earlier staging authorization limitation. Derived Project reconciliation awaits authenticated CLI access.
<!-- END ORIGINAL ISSUE BODY -->

## Original comments

No comments at import.
