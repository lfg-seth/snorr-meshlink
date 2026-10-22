# GitHub issue #23: Verify MeshMonitor browser views, two-gateway behavior and storage growth

Immutable import evidence dated **2026-10-21 (America/Los_Angeles)**, retrieved 2026-10-22T01:33:06Z. This snapshot preserves the GitHub record at migration; it is not an active task queue. Historical instructions and claims below describe their original context. Use the repository's current tracker for later status and authorization.

- Source: [Verify MeshMonitor browser views, two-gateway behavior and storage growth](https://github.com/lfg-seth/snorr-meshlink/issues/23)
- GitHub state: open; state reason: not supplied.
- Tracking label at import: `status:verify`.
- Labels: `task`, `area:backhaul`, `status:verify`, `priority:normal`.
- Assignees: none.
- Author: lfg-seth.
- Created (UTC): 2026-10-17T21:58:48Z.
- Updated (UTC): 2026-10-17T22:02:31Z.
- Closed (UTC): not closed.
- Milestone: none.
- Comments preserved: 1 of 1 reported by GitHub.

## Original issue body

<!-- BEGIN ORIGINAL ISSUE BODY -->
## Outcome

Follow-up to the owner-authorized private MeshMonitor deployment (#22), separated from installation/recovery acceptance. MeshMonitor 4.17.0 is an exploratory read-only subscriber; the existing portal remains authoritative for exact MQTT archiving, GPS measurement freshness and per-gateway operational receipts.

## Acceptance criteria

- [ ] Review authenticated MeshMonitor and SNORR Grafana dashboard in native desktop/mobile browsers; distinguish live values, unknowns and cached telemetry.
- [ ] Observe fresh G001 and G002 copies of deliberately scoped packets and verify reception/grouping without replacing content-aware portal deduplication. Initial live check saw only one gateway.
- [ ] Measure 24-hour and longer database/Prometheus growth with 30-day global metrics retention and no automatic MeshMonitor history pruning.
- [ ] Record outage/stale/replay behavior and explicitly retain the upstream GPS observation-time versus measurement-time and packet-ID dedup limitations.

## Evidence

- [Deployment and recovery](https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/meshmonitor-lxc.md)
- [Scope decision](https://github.com/lfg-seth/snorr-meshlink/blob/main/.scratch/pilot/issues/20-monitoring-scope-stack.md)

No custom exporter, firmware changes, raw-history backfill, public route, searchable logs or external notifications are activated by this follow-up. Off-host recovery remains #7. No active session claim is retained.
<!-- END ORIGINAL ISSUE BODY -->

## Original comments

### Comment 6241891801

- Source: [comment 6241891801](https://github.com/lfg-seth/snorr-meshlink/issues/23#issuecomment-6241891801)
- Author: lfg-seth.
- Created (UTC): 2026-10-17T22:02:31Z.
- Updated (UTC): 2026-10-17T22:02:31Z.

<!-- BEGIN ORIGINAL COMMENT 6241891801 -->
Published evidence is currently available on the deployment branch: https://github.com/lfg-seth/snorr-meshlink/blob/codex/deploy-meshmonitor/docs/operations/meshmonitor-lxc.md . PR #24 is open awaiting explicit merge authorization, so the main-branch record link becomes available after merge. Live deployment/restart/recovery is complete. Final live check sees four node rows (including inferred gateway placeholder), 24 telemetry rows, seven ingested MQTT packet logs, two voltage series and one gateway. These growing counts are observations, not field or two-gateway acceptance. No active session claim retained.
<!-- END ORIGINAL COMMENT 6241891801 -->
