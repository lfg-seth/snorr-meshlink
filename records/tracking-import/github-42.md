# GitHub issue #42: Populate gateway battery graphs from reported voltage

Immutable import evidence dated **2026-10-21 (America/Los_Angeles)**, retrieved 2026-10-22T01:33:06Z. This snapshot preserves the GitHub record at migration; it is not an active task queue. Historical instructions and claims below describe their original context. Use the repository's current tracker for later status and authorization.

- Source: [Populate gateway battery graphs from reported voltage](https://github.com/lfg-seth/snorr-meshlink/issues/42)
- GitHub state: open; state reason: not supplied.
- Tracking label at import: `status:verify`.
- Labels: `bug`, `status:verify`, `area:portal`.
- Assignees: none.
- Author: lfg-seth.
- Created (UTC): 2026-10-21T21:00:12Z.
- Updated (UTC): 2026-10-21T21:19:31Z.
- Closed (UTC): not closed.
- Milestone: none.
- Comments preserved: 3 of 3 reported by GitHub.

## Original issue body

<!-- BEGIN ORIGINAL ISSUE BODY -->
## Outcome — deployed 2026-10-21

Owner restores connectivity and authorizes deployment. [PR #46](https://github.com/lfg-seth/snorr-meshlink/pull/46) is merged; application **fa035509dfc2fd1492c8ae01618d99269c9a4f92** is deployed at meshlink.spp.lol. Zero-cadence rendering hid isolated measured voltage samples. Exact dots now appear with unknown cadence; known-cadence curves preserve outage breaks.

## Verified

- Owner confirms one installed 1000 mAh LiPo in each gateway; inventory and both live portal pack profiles/capacities/descriptions agree.
- Production readback confirms original zero cadence on both gateways, 47 measured G002 voltage samples and zero G001 battery reports.
- Actual React regression fails before and passes after correction. All 47 portal tests, TypeScript and live build pass on server Node 22.23.1; original pinned CI also passes.
- G002 battery-specific expected cadence is five minutes, matching today's verified radio profile; G001 cadence remains unknown. All nine identities, other metadata and monitoring enablement are preserved.
- Actual components render 48 captured live G002 samples as a measured curve with approximate 80% at 3.996 V. The same history renders as exact dots without cadence. G001 correctly awaits reports.
- All nine public HTTPS build files match the tested build, all six services are active, public/authentication/token/OS boundaries pass, and final backup restores live/demo databases/APIs/history in isolation. Fresh MQTT archive reception, latest 200 envelope checks and empty queue pass.
- Initial public asset 403 is traced to root-only staging modes, corrected to 0644 for public build files and all checks rerun successfully. No protection bypass or secret permission expansion.

## Evidence / remaining confirmation

[Durable deployment, exact backups/hashes and limits](https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/gateway-battery-graphs.md#verification-and-deployment).

No native browser/mobile review or field/runtime/calibration acceptance claimed. Remaining check: refresh the portal on an owner device and confirm graph presentation. G001 has no battery telemetry yet; enabling it remains separately authorized later work, not a rendering failure. No radio/backend/schema changes.

Codex Windows desktop session releases claim to Verify. Source/static rollback retained at /opt/meshlink-rollback-fa03550; private snapshots/render evidence remain on the LXC. Derived Project reconciliation awaits authenticated GitHub CLI, absent locally/on LXC.
<!-- END ORIGINAL ISSUE BODY -->

## Original comments

### Comment 6326574201

- Source: [comment 6326574201](https://github.com/lfg-seth/snorr-meshlink/issues/42#issuecomment-6326574201)
- Author: lfg-seth.
- Created (UTC): 2026-10-21T21:07:24Z.
- Updated (UTC): 2026-10-21T21:07:24Z.

<!-- BEGIN ORIGINAL COMMENT 6326574201 -->
Pinned-runtime verification now passes: [Portal CI on c15859a](https://github.com/lfg-seth/snorr-meshlink/actions/runs/39675958265), using repository Node 22.23.1, completes successfully. [PR #46](https://github.com/lfg-seth/snorr-meshlink/pull/46) contains the tested correction and confirmed inventory; evidence published in 6ad5cc3. Review, production metadata/history readback, pack metadata updates, deployment and live/native verification remain pending; recorded SSH hostname returns NXDOMAIN. No retained session claim.
<!-- END ORIGINAL COMMENT 6326574201 -->

### Comment 6326603589

- Source: [comment 6326603589](https://github.com/lfg-seth/snorr-meshlink/issues/42#issuecomment-6326603589)
- Author: lfg-seth.
- Created (UTC): 2026-10-21T21:09:01Z.
- Updated (UTC): 2026-10-21T21:09:01Z.

<!-- BEGIN ORIGINAL COMMENT 6326603589 -->
Owner restores connectivity and authorizes deployment on 2026-10-21. Codex Windows desktop session reclaims the bounded release: inspect live metadata/history, verify backup, merge/publish PR #46, deploy tested frontend, apply confirmed gateway battery details and verify recovery/live graphs. No radio configuration or flashing. SSH now succeeds; current source 5d07d61 and all six services active.
<!-- END ORIGINAL COMMENT 6326603589 -->

### Comment 6326795072

- Source: [comment 6326795072](https://github.com/lfg-seth/snorr-meshlink/issues/42#issuecomment-6326795072)
- Author: lfg-seth.
- Created (UTC): 2026-10-21T21:19:31Z.
- Updated (UTC): 2026-10-21T21:19:31Z.

<!-- BEGIN ORIGINAL COMMENT 6326795072 -->
Deployment evidence is published to origin/main in [f1e4c4d](https://github.com/lfg-seth/snorr-meshlink/commit/f1e4c4d). Application source remains fa03550. Final public assets, recovery and fresh ingestion pass; claim released. Remaining owner-device presentation confirmation only. G001 correctly awaits battery telemetry; this deployment does not configure its radio.
<!-- END ORIGINAL COMMENT 6326795072 -->
