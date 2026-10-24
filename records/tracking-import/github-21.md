# GitHub issue #21: Open neighbor devices through minimap icons

Immutable import evidence dated **2026-10-21 (America/Los_Angeles)**, retrieved 2026-10-22T01:33:06Z. This snapshot preserves the GitHub record at migration; it is not an active task queue. Historical instructions and claims below describe their original context. Use the repository's current tracker for later status and authorization.

- Source: [Open neighbor devices through minimap icons](https://github.com/lfg-seth/snorr-meshlink/issues/21)
- GitHub state: open; state reason: not supplied.
- Tracking label at import: `status:verify`.
- Labels: `task`, `status:verify`, `area:portal`.
- Assignees: none.
- Author: lfg-seth.
- Created (UTC): 2026-10-17T20:40:57Z.
- Updated (UTC): 2026-10-21T00:39:41Z.
- Closed (UTC): not closed.
- Milestone: none.
- Comments preserved: 5 of 5 reported by GitHub.

## Original issue body

<!-- BEGIN ORIGINAL ISSUE BODY -->
## Outcome

Owner requests replacing the neighbor card's separate Open device buttons with clickable minimap node icons.

## Acceptance criteria

- Remove the separate Open device buttons from the neighbor card.
- Each located endpoint icon opens its corresponding device card and supports keyboard activation with an accessible name.
- Preserve marker appearance, assignment labels, map lines and single-card navigation; keep unknown locations explicit.
- Verify the portal interaction checks and build. Record any pre-existing failures independently.

## Claim and scope

In progress: Codex session on the Dell Linux workspace, 2026-10-17. User-authorized UI change only; no deployment or hardware work. Preserve existing demo changes and the unfinished endpoint-location test edits.

<!-- END ORIGINAL ISSUE BODY -->

## Original comments

### Comment 6240736808

- Source: [comment 6240736808](https://github.com/lfg-seth/snorr-meshlink/issues/21#issuecomment-6240736808)
- Author: lfg-seth.
- Created (UTC): 2026-10-17T20:44:45Z.
- Updated (UTC): 2026-10-17T20:44:45Z.

<!-- BEGIN ORIGINAL COMMENT 6240736808 -->
Local implementation is ready for verification. Removed the separate Open device buttons; neighbor minimap endpoints are named native buttons that select by persistent device identity and stop click propagation. Assigned marker labels, colocated icons, map lines and explicit missing locations are preserved.

Validation: focused interaction check passes; 45 portal checks pass excluding the broad map/legend interaction test. Typecheck/production build and Git whitespace checks pass. The broad test stalls in sandboxed and unsandboxed runs (also recorded before this change); its pre-existing unfinished endpoint-location assertions remain preserved. No native browser surface is available, so native keyboard/WebGL/visual review is unverified.

Evidence: `portal/src/CardMiniMap.tsx`, `portal/src/DeviceSheet.tsx`, `portal/src/SignalLinkDetail.tsx`, `portal/tests/infrastructure.test.mjs` and the 2026-10-17 session entry “Open neighbor devices from minimap icons”. These are uncommitted local changes; no published source or deployment is claimed. Unrelated demo and test work is preserved.

Session claim released. Next: visually verify both icon-to-device transitions, resolve the existing broad-test stall/unfinished expectations, then publish scoped source when requested. No deployment or hardware work performed.

<!-- END ORIGINAL COMMENT 6240736808 -->

### Comment 6303667496

- Source: [comment 6303667496](https://github.com/lfg-seth/snorr-meshlink/issues/21#issuecomment-6303667496)
- Author: lfg-seth.
- Created (UTC): 2026-10-20T22:58:46Z.
- Updated (UTC): 2026-10-20T22:58:46Z.

<!-- BEGIN ORIGINAL COMMENT 6303667496 -->
Claimed by Codex on the Dell Linux workspace, 2026-10-20, for the owner's request to push all existing changes. Scope: reconcile latest main, verify and publish the existing demo/minimap edits and session records through a linked PR. No deployment or hardware change. Native review and hosted demo refresh remain separate acceptance steps.
<!-- END ORIGINAL COMMENT 6303667496 -->

### Comment 6303704316

- Source: [comment 6303704316](https://github.com/lfg-seth/snorr-meshlink/issues/21#issuecomment-6303704316)
- Author: lfg-seth.
- Created (UTC): 2026-10-20T23:01:07Z.
- Updated (UTC): 2026-10-20T23:01:07Z.

<!-- BEGIN ORIGINAL COMMENT 6303704316 -->
Published the saved local work in draft PR #38: https://github.com/lfg-seth/snorr-meshlink/pull/38. Demo commit 8264b45; minimap/test commit 3c4f592. All 59 backend tests pass; TypeScript/build and 45 portal checks pass with the previously stalled broad map/legend check excluded. Full portal run timed out after 55 seconds; saved unfinished endpoint-location assertions are preserved and still disagree with the retained location section. No full-suite pass or native visual review claimed. Production remains at bed40dd; no deployment or hosted database refresh. Handoff to Verify, no retained session claim. Next: resolve the broad test/endpoint expectations and perform scoped native review before merge/release.
<!-- END ORIGINAL COMMENT 6303704316 -->

### Comment 6304937975

- Source: [comment 6304937975](https://github.com/lfg-seth/snorr-meshlink/issues/21#issuecomment-6304937975)
- Author: lfg-seth.
- Created (UTC): 2026-10-21T00:29:23Z.
- Updated (UTC): 2026-10-21T00:29:23Z.

<!-- BEGIN ORIGINAL COMMENT 6304937975 -->
Claimed by Codex on Dell Linux, 2026-10-20. Owner explicitly requests merge and deploy of PR #38. Resolve release-blocking test expectations, merge tested source, deploy with private live/demo backups and rollback, refresh the separate synthetic demo, verify source/static/API isolation and isolated recovery. Preserve live identities/configuration/history, credentials and all hardware. Native review remains evidence-dependent.
<!-- END ORIGINAL COMMENT 6304937975 -->

### Comment 6305073388

- Source: [comment 6305073388](https://github.com/lfg-seth/snorr-meshlink/issues/21#issuecomment-6305073388)
- Author: lfg-seth.
- Created (UTC): 2026-10-21T00:39:41Z.
- Updated (UTC): 2026-10-21T00:39:41Z.

<!-- BEGIN ORIGINAL COMMENT 6305073388 -->
Owner-authorized merge/deployment complete: PR #38 merged as application 5d07d61d916290ea81d5ed98bfdadc6127f407eb; production https://meshlink.spp.lol serves it. Release evidence: https://github.com/lfg-seth/snorr-meshlink/commit/87b27ab and https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/portal-lxc.md#demo-feature-examples-and-minimap-navigation--2026-10-20.

All 59 backend and 46 portal checks, TypeScript/live build pass locally/on LXC; both PR and merged-main CI pass. Corrected the unfinished endpoint-removal assertions; full broad map interaction now passes. All 126 installed application source files and nine installed/public build files match. Expanded demo feature state, six services, auth/proxy/token/OS isolation and isolated live/demo backup recovery pass. Old demo workspace is preserved root-private; live database/configuration are unchanged during promotion, and all nine live identities/history remain intact.

Native browser/WebGL/mobile/keyboard review is unverified because no browser surfaces are available; keep remaining visual acceptance in Verify with #6. Live feed is online, latest 200 archived envelopes validate and queue is empty, but no new receipt appeared in the 45-second check. #39 tracks the pre-existing bounded-history verifier assumption. Session claim released. Next: native review of the deployed demo and both icon-to-device transitions.
<!-- END ORIGINAL COMMENT 6305073388 -->
