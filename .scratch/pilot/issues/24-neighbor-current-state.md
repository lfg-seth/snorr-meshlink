# Correct current neighbor signals with relative age

Owner-selected GH-47 work, 2026-10-21, under the [local tracking trial](../../../docs/operations/local-tracking.md). This decision covers application ingestion and current signal presentation. GH-51/GH-52 supply related firmware evidence; their original absolute-timestamp proposals are not accepted requirements. Draft PR #50 remains an incomplete, undeployed checkpoint.

## Comparison and selection

| Approach | Useful behavior | Cost or limit |
| --- | --- | --- |
| Relative age on loaded history rows | Uses installed SNNS hearing age without a new payload or synchronized clocks | A new snapshot can renew receipt age; truncating the history response can discard the oldest anchor. Requires persistent hearing identity to avoid renewal. |
| Small persistent current-neighbor state driven by relative evidence | Retains each hearing's receipt anchor across polls, history limits and backend restarts; separates current presentation from raw reports | Requires private state and source ordering. Relative age still excludes delay before the worker's first receipt. |
| Expire source entries and stale transport queues | Can keep old snapshots out of the live path without UTC clocks | Installed source expiry is thirty minutes, but radio and gateway MQTT queue residence is unbounded. Every buffering path needs implementation and verification before a strict hearing-age guarantee. |
| Absolute hearing/encoding clocks | Can preserve original source age through long delivery delays | Requires clock acquisition, validity/step handling, payload changes and separate board rollout. It is an alternative, not a prerequisite selected here. |

Select **persistent current state using the installed relative evidence**. Standard NeighborInfo remains in history and never updates current signals. Keep the original worker receipt anchor for unchanged hearing; increasing report sequence or receiving the table again is not new hearing. New passive hearing evidence can update the current reading. Expire at two hours of reported hearing age plus elapsed time since the retained receipt. Never write a derived value into `observedAt` or call it measured UTC hearing time.

This directly addresses the [measured B002/G001 cached-table failure](../../../docs/operations/neighbor-report-freshness-20261021.md). Deleting old database history would not: a newly published standard table could reinsert the same stale link.

## Source evidence and delivery boundary

- [Installed collector](../../../firmware/src/modules/SnorrNeighborSignals.h): bounded 32-entry storage, eight rows per report, thirty-minute monotonic expiry, relative hearing age, observation count, boot/sequence and uptime. Uptime is `millis()/1000`; it wraps after about 49.7 days. Independent integer rounding can move a derived last-hearing uptime by one second between unchanged snapshots.
- [Installed standard table](../../../firmware/src/modules/NeighborInfoModule.cpp): per-entry hearing clock omitted; cached entries expire after twice the stored broadcast interval. [Official documentation](https://meshtastic.org/docs/configuration/module/neighbor-info/) describes periodic table publication and the default six-hour interval; installed source controls this pilot's exact behavior.
- [Gateway queue structure](../../../firmware/src/mqtt/MQTT.h) and [publication](../../../firmware/src/mqtt/MQTT.cpp): sixteen entries bound memory, but entries have no enqueue age or expiry. Reconnect can publish old snapshots. [Radio queue processing](../../../firmware/src/mesh/RadioLibInterface.cpp) can defer transmission for channel activity without a neighbor-specific residence cutoff.
- [Worker](../../../backend/mqtt_worker.py): captures `receivedAt` once and preserves it through its durable spool and API retries. Backend downtime after that receipt counts toward expiry. Clean MQTT sessions and retained-packet rejection do not bound all prior delivery delay; see the [MQTT 3.1.1 session rules](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718030).

The UI must call this an **estimated hearing age**. A report first received after an unseen long radio/MQTT delay can still look recent. The selected application fix must not claim a strict two-hour cutoff since actual hearing through outages. GH-51/GH-52 remain open local follow-ups for a verified transport-expiry design or separately selected source-time alternative. No firmware edits, builds, flashing or device configuration are implied.

## Verification and handoff

[Application behavior, checks and remaining acceptance](../../../docs/operations/neighbor-signal-visibility.md). Preserve raw archives, reports, observations and original receipt/source clocks. Source publication, deployment, fresh radio receipt, native presentation and field acceptance remain separate.
