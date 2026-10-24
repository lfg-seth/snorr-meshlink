# Device-card battery summary — LOCAL-8

2026-10-24. Owner activates the [canonical request](../../records/wishlist.md#device-card-battery-summary-without-duplicate-sensor-readings)
for frontend implementation. Source was prepared on `codex/local-8-battery-summary`
from `origin/main` at `520fbfc`; the subsequently authorized 0.1.2 deployment
is recorded below.
The original checkout and its unrelated hardware edits remain untouched.

## Card presentation

One shared [summary](../../portal/src/BatterySummary.tsx) appears near the top
of member details (Map and Users), repeater/router map cards, gateway map cards
and the selected Infrastructure detail. It shows estimated percentage, device
battery voltage, charging/discharging state and one current value. Member GPS
quality sits to the right of percentage; its header battery icon stays present.
The icon retains its existing reported-percentage semantics, distinct from the
profile-based voltage estimate. Missing values remain Unknown.

The entire Sensor voltage & current section is removed, including on equipped
devices. The history detail no longer repeats current, percentage or last voltage;
graphs, period controls and exact voltage-history tables remain. Temperature,
humidity, relationships, placement, solar, warnings and configuration controls
are preserved. GH-44's conditional sensor-section retention is superseded by
LOCAL-8's complete removal; GH-45's percentage/GPS placement is included.
Historical imported issues stay unchanged. LOCAL-7 and page redesigns are outside
this change.

## MeshLink 0.1.2 deployment - 2026-10-24

Owner explicitly authorizes merging PR #60 and production deployment. Final-head
Portal CI and Project record checks pass before merge **`6ac0937cca47d9a1c8e0ebc2a12c77c52836e962`**.
Release metadata and changelog advance together to **0.1.2** in
**`359e6ba237d74d23ead5b9c2d88081604447c197`**, pushed to main and identified by
immutable annotated **`meshlink-v0.1.2`**. The separate SNORR Firmware version
and installed radio profiles are unchanged.

### Same-commit checks and promotion

- Clean Git source at `/opt/meshlink-release-local8-359e6ba` passes **75 backend
  tests**, **60 portal tests**, TypeScript and the live build on Node 22.23.1.
  The release has no backend source or migration difference from the previous
  deployed `a405987`; installed migration files match. Local documentation,
  whitespace and portal checks also pass. Existing large-bundle warning remains.
- Main and release-tag [Portal CI](https://github.com/lfg-seth/snorr-meshlink/actions/runs/40125091486)
  and [Backend CI](https://github.com/lfg-seth/snorr-meshlink/actions/runs/40125091349)
  pass. Tag/source publication is followed by the separately requested manual
  promotion, rather than an automatic production rollout.
- Promotion holds `/run/lock/meshlink-deploy.lock`, retains rollback at
  `/opt/meshlink-rollback-local8-359e6ba`, publishes hashed assets before the
  atomic index switch and retains earlier assets for open tabs. Backend/portal
  source and root release metadata match the checked source. Remove the retired
  `PowerReadings.tsx` source file; preserve installed verification helpers and
  one-off migration records.
- While workers/APIs are stopped, exact hashes of both databases, worker queue,
  private credentials and `/etc/meshlink` remain unchanged. Eight cached
  current/raw pairs retain their values and source clocks through the switch.
  No schema operation, packet replay, configuration or radio change occurs.
- All **ten** build files match loopback and public HTTPS. `/version.json`
  identifies **0.1.2 / 359e6ba**, live mode and `trackedChanges: false`.
  Public index SHA-256:
  `61a5bfdf23a18f8c0a4025df867437e53d0e5ec5f93670f99a471792dd151ae2`.
  All six services are active; after backup recovery, three fresh archive
  receipts arrive, the newest 200 envelope records validate and the queue is empty.

### Card verification

Authenticated loopback state is projected into the actual deployed components
without names, coordinates or raw tracks. All **nine infrastructure devices and
one member** pass percentage/voltage/current selection and single-summary checks.
Four cards have measured sensor-path current, six correctly show Unknown, and
both humidity-bearing cards retain their readings. This verifies current API
data against the installed source, not an authenticated native live-map session.

The public production demo is visually checked at desktop **1280 × 720** and
mobile **390 × 844**: member percentage/GPS alignment and retained header icon,
repeater measured current, gateway unknown current, two-column wrapping and
scrollable dialogs. Infrastructure detail has exactly one summary, no sensor
section, retained temperature/humidity, graph and configuration controls. Browser
HTML metadata identifies the intended source/version. Backup quiescing briefly
shows retained/offline readings; normal live/demo feed recovers afterward.
Synthetic screenshot evidence is retained under ignored
`local-data/local-8-worktree/local-data/production-*-*.png` in the original checkout.

### Backup and recovery evidence

Normal state/static backups remain root-private in `/var/backups/meshlink`:

| Phase | Archive | SHA-256 |
| --- | --- | --- |
| Before | `meshlink-20261024T192348Z.tar.gz` | `08714e525b111aa75bdb8c6e4f9ccee549697f8ea28965b356bfb21e1669b2bc` |
| After | `meshlink-20261024T192815Z.tar.gz` | `27bae5a9e4f88acaacaf398a4550ce0b67ecadadb622316dff121b75e289f99b` |

The task also retains complete archives with matching portal source, root
version metadata and source identity in the release directory:

| Archive | SHA-256 |
| --- | --- |
| `pre-complete-backup.tar.gz` | `d141600f3dc2551a85743b827b856c17cb575f16cb3c85e676a4caedaabba3f4` |
| `post-complete-backup.tar.gz` | `69a4e731d5fb7b3191088c93315492a8a77c58ba14e1bdba476913417e97bef5` |

Both phases pass isolated live/demo database integrity, credential/record/history
and API recovery, proxy/authentication throttling and live/demo token/OS isolation.
Complete archive database bytes match the normal verified backups; source
identity and the post-release static manifest match the release.

The installed live verifier initially fails its fixed two-member/B001+B002
assumption after the owner's separate B001 decommissioning. A task-local
`verify-live-provisioned.py` compares exact member/infrastructure identities to
the backup database, retains gateway-mapping coverage and verifies those same
identities after restore. The installed helper is preserved. The existing
task-local bounded demo verifier checks exact newest **50,000 of 68,643** samples
and correct truncation after release; no history is deleted and GH-39 remains
open. Logs and helper copies remain private in the release directory.

Production source/card rollout is complete. Owner-phone authenticated native
acceptance, calibration/whole-battery accounting and installed recovery-verifier
maintenance remain separate follow-ups. These backups share the LXC disk;
off-host disaster recovery remains the existing GH-7 gate.

## Measurement selection

- Battery voltage continues to come from `DeviceMetrics.voltage`, normalized as
  `battery`, and projected as infrastructure `battery` or member `batteryVoltage`.
  Sensor bus voltage never replaces it. Existing EVE/LiPo profile curves and
  percentage rounding are reused without modification.
- [Adapter](../../backend/mqtt_adapter.py) and
  [state projection](../../backend/pb_hooks/meshlink.js) keep environment current
  (`sensorCurrentMa`) separate from power channels (`powerNCurrentMa`). Ordinary
  INA219 firmware's documented output is channel 1; see the
  [R006 acceptance](ina219-audit.md#local-power-only-acceptance). The presentation
  selects channel 1 only when it is the sole reported power-current channel,
  preferring it over the legacy environment current to eliminate duplicates.
  With no power-current channels, a single environment current can be shown.
  Other/multiple channels, duplicate metric entries and nonfinite current remain
  Unknown. There is no selection by array order, sign, magnitude or bus voltage.
- Displayed current is explicitly **measured sensor-path current**, with source
  and unverified battery-flow/calibration accounting visible. It is not promoted
  to a confirmed whole-battery measurement. The old optional `batteryCurrentMa`
  frontend field had no producer in the inspected state API; it no longer drives
  card interpretation.
- Direction from measured current requires the API's explicit
  `currentConvention: "positive-charging"`. This is the
  [owner-confirmed, deployed convention](radio-report-ingestion.md#fleet-current-polarity-correction---2026-10-24),
  already normalized by [telemetry projection](../../backend/pb_hooks/telemetry.js).
  The frontend never inverts again. Positive/negative/zero display as
  Charging/Discharging/Steady **(sensor path)**. Unmarked signs do not establish
  charge direction. Current keeps its sign, one decimal and mA; voltage uses
  three decimals and V.
- Without confirmed measured direction, the existing battery-voltage trend may
  supply an explicitly labeled **voltage estimate** of direction. Its age comes
  from the latest valid history sample, not the newest device contact. It never
  supplies mA. Sparse history produces Unknown; member data has no current or
  voltage-history source in this contract, so those fields remain Unknown.
- Battery voltage and current use their own measurement clocks and receipt
  fallbacks, cadence and missing thresholds. Fresh GPS/contact/temperature never
  refreshes them. Old measurements retain stale labels even after a new receipt;
  feed outages mark retained readings historical. Unknown cadence stays unknown.

No adapter, ingestion, API projection, database/history, radio or live device
configuration is changed. Multi-channel battery-path mapping and physical
calibration remain separate prerequisites for stronger battery-flow claims.

## Initial implementation checks

- `python scripts/check-project.py portal`: **60 tests pass**, TypeScript and
  production build pass on Node 22.23.1. Existing large-chunk build warning remains.
  Focused tests cover complete-section/duplicate removal across repeater/gateway
  details, member integration, retained environment/history/configuration, missing
  values, stale and offline data, receipt fallback, zero, both current directions,
  unmarked polarity, arbitrary/ambiguous channels and labeled voltage estimates.
- In-app browser visually verifies actual components with synthetic readings at
  desktop **985 × 782** and mobile **390 × 844**: two-column wrapping, member
  percentage/GPS alignment, header icon, repeater current and missing/offline
  gateway. Mobile scroll retains the header and exposes all summary fields.
  The preview uses ignored local fixtures; it does not access live telemetry.
- These initial source checks preceded merge/versioning and the separately
  authorized production release recorded above. Native authenticated live/owner
  phone acceptance and calibrated whole-battery flow remain separate gates.

2026-10-24 follow-up: the installed recovery-verifier device-count and bounded
history assumptions are now corrected and both installed live/demo recoveries
pass. [Maintenance evidence](backup-recovery-verifiers.md). The earlier
release-time task-local checks above remain historical evidence.
