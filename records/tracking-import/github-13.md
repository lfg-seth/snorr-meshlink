# GitHub issue #13: Choose deployment branch and staging policy before automating releases

Immutable import evidence dated **2026-10-21 (America/Los_Angeles)**, retrieved 2026-10-22T01:33:06Z. This snapshot preserves the GitHub record at migration; it is not an active task queue. Historical instructions and claims below describe their original context. Use the repository's current tracker for later status and authorization.

- Source: [Choose deployment branch and staging policy before automating releases](https://github.com/lfg-seth/snorr-meshlink/issues/13)
- GitHub state: open; state reason: not supplied.
- Tracking label at import: `status:triage`.
- Labels: `area:portal`, `priority:normal`, `status:triage`, `feature`.
- Assignees: none.
- Author: lfg-seth.
- Created (UTC): 2026-10-17T20:10:19Z.
- Updated (UTC): 2026-10-17T20:10:19Z.
- Closed (UTC): not closed.
- Milestone: none.
- Comments preserved: 0 of 0 reported by GitHub.

## Original issue body

<!-- BEGIN ORIGINAL ISSUE BODY -->
## Outcome

Existing CI builds/tests relevant main pushes and PRs. The owner's automatic-deployment discussion left deployment branch, staging scope and private connection unresolved.

## Acceptance criteria

- [ ] Record the owner's deployment-branch and staging choice.
- [ ] Design the smallest authorized connection to the existing LXC and a repeatable update command.
- [ ] Gate any future deployment on successful checks for the same commit, backup/recovery, serialized migration and rollback handling.
- [ ] Track implementation and live acceptance separately after the policy is settled.

## Evidence and decisions

- [records/sessions.md#2026-10-16--review-branch-builds-and-automatic-deployment-requirements](https://github.com/lfg-seth/snorr-meshlink/blob/main/records/sessions.md#2026-10-16--review-branch-builds-and-automatic-deployment-requirements)
- [docs/operations/portal-lxc.md](https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/portal-lxc.md)

## Scope and authorization

No runner installation, credentials, deployment policy or automatic application deployment is configured by this tracking migration.

Migrated from repository records on 2026-10-17; tracking setup: #1.
<!-- END ORIGINAL ISSUE BODY -->

## Original comments

No comments at import.
