# GitHub issue #49: Improve portal sign-in persistence to avoid roughly hourly reauthentication

Immutable import evidence dated **2026-10-21 (America/Los_Angeles)**, retrieved 2026-10-22T01:33:06Z. This snapshot preserves the GitHub record at migration; it is not an active task queue. Historical instructions and claims below describe their original context. Use the repository's current tracker for later status and authorization.

- Source: [Improve portal sign-in persistence to avoid roughly hourly reauthentication](https://github.com/lfg-seth/snorr-meshlink/issues/49)
- GitHub state: open; state reason: not supplied.
- Tracking label at import: `status:deferred`.
- Labels: `bug`, `area:portal`, `status:deferred`.
- Assignees: none.
- Author: lfg-seth.
- Created (UTC): 2026-10-21T21:45:53Z.
- Updated (UTC): 2026-10-21T21:45:53Z.
- Closed (UTC): not closed.
- Milestone: none.
- Comments preserved: 0 of 0 reported by GitHub.

## Original issue body

<!-- BEGIN ORIGINAL ISSUE BODY -->
## Owner report — 2026-10-21

Owner reports having to sign back in every hour or so and requests better sign-in persistence. Approximate duration is owner-reported, not a measured token lifetime. Browser/device, application version, idle versus active use, tab/reload behavior and reproduction details have not been captured; no cause is established.

## Expected behavior / future acceptance

- Keep a valid portal session signed in through ordinary use instead of prompting for credentials roughly every hour.
- When activated, reproduce the reported expiry and verify persistence across the observed failure boundary, including relevant refresh/revisit behavior.
- Preserve deliberate sign-out, rejected/revoked-session handling and authenticated live/demo separation.

Desired longer session duration and cross-tab/browser-restart expectations remain to define when activated. Related native authentication verification: #6. Do not assume the earlier reload-persistence fix resolves this newly reported issue.

## Deferral and durable record

Capture only for the portal fix list; diagnosis, design, implementation and testing await explicit owner activation. No active claim or milestone.

[Durable wishlist](https://github.com/lfg-seth/snorr-meshlink/blob/main/records/wishlist.md#improve-sign-in-persistence).
<!-- END ORIGINAL ISSUE BODY -->

## Original comments

No comments at import.
