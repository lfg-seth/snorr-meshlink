# GitHub issue #4: Investigate INA219 current discrepancy with simultaneous same-path measurements

Immutable import evidence dated **2026-10-21 (America/Los_Angeles)**, retrieved 2026-10-22T01:33:06Z. This snapshot preserves the GitHub record at migration; it is not an active task queue. Historical instructions and claims below describe their original context. Use the repository's current tracker for later status and authorization.

- Source: [Investigate INA219 current discrepancy with simultaneous same-path measurements](https://github.com/lfg-seth/snorr-meshlink/issues/4)
- GitHub state: open; state reason: not supplied.
- Tracking label at import: `status:in-progress`.
- Labels: `bug`, `status:in-progress`, `area:hardware`, `priority:high`.
- Assignees: lfg-seth.
- Author: lfg-seth.
- Created (UTC): 2026-10-17T20:09:55Z.
- Updated (UTC): 2026-10-21T20:49:38Z.
- Closed (UTC): not closed.
- Milestone: [#1](https://github.com/lfg-seth/snorr-meshlink/milestone/1).
- Comments preserved: 0 of 0 reported by GitHub.

## Original issue body

<!-- BEGIN ORIGINAL ISSUE BODY -->
## Outcome

R004's amp-scale symptom is reproduced and narrowed to the INA219's own shunt-voltage conversions. Correct config/calibration and stable held-register reads rule against a current-scale/unit conversion error in the captured cases. Physical input/wiring/interference or sensor/module fault remain unresolved; actual amp-scale current is not established.

## Acceptance criteria

- [ ] Confirm complete physical sensor/shunt/wiring and supply/load paths. Owner confirms installed R100 and battery → INA219 → board; polarity/ground/other branches remain unconfirmed.
- [ ] Capture simultaneous series current, shunt voltage and sensor output under the same battery-only conditions; record uncertainty.
- [x] Capture raw shunt/current/config/calibration registers using explicitly authorized diagnostics.
- [x] Narrow the cause from evidence; retain signs/channels and avoid arbitrary correction factors. This is diagnostic narrowing, not an accuracy fix.

## Evidence — 2026-10-21

[Published audit and exact image hashes](https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/ina219-audit.md#r004-reinvestigation--2026-10-21), project commit [330573d](https://github.com/lfg-seth/snorr-meshlink/commit/330573d), [firmware diagnostic review](https://github.com/lfg-seth/firmware/pull/2).

- Existing firmware reports −1,152.6 mA; diagnostic reports still reach roughly −1.4 A. Correct config/calibration `399f/1000`.
- Six held conversions × three reads are individually identical and have exact current/shunt multiplication, while separate conversions imply +1.24 to −1.50 A with R100. Raw values precede portal conversion.
- R004 runs `rak4631-ina219-debug` / `2.7.26.09d8a9d`, with complete original identity/keys/channels/local/module profile independently preserved. Device/environment 900 seconds, power telemetry disabled, battery INA address unset.
- Existing actual-source conversion/transport harness passes at multipliers 1 and 10; both target builds pass. Hardware accuracy remains unverified.

## Active zero-input follow-up — 2026-10-21

Owner confirms the −11.1 to −11.3 mA / approximately −1.12 mV trace was recorded with battery disconnected and USB retained. This resolves the earlier physical-state uncertainty for that trace.

Owner proposes bridging INA219 VIN+ to VIN−, with battery still disconnected and USB/INA219 powered. Subsequent transition capture gives fresh matched current replies of 0.0, −0.3 and −0.1 mA. Four held triples remain individually stable at −0.02 to +0.02 mV with exact current arithmetic. **Physical bridge application is still awaiting owner confirmation**; do not attribute the change to the bridge yet. [Published follow-up](https://github.com/lfg-seth/snorr-meshlink/commit/894f892), [audit](https://github.com/lfg-seth/snorr-meshlink/blob/main/docs/operations/ina219-audit.md#battery-removed-confirmation-and-input-bridge-check).

Next: confirm bridge state, then compare bridge-on/bridge-off with battery still disconnected. Physical shunt millivolts, exact wiring/other branches and loaded accuracy remain unverified. No correction factor is applied.

Codex Windows desktop session retains this bounded claim explicitly awaiting the owner's bridge-state reply. Serial is closed. Unchanged diagnostic `2.7.26.09d8a9d` again passes full owner/local/module/channel equality. No new flash, saved profile change or other-board action. Owner's R004 diagnostic authorization remains in scope. Derived Project reconciliation remains pending authenticated GitHub CLI, unavailable on this desktop.

<!-- END ORIGINAL ISSUE BODY -->

## Original comments

No comments at import.
