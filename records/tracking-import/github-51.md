# GitHub issue #51: Fix gateway firmware neighbor timestamps for reliable signal expiry

Immutable import evidence dated **2026-10-21 (America/Los_Angeles)**, retrieved 2026-10-22T01:33:06Z. This snapshot preserves the GitHub record at migration; it is not an active task queue. Historical instructions and claims below describe their original context. Use the repository's current tracker for later status and authorization.

- Source: [Fix gateway firmware neighbor timestamps for reliable signal expiry](https://github.com/lfg-seth/snorr-meshlink/issues/51)
- GitHub state: open; state reason: not supplied.
- Tracking label at import: `status:triage`.
- Labels: `bug`, `status:triage`, `area:firmware`.
- Assignees: none.
- Author: lfg-seth.
- Created (UTC): 2026-10-21T22:03:50Z.
- Updated (UTC): 2026-10-22T01:03:24Z.
- Closed (UTC): not closed.
- Milestone: none.
- Comments preserved: 0 of 0 reported by GitHub.

## Original issue body

<!-- BEGIN ORIGINAL ISSUE BODY -->
## Approach under review — 2026-10-21

Owner questions whether absolute timestamps are necessary and asks about not storing stale readings and simpler alternatives. The timestamp-specific acceptance criteria below are the initial proposal, not an approved design requirement. Compare existing SNNS relative ages/boot/sequence evidence, excluding cached standard tables from current signal state, source expiry and dropping stale queued neighbor reports on reconnect. The current custom collector already expires entries after thirty minutes using monotonic uptime. Preserve raw archive/history; normalizing a new table receipt must not reintroduce an old link. Relative receipt-based expiry alone cannot bound unseen delivery delay; test buffering/replay before claiming the two-hour hearing limit. No alternative is selected and no implementation/flash is authorized by this discussion.

## Problem and outcome

G001/G002 can publish a new standard neighbor table containing stale entries, making B002/G001 appear recent despite owner-confirmed isolation. Current custom SNNS v1 reports hearing age, boot ID, sequence and uptime, but no source hearing/encoding epoch. Router broadcast processing overwrites packet rx_time after encoding; it must not be assumed to be a universal source creation clock.

Provide trustworthy source timing in gateway neighbor reports so portal #47 can retain fresh signals and hide signals at two hours without refreshing their age on receipt.

## Scope

G001/G002 HELTEC_V3, dedicated heltec-v3-gateway target; last verified firmware 2.7.26.9d2fd8f. Coordinate a shared versioned timing contract with the [repeater firmware ticket #52](https://github.com/lfg-seth/snorr-meshlink/issues/52). Preserve relative ages and report identities, existing reception filters/cadence, CLIENT role, LoRa TX disabled and local MQTT reporting. Preserve forwarding of repeater source timing as payload data, independently of gateway receipt clocks.

## Acceptance criteria

- [ ] Define and document a bounded, versioned report extension carrying a source hearing timestamp or source encoding timestamp tied to the existing hearing ages, with explicit clock validity/quality. Define precision, rounding and clock-change behavior; invalid/unsynchronized clocks remain unknown.
- [ ] Stamp timing at the reporting source and preserve it through local routing, MQTT buffering/reconnect and forwarding. Do not substitute broker receipt, ingestion time or a forwarded packet's rx_time for hearing time.
- [ ] Preserve current RSSI validation and valid zero SNR/hearing-age semantics, boot/sequence/counts, bounded packet/table behavior and passive collection. A periodic standard table or unchanged observation must not establish new hearing activity.
- [ ] Add actual encoder/module regressions for fresh and old entries, unknown/future/stepped clocks, reboot/uptime rollover and delayed/duplicate delivery. Verify compatible interpretation alongside legacy SNNS/standard reports through #47; legacy unknown-time reports must not become fresh.
- [ ] Build the dedicated gateway target, publish reviewed source on the authorized firmware branch with reproducible artifacts/checksums, and pin the published source through the project submodule. Do not reset or clone device profiles.
- [ ] When hardware rollout is separately authorized, identify/back up each gateway, independently verify preserved identity/keys/channel/Wi-Fi/MQTT/telemetry and LoRa TX disabled through reboot, then record fresh and deliberately delayed report evidence with #47. Separate build, flash, RF/MQTT receipt and portal results.

## Dependencies and evidence

Portal ingestion/display and final two-hour end-to-end acceptance remain in #47 / draft PR #50; do not close that issue merely because firmware builds. Coordinate the same payload contract with #52; no member firmware change is implied.

[Measured B002/G001 diagnosis](https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/neighbor-report-freshness-20261021.md). [Firmware compatibility/source evidence](https://github.com/lfg-seth/snorr-meshlink/blob/fix/neighbor-signal-freshness/docs/operations/neighbor-signal-visibility.md#current-firmware-compatibility-check). [Gateway build/profile record](https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/g002-neighbor-gateway.md). [Flashing handoff](https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/board-flashing-handoff.md).

## Authorization and status

Owner requests ticket creation on 2026-10-21. Ready means a bounded corrective follow-up, not an active implementation claim or rollout authorization. Capture only in this session; no firmware edits, builds, flashing, configuration changes or deployment. Claim separately when selected; hardware actions need explicit board scope.
<!-- END ORIGINAL ISSUE BODY -->

## Original comments

No comments at import.
