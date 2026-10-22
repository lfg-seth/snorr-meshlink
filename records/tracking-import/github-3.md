# GitHub issue #3: Verify forced GPS relaying and local viewing through backhaul outages

Immutable import evidence dated **2026-10-21 (America/Los_Angeles)**, retrieved 2026-10-22T01:33:06Z. This snapshot preserves the GitHub record at migration; it is not an active task queue. Historical instructions and claims below describe their original context. Use the repository's current tracker for later status and authorization.

- Source: [Verify forced GPS relaying and local viewing through backhaul outages](https://github.com/lfg-seth/snorr-meshlink/issues/3)
- GitHub state: open; state reason: not supplied.
- Tracking label at import: `status:ready`.
- Labels: `field-test`, `status:ready`, `priority:high`, `area:backhaul`.
- Assignees: none.
- Author: lfg-seth.
- Created (UTC): 2026-10-17T20:09:54Z.
- Updated (UTC): 2026-10-17T20:15:25Z.
- Closed (UTC): not closed.
- Milestone: [#1](https://github.com/lfg-seth/snorr-meshlink/milestone/1).
- Comments preserved: 0 of 0 reported by GitHub.

## Original issue body

<!-- BEGIN ORIGINAL ISSUE BODY -->
## Outcome

Direct bench reception and worker restart checks do not prove forced relaying or useful local operation without internet.

## Acceptance criteria

- [ ] Define a controlled test that distinguishes forced RAK relaying from direct V4-to-V3 reception.
- [ ] Observe gateway Wi-Fi/broker interruptions and recovery; preserve GPS measurement timestamps and deduplication.
- [ ] Verify local command-post and companion-app viewing without internet, prepared maps and explicit stale/missing positions.
- [ ] Record attempts, failures, configuration and measured recovery behavior in records/field-results.md.

## Evidence and decisions

- [PROJECT.md](https://github.com/lfg-seth/snorr-meshlink/blob/main/PROJECT.md)
- [docs/operations/live-mqtt.md](https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/live-mqtt.md)
- [docs/operations/rak-pilot-setup.md](https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/rak-pilot-setup.md)

## Scope and authorization

Do not silently change gateway transmit permissions or radio profiles. Missing results remain unverified.

Migrated from repository records on 2026-10-17; tracking setup: #1.
<!-- END ORIGINAL ISSUE BODY -->

## Original comments

No comments at import.
