# GitHub issue #2: Measure B001/B002 phone-free GPS freshness and battery runtime

Immutable import evidence dated **2026-10-21 (America/Los_Angeles)**, retrieved 2026-10-22T01:33:06Z. This snapshot preserves the GitHub record at migration; it is not an active task queue. Historical instructions and claims below describe their original context. Use the repository's current tracker for later status and authorization.

- Source: [Measure B001/B002 phone-free GPS freshness and battery runtime](https://github.com/lfg-seth/snorr-meshlink/issues/2)
- GitHub state: open; state reason: not supplied.
- Tracking label at import: `status:ready`.
- Labels: `field-test`, `area:hardware`, `status:ready`, `priority:high`.
- Assignees: none.
- Author: lfg-seth.
- Created (UTC): 2026-10-17T20:09:52Z.
- Updated (UTC): 2026-10-17T20:15:24Z.
- Closed (UTC): not closed.
- Milestone: [#1](https://github.com/lfg-seth/snorr-meshlink/milestone/1).
- Comments preserved: 0 of 0 reported by GitHub.

## Original issue body

<!-- BEGIN ORIGINAL ISSUE BODY -->
## Outcome

Bench GPS ingestion works, but sustained freshness and runtime are unmeasured. Use the two confirmed member trackers before expanding the planned six-member pilot.

## Acceptance criteria

- [ ] Agree the run configuration, sampling and acceptable stale/missing rate before starting; preserve the 15-minute stale threshold.
- [ ] Measure power-on automatic GPS without a phone, GPS measurement age separately from receipt age, both-gateway receipts and battery-only runtime.
- [ ] Record whether each tracker reaches the four-hour minimum and how it compares with the 12-hour target; retain unknowns and interruptions.
- [ ] Publish sanitized results and configuration references in records/field-results.md; keep raw tracks private.

## Evidence and decisions

- [records/field-results.md#test-005--live-portal-gps-ingestion](https://github.com/lfg-seth/snorr-meshlink/blob/main/records/field-results.md#test-005--live-portal-gps-ingestion)
- [docs/operations/heltec-bench-checklist.md](https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/heltec-bench-checklist.md)

## Scope and authorization

Tracking setup only: a future test must have an agreed run plan and available hardware. No hardware changes or field results are implied.

Migrated from repository records on 2026-10-17; tracking setup: #1.
<!-- END ORIGINAL ISSUE BODY -->

## Original comments

No comments at import.
