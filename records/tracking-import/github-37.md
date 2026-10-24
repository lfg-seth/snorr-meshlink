# GitHub issue #37: Allow starting, stopping and restarting member GPS tracking sessions while devices stay on

Immutable import evidence dated **2026-10-21 (America/Los_Angeles)**, retrieved 2026-10-22T01:33:06Z. This snapshot preserves the GitHub record at migration; it is not an active task queue. Historical instructions and claims below describe their original context. Use the repository's current tracker for later status and authorization.

- Source: [Allow starting, stopping and restarting member GPS tracking sessions while devices stay on](https://github.com/lfg-seth/snorr-meshlink/issues/37)
- GitHub state: open; state reason: not supplied.
- Tracking label at import: `status:deferred`.
- Labels: `area:portal`, `feature`, `status:deferred`.
- Assignees: none.
- Author: lfg-seth.
- Created (UTC): 2026-10-20T03:11:05Z.
- Updated (UTC): 2026-10-20T03:11:05Z.
- Closed (UTC): not closed.
- Milestone: none.
- Comments preserved: 0 of 0 reported by GitHub.

## Original issue body

<!-- BEGIN ORIGINAL ISSUE BODY -->
## Owner request — 2026-10-19

Improve how member-node (client) GPS tracking sessions work. Provide a way to start, stop and restart a tracking session even when the device remains powered on the entire time.

## Requested behavior / future acceptance

- Start a GPS tracking session for a node that is already powered on.
- Stop a tracking session without requiring the node to power off.
- Restart a tracking session while the node stays on; session boundaries must be independent of device uptime or reboot boundaries.
- Verify the stop/start/restart sequence with a continuously powered device when this work is activated.

Control location, authorized roles, whether restart resumes a session or creates a new one, and treatment of GPS reports outside active sessions remain to define when activated. This captures tracking-session control; it does not select changes to radio broadcasting or raw-data retention.

## Deferral and durable record

Deferred by owner for later. Capture only: no research, design, implementation or testing until explicit owner activation. No active claim or milestone.

[Durable wishlist](https://github.com/lfg-seth/snorr-meshlink/blob/main/records/wishlist.md#member-gps-tracking-session-controls).
<!-- END ORIGINAL ISSUE BODY -->

## Original comments

No comments at import.
