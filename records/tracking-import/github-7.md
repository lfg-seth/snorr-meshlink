# GitHub issue #7: Establish and verify off-host live and demo backup recovery

Immutable import evidence dated **2026-10-21 (America/Los_Angeles)**, retrieved 2026-10-22T01:33:06Z. This snapshot preserves the GitHub record at migration; it is not an active task queue. Historical instructions and claims below describe their original context. Use the repository's current tracker for later status and authorization.

- Source: [Establish and verify off-host live and demo backup recovery](https://github.com/lfg-seth/snorr-meshlink/issues/7)
- GitHub state: open; state reason: not supplied.
- Tracking label at import: `status:triage`.
- Labels: `task`, `priority:high`, `area:backhaul`, `status:triage`.
- Assignees: none.
- Author: lfg-seth.
- Created (UTC): 2026-10-17T20:10:02Z.
- Updated (UTC): 2026-10-17T21:58:50Z.
- Closed (UTC): not closed.
- Milestone: [#1](https://github.com/lfg-seth/snorr-meshlink/milestone/1).
- Comments preserved: 1 of 1 reported by GitHub.

## Original issue body

<!-- BEGIN ORIGINAL ISSUE BODY -->
## Outcome

Isolated backup restoration is recorded. Off-host backup destination, scheduling, retention and recovery ownership remain unfinished.

## Acceptance criteria

- [ ] Select an owner-approved private destination and retention/ownership policy using existing resources first.
- [ ] Implement authorized off-host transfer without exposing credentials or live data in GitHub.
- [ ] Restore an off-host copy in isolation and verify identities, history, archive and live/demo separation.
- [ ] Document recovery procedure, failure visibility and measured evidence.

## Evidence and decisions

- [docs/operations/portal-lxc.md](https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/portal-lxc.md)
- [docs/operations/development-handoff.md](https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/development-handoff.md)

## Scope and authorization

No new service purchase or upload of operational data is authorized by capturing this issue.

Migrated from repository records on 2026-10-17; tracking setup: #1.
<!-- END ORIGINAL ISSUE BODY -->

## Original comments

### Comment 6241855655

- Source: [comment 6241855655](https://github.com/lfg-seth/snorr-meshlink/issues/7#issuecomment-6241855655)
- Author: lfg-seth.
- Created (UTC): 2026-10-17T21:58:50Z.
- Updated (UTC): 2026-10-17T21:58:50Z.

<!-- BEGIN ORIGINAL COMMENT 6241855655 -->
The owner-authorized private monitoring deployment (#22) adds another local-only recovery scope: MeshMonitor SQLite/configuration, daily 02:45 Pacific consistent backups (14 archives) and an isolated boot/row-preservation restore check pass. Backups remain on that LXC’s disk. Include MeshMonitor and the existing Grafana/Prometheus configuration/state in the eventual owner-selected off-host destination and recovery policy; no off-host copy or new destination is claimed. Operations record: docs/operations/meshmonitor-lxc.md.
<!-- END ORIGINAL COMMENT 6241855655 -->
