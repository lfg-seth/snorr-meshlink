# GitHub issue #52: Fix repeater firmware neighbor timestamps across relay and backhaul delays

Immutable import evidence dated **2026-10-21 (America/Los_Angeles)**, retrieved 2026-10-22T01:33:06Z. This snapshot preserves the GitHub record at migration; it is not an active task queue. Historical instructions and claims below describe their original context. Use the repository's current tracker for later status and authorization.

- Source: [Fix repeater firmware neighbor timestamps across relay and backhaul delays](https://github.com/lfg-seth/snorr-meshlink/issues/52)
- GitHub state: open; state reason: not supplied.
- Tracking label at import: `status:triage`.
- Labels: `bug`, `status:triage`, `area:firmware`.
- Assignees: none.
- Author: lfg-seth.
- Created (UTC): 2026-10-21T22:03:53Z.
- Updated (UTC): 2026-10-22T01:03:28Z.
- Closed (UTC): not closed.
- Milestone: none.
- Comments preserved: 0 of 0 reported by GitHub.

## Original issue body

<!-- BEGIN ORIGINAL ISSUE BODY -->
## Approach under review — 2026-10-21

Owner questions whether absolute timestamps are necessary and asks about not storing stale readings and simpler alternatives. The timestamp-specific acceptance criteria below are the initial proposal, not an approved design requirement. Compare existing SNNS relative ages/boot/sequence evidence, excluding cached standard tables from current signal state, source expiry and dropping stale queued neighbor reports on reconnect. The current custom collector already expires entries after thirty minutes using monotonic uptime. Preserve raw archive/history; normalizing a new table receipt must not reintroduce an old link. Relative receipt-based expiry alone cannot bound unseen delivery delay; test buffering/replay before claiming the two-hour hearing limit. No alternative is selected and no implementation/flash is authorized by this discussion.

## Problem and outcome

RAK neighbor SNNS v1 reports contain relative hearing ages, boot/sequence/uptime and a thirty-minute collector expiry, but no absolute source hearing/encoding clock. On reception/relay, packet rx_time becomes a transport gateway clock. Delayed reports therefore cannot certify a two-hour hearing limit from their receipt timestamp.

Provide source timing that survives LoRa relaying and MQTT delays, allowing portal #47 to show valid current repeater observations and hide stale ones without inventing a hearing clock.

## Scope

R001–R005 RAK4631 reporters. Last ordinary released neighbor image is 2.7.26.0b65f2e; R004 separately runs diagnostic 2.7.26.09d8a9d for INA219 issue #4. Preserve that diagnostic branch/state and coordinate any later R004 rollout; this ticket does not authorize replacing it. Coordinate/reuse the shared versioned source-timing contract from [gateway firmware ticket #51](https://github.com/lfg-seth/snorr-meshlink/issues/51). Preserve passive direct-reception filtering, CLIENT bench operation, GPS/standard-report behavior, bounded reports, existing airtime/cadence gates, AHT compatibility and current sensor configuration.

## Acceptance criteria

- [ ] Implement the shared bounded, versioned payload extension with a source hearing timestamp or an encoding timestamp tied to per-neighbor hearing ages, retaining boot/sequence/counts and precision/clock-quality provenance.
- [ ] Define and test what happens with no valid time source, newly acquired/lost time, clock steps, reboot and monotonic-counter rollover. Unknown or untrustworthy time stays explicit; firmware must not fabricate an epoch from uptime or later gateway receipt.
- [ ] Source timing remains unchanged through relay hops, retransmission, duplicate gateway delivery and delayed backhaul/replay. Omitted/expired collector rows do not erase history or establish link failure; repeated table delivery does not refresh hearing activity.
- [ ] Add actual collector/module regressions for serialization bounds/versioning, legacy compatibility, fresh/old/unknown/future clock evidence, radio/airtime gates and delayed delivery. Preserve valid zero and negative signal values and bounded resource use.
- [ ] Build the selected RAK4631 target, publish reviewed source/artifacts/checksums on the authorized firmware branch, and pin the published source in the project. Reuse #51's shared implementation where applicable rather than defining a conflicting wire format.
- [ ] When board rollout is separately authorized, identify and privately back up each selected board; preserve identity/keys/channel/radio/sensor profile through independent reboot readback. Verify the report's original hearing timing through the required gateways with #47, including delayed/duplicate cases and visible expiry at two hours. Record rollout scope, actual receipts and remaining limits separately from source checks.

## Dependencies and evidence

Agree the common payload contract with [gateway firmware ticket #51](https://github.com/lfg-seth/snorr-meshlink/issues/51); either target's build alone does not complete the other. Portal ingestion/validation, historical-data handling and final display acceptance remain in #47 / draft PR #50. No B001/B002 firmware update is assumed: these radios can be observed by the reporting receiver.

[Firmware compatibility/source evidence](https://github.com/lfg-seth/snorr-meshlink/blob/fix/neighbor-signal-freshness/docs/operations/neighbor-signal-visibility.md#current-firmware-compatibility-check). [Existing RAK contract/build](https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/rak-neighbor-signals.md). [Bench rollout evidence](https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/repeater-gateway-check-20261019.md). [Flashing handoff](https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/board-flashing-handoff.md).

## Authorization and status

Owner requests ticket creation on 2026-10-21. Ready means a bounded corrective follow-up, not an active implementation claim or rollout authorization. Capture only in this session; no firmware edits, builds, flashing, device configuration or deployment. Claim separately when selected; authorize the exact boards before hardware actions.
<!-- END ORIGINAL ISSUE BODY -->

## Original comments

No comments at import.
