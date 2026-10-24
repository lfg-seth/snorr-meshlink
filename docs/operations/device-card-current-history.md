# Device-card INA219 current history

2026-10-24. Owner requests a current graph on INA219-equipped device cards,
a 30-minute average and 30-minute/6-hour options on both current and voltage
graphs. Source is prepared on `codex/device-current-history` from `origin/main`
`198507e`. The subsequently authorized 0.1.4 deployment is recorded below.

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

## MeshLink 0.1.4 deployment - 2026-10-24

Owner explicitly requests merging and deploying [PR #64](https://github.com/lfg-seth/snorr-meshlink/pull/64).
Final-head Portal/Backend/record CI passes before merge **`8b92f2e`**. Release
metadata and changelog advance together in **`91d0cedb1385c6cc718b1f36f9ecc8f444b0eed4`**,
published to main and immutable annotated **`meshlink-v0.1.4`**. The separate
SNORR Firmware version and all installed radio profiles remain unchanged.

- The exact clean release passes **89 backend tests**, **63 portal tests**,
  TypeScript and a live build on server Node 22.23.1, in isolated
  `/opt/meshlink-release-current-91d0ced`. All migration files match production;
  no migration runs. Main/tag [Portal CI](https://github.com/lfg-seth/snorr-meshlink/actions/runs/40140318190)
  and [Backend CI](https://github.com/lfg-seth/snorr-meshlink/actions/runs/40140318157)
  pass. This full Linux run resolves the local Windows transport-check limit.
- Promotion holds `/run/lock/meshlink-deploy.lock`, verifies a pre-release
  backup and isolated live/demo recovery before source replacement, and keeps
  prior source/metadata/static assets at
  `/opt/meshlink-rollback-current-91d0ced`. Publish hashed assets before the
  atomic index switch and retain old assets for open tabs.
- While both APIs/workers are stopped, exact hashes of live/demo databases,
  credentials, the worker queue and `/etc/meshlink` stay unchanged. No stored
  reading, assignment, configuration, key, packet or observation is rewritten.
- All **ten** build files match loopback and public HTTPS. Public
  `/version.json` and installed `SOURCE_COMMIT` identify **0.1.4 / 91d0ced**,
  live mode and `trackedChanges: false`. Public index SHA-256:
  `f9e5011e957dc63a7bb6d007bfbc5415602786be2d0eb2d9dd34f98eb73c2eac`.
- Authenticated production verification covers **45 current-history windows**
  (all five periods for all nine infrastructure devices) and both short voltage
  windows per device. Five devices select a supported measured-current source;
  every returned 30-minute mean/count agrees with the deduplicated source
  observations, including sign conversion. Unequipped/ambiguous devices retain
  empty current histories and Unknown averages. Ten additional demo
  current-history windows pass. Public authenticated current history and live
  state/feed pass through HTTPS.
- Post-release backup checksum, normal live/demo isolation, protected routes,
  per-client sign-in throttling and isolated database/API/history recovery all
  pass. All six services are active. Three new MQTT archive receipts arrive;
  the latest **200** envelopes validate and the queue is empty.

### Backup and rollback evidence

Normal archives and verification logs remain root-private on the LXC:

| Phase | Archive | SHA-256 |
| --- | --- | --- |
| Before | `meshlink-20261024T225142Z.tar.gz` | `ec22d921f6abc6847ee6e388482091b3b571173c290bd5f1648aab08fbb6f696` |
| After | `meshlink-20261024T225316Z.tar.gz` | `5cddb791ab4927cf8e3473799d973b70baf70c71db4b26ee97b6a80d86d3611e` |

`/root/current-history-20261024` retains the build manifest, protected hashes,
deployment/acceptance summaries, pre/post recovery logs and exact release-source
archive. Source archive SHA-256:
`56385ce6f9d8beaf4497afd93dc5b7d51557cd8fd25ee275ab023826bbeb1d01`.
Normal backups contain state, matching backend/deployment source and static
frontend; the source archive and rollback directory additionally retain portal
source and root release metadata. Backups share this LXC disk; existing GH-7
off-host recovery remains open.

Next: owner-phone authenticated native acceptance of the deployed cards. Native
responsive presentation was checked with fictional data before release; this
deployment verifies actual live data/API/static bytes. Physical calibration,
whole-battery accounting, runtime and field gates remain separate.
