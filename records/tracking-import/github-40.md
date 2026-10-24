# GitHub issue #40: Diagnose missing production node updates

Immutable import evidence dated **2026-10-21 (America/Los_Angeles)**, retrieved 2026-10-22T01:33:06Z. This snapshot preserves the GitHub record at migration; it is not an active task queue. Historical instructions and claims below describe their original context. Use the repository's current tracker for later status and authorization.

- Source: [Diagnose missing production node updates](https://github.com/lfg-seth/snorr-meshlink/issues/40)
- GitHub state: open; state reason: not supplied.
- Tracking label at import: `status:verify`.
- Labels: `bug`, `area:backhaul`, `status:verify`, `area:portal`.
- Assignees: none.
- Author: lfg-seth.
- Created (UTC): 2026-10-21T02:37:50Z.
- Updated (UTC): 2026-10-22T01:06:23Z.
- Closed (UTC): not closed.
- Milestone: none.
- Comments preserved: 4 of 4 reported by GitHub.

## Original issue body

<!-- BEGIN ORIGINAL ISSUE BODY -->
## Observed behavior

Owner reports missing production node updates on October 20. Both independent portal/MeshMonitor streams stop at 20:19:33 Pacific October 19, before today's application deployment.

## Confirmed failure and current recovery

After owner connects gateways/debug sniffer, G001 is receiving mesh traffic with roughly 85,723 seconds console uptime but logs `MQTT not connected, queue packet` and `MQTT queue is full, discard oldest`. This establishes gateway-uplink failure and loss of older buffered packets; underlying Wi-Fi/session trigger is unknown.

G002 resumes publishing after recent boot at 19:44:44.367 Pacific October 20. G001 restarts during ordinary serial API inspection (default USB control-line reset is plausible, not established), then resumes delivery at 19:47:00.592. No reboot command, saved configuration write, flash or broker change issued. Final readback uses inactive DTR/RTS before opening and confirms both Wi-Fi/MQTT connected, exact preserved local/module/channel profiles and expected firmware/settings.

Original archive check now passes: 3,775 records, two new receipts, 200 verified envelopes, zero pending queue. Fresh B001/B002 GPS fixes and both-gateway receipts pass. Both gateway own reports and R001/R002/R003/R004 receipts resume. R005 has no new report in the short checkpoint; not declared offline. Independent sniffer has 12 decoded receptions/six duplicates over 65.101 seconds, with no gap event/session error.

## Remaining verification

- [ ] Identify original disconnection trigger and automatic reconnect behavior during a captured recurrence, separating Wi-Fi loss from MQTT failure before a reset.
- [ ] Verify sustained fresh per-gateway delivery/outage recovery; confirm fresh R005 receipt during its reporting interval when powered.

## Evidence and handoff

[Sanitized diagnosis and recovery](https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/node-update-outage-20261020.md#connected-gateway-follow-up-and-recovery), published in [12e4409](https://github.com/lfg-seth/snorr-meshlink/commit/12e4409). Prior diagnosis b112885 remains historical evidence.

Codex Windows claim released to Verify. All serial sessions closed; private raw/profile/location evidence remains ignored. No permanent fix, sustained freshness or field acceptance claimed. Derived Project reconciliation remains pending authenticated management-host CLI access.
<!-- END ORIGINAL ISSUE BODY -->

## Original comments

### Comment 6321880999

- Source: [comment 6321880999](https://github.com/lfg-seth/snorr-meshlink/issues/40#issuecomment-6321880999)
- Author: lfg-seth.
- Created (UTC): 2026-10-21T17:08:30Z.
- Updated (UTC): 2026-10-21T17:08:30Z.

<!-- BEGIN ORIGINAL COMMENT 6321880999 -->
Codex Windows session 2026-10-21 claims owner-requested G002 Wi-Fi replacement and short connection verification. Attached COM6 independently identifies G002 !849ad7a0 on expected 2.7.26.9d2fd8f; complete profile privately backed up. Changing only network credentials; sustained reconnect/root-cause verification remains separate.
<!-- END ORIGINAL COMMENT 6321880999 -->

### Comment 6321936876

- Source: [comment 6321936876](https://github.com/lfg-seth/snorr-meshlink/issues/40#issuecomment-6321936876)
- Author: lfg-seth.
- Created (UTC): 2026-10-21T17:11:11Z.
- Updated (UTC): 2026-10-21T17:11:11Z.

<!-- BEGIN ORIGINAL COMMENT 6321936876 -->
G002 owner-requested Wi-Fi replacement complete on verified COM6 !849ad7a0 / unchanged 2.7.26.9d2fd8f. Complete independent profile comparison passes with only supplied network fields changed; identity/keys, channels, TX-disabled radio, neighbor and MQTT settings preserved. Console observes IP acquisition, MQTT connected and queued publish. Serial closed. Sanitized evidence/capture limits published in 315a74a: https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/g002-neighbor-gateway.md#wi-fi-replacement--2026-10-21 . Credentials remain private. Releasing Windows session claim to Verify; fresh production ingestion, sustained delivery and original reconnect failure remain unverified. Project reconciliation pending authenticated CLI access.
<!-- END ORIGINAL COMMENT 6321936876 -->

### Comment 6330135258

- Source: [comment 6330135258](https://github.com/lfg-seth/snorr-meshlink/issues/40#issuecomment-6330135258)
- Author: lfg-seth.
- Created (UTC): 2026-10-22T01:04:20Z.
- Updated (UTC): 2026-10-22T01:04:20Z.

<!-- BEGIN ORIGINAL COMMENT 6330135258 -->
Codex Windows session claims owner-requested second G002 Wi-Fi replacement and short saved-profile/connection verification, 2026-10-21. Scope is attached G002 only with supplied credentials; preserve firmware, identity/keys, radio, MQTT and five-minute telemetry. No sustained outage/reconnect acceptance or other board change implied.
<!-- END ORIGINAL COMMENT 6330135258 -->

### Comment 6330162919

- Source: [comment 6330162919](https://github.com/lfg-seth/snorr-meshlink/issues/40#issuecomment-6330162919)
- Author: lfg-seth.
- Created (UTC): 2026-10-22T01:06:20Z.
- Updated (UTC): 2026-10-22T01:06:20Z.

<!-- BEGIN ORIGINAL COMMENT 6330162919 -->
Second owner-requested G002 Wi-Fi replacement completes on 2026-10-21 Pacific. COM6 independently identifies HELTEC_V3 !849ad7a0 / unchanged 2.7.26.9d2fd8f. New private full backup and exact independent post-restart comparison pass: only network Wi-Fi SSID differs; supplied password already matches. Keys/channels, MQTT, CLIENT/LoRa TX disabled, neighbor collector and enabled 300-second telemetry preserved. Retained console captures IP acquisition, MQTT connected and publication activity. Serial closed; no flash/reset/other-board/server/application change. Evidence committed and pushed to origin/main as 87d2422: https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/g002-neighbor-gateway.md#clifford-int24-wi-fi-update---2026-10-21 . Credentials/raw profiles remain private. Release Windows session claim to Verify; independent broker/production receipt, original outage trigger and sustained reconnect checks remain unverified. Derived Project reconciliation pending authenticated management-host CLI.
<!-- END ORIGINAL COMMENT 6330162919 -->
