# GitHub issue #47: Hide stale neighbor signals and prevent cached reports refreshing link activity

Immutable import evidence dated **2026-10-21 (America/Los_Angeles)**, retrieved 2026-10-22T01:33:06Z. This snapshot preserves the GitHub record at migration; it is not an active task queue. Historical instructions and claims below describe their original context. Use the repository's current tracker for later status and authorization.

- Source: [Hide stale neighbor signals and prevent cached reports refreshing link activity](https://github.com/lfg-seth/snorr-meshlink/issues/47)
- GitHub state: open; state reason: reopened.
- Tracking label at import: `status:triage`.
- Labels: `bug`, `area:portal`, `status:triage`.
- Assignees: none.
- Author: lfg-seth.
- Created (UTC): 2026-10-21T21:24:27Z.
- Updated (UTC): 2026-10-22T01:05:08Z.
- Closed (UTC): not closed.
- Milestone: none.
- Comments preserved: 0 of 0 reported by GitHub.

## Original issue body

<!-- BEGIN ORIGINAL ISSUE BODY -->
## Simpler approach reassessment — 2026-10-21

Owner questions the timestamp-first approach and asks about not storing stale readings. Absolute UTC hearing timestamps are not an approved design requirement. The initial draft below overconstrains the solution: the actual observed bug can be addressed by excluding cached standard tables from current-link evidence and using the existing SNNS relative ages/boot/sequence evidence. Custom source entries already expire after thirty minutes on monotonic uptime. Removing old database rows alone would permit a new table delivery to reinsert an old signal.

Compare a small expiring current-neighbor state and monotonic source/queue expiry (with stale snapshots dropped and fresh passive data after reconnect) against the absolute-source-time alternative. Relative hearing age plus elapsed time since first receipt is useful online but does not bound unseen transport delay. For strict outage-safe expiry, verify all buffering residence bounds or carry source-time information; do not assume synchronized UTC clocks are the only solution. #51/#52 now mark timestamp criteria as initial proposals under review. No alternative is selected; this issue is Triage rather than blocked on an unselected timestamp design. Existing code/tests remain the absolute-time-only checkpoint, not a completed new solution.

## Current outcome — firmware compatibility reviewed 2026-10-21

Owner requests correcting misleading neighbor freshness and hiding signals two or more hours old across the portal; then asks whether installed firmware supports it.

The tested frontend filter exists in **draft PR #50**, but is not a complete useful release: every inspected live signal has unknown absolute hearing time, so the current filter hides all of them. Do not deploy this checkpoint as the completed fix.

## Firmware facts

- Current custom RAK/V3 SNNS reports contain relative hearing age at encoding, boot ID, sequence, uptime and thirty-minute collector expiry. Standard NeighborInfo omits per-entry hearing time/age.
- Both gateway-own live packets contain plausible rx_time clocks. Source inspection disproves the initial universal creation-clock interpretation: Router::handleReceived overwrites rx_time during broadcast processing after encoding, and forwarded packets acquire the receiving gateway's clock.
- A reliable absolute cutoff through delayed delivery needs a source hearing/encoding timestamp within the report payload with explicit clock quality, followed by ingestion support. B002 itself need not report neighbors for a gateway/repeater to observe it; this does not imply member firmware must change.

## Next bounded work

Prepare a compatible reporter timestamp extension and ingestion provenance; preserve legacy decoding with unknown timing; reject invalid/future/uncertain clock evidence; verify delayed delivery and replay cannot refresh hearing activity; retain fresh verified readings and expire at two hours across every view. Complete isolated backend/portal and fresh hardware receipts before release acceptance. Source changes and device flashing remain separate; no firmware or hardware change is authorized merely by the PR.

## Existing evidence and handoff

Application a9ae4b9 implements the filter; records b53434d correct the compatibility handoff. All 52 filter tests/TypeScript/build pass locally and on pinned server Node; Portal CI 4615069 succeeds. Replay of 2,000 live API rows confirms the present hide-all consequence. These checks do not verify a timestamp pipeline.

[Draft PR #50](https://github.com/lfg-seth/snorr-meshlink/pull/50). [Firmware compatibility and source evidence](https://github.com/lfg-seth/snorr-meshlink/blob/fix/neighbor-signal-freshness/docs/operations/neighbor-signal-visibility.md#current-firmware-compatibility-check). [Original diagnosis](https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/neighbor-report-freshness-20261021.md).

Codex Windows compatibility-review claim released. No device, firmware, backend, schema or production change this review. Production fa03550. #43 layout remains deferred; Project reconciliation awaits authenticated CLI management host.

## Firmware dependencies captured — 2026-10-21

Owner requests separate corrective tickets; created [Fix gateway firmware neighbor timestamps for reliable signal expiry #51](https://github.com/lfg-seth/snorr-meshlink/issues/51) and [Fix repeater firmware neighbor timestamps across relay and backhaul delays #52](https://github.com/lfg-seth/snorr-meshlink/issues/52). Those tickets own firmware source, compatible shared report contract and separately authorized device rollout. This issue retains backend ingestion/provenance, visibility behavior and final two-hour end-to-end acceptance. Completion of the useful end-to-end fix is blocked by the source-timing capability in #51 and #52; decoder work may be prepared once their shared contract is agreed.

Ticket creation only: both firmware issues are Ready, unassigned and unclaimed, with explicit hardware-authorization boundaries. PR #50 stays draft and production stays unchanged.
<!-- END ORIGINAL ISSUE BODY -->

## Original comments

No comments at import.
