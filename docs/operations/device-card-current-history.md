# Device-card INA219 current history

2026-10-24. Owner requests a current graph on INA219-equipped device cards,
a 30-minute average and 30-minute/6-hour options on both current and voltage
graphs. Source is prepared on `codex/device-current-history` from `origin/main`
`198507e`. Production deployment remains a separately selected step.

## Presentation and measurements

Repeater/backhaul map sheets and selected Infrastructure detail show a current
graph when channel-1 or legacy environment current is reported or its cadence
is configured. Unequipped devices retain their voltage graph without an empty
current panel. The current card summary and graph use the same source: the
sole power-current channel must be channel 1; otherwise, legacy environment
current is allowed only when no power-current channels are present. Unmapped
or multiple power channels produce no selected history or average.

Both graphs offer **30min / 6hr / 24hr / 7day / 30day**, with 24 hours remaining
the default. Short ranges label the horizontal axis in local hours/minutes.
Each graph has independent controls. Curved interpolation keeps outage gaps
disconnected; zero, negative and positive current remain visible, and isolated
readings appear as points. Unknown current cadence never implies continuity.

The separate **30-minute average** is the arithmetic mean of unique readings
in the latest 30 minutes, independent of the graph range. The displayed sample
count makes its basis explicit. It does not fill missing intervals or estimate
current from battery voltage. Empty, incomplete or expired history displays
Unknown; offline/error states and stale measurements remain labeled. History
refreshes once a minute, and an old response's average expires after one missed
refresh rather than being presented as a current window indefinitely.

Current remains measured sensor-path current, with whole-battery accounting
and calibration unverified. The API applies the existing positive-charging
convention once: raw negative becomes displayed positive, raw positive becomes
displayed negative, and zero stays zero. The frontend does not invert again.
Source evidence and radio configuration are unchanged. Member sensor ingestion
remains outside the existing supported contract; no current is fabricated for
member cards that have no sensor readings.

## API and retention

The authenticated, human-account-only
`GET /api/meshlink/current-history/{id}?hours=0.5|6|24|168|720` reads existing
observations for the selected infrastructure device. Worker/anonymous accounts
are denied. The voltage-history endpoint accepts the same five ranges.

Current queries use the selected metric only and include signed and zero
values without requiring battery voltage in that packet. Valid source time
determines the window; an absent source clock uses its original receipt time,
with timestamp quality and both clocks returned. A delayed measured packet is
not made current by its receipt. Gateway duplicates do not add samples; reports
sharing the same effective timestamp retain the newest receipt once.

Each history window is bounded to 50,000 readings with an explicit truncation
flag. A separate bounded 30-minute query supplies the average when the graph
range is longer; the half-hour range reuses its own result. Incomplete average
input yields Unknown. There are no database migrations, evidence rewrites,
configuration changes or production mutations.

## Verification and remaining gates

- Portal scope: **63 tests**, TypeScript and production build pass on Node
  22.23.1; existing large-bundle warning remains. Coverage includes all ranges,
  signed/zero samples, gaps, unchanged average across graph ranges, expiry,
  sensor absence, cancellation and stale response rejection.
- Backend integration covers source selection, polarity, zero, gateway
  deduplication, missing source clocks, all five periods, average independence,
  ambiguous channels, empty results, unchanged stored evidence and authorization.
  Both new API tests pass. Two full Windows runs each attempt **89 tests** with
  seven platform skips and one connection reset in different existing tests
  (simulation-control restart, then member short name). Both affected tests
  pass together in isolation; each also passes in the other full run. Preserve
  that local transport limitation; the PR's Linux backend CI remains required.
- Native in-app browser verifies actual components using fictional local
  telemetry: desktop 1280 × 720 and a 390 × 844 iframe viewport, independent
  short-range buttons, readable axes/average and scrollable mobile layout.
  Screenshots remain in ignored `local-data/current-history-worktree/local-data/`.

Next: review and merge the source, then select a versioned manual release with
the existing backup/recovery process. Authenticated deployed history and owner
phone acceptance remain unverified. Sensor calibration and runtime/field gates
are unchanged.
