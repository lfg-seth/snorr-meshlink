# GitHub issue #39: Handle bounded battery history in demo recovery verification

Immutable import evidence dated **2026-10-21 (America/Los_Angeles)**, retrieved 2026-10-22T01:33:06Z. This snapshot preserves the GitHub record at migration; it is not an active task queue. Historical instructions and claims below describe their original context. Use the repository's current tracker for later status and authorization.

- Source: [Handle bounded battery history in demo recovery verification](https://github.com/lfg-seth/snorr-meshlink/issues/39)
- GitHub state: open; state reason: not supplied.
- Tracking label at import: `status:ready`.
- Labels: `bug`, `status:ready`, `area:portal`, `priority:normal`.
- Assignees: none.
- Author: lfg-seth.
- Created (UTC): 2026-10-21T00:37:49Z.
- Updated (UTC): 2026-10-21T00:37:49Z.
- Closed (UTC): not closed.
- Milestone: none.
- Comments preserved: 0 of 0 reported by GitHub.

## Original issue body

<!-- BEGIN ORIGINAL ISSUE BODY -->
## Observed behavior

During the owner-authorized PR #38 release on 2026-10-20, the pre-existing hosted demo returned 50,000 battery samples with `truncated: true` for the 7-day and 30-day windows. This matches the existing API limit. `deploy/portal/verify-demo.py` rejects that valid response because it assumes every history window is untruncated; its restored-history comparison also assumes the entire query fits the cap.

The pre-release demo database has valid integrity and recovers correctly in an isolated instance. A separate check verified the exact newest bounded samples and truncation flags for all three windows. The refreshed synthetic checkpoint currently fits the cap and passes the existing verifier; a long-running demo can reach the same limit again.

## Acceptance criteria

- Accept valid bounded history responses while checking ordering, exact saved values, sample cap and the correct truncation flag against the restored database.
- Preserve checks for corrupt backups, missing expected history and API/authentication separation.
- Cover the over-limit case through a regression at the appropriate verification seam.
- Keep this scoped to verification; no API limit expansion, history deletion, live data replacement or hardware change.

## Evidence

- Release and backup evidence: `docs/operations/portal-lxc.md` and the 2026-10-20 session log.
- PR #38: https://github.com/lfg-seth/snorr-meshlink/pull/38

No active session claim. Next: implement the verifier correction when selected; current release verification passes for the refreshed demo.

<!-- END ORIGINAL ISSUE BODY -->

## Original comments

No comments at import.
