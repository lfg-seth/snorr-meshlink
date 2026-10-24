# GitHub issue #8: Capture and diagnose recurring high channel utilization

Immutable import evidence dated **2026-10-21 (America/Los_Angeles)**, retrieved 2026-10-22T01:33:06Z. This snapshot preserves the GitHub record at migration; it is not an active task queue. Historical instructions and claims below describe their original context. Use the repository's current tracker for later status and authorization.

- Source: [Capture and diagnose recurring high channel utilization](https://github.com/lfg-seth/snorr-meshlink/issues/8)
- GitHub state: open; state reason: not supplied.
- Tracking label at import: `status:triage`.
- Labels: `bug`, `priority:normal`, `status:triage`, `area:firmware`.
- Assignees: none.
- Author: lfg-seth.
- Created (UTC): 2026-10-17T20:10:08Z.
- Updated (UTC): 2026-10-17T20:10:08Z.
- Closed (UTC): not closed.
- Milestone: none.
- Comments preserved: 0 of 0 reported by GitHub.

## Original issue body

<!-- BEGIN ORIGINAL ISSUE BODY -->
## Outcome

The owner reported a 58% utilization spike. A dedicated receive-only V3 sniffer now exists, but the cause and high-load capture completeness remain unverified.

## Acceptance criteria

- [ ] Capture a real recurrence with synchronized client/gateway observations and the dedicated sniffer.
- [ ] Distinguish packets, duplicates/repeats and local airtime/accounting behavior.
- [ ] Compare an explicitly scoped one-router bench run with a recorded baseline.
- [ ] Record the supported cause or remaining hypotheses and capture limits; separately verify Linux GUI/USB use before relying on it.

## Evidence and decisions

- [docs/operations/channel-utilization-diagnostic.md](https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/channel-utilization-diagnostic.md)
- [docs/operations/airtime-sniffer.md](https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/airtime-sniffer.md)

## Scope and authorization

No router-role change, firmware flash or radio-profile change is authorized by this migration.

Migrated from repository records on 2026-10-17; tracking setup: #1.
<!-- END ORIGINAL ISSUE BODY -->

## Original comments

No comments at import.
