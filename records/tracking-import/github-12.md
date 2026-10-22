# GitHub issue #12: Revisit Heltec MQTT over WebSockets only if the deployed transport needs it

Immutable import evidence dated **2026-10-21 (America/Los_Angeles)**, retrieved 2026-10-22T01:33:06Z. This snapshot preserves the GitHub record at migration; it is not an active task queue. Historical instructions and claims below describe their original context. Use the repository's current tracker for later status and authorization.

- Source: [Revisit Heltec MQTT over WebSockets only if the deployed transport needs it](https://github.com/lfg-seth/snorr-meshlink/issues/12)
- GitHub state: open; state reason: not supplied.
- Tracking label at import: `status:deferred`.
- Labels: `area:backhaul`, `research`, `status:deferred`.
- Assignees: none.
- Author: lfg-seth.
- Created (UTC): 2026-10-17T20:10:17Z.
- Updated (UTC): 2026-10-17T20:10:17Z.
- Closed (UTC): not closed.
- Milestone: none.
- Comments preserved: 0 of 0 reported by GitHub.

## Original issue body

<!-- BEGIN ORIGINAL ISSUE BODY -->
## Outcome

Migrate the unresolved original WebSockets research question. The pilot now uses actual TCP/TLS MQTT through Nginx on 8883 with live portal ingestion; that implementation does not establish stock WebSockets support or resolve the old research question.

## Acceptance criteria

- [ ] Owner explicitly reactivates WebSockets research or identifies a concrete need not met by the current path.
- [ ] If reactivated, verify current V3/V4 transport support and Cloudflare requirements against primary sources.
- [ ] Record a scoped answer or an owner decision to retire the alternative; preserve the historical connectivity evidence.

## Evidence and decisions

- [.scratch/pilot/issues/09-heltec-websocket-research.md](https://github.com/lfg-seth/snorr-meshlink/blob/main/.scratch/pilot/issues/09-heltec-websocket-research.md)
- [docs/operations/live-mqtt.md](https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/live-mqtt.md)
- [docs/research/dispatch-portal-transport.md](https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/research/dispatch-portal-transport.md)

## Scope and authorization

Deferred alternative. This is not a claim that the working pilot MQTT path is broken or a request to redesign it.

Migrated from repository records on 2026-10-17; tracking setup: #1.
<!-- END ORIGINAL ISSUE BODY -->

## Original comments

No comments at import.
