# GitHub issue #5: Verify fresh G002 neighbor and sensor-power delivery end to end

Immutable import evidence dated **2026-10-21 (America/Los_Angeles)**, retrieved 2026-10-22T01:33:06Z. This snapshot preserves the GitHub record at migration; it is not an active task queue. Historical instructions and claims below describe their original context. Use the repository's current tracker for later status and authorization.

- Source: [Verify fresh G002 neighbor and sensor-power delivery end to end](https://github.com/lfg-seth/snorr-meshlink/issues/5)
- GitHub state: open; state reason: not supplied.
- Tracking label at import: `status:verify`.
- Labels: `field-test`, `priority:high`, `area:backhaul`, `status:verify`.
- Assignees: none.
- Author: lfg-seth.
- Created (UTC): 2026-10-17T20:09:58Z.
- Updated (UTC): 2026-10-20T02:46:48Z.
- Closed (UTC): not closed.
- Milestone: [#1](https://github.com/lfg-seth/snorr-meshlink/milestone/1).
- Comments preserved: 1 of 1 reported by GitHub.

## Original issue body

<!-- BEGIN ORIGINAL ISSUE BODY -->
## Outcome

The deployed decoder and fresh R005/G001 normalization pass. Fresh G002 neighbor/power receipt remains unverified; earlier two-gateway GPS and voltage checks are separate evidence.

## Acceptance criteria

- [ ] Observe new reports from known configured devices through G002, distinguishing fresh traffic from archive replay.
- [ ] Check RF/MQTT archive receipt and normalized portal records with gateway identity preserved.
- [ ] Verify both-gateway deduplication without losing per-gateway evidence.
- [ ] Record the observed result and limits; if G002 is absent, capture the first failing stage rather than assuming a cause.

## Evidence and decisions

- [docs/operations/radio-report-ingestion.md](https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/radio-report-ingestion.md)
- [docs/operations/r002-release-update.md](https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/r002-release-update.md)
- [docs/operations/r004-preparation.md](https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/r004-preparation.md)

## Scope and authorization

Migrated verification follow-up. Record measured evidence separately from implementation; this migration performs no application deployment or hardware change.

Migrated from repository records on 2026-10-17; tracking setup: #1.
<!-- END ORIGINAL ISSUE BODY -->

## Original comments

### Comment 6282146289

- Source: [comment 6282146289](https://github.com/lfg-seth/snorr-meshlink/issues/5#issuecomment-6282146289)
- Author: lfg-seth.
- Created (UTC): 2026-10-20T02:46:47Z.
- Updated (UTC): 2026-10-20T02:46:47Z.

<!-- BEGIN ORIGINAL COMMENT 6282146289 -->
2026-10-19 scoped G002 neighbor verification now passes under #31. After owner-supplied replacement Wi-Fi, fresh R005 19:40:38, R002 19:41:39 and R001 19:41:47 Pacific SNNS copies arrive through G002. Independent database checks confirm G001/G002 receipts for each packet and no duplicate reports; G002-copy portal outcomes correctly duplicate. G002's own richer collector delivers a five-row self-observer report at 19:42:36, normalized/accepted, with authenticated snapshot provenance checks.

Current RAK bench profile deliberately disables power telemetry, so fresh sensor-power verification is not claimed and this issue remains open. Evidence: docs/operations/g002-neighbor-gateway.md / TEST-021, published with session records. Sustained cadence/calibration/field limits remain.
<!-- END ORIGINAL COMMENT 6282146289 -->
