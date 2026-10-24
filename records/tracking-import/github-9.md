# GitHub issue #9: Review expanded local demo data and prepare its release

Immutable import evidence dated **2026-10-21 (America/Los_Angeles)**, retrieved 2026-10-22T01:33:06Z. This snapshot preserves the GitHub record at migration; it is not an active task queue. Historical instructions and claims below describe their original context. Use the repository's current tracker for later status and authorization.

- Source: [Review expanded local demo data and prepare its release](https://github.com/lfg-seth/snorr-meshlink/issues/9)
- GitHub state: open; state reason: not supplied.
- Tracking label at import: `status:verify`.
- Labels: `task`, `status:verify`, `area:portal`, `priority:normal`.
- Assignees: none.
- Author: lfg-seth.
- Created (UTC): 2026-10-17T20:10:10Z.
- Updated (UTC): 2026-10-21T00:39:35Z.
- Closed (UTC): not closed.
- Milestone: none.
- Comments preserved: 4 of 4 reported by GitHub.

## Original issue body

<!-- BEGIN ORIGINAL ISSUE BODY -->
## Outcome

Existing uncommitted work fills member batteries, infrastructure power/humidity and SNNS details in the synthetic checkpoint and simulation worker. Its recorded integration checks pass locally; native review and hosted refresh are outstanding.

## Acceptance criteria

- [ ] Review the local portal for member batteries, signed/zero/missing sensor values, humidity and directional neighbor metadata.
- [ ] Review and commit the existing coherent demo changes independently of the tracking migration, preserving the unrelated infrastructure test.
- [ ] When release is authorized, back up the separate hosted demo, refresh deliberately and verify proxy/isolation/recovery boundaries.
- [ ] Record source and deployed state separately; avoid replacing live data or saved demo edits without the approved release procedure.

## Evidence and decisions

- [backend/demo/README.md](https://github.com/lfg-seth/snorr-meshlink/blob/main/backend/demo/README.md)
- [records/sessions.md](https://github.com/lfg-seth/snorr-meshlink/blob/main/records/sessions.md)

## Scope and authorization

The tracking migration does not commit, deploy or replace the pre-existing application/demo work.

Migrated from repository records on 2026-10-17; tracking setup: #1.
<!-- END ORIGINAL ISSUE BODY -->

## Original comments

### Comment 6303666172

- Source: [comment 6303666172](https://github.com/lfg-seth/snorr-meshlink/issues/9#issuecomment-6303666172)
- Author: lfg-seth.
- Created (UTC): 2026-10-20T22:58:41Z.
- Updated (UTC): 2026-10-20T22:58:41Z.

<!-- BEGIN ORIGINAL COMMENT 6303666172 -->
Claimed by Codex on the Dell Linux workspace, 2026-10-20, for the owner's request to push all existing changes. Scope: reconcile latest main, verify and publish the existing demo/minimap edits and session records through a linked PR. No deployment or hardware change. Native review and hosted demo refresh remain separate acceptance steps.
<!-- END ORIGINAL COMMENT 6303666172 -->

### Comment 6303702828

- Source: [comment 6303702828](https://github.com/lfg-seth/snorr-meshlink/issues/9#issuecomment-6303702828)
- Author: lfg-seth.
- Created (UTC): 2026-10-20T23:01:01Z.
- Updated (UTC): 2026-10-20T23:01:01Z.

<!-- BEGIN ORIGINAL COMMENT 6303702828 -->
Published the saved local work in draft PR #38: https://github.com/lfg-seth/snorr-meshlink/pull/38. Demo commit 8264b45; minimap/test commit 3c4f592. All 59 backend tests pass; TypeScript/build and 45 portal checks pass with the previously stalled broad map/legend check excluded. Full portal run timed out after 55 seconds; saved unfinished endpoint-location assertions are preserved and still disagree with the retained location section. No full-suite pass or native visual review claimed. Production remains at bed40dd; no deployment or hosted database refresh. Handoff to Verify, no retained session claim. Next: resolve the broad test/endpoint expectations and perform scoped native review before merge/release.
<!-- END ORIGINAL COMMENT 6303702828 -->

### Comment 6304936799

- Source: [comment 6304936799](https://github.com/lfg-seth/snorr-meshlink/issues/9#issuecomment-6304936799)
- Author: lfg-seth.
- Created (UTC): 2026-10-21T00:29:18Z.
- Updated (UTC): 2026-10-21T00:29:18Z.

<!-- BEGIN ORIGINAL COMMENT 6304936799 -->
Claimed by Codex on Dell Linux, 2026-10-20. Owner explicitly requests merge and deploy of PR #38. Resolve release-blocking test expectations, merge tested source, deploy with private live/demo backups and rollback, refresh the separate synthetic demo, verify source/static/API isolation and isolated recovery. Preserve live identities/configuration/history, credentials and all hardware. Native review remains evidence-dependent.
<!-- END ORIGINAL COMMENT 6304936799 -->

### Comment 6305072169

- Source: [comment 6305072169](https://github.com/lfg-seth/snorr-meshlink/issues/9#issuecomment-6305072169)
- Author: lfg-seth.
- Created (UTC): 2026-10-21T00:39:35Z.
- Updated (UTC): 2026-10-21T00:39:35Z.

<!-- BEGIN ORIGINAL COMMENT 6305072169 -->
Owner-authorized merge/deployment complete: PR #38 merged as application 5d07d61d916290ea81d5ed98bfdadc6127f407eb; production https://meshlink.spp.lol serves it. Release evidence: https://github.com/lfg-seth/snorr-meshlink/commit/87b27ab and https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/portal-lxc.md#demo-feature-examples-and-minimap-navigation--2026-10-20.

All 59 backend and 46 portal checks, TypeScript/live build pass locally/on LXC; both PR and merged-main CI pass. Corrected the unfinished endpoint-removal assertions; full broad map interaction now passes. All 126 installed application source files and nine installed/public build files match. Expanded demo feature state, six services, auth/proxy/token/OS isolation and isolated live/demo backup recovery pass. Old demo workspace is preserved root-private; live database/configuration are unchanged during promotion, and all nine live identities/history remain intact.

Native browser/WebGL/mobile/keyboard review is unverified because no browser surfaces are available; keep remaining visual acceptance in Verify with #6. Live feed is online, latest 200 archived envelopes validate and queue is empty, but no new receipt appeared in the 45-second check. #39 tracks the pre-existing bounded-history verifier assumption. Session claim released. Next: native review of the deployed demo and both icon-to-device transitions.
<!-- END ORIGINAL COMMENT 6305072169 -->
