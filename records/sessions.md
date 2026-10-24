# Session log

## 2026-10-24 - Selected R006 and gateway admin/cadence bench

- After PR #57 merges, owner explicitly authorizes flashing R006/G001/G002,
  using B002 for admin, preserving keys/profiles, keeping V3s receive-only,
  restoring intended settings and storing secrets in 1Password. One worker
  owns the [bounded bench](../.scratch/tasks/local-3-admin-bench.md). G002 is
  re-identified after its USB reconnect; MC00 and other boards are untouched.
- Install ordinary `rak4631` and dedicated `heltec-v3-gateway`
  **2.7.26.4c96b9b**, reviewed/published source
  **4c96b9ba0360f01752892a41d09ccacda82747bb**. Exact image/partition/hash,
  application-only write and independent original owner/security/channel/local/
  module comparisons pass through reboot. Gateway rebuild succeeds in 357.361
  seconds; use the prior exact reviewed RAK build. No new firmware source or
  published release asset/pointer, server deployment or map write.
- Actual R006 source SNNS gaps **195 / 315 / 315 / 195 / 915 / 195 / 195
  seconds** verify 180/300/900, retained cooldown on shortening, saved reboot
  and restored cadence. All seven measured reports match across gateway
  serial/MQTT paths. Each gateway contributes 39 own reports, with consecutive
  gaps 75–76 seconds within two observed boots. Record source clocks, host
  receipt gaps and boot/sequence identity separately.
- B002's existing stock V4/Python SDK 2.7.11 controller is unauthorized before
  temporary key enrollment, then supports encrypted read/change/readback.
  Two-second reboot attempts return session-key errors; a 15-second remote
  reboot successfully discards an uncommitted edit. A saved 900-second write
  returns an error ACK but independently survives a distinct reboot. Preserve
  failures and use result/boot readback; the precise transport cause and generic
  operator-tool compatibility remain unproven. No firmware fix is claimed.
- At 15:48:14 UTC, original R006 telemetry/security are restored through reboot.
  Separate final all-board comparisons pass; R006 device/power 180, environment
  off and empty admin allowlist, V3 TX disabled/local-only and individual network
  profiles, B002 stock firmware/profile unchanged. B002 is rejected again after
  restoration. All serial/subscriber handles close and temporary build mapping
  is removed. Nine concealed original/final profile/observer entries are verified
  in **SNORR MeshLink — Pilot**; raw evidence remains ignored/private.
- Validation: strict actual-receipt aggregation, 34 existing updater tests and
  ten release tests pass in the project environment; changed-record links and
  whitespace pass. Source extreme/rollover/
  airtime-gate tests and read-only review remain the prior software evidence;
  no physical rollover, calibrated power, battery soak, field/forced-relay,
  outage-age bound, independent RF silence or authenticated portal acceptance
  is inferred. [Exact images, measurements, failed/restored attempts and limits](../docs/operations/repeater-update.md#r006-and-gateway-admin-bench---2026-10-24),
  [TEST-006](field-results.md#test-006--saved-snns-interval-and-selected-controller-admin-bench).
- Publish sanitized root records on short-lived branch
  `bench/local-3-admin-cadence`; preserve unrelated untracked `3DModels/`.

Next required bench: a transmitting intermediate and proof excluding direct
reception for remote changes, interrupted/lost commands and restoration; resolve
operator-tool ACK/result handling before inaccessible placement. Continue the
independent software freshness/release assignments while bench/access gates wait.

## 2026-10-23 - Complete LOCAL-3 saved SNNS interval software

- Complete the bounded [saved-interval assignment](../.scratch/tasks/local-3-snns-interval.md)
  with one implementation worker and one read-only reviewer. Radio SNNS reads
  saved `telemetry.device_update_interval`, retaining RAK's 180-second fallback
  and minimum, safe saturation at 2,147,468 seconds, sampled jitter, outstanding
  cooldown, scheduler/startup, expiry/rotation, priority and airtime gates.
  Gateway local reports retain 60 seconds plus jitter and disabled RF TX;
  environment/power and standard NeighborInfo keep their separate settings.
- Publish reviewed firmware **`4c96b9ba0360f01752892a41d09ccacda82747bb`** by
  fast-forward to `origin/snorr/develop`; update the root source pin and
  profile/bench guidance on short-lived branch `feat/local-3-snns-interval`.
  The reviewer checks fixed diff `b23f09d5b..4c96b9ba0`, finds no actionable
  issues and independently repeats the sanitized behavioral matrix. No
  follow-up code changes are required.
- Validation: the actual module/real Throttle tests cover saved settings,
  extremes, changes, retained jitter, no catch-up, reboot reconstruction,
  rollover including zero and local/radio modes. Both fallback profiles and
  collector capacities pass ASan/UBSan; existing INA219 x1/x10 checks, 34
  updater and ten release tests pass. Ordinary `rak4631` and
  `heltec-v3-gateway` full builds pass on the committed source. Resolve the
  Windows gateway command-length failure with a temporary package-cache drive
  mapping and run final builds sequentially after shared output invalidation.
  Trunk is unavailable; configured clang-format 16.0.3, YAML/Python syntax and
  whitespace/link checks pass. [Evidence and build limits](../docs/operations/repeater-update.md#saved-snns-interval-software-verification).
- No board flashing, remote-admin provisioning, release manifest/artifact
  publication, production-pointer update or live deployment is performed.
  The harness stubs the scheduler boundary and reconstructs module state; real
  scheduler execution, flash persistence, admin transport/authorization and
  RF/MQTT/portal acceptance remain unverified. Preserve the unrelated image.

Next required bench step: explicitly select and identify a RAK and authorized
transmitting controller, preserve the complete private profile/keys, use an
independently verified selected image, then perform LOCAL-3 section-2 admin
read/change/readback, unauthorized-key rejection, save/reboot, relay/interrupted
command and both-gateway cadence checks; restore the intended profile. Freshness,
release, sensor accuracy, soak and deployment gates remain separate.

## 2026-10-23 - Accept agent-workflow restructuring for merge

- Owner requests merging [PR #56](https://github.com/lfg-seth/snorr-meshlink/pull/56)
  into main through a normal merge, preserving implementation **3ce31bd**.
  Mergeability passes and no review findings are present. The
  [Linux project-record check](https://github.com/lfg-seth/snorr-meshlink/actions/runs/40065582334)
  passes on that implementation: runner regression tests and changed-record
  links/whitespace. This does not establish the separate backend Linux release gate.
- This handoff adds only the merge acceptance record. Keep existing task states,
  hardware/live-access blockers and the unrelated untracked image unchanged.

Next useful step: select the saved SNNS interval assignment and prepare the
B001/B002 GPS/runtime plan from the tracker; bench execution still needs its
agreed devices, access and criteria.

## 2026-10-23 - Structure bounded agent assignments and repeatable checks

- Owner requests implementation of the agent-efficiency workflow. Keep the
  tracker as the only status queue; add Software/Bench lanes and focused next
  briefs for LOCAL-3 SNNS interval, GH-2 run preparation, LOCAL-4 power planning
  and LOCAL-6 release foundation. Partition parent criteria into independently
  verifiable assignment boundaries without marking implementation or hardware
  acceptance complete. Deferred work and imported GitHub records stay held.
- Reduce PROJECT.md from 29,760 to 5,812 bytes (80%); preserve the original prose
  and adjusted evidence links in
  [the historical brief](project-brief-history-20261023.md). README now points to
  canonical status rather than maintaining a dated status copy. Add the
  [assignment template](../docs/operations/task-template.md), resource ownership,
  scoped context/review rules and compact handoff to the existing local workflow;
  align machine-switch instructions and AGENTS.md using writing-for-agents.
- Add [check-project.py](../scripts/check-project.py) and
  [scope documentation](../scripts/README.md), reusing existing updater,
  firmware-release, portal and backend suites. Default docs checks validate
  changed/untracked inline local file/heading links and Git whitespace. Add
  runner regression coverage and a source-only project-record CI workflow.
- Validation: eight runner regression tests, 34 updater tests and ten pinned
  firmware-release tests pass. Changed-document links/whitespace and exact
  archive-content preservation pass; project-record CI YAML parses and its
  read-only check wiring validates. Initial Windows sandbox temp/submodule
  access and system-Python dependency failures are resolved using approved
  execution and the existing project environment. No application suite rerun,
  Linux CI result, live-system check, firmware build or hardware action claimed.
- Publication uses short-lived branch `docs/agent-workflow`; preserve the
  pre-existing untracked image. Source publication does not deploy the portal.

Next useful step: select
[the SNNS interval assignment](../.scratch/tasks/local-3-snns-interval.md) for
software implementation and
[the B001/B002 run-plan assignment](../.scratch/tasks/gh-2-run-plan.md) for the
next bench preparation; actual runs retain their hardware/access/criteria gates.

## 2026-10-23 - Settle repository name, manual deployments and public editorial policy

- Owner keeps `snorr-meshlink`, selects manual production deployments from
  reviewed main source and no staging site now. Update release operations and
  project direction; no remote rename is pending. Resolve GH-13's policy choice
  locally and park its unselected automation/staging implementation in Deferred.
- Owner wants most project material public and human-readable, expecting to
  copyedit most/all prose. Record the editorial policy in records/content.md and
  LOCAL-5: useful drafts, owner copyedit/review, approved publication through
  manual deployments. Inventory/operations content is eligible, not categorically
  hidden. Exclude agent internals and provisionally task/issue pages from the
  site; retain existing secrets/member/raw-location boundaries.
- Validation: local links and whitespace checks. Documentation only; no site,
  deployment, GitHub issue/Project or hardware changes. LOCAL-5 remains deferred.

Next useful step: continue the selected firmware/application work; activate
LOCAL-5 separately when ready to build the public documentation section.

## 2026-10-23 - Accept permanent local tracking, migrate firmware branch and version MeshLink

- Owner selects `snorr/develop` and commits to local tracking. Publish firmware
  commit **b23f09d5b** on that branch, update workflow/provenance validation and
  submodule branch/pin; all 10 release-tool checks pass. Keep the former remote
  branch as historical evidence; no firmware runtime change or hardware flash.
- Archive pre-acceptance main **0713f7e** at
  `archive/pre-local-tracking-20261023`; fetched main has no commits absent from
  the trial. Promote the accepted trial through a normal merge into main, retain
  historical trial/archive refs, and keep main tracking origin/main. Update
  agent/workflow/handoff instructions and disable automated GitHub tracking
  provisioning. Historical issues/Project remain intact.
- Implement independent MeshLink **0.1.0** using `meshlink-release.json`,
  CHANGELOG.md, package/lockfile/tag checks, generated portal version.json and
  HTML version/source metadata, plus main/tag CI. Version covers portal/backend
  source together; firmware versions remain separate. Document release/rollback
  and the distinction between portal metadata and actual backend deployment.
- Validation: 56 portal tests, typecheck/build, generated metadata/HTML checks,
  four workflow YAML parses, tracking schema and whitespace checks pass. System
  Python initially lacks dependencies; use the project virtual environment and
  add missing Windows tzdata there. Fix the repeated cutover-test database lock
  by explicitly closing its SQLite inspection connection; targeted check passes.
  Full backend Windows runs still show intermittent connection resets and skip
  seven POSIX-only tests. Hold the combined release tag pending clean Linux CI;
  no claim of an all-green backend suite or production deployment.
- Final publication: implementation **b876ab9**, normal main merge **25ef83b**,
  both pushed. This workspace now uses main/origin-main. A clean main build
  emits MeshLink 0.1.0, source 25ef83b and trackedChanges=false. Final Windows
  backend run: 74 tests, three connection-reset errors and seven POSIX skips;
  cutover cleanup passes. Keep the release tag pending Linux validation.
- GitHub metadata still identifies the project as `lfg-seth/snorr-meshlink`;
  repository rename has not occurred. Preserve origin until the actual rename.
  Existing untracked image is untouched. Use the writing-for-agents skill for
  permanent agent instructions.

Next useful step: confirm backend/Linux CI, then tag the accepted application
release; proceed with LOCAL-3/LOCAL-4/LOCAL-6 firmware work on snorr/develop.

## 2026-10-23 - Establish SNORR firmware 0.1.0 development baseline

- Owner selects 0.1.0 for the current state, without beta suffixes, and requests
  GitHub/project updates. Add [release index](firmware-releases/README.md) and
  [immutable baseline/changelog](firmware-releases/0.1.0.md) pinned to firmware
  source 5c2c1adad098eea1e4795158d19c9debe306eded, with last-verified fleet builds
  and linked checksum/profile evidence. No fresh device audit is implied.
- Update LOCAL-6, tracker and project brief: 0.1.1 fixes, 0.2.0 next development
  milestone, 1.0.0 first accepted production. Supersede beta.N/RC naming advice.
  Preserve child tickets and existing runtime versions, stock member images,
  diagnostic exceptions and publication/acceptance limits.
- Validation: release/parent links and Git whitespace. No firmware code, build,
  tag rewrite, flash or site deployment. GitHub publication is the authorized
  trial-branch record push; issues/Project board retain trial behavior.

Next useful step: implement product-version embedding and coordinated target
manifests for the next numbered development release under LOCAL-6.

## 2026-10-23 - Parent SNORR firmware release and fleet-version tracking

- Owner identifies the current phase as beta and requests a parent firmware
  ticket. Create [LOCAL-6](../.scratch/pilot/issues/28-snorr-firmware-releases.md)
  above LOCAL-3 RAK/shared firmware and LOCAL-4 gateway readiness; add reciprocal
  parent links and one tracker entry. Child implementation and hardware gates
  remain intact; shared SNNS timing still belongs to LOCAL-3.
- Recommend SNORR 1.0.0-beta.N, rc.N and production 1.0.0, with semantic version
  rules tied to an explicit compatibility contract. Dates/names are supplemental.
  Record separate upstream/source/target/checksum identity, profile revisions,
  immutable manifests, release notes and a verified per-device rollout ledger.
- Current mixed installed builds are not relabelled. Stock member trackers need
  explicit build/test inclusion before an all-node SNORR version claim; otherwise
  name the release infrastructure-only. No tag, firmware edit/build or flash.
- Validation: consult the SemVer specification, check new/parent links, tracker
  membership and Git whitespace. Existing untracked image remains untouched.

Next useful step: implement the release metadata/target-matrix foundation and
select the first coordinated beta's scope alongside child readiness work.

## 2026-10-23 - Scope gateway hardware readiness and public Markdown documentation

- Create [LOCAL-4](../.scratch/pilot/issues/26-gateway-production-readiness.md)
  with power characterization, four/eight 18650 alternatives, two 60 x 100 mm
  panels or external advertised 6 W/5 V USB solar, INA219, Muzi whip, enclosure
  CAD/print/fit/weather tests, gateway firmware and end-to-end acceptance.
  Record planned hardware without overwriting installed LiPo allocations.
- Move gateway-specific LOCAL-3 readiness and GH-40 remaining reconnect
  acceptance into LOCAL-4. Shared SNNS timing remains LOCAL-3; imported history
  and GitHub issues/Project remain unchanged. Source confirms a shared firmware
  tree but distinct Heltec ESP32-S3 and RAK nRF52840 build targets/binaries.
- Create deferred [LOCAL-5](../.scratch/pilot/issues/27-public-markdown-blog-wiki.md)
  for public Markdown blog/wiki, automatic content updates through site releases
  and illustrated pages per node type. Add hardware index and initial gateway
  source page; pictures, wiring/CAD and public site rendering remain pending.
- Validation: local link and whitespace checks. Documentation only; no
  implementation, purchases, prints, hardware/configuration changes or site
  publication. Wi-Fi power, solar yield, INA219 accuracy and autonomy remain
  unknown; advertised power is not a measurement.

Next useful step: identify actual gateway power components and agree a measured
energy/charging run before selecting the pack, solar option and enclosure.

## 2026-10-23 - Consolidate production firmware readiness before mountain redeployment

- Owner requests a ticket covering configurable SNNS timing and other firmware
  needs before placing RAK nodes back on the mountain. Create
  [LOCAL-3](../.scratch/pilot/issues/25-production-firmware-readiness.md), separating
  required changes, configuration acceptance, gateway prerequisites and physical
  deployment gates. Current source confirms compiled SNNS timing, standard
  remote-admin support, and gateway MQTT credential logging/insecure TLS.
- Consume local GH-51/GH-52 timing work, remaining GH-26/GH-27 acceptance and
  firmware release/rollout ownership into LOCAL-3. Preserve immutable imports,
  completed evidence and GitHub state. Keep R006 map/portal handoff current;
  retain INA219, utilization, reconnect and field/runtime tasks as dependencies.
- Specify the proposed device-telemetry interval coupling, minimum/fallback,
  preserved jitter/airtime behavior, remote key authorization checks and ordinary
  production images without diagnostic/dummy-load flags. Absolute timestamps
  remain an open choice; existing portal freshness behavior is not replaced.
- Validation: inspect pinned source and current operational records; check local
  ticket links, consolidation membership and Git whitespace. Documentation only:
  no firmware build, hardware action, remote command or deployment. Production
  readiness and physical power/current accuracy remain unverified.

Next useful step: implement/test LOCAL-3's configurable SNNS interval, then
verify remote administration on a selected bench controller/board; resolve the
shared freshness and gateway prerequisites before final release acceptance.

## 2026-10-23 - Prepare three-minute repeater rollout and reusable updater

- Owner requests all available repeater statistics every **180 seconds**, a
  prompt-driven firmware/configuration updater for R001–R006, and R006's map
  placement. Retain R001–R005's temperature/environment profile and R006's
  **INA219-only/no-temperature** exception. Exact site coordinates stay private.
- Build ordinary RAK source **`0634b775f65804968f5a18a7e8824db415556db2`**
  with the RAK-specific 180-second private SNNS baseline; standard NeighborInfo
  remains separate at 21,600 seconds with its existing 14,400-second minimum.
  Jitter, empty-report suppression, congestion and airtime gates still apply.
- Add the reusable updater, tracked sensor/identity profiles, pinned helper
  dependencies and download-only release selection. Full private profile/key
  backups, recorded USB/node/hardware matching, checksum/application-only UF2
  guards and complete independent post-reboot comparison protect each board.
  Thirty-four offline checks and Python compilation pass; no hardware is touched
  by those checks. [Procedure and rollout status](../docs/operations/repeater-update.md).
- Release CI/public download verification is pending and the production tag
  pointer stays unset. Add an explicit `--local-bundle` fallback, checked
  against the fixed tracked source/image manifest and staged privately with
  exact manifest/checksums/UF2/OTA files; `publishedArtifact: false` preserves
  its actual local-build provenance. R006's local three-minute firmware/profile
  acceptance now passes; other boards require individual physical connection. R006's
  map write is pending because server DNS is unavailable; no portal data has
  changed during this preparation.
- The first native R006 attempt used a 1200-baud touch, entered serial-only
  DFU on the same USB identity/COM26 and stopped before an application write
  because no UF2 volume appeared. Correct the updater to request DFU through
  the verified open Meshtastic API after complete backups; remove the touch.
  Six additional offline checks prove mode boundaries and backup/DFU/close
  ordering. Verified application-only serial OTA recovery completes with
  759,304 application bytes, no SoftDevice/bootloader bytes and `Device
  programmed` after 45.03 seconds.
- At **2026-10-24T00:51:19Z / October 23 17:51:19 Pacific**, the corrected full
  native Windows UF2 updater exits successfully on R006, ordinary
  **2.7.26.0634b77**, UF2 SHA256
  **0734127c43d85ef846caff0f161590183aea964268fcf8fdf1649142970cc9ba**.
  Full intended owner/key/channel/local/module configuration persists through
  explicit reboot: CLIENT, device/power 180 seconds, environment off, compiled
  SNNS 180 seconds and standard NeighborInfo 21,600 seconds. Serial closed;
  private gate is `private/bench/R006-local-0634b77-verified/finalverified-radio.json`.
  Independent comparison of original pre-failure profile against the
  corrected run's before-profile also passes, along with intended/final
  reboot equality: original full configuration, identity/keys and channels
  survive serial recovery. Private evidence is the same directory's
  `recovery-chain-verification.json`. R001–R005 remain unchanged and
  unconnected. Linux hardware, current calibration,
  battery-only behavior, runtime and field coverage remain unverified.
- Independent subscribe-only TLS MQTT capture records **three automatic
  nonretained cycles each of device, power and SNNS through both gateways**,
  nine source packets / 18 gateway copies after the final clock gate. Eligible
  receipts span **00:52:07.802–00:58:53.068 UTC**. Device and power measurement
  gaps are **180/180 seconds**; same-boot consecutive SNNS report gaps are
  **195/195 seconds**, including normal jitter/scheduling. Latest battery is
  4.164 V; INA219 channel 1 is 4.196 V / -0.2 mA; no environment packet.
  Overlapping observer copies are excluded. Authenticated portal ingestion
  and sustained/field acceptance remain separate. [Measurements/evidence](../docs/operations/repeater-update.md#r006-installed-verification).
- Firmware source/build and release tooling are pushed as **0634b775f**;
  external-app workflow-comment retry **5c2c1ad** is also published and pinned
  by this repository. Neither push starts the new Actions workflow; local
  build, sensor/neighbor/release checks and strict workflow lint pass. Public
  release publishing remains pending Actions investigation; no default-branch
  or repository-setting change is made. Add the reviewed manual R006 metadata
  migration, with coordinates kept private, for the server-access handoff.

Next useful step: when server access recovers,
apply/verify the private map placement
and portal cadence metadata with backup/recovery checks, and publish/verify
the exact release before setting the public production pin. Connect other
repeaters one at a time for the same updater and acceptance checks.

## 2026-10-23 - Prepare R006 with INA219-only production telemetry

- Owner assigns fresh assembly **R006** and requests production preparation
  with INA219 only/no temperature sensor. Build ordinary `rak4631` from clean
  published **09d8a9dbf**, retaining INA219 fixes/SNNS without diagnostic or
  dummy-load flags. Flash verified UF2 SHA256 **8429d164a70d9b3d7ef3d0f58d28c568dbe2cff51aa32ac6363071427314784e**;
  preserve node/hardware identity. [Manifest](../docs/operations/r006-production-image.json)
  and [full preparation/evidence](../docs/operations/ina219-audit.md#r006-production-preparation--2026-10-23).
- Independently verify the complete intended CLIENT/private-US-pilot profile
  through reboot: device and power telemetry **900 seconds**, environmental
  reporting disabled, neighbors enabled, GPS off and random-PIN Bluetooth.
  The formerly keyless UNSET profile creates its first PKI pair, which persists
  through reboot. Two fresh local power requests verify corrected **channel 1**.
- At **14:10:51 Pacific**, register R006 unlocated with no weather capability
  and unknown battery capacity/arrangement. Exact quiesced fingerprints preserve
  all old rows across 31 live/32 demo tables/schema; only R006 device/event/
  migration marker and provisioning/mapping/manifest changes are added. All
  other protected private files are preserved. Application **443ba03** stays
  deployed; no application or other-radio change.
- After final startup/clock setting, three unique automatic reports arrive
  through **both G001/G002**, with six retained gateway copies and correct
  accepted/duplicate outcomes. Device battery **3.882 V**, INA219 channel 1
  **3.856 V / −275.7 mA** and one SNNS neighbor report reach authenticated
  portal state. Device/power measurement clocks are valid; SNNS calendar
  hearing time remains unknown. Temperature/humidity absent; serial closed.
  This completes GH-5's remaining fresh power check; remove its local Verify
  entry without changing GitHub issues/Project.
- Complete pre/post backups pass isolated live and independent demo recovery;
  final archive **meshlink-20261023T211331Z.tar.gz**, SHA256
  **7730b6aa4f633cf0119c42e83921d92ba8f2a1ad18c1732807a8971555655f76**.
  The installed demo verifier hits known GH-39 bounded-history assumptions;
  private archived database/table/API-window/isolation verification passes
  without modifying that verifier or any history. All four services active.
- Validation: ordinary build/UF2-OTA payload checks, final full profile/PKI
  readback, actual local power replies, live isolated provisioning/deduplication
  and full recovery pass. Retained artifacts match the recorded manifest;
  applied provisioning source matches its tracked copy. Documentation links
  and whitespace checks pass. No sustained cadence/runtime, physical current
  calibration, native UI or field acceptance claimed.

Next useful step: choose an actual R006 site and record its battery assembly,
then observe repeated 15-minute delivery and battery runtime. GH-4's physical
same-path calibration/marking/polarity and R004 bridge confirmation remain
separate; startup acceptance does not establish field readiness.

## 2026-10-23 - Flash and test fresh INA219 assembly

- Owner brings a brand-new RAK19003/RAK4631 and INA219 inline with an 18650
  forward for troubleshooting and authorizes flashing/testing. Identify
  `!da581e5f` / default `1e5f`, USB `E9B12C5CA98FBCB8`; **R006 stays
  provisional**, without rename or portal registration. Record the new
  assembly without inferring purchases or stock totals.
- Record stock version **2.7.15.567b8ea** and privately back up complete configuration.
  Verify the existing diagnostic UF2 hash, match bootloader identity and flash
  **2.7.26.09d8a9d** without rebuilding/resetting. Independent version and
  post-restart intended-profile checks pass. Identity/security/channels
  survive; enable only environmental measurement, record five automatic
  firmware-upgrade setting differences, and retain region UNSET. R004 and
  other boards are untouched. [Detailed image/profile evidence](../docs/operations/ina219-audit.md#fresh-rak190034631-comparison--2026-10-23).
- Two USB-charging captures provide five fresh request-matched readings
  **−270.7 to −279.4 mA / 3.844–3.848 V**. Six initialized held conversions,
  each read three times, pass stability and exact current/shunt arithmetic
  with calibration **0x1000**, restored continuous configuration and no
  captured overflow/diagnostic I2C errors. Exclude one pre-initialization
  zero-calibration triple. The amp-scale symptom is absent; this is not an
  independent accuracy result. Owner's USB **280 mA / 5 V** is a different
  path. Raw evidence stays private and serial is closed.
- Update inventory, bench results, flashing handoff and GH-4's local next
  action. Physical shunt marking/polarity, same-path current accuracy and
  battery-only testing remain pending. No RF/MQTT/portal, runtime or field
  acceptance result; no firmware source/submodule or GitHub tracking change.
- Documentation verification: whitespace checks and all 303 relative file
  targets in changed records pass; new evidence heading/anchor resolves.

Next useful step: confirm the fresh shunt marking and VIN orientation, then
compare physical millivolts directly across the shunt and series battery
current with simultaneous diagnostic readings under unchanged USB charging.
Retain R004's separate pending bridge-state confirmation.

## 2026-10-21 - Deploy relative-age current neighbor signals

- Owner explicitly authorizes deployment. Release pinned trial source **443ba03** at **19:18:53 Pacific**, preserving concurrent LOCAL-1/LOCAL-2 wishlist records and leaving `main`, draft PR #50 and GitHub issue/Project status unchanged. The tracking trial is not accepted into `main`, and no general deployment-branch policy is selected. [Deployment evidence](../docs/operations/neighbor-signal-visibility.md#deployment---2026-10-21).
- Isolated server 74 backend/55 portal checks, TypeScript/live build and trial migrations on consistent live/demo copies pass. Back up and verify recovery before promotion. Quiesce both APIs/workers, retain rollback source/static/state, then explicitly migrate live and demo together. Exact fingerprints of all 19 live/20 demo pre-existing application tables and all 11 protected configuration/credential/queue files are preserved; current collections initially empty, with no history backfill or demo reset.
- Nine public asset hashes, live/public authentication and isolation boundaries, all six services, fresh MQTT archival and empty queue pass. Fresh SNNS from G001/G002/R003 creates ten useful current readings; null absolute hearing clocks and standard-table exclusion remain honest. Actual React renders of those readings pass offline estimated-age presentation and exact two-hour clock-advanced expiry. B002/G001's unchanged count-81 snapshots remain excluded; the pair becomes eligible only after newer source hearing/count-82 evidence. No independent physical-link or delay-bound claim.
- Pre- and post-release backups pass separate live/demo recovery. Additional isolated restore confirms all ten saved current readings and three observer frontiers preserve exact IDs, relative-age anchors and historical references. Keep archives, logs, manifests and rollback private on the host. No radio/firmware/configuration action or R004 diagnostic change. GH-47 remains Verify for native and sustained/outage acceptance; the unseen upstream delay limit remains GH-51/GH-52 work.

Next useful step: refresh the portal and verify native desktop/mobile neighbor presentation, then observe sustained expiry/outage behavior. Select and verify bounded source/queue work before claiming a strict two-hour hearing limit through upstream delays.

## 2026-10-21 - Capture five-minute member status and battery reporting

- Owner endorses the Infrastructure-page feedback; retain it with LOCAL-1 without selecting the exact neighbor layout/page name or starting implementation.
- Add [LOCAL-2](wishlist.md#member-node-and-battery-reports-without-a-gps-fix) to the wishlist and Deferred queue. Capture owner-reported missing member battery data and the requested five-minute (300-second) node/status and battery broadcasts, even without a satellite fix or phone. Retain 15 minutes as the maximum baseline reporting interval and five minutes as the current requested setting; GPS staleness requirements remain separate.
- Preserve separate node identity, battery telemetry, receiver-measured signal and GPS freshness semantics. Future acceptance follows actual member transmissions through both available gateways and portal ingestion, including no-fix operation, repeated cycles, fix recovery, reboot and cadence/runtime effects. The cause is unverified and no radios/settings, code, live data or GitHub issues/Project changed.
- Verification: captured requirements reviewed against the request; relative documentation file targets resolve and whitespace checks pass. Documentation only; no device or application tests performed.

Next useful step: activate LOCAL-2 when ready and identify available member trackers/settings before diagnosing the missing reports or applying the five-minute profile.

## 2026-10-21 - Capture Infrastructure page overhaul

- Owner requests a tracker entry and feedback. Record [LOCAL-1](wishlist.md#infrastructure-page-overhaul) in the wishlist and Deferred queue: richer device summary cards with last heard, battery and GPS highlights; include member devices; open full node cards; replace the main neighbor table with a readable current-state view; optionally retain a collapsed, sortable, paginated debug table with timestamps; consolidate useful unique detail into full cards.
- Recommend keeping contact, GPS and battery freshness distinct. Preserve tentative choices about neighbor presentation, debug-table retention and a broader page name. Cross-link related parked card requests and keep GH-47 release/acceptance plus GH-51/GH-52 timing limits separate. No implementation or other deferred item activated; GitHub issues/Project stay unchanged under the local-tracking trial.
- Verification: captured requirements reviewed against the owner's request; relative documentation file targets resolve and whitespace checks pass. Documentation only; no application tests or native UI validation performed.

Next useful step: activate LOCAL-1 when ready, then settle the current-neighbor presentation and audit which unique details/controls must move into the full card before implementation.

## 2026-10-21 - Correct current neighbor signals with relative age

- Owner selects GH-47 on the local-tracking trial and requests comparison before design selection. Compare per-row relative-age filtering, persistent current state, stale-queue/source expiry and the optional absolute-clock alternative. Select a small durable current state using installed SNNS evidence; no absolute hearing timestamp requirement. [Decision and source evidence](../.scratch/pilot/issues/24-neighbor-current-state.md).
- Reproduce cached standard NeighborInfo replacing valid SNNS signal strength. Preserve standard tables and all raw reports/history, but exclude them from current signals. Retain each unchanged hearing's original receipt anchor and expire estimated age at two hours, including offline across map lines, directions/colors, node relationships, selected details/minimap and the Infrastructure table. Persist ordering and expired hearing guards across restart; handle partial tables, duplicates, known old boots, count reset/saturation and monotonic-counter rollover. Review finds and fixes a rejected-old-boot bootstrap loophole before publication. No fabricated UTC hearing time or historical anchor backfill.
- Publish source **1282463** and merge [PR #55](https://github.com/lfg-seth/snorr-meshlink/pull/55) into `trial/local-tracking` as **3d6bd1e** after [74 backend](https://github.com/lfg-seth/snorr-meshlink/actions/runs/39709144039) and [55 portal](https://github.com/lfg-seth/snorr-meshlink/actions/runs/39709144081) CI checks pass, including TypeScript/build on pinned Node 22.23.1. Eleven focused actual PocketBase regressions and migration down/up pass locally. Existing neighbor atomic and 17 adapter/queue checks pass; the local Windows demo simulation lacks timezone data, while full Linux CI passes. [Behavior, storage, checks and limits](../docs/operations/neighbor-signal-visibility.md).
- Update only the affected local tracker entries at handoff: GH-47 moves to Verify for separately authorized release and fresh/native acceptance; GH-51/GH-52 retain the unselected firmware/transport scope. Reported age excludes unseen delay before worker receipt, so a strict actual-hearing limit across radio/MQTT outages remains unverified. Sequence rollback/wrap fails closed; large networks retain the snapshot cap. Preserve R004 diagnostics, GH-4's pending owner reply, all deferred layout work, `main`, production and draft PR #50. No GitHub issue/Project change, firmware build/flash, device action or deployment.

Next useful step: separately authorize the backend/portal release and verify fresh passive reports plus offline calculated expiry. Select bounded source/queue work under GH-51/GH-52 before claiming a strict two-hour hearing limit through upstream outages.

## 2026-10-21 - Remove the temporary neighbor-options worktree

- Inspect `.scratch/worktrees/neighbor-options` after the owner's cleanup question. Its tracked, untracked and ignored-file status is clean; verify HEAD **22fcd7f** exactly matches the published `origin/fix/neighbor-signal-freshness` branch through remote readback.
- Remove the temporary checkout with normal `git worktree remove`. Preserve the local/remote branch and its draft implementation, comparison notes and history. Remaining worktrees are the local-tracking trial and the separate private main checkout; the trial working tree is clean after removal. No application, firmware, device, deployment or GitHub tracking changes; no application tests needed for checkout removal.

Next useful step: continue from the local tracker. Recreate an isolated checkout from the preserved neighbor branch only when that work is selected.

## 2026-10-21 - Trial compact repository tracking

- Owner authorizes the proposed reversible trial. Create `trial/local-tracking` from `origin/main` **0713f7ea60d7bd839d246630655d6d9f70a736db**, preserving the original `docs/telemetry-release-record` branch, other worktrees and unrelated untracked files. Keep `main`, GitHub issues and the Project board unchanged; no merge, archive or deletion yet.
- Make [.scratch/TRACKER.md](../.scratch/TRACKER.md) the single current queue with Current, Next, Verify and Deferred entries. Preserve all **36 open issues and 25 comments** in the [one-time local import](tracking-import/index.md), including original requirements, labels, timestamps, holds and handoffs. Retain GH-4's existing R004 diagnostic claim awaiting owner bridge-state confirmation; GH-47/GH-51/GH-52 remain Triage with no selected timing design. Migration activates no deferred work.
- Update agent instructions and project navigation for tracker/latest-session startup, with detailed history read only for the selected task. Replace routine issue claims, label updates and Project synchronization with a local handoff update. Preserve existing evidence records and publication/hardware boundaries. [Trial, machine handoff, acceptance and rollback procedure](../docs/operations/local-tracking.md).
- Verification passes: all 36 issue IDs appear once in their imported status groups, all 25 comments are accounted for, 243 relative documentation links resolve and whitespace/scope checks pass. Read-only review corrects GH-5's summary to retain already-passed G002 neighbor delivery while preserving the pending sensor-power scope. This is a documentation/tracking change with no application, firmware, service or hardware action. No measured speed, token or cost saving is claimed; assess during actual work.

Next useful step: use this branch for the next owner-selected task and assess the simpler handoff. If rejected, keep trial records and return to the prior workflow; if accepted later, archive the pre-merge main state and merge normally before separately retiring old issue tracking.

## 2026-10-21 - Deploy telemetry receipt-time fallback

- Owner explicitly says deploy. Reclaim [Prevent battery display freezing when telemetry loses its measurement clock #53](https://github.com/lfg-seth/snorr-meshlink/issues/53), update the demo recovery verifier for the new history provenance and merge [PR #54](https://github.com/lfg-seth/snorr-meshlink/pull/54) as **8c5350e8834a771781d594414bd6b7c812a5f136**. Final PR CI and isolated LXC 63 backend/49 portal checks, TypeScript/live build pass. Preserve concurrent worktrees; use a separate main-based release-record branch.
- Pre-release backup and isolated live/demo recovery pass. Deploy backend/frontend together with rollback retained; all migration files and protected live/demo database, account-credential and worker-configuration hashes remain unchanged during promotion. Public nine-file manifest, all six services, live/demo isolation, public/authentication boundaries and post-release isolated recovery pass. Fresh MQTT archival and empty queue pass. [Exact hashes, checkpoints and remaining limits](../docs/operations/battery-contact-freshness-20261021.md#deployment---2026-10-21).
- Actual React components against sanitized live R002/R004 data render the correct selected voltage/age and history without an unknown-time message. Histories include prior unknown-time samples immediately. Fresh normal-cadence packets pass: R004 **4.091 V**, measured **18:24:16 Pacific**, replaces its selected five-hour-old reading; R002 **4.110 V**, measured **18:26:54**, advances its reading/history. Both now supply valid calendar time, correctly preferred; no radio/firmware/configuration/clock change performed. Final fresh-telemetry backup and isolated live/demo recovery pass. Release deployment claim to Verify with no retained session claim; native browser/mobile and sustained freshness remain unverified.

Next useful step: refresh the portal and confirm native presentation, then continue sustained telemetry freshness/outage verification under the existing issues. Derived Project reconciliation still awaits authenticated CLI access.

## 2026-10-21 - Implement telemetry receipt-time fallback

- Owner authorizes backend/portal changes under [Prevent battery display freezing when telemetry loses its measurement clock #53](https://github.com/lfg-seth/snorr-meshlink/issues/53): valid device calendar time first, otherwise receipt time for displayed measurement time/age; retain absent/invalid source clocks in storage and use no uptime ordering. Claim #53 and create a separate branch from origin/main, preserving draft neighbor PR #50.
- Actual PocketBase regression reproduces 4.19 V freezing ahead of a newer 4.05 V unknown-time report, then passes with shared per-metric effective-time selection. Preserve GPS/neighbor timing and original source/receipt provenance; duplicate receipts cannot refresh selected telemetry. Apply fallback consistently to telemetry values, battery history, cards, charge/power presentation and supported telemetry health. [Behavior, evidence and remaining release work](../docs/operations/battery-contact-freshness-20261021.md#receipt-fallback-correction).
- All 49 portal tests/TypeScript/production build pass locally. Targeted actual-binary backend tests pass for source-clock loss/recovery, delayed/duplicate packets, invalid/future clocks, health and mixed-clock history. Full Windows suite exposes connection resets on authorization tests and missing timezone data; Linux CI is the full verification path. Automatic approval review rejects isolated LXC source staging, so no source transfer or production change is made; use authorized GitHub CI publication instead.

- Publish application **6ee314a** and deterministic receipt-order fixture correction **d382ce2** in [PR #54](https://github.com/lfg-seth/snorr-meshlink/pull/54). Preserve concurrent main **87d2422**'s G002 Wi-Fi record in merge **7a71f67**, resolving only session-log insertions. All **63 backend checks** pass on Linux Python 3.14.3 / PocketBase 0.40.5 and all **49 portal checks**, TypeScript and build pass on pinned Node 22.23.1. Release implementation claim to Verify for deployment and fresh/native acceptance; no retained session claim. Final evidence links are in the diagnosis/correction record.

Next useful step: release PR #54's backend/frontend together through the existing backup/recovery procedure and verify new unique R002/R004 receipts and native presentation. No device action, migration or deployment in this implementation session; derived Project reconciliation still awaits authenticated CLI access.

## 2026-10-21 - G002 second Wi-Fi replacement

- Owner authorizes supplied Wi-Fi settings on attached G002 only. Read startup/hardware handoff records, search related issues and claim [Diagnose missing production node updates](https://github.com/lfg-seth/snorr-meshlink/issues/40) for this scoped configuration follow-up. Preserve concurrent portal work in the original checkout; record hardware evidence in an isolated main checkout.
- Independently identify COM6 HELTEC_V3 `!849ad7a0`, unchanged **2.7.26.9d2fd8f**. New complete private backup and independent post-restart profile comparison pass: only Wi-Fi SSID differs, with owner-supplied password already matching. Identity/keys/channels, MQTT, CLIENT/TX disabled, neighbor collector and enabled 300-second device telemetry preserved.
- Retained console observes IP acquisition, MQTT connected and publication activity. No flash/reset, other-board write or server/application change; serial closed. [Evidence and limits](../docs/operations/g002-neighbor-gateway.md#clifford-int24-wi-fi-update---2026-10-21). Keep credentials/profiles/raw logs private.
- Release scoped Windows claim to Verify; #40 remains open for original failure trigger and sustained reconnect verification. GitHub CLI is unavailable on this desktop; derived Project reconciliation remains pending the authenticated management host.

Next useful step: observe sustained per-gateway delivery and capture Wi-Fi/MQTT state before resetting during a recurrence; independent production ingestion was not checked in this short Wi-Fi task.

## 2026-10-21 - Capture neighbor-card cleanup and sign-in persistence fixes

- Owner adds two more portal fix-list items. Search existing authentication and endpoint issues; create [Remove "Endpoint locations" from neighbor signal cards](https://github.com/lfg-seth/snorr-meshlink/issues/48) and [Improve portal sign-in persistence to avoid roughly hourly reauthentication](https://github.com/lfg-seth/snorr-meshlink/issues/49), linked from [the wishlist](wishlist.md#remove-endpoint-locations-from-neighbor-signal-cards). Record the sign-in interval as approximate owner-reported behavior with cause and reproduction details unknown; link existing native authentication verification #6 without treating the prior reload fix as resolution.
- Creation responses verify both issues open with exactly `status:deferred` and `area:portal`, typed feature and bug respectively, without assignees or milestones. Capture only; no diagnosis, application implementation, testing or deployment. Fetch origin and preserve unrelated battery-box model. GitHub CLI remains unavailable on this desktop; derived Project reconciliation is pending the authenticated management host.

Next useful step: keep the additions deferred until owner activation, then verify section removal and diagnose sign-in expiry against a captured browser/session case; reconcile the derived Project when authenticated CLI access is available.

## 2026-10-21 - Explain recent B002/G001 neighbor report during isolation

- Owner reports a roughly 36-minute-old B002/G001 report despite physical isolation. Search existing work and claim [Diagnose recent B002/G001 neighbor reports while radios are isolated](https://github.com/lfg-seth/snorr-meshlink/issues/47) for read-only diagnosis. Preserve unrelated battery-box model; fetch origin.
- Reproduce recent standard-table receipt with unknown hearing time in live SQLite and authenticated state. Private archive decode confirms G001 itself publishes distinct, non-retained/non-duplicate reports at 07:46 and 13:46 Pacific, advertising six-hour cadence and repeating B002's 6.25 dB SNR without a last-heard clock. Latest richer B002/G001 report is 06:44 Pacific, already 29m 32s since hearing, with count 314 unchanged across preceding reports. [Evidence, code path and limits](../docs/operations/neighbor-report-freshness-20261021.md).
- Explain cached standard-table publication and portal latest-row selection: report receipt is not fresh RF evidence. Standard firmware retains neighbors for twice their stored broadcast interval; exact live entry interval/expiration and absolute last-heard time remain unknown. No hardware, application, configuration or deployment change. The separate two-hour cutoff request #43 remains deferred; using report receipt as activity would preserve this failure mode.
- Complete diagnostic scope and release claim after evidence publication. GitHub CLI is unavailable on this desktop, so derived Project reconciliation remains pending the authenticated management host. Private payloads/keys/locations stay outside Git.

Next useful step: when owner activates a correction, preserve hearing freshness separately from periodic table publication and verify the isolated-pair case before deploying.

## 2026-10-21 - Deploy gateway battery graph correction

- Owner restores connection and authorizes deployment. Reclaim [Populate gateway battery graphs from reported voltage](https://github.com/lfg-seth/snorr-meshlink/issues/42); live inspection confirms original zero cadence, 47 G002 measured voltage samples and zero G001 battery reports. Merge [PR #46](https://github.com/lfg-seth/snorr-meshlink/pull/46) and synchronize main to **fa03550**.
- Verify pre-release backup and isolated live/demo recovery. Server pinned Node 22.23.1 passes all **47 portal tests**, TypeScript and live build. Fourteen backend hooks/migrations match prior deployment. Publish frontend source/assets with rollback retained; quiesced live/demo database and private configuration hashes remain unchanged. Separately save both owner-confirmed `lipo-1s` / **1000 mAh** pack profiles/descriptions and G002 battery cadence **5 minutes**; all nine identities, unrelated metadata and warning enablement survive independent readback. No radio/backend/schema change.
- Actual React/live-history checks show 48 G002 samples as a curve and approximately 80% at 3.996 V; unknown cadence renders the same samples as dots. G001 correctly awaits its first battery report. Public checks catch root-only staged asset modes; correct only public build files to 0644, then all nine HTTPS build hashes match. All six services, public/authentication boundaries, final live/demo isolated recovery and fresh MQTT ingestion pass. [Exact backups, hashes and limits](../docs/operations/gateway-battery-graphs.md#verification-and-deployment).
- Release claim to Verify for native presentation confirmation. No native/mobile or field/capacity/runtime acceptance claimed; G001 telemetry remains separate. Preserve private evidence and unrelated battery-box model. GitHub CLI is unavailable locally/on LXC; derived Project reconciliation remains pending the authenticated management host.

Next useful step: refresh the portal and confirm G002's visible graph; enable/verify G001 telemetry only when separately authorized and connected.

## 2026-10-21 - Gateway pack confirmation and empty graph correction

- Owner confirms one installed **1000 mAh LiPo in each of G001/G002**. Update inventory without increasing stock; retain uncertainty for remaining pack labels and actual capacity/runtime.
- Search existing issues and claim [Populate gateway battery graphs from reported voltage](https://github.com/lfg-seth/snorr-meshlink/issues/42). Actual chart reproduction fails twice with valid history and the original zero gateway cadence. Same-input positive-cadence control passes without a battery profile. Fix hidden isolated samples by plotting exact dots; retain curves/outage boundaries for known cadence. Publish application **c15859a** in [PR #46](https://github.com/lfg-seth/snorr-meshlink/pull/46). All **47 portal tests**, TypeScript and production build pass on desktop Node 25.6.0 and [pinned 22.23.1 CI](https://github.com/lfg-seth/snorr-meshlink/actions/runs/39675958265). Release claim to Verify; derived Project sync awaits authenticated CLI access.
- Recorded portal SSH hostname returns NXDOMAIN, preventing current production history/config readback, metadata updates and deployment. Request current LXC address. No hardware, backend, schema or server change; preserve unrelated owner work and battery-box model. [Evidence and remaining release steps](../docs/operations/gateway-battery-graphs.md).

Next useful step: restore portal host access, verify live gateway metadata/history, apply confirmed pack details and release the reviewed frontend with standard backup/recovery checks. G001 telemetry enablement remains separate.

## 2026-10-21 - Capture three portal node-card fixes

- Owner requests additions to the portal fix list. Search existing portal issues and create [Simplify node-card neighbors and hide links after two hours of inactivity](https://github.com/lfg-seth/snorr-meshlink/issues/43), [Hide node-card sensor voltage and current when no sensors are present](https://github.com/lfg-seth/snorr-meshlink/issues/44), and [Add member-node battery percentage beside GPS quality on node cards](https://github.com/lfg-seth/snorr-meshlink/issues/45). Preserve the requested miles, two-hour cutoff, sensor-presence condition and top battery icon in [the wishlist](wishlist.md#node-card-neighbor-details-and-inactivity-cutoff).
- Creation responses verify three open issues with `feature`, `area:portal` and exactly `status:deferred`, without assignees or milestones. Capture only; no application research, design, implementation, testing or deployment. Preserve the unrelated infrastructure-test edit and battery-box model. Fetch origin; main matches origin/main. GitHub CLI is unavailable on this desktop, so derived Project reconciliation remains pending the authenticated management host.

Next useful step: keep these fixes deferred until owner activation; reconcile the derived Project with the existing sync script when authenticated CLI access is available.

## 2026-10-21 - R004 battery-removed confirmation and bridge preparation

- Owner confirms the earlier **−11.1 to −11.3 mA** trace was captured with the battery disconnected and USB connected. This resolves the prior trace's physical-state uncertainty; current accuracy and any other connected branch remain unverified.
- Reclaim [Investigate INA219 current discrepancy with simultaneous same-path measurements](https://github.com/lfg-seth/snorr-meshlink/issues/4) for the owner-proposed VIN+ to VIN− bridge, with battery absent and USB/INA219 powered. Bridge confirmation remains pending. New transition trace reports **0.0, −0.3, −0.1 mA** in fresh matched replies; four held triples remain stable at **±0.02 mV** or less, with correct current arithmetic. Do not attribute the change to the bridge until physical state is confirmed.
- Complete profile comparison passes on unchanged diagnostic **2.7.26.09d8a9d**. No flash, saved configuration change or other-board action. Close serial; retain claim explicitly awaiting the owner's bridge-state reply. Preserve private raw captures and unrelated battery-box model. [Evidence](../docs/operations/ina219-audit.md#battery-removed-confirmation-and-input-bridge-check).

Next useful step: confirm VIN+/VIN− bridge state, then compare bridge-on and bridge-off readings with battery still disconnected.

## 2026-10-21 - R004 INA219 register investigation and zero-test preparation

- Owner reconnects R004 with installed R100 between battery and board and authorizes flashing for diagnosis. Read startup/handoff records, synchronize main, inspect and claim [Investigate INA219 current discrepancy with simultaneous same-path measurements](https://github.com/lfg-seth/snorr-meshlink/issues/4). Preserve unrelated battery-box model and existing private worktree.
- Identify COM17 RAK4631 `!77fdb9f1`, USB `820C9B4F0C2D7675`; privately back up full profile/keys/channels. Existing firmware reproduces **−1,152.6 mA**. Publish opt-in diagnostic source `4ad67eb35`, then held-conversion probe `09d8a9dbf` on authorized firmware branch, with [scoped draft review](https://github.com/lfg-seth/firmware/pull/2). Both RAK builds pass; current image is **2.7.26.09d8a9d**, with independent full identity/key/channel/local/module equality. No other board or saved configuration changes.
- Correct live config/calibration **0x399F / 0x1000**; six held conversions reread identically three times and have exact current/shunt multiplication, yet imply **+1.24 to −1.50 A** across separate conversions. The original symptom persists in fresh matched replies. Narrow source of large values to the sensor's shunt conversions; physical input/wiring/interference/module fault remains unresolved. Existing actual-source R100 harness passes at multipliers 1 and 10; pinned formatting/whitespace checks pass, Trunk unavailable. [Audit, exact image hashes, measurements and limits](../docs/operations/ina219-audit.md#r004-reinvestigation--2026-10-21).
- Owner proposes battery removal with USB retained for a zero-current check. Subsequent trace gives **−11.1 to −11.3 mA**, but physical battery-removal state is unconfirmed; do not accept it as a zero-current result. Wiring and physical millivolt evidence remain pending. Close serial; retain diagnostic image for comparison and ordinary pinned release as recovery. No accuracy fix, battery-only acceptance, RF/MQTT/portal verification or field result claimed.
- Hand off #4 to Verify without retained session claim, pending physical state/measurement. Project reconciliation helper cannot run without authenticated GitHub CLI on this desktop. Private profiles/raw logs stay ignored; publish only sanitized evidence and source pin.

Next useful step: confirm battery is disconnected with USB/INA219 powered, capture fresh raw/current values, and compare DC millivolts across R100 before changing calibration or replacing hardware.

## 2026-10-21 - Enable G002 telemetry every five minutes

- Owner authorizes connected G002 only and leaves G001 for later. Search existing issues and claim [Enable G002 device telemetry every five minutes](https://github.com/lfg-seth/snorr-meshlink/issues/41). Synchronize main and preserve unrelated battery-box model.
- Identify COM6 HELTEC_V3 `!849ad7a0` / unchanged `2.7.26.9d2fd8f`; privately back up complete profile. Set device telemetry enabled and interval **300 seconds**. Independent complete profile comparison after configuration restart passes with exactly these two changes; keys/identity/network/MQTT/radio/neighbor configuration preserved, LoRa TX disabled.
- First device report **14076657**, **4.25 V**, measured **10:17:13 Pacific**, reaches production observations at **10:17:14.159**. Console confirms encrypted MQTT publication and LoRa TX-disabled rejection. [Evidence](../docs/operations/g002-neighbor-gateway.md#five-minute-device-telemetry-enabled---2026-10-21). Close serial; no G001/server/application/firmware change. Sustained cadence, calibration/runtime and #40 reconnect acceptance remain separate.
- Close scoped #41 after evidence publication; release claim. Derived Project reconciliation remains pending authenticated CLI access. Private credentials/profiles/raw logs remain ignored.

Next useful step: update G001 when connected and authorized; observe sustained G002 delivery without treating this single receipt as endurance evidence.

## 2026-10-21 ? Explain missing gateway battery metrics

- Owner asks why G001/G002 lack battery readings. Read-only production inspection confirms zero gateway observations but fresh own-source receipts, with both node IDs mapped for infrastructure telemetry.
- Parse saved profiles with protobuf defaults: both disable device telemetry and set interval `2147483647` seconds. G002 uses today's independent readback; G001's saved October 19 profile is historical. Firmware requires enabled device telemetry for periodic publication; custom neighbor reporting is independent. Portal already accepts gateway voltage. [Diagnosis and limits](../docs/operations/g002-neighbor-gateway.md#gateway-battery-reporting-diagnosis--2026-10-21).
- Explanation only; no hardware/application/server settings changed. Disabled fields predate the Wi-Fi update. No new claim or closure of #40's sustained reconnect verification.

Next useful step: when authorized, enable gateway device telemetry at a practical interval, retain LoRa TX disabled and verify fresh voltage through MQTT and portal.

## 2026-10-21 ? G002 Wi-Fi replacement

- Owner supplies replacement Wi-Fi for connected G002. Inspect/claim [Diagnose missing production node updates](https://github.com/lfg-seth/snorr-meshlink/issues/40) for bounded follow-up; synchronize main and preserve unrelated battery-box model.
- Identify COM6 HELTEC_V3 `!849ad7a0` on unchanged `2.7.26.9d2fd8f`; privately back up profile and save only supplied Wi-Fi fields. Independent complete profile comparison passes after configuration restart, preserving identity/keys/channels/radio/MQTT. Inactive DTR/RTS precede serial open. Console observes IP acquisition, MQTT connected and queued publish. Correct optional status-capture attribute error and pass independent verifier rerun. [Evidence and capture limits](../docs/operations/g002-neighbor-gateway.md#wi-fi-replacement--2026-10-21).
- Close serial and release #40 to Verify; no retained claim, firmware/server change, other-board write or private-data publication. Production ingestion, sustained delivery and automatic reconnect remain unverified. Derived Project reconciliation pending authenticated CLI access.

Next useful step: observe fresh G002 production receipts and sustained outage recovery under #40 when selected.

## 2026-10-20 — Connected gateways recover production delivery

- Owner connects both gateways and debug receiver; reclaim #40. Identify G001 COM21, G002 COM22 and dedicated sniffer COM6. Passive logs show G002 publishing after recent boot, while G001 is still receiving RF after approximately 85,723 seconds uptime but reports disconnected MQTT and a full queue discarding older packets. Both retain expected firmware/profile and last supplied Wi-Fi settings.
- G001 restarts during ordinary serial API inspection, potentially from default USB control-line states; no reboot command/configuration write/flash is issued. Its delivery resumes at **19:47:00.592 Pacific**, after G002 at **19:44:44.367**. Subsequent safe-control-line readback confirms both Wi-Fi/MQTT connections and exact preserved local/module/channel profiles. [Evidence and limits](../docs/operations/node-update-outage-20261020.md#connected-gateway-follow-up-and-recovery).
- Original archive check turns green: 3,775 records, two new receipts, 200 valid recent envelopes and empty queue. Fresh B001/B002 GPS fixes reach both gateways; gateway-originated reports and R001/R002/R003/R004 also resume. No fresh R005 observed in the short checkpoint. Dedicated sniffer records 12 decoded receptions/six duplicates without a gap event or capture error over 65.101 seconds. No sustained/reconnect root-cause or field acceptance claimed.
- Close serial interfaces and release claim to Verify: current delivery recovered, original trigger/automatic reconnect reliability unresolved. Raw/profile/track evidence stays ignored/private. Preserve unrelated battery-box model and firmware; derived Project reconciliation remains pending the authenticated management host.

Next useful step: observe a recurrence with gateway connection status and console already captured, distinguishing Wi-Fi loss from MQTT-session failure before any reset; verify the remaining R005 receipt during its full reporting interval when powered.

## 2026-10-20 — Diagnose missing production node updates

- Owner reports missing production updates; search current issues and claim [Diagnose missing production node updates](https://github.com/lfg-seth/snorr-meshlink/issues/40). Fetch/fast-forward main to preserve the other workstation's published release/evidence; preserve unrelated untracked battery-box model and firmware.
- Read-only archive check reproduces missing fresh deliveries. Production and independent MeshMonitor both stop receiving G001/G002 at **20:19:33 Pacific October 19**, before today's application deployment. Production has 3,746 archived deliveries, nine real devices, empty queue, healthy database/storage and an active subscribed worker. Separate validating-TLS subscriber authenticates/subscribes but receives no packets. [Sanitized evidence and exact limits](../docs/operations/node-update-outage-20261020.md).
- Locate the failing observed boundary upstream of portal ingestion; do not assert power/Wi-Fi/broker/gateway root cause. Broker is active but connection logs require unavailable privilege; no gateway is attached locally. Ask owner for current gateway power/Wi-Fi status. No production, broker, radio or firmware changes; no recovery claimed.
- Release session claim to Verify pending gateway-side/broker-admin evidence. GitHub CLI is unavailable on this desktop; derived Project reconciliation remains pending the authenticated management host.

Next useful step: confirm both gateways' power/Wi-Fi and MQTT sessions; inspect broker connection logs if needed, then verify fresh archive and normalized per-gateway receipts after correction.

## 2026-10-20 — Merge and deploy demo/minimap release

- Owner explicitly requests merge and deployment. Complete PR #38's test correction, obtain passing hosted backend/portal checks and merge the exact reviewed head as application `5d07d61d916290ea81d5ed98bfdadc6127f407eb`. Local main fast-forwards and tracks origin/main. Both merged-main CI workflows pass too.
- Build/test that exact source in isolated `/opt/meshlink-release-5d07d61` on the pinned server runtime: 59 backend and 46 portal checks, TypeScript/live build pass. Replace the initial stage's outdated shared dependency symlink with its own lockfile install; no production dependency mutation. Preflight confirms all fourteen hook/migration files are semantically unchanged (old CRLF endings only), so no migration.
- Take and verify pre-release backup `meshlink-20261021T003040Z.tar.gz`; preserve source/static rollback and complete old demo workspace at root-private `/opt/meshlink-rollback-5d07d61`. Deliberately refresh only the separate hosted synthetic demo from the verified checkpoint. Exact live database-file and configuration fingerprints remain unchanged during promotion; preserve all nine live identities, private configuration and operational/history/archive rows. Publish assets before the index and retain prior assets for open tabs.
- All 126 application source files and nine installed/public HTTPS build files match the tested release. Expanded demo member battery, humidity, signed/zero/missing sensor values and three SNNS examples (thirteen links) pass state checks. Six services, public/protected routes, authentication throttling, demo/live token and OS boundaries and post-release isolated live/demo database/API/history recovery pass. Post-release backup `meshlink-20261021T003651Z.tar.gz` and both SHA-256 hashes are recorded in [release operations](../docs/operations/portal-lxc.md#demo-feature-examples-and-minimap-navigation--2026-10-20).
- Pre-existing old-demo 7-day/30-day histories correctly return the API's 50,000-sample cap with truncation; the existing verifier rejects that valid response. Independently verify exact bounded saved samples/flags on an isolated pre-release restore. Fresh checkpoint passes the standard post-release verifier. Record [the scoped verifier bug #39](https://github.com/lfg-seth/snorr-meshlink/issues/39); no API limit change or history deletion.
- Live feed is online, queue is empty and the latest 200 archived envelopes validate. No new MQTT receipt appears during a 45-second observation, so no fresh-radio claim. Browser inventory is empty: native WebGL/mobile/keyboard visual review remains in #6. Hand off release evidence to #9/#21 without a retained session claim; preserve explicit native-review limits. No hardware changes, field acceptance or private-data publication.

Next useful step: complete native portal/demo review under #6 and the remaining #9/#21 acceptance checks, then address #39 when selected. Fresh radio delivery, sustained GPS freshness/runtime, outage behavior and off-host backup work remain separate from this deployed software release.

## 2026-10-20 — Resolve portal release test blocker

- Owner explicitly authorizes merging and deploying PR #38. Claim #9/#21 for the release and inspect hosted checks: backend CI passes; Portal CI stops during the broad map test with runner shutdown, without an assertion result.
- Isolate the broad map/legend test: it times out after 25 seconds. Temporary checkpoints locate the stop at the unfinished assertion expecting no endpoint-location section. Comparing its boolean result instead produces the deterministic `true !== false` failure in two seconds; formatting the DOM-valued assertion caused the apparent hang.
- Restore expectations for the existing endpoint-location section and unknown-location context, retaining minimap icon navigation. The same complete interaction scenario passes in 2.9 seconds. Remove all temporary instrumentation. This corrects the test without changing portal behavior; full suite/build and hosted CI are the next release checks.

Next useful step: publish the correction in PR #38, merge after complete checks, then deploy the merged source with verified live/demo backups, a preserved prior demo workspace, source/static rollback and post-release isolation/recovery verification. Native WebGL/mobile review remains separate.

## 2026-10-20 — Publish all saved local changes

- Owner requests pushing all local changes. Fetch origin and fast-forward main from `b108cf3` to `b55bb33`, temporarily stashing/restoring every local edit. Resolve the session-log conflict by preserving both histories and synchronize the clean firmware checkout to the already published `473a9ed41` pin; no new firmware change.
- Publish demo generator/worker/checkpoint, tests/docs and verifier as `8264b45` (Refs #9), and minimap navigation plus all saved infrastructure-test edits as `3c4f592` (Refs #21), on `codex/publish-local-demo-minimap-20261020`. [Draft PR #38](https://github.com/lfg-seth/snorr-meshlink/pull/38) targets main under the repository PR workflow. This session-record commit accompanies that publication; main remains at the fetched remote tip.
- Verification: all 59 backend integration checks pass outside the sandbox (sandbox sockets are denied); TypeScript/production build and whitespace checks pass. All 45 portal checks pass outside the sandbox with `--test-skip-pattern='unlabelled signal lines'`. The full portal run times out after 55 seconds, matching the recorded broad interaction stall. Preserve its unfinished endpoint-location assertions, which still disagree with the retained location section; no full-suite pass or native browser/WebGL review claimed. Existing bundle-size warning remains.
- Return #9/#21 to Verify with publication evidence and release both session claims. Initial Project reconciliation checks 36 issues and applies 17 updates, including importing newer issues without activating deferred work; handoff reconciliation checks 36 issues and applies the two Verify transitions. Preserve all prior local session notes. No merge, deployment, hosted demo refresh, hardware operation or private-data publication.

Next useful step: resolve the broad interaction check and endpoint-location expectations, complete native review and finish draft PR #38. A hosted demo release still requires its separate backup, refresh, isolation and recovery procedure.

## 2026-10-20 — Check local changes against production

- Owner asks whether local changes remain outside production. Working tree has 13 modified files and untracked `backend/demo_scenario.py`: demo feature-data refresh, neighbor minimap device selection, associated tests/docs and existing session notes. Preserve all edits.
- Read production release markers over SSH: application `bed40dd3204b5ce98ce967468c97d69b5b78d0e5`, records `09e959056fad589b8afdd40b8feb6c33b762a0a3`. Checksums confirm the edited demo generator/worker/checkpoint and four portal source files differ from hosted source; the new demo scenario module is absent there. These local application changes are not deployed.
- Local HEAD `b108cf3` matches the cached origin/main ref, but live GitHub main is `b55bb330e4534512bbcd07d6c2ddf8cd0f64de30`; the cached ref is stale. No pull, commit, push, deployment, tests or hardware changes performed.

Next useful step: reconcile the newer GitHub changes while preserving this working tree, then finish release verification before publishing/deploying the pending application work.

## 2026-10-19 — Defer manual GPS tracking session controls

- Owner adds a request to start, stop and restart member GPS tracking sessions while devices stay powered on. Search existing issues; create [Allow starting, stopping and restarting member GPS tracking sessions while devices stay on](https://github.com/lfg-seth/snorr-meshlink/issues/37) and link the requested behavior in [the wishlist](wishlist.md#member-gps-tracking-session-controls).
- Creation response verifies an open issue with `feature`, `area:portal` and exactly `status:deferred`, without assignee or milestone. No research, design, implementation, testing or deployment. Fetch origin and confirm main is current; preserve existing records, firmware and unrelated untracked battery-box model. Project synchronization remains pending authenticated CLI access on the management host.

Next useful step: keep session controls deferred until owner activation, then define session semantics and controls; reconcile the derived Project with the existing sync script when CLI access is available.

## 2026-10-19 — G001 completes richer gateway neighbor rollout

- Owner connects G001 for the existing authorized rollout; reclaim [Enable richer passive neighbor measurements on Heltec V3 gateways](https://github.com/lfg-seth/snorr-meshlink/issues/31). Identify HELTEC_V3 `!9ea13cc0`, COM6 / ESP32-S3 / 8 MB; privately back up complete own profile and all flash bytes. Recheck exact cached V3 image/hash and original app0 partition/OTA selection; flash only verified **2.7.26.9d2fd8f** application with esptool hash verification. No rebuild/source change/reset/profile clone or other-board write; project firmware pin remains `473a9ed41`.
- Full independent intended user/channel/security/local/module comparison passes after flashing and through explicit reboot: CLIENT, LoRa TX disabled, enabled/local-only neighbor module with standard 21600-second default. G001 already matches owner-supplied Wi-Fi; preserve original Wi-Fi/MQTT unchanged. [Image, recovery fingerprint and limits](../docs/operations/g001-neighbor-gateway.md).
- First 180.3-second validating-TLS window has six G001 deliveries/no decode errors; own report arrives at its end, superseding earlier mid-window absence. At **19:57:55.391 Pacific**, packet **a1a5ea71**, boot 1325647066 / sequence 1 / uptime 72 seconds, is normalized/accepted with direct RSSI/SNR/hearing-age/count rows for R005/R002/R004. Authenticated portal exactly matches all three rows/provenance and null absolute hearing clocks; nine devices and 13 existing G002 reports retained. Fresh normal gateway forwarding and expected duplicate receipts pass. [TEST-022](field-results.md#test-022--g001-completes-passive-gateway-neighbor-rollout).
- Passive continuation with serial closed reaches sequence 2/six rows at 19:59:10 and sequence 3/seven rows at **20:00:25**, covering all five repeaters and both trackers. R002/R004/B002 observation counts increase to 2 with updated signal readings and hearing ages; short counter-update evidence is separate from sustained cadence/delivery acceptance.
- Existing gateway source mappings suffice; no new server config/application deployment or recovery-test rerun. Keep board-specific recovery backup/raw measurements private, unrelated battery-box model untracked and G002/MC00 unchanged. Both scoped gateway rollout acceptances pass; close #31 after publishing evidence. Sustained cadence/runtime, calibration, independent RF-silence and field testing remain separate. CLI Project reconciliation pending unavailable GitHub CLI on this desktop.

Next useful step: observe both updated gateways during a longer passive tracking run and backhaul interruption test when authorized, keeping source-observer measurements separate from gateway delivery and GPS measurement age.

## 2026-10-19 — Capture three deferred map changes

- Owner requests three portal map issues for later. Search existing issues; capture [Keep overlapping map nodes separately visible and selectable](https://github.com/lfg-seth/snorr-meshlink/issues/34), [Show only the selected node's neighbor signals on the desktop main map](https://github.com/lfg-seth/snorr-meshlink/issues/35), and [Default the map to the center of all node locations](https://github.com/lfg-seth/snorr-meshlink/issues/36). Verify creation responses: all open with exactly `status:deferred`, `area:portal` and one type label, without assignee or milestone.
- Extend [the durable wishlist](wishlist.md) with requested behavior and remaining questions. Capture only; no feature research, design, implementation, testing or deployment. Preserve unrelated untracked battery-box model and firmware submodule.
- Fetch origin and confirm main matches origin/main before record edits. GitHub CLI is unavailable on this desktop, so derived Project synchronization remains pending the authenticated management host.

Next useful step: keep these issues deferred until owner activation; reconcile Project cards with `scripts/github/sync-project.py --apply` on the management host.

## 2026-10-19 — G002 richer passive gateway neighbor collection

- Owner connects G002 and activates the same richer measurements on gateways. Claim [Enable richer passive neighbor measurements on Heltec V3 gateways](https://github.com/lfg-seth/snorr-meshlink/issues/31); add dedicated `heltec-v3-gateway` target using the existing collector, keeping ordinary V3/MC00 targets unchanged. Source `9d2fd8fd0`, documentation-format follow-up `473a9ed41`, published through [merged firmware PR](https://github.com/lfg-seth/firmware/pull/1) on `snorr/rak-survey`; project pins published follow-up. Collector capacities 32/10 and actual-module sanitizer checks pass; full pinned ESP32 build succeeds. Trunk unavailable locally; pinned Prettier corrects initial Markdown-only CI failure, and final Trunk/label/Semgrep checks pass.
- API/flash identify HELTEC_V3 G002 `!849ad7a0`, COM6 / ESP32-S3 / 8 MB. Save complete private profile/full-flash recovery copy, compare partition bytes and verify active app0; application-only flash **2.7.26.9d2fd8f** passes esptool hash check. Independent full identity/channel/key/intended-profile comparison passes through explicit reboot: CLIENT, LoRa TX disabled, enabled/local-only neighbor collector, standard NeighborInfo default 21600 seconds. [Exact image/hash/evidence](../docs/operations/g002-neighbor-gateway.md).
- Prior saved Wi-Fi repeatedly reports no-AP reason 201. Owner supplies replacement network; save/readback while preserving MQTT/LoRa. Live worker accepts gateways only as forwarders, so after standard private backup add both already registered gateway IDs as allowed infrastructure report sources, preserving all other config; restart only worker. No application/schema/frontend release or archive replay.
- At **19:42:36 Pacific**, G002's own SNNS packet **b92f2bfd**, sequence 1 / uptime 70 seconds, is normalized/accepted with RSSI/SNR/hearing age/counts for five direct neighbors (R001/R002/R004/R005/B002). 180.3-second validating-TLS sample has eight G002 deliveries/no decode errors. Authenticated snapshot confirms all five rows with correct observer/gateway provenance, unknown absolute hearing clocks and all nine devices. Three fresh R001/R002/R005 report copies retain G001/G002 receipts without duplicate reports. [TEST-021](field-results.md#test-021--g002-gateway-originated-passive-neighbor-reports). Historical [G002 forwarding/power follow-up](https://github.com/lfg-seth/snorr-meshlink/issues/5) gains neighbor/deduplication evidence; power remains deliberately disabled/unverified.
- Post-change private backup/isolated database/API restore, history/credentials/device preservation, public HTTPS/protected routes and authentication throttling pass. Keys, Wi-Fi, raw console/packets, backups and build cache stay ignored/private. G001 and MC00 unmodified; preserve unrelated battery-box model. No sustained cadence/runtime, calibration, independent RF-silence or field acceptance. Release claim to Verify pending G001 connection/update. CLI Project reconciliation remains pending because GitHub CLI is unavailable on this desktop.

Next useful step: connect/identify/back up G001 and apply the same verified V3 gateway image/local-only collector policy, verifying its own Wi-Fi and fresh observer-specific MQTT/portal reports. Reuse the verified local image; no RAK UF2, full-profile copy, reset or key replacement.

## 2026-10-19 — Verify production portal is current

- Owner requests checking production currency and updating/redeploying if behind. Claim [Verify production portal matches latest published application](https://github.com/lfg-seth/snorr-meshlink/issues/33). Fetch origin; main remains `c267942`. There are no changes between deployed application `bed40dd3204b5ce98ce967468c97d69b5b78d0e5` and origin/main in `portal`, `backend` or `deploy/portal`, and no newer application on published remote branches. Project-record commits do not require application redeployment.
- Production SOURCE_COMMIT matches that release. All 91 retained backend/frontend source files match production; all nine retained build files match installed files and public HTTPS responses byte-for-byte. Index SHA-256: `b2afae242c946c0054825c545696aa687e791f86d154ef3d453e3c394519457c`. All six services are active. Public health returns 200, anonymous live state 401, and admin/raw-device/worker routes 404. No credentials sent through public HTTPS.
- No redeployment needed or performed. Existing demo/minimap work (#9/#21) remains separate; this Windows checkout has no pending application edits. No native browser review, new build, backup recovery or field verification performed. Preserve unrelated battery-box model and firmware. CLI Project reconciliation remains pending the authenticated management host.

Next useful step: continue the scoped portal/demo review when requested; production already serves the latest published application.

## 2026-10-19 — Update production infrastructure locations

- Owner authorizes replacement database locations for R001–R005 and G001–G002. Claim [Update seven production infrastructure locations](https://github.com/lfg-seth/snorr-meshlink/issues/32); no matching existing location-update issue found. Preserve unrelated battery-box model and firmware submodule.
- Existing production backup completes with archive validation and SHA-256 (`meshlink-20261020T022820Z.tar.gz`). Patch only latitude/longitude in the seven device configuration objects through the loopback superuser API, preserving other configuration and device identities. Exact readback matches all seven owner inputs; authenticated live portal state independently matches and confirms non-simulation mode. All nine devices remain present. Root-private before/request/after/verification evidence: `/root/meshlink-maintenance/location-update-20261020T022905Z`.
- Record sanitized site update; exact coordinates stay outside Git. Historical provisioning inputs are unchanged. No radio configuration, installation or field verification performed. CLI Project reconciliation remains pending the authenticated management host.

Next useful step: owner reviews the updated live map; installation, permission and coverage remain separately unverified.

## 2026-10-19 — Check post-reflash gateway delivery

- Owner repairs DNS; retry succeeds. Read-only live archive/normalized receipts at 19:19 Pacific confirm **all five through G001**: R001 19:15:37, R002 19:15:22, R003 19:17:04, R004 19:15:28, R005 19:15:08. Fresh normalized temperature also passes for R003/R004/R005 (24.769783/27.470970/26.064301°C), with unknown measurement clocks. Actual worker/API services active; initial nonexistent service-name probe is not a failure finding. Earlier access and short-window limits below are superseded. R001/R002 temperature, G002, calibration and sustained cadence remain unverified. Publish receipt evidence and update scoped hardware issues; off-host/field acceptance unchanged.

- Owner asks whether R001–R005 reach the gateway, then changes desktop networks and requests retry. Existing portal SSH hostname returns NXDOMAIN before/after change, including direct queries to both configured local DNS servers; alternate existing SSH host times out. Ask owner for current portal hostname/IP without changing DNS/network configuration.
- Two independent read-only TLS MQTT observations, 19:14:39–19:15:35 and 19:16:18–19:17:13 Pacific, confirm seven fresh non-retained G001 deliveries from R003/R004/R005 with matching topic/envelope identities and recent radio-receipt timestamps. All three send SNNS; R004 sends device telemetry; R003 sends **24.769783°C**. [Evidence/limits](../docs/operations/repeater-gateway-check-20261019.md), [TEST-020](field-results.md#test-020--fresh-post-reflash-gateway-receipts).
- R001/R002 and G002 not observed in short windows; no offline conclusion. R003 temperature operation now passes RF/MQTT observation, while its telemetry wall-clock time remains invalid. One first-window decode error remains unclassified. Portal normalization, sustained cadence, calibration and forced relay remain unverified. No radio/broker/DNS changes; preserve ignored private evidence, firmware pin and unrelated battery-box model.

Next useful step: observe a full reporting cycle with all five powered, verify R001/R002 temperature hardware if expected, and check fresh G002 delivery under its existing follow-up. CLI Project reconciliation remains pending authenticated management host.

## 2026-10-19 — R005 CLIENT bench reflash completes five-radio rollout

- Owner connects R005 for the same CLIENT/temperature-only/no-INA219 configuration. Claim [Reflash R005 for CLIENT bench operation with temperature telemetry only](https://github.com/lfg-seth/snorr-meshlink/issues/30); identify RAK4631 `!f95b5501` by node/USB serial, save fresh complete private backup, verify pinned cache and replace dummy-load `2.7.26.8dd4dac` with ordinary released neighbor-signal `2.7.26.0b65f2e` through matched UF2 bootloader. This removes GPIO31 HIGH startup override; no rebuild/reset/key replacement or physical load measurement.
- Full independent identity/key/channel/profile comparison passes through explicit clock synchronization/reboot: CLIENT, device/environment 900-second telemetry, disabled power measurements/display, unconfigured battery INA address, NeighborInfo transmission enabled. Preserve radio profile/Fahrenheit preference and account for API role-dependent sleep readback. [Operating evidence](../docs/operations/r005-client-bench.md), [TEST-019](field-results.md#test-019--r005-ordinary-release-client-temperature-only-reflash).
- Local environment request plus 45 seconds yields no temperature. Sensor operation remains unverified; cached device values with uptime 1,453,310 seconds excluded. No gateway/portal delivery, utilization improvement or physical INA219/load removal/current-discrepancy resolution claimed. Other radios/live portal metadata unchanged; preserve firmware pin/unrelated battery-box model. Documentation links/whitespace checks pass.
- R001–R005 now share the verified ordinary release/CLIENT/temperature measurement policy. Update current project brief/flashing handoff and mark old R005 load preparation historical. Release claim and leave issue Verify pending fitted-sensor/wiring/detection check and fresh temperature. CLI Project reconciliation remains pending the authenticated management host.

Next useful step: verify fresh temperature reports from updated bench radios and fresh per-gateway/portal delivery, keeping local readback distinct from measured sensor/network operation. Historical load/current investigations remain separate.

## 2026-10-19 — R004 CLIENT bench reflash

- Owner connects R004 and requests same authorized CLIENT/temperature-only/no-INA219 configuration. Claim [Reflash R004 for CLIENT bench operation with temperature telemetry only](https://github.com/lfg-seth/snorr-meshlink/issues/29); identify RAK4631 `!77fdb9f1` by node/USB serial, save fresh private complete backup, verify pinned release cache and reflash released neighbor-signal `2.7.26.0b65f2e` through matched UF2 bootloader. No rebuild/reset/key replacement.
- Full independent profile/identity/key/channel comparison passes through explicit clock synchronization/reboot: CLIENT, device/environment 900-second telemetry, formerly enabled power measurements now disabled, power display disabled, battery INA address unconfigured, NeighborInfo transmission enabled. Preserve radio profile/Fahrenheit preference and account for role-dependent API sleep readback. [Operating evidence](../docs/operations/r004-client-bench.md), [TEST-018](field-results.md#test-018--r004-client-temperature-only-bench-reflash).
- Local environment request plus 45 seconds returns no temperature. Sensor operation remains unverified; cached device values with uptime 3,065 seconds excluded. No gateway/portal delivery, physical INA219 removal or resolution of historical current discrepancy claimed. Other radios/live portal unchanged; preserve firmware pin/unrelated battery-box model. Local documentation links and whitespace checks pass.
- Release claim and leave issue Verify pending fitted-sensor/wiring/detection check and fresh temperature. CLI Project reconciliation remains pending the authenticated management host.

Next useful step: identify/back up the next connected repeater before updating; R005 has a historical dummy-load image exception to account for. Obtain fresh temperature reports from updated nodes before accepting sensor operation.

## 2026-10-19 — R003 CLIENT bench reflash

- Owner connects R003 for the same authorized CLIENT/temperature-only/no-INA219 rollout. Claim [Reflash R003 for CLIENT bench operation with temperature telemetry only](https://github.com/lfg-seth/snorr-meshlink/issues/28); identify RAK4631 `!05237743` by node/USB serial, save fresh complete private backup, verify pinned release cache and flash released neighbor-signal `2.7.26.0b65f2e` through matched UF2 bootloader. This replaces the earlier `cc5907b` AHT image while retaining its sensor fix; no rebuild/reset/key replacement.
- Independent full profile/identity/key/channel comparison passes through clock synchronization/explicit reboot: CLIENT, device/environment 900-second telemetry, disabled power measurements/display, unconfigured battery INA address and NeighborInfo over LoRa. Account for CLIENT-specific API sleep readback. [Operating evidence](../docs/operations/r003-client-bench.md), [TEST-017](field-results.md#test-017--r003-client-temperature-only-bench-reflash).
- Local environment request plus 45-second observation returns no temperature. Sensor operation remains unverified on the updated image; cached device metrics and historical sensor results are excluded as fresh evidence. Other radios/live portal unchanged. Preserve firmware pin and unrelated battery-box model. Documentation link/whitespace checks pass.
- Release claim and leave issue Verify pending fitted-sensor/wiring/detection check and fresh temperature. CLI Project reconciliation remains pending the authenticated management host.

Next useful step: connect the next repeater for individual identification/backup/update; obtain fresh temperature evidence from the updated bench nodes before accepting sensor operation.

## 2026-10-19 — R002 CLIENT bench reflash

- Owner connects R002 and requests the same CLIENT/temperature-only/no-INA219 configuration as R001. Claim [Reflash R002 for CLIENT bench operation with temperature telemetry only](https://github.com/lfg-seth/snorr-meshlink/issues/27); identify RAK4631 `!b456f760` by node/USB serial, save fresh complete private backup, reverify pinned release cache and reflash released neighbor-signal `2.7.26.0b65f2e` through matched UF2 bootloader. No rebuild/reset/key replacement.
- CLIENT, device/environment 900-second telemetry, disabled power measurements/display, unconfigured battery INA address and NeighborInfo transmission pass full independent readback through explicit clock synchronization/reboot. Identity/keys/channel/radio profile preserved; account for CLIENT-specific API sleep default. [Operating evidence](../docs/operations/r002-client-bench.md), [TEST-016](field-results.md#test-016--r002-client-temperature-only-bench-reflash).
- Local environment request and 45-second observation return no temperature. Keep actual sensor operation and fresh gateway/portal delivery unverified. Local device metrics are separate from delivery evidence. Other radios/live portal metadata unchanged; preserve unrelated battery-box model and firmware pin. Documentation link/whitespace checks pass.
- Release active claim and retain issue in Verify pending fitted-sensor/wiring/detection check and fresh temperature. CLI Project reconciliation remains pending the authenticated management host.

Next useful step: connect the next repeater for the same identity/backup/flash procedure; obtain fresh temperature readings from configured R001/R002 before accepting sensor operation.

## 2026-10-19 — R001 CLIENT bench reflash

- Owner requests repeater reflashes as CLIENT for bench testing, temperature sensors only and no INA219 configuration; connects R001. Claim [Reflash R001 for CLIENT bench operation with temperature telemetry only](https://github.com/lfg-seth/snorr-meshlink/issues/26). Identify RAK4631 `!a65601b3` by node/USB identity, save fresh private complete backup and verify the pinned release cache.
- Flash released `2.7.26.0b65f2e` directly through matched UF2 bootloader; preserve identity/keys/channel/radio profile without reset/rebuild. Save CLIENT, device/environment telemetry 900 seconds, power telemetry/display disabled and NeighborInfo over LoRa. Independent full readback passes after explicit reboot. API reports a role-dependent sleep default (300 seconds for CLIENT); other profile fields match the expected original plus intended changes. [Operating evidence](../docs/operations/r001-client-bench.md), [TEST-015](field-results.md#test-015--r001-client-temperature-only-bench-reflash).
- A local environment request and 45-second observation yield no temperature. Keep sensor operation, fresh gateway/portal delivery, cadence and utilization improvement unverified. Historical/cached battery/utilization data are not accepted as fresh evidence. Other boards and live portal metadata remain unchanged. Preserve unrelated battery-box model and firmware pin.
- GitHub CLI/Project access is unavailable on this Windows host; reconcile the derived board on the authenticated management host. Issue remains Verify with no retained active claim, pending fitted-sensor/detection check and fresh temperature evidence.

Next useful step: connect the next repeater for the same identity/backup/flash workflow; separately confirm R001's fitted temperature sensor/wiring and obtain a fresh report. No stock quantities, purchase, installation or field acceptance changed.

## 2026-10-19 — Cancel content work and merge MeshMonitor publication

- Owner cancels [Create a local SNORR MeshLink brag video](https://github.com/lfg-seth/snorr-meshlink/issues/25). Remove both local compositions, assets, caches, dedicated tooling and pending content/session entries; verify neither preview is running. Close the issue as not planned and release its assignment.
- Owner explicitly authorizes [MeshMonitor PR #24](https://github.com/lfg-seth/snorr-meshlink/pull/24). Merge the unchanged published head `a35e00f` with a merge commit, `f17a1e097d0d2230cef05e6cc3634d79452bb34b`, and close [deployment issue #22](https://github.com/lfg-seth/snorr-meshlink/issues/22) as completed. Preserve verification follow-ups [#23](https://github.com/lfg-seth/snorr-meshlink/issues/23) and [#7](https://github.com/lfg-seth/snorr-meshlink/issues/7).
- Fast-forward local main and retain its origin/main tracking. Preserve the unrelated battery-box model and firmware. No application or hardware changes; no new service/runtime acceptance claimed. GitHub CLI Project access remains unavailable on this Windows host; issue closures use the verified native Done workflow, with a full board reconciliation pending the authenticated management host.

Next useful step: resume phone-free GPS freshness/runtime and relay/outage verification; monitoring browser, second-gateway, growth and off-host recovery checks remain open.

## 2026-10-17 — Deploy private MeshMonitor with existing Grafana/Prometheus

- Owner authorizes MeshMonitor on its separate existing Ubuntu LXC, then supplies the existing Grafana/Prometheus hosts and selects internal access only, proposed retention and deployment. Resolve the one monitoring scope decision; claim [deployment](https://github.com/lfg-seth/snorr-meshlink/issues/22). [Operating evidence](../docs/operations/meshmonitor-lxc.md) records the exact release, private credentials handoff, boundaries and recovery.
- Verify official 4.17.0 LXC/application assets by release-API SHA-256. Install only application and bundled Node 24.21.0 into the existing LXC, preserving OS/accounts. Dedicated unprivileged systemd service, private persistent SQLite, explicit private IPv4 bind, random admin password, disabled anonymous account/mode and separate non-admin metrics token. Reuse existing read-only MQTT credentials with a distinct client ID; standalone subscribe-only TLS source, private channel key and MQTT packet log. No radio/broker/public-route change.
- Apply a version/seam-checked local no-pruning overlay: telemetry/packet/coverage/history cleanup guards plus explicit bind option. Five actual cleanup-body checks and JavaScript syntax pass. Latest recovery checkpoint retains four node rows, 21 telemetry rows and six ingested MQTT packet rows through one gateway. Four voltage/weather values match archived-byte decoding and stored portal observations. Existing GPS API/worker stay healthy.
- Add authenticated 30-second scrape and a separate Grafana folder/dashboard. All existing configuration/rules validate, original three dashboard specifications compare equal, all ten panel expressions query from Grafana, and per-node voltage/airtime metrics export. Existing 21 targets retain their health (four already down); the new target is up. Set server-wide Prometheus retention from 15d to agreed 30d, extending all series. No searchable logs, notifications, custom exporter or history import.
- Restart preserves every checked row ID and the accounts/keys/token, reconnecting MQTT with zero upstream publish/local republish counters. Daily 02:45 Pacific online SQLite/configuration backups retain 14 archives. Final isolated restored app boots with all external sources disabled in its disposable copy, passes integrity and exact retained row counts. Backups remain on the same disk; extend the existing [off-host recovery issue](https://github.com/lfg-seth/snorr-meshlink/issues/7) with this scope.
- [Verify MeshMonitor browser views, two-gateway behavior and storage growth](https://github.com/lfg-seth/snorr-meshlink/issues/23) owns remaining native desktop/mobile review, fresh G002, outage/replay and growth evidence. Upstream GPS observation times, packet-ID dedup, telemetry NULL-channel handling and absent MQTT protocol-count metrics differ from portal semantics; dashboard labels preserve the distinction. No field-readiness claim.
- Python compilation, installer execution/shell syntax, policy checks, real API/scrape/query checks and backup/restart recovery pass. Preserve the unrelated untracked battery-box model and unchanged firmware pin. GitHub CLI/Project authentication is unavailable on this Windows session; reconcile issue-derived board statuses with `scripts/github/sync-project.py --apply` on the authenticated management host at the next connected session.
- Publish implementation/evidence commit `42aa27a` on `codex/deploy-meshmonitor` and open [deployment PR #24](https://github.com/lfg-seth/snorr-meshlink/pull/24). No portal/backend CI run is triggered because existing path filters do not cover these separate deployment files. Automatic approval review rejects the attempted default-branch merge because explicit merge authorization is required. Leave the PR open and request that authorization; do not bypass the rejection. The live deployment is unaffected. This handoff note is a separate pushed follow-up commit.

Next useful step: open the two internal UIs with the private admin/existing Grafana login, review the views, then observe both gateways and measure storage growth under the scoped verification issue. Keep member GPS tracking first and existing archive/freshness semantics authoritative.

## 2026-10-17 — Open neighbor devices from minimap icons

- Owner requests removal of the neighbor card's separate Open device buttons, using the minimap endpoint icons instead. Search existing issues and claim [Open neighbor devices through minimap icons](https://github.com/lfg-seth/snorr-meshlink/issues/21). Thread optional selection through DeviceSheet to CardMiniMap; neighbor endpoints become named native buttons that select by persistent device identity and stop click propagation. Other device-card minimaps retain their current behavior. Remove the separate button group and unused styles.
- Add focused interaction coverage for both endpoint selections, assigned shortnames, updated callbacks, colocated icons, button/tab semantics and missing coordinates. Update the existing broad interaction check to expect minimap buttons. Preserve its pre-existing unfinished Endpoint locations assertions and all unrelated demo/application/session edits; do not remove the location section as part of this request.
- Verification: focused interaction check passes; 45 portal checks pass with the broad map/legend interaction test excluded. That broader test stalls in sandboxed and unsandboxed runs and is stopped; a previous session recorded the same test stall, so no full-suite pass is claimed. Typecheck/production build and Git whitespace checks pass. No browser surfaces are available for native keyboard, WebGL or visual review. Existing bundle-size warning remains.
- Local implementation only; no commit, push, deployment, hardware work or change to deferred priorities. Hand off the issue to Verify without retaining a session claim.

Next useful step: visually review the neighbor minimap icons and confirm each opens the matching device card; resolve the existing broad-test stall and unfinished endpoint-location expectations before a complete portal release check. Commit/publish the scoped UI changes when requested, preserving the unrelated work.

## 2026-10-17 — Recommend the next work from the live queue

- Owner asks what to work on next. Read the startup records and live GitHub issue queue, including acceptance criteria for phone-free tracking/runtime, forced relay/outage viewing, INA219 diagnosis and the unfinished demo release. Reconcile the Project from authoritative issue labels: 20 issues checked, zero changes needed; no active session claims appear in the open issue list.
- Recommend agreeing the B001/B002 battery-only trial plan first, then measuring automatic phone-free GPS freshness, both-gateway receipts and runtime against the 15-minute stale threshold, four-hour minimum and 12-hour target. Follow with controlled relay/outage verification. If radios are unavailable, review and finish the existing local demo work as a bounded software alternative. INA219 accuracy remains unresolved before power-design conclusions.
- Preserve all existing application/test/session edits. Recommendation only: no issue claimed, test run, hardware operation, deployment, commit or push performed.

Next useful step: agree the configuration, stale/missing acceptance rate and available hardware for [Measure B001/B002 phone-free GPS freshness and battery runtime](https://github.com/lfg-seth/snorr-meshlink/issues/2).

## 2026-10-17 — Install GitHub CLI and configure the Project board

- Owner requests management tooling and Project setup, then completes the separate CLI device authorization. Install official GitHub CLI 2.102.0 at `/home/setheth/.local/bin/gh`, already on PATH, after verifying archive SHA-256 `bb766f710eef8ede859c18578c72c327597cd4c8a85b06001b1f3843c6019386` against both release metadata and the published manifest (digest `afe49e9affa232faa8212aed035417166f6ade9b9470acb53d4dbd28c0504e8d`). Version and authenticated Project access pass; credentials are in the system keyring. No token/device code is published. [Official release](https://github.com/cli/cli/releases/tag/v2.102.0).
- Create the linked, default-private [SNORR MeshLink Project](https://github.com/users/lfg-seth/projects/2), preserving the unrelated closed Project. Configure Triage, Ready, In progress, Verify, Done and Deferred with preserved existing option identities. Create All work, Current work, Verification, Bugs and Deferred wishlist views; API readbacks verify filters/layouts and Status grouping on the three boards.
- Import all 20 GitHub issues, including completed migration history; preserve all seven deferred issues and existing labels/blockers. Keep issue labels authoritative. Add tracked Project configuration and a CLI-backed sync command that imports missing repository issues, derives board status from labels/closed state, refuses invalid open-status labels before writes, preserves unrelated Project items and verifies updates. Native auto-close/item-added/PR-linked/PR-merged defaults are removed; native Item closed → Done and Auto-add sub-issues remain enabled.
- Full-repository native auto-add creation/toggle is unavailable through the exposed API/CLI. The documented sync command supplies import and label-to-board reconciliation during sessions; no unattended full-repository sync or new GitHub secret is configured. Update README, tracking rules, roadmap and issue-entry links to the live board. Project stays private; public issue views remain available.
- Configuration/YAML/Python/status-guard checks pass. Initial import exposes delayed API readback on the last item; a later read confirms correct status, and the sync command now retries reads with a bounded delay without repeating mutations. Real setup-issue In progress → Verify synchronization passes, followed by a zero-change check across all 20 issues. Native browser visual review is unavailable; no application/firmware tests, deployment, hardware operation, purchase or deferred activation occurs.
- Preserve all pre-existing demo/application/test edits and earlier uncommitted session notes. Publish only the board setup source, documentation and this entry in `ac06bc3`. Close the completed setup issue after publication: native Item closed → Done passes on its real closure without running the sync writer. The final read-only check verifies all 20 issues with zero pending board changes.

Next useful step: use the board's Current work and Verification views during authorized project sessions, synchronizing from issue labels at startup and after updates. Run owner-agreed phone-free tracking/runtime and relay/outage trials before wider field rollout; native visual review and unattended synchronization remain separate follow-ups.

## 2026-10-17 — Migrate progress tracking to GitHub

- Owner adopts the proposed GitHub workflow. The authenticated GitHub MCP server creates the migration issue and 19 scoped work/verification/deferred issues, with type, area, priority, status and blocker labels. Preserve the 20 resolved historical questions as decision evidence; migrate the three unresolved questions with monitoring in triage and survey/WebSockets deferred. All three wishlist ideas remain deferred; future communications/rollout remain parked.
- GitHub Issues now owns current status and session claims; Markdown retains decisions, measurements and operating records. Update AGENTS.md, tracker/map entry points, successor links, README, project brief, development handoff, wishlist and evidence-based roadmap. Add public-safe bug/task/feature/test forms and a PR handoff template. Labels supply working status views without duplicate local queue maintenance.
- Add a narrowly scoped repository workflow to provision label metadata, three evidence-based milestones and initial issue assignments using the built-in issues-write token. Configuration validation, YAML parsing, Python compilation, local documentation links and isolated bootstrap simulation pass; the simulation verifies existing owner milestone preservation, no status writes and a zero-write rerun. Published source [d6b0487](https://github.com/lfg-seth/snorr-meshlink/commit/d6b0487d52b5e413c2c151bc3a431a3e9c9df882) triggers [Tracking setup](https://github.com/lfg-seth/snorr-meshlink/actions/runs/39065906423): both hosted jobs pass; 18 label definitions, three milestones and seven initial milestone assignments are verified. Representative bench, field and rollout issue readbacks confirm their milestone and preserved status.
- No Project management tools are exposed by the MCP server; no authenticated CLI or browser is available. [Finish GitHub Project board setup](https://github.com/lfg-seth/snorr-meshlink/issues/19) records this access gap and exact acceptance checklist. Filtered issue views are available meanwhile. No board, readiness percentage, deployment, hardware change, purchase or deferred-feature activation is claimed.
- Preserve pre-existing demo/application/test edits and earlier uncommitted session entries. Published only the coherent tracking migration paths and this entry; application checks are outside this documentation/metadata change. Existing main is synchronized with origin before publication.

[Migration issue](https://github.com/lfg-seth/snorr-meshlink/issues/1) is closed with published verification evidence; the separate board follow-up remains blocked. All pre-migration session-log changes are preserved exactly.

Next useful step: use the ready phone-free tracking and relay/outage issues for owner-agreed measured trials. Finish the Project board when a management surface is available.

## 2026-10-17 — Test the newly added GitHub MCP server

- Owner requests connection testing after adding the GitHub MCP server and completing device authorization. The new `mcp_server_github` connection successfully authenticates as `lfg-seth`, lists project issues and pull requests (both empty), and reads the main-branch workflow directory containing backend and portal CI definitions.
- Read access is verified through the new server rather than the existing GitHub app connector. Write access is untested; no GitHub records or settings changed. No Projects or milestone tools are exposed by the new server in this session. Preserve all existing local edits; no tests, deployment, hardware operation or commit performed.

Next useful step: use the authenticated server for the proposed issue workflow when adopted; separately establish Project/milestone management access if needed.

## 2026-10-17 — Fill demo data for current portal features

- Owner reports missing demo values for newer portal features. Reproduce through the real demo state endpoint: member voltage/pack settings, infrastructure battery profiles, humidity, sensor-power channels and SNNS report details are absent from the tracked checkpoint. Add shared fictional scenario values to the generator and simulation worker, then rebuild the synthetic checkpoint/manifest with the current schema. Preserve existing GPS-quality/history and unknown/stale/never-reported examples.
- Add 3000/1100/1000 mAh LiPo member examples, EVE 26V repeater profiles, humidity, signed/zero sensor readings on distinct channels and three SNNS observations demonstrating hearing age/counts and complete/partial coverage with capacity eviction. Keep radio signs independent of battery charging claims. Expand demo integration checks and let hosted recovery verification accept additional saved signal rows; restored row counts still match the backup. Update demo refresh documentation.
- Gracefully stop the identified local launcher, preserve its complete prior workspace as ignored `local-data/demo-before-feature-refresh-20261017-130037`, initialize the updated demo and restart the launcher. Local portal/API readiness, synthetic marker, thirteen signal rows, member voltage and humidity pass. Reload the local browser to obtain a fresh demo token. The old workspace and saved edits remain available in the backup.
- Verification: six demo integration checks pass, including worker refresh, saved-edit persistence, history windows and authentication boundaries. The broader system-Python suite passes 42 checks but cannot import MQTT tests without cryptography; run the 17 MQTT checks successfully using the existing project virtual environment (59 checks combined). Python compilation and Git whitespace checks pass. No hosted deployment or native visual review performed; the hosted demo keeps its existing database until deliberately refreshed after backup. Preserve the unrelated infrastructure-test edit and concurrent session notes. No hardware, tracker decision, commit or push performed.

Next useful step: reload the local portal and inspect member batteries, Infrastructure sensor power/humidity and neighbor relationship details; when releasing, refresh the separately backed-up hosted demo and run its proxy/isolation/recovery checks.

## 2026-10-17 — Review GitHub progress-tracking workflow

- Owner requests an assessment of current progress tracking and a suggested GitHub workflow. Review the local tracker, pilot map, project brief, session history, roadmap, wishlist and existing CI workflows; read GitHub issue/PR collections through the connected account. The local tracker has 23 tickets (20 resolved, three open), while GitHub returns no issues or pull requests. Local resolution includes design/research completion and must not be read as field-readiness completion. The roadmap still describes the October 12 snapshot.
- Recommend GitHub Issues and one Project board for execution status, with a distinct verification stage, deferred wishlist view, a small label set and evidence-based bench/field milestones. Keep local Markdown authoritative for decisions and measured evidence; link records rather than maintaining duplicate narrative histories. Preserve passive tracking first, communications second and later law-enforcement expansion. Parked ideas require explicit owner activation.
- Proposed session workflow: reconcile relevant issue/record state, claim authorized work, link implementation and validation evidence, distinguish code/deployment/hardware verification, and update the issue and session record at handoff. Establish the convention in repository instructions if adopted. Existing backend/frontend CI can support linked pull requests; code merges must not imply field-test acceptance.
- Suggestion only: no GitHub issues, board, labels, milestones, pull requests, tracker states or repository instructions changed. Milestone enumeration was unsupported by the connector, and account-level Projects were not inspected. Preserve all pre-existing local edits, including this session log. Read-only review and documentation update only; no tests, deployment, hardware operation or commit performed.

Next useful step: adopt the workflow, reconcile current work and verification gaps into a small initial issue queue, and refresh the roadmap from the current evidence before configuring the board. Avoid importing all historical decisions as active work.

## 2026-10-17 — Summarize project readiness and remaining work

- Owner asks for project state and what needs work. Review project brief, session history, pilot map/tracker, terminology, inventory, deferred wishlist and latest INA219 evidence. Recorded bench GPS/MQTT ingestion and deployed portal are working; six-member field readiness, sustained freshness/runtime, forced relaying and outage/local viewing remain unverified.
- Prioritize a measured two-tracker pilot using existing hardware, reliable power measurements and repeatable radio/load tests before wider rollout. Fresh G002 neighbor/power delivery, authenticated mobile review and off-host backups remain follow-ups; outbound messaging/remote administration, monitoring selection and the custom survey tool remain separate unfinished scope. Preserve deferred ideas.
- Local main tracks origin/main with pre-existing edits to this session log and the infrastructure test. Preserve both; do not treat the unfinished test expectation as implemented behavior. No live service/hardware inspection, tests, tracker changes, deployment or commit performed for this status review.

Next useful step: define and run a logged B001/B002 battery-only tracking trial, measuring GPS measurement age, delivery through both gateways, runtime and relay/outage behavior against the agreed 15-minute stale threshold and four-hour minimum runtime (12-hour target). Resolve sensor state/accuracy before using INA219 readings for power-design conclusions.

## 2026-10-17 — Review project state and pull desktop changes

- Owner requests repository/project status and a pull. Fetch origin and fast-forward `main` by 18 commits from `0e3d8dc` to `5c9c76a`; main matches `origin/main`. Initialize/update recursive submodules to the recorded firmware pin `d929b800909a6ee48254dbcb6d104d9c7f54ce5f`. Temporarily stash and then restore the existing infrastructure-test edit and automatic-deployment session note without conflicts.
- Latest records describe deployed RAK neighbor/signed-power ingestion (`bed40dd`), R002/R004 released firmware, the R005 dummy-load build and a dedicated V3 airtime sniffer. INA219 magnitude/calibration, fresh G002 delivery, sustained GPS/runtime/outage behavior and field readiness remain unverified. The later shunt estimate does not resolve the current discrepancy. Monitoring selection and direct-link survey work remain open/deferred.
- The pre-existing local test edit expects endpoint locations to be removed, while `SignalLinkDetail.tsx` still renders that section. Preserve the unfinished edit; no application fix is part of this sync. Start the targeted infrastructure test, but stop it after it produces only the TAP header and no test results; no test pass/failure established. Git whitespace and branch/submodule checks pass. No hosted-service inspection, deployment, hardware operation or new commit performed.

Next useful step: decide whether to finish the local neighbor-card change, or resume bench verification of the INA219 discrepancy and fresh G002 delivery. Preserve the existing local edits; source synchronization does not change the hosted portal or radio firmware.

## 2026-10-16 — Apply the reported probe resistance baseline

- Owner reports 0.16 Ω with the probe tips shorted on the same resistance range. Subtract from the removed shunt's 0.45 Ω reading to obtain an estimated 0.29 Ω; meter resolution/accuracy and changing contact resistance prevent treating this as calibrated. Update inventory and the INA219 audit.
- A true 0.29 Ω shunt with the firmware's 0.1 Ω calibration would scale current by 2.9×: 8–16 mA becomes 23.2–46.4 mA, still insufficient to explain roughly one amp. No calibration/configuration change, firmware flash or new assembled-board measurement performed.

Next useful step: establish actual shunt resistance and restored sensor state, then compare raw INA219 shunt/current/config/calibration registers under the same battery-only conditions. The original high-current cause remains unresolved.

## 2026-10-16 — Build and flash a dedicated Heltec V3 airtime sniffer

- Owner requests dedicated V3 capture, Windows/Linux GUI/script, every observed message including undecryptable traffic/repeats, useful decoded data and per-run logs; flashing authorized. Identify MC00 `!9ea0432c` on COM6, distinct from G001/G002. Preserve original full flash/profile/keys privately, then verify CLIENT_MUTE/TX/Wi-Fi/Bluetooth/MQTT off through reboot.
- Publish sniffer instrumentation `efca052b6` and required Wi-Fi-free OTA compile guard `f95a443bb` on the authorized firmware branch. Concurrent INA219 source `d929b8009` includes both and remains the project pin. Preserve concurrent sensor work and unrelated battery-box model. Build isolated exact source `f95a443bb` as `2.7.26.f95a443`; short temporary aliases solve Windows compiler command-length failure. Application-only flash/hash verification and independent version/identity/security/channel/RF readback pass. [Hardware/image/recovery](../docs/operations/airtime-sniffer.md).
- [GUI/CLI](../scripts/airtime-sniffer/README.md) captures raw receptions before firmware duplicate filtering/decryption, prints opaque ciphertext, decodes known-channel text/GPS/telemetry/neighbors/SNNS and retains every duplicate. Separate raw/JSONL/text/summary files per run, transport-gap detection, current/peak receive airtime and sender/relay-hint totals. Host sends no serial commands. Private host keys include original and current pilot keys; board channel keys are unchanged.
- Twelve Windows checks including Tk interaction pass; eleven Linux checks pass with GUI explicitly skipped for missing Tk/display; Linux launcher syntax and portable C++ sanitizer framing checks pass. Three-minute hardware capture has ten receptions/seven duplicates, all B002 GPS/R005 SNNS copies decoded, zero reported stream gaps, final receive airtime 10.27%. Keyless, keyed and GUI replays preserve exactly all ten frames; opaque full hex printing passes. [TEST-014](field-results.md#test-014--dedicated-heltec-v3-airtime-sniffer).
- UART status observes TX0/RX3/bad0; no Packet TX log appears. An optional later self-stat request times out, is not used by the capture tool and changes no setting. No external RF-silence measurement, high-load completeness, real RF-error event, 58% recurrence or native Linux USB/GUI claim. Close capture/API handles afterward; COM6 is free. Resolve [Build a dedicated Heltec V3 airtime sniffer](../.scratch/pilot/issues/23-airtime-sniffer.md).

Next useful step: run the GUI during a utilization spike and compare a deliberately scoped one-router bench run. Preserve the dedicated sniffer image/profile and existing gateway/repeater roles; raw logs/keys remain private. Git attributes keep the Linux launcher LF-only even in Windows checkouts.

## 2026-10-16 — Clarify the R004 series-current measurement

- Owner confirms **8–16 mA**, measured in series between the battery and INA219; `8016 mA` was a typo. Record the precise measurement path in the [INA219 audit](../docs/operations/ina219-audit.md). The owner reports unstable open-lead millivolt readings, so no usable physical R100 voltage-drop measurement is established. Open-lead behavior alone does not establish meter failure or low-voltage accuracy.
- No additional firmware/configuration/hardware operation is performed. The historical roughly one-amp discrepancy remains unresolved, and the tested source fixes remain unflashed.

Next useful step: check the meter's DC-millivolt zero with voltage-mode leads shorted, then obtain a usable R100 voltage drop or explicitly scope a diagnostic firmware build/flash exposing raw shunt/current/config/calibration registers on battery power. Preserve the owner's 8–16 mA result as reported evidence.

## 2026-10-16 — Audit INA219 current against R100 and the owner's meter

- Owner reports R004 showing about one amp without R005's dummy load, confirms R100 shunts and measures 8–16 mA on battery with a desk multimeter. Verify pinned Adafruit 1.2.3 calibration (0.1 Ω, calibration 4096, current divider 10), both RAK targets' default 1× multiplier, saved power/900-second telemetry settings, and signed unchanged MQTT/frontend units. No mismatched R100 calibration or portal scaling found. [Audit and evidence](../docs/operations/ina219-audit.md).
- Identify newly connected COM17 as R004 on unchanged `2.7.26.0b65f2e`. Read relevant config and request telemetry without a saved-setting change, explicit reboot or flash; close serial afterward. USB-connected local reports are −5.9/−5.8 mA; the portal receives −5.8 mA in both formats. Read-only database history confirms earlier R004 +939–1,071 mA in both environment/power reports and R005 near-full-scale values. USB readings are different conditions from the owner's battery-only measurement, not a calibration result. Actual shunt/register evidence remains pending.
- Publish firmware `d929b8009` on the authorized branch: fix wrong telemetry-union writes (PowerMetrics now channel 1), retain legacy environment readings, reject unsupported variants/failed I2C reads, and apply the existing multiplier consistently to the integer accessor. Reproduce channel and failed-read defects before fixing. Actual sensor/Adafruit/generated-layout harness passes zero, ±8, ±16, ±50 and ±1,000 mA, alternate 10× multiplier, and failed voltage/current reads in each format with address/undefined-behavior sanitizers. Twelve MQTT adapter checks pass. The channel bug does not inflate the float; a live I2C failure is not established as the one-amp cause.
- Isolated ordinary RAK build passes using base `8dd4dacef` plus the final INA219 source: 759,336 bytes flash / 105,252 bytes RAM. Preserve private build/capture evidence; inherited binary version filenames are not a new release identity. Trunk unavailable; pinned repository-configured clang-format/Black and whitespace checks pass. Existing public assets, hardware images, live database/history and unrelated sniffer/battery-box work are preserved. Pin published source in the project; no ticket decision or new release/flash claimed.

Next useful step: while the battery-only symptom is present, measure DC millivolts across R100 and compare the simultaneous sensor report. Expected 8–16 mA gives 0.8–1.6 mV; one amp gives 100 mV. The high-current discrepancy remains unresolved; no arbitrary scale correction, verified charging direction or sensor accuracy is claimed.

## 2026-10-16 — Diagnose a reported 58% channel-utilization spike

- Owner connects a Heltec V4 and reports 58% on both gateway/client OLEDs. Identify COM5 as stock `2.7.26.54e0d8d` B001 CLIENT. Save approximately 3.4 minutes of private serial/protocol evidence and local-destination statistics without flashing, rebooting or changing saved settings; close serial access afterward. Preserve unrelated battery-box model.
- Fresh utilization samples are 4.00%, 4.81%, 0%, 13.74% and 8.09%; B001 hourly transmit utilization is 0.515–0.535%. Observe two GPS transmissions and 19 receptions, 16 duplicates (84%), zero new bad receptions, zero B001 relay transmissions and three canceled pending forwards. B001 positions return through three/four routers; R005 environment/power/private reports each arrive directly and through three routers. [Sanitized readout and limits](../docs/operations/channel-utilization-diagnostic.md).
- Multiple reachable ROUTER nodes demonstrably amplify airtime. A transient repeated-traffic burst leads the explanation, but the earlier 58% event is not reproduced or precisely attributed; gateway logs and interference at the event time remain unobserved. Raw configuration, tracks and logs remain ignored under `private/bench/v4-util-20261016/`. No radio configuration or firmware fix is claimed.

Next useful step: capture an actual recurrence on client/gateway and compare a deliberately scoped one-router bench run. Documentation/whitespace verification only; no field coverage, sustained load or hardware configuration change.

## 2026-10-16 — Add RAK neighbor and sensor power ingestion

- Owner requests database/portal support for flashed RAK neighbor reports and INA219 sensors. Synchronize main, preserve the unrelated untracked battery-box model and retain the firmware pin. Add strict SNNS v1 and bounded standard NeighborInfo decoding, transactional private report/link storage and per-gateway receipt deduplication. Preserve unknown radio IDs, hearing ages/counts, boot/sequence/coverage metadata and unknown absolute hearing clocks.
- Normalize signed PowerMetrics channels 1–8 and legacy environment sensor voltage/current with independent field presence and original clocks. Future measurement checks use original receipt time, including replay. Show sensor/channel readings in Infrastructure and map node cards; extend neighbor tables/relationship cards and prevent delayed lower sequences from replacing newer same-boot reports. Do not map raw current to charging/discharging, battery voltage or solar output.
- Add dry-run-first, cutoff-bounded private archive recovery through normal ingestion. An isolated live database copy preserves all nine identities/configurations, accounts, assignments, positions and raw archive. Its 1,570 archived receipts yield 11 reports/15 directional rows and nine power supplements; second replay adds zero records (20 duplicates). R004/R005 power readings appear with literal channel/sign. Only G001 is represented; G002, calibration and field behavior remain unverified. [Contract and evidence](../docs/operations/radio-report-ingestion.md).
- Final LXC tests pass 57 backend and 45 frontend checks, TypeScript and production build, including final clock/order regressions; local decoder-only checks pass. Windows full checks are limited by missing frontend dependencies and sandbox temp/socket access. No hardware, profile, site or member data change.
- Publish/deploy application `bed40dd` after verified backup. Additive migration preserves all existing records in live and demo databases. Live archive replay accepts 12 reports/ten power supplements; fresh R005 power/neighbor normalization follows through G001. Final backup has 13 reports/21 link rows; all original protected/history/archive rows and device identities/configurations remain intact. Nine public assets, authenticated live state/feed, six services, public boundaries and isolated live/demo recovery pass. Restore verifies exact power/link metadata and zero-addition repeat replay (22 duplicates). [TEST-013](field-results.md#test-013--rak-neighbor-and-sensor-power-portal-integration).
- Initial demo readiness race recovers on bounded retry; private release-helper comparison/readiness errors are corrected without replacing live data. Native browser verifies published demo navigation/table/empty power state; populated fields are covered by DOM tests/live API. Sensor sign/calibration, fresh G002 and authenticated native/mobile visuals remain limited.

Next useful step: inspect the populated live UI on the owner's phone/browser, restore/verify fresh G002 delivery, and establish INA219 wiring/polarity/calibration before interpreting current as battery or solar behavior. Sanitized source/records are committed and pushed; raw captures/credentials remain private.

## 2026-10-16 — Recheck R005 with one full cell and a USB meter

- Owner reports replacing the disconnected batteries with one fully charged cell and observing 0.08 A on an inline USB input meter. Identify R005 on COM19, verify debug API remains off, refresh serial time and request fresh sensor data without a firmware/profile change.
- New PowerMetrics sample at epoch `1792206853` reports 4.200 V / −323.1 mA on the inherited observed channel 3; device voltage is 4.177 V. Preserve raw packet evidence separately from prior battery-disconnected captures. Record the USB reading as owner-observed total input; it does not isolate dummy-load draw or validate INA219 sign/calibration/common-path accounting.

Next useful step: establish the actual charger/INA219/load branch wiring and compare calibrated same-path measurements or a controlled load-on/load-off baseline. Expected 50 mA remains unverified; no charging-rate, endurance or calibration result claimed. Documentation/whitespace checks only; no build, flash or database schema change.

## 2026-10-16 — Build, flash and register R005 with an always-on dummy load

- Owner requests a one-off latest-project RAK build asserting the fitted dummy load while operating, then flashing the connected RAK as R005 and registering it at R001's saved location with INA219/temperature sensors. Read handoff/source instructions, synchronize clean repositories, preserve unrelated battery-box model. Identify RAK4631 `!f95b5501` on COM19; privately back up complete original configuration/keys. Owner confirms 2 kΩ base resistor to 2N2222 on RAK19007 AIN1.
- Publish firmware `8dd4dacef1cd7a6545983e3dc000ad533101113f` on authorized `snorr/rak-survey`: explicit `rak4631-r005-load` target holds P0.31 / GPIO31 HIGH at Arduino variant startup; ordinary RAK builds remain unchanged. Exclude conflicting Dropzone input use. Exact clang-format 16.0.3/whitespace checks, committed-source target build and linked startup/GPIO disassembly pass. Trunk unavailable. New version `2.7.26.8dd4dac`, UF2/OTA hashes and recovery evidence recorded in [R005 preparation](../docs/operations/r005-preparation.md).
- Match bootloader USB serial/RAK4631 board ID, flash verified UF2, apply saved pilot profile/name/900-second device/environment/power telemetry and neighbor transmission. Original US region and device security keys retained. Independent intended-profile/key readbacks pass before/after explicit reboot; final debug API off. A serial-close race after reboot raises an exception; independent post-reboot readback passes. No factory reset, bootloader replacement, other-board change or gateway configuration.
- Isolated database-copy identity rejection, idempotence and all-existing-device preservation pass. Apply identity-pinned manual registration, worker mapping and private recovery manifest; live authenticated state confirms nine devices and exact R001 planned-site equality, with unknown equipment/warnings disabled. G001 battery/weather normalization and SNNS/power archival pass; current/custom-neighbor normalized decoding and G002 delivery remain unverified. Final complete backup/public/authentication/isolated API-history recovery passes.
- Startup opens INA219 and AHT-family drivers. Initial current roughly −1.1 A at 4.184 V exceeds owner's expected 50 mA; owner suggests charging, disconnects batteries and confirms R100 shunt. Fresh post-disconnection local reports are −0.4 mA at 4.180 V and −0.3 mA at 4.188 V, with working temperature/humidity. Record measured reports separately from calibrated physical current; expected dummy-load draw is not verified. R005 database metadata captures this limit while all other device configurations are preserved. Raw data/keys/builds stay private.

Next useful step: establish whether battery removal also removed the dummy-load supply, then compare load voltage/current and INA219 readings with a meter under a known supply path. No field coverage/endurance, sustained cadence, sensor calibration or installed-site acceptance claimed. Source and project records are committed/pushed; see final response for project commit.

## 2026-10-16 — Update sensor-free R002 to released RAK firmware

- Owner connects R002 and requests update, confirming no external sensors. Preserve unrelated battery-box model; repository main is current. Identify COM9 RAK4631 `!b456f760`, snapshot entire current stock profile/keys privately, verify cached pinned UF2, match COM11/F: bootloader identity and install released `2.7.26.0b65f2e`. No rebuild/reset/key replacement, region or other-board change.
- Preserve exact original local configuration, channels, owner and hardware identity. Keep 900-second device telemetry; disable all external-sensor measurements and enable NeighborInfo/LoRa reporting at standard six-hour interval. Independent full readback passes before and after clock synchronization/explicit reboot. [Operation](../docs/operations/r002-release-update.md).
- Back up live portal, update only R002 firmware/no-sensor metadata through the local-only administration API and private provisioning manifest, preserving identity/site/equipment/other records. Authenticated portal and final backup recovery/public/proxy/authentication checks pass. No source/schema/frontend/worker identity change.
- Fresh R002 4.202 V device report reaches G001/MQTT and live normalized battery observation; fresh 40-byte SNNS v1 reaches G001/archive. No external-sensor report expected. G002 fresh delivery and normalized custom-neighbor decoding remain unverified. [TEST-011](field-results.md#test-011--r002-released-firmware-update-without-external-sensors).

Next useful step: verify the second gateway path and sustained reporting, or update the next explicitly requested board. No runtime/field coverage/calibration claim. Publish sanitized records; raw keys/settings/captures stay private.

## 2026-10-16 — Flash, configure and register R004

- Owner requests newly connected RAK as R004, latest firmware per notes, temperature sensor/INA219, and same location as R001. Read session/hardware instructions, preserve the unrelated untracked battery-box model, and fast-forward-check main (already current). Discover COM17 RAK4631 `!77fdb9f1`, formerly MR03/`2.7.17.36133d29d`, and privately back up the complete configuration/keys.
- Verify pinned cached release assets, identity-match COM18/RAK4631 UF2 bootloader and flash released `2.7.26.0b65f2e`; no rebuild/reset/key replacement or other board update. Set R004 naming and matching private pilot channel/radio, ROUTER/local-only, 900-second device/environment/power telemetry and neighbor transmit enable. Clear old fixed position, synchronize clock and independently verify the whole intended profile and original keys before/after explicit reboot. [Exact operation, hashes and evidence](../docs/operations/r004-preparation.md).
- Local temperature/humidity, battery voltage and INA219 legacy/PowerMetrics reports arrive. INA219 reports 0.008 V / about 1.6–1.9 mA while device voltage is about 4.1 V; wiring, calibration and the legacy union/channel mapping must be checked before battery-current/charging interpretation. No solar reading inferred.
- Add the guarded manual R004 migration after isolated invalid-identity/idempotence/preservation checks and backup recovery. Register R004 in live PocketBase/portal, copy only R001's private planned coordinates, record fitted sensors and leave R004-specific battery/antenna/solar unknown. Merge worker identity mapping, extend private provisioning manifest and verify eight-device authenticated state, preserved history, services, public boundaries and backup recovery. No application rebuild, demo change or new ticket decision.
- Fresh post-registration automatic battery packet (4.143 V) and environment packet (26.510239°C / 21.435547% RH) reach G001/MQTT and accepted live R004 observations with valid measurement clocks. A 40-byte SNNS v1 companion reaches G001/MQTT/archive; normalized neighbor/current decoding remains unsupported. G002's last receipt is October 15, so its fresh path and two-gateway deduplication are not verified. [TEST-010](field-results.md#test-010--r004-released-firmware-and-live-registration).

Next useful step: check INA219 wiring and meter readings on the intended power path, then restore/verify G002 delivery. Portal current/custom-neighbor decoding, sustained cadence/runtime, native browser visuals, site permission/installation and field coverage remain outstanding. Raw keys, tracks, exact locations and capture/configuration evidence stay private; stock counts/purchases are unchanged.

## 2026-10-16 — Publish cached RAK prerelease and download-first flashing

- Owner authorizes fixing inherited release automation, publishing the cached RAK build on their firmware fork and making future chats download it. Claim/resolve [Publish the cached RAK build as a fork prerelease](../.scratch/pilot/issues/22-rak-prerelease.md). Verify retained UF2/OTA ZIP against recorded sizes/hashes; reuse the exact tested bytes without rebuilding. Owner signs into GitHub to enable the authorized asset upload; no credentials are exposed or committed.
- Publish firmware release-only commit `8fe47325e38b82c8b2358293484ff845320d1be6` and tag `snorr-rak4631-2.7.26.0b65f2e-pre.1` on `snorr/rak-survey`. Gate all six upstream release jobs to `meshtastic/firmware`; add a read-only SNORR asset verifier, tracked manifest, integrity tests and release notes. Cached binary source remains `0b65f2e8444ea2dd3566f61ba2614d6eb33d3fd2`; the verifier rejects additional firmware/build-input changes between that source and the tag. No history rewritten.
- Publish [the RAK4631 prerelease](https://github.com/lfg-seth/firmware/releases/tag/snorr-rak4631-2.7.26.0b65f2e-pre.1) with UF2, Nordic OTA ZIP, build-manifest.json and SHA256SUMS, explicit bench/hardware-unverified status and source provenance. Public download/byte/hash/manifest checks and repeat-run cache reuse pass. [GitHub run 38994730691](https://github.com/lfg-seth/firmware/actions/runs/38994730691) succeeds: SNORR verification passes; Docker/PPA/OBS/COPR/upstream website/version-bump jobs all skip.
- Update the firmware pin, AGENTS/project/operation/handoff notes and add `scripts/bench/download-rak-release.py`. Routine flashing downloads/checks pinned assets into ignored private cache; it does not rebuild or flash. Six verifier regressions and YAML repository/permission checks pass; use pinned Black 26.5.1 with Trunk unavailable. Verify documentation links/whitespace; preserve the unrelated battery-box file. No binaries, private profiles, raw logs/tracks or credentials enter Git.

Next useful step: use the download helper in a named-board flashing chat, preserve identity/configuration and verify new RF/MQTT/portal evidence separately. No hardware flash, device configuration, sensor calibration, field/runtime test or portal deployment performed.

## 2026-10-16 — Save a reusable board flashing and configuration handoff

- Owner clarifies INA219 placement inline between battery and RAK and asks whether a new chat can recover the flashing/configuration notes. Record that owner-reported wiring in inventory without inventing sensor counts, per-board allocation, charger junction, polarity/calibration or measured current. Treat the sensor as battery/load-path sensing; total battery charging/discharging interpretation awaits the actual charge path, and solar-input measurement is unsupported by this placement.
- Existing RAK source/build evidence and checksums were already published in project commit `3756b0b` and firmware `0b65f2e84`. Add [Board flashing and configuration handoff](../docs/operations/board-flashing-handoff.md) as the single starting point for future chats, linked from AGENTS.md, README and development handoff. Record the owner-authorized firmware fork destination to prevent repeating the resolved publishing question.
- Save the previously chat-only portal-gap assessment: neighbor/current ingestion, INA219 packet channel/sign verification, GPS quality flags, sensor cadence/health clocks, live messaging/admin gaps, intrusion mapping and pinned gateway TLS/logging issue. Separate current support from pending integration; link source and measured evidence. Include a scoped example request for R003 that preserves keys/profile, performs the intended normal update and verifies new gateway traffic without a factory reset.
- Documentation/inventory only: no firmware, configuration, hardware state, source pin, live service, tracker decision or credential changed. Check local documentation links and Git whitespace; preserve the unrelated untracked battery-box model.

Next useful step: in a new chat, request a named board update using the handoff. Rediscover the board, privately snapshot configuration and choose the pinned target before writing; verify RF, MQTT and portal ingestion separately and record measured outcomes.

## 2026-10-16 — Implement passive RAK neighbor signal reports

- Owner asks whether the RAK branch already has richer neighbor signal information and brings implementation forward if missing. Fetch both remotes; firmware `snorr/rak-survey` remains at `cc5907b1f`, containing the AHT fix only. Claim [Improve passive neighbor signal reporting in the RAK fork](../.scratch/pilot/issues/21-rak-neighbor-signals.md). Preserve the unrelated untracked battery-box model.
- Commit firmware source `0b65f2e84`: primary-channel direct-reception RSSI/SNR, monotonic hearing age and accepted observation counts; bounded 32-entry table, least-recently-heard eviction, 30-minute expiry and rotating eight-row/152-byte private-port companion reports. Retain AHT support and standard GPS/NeighborInfo. Existing enable/transmit settings gate the module; no saved radio setting changed. Background priority, jitter, airtime admission and five-minute radio minimum keep diagnostics conditional. [Contract and rollout boundary](../docs/operations/rak-neighbor-signals.md).
- Collector and actual-module harness checks pass with address/undefined-behavior sanitizers, including zero/negative SNR, unknown/relayed/MQTT rejection, encoding, bounded rotation/eviction, expiry, primary-channel/configuration/airtime/role gates and cooldowns across timer rollover. Collector passes capacities 32 and 10. Trunk is unavailable; exact clang-format 16.0.3 repository configuration and whitespace checks pass. Initial target compilation caught an incorrect packet-release API call, fixed before the commit. Final committed-source build succeeds as `2.7.26.0b65f2e`: 759,256 bytes flash, 105,252 bytes static RAM. Preserve artifacts/log/checksums privately and record hashes in operations; runtime allocation peaks remain unmeasured.
- Automatic approval review initially rejects pushing to `git@github.com:lfg-seth/firmware.git` because standing publication authorization names the project repository. Owner first requests keeping the work in this repo, then identifies the firmware fork and explicitly authorizes pushing there. Remove the temporary patch packaging/version-helper change; push succeeds on `snorr/rak-survey`, with a clean firmware checkout and exact local/remote commit match. Pin the published firmware in this repository and resolve the source task. No history rewrite.

Next useful step: separately implement/test portal `SNNS` decoding and arrange an authorized bench flash with both-gateway delivery/GPS-airtime-runtime comparisons. No hardware flash, gateway provisioning, portal deployment, measured RF delivery or field validation performed. The unrelated battery-box model remains outside the commits.

## 2026-10-16 — Deploy demo-first entry and iPhone login fix

- Owner requests push and deployment. Commit/push application source `60ea977` to `origin/main` and deploy its frontend source/static assets to the LXC. Anonymous production entry now opens the separate database demo with Sign in at the top; live session restoration and independent API routes remain intact. Username/password inputs have a minimum 16px font. No backend/schema, radio or provisioning change.
- All 43 frontend checks, typecheck and live build pass on the pinned server runtime after adding the same commit's synthetic test fixture to staging. All nine released files match through public HTTPS; public synthetic sign-in/state and the published input font rule pass. Live state/device identity, worker heartbeat, protected routes, authentication throttling, demo isolation and all six services pass. Pre/post-release backups pass isolated live/demo database/API/history recovery, preserving the MQTT archive. [Release and rollback evidence](../docs/operations/portal-lxc.md#demo-first-entry-and-iphone-login-fields--2026-10-16).
- Native browser inventory is empty; iPhone focus/keyboard and visual behavior remain unverified. Preserve the concurrently added branch-build/automatic-deployment session note outside these commits. Existing bundle-size warning remains; no fresh radio reception or field-performance verification claimed.

Next useful step: open the public site on iPhone, confirm automatic demo entry and top-header sign-in, then focus/dismiss both login fields and verify manual pinch zoom. Publish deployment evidence separately from the application release.

## 2026-10-16 — Review branch builds and automatic deployment requirements

- Owner asks whether branch pushes can build/deploy automatically. Inspect both tracked GitHub Actions workflows: relevant pushes to `main` and pull requests run frontend tests/typecheck/build or backend integration checks; manual dispatch is available. The portal workflow saves a seven-day build artifact only for pushes to `main`. Direct pushes to other branches without a pull request do not trigger these workflows. No automatic application deployment workflow is tracked, consistent with the LXC operations record.
- Explain a proposed setup: branch CI, a designated deployment branch/environment, a secure deployment connection to the existing private LXC, and a repeatable update script gated on successful checks for the same commit. Reuse backup/recovery verification, preserve independent live/demo state and private credentials, publish tested assets, serialize deployments and record source/rollback releases. PocketBase uses `--automigrate=false`; migration execution and schema-compatible rollback need explicit handling. The simulation installer refuses live provisioning and is not the live update command.
- Verify GitHub trigger, self-hosted runner and deployment-environment capabilities against [workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), [runner documentation](https://docs.github.com/en/actions/concepts/runners/self-hosted-runners) and [environment documentation](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments). No branch policy is accepted, pipeline implemented, server accessed or application deployed. GitHub settings, runner availability and latest hosted run results were not inspected. Documentation-only session note; no application tests run and no commit requested.

Next useful step: choose the automatic deployment branch and whether other branches need an isolated staging portal, then implement the deployment workflow and live update script with the selected private connection.

## 2026-10-16 — Default to the database demo in production builds

- Owner requests demo-first startup even in production, retaining Sign in at the top. Remove the live-build restriction from anonymous demo startup and relabel the existing header action **Sign in**. Keep the production build's live account form and independent demo API routing; saved live tokens still undergo server validation before opening the live workspace. Anonymous refresh returns to the demo; sign-out clears the live token and offers the account form/View demo.
- Keep Sign in available while the demo loads; cancel the pending demo attempt when it is selected so a late response cannot replace the account form. Failed or misdirected demo responses expose sign-in without rendering fallback fixtures. Preserve the preceding iPhone input-font fix.
- Update the real-application DOM regression for production demo startup, header placement, refresh, demo read/write isolation, unavailable/misdirected databases, cancellation during loading and live sign-in restoration/rejection. The changed test fails before the application fix and passes after it. `npm run check` passes all 14 reported frontend test files, typecheck and the default live production build. Whitespace checks pass; existing MapLibre size warning remains. Native browser/iPhone visual and keyboard behavior remain unverified.

Next useful step: deploy both portal changes and verify anonymous demo entry, top-header sign-in and iPhone field focus on the public site. Local source/build only; no commit, push or deployment performed.

## 2026-10-16 — Prevent iPhone sign-in field focus zoom

- Owner reports iPhone automatically zooming into the mobile login fields. Those fields inherit the assignment form's `0.77rem` text size (about 12px at the default root size). Add a scoped `.backend-login input` font size of `max(16px, 1rem)` so both fields remain readable without reducing larger user font settings. Preserve the existing viewport and manual pinch zoom.
- `npm run check` passes all 14 reported frontend test files, typecheck and production build; `git diff --check` passes. Existing MapLibre chunk-size warning remains. Native iPhone focus/keyboard behavior is not reproduced or verified here; no artificial CSS-only regression test added for browser behavior. [WebKit focus-zoom implementation](https://github.com/WebKit/WebKit/blob/main/Source/WebKit/UIProcess/ios/WKContentViewInteraction.mm) uses the focused field's font size when revealing it.

Next useful step: deploy the CSS fix and verify username/password focus, keyboard dismissal and manual pinch zoom on an iPhone. Local source/build only; no commit, push or deployment performed.

## 2026-10-16 — Publish and deploy accumulated local changes

- Owner requests pushing and deploying all local changes. Commit/push application release `3ca3a94` to `origin/main`, retaining tracking against `origin/main`. Include GPS quality, separate database demo, neighbor table/signal map, card mini maps/labels, battery history, research/tracker records and the existing clean stock-firmware submodule pointer. No hardware flash or monitoring-stack implementation performed. Use the repository's established author identity for this commit because this machine has no Git identity configured.
- Frontend tests/typecheck/live production build and all 52 backend checks pass locally and on the LXC; its pinned Node runtime reports 43 frontend checks. The initial restricted backend run could not open localhost sockets; the authorized rerun passes. The known MapLibre bundle-size warning remains. Both additive migrations pass on a private live database copy and on the live database, preserving fingerprints of every pre-existing operational table and all seven device identities. Live signal rows remain empty.
- Deploy exactly committed application source to the owner-authorized LXC. Add the separate `meshlink-demo` OS account, loopback API and synthetic worker, independent state/binary and `/demo-api` Nginx proxy. Verify live/demo tokens and OS access boundaries; keep worker/administration/raw collections private. Public synthetic demo sign-in, history and all nine build files pass through HTTPS; live authenticated state, worker heartbeat, all 15 history queries, proxy boundaries, authentication throttling and all six services pass. [Release/backup evidence](../docs/operations/portal-lxc.md#gps-neighbor-maps-battery-history-and-database-demo-release--2026-10-16).
- Retain rollback source/assets/configuration at `/opt/meshlink-rollback-3ca3a94` and the staged tested build at `/opt/meshlink-release-20261016`. Pre-release backup restores successfully. The first post-release demo recovery check catches an older installed backup helper: install the updated `/usr/local/sbin/meshlink-backup` used by systemd and take a corrected complete backup. Replace the verifier's incorrect fixed sample-count expectation with exact comparison to saved samples. Final backup `meshlink-20261016T211956Z.tar.gz` passes checksum and isolated live/demo database/API/history recovery, including the private MQTT archive.
- Existing archive verification checks 200 recent envelopes/binary lengths with SQLite integrity good and no queued receipts. No new MQTT archive receipt arrives during the 60-second post-release observation window, so fresh radio ingestion and new quality-bearing fixes are not revalidated; the broker-connected worker heartbeat passes. Native browser/WebGL/mobile review remains unverified because browser inventory is empty; real neighbor ingestion, field validation and off-host backup remain open. Raw state, credentials and tracks stay outside Git.

Next useful step: visually review the deployed map, node/relationship cards and battery periods on desktop/mobile, then verify new GPS-quality-bearing packets when the bench reports. Real neighbor ingestion remains a separate integration; monitoring choices remain open and parked firmware/wishlist work stays parked.

## 2026-10-16 — Explore private Meshtastic monitoring and recording

- Owner invokes Wayfinder to investigate current Meshtastic monitoring/Grafana projects and setup requirements. Claimed [Check Meshtastic monitoring and recording stacks for the pilot](../.scratch/pilot/issues/19-meshtastic-monitoring-research.md); research completed in an isolated worktree/branch, preserving all unrelated staged and unstaged changes. Resolved the research only; no implementation decision is resolved.
- Primary-source comparison identifies MeshMonitor's standalone subscribe-only MQTT, Prometheus/Grafana assets and Proxmox LXC template as the leading packaged trial; tcivie's encrypted MQTT/TimescaleDB/Grafana bundle is the SQL alternative. MeshView/Malla need TLS adaptation in inspected clients; hacktegic's exporter skips encrypted packets. Source findings are not runtime compatibility tests.
- Record a [proposed private setup](../docs/research/meshtastic-monitoring-setup.md): preserve exact PocketBase archiving and portal GPS semantics, distinguish numeric metrics from logs, evaluate a private read-only collector, and verify dual-gateway receipt/dedup behavior and timestamps. Existing 4-CPU/8-GiB/64-GiB allocations are recorded; current free headroom is unmeasured. Loki/Alloy can follow metrics; retention/access/hosting remain proposals.
- Push the primary-source report on `research/meshtastic-monitoring-20261016`, commit `f69b6a4`; no PR/merge. Create [Choose a private monitoring scope and pilot stack](../.scratch/pilot/issues/20-monitoring-scope-stack.md) as the owner decision after the research. No radio, firmware, MQTT ACL, production service, inventory, expense or notification integration changed; parked wishlist and fork work remain parked.

Next useful step: choose whether to evaluate MeshMonitor plus Prometheus/Grafana first, or a narrow exporter on the existing worker, and whether log search belongs in that initial evaluation. Research-branch publication status is recorded in the research ticket; the main-worktree setup/tracker/session edits remain uncommitted. No application or hardware tests run; documentation/link and whitespace checks only.

## 2026-10-16 — Attempt to inspect legacy MQTT messages

- Owner requested a quick private inspection for the latest old messages and timestamps. SSH to the broker succeeds using the recorded port, but root-only archive inspection stops at `sudo: a password is required`. No archived file metadata, logs or payloads were read; no live broker changes made.
- Network sandbox required an approved external SSH call; the default local SSH configuration also has a permissions error, bypassed with `-F /dev/null`. Archive content and recoverable timestamps remain unknown.
- Owner supplied a privileged listing and latest-log tail: archived `mosquitto.db` is 47 bytes; logs include the current file, `.1`, and six compressed rotations. Mosquitto 2.0.18's [persistence writer](https://github.com/eclipse-mosquitto/mosquitto/blob/v2.0.18/src/persist_write.c) and [fixed structures](https://github.com/eclipse-mosquitto/mosquitto/blob/v2.0.18/src/persist.h) make 47 bytes consistent with header/configuration only, indicating no saved message records (inferred from size, not a binary parse). Supplied tail contains saves, failed connections, restarts and the audit rejection, with no successful message receipts. Final shutdown/save was October 13 at 13:44:08 Pacific; this is not a last-message timestamp. No remote IPs or raw log lines copied into Git.

Next useful step: search all archived log rotations for successful client connections or any PUBLISH logging to establish the latest recorded legitimate activity; ordinary log levels may not establish last-message time or contents. Existing unrelated edits preserved; no commit or push requested/performed.

## 2026-10-16 — Clarify legacy Mosquitto archive and message history

- Confirmed from the recorded October 13 reset and its installer that legacy configuration, data and logs were moved to the broker's private `/root/meshlink-archive/mqtt-legacy-20261013T204408Z` after stopping Mosquitto to flush persistence. Archive contents and recoverable message counts remain uninspected; this review did not access the server.
- Checked the official Mosquitto configuration/MQTT manuals: retained messages and persistent-session queues can preserve limited message state; broker persistence is not a complete traffic history. The fresh broker installer enables persistence. Separate full-payload worker archiving began October 15 and only covers delivered traffic, subject to broker ACLs and delivery gaps.

Next useful step if historical recovery is requested: inspect the legacy archive's file metadata and any persistence database privately, without changing the live broker. Existing unrelated edits preserved; no commit or push requested/performed.

## 2026-10-16 — Minimal battery history on repeater and gateway cards

- Add a compact voltage chart to repeater/gateway map cards and reuse it in Infrastructure battery detail. Provide 24hr/7day/30day buttons, small axis values and a single smooth monotone line without dots, grid, area fill or cursor. Curves stay within adjacent readings and leave battery missing-timeout gaps disconnected. Keep unknown/invalid/future readings out of the plot; preserve current/stale/offline indications and recent exact readings in the detail disclosure.
- Add an authenticated, no-store, on-demand history route and device/time index migration. Admin/member access follows the existing infrastructure snapshot; worker/anonymous access is denied. Bound each period to the latest 50,000 observations with explicit truncation. Refresh selected history once a minute, merge recent snapshots, abort obsolete device/period requests and retain loaded readings on refresh failure. The ordinary two-second state snapshot remains small.
- Rebuild the synthetic checkpoint with 17,283 timed voltage examples covering 30 days: Demo ridge relay recovers daily with sun cycles, Demo canyon relay shows daily charging but a roughly 0.51 V monthly deficit, and Demo dispatch gateway stays nearly steady. Update the simulation worker to continue all three patterns from a persisted/rebased scenario clock. These are fictional examples, not solar sufficiency diagnoses or measured runtime.
- Back up the running local demo privately, refresh only its illustrative voltage history/configuration, and restart its verified launcher so the new route and worker are active at localhost:5173. Through the actual frontend proxy, verify all three periods, separate simulation identity and online feed. Saved members, assignments and neighbor observations exactly match the pre-refresh backup; synthetic checkpoint checksum and SQLite integrity pass.
- Frontend checks/typecheck/default live build and all 52 backend checks pass, including real-database history windows/access, solar cycles/deficit, curved bounds/outage gaps and rapid period/device switches. Native browser visual review remains unavailable (empty browser inventory); existing MapLibre bundle-size warning remains. Preserve prior staged/unstaged edits; no production deployment, hardware change, commit or push requested/performed.

Next useful step: review repeater/gateway cards in the running local demo, comparing 24hr with 7day/30day on the two relays. Deploy the history hook and index migration with the frontend when a release is requested.

## 2026-10-16 — Match mini-map marker styles and states to the main map

- Replace the generic mini-map badge with the main map's shared marker classes/CSS. Share class selection for client GPS age and infrastructure type; tracker and infrastructure node cards retain the matching selected outline. Relationship endpoints use their own current status and update as time or position records change. Preserve assigned member shortnames, map framing, signal lines and button-free mini maps.
- Regression checks compare actual main/mini marker classes and computed colors, dimensions, shape, borders, shadows and selected outlines. Cover Active/Recent/Stale/No Location transitions in relationship and node cards, plus Users and gateway styling. Frontend tests, typecheck, production build and whitespace checks pass; the existing bundle-size warning remains. Native WebGL/visual review remains unverified. Preserve unrelated edits; no deployment, database/radio change, commit or push performed.

Next useful step: visually review matching marker states in local node and relationship cards.

## 2026-10-16 — Assigned member shortnames on card mini maps

- Reproduce the owner's reported mismatch in the actual Map card: the main marker displays the assigned member shortname ALIAS while its mini map displays S001. The tracker mini map directly used the device shortname, and relationship mini maps used device-labeled endpoints. Reuse the existing assignment-aware map-label function for Map/Users tracker cards and client endpoints in relationship mini maps. Device shortnames remain the fallback when no active member shortname exists.
- Add regression checks for assigned clients, relationship endpoint labels, assignment release restoring the device label and Users cards. Observe the ALIAS-versus-S001 assertion fail before the fix. Frontend tests, typecheck and production build pass; whitespace checks pass. DOM adapters verify labels; native visual review remains unverified and the existing bundle-size warning remains. Preserve unrelated edits; no database/radio change, deployment, commit or push performed.

Next useful step: review assigned client markers in the local node and relationship cards.

## 2026-10-16 — Minimal maps in node and relationship cards

- Add a lazy-loaded mini map to tracker/member-client and infrastructure detail sheets, including gateway/router cards and tracker cards opened from Users. Each shows only its node. Relationship cards show just the two endpoints and their existing signal-colored connection, independently of the main signal overlay. Reuse the main map style and worker setup; share Topo/Aerial imagery selection across cards and page navigation for the current app session.
- Center single nodes and fit both relationship endpoints with padding and a zoom cap, including on sheet resize. Keep panning/touch zoom available, omit map buttons, preserve visible USGS attribution and allow card scrolling over maps. Separate labels for co-located endpoints. Unknown/invalid positions remain explicit; missing endpoints never produce invented locations or lines. Existing planned/recorded-location details remain available.
- Frontend tests, typecheck and production build pass, including marker isolation, framing, line geometry/color updates, synchronized basemap changes, gateway cards, Map-to-Users navigation and unknown positions. DOM/MapLibre adapters verify behavior; browser inventory is empty, so native WebGL, tiles and desktop/mobile visual review remain unverified. Existing bundle-size warning remains. Preserve unrelated staged/unstaged work; no deployment, database/firmware change, commit or push performed.

Next useful step: visually review single-node and relationship mini maps in the local demo on desktop/mobile.

## 2026-10-16 — Restore assigned-device map shortnames in the database demo

- Reproduce the S00X fallback against the tracked synthetic database and the actual map-label function: all five saved member shortnames were blank after replacing browser fixtures with database-backed demo state. Assignment lookup and marker rendering still worked; existing UI tests supplied their own member shortnames and missed the checkpoint omission.
- Seed AVERY/JORD/MORG/RILEY/CASEY in the demo generator and rebuild its synthetic checkpoint/manifest. Restore only blank shortnames for matching fictional members through the running local demo API; preserve saved assignments and signal edits. Verify the frontend's `/demo-api` proxy now yields AVERY/JORD/MORG/RILEY for assigned devices and S005/S006 for unassigned ones. No production or radio changes.
- Add a regression test that reads saved members/assignments/devices from the actual checkpoint and runs the map-label function. Observe the exact failure before fixing it. All 41 frontend tests, typecheck/build and three demo-database integration checks pass; whitespace checks pass. Existing MapLibre bundle-size warning remains. Native browser visual review remains unverified. Preserve unrelated staged/unstaged work; no commit or push requested/performed.

Next useful step: review the restored names in the running local map; its normal polling reads the corrected saved records.

## 2026-10-16 — Rename node-card list to Neighbors

- Replace the map node-card heading and accessible section label Relationships with Neighbors, and align the empty-state message, existing test expectation and portal guide. Text-only change; whitespace checks pass. No tests rerun, deployment, commit or push performed; unrelated edits preserved.

Next useful step: review the Neighbors list in the local demo.

## 2026-10-16 — Relationship card endpoint buttons

- Extend [Show neighbor signal connections on the map](../.scratch/pilot/issues/18-map-neighbor-signals.md) with two Open [node] buttons at the top of each relationship card. Each opens its tracker or infrastructure card in place; its relationship row can return to the relationship card. Reuse tracker marker-selection behavior, including parent selection and trail clearing, and retain exactly one open card with the overlay either on or off.
- Frontend tests, typecheck and default live build pass, including navigation through both endpoint buttons and back through relationship rows on desktop/mobile dialog APIs. Whitespace checks pass; native browser visual review remains unverified and the existing MapLibre bundle warning remains. Preserve unrelated edits; no service start, deployment, database/firmware change, commit or push performed.

Next useful step: review node → relationship → either node navigation visually in the local demo.

## 2026-10-16 — Simplify signal lines and add node relationships

- Refine [Show neighbor signal connections on the map](../.scratch/pilot/issues/18-map-neighbor-signals.md) at the owner's request: remove all line labels, retain colored/selectable lines, hide legend explanations behind an accessible info button and place the legend outside toolbar flow so only its own box expands. Align toolbar controls at the top to prevent stretched buttons.
- Preserve tracker/infrastructure marker selection above line targets by stopping marker click propagation and ignoring marker-originated layer clicks. Map node cards now show only a relationship and colored SNR pill per relationship row; selecting the row opens the full relationship sheet. Lists and details work with the overlay off and with known endpoints lacking coordinates. Turning the layer off changes visibility without dismissing cards. No readings or explanatory copy are added to the compact rows.
- Frontend tests, typecheck, default live build and explicit demo build pass, covering no map labels, collapsed/revealed legend help and isolated CSS layout, marker click precedence, compact tracker/infrastructure relationship rows, relationship selection on desktop/mobile, retained offline/live updates and access without GPS or the overlay. Existing grouping/timestamp/unknown-value checks remain passing. Native visual/WebGL review remains unverified; existing MapLibre bundle warning remains. Preserve prior edits; no database/firmware change, service start, deployment, commit or push performed.

Next useful step: review the simplified map and node-to-relationship interaction visually in the database demo.

## 2026-10-16 — Map neighbor signal overlay

- Implement [Show neighbor signal connections on the map](../.scratch/pilot/issues/18-map-neighbor-signals.md): Show/Hide signal strength toggle beside and styled like Fit area, colored geographic lines, directional SNR label buttons and selectable responsive detail sheets. Use the existing authenticated/demo API link records; preserve unrelated edits.
- Group one connection per known mapped pair, retaining both directions/report sources without inventing reverse reception. Color by the weakest finite SNR among latest readings per direction/source (green ≥5 dB, amber 0–<5 dB, red <0 dB, neutral unknown); these are display bands, not receiver limits or delivery guarantees. Known hearing times order delayed reports; a newer missing reading never borrows an older SNR. Unknown final-hop identity never becomes an original-source connection.
- Cards show SNR/RSSI including zero/missing readings, separate hearing and report timestamps with ages, path/original source, loaded observation count and recorded/configured/planned endpoint context. Labels support keyboard activation, lines have wider pointer targets, selection replaces existing cards, feed loss retains observations and basemap changes preserve the overlay. Lines depict displayed endpoint locations, not measured RF paths or historical endpoint positions.
- Full frontend tests, TypeScript/default live build and explicit demo build pass; focused grouping and React interaction checks cover missing identities/coordinates, delayed reception, weaker reverse SNR, live updates, line/label selection, empty state, toggle cleanup and mobile/desktop sheet API behavior. Whitespace checks pass. Native browser/WebGL visual review is unavailable (browser inventory empty); existing MapLibre bundle-size warning remains. No service start, deployment, database/firmware change, commit or push requested/performed.

Next useful step: review the overlay visually with the database demo; existing real signal ingestion remains a separate integration task before live observations can populate it.

## 2026-10-16 — Simple local development README

- Add root `README.local.md` with startup, one-time setup, portal/dashboard URLs, public demo credentials, member sign-in, stop behavior, build/check commands and writable/checkpoint database paths. Link it from the main README. Check local documentation links and whitespace; no source or runtime changes, tests rerun, commit or deployment. Preserve existing edits and keep local services stopped as requested.

Next useful step: follow the short README when local development resumes.

## 2026-10-16 — Stop local demo services

- Owner requests stopping local development. Confirm the demo PocketBase on localhost:8092 and its synthetic worker are running; the frontend on 5173 is already stopped. Stop the identified worker first, then its demo server supervisor, and verify neither 5173 nor 8092 accepts connections. Preserve the demo database and all working-tree edits; no production service, commit or deployment changes.

Next useful step: run `python3 backend/launch.py` when local development resumes.

## 2026-10-16 — Local launch and build commands clarified

- Confirm existing `python3 backend/launch.py` supervises the separate demo PocketBase (8092), simulation worker and Vite (5173), preserving the writable demo database and stopping its children on Ctrl+C. It requires initialized demo state/dependencies and refuses occupied ports.
- Confirm repository-root frontend commands: `npm --prefix portal run build` for the default live production build, `VITE_PORTAL_MODE=demo npm --prefix portal run build` for the explicit database-demo build, and `npm --prefix portal run check` for frontend tests plus build. First-time setup remains in the demo guide. No service, source-code, database, deployment or commit changes performed; existing edits preserved.

Next useful step: use the launcher after stopping existing local services, or run the documented build/check command as needed.

## 2026-10-16 — Database-backed demo and neighbor signal table

- Owner keeps the fork proposal parked and requests a neighbor table populated from a separate inspectable PocketBase with its synthetic database tracked in Git. Complete [Serve the demo and neighbor table from a separate PocketBase](../.scratch/pilot/issues/17-database-demo-neighbor-table.md). [Demo guide and public demo-only credentials](../backend/demo/README.md).
- Generate `backend/demo/data.db` solely from fictional fixtures in a fresh disposable PocketBase; retain a checksum manifest and synthetic marker. Initialize an ignored writable copy at `local-data/demo/pb_data/data.db`, rebasing scenario timestamps once in the DB, preserving later edits and refusing overwrite. Seed six trackers, five members, four infrastructure devices and ten directional link observations alongside saved scenario records. Production stays on the VM with operational data/secrets outside Git.
- Replace application memory-only demo data/mutations with separate PocketBase API reads/writes. Keep live/demo request origins and token persistence separate, reject a non-simulation demo response and remove page-level sample fallbacks. Add Infrastructure receiver-filtered Neighbor signals table and a locked additive `link_observations` collection exposed through authenticated state. Preserve signal zeros, unknown values/relay identities, original-source separation and independent report/hearing times. No sample rows enter ordinary migrations; live signal ingestion and fork firmware remain unimplemented.
- All 51 backend checks pass in the existing `.venv` against real disposable databases, including checkpoint/runtime isolation, record edits reaching state, restart persistence and authorization. Frontend tests, typecheck, default live build and explicit demo build pass, including API separation, unavailable/misdirected demo rejection, table filtering and unknown/zero readings. Verify the actual Vite `/demo-api` response matches all ten SQLite signal records and the synthetic worker is online. Existing MapLibre bundle warning remains; no browser surfaces are available for native desktop/mobile visual review.
- Existing frontend occupies 5173, so do not stop it. Start the new demo API on 8092 and its synthetic worker alongside it; portal is `http://127.0.0.1:5173`, dashboard `http://127.0.0.1:8092/_/`. Preserve prior GPS-quality, firmware, cadence-research and other edits. Add only the synthetic checkpoint/manifest/guide to Git tracking; no commit, push, VM deployment or hardware change requested/performed.

Next useful step: owner opens Infrastructure and the demo dashboard to inspect/edit the same rows. Before public release, provision a separate demo API service/proxy and apply the signal migration with its state hook; native visual review and real signal ingestion remain outstanding.

## 2026-10-16 — Fork neighbor reporting improvements explored

- Owner asks whether our fork can improve NeighborInfo for project needs. Extend [node and neighbor telemetry](../docs/research/node-neighbor-telemetry.md#follow-up-tailoring-our-fork) and the existing [research answer](../.scratch/pilot/issues/16-node-neighbor-telemetry.md#fork-customization-follow-up) with passive infrastructure collection of RSSI/SNR, actual hearing age and optional bounded window summaries. Member trackers can keep ordinary GPS broadcasts; only instrumented observers/export paths need the new feature.
- Propose independent gateway MQTT/repeater LoRa schedules, separate expiry and publication, bounded local capacity covering the planned node set and capped/batched radio summaries. Suggested intervals/capacity remain bench hypotheses. Preserve standard NeighborInfo with a versioned private companion payload, GPS priority, airtime gates and gateway silence. Explain duplicate filtering, relay-identity ambiguity and incomplete snapshots; no delivery-rate or complete-topology claim.
- Read-only source/design research and documentation checks only. Local firmware remains at the upstream pin, two commits behind the locally recorded fork branch; reconcile the latest fork before coding. No fetch, firmware change, setting change, build, flash, deployment or commit requested/performed. Existing working-tree changes preserved.

Next useful step: when implementation is requested, define the first report payload and bench acceptance checks, then implement one infrastructure observer/export path before changing the fleet.

## 2026-10-16 — Node and neighbor signal capture reviewed

- Owner asks what else nodes can report and whether neighbor signal strength from repeaters/gateways can be captured in a table. Complete [Check node telemetry and directional neighbor signal reporting](../.scratch/pilot/issues/16-node-neighbor-telemetry.md), with pinned Meshtastic source and official documentation in [node and neighbor telemetry](../docs/research/node-neighbor-telemetry.md).
- Gateway envelopes can include final-hop RSSI/SNR; optional NeighborInfo provides directional neighbor SNR without RSSI or transmitted per-neighbor hearing time. Keep origin/observer/heard-node identities separate, preserve gateway copies and unknown values, and avoid implying reverse connectivity or delivery reliability. Pinned NeighborInfo defaults to six-hour reports, minimum four hours, with ten neighbors; enabling/exporting it requires configuration/build/path verification.
- Record proposed table columns and directional history storage, plus uptime, airtime/channel use, diagnostic counters, transmitted GPS context and fitted sensors as additional candidates. Recommend receive-only gateway metadata extraction first. Exact raw MQTT receipts are already archived privately, but neighbor/signal normalization and portal display are not implemented.
- Documentation only; no live archive inspection, device setting readback/change, firmware change, implementation, deployment, hardware test or commit requested/performed. Check documentation links/whitespace; preserve all pre-existing working-tree edits, including the local GPS-quality feature.

Next useful step: implement gateway receipt signal capture and an Infrastructure table when requested; verify NeighborInfo module/configuration and actual delivery before adding repeater-reported rows.

## 2026-10-16 — Plain-language GPS quality pill

- Owner requests a visual confidence/quality indication without technical abbreviations or invented metre accuracy. Complete [Show plain-language GPS quality in tracker cards](../.scratch/pilot/issues/15-gps-quality-pill.md): green Good / amber Limited / red Poor / neutral Unknown, with bars and text. Tap/click or keyboard-activate for a plain-language explanation about the recorded fix, environmental limitations and separate Last GPS age. Reported satellite count is secondary context; no raw quality score, probability or accuracy radius is displayed.
- Extend MQTT decoding and validated PocketBase ingestion with optional PDOP/satellite values stored on each historical/latest position in existing JSON fields. Absent/zero remains unknown; newer missing quality clears prior quality, and delayed/duplicate/unknown/future packets retain existing ordering and freshness behavior. No migration, archive replay/backfill or firmware/settings change. Demo-only fixtures illustrate the quality categories. Provisional thresholds and primary-source rationale are recorded in the ticket answer and linked contract.
- All 48 backend tests pass against disposable actual PocketBase instances; the initial sandbox run could not open localhost sockets and the permitted rerun passes. Frontend tests/typecheck/default and live builds pass, including wire scaling, metadata validation, duplicate/delayed/restart association, missing-quality replacement, disclosure interaction and Map/Users rendering independently of age. Whitespace checks pass; existing MapLibre bundle warning remains. Browser inventory is empty, so native visual/mobile/keyboard review is unverified.
- No live deployment, hardware/field test or commit requested/performed; preserve unrelated firmware, GPS cadence research and prior session-log edits.

Next useful step: review the pill visually on desktop/mobile, then release worker, backend hook and frontend together when deployment is authorized. Live historical points without quality remain Unknown until a new quality-bearing position arrives.

## 2026-10-16 — GPS quality in location reports checked

- Owner asks whether nodes report GPS accuracy with location. Stock Meshtastic position packets support optional DOP and satellite count ([official configuration](https://meshtastic.org/docs/configuration/radio/position/#position-flags)); pinned `v2.7.26.54e0d8d` PositionModule includes these when enabled, but does not populate `gps_accuracy` in normal node-originated position broadcasts. DOP is a satellite-geometry quality indicator, not a measured error radius in metres.
- Saved private B001/B002 GPS snapshots have position flags 939 (DOP and satellite count enabled, HVDOP disabled). The retained TEST-004 capture contains PDOP 183/282, corresponding to 1.83/2.82, and satellite counts 9/8, with duplicate gateway receipts. These are historical bench observations, not current device readback or field accuracy measurements. Raw locations and identities stay private.
- The current MQTT adapter normalizes coordinates and GPS measurement time but does not expose DOP/satellite count to the portal. No implementation, configuration change, hardware test or commit performed; preserve unrelated edits.
- Follow-up: owner asks whether all position flags are enabled. Decode saved member value 939 against the pinned schema: enabled ALTITUDE, ALTITUDE_MSL, DOP, SATINVIEW, TIMESTAMP, HEADING and SPEED; disabled GEOIDAL_SEPARATION, HVDOP and SEQ_NO. HVDOP selects separate horizontal/vertical DOP instead of PDOP. Saved configuration only; no live readback or setting change.

Next useful step: if GPS quality display is requested, carry received DOP/satellite values through ingestion and label them as quality indicators; a trustworthy metre-radius estimate needs separate receiver/error-model evidence.

### Portal GPS quality integration discussed

- Owner accepts the existing position flags unchanged and asks how to include reported data, especially quality, in the portal. Inspect the adapter, PocketBase ingestion/snapshot and shared tracker detail card. Recommend extending the normalized position with PDOP and satellite count first, retaining these on each historical position and its matching latest-position object. Existing JSON payload/latest-position fields and snapshot forwarding support an additive change without a new collection.
- Proposed presentation: a GPS quality row showing PDOP and a separate satellite count, with a short explanation that lower DOP indicates better satellite geometry, not metre accuracy. Keep quality attached to the same GPS measurement as the coordinates; missing/zero DOP remains unknown and older points without quality stay valid. Preserve position-age/stale behavior separately. Other already-transmitted altitude, speed and course data can follow the same ingestion path, with pinned-source units checked before use.
- This is an integration recommendation, not implemented or deployed behavior or a newly resolved tracker decision. No firmware/settings change, tests or commit performed; unrelated edits preserved.

Next useful step: when implementing, cover wire scaling (183 → 1.83), missing indicators, matching historical/latest measurements and unchanged two-gateway deduplication, then add the quality fields to the shared Map/Users card.

### Accuracy in metres checked

- Owner asks whether metre accuracy is possible. Current stock broadcasts do not provide a per-fix metre-error estimate; PDOP alone cannot supply one without an additional error model. The pinned V4 target assumes L76K, and [Heltec's compatible module](https://heltec.org/project/l76-gnss-module/) lists 2.5 m CEP as a product specification, not each fix's error. Exact installed GPS modules remain unverified in the inventory.
- A possible receiver-native route merits bench verification before any firmware promise: [GPSD's CASIC driver](https://gitlab.com/gpsd/gpsd/-/blob/master/drivers/driver_casic.c) decodes NAV-PV horizontal/vertical error variances into metre estimates. Its header explicitly notes the L76K public protocol document does not document NAV messages; this does not establish support on our units. Some other receivers explicitly expose horizontal accuracy, e.g. [u-blox NAV-PVT](https://content.u-blox.com/sites/default/files/products/documents/u-blox7-V14_ReceiverDescriptionProtocolSpec_%28GPS.G7-SW-12001%29_Public.pdf).
- Recommend first identifying/probing the existing fitted module for a documented per-fix error estimate, then, if supported, implementing firmware reading/transmission and portal storage/display with explicit estimate/confidence semantics. No hardware purchase, firmware/configuration change, actual probe, implementation or commit performed. Do not substitute the advertised specification or an arbitrary PDOP multiplier for observed metre accuracy.

Next useful step: verify the installed module and supported accuracy messages on one owned V4 before deciding whether metre estimates can be added without hardware changes.

## 2026-10-16 — Deploy sign-in refresh fix

- Owner authorizes deployment. Commit and push source `ee5e57e`; build/test it in an isolated LXC release directory with dependencies from the lockfile. The initial shared dependency folder lacked jsdom; isolated installation resolves that without changing the running services. Frontend tests/typecheck/production build pass locally and on the pinned server Node runtime.
- Take and verify a pre-release backup, then publish frontend assets before atomically replacing the index. All seven files match the staged build through Nginx and public HTTPS. Loopback sign-in, saved-token reuse/current account, invalid-token rejection, real-device counts and live MQTT heartbeat pass. All four services remain healthy. No backend code, schema or provisioning changes; old hashed assets and root-private source/static rollback remain available.
- Post-release backup `meshlink-20261016T161434Z.tar.gz`, SHA-256 `888f4a778e53938dbdf4b158aa06026f8149f3201aa2974b7cc64b81d9b6747a`, passes isolated integrity/API/history recovery including MQTT archive preservation. Public TLS, proxy boundaries and per-client sign-in throttling pass. [Full release evidence and pre-release backup](../docs/operations/portal-lxc.md#sign-in-refresh-fix--2026-10-16).
- No connected browser is available for native sign-in/refresh review; actual React DOM regression tests cover refresh, sign-out, rejected tokens, outage/retry, blocked storage and late responses. Preserve unrelated firmware, GPS cadence research and earlier uncommitted session-log entries.

Next useful step: load the updated site and sign in once, then refresh the same tab to confirm the owner's browser retains sign-in. Closing the tab ends this tab-scoped session; demo refresh still returns to sign-in.

## 2026-10-16 — Preserve portal sign-in through refresh

- Owner reports page refresh signs them out. Reproduce with the real live-mode React app in the DOM harness: sign in, remount, assert the authenticated workspace remains. The original app fails because its account/token exist only in React memory; no backend rejection is needed to reproduce it.
- Save only the account bearer token in tab-scoped `sessionStorage`. Reload validates it through the existing protected snapshot endpoint before showing the workspace, using current server account details. Sign-out and rejected authentication remove the saved token. Temporary connection failure offers retry without discarding the sign-in; blocked browser storage retains working memory-only sign-in. Demo entry remains memory-only. Update backend usage/security documentation.
- Frontend test suite, TypeScript check and production build pass. Regression coverage includes authenticated reload, sign-out across reload, 401/403 rejection, temporary outage/retry, a late restore response after sign-out, blocked storage and separate demo access. DOM tests use actual React with a MapLibre adapter; native browser/live-service verification is still outstanding. Existing MapLibre bundle warning remains.
- Owner authorizes deployment on follow-up. Prepare a source commit with only the sign-in fix and its documentation; preserve unrelated firmware, GPS cadence research and pre-existing session-log edits. Origin fetch succeeds and main matches origin/main. Deployment verification will be recorded separately after release.

Next useful step: deploy this reviewed frontend to `meshlink.spp.lol` with a verified backup and retained rollback assets, then check the public build and protected API boundaries. Native browser verification remains outstanding because no connected browser is available.

## 2026-10-15 — Map release and public demo entry

- Owner authorizes deploying the accumulated map/device-card changes and asks for a View demo button on sign-in without an account. Add explicit browser-only demo entry to the live build, a visible Demo label and Exit demo in the shared mobile/desktop header, and return to sign-in on refresh/sign-out. Extract App from the mounting entry point so the actual live-build sign-in/demo/authentication flow can be tested. No anonymous operational API access is added.
- Deploy and push source commit `3964f46` to the existing LXC/public portal. Local frontend tests/typecheck/live production build and all 46 backend integration tests pass; the staged server runtime also passes all 46 backend tests. The additive shortname migration passes first on a private live-database copy, then on the live database with exact checks that existing operational rows and all seven device identities are preserved.
- Public HTML/assets match the verified live build byte-for-byte; authenticated snapshots contain only B001/B002 and five infrastructure devices, with the correct Heltec V4 type metadata. Worker heartbeat, all four services, anonymous profile/state denial, proxy boundaries, sign-in throttling and public TLS checks pass. No demo accounts or synthetic records are added to PocketBase. Preserve earlier hashed assets for open tabs and retain private rollback source/static files at `/opt/meshlink-rollback-3964f46`.
- Pre-release backup: `meshlink-20261015T222413Z.tar.gz`. Post-release backup `meshlink-20261015T222458Z.tar.gz`, SHA-256 `6873c79a5949cef61ace28916c8f60550c298fb8ce16abcca193e0ec295d516d`, passes isolated integrity/API/history recovery, including MQTT archive preservation. [Release operations](../docs/operations/portal-lxc.md#map-and-demo-release--2026-10-15).
- No connected browser is available for visual review; interaction tests use real React/DOM with a MapLibre adapter. Preserve the unrelated firmware checkout and GPS cadence research.

Next useful step: review View demo and the map sheets in a mobile/desktop browser. Friendly-area boundaries, complete long-session aggregation and measured INA219 current remain separate follow-ups.

## 2026-10-15 — Always-active full-battery demo tracker

- Owner requests one full-battery demo whose GPS never exceeds two minutes old. Set Demo Avery/S001 to 100% and derive its standalone simulated position/contact timestamps from the current minute using the existing app clock. This also recovers immediately on the next clock update after an inactive tab; other fixture ages and authenticated backend observations stay unchanged.
- Frontend tests and typecheck/production build pass, covering fresh GPS/Active status at startup, minute boundaries and after long clock jumps without mutating the original fixtures, plus the rendered solid-green 100% battery. No backend change, deployment or commit requested/performed; preserve unrelated edits.

Next useful step: review Avery's solid green battery and Active pill in the demo card.

## 2026-10-15 — Battery size and digit alignment refinement

- Owner requests slightly smaller battery/digits and vertical/horizontal centering. Reduce the icon to 90% of pill height while retaining the 30:14 aspect ratio; reduce digits from 10 to 9 SVG units. Following visual feedback that digits remain too high, move their middle anchor down to x=13.5/y=8 for optical alignment. Preserve existing colors, values and solid 100% appearance.
- Existing rendered component checks and frontend typecheck/production build pass. No connected browser for visual sizing review; no backend change, hosted deployment or commit requested/performed. Preserve other working-tree changes.

Next useful step: review the refined battery in the tracker card at mobile/desktop sizes.


## 2026-10-15 — Stock member GPS timing options reviewed

- Owner asks whether stock firmware can report faster and whether movement-based reporting is better. Check official position/device documentation and pinned stock `2.7.26.54e0d8d` source; capture findings in [member GPS cadence](../docs/research/member-gps-cadence.md). Private-channel configuration permits explicit 60/30-second periodic intervals; GPS acquisition, periodic broadcasts and movement distance/minimum-time settings are separate controls. Default-channel interval enforcement must not be confused with this private profile.
- Recommend comparing a 60-second periodic / 30-second GPS profile with a hybrid: retain 120-second periodic reports, enable smart broadcasting, explicitly set 30-second minimum and 50-metre displacement with 30-second GPS acquisition. These are proposed bench profiles, not approved/applied device settings or measured delivery/runtime claims. Movement requires both displacement and elapsed time; periodic fallback remains useful for stationary/slow searches. Faster reporting increases offered radio traffic; measure freshness, congestion and battery runtime against the existing four-hour minimum/twelve-hour target.
- Source caveat: GPS publication calls `handleNewPosition()` without the smart-enable check, and that handler tests distance/time independently of the toggle. Thus the recorded smart-off setting does not establish strictly fixed-only transmissions. Current documentation also contains inconsistent defaults; use explicit values and reboot/readback. No bug fix or hardware/configuration change performed.
- No ticket decision, deployment or commit requested/performed. Preserve all unrelated working-tree edits.

Next useful step: compare the proposed profiles using actual source measurement/receipt gaps, transmission counts and battery runtime before selecting an operational cadence.

## 2026-10-15 — Session clock clarity, distance and battery sizing

- Owner questions First Seen 99 minutes ago versus Time Active 1h 27m for Demo Morgan. Clarify that the first is age since the first GPS point and the second is the observed first-to-last span (99 minus 12 minutes since the latest point = 87 minutes). Keep Time Active and change First Seen to clock time only, with Unknown retained when unavailable. Last GPS/Last Heard age behavior remains separate.
- Add Distance Travelled beside Time Active in the latest-session summary, displaying miles to one decimal. Sum great-circle segments only between valid, ordered/deduplicated points in that same session; do not bridge >2-hour gaps or include prior sessions. Single point displays 0.0 mi and no timed points Unknown. This is a GPS-sample estimate, not measured route length; missing data/noise and the existing 500-point/12-hour snapshot cap limit completeness.
- Give battery and status pill one shared full CSS height including pill padding; preserve the icon's 30:14 aspect ratio and existing colors/digit/full-charge rules. This supersedes the earlier font-height icon request.
- Frontend tests/typecheck/build pass, including clock-only First Seen, duration semantics, displayed one-decimal distance placement, multi-leg mileage, prior-session exclusion, stationary/single-point/unknown behavior and dateline crossing. Existing MapLibre bundle warning remains; browser visual sizing/native review is unavailable. No backend/API/schema change, hosted deployment, hardware action or commit requested/performed; pre-existing work preserved.

Next useful step: visually review the larger battery and session summary; full session/distance completeness still needs the deferred backend snapshot aggregation work.


## 2026-10-15 — Current member GPS cadence checked

- Owner asks the currently configured location-reporting cadence. Saved/reboot-verified B001/B002 Heltec V4 profiles in TEST-001 use 120-second periodic position broadcasts, 60-second GPS acquisition and smart broadcasting disabled. No later recorded member cadence change found; TEST-004/005 establish automatic GPS reception/ingestion, not a sustained two-minute delivery guarantee.
- Read-only records review; no device readback, radio configuration, hardware test, ticket change or commit performed. Preserve existing working-tree edits.

Next useful step: if actual delivery cadence is needed, measure GPS measurement/receipt gaps from retained observations and compare with the saved profile.

## 2026-10-15 — Compact battery/copy indicators and latest recorded trail

- Owner requests UI-only refinement: compact battery beside status, icon-based coordinate copy, Area/Coordinates on one row, sheets that shrink to content with an approximately 85% viewport limit, “Show Recorded Trail” for the latest continuous session and always-visible session info below GPS/contact times. Read the supplied Lucide icon references and use small inline outline SVGs without another runtime dependency.
- Battery outline/digits match red for 00–19, amber 20–39, green 40–99; 100 is solid green with no visible digits. Unknown/invalid values stay neutral/unknown. Fractional reports are floored; glyph height matches the pill font. Copy works from either text or symbol, shows a brief animated green check and accessible announcement, and handles clipboard failure with a manual-copy message. Mobile sheets have auto height/max 85dvh, bottom safe-area padding and sticky close controls.
- Replace the history range selector, point buttons/details and expanding explanations with one Show Recorded Trail checkbox. Latest loaded GPS session splits only on gaps greater than two hours; exact two-hour gaps stay connected. Sort/deduplicate valid, nonfuture measurement times without mutating inputs, include a known current position, draw only that session and retain dots after card close. Dots are noninteractive and do not block device pins. Shared page state lets a trail chosen on Users appear on Map; login changes clear it.
- Display First Seen from the latest session's earliest available GPS point, separate stored Last Heard and Time Active as the observed first-to-last GPS span, with a fixed loaded-point note. Silence does not grow activity. Session start/duration are unknown without timed points. No backend/API/schema changes: PocketBase currently returns at most 500 GPS points in 12 hours and no session summary. Complete long-session trails/start/activity values need a later backend snapshot aggregation change using retained observations; a new collection is not necessarily needed. Friendly-area mapping remains unconfigured.
- Frontend tests/typecheck/production build pass, including two-hour boundaries, splits, sorting/deduplication, invalid/unknown/future timestamps, current-position inclusion, duration formatting, battery color/digit/full-charge boundaries, copy success/failure/text tapping, map trail features and unchanged card content on checkbox toggles. Existing MapLibre bundle warning remains. No browser surface is connected for actual layout/animation/native clipboard review. Prior backend, firmware, inventory and other work is preserved; no hosted deployment, hardware action, ticket resolution or commit requested/performed.

Next useful step: review the compact sheet in a connected desktop/mobile browser. When backend work is brought forward, provide complete latest-session points and explicit session metadata beyond the current 12-hour/500-point snapshot window.


## 2026-10-15 — Simplified tracker location card and member map shortnames

- Owner requests Location fields (friendly Area, copyable Coordinates to five decimals, Last GPS and Last Heard), a pill beside the name, device-type/radio-name eyebrow and only reported Battery percent. Implement shared card on Map/Users; remove the detailed member battery estimate/voltage/configuration section, while preserving its existing backend storage/API and location history. Clipboard success/failure is announced; coordinates remain manually selectable. Battery is the final field.
- Last GPS uses source measurement time and Last Heard uses receipt-based contact independently; local clocks omit seconds, age uses whole minutes and displays `+2hrs` after two hours. Missing/invalid/future times remain unknown. Provisional pills use Active <2 min, Recent 2–15 min, Stale 15 min–2h and No Location >2h/unknown/no position, pending the owner's optional threshold answer. The existing 15-minute stale summary rule is unchanged. Last known map pins/coordinates remain visible for No Location; no fresh fix is inferred from receipt time.
- Area displays a supplied friendly name or “Unknown area.” Project notes specify owner-defined Google Earth KML/KMZ boundaries, but no dataset/resolver is configured or found. Actual area lookup remains outstanding; no geographic names or boundaries invented. Device type comes from configuration; demo fixtures/confirmed B001/B002 use Heltec V4, other unknown metadata shows Device.
- Add optional five-character member shortnames with additive migration, authenticated own-profile route, owner account-creation prompt and Users form. Validate 1–5 letters/digits/underscores/dashes on server; derive the target member from authentication and reject unrelated fields/worker/anonymous access. Account creation saves a supplied alias transactionally. Assigned map markers use the saved choice; blank/unassigned falls back to the unchanged radio label. Marker width adapts to five characters. Existing records are not assigned invented aliases; fictional demo aliases are explicitly synthetic.
- All 46 backend tests pass in the existing project virtual environment against disposable PocketBase databases, including profile validation, cross-member/role mutation rejection, persistence, account transaction behavior and unchanged tracker/assignment records. System Python initially lacked cryptography; use the existing `.venv` with the required MQTT dependencies. Frontend tests/typecheck/build pass, including exact age/status boundaries, aliases through assignment/release, old-coordinate retention, copy success/failure, card placement/content, shortname form and existing infrastructure/history interactions. Verify the live-cutover metadata addition separately. Existing MapLibre bundle-size warning remains; no connected browser for visual/native clipboard/gesture review.
- Preserve prior firmware, infrastructure, inventory and other frontend work. No live database/schema change, hosted deployment, hardware action, radio naming command, ticket resolution or commit requested/performed.

Next useful step: provide/configure owner area boundaries, confirm the provisional status thresholds, visually review the tracker sheet, and deploy the additive backend/frontend change together when requested.


## 2026-10-15 — Full-screen map and mobile device sheets

- Owner requests map-only viewing with full-width Apple-style mobile detail sheets for infrastructure/member devices, tracking stats on Users, cleaner battery copy and a remembered infrastructure overlay toggle. Map now fills the available viewport beside navigation; basemap/fit/layer controls overlay it and no detail opens until selection. Infrastructure starts on and persists its preference for one year in a SameSite=Lax cookie (Secure on HTTPS).
- Share one native-dialog device sheet: nearly full-height, independently scrollable and animated upward on mobile through 850px; compact nonmodal overlay on desktop. Close control stays visible; Escape, backdrop and a downward handle swipe dismiss. Preserve GPS versus receipt ages, history/point attribution, member battery configuration, infrastructure weather/last heard and offline/stale indications. Move summary counts and searchable tracker list to Users; even devices without positions retain inspection/configuration access there. History remains visible after map-sheet close so points can still be selected.
- Infrastructure estimate labels now say “Estimated battery percentage” without voltage-estimate warnings. Replace visible trend/rate copy with charging/discharging/steady direction and mA availability. No measured current is present in the live contract: display `— mA` rather than relabelling a voltage slope. Optional frontend signed `batteryCurrentMa` supports a supplied current; backend ingestion/sign mapping remains separate. Record owner's planned INA219 use on repeaters/gateways in inventory without claiming installation, measured data or changed quantities.
- Frontend tests/typecheck/production build pass, including actual React/DOM interactions for exclusive device selection, mobile modal versus desktop panel APIs, close/cancel/Escape, focus restoration, history, cookie remounts, offline status, infrastructure-only maps and never-seen device inspection. Current checks distinguish signed mA readings from missing/invalid current and voltage-only history. Existing MapLibre bundle-size warning remains. Computer-use inventory exposes no apps or browsers, so native modal/gesture behavior, animation, WebGL/tiles and visual layout remain unverified.
- Existing firmware, infrastructure battery/history UI, package/inventory/session and research work preserved. No firmware/backend change, hardware test, hosted deployment, ticket resolution or commit requested/performed.

Logo/layout follow-up: owner supplies the [SNORR logo](https://snorr.vegas/wp-content/uploads/2021/12/cropped-SNORR-Final-Logo.png), requests the same mobile header as the other pages and reduces sheets to about 80% of the screen. Bundle the unchanged PNG locally in shared branding, restore the mobile map logo/navigation plus common topbar/status header, and size all mobile device sheets to `80dvh` with independent scrolling/sticky close controls. Desktop keeps the compact overlay. Frontend checks/typecheck/build pass; no connected browser for visual review and no hosted deployment/commit requested.

Banner cleanup follow-up: owner removes both environment/feed banners from Map on every screen size and the breadcrumb/clock bar from every page. Do not render the two banners on Map; retain their account/demo/feed controls on other pages and keep shared logo/navigation visible. Remove unused breadcrumb/clock styling and the mobile banner override. Map outage notices and 80%-height device sheets remain available. Frontend checks/typecheck/build pass; browser visual review and hosted deployment remain outstanding. No commit requested/performed.

Infrastructure visibility follow-up: owner removes the infrastructure toggle and requires infrastructure always on. Remove visibility state, cookie reads/writes, toggle props/control and unused styling; render infrastructure markers unconditionally and ignore previous off cookies. Update existing DOM coverage to retain infrastructure after page remount with an old off cookie and with zero member trackers. Frontend checks/typecheck/build pass; no hosted deployment or commit requested/performed.

Next useful step: review the map and sheets in a connected browser at desktop/mobile widths, then deploy when requested. INA219 installation and live current telemetry remain unverified.


## 2026-10-15 — Member battery voltage and configurable LiPo estimate

- Owner requests backend/frontend support for end-user voltage broadcasts, battery type/size configuration and similar state-of-charge estimates for the purchase-list 1000/3000 mAh LiPo packs. Preserve the earlier 1100 mAh inventory label for the smaller packs and unchanged stock counts; suggestions include 1000/1100/3000 with other positive whole capacities or unknown accepted. No installed device/pack mapping inferred.
- Normalize member battery telemetry into existing PocketBase observations/receipts with source validation and two-gateway deduplication. Expose separate voltage, measurement/receipt timestamps, timestamp quality and configuration in tracker snapshots. Battery packets preserve GPS measurements/history; old/future/unknown clocks cannot overwrite newer known battery measurements. Member nonbattery telemetry remains outside operational normalization; raw archive remains complete for received traffic.
- Add admin-only battery type/capacity configuration using the existing route and selected-tracker Battery UI. Generic 1S 3.7/4.2 V LiPo lookup uses the pinned Meshtastic nonlinear reference, rounded to 5%, with raw volts and offline/unknown-time/15-minute stale indication. Capacity is metadata, not a runtime estimate or percentage multiplier. [Source/profile details](../docs/research/member-battery-charge.md).
- All 44 backend checks pass locally and on the LXC runtime in disposable databases; full working-tree frontend and isolated staged frontend checks/typecheck/live build pass, including rendered battery state/admin-controls tests. Deploy only the member change after verified backup `meshlink-20261015T203559Z.tar.gz`; no schema migration or radio/telemetry-setting change needed. Post-deployment backup `meshlink-20261015T203735Z.tar.gz` restores in isolation and proxy/auth boundaries pass.
- Check ten actual archived messages through the new decoder: no member battery-voltage packets available, so no backfill performed. B001/B002 keep unknown profile/capacity and voltage absent; do not invent readings or silently assign packs. Real member voltage reception/calibration, installed-pack selection and full browser visual review remain unverified. Preserve unrelated local firmware/infrastructure UI/inventory/session work outside this release; local battery helper now re-exports the shared estimator without changing EVE results.

Next useful step: admin selects the installed LiPo type/capacity for each tracker, then verify the first actual member voltage packet and compare to a multimeter. No firmware/cadence change made.

## 2026-10-15 — Archive all received MQTT traffic in PocketBase

- Owner directs saving all MQTT data now and deciding how to use it later. Add private `mqtt_archive` collection and worker-only archive route: exact payload bytes as base64, topic, arrival time, QoS/retain/duplicate flags, stable receipt UUID and bounded normalization outcome/reason. Unsupported, unknown-source, retained, malformed and duplicate deliveries are preserved; existing operational normalization/contact/freshness rules stay intact.
- Subscribe to the configured project root (`snorr/pilot/#`), archive before normalized ingestion and acknowledge QoS 1 after private SQLite persistence. API retries reuse archive IDs; old normalized queue entries still drain, and backend validation rejection receipts no longer block the queue. No raw data/keys enter Git, no automatic expiry is introduced, and archive access stays behind trusted PocketBase administration.
- Deploy additive migration and worker/hooks to the authorized LXC after verified backup `meshlink-20261015T202515Z.tar.gz`. Verify an actual new live receipt, byte-length preservation, zero pending queue and active services. All 42 backend tests pass locally and on the production runtime against disposable databases. Post-update backup `meshlink-20261015T202742Z.tar.gz` and isolated recovery include the archive; protected proxy and login checks pass.
- Worker requests all root topics, but broker delivery remains ACL-limited: documented read permission is `snorr/pilot/2/e/#`. Broker SSH works as the owner, but ACL inspection/change requires unavailable sudo authentication; root SSH is denied. No broker permissions were changed. Raw ciphertext retains later decoding options with the matching private key; past discarded data and offline/QoS-0 losses are not recovered. [Operations and limits](../docs/operations/live-mqtt.md#raw-mqtt-archive--2026-10-15).
- Preserve the pre-existing firmware, frontend, inventory and session edits outside this change.

Next useful step: let the archive collect real traffic; broker admin can expand the worker read ACL to `snorr/pilot/#` if topics outside the existing encrypted subtree are needed. Review stored packet types when the owner brings interpretation forward.

## 2026-10-15 — Last-heard ingestion semantics reviewed

- Owner asks whether last heard can use the latest MQTT packet from a node. Inspect adapter, worker and ingestion: live worker subscribes to the configured encrypted channel, filters registered sources/gateways, and currently normalizes member positions plus infrastructure voltage/environment telemetry. Other application packets are counted as ignored, not archived. Rejected adapter packets are counted, while backend validation failures retain bounded receipts.
- Accepted/duplicate normalized receipts update the originating device's lastContactAt using original worker receipt time, independently of sensor/GPS measurement clocks. Snapshot and map stats already expose that field; demo infrastructure fixtures currently omit receipt timestamps. Queued API ingestion preserves original arrival time.
- Recommend extending last heard to validated packets originating from a registered node regardless of application kind, retaining only needed contact metadata. Keep gateway latest MQTT uplink activity separate: forwarding another node's packet proves gateway activity, not a fresh packet originating from the gateway or each relay. Keep sensor/GPS measurement ages independent. No catch-all ingestion, raw-payload archive or last-heard behavior change implemented in this review.

Next useful step: choose all-valid-origin-packet contact tracking plus separate gateway uplink age, then implement/test the adapter/receipt contract without refreshing telemetry/GPS timestamps.

## 2026-10-15 — RAK charging and solar specifications checked

- Owner asks about published RAK4631 charge/discharge/cutoff/solar behavior. Inventory identifies RAK19007 base boards; per-unit revision remains unverified. Read the official RAK19007 datasheet and RAK support explanations, and inspect the pinned Meshtastic source without modifying firmware.
- Record charging target 4.2 V, documented 350 mA charge current, nominal 5 V solar input / 5.5 V maximum and 3.3–4.3 V documented battery operating range. Distinguish 2.9 V charger precharge and recharge hysteresis from low-voltage discharge protection. Source has software low-battery sleep near 3.1 V; physical protection and real sleep/restart thresholds remain untested. [Sources and distinctions](../docs/research/battery-charge-estimate.md#rak19007-charging-and-low-voltage-behavior).
- No hardware/protection installation claim, field measurement, threshold/code change, ticket resolution or deployment.

Next useful step: confirm actual base-board revision, battery protection and panel voltage, then bench-test normal low-battery sleep and solar recovery when hardware is available.

## 2026-10-15 — EVE battery profile and approximate charge display

- Owner identifies EVE 26V 18650 2550 mAh / 7.5 A cells, confirms direct battery voltage and supplies 3.6/4.2/2.5 V nominal/full/cutoff. Update inventory without changing counts or claiming assembly/calibration.
- Verify EVE specifications and visually inspect the manufacturer's reference discharge chart using PDF rendering. Document approximate nonlinear lookup from the 0.2C/77°F curve, interpolation, 5% display rounding and limits in [battery charge estimate](../docs/research/battery-charge-estimate.md). This is a loaded reference curve, not measured pack calibration or open-circuit data.
- Add shared estimated charge display to Infrastructure battery detail and map quick stats for R001/R002/R003 and explicitly configured EVE 1S profiles. Other/unknown profiles stay unknown; member percentages and raw backend telemetry remain unchanged. Preserve voltage, unknown/stale/offline indications and charging-bias context. Cell cutoff is separate from unverified node cutoff and runtime; no warning rule changes or hosted deployment.
- Verify nonlinear interpolation, bounds/invalid inputs, profile isolation, monotonicity, 5% rounding and rendered UI through frontend checks. Hardware calibration, actual charge-state verification and browser visual review remain outstanding. Existing unrelated firmware change preserved; no commit requested.

Next useful step: review the approximate percentages locally, then compare telemetry to a multimeter and record a normal-load battery discharge when nodes are available.

## 2026-10-15 — Voltage-derived charge estimate discussion

- Owner asks whether battery chemistry/voltage can provide estimated state of charge and clarifies 2550 mAh 18650 cells in two- or four-cell parallel packs. Record owner-reported wiring and rated arithmetic in inventory without assigning unconfirmed per-device configurations or measured capacities.
- A coarse chemistry-specific voltage lookup is feasible after confirming the cell model/charge profile and that telemetry measures battery terminals. Discuss calibration, charger/load influence, temperature and usable cutoff; capacity/parallel count alone does not define the voltage curve or remaining runtime. TI primary-source reference: https://www.ti.com/document-viewer/lit/html/SSZT786/GUID-5DD8C3D9-BCBE-467B-90E5-FAA672AAC15D .
- No estimate curve, new hardware, backend/frontend implementation, field measurement or ticket resolution in this discussion.

Next useful step: identify cell make/model or nominal/full-charge voltage and confirm per-device parallel packs/measurement path, then choose an explicitly approximate UI profile.

## 2026-10-15 — RAK4631 small dummy-load guidance

- Owner asks about a conservative resistor load and chip GPIO limits. Reviewed [Nordic GPIO specifications](https://docs.nordicsemi.com/r/bundle/ps_nrf52840/page/gpio.html), [Nordic support's package-current guidance](https://devzone.nordicsemi.com/f/nordic-q-a/82106/nrf52840-gpio-drive-capability), and [RAK4631 electrical documentation](https://docs.rakwireless.com/product-categories/wisblock/rak4631/datasheet/).
- Standard-drive logic levels are specified at 0.5 mA; high drive at 5 mA with VDD >= 2.7 V (3 mA at lower supply). Nordic support gives 15 mA total GPIO sink/source ceiling for the package; table values of 14/15 mA are not conservative per-pin design targets. Suggested starting at 10 kOhm GPIO-to-ground (~0.33 mA at 3.3 V), with an unused output verified first. A 2.2 kOhm load (~1.5 mA) requires explicit high-drive configuration for this guidance.
- A power-rail resistor, optionally switched by a MOSFET, better suits a larger battery dummy load; exact rail, baseboard wiring/regulator budget and firmware pin use must be checked before wiring. No hardware connected, firmware changed, load/current measured, ticket resolved or commit requested. Existing working-tree edits preserved.

Next useful step: identify the exact baseboard and whether the intended test is battery drain or processor work, then select the load and connection accordingly.

## 2026-10-15 — Linux infrastructure battery UI

- Owner resumes frontend development without nodes and requests better repeater battery direction/rate/history. Synced main (already current); preserved the pre-existing firmware submodule change.
- Added voltage-derived charging/discharging/steady estimates and mV/hour slope from actual elapsed times over the latest continuous hour. Require three reports over ten minutes, break on configured battery timeout, and label stale/unknown-time/offline estimates as historical. Charger state/current remain unmeasured; no battery capacity/runtime claims.
- Replaced the fixed-axis dots with a full-width time chart, adaptive voltage scale, 1h/6h/24h/all-loaded ranges, keyboard/selectable exact readings, range/change summary and reading table. Expose existing 40-observation snapshot limit; retain unknown-clock handling. Added richer fictional demo histories only; backend, hardware, hosted services and private data unchanged.
- Frontend tests/typecheck/production build pass, including direction, irregular sampling, sparse data, outages and invalid timestamps. Existing MapLibre bundle-size warning remains. Visual browser review could not run: computer-use inventory has no browsers/apps. No hardware or live telemetry validation, hosted deployment, ticket resolution or commit requested/performed.

Follow-up: owner reports repeated backhaul details after switching devices. Reproduced using actual React components in a temporary jsdom harness: switching to the backhaul leaves two battery sections and emits duplicate-key warnings. BatteryHistory and RuleForm shared the selected device ID as sibling keys. Give each component a distinct prefixed key; repeated repeater/backhaul switches now retain exactly one battery section and one rule form. Add a persistent DOM regression test and pinned development-only jsdom dependency to the existing Node test command. Browser visual review remains unavailable; this verifies actual React reconciliation and rendered DOM rather than appearance.

Map follow-up: owner requests named/selectable infrastructure markers with quick power/weather/last-heard stats. Replace generic R/B/site-count pins with individual R001/G001-style labels, preserving separate selection at colocated coordinates using screen offsets. Member pins now show full short names such as S001. Add an on-map quick-stats panel for voltage, inferred direction/rate, available temperature/RH, receipt-based last heard and planned-site/offline/stale/unknown-time indicators. State of charge is explicitly unknown because the current infrastructure contract does not provide a percentage; do not derive one from voltage. Layer-off and close controls clear the panel; no new telemetry or deployment.

DOM interaction tests exercise actual map React components with a minimal MapLibre marker adapter (no WebGL/tiles), covering colocated labels, device switching, sensor availability, offline status, close and layer toggling. Frontend tests/typecheck/build pass; browser visual/hardware checks remain outstanding.

Temperature follow-up: owner requests Fahrenheit throughout the site while preserving Celsius in the backend. Centralize presentation conversion and apply it to both infrastructure details and map quick stats. Update rendered-DOM assertions for both surfaces (8.4°C displays as 47.1°F); preserve unavailable-reading behavior and raw telemetry.

Next useful step: review local Infrastructure detail and infrastructure map quick stats on desktop/mobile, then decide whether to expand backend battery history/state-of-charge telemetry and deploy the reviewed frontend.

## 2026-10-15 — Restore connected gateway Wi-Fi

- Owner requests restoring supplied Wi-Fi credentials on the connected gateway. After USB reconnection, COM6 identifies as G002 (`!849ad7a0`). G001 is unchanged.
- Privately back up settings, apply supplied credentials with Wi-Fi enabled, and reconnect to verify exact saved values. Serialized MQTT and LoRa settings remain unchanged. Credentials and snapshots stay in ignored `private/bench/2026-10-15-gateway-wifi/`.
- Saved configuration passes; hotspot association and subsequent MQTT delivery remain unverified. No firmware, hardware allocation, portal or radio-profile changes.

Next useful step: keep the hotspot available and verify fresh G002 receipts in the live portal.

## 2026-10-14 — Correct standalone-demo frontend on live portal

- Owner reports demo data after repeater deployment. Fresh public browser reproduces six fictional trackers; authenticated loopback confirms live backend/configurations retained. Served bundle matches staged artifact. Cause: build omitted `VITE_PORTAL_MODE=live`, selecting old demo default. Earlier API/restore checks missed browser entry behavior.
- Production now defaults live while retaining local development/explicit standalone demo. Vite validates/records mode in HTML; deployment refuses non-live artifacts and live verifier checks served mode. Two regression tests added; all 10 frontend tests/typecheck/build pass. Deploy hashed assets before atomic HTML replacement after private backup; no database/radio/credential changes.
- Hosted mode assertion changes from failure to pass; fresh public browser shows sign-in. Configuration preservation, public HTTPS/auth boundaries and isolated corrected-build restore pass. Backup/checksum in [operations](../docs/operations/repeater-telemetry.md#frontend-mode-correction). Authenticated browser rendering still needs account-holder review.

Next useful step: owner refreshes/signs in to review live Infrastructure cards; continue sustained telemetry/coverage/power measurements. Publish correction to origin/main, preserving unrelated 3MF.

## 2026-10-14 — Three repeaters provisioned with live telemetry

- Owner authorizes adding R001/R002/R003 at two supplied planned sites with antenna, four 2550 mAh 18650 cells each and 160 mA solar-cell records; explicitly includes live infrastructure telemetry. Exact coordinates remain private. Record planned assemblies without inferring chemistry, wiring, aggregate capacity or panel wattage. Warn monitoring remains disabled pending deployment activation; live readings are enabled.
- Extend encrypted MQTT decoding, PocketBase observations/health and portal humidity/unknown-clock display; group colocated map markers. Add guarded transactional provisioning, isolated rollback/preservation checks and dynamic restore expectations. Fix existing generated-password CLI parsing using `--`. Existing trackers/accounts/history and credentials are preserved.
- Staged 39 backend tests and 8 frontend tests/TypeScript/build pass. First deployment attempt safely stops before provisioning because the old restore verifier assumes four accounts; actual deployment has five. Correct verifier and rerun backup/restore before successful migration. No reset or synthetic live records.
- Live authenticated configuration matches all three exact private plans. R001 4.115 V, R002 4.159 V, R003 3.634 V; R003 19.8942°C/36.7484% RH. Each of four genuine radio reports arrives through both gateways: eight receipts, four observations, accepted/duplicate pairs. Valid wall-clock measurements are preserved; unknown uptime clocks are separately tested.
- Public HTTPS/authentication boundaries, proxy throttling and isolated seven-device restore pass. Matching final private backup/checksum and details: [operations](../docs/operations/repeater-telemetry.md), [TEST-009](field-results.md#test-009--live-repeater-provisioning-and-telemetry). No new hardware purchases, field installation or deferred survey work.

Next useful step: review authenticated rendering on the owner's devices, confirm installed-site status and monitoring thresholds, then measure sustained telemetry/GPS freshness, power endurance and actual relay coverage. Solar-input measurement, sensor calibration and off-host backup remain unverified. Publish this completed source/record checkpoint to origin/main; preserve unrelated 3MF.

## 2026-10-14 — R003 AHT fix ported, built and flashed

- Owner explicitly authorizes bringing the identified changes forward, building and flashing R003. Sync main (already current), initialize pinned firmware/nested submodules and read firmware agent/build instructions. Switch clean firmware to the existing `snorr/rak-survey` project branch and port only the RAK sensor-detection fix; no forced reporting intervals, old defaults or survey implementation. Publish functional commit `b0aa05b41` and concise-comment follow-up `cc5907b1fc7b4c200e23f43e10baa54c39aeaf25`; no history rewritten.
- Native Windows PlatformIO build succeeds as `2.7.26.cc5907b`. Recover a stalled compiler download using the exact registry-checksummed archive; remaining dependencies install normally. Build uses pinned GCC 9.3.1, nordicnrf52 10.11.0 and Arduino framework source `9ddcbc9568b12f102f9e88bd4d1b88ea789213a4`. Trunk is unavailable; changed line passes scoped clang-format 16.0.3 and whitespace checks. Vendor-library warnings remain; no full native/MCP suite claim.
- Snapshot R003's complete private profile/keys. Identity-check it, enter its UF2 bootloader and flash the checksum-verified custom image without reset/bootloader change. Reconnect on COM14; custom version and complete pilot-profile checks pass. Entire local/module/channel configurations equal the pre-flash snapshot, including channel/device keys, role/radio settings, debug off and enabled device/environment reports at 900 seconds.
- AHT-family readings now work: local sample 22.90535°C/35.01892% RH; automatic environmental packet at 22.97821°C/34.962845% RH reaches both V3s. New battery packet (4.267 V, charging/no-battery level 101) also reaches both: 4/4 new receipts pass. Exclude older packets drained from gateway queues. Post-flash telemetry clocks initially report uptime-like 66/91 values; do not treat them as Unix measurement times. No gateway, R001/R002, portal or other hardware changes.
- Keep artifacts, checksums, build logs, configuration/key snapshots and raw receipts ignored/private. Update submodule pointer, inventory, project/map and handoff; [exact source/build/flash evidence](../docs/operations/r003-aht-build.md), [TEST-008](field-results.md#test-008--r003-custom-aht-build-and-radio-telemetry). The stock-only R003 limitation is resolved by this authorized custom image; original two-repeater field allocation and deferred survey scope remain unchanged.

Next useful step: measure sustained 15-minute device/environment delivery and battery/solar runtime, compare sensor/voltage to references, and verify required V4-to-RAK GPS relaying. Portal infrastructure ingestion/display and clock-validity handling are separate work. Publish the parent source pointer and these records after the already-pushed firmware commits.

## 2026-10-14 — Existing fork AHT fix confirmed

- Owner recalls fixing the RAK temperature-sensor issue in the older firmware fork and requests verification. Read the existing fork audit, then independently inspect GitHub's exact commit diff and current develop source. Confirm `e617a4dcfd95500c73f570c583f3ea6d02aa4881` (2025-12-31, “fix AHT10 for RAK4631”) comments out HAS_NCP5623. This survives at current develop `76d5156e72d9d9aaa9722b7bbc1336335b685984` and R003's former reported source revision `36133d29d`.
- The same commit forced environmental enable/15-second reports; later commits revert the forced behavior while retaining the variant fix. Link this existing finding into the R003 setup record. The source change matches the stock scanner exclusion; it does not prove the tentatively identified AHT21's wiring or operation. No firmware/configuration/hardware change, build, flash, ticket resolution or broader fork transplant.

Next useful step, if owner brings custom firmware forward: port only the RAK sensor-detection compatibility change onto the pinned current release, retain configured 900-second device/environment reports, build a traceable image and verify actual temperature/humidity on R003. Stock firmware remains installed pending that scope change.

## 2026-10-14 — R003 prepared; stock AHT sensor limitation identified

- Owner replaces the connected RAKs with another unit, requests R003 with matching stock pilot configuration and temperature/humidity if available, confirms antenna, and tentatively identifies AHT21 at 0x38. Sync main (already current), preserve unrelated untracked 3MF, identify COM14 RAK4631 `!05237743` and privately back up its older profile.
- Full reset, 1200-baud Nordic entry on COM15 and official matching stock package install succeed. Apply shared private profile with device/environment telemetry explicitly enabled at 900 seconds each; reapply after role defaults, clear unrelated telemetry options and verify the complete profile after configuration reboot. Private provisioning/verifier updated; no changes to disconnected R001/R002 or the gateways/portal.
- Both V3s receive two automatic device-metric packets (4/4 receipts) with firmware-reported 4.259/4.278 V and level 101. No temperature/humidity arrives in gateway observation or short local request. Brief private debug logging restored off. Pinned standard RAK variant defines HAS_NCP5623, which compiles out the scanner's AHT detection case; environmental enable alone cannot overcome that stock-target exclusion. Sensor model/wiring and actual voltage calibration remain unverified.
- Record third existing-stock allocation, verification and source explanation in [setup](../docs/operations/rak-pilot-setup.md#r003-environmental-sensor-follow-up--2026-10-14), inventory and [TEST-007](field-results.md#test-007--r003-stock-setup-and-environmental-sensor-limit). Keep the original two-repeater field plan, stock firmware constraint and deferred custom survey scope; no new purchase, site work, custom firmware or tracker status change.
- Final explicit reboot/reconnection passes the complete profile, including debug off and unrelated sensor modules disabled. Local Python close/disconnect race recurs after reboot, with successful subsequent device readback.

Next useful step: owner chooses whether to retain stock with this sensor unavailable or bring forward a targeted firmware/sensor compatibility change. Forced GPS relaying, actual sensor wiring/model verification, calibrated battery voltage and sustained cadence/runtime tests remain outstanding; portal telemetry is separate.

## 2026-10-14 — Enable RAK battery-voltage telemetry

- Owner asks whether R001/R002 track/report battery voltage. Check saved profiles and pinned stock `DeviceTelemetry.cpp`: a 900-second interval alone does not enable broadcasts. Initial setup missed `device_telemetry_enabled`, which remained false. Correct it to true on both identified RAKs and retain the interval.
- Independent complete profile checks pass after configuration reboot on both devices, including the added enable-flag assertion. Private setup/verification helpers are corrected; keys/configuration stay outside Git. Stock device metrics include voltage and battery level, with level 101 for charging/no battery. Actual voltage calibration and timed periodic RF delivery remain unmeasured; the portal's existing GPS worker does not ingest battery telemetry.

Next useful step: connect the verified battery assembly, compare reported voltage to a meter, observe automatic telemetry reception at the V3s, then implement portal infrastructure telemetry separately when brought forward. No radio/channel, inventory quantity, site, battery specification or ticket status change.

## 2026-10-14 — Two stock RAK pilot repeaters prepared

- Owner brings forward setup of two plugged-in RAK repeaters with stock firmware and permits flash/reset; confirms suitable 915 MHz antennas on both. Sync main from origin (already current), preserve the unrelated untracked 3MF, read the pilot/inventory/handoff and identify COM8/COM9 as RAK4631 R001/R002. No purchase, stock-count change, site installation or custom survey work.
- Privately back up previous configurations; verify the official nRF52840 release archive digest and matching RAK4631 UF2. Install stock `2.7.26.54e0d8d`. Both APIs time out after full reset; 1200-baud entry and official matching Nordic serial firmware reinstall restore access without a bootloader update. Cause remains unresolved. Full reset replaces legacy keys, admin configuration and old fixed locations.
- Configure the shared private pilot channel/radio profile, visible ROUTER roles, local-only rebroadcast, US/LONG_FAST slot 35, hop limit 3 and 10 dBm. GPS/fixed location, MQTT/Wi-Fi and channel gateway functions off; device telemetry 900 seconds. Stock role-change defaults override initial values; reapply the explicit profile after role change and verify independently. Complete exports/keys stay private.
- Six of six direct encrypted zero-hop fixture receipts pass: each RAK reaches the other and both independently identified receive-only V3s. Existing gateway/portal configurations unchanged. [Setup and recovery record](../docs/operations/rak-pilot-setup.md), [TEST-006](field-results.md#test-006--stock-rak-pilot-repeater-preparation).
- Final explicit reboot/reconnection checks pass both complete profiles. Local Python cleanup reports an already-disconnected stream after reboot requests; successful subsequent readbacks verify the devices. No battery power cycle performed.
- Owner later completes the earlier requested double-reset gesture, exposing both RAK4631 recovery drives. Recopy the same checksum-verified stock UF2 without erasing configuration; both return to COM8/COM9 and pass the complete independent pilot-profile checks again. No further button action needed.

Next useful step: physically label R001/R002, reconnect a GPS V4, then prove each repeater is required in an isolated V4-to-RAK-to-V3 path with original GPS measurement times retained at dispatch. Sustained freshness, local operation during internet loss, actual battery/solar assembly and runtime remain untested. No decision ticket status changed; custom survey work stays deferred.

## 2026-10-14 — Real MQTT GPS portal deployed; secrets stored in 1Password

- Owner authorizes the recommended receive-only GPS integration, replacement of fake data and project-secret storage in 1Password. Create SNORR MeshLink — Pilot and store the existing channel/broker/gateway/portal provisioning secrets and replacement Wi-Fi without password rotation or values in Git/logs. Windows MCP environment mounts are unavailable; root-owned group-readable LXC JSON config is provisioned separately and does not automatically sync vault edits. Owner corrects broker SSH to `mqtt.snorr.org:64582`; export only the read-only worker credential.
- Apply/read back replacement Wi-Fi on both V3s, preserving MQTT and transmit-disabled LoRa configurations. Independently identify COM4 B002, COM5 B001, COM6 G001, COM7 G002 and confirm four distinct stable hardware identities. No quantities, firmware or RAK changes. Owner restores B001 reporting during live validation.
- Implement encrypted Meshtastic position decoding, verified node/gateway mapping, true GPS-solution timestamps, gateway-independent packet identity, private durable API retry queue, broker-aware heartbeat/reconnect and service supervision. Correct an early `Position.time` clock mistake to `Position.timestamp`; regression coverage prevents receipt/transmit clocks refreshing old fixes. Native simulation remains a development tool; the guarded installer cannot overwrite live provisioning.
- Automatic review rejects broad broker-export disclosure; a scoped worker-only export succeeds. It also rejects a proposed partial-tracker cutover; no partial cutover occurs. After owner reports B001 fixed, the strict five-minute preflight passes all four paths with actual GPS ages about 6–75 seconds. A backup/verified isolated recovery precedes the transactional real-device cutover. The backup verifier now waits for API HTTP readiness after service restart, fixing an observed startup race.
- Hosted API has simulation disabled and four real bench devices, with demo members/accounts retired/disabled and admin access preserved. Publish the sign-in-first live frontend. The live worker saves two observations/four receipts initially; after a verified worker restart, three observations/six receipts are retained, with both trackers deduplicated across both gateways. Latest checked ages after restart are about 143–145 seconds. Inbound/outbound text, name updates and telemetry remain separate/unimplemented. [TEST-005](field-results.md#test-005--live-portal-gps-ingestion).
- Verify the new live backup, isolated restore, proxy authorization/throttling and credential-free public HTTPS boundaries. Public browser sign-in entry renders; authenticated live map/history browser QA remains outstanding. All 36 backend tests and eight frontend tests pass; pinned Node build/TypeScript, Python/shell/service syntax and whitespace checks pass. Existing MapLibre size warning remains. Private raw tracks, credentials, DB/queue and unrelated untracked 3MF stay outside Git.

Next useful step: owner reviews the authenticated live map/history using the unchanged admin login now stored in 1Password, then measure sustained freshness, phone-free startup, Wi-Fi/broker outages and battery runtime. Real member provisioning and off-host backups remain outstanding. Commit/push this coherent integration checkpoint; no ticket status/decision changed, no survey/wishlist expansion or outbound radio feature activated.

## 2026-10-14 — Live portal development prerequisites reviewed

- Owner resumes development and asks what is needed to connect MQTT and replace fictional portal data. Reviewed the handoff, current worker, ingestion validation, physical bench identities and LXC deployment records. Real radio-to-MQTT GPS delivery is already recorded; the missing implementation is the persistent encrypted-protobuf adapter feeding the authenticated normalized ingestion endpoint.
- Interpret the requested replacement as a real-device-only cutover. Plan a verified hosted backup before retiring fictional operational records, preserve portal access, provision the two V4 trackers/two V3 gateways with verified physical mappings, and disable simulation updates and simulated send/name outcomes. No hosted records or services changed.
- Prerequisites: privately provision the existing read-only MQTT account and channel key to the worker host; build/test decoding, timestamp preservation, duplicate receipts and reconnect/outage behavior; keep both V4s powered with sky view and both V3s on working Wi-Fi for end-to-end verification. Desktop serial ports are accessible, but local bench dependencies and per-V3 port mapping still need setup if serial inspection is used.

Next useful step: implement the receive-only GPS adapter and safe real-device provisioning/cutover procedure, then deploy after backup and verify live GPS in the portal. No implementation, new hardware test, ticket resolution, commit or push in this prerequisite review.

## 2026-10-14 — All four Windows serial ports accessible

- After owner reconnects the V3s, both CP2102 bridges report healthy drivers (error code 0), assigned COM6 and COM7. Both V4 ports COM4/COM5 and both V3 ports COM6/COM7 pass brief native open/close with DTR/RTS disabled. No additional Windows driver permissions needed for serial access.
- No firmware/configuration changes, GPS/MQTT delivery test or hosted deployment. V3 label-to-port mapping remains to read through the device protocol.

Next useful step: install local bench dependencies and read device identities, then resume the MQTT ingestion adapter using the accessible LXC. Hosted simulation-data handling remains to settle before changing its database.

## 2026-10-14 — Windows driver installation recheck

- Owner reports driver installed. One CP2102 bridge now has a healthy driver and COM6; native open/close passes on COM4, COM5 and COM6. The second CP2102 bridge still reports missing-driver error 28 and has no COM port. Per-V3 identity remains unverified. No hardware quantity changes.
- Windows hardware rescan via `pnputil /scan-devices` is denied by the current Windows token even outside the sandbox. No radio/configuration changes or application-level packet tests.

Next useful step: unplug/replug both V3s to trigger driver detection; if the second bridge remains unconfigured, use administrator Device Manager to apply the installed CP210x driver to that device.

## 2026-10-14 — Windows desktop access smoke check

- Synced main from origin (already current), preserving the unrelated untracked 3MF file. Firmware submodule is pinned but not initialized in this checkout.
- All four boards enumerate on Windows USB. V4 descriptor identities match B001 on COM4 and B002 on COM5; both ports pass a brief native open/close with DTR/RTS disabled. Both CP2102 bridges have Windows device error 28 (missing drivers), so neither V3 has a COM port. No firmware/configuration write or application-level GPS/radio test performed.
- Initial sandbox CIM/WSL access denials clear with approved outside-sandbox read-only checks. Ubuntu-24.04 WSL starts as the owner, with Python available but no attached USB serial devices. Native Python lacks serial/Meshtastic/MQTT packages. Existing SSH access to root@meshlink.int.spp.lol succeeds; API and simulation worker services are active. No hosted data/service changes.

Next useful step: install the signed [Silicon Labs CP210x Windows VCP driver](https://www.silabs.com/software-and-tools/usb-to-uart-bridge-vcp-drivers) with Windows administrator access, then verify both V3 serial ports and set up local bench dependencies. Native Windows serial plus LXC deployment is available; WSL USB passthrough is unnecessary for that path. Live MQTT adapter and hosted demo-data choice remain pending.

## 2026-10-14 — Dell Linux to Windows/WSL development handoff

- Owner requests committing/pushing all pending publishable work for desktop continuation and confirms regular switching between the Dell Linux laptop and Windows desktop running WSL. Record the ongoing workflow in PROJECT.md, the environment plan, inventory and the linked handoff; GitHub is the sync point for both machines.
- Handoff includes broker setup/testing/password-compatibility scripts, serial access/export helpers, source review, bench checklist and sanitized four-device radio/MQTT/GPS evidence. Private credentials, channel key, flash backups, raw GPS captures, local databases and private bench helpers remain ignored on the Dell; they are not transferred through GitHub.
- Portal is still the hosted simulation. Live MQTT ingestion was explicitly brought forward but no adapter/deployment has started. The next developer must settle demo-data handling, provision stable physical identities and build/test the persistent worker before claiming live portal tracking. No additional hardware or radio changes in this handoff.

Next useful step on Windows/WSL: pull main (including submodules), read docs/operations/development-handoff.md, then resume the live ingestion adapter. Python compilation, shell syntax, Git whitespace and unchanged pinned firmware-submodule checks pass. The isolated broker test cannot be rerun on this Dell because `mosquitto_passwd` is absent; the earlier recorded remote test pass is retained without claiming a new pass. Publication follows this checkpoint commit.

## 2026-10-14 — Live portal MQTT integration brought forward

- Owner asks to connect MQTT to the portal and identify prerequisites. Reviewed existing deployment, normalized ingestion boundary and private bench subscriber code. Broker worker credentials and channel key already exist privately; the remaining software is a persistent decoder/identity adapter and hosted worker integration, replacing synthetic updates.
- Recommend first connecting the two verified V4 trackers and two V3 gateways for read-only GPS ingestion, preserving measurement timestamps and per-gateway receipts while deduplicating displayed observations. Confirm handling of existing fictional portal records before changing hosted data. Keep live devices powered with GPS sky view for end-to-end verification. No deployment, credential transfer, database change, radio transmission, ticket resolution, commit or push performed; existing edits preserved.

Next useful step: confirm whether the hosted portal should show only real bench devices or retain a separately labelled simulation, then implement/test and deploy the ingestion worker with a backup and live GPS verification.

## 2026-10-14 — Replacement hotspot and real GPS delivery verified

- Owner reconnects nodes, reports satellites and supplies new hotspot credentials. USB permissions changed; owner restores scoped ACL access after interactive sudo is required. Initial automatic permission-review timeout succeeds on its permitted retry. Save new Wi-Fi privately, apply to both V3s and verify private equality with MQTT config unchanged and LoRa transmit disabled. Both gateways reconnect to Wi-Fi/MQTT.
- Direct snapshots show internal GPS positions on both V4s. First observation spanning the hotspot transition sees B001 only; subsequent clean automatic observation sees one real GPS report per V4 through both gateways (4/4 paths). B001 reports 9 satellites and 21.13-second fix age; B002 reports 8 satellites and 35.40/35.41-second fix age at subscriber receipt. Original GPS measurement timestamps survive encrypted radio/MQTT delivery. No forced/synthetic position used. [TEST-004](field-results.md#test-004--automatic-gps-positions-through-both-mqtt-gateways).
- Raw coordinates, Wi-Fi/broker credentials and evidence stay ignored/private. Temporary observer exits after collection; no continuous recorder or live portal adapter installed. Short sample does not establish sustained delivery, phone-free startup, outage behavior, battery runtime or field performance. No firmware source change, inventory quantity change, ticket decision, commit or push; unrelated edits preserved.

Next useful step: connect a persistent MQTT ingestion worker to the existing portal database, then measure sustained GPS freshness/duplicate handling, power-on behavior and battery runtime separately.

## 2026-10-14 — Actual Heltec MQTT delivery and reboot recovery pass

- Owner completes the guarded broker password compatibility fix. Retrieve its private export, confirm both gateway credentials are 30 bytes, then provision both V3s. Exact saved credentials, TLS endpoint/root/encrypted-protobuf settings, uplink-only channels and disabled LoRa transmit pass private readback. Both gateways connect to the hotspot and public broker; worker credential remains usable.
- Each V4 encrypted fixture reaches the read-only worker subscriber through both V3s: 4/4 member/gateway checks pass. Independently reboot both V3s, verify every networking/receive-only setting persists, then confirm reconnection and repeat fresh fixtures: 4/4 pass again. Subscriber verifies broker certificate/hostname; stock Heltec direct TLS uses `setInsecure()`, so its server identity validation is not established. Serial debug logging is suppressed; credentials/configs/captures stay ignored/private.
- Update sanitized readiness, inventory and TEST-003 records. All four boards are stock-flashed/profile-verified and ready for passive GPS/runtime testing. No fresh GPS positions collected, portal adapter integrated, battery runtime measured, broker/hotspot outage test or sustained delivery claim. No hardware count changes, firmware source patch, ticket decision, commit or push; unrelated edits preserved.

Next useful step: give both GPS-equipped V4s sky view and verify fresh GPS measurement timestamps through both gateways, then measure phone-free restart/reporting and battery runtime. Portal ingestion remains a separate unfinished adapter.

## 2026-10-14 — Hotspot connected; stock MQTT password limit found

- Owner supplies hotspot/broker credentials and reports a hotspot reset in compatibility mode. Native NetworkManager confirms actual SSID is the original hotspot name; the parenthesized string is its Wi-Fi interface label. Both V3s associate and obtain IPs after recovery. Saved SSID/password matches are checked privately; credentials remain mode-0600 under ignored `private/bench/`, never copied into project records.
- Broker SSH recovers after network blip; reading its root-private credential file requires interactive sudo. Prepared/uploaded a private export helper, but owner supplies credential JSON instead. Permission-review timeout recovers on the single permitted retry; no ongoing approval rejection.
- Certificate/hostname-validating read-only subscriber authenticates to public broker. Gateway provisioning still leaves MQTT off and account settings unchanged: supplied gateway passwords are 48 bytes, whereas pinned NanoPB MQTT password field allows 31 bytes plus terminator. Actual two-V4/two-V3 MQTT fixture test receives zero of four expected deliveries; this is a failed client-provisioning test, not proof of a broker transport/ACL defect. No GPS/portal claim.
- Correct future fresh-installer gateway generation to 30 characters, retaining 48-character worker credentials. Prepare/upload [guarded live compatibility fix](../scripts/server/fit-v3-mqtt-passwords.py) that replaces only the two gateway passwords, preserves worker/ACL/listeners, backs up privately, reloads, verifies and exports privately. [Isolated real-Mosquitto tests](../scripts/server/test-fit-v3-mqtt-passwords.py) pass new/old authentication, worker/hash/ACL preservation, rerun idempotency and injected-failure rollback. Syntax and local/remote SHA256 match; no production account changes performed.
- Owner sudo execution requested as the remaining privileged step; new values will be retrieved privately, not pasted. All radios retain their verified roles; no firmware source patch/flash, ticket resolution, commit or push. Other in-progress changes preserved.

Next useful step: owner runs the uploaded compatibility fix, retrieve its owner-private export, provision/read back both V3 accounts, then verify live radio-to-MQTT delivery and reconnect. Fresh GPS and portal ingestion remain separate.

## 2026-10-14 — Four Heltecs prepared; local radio smoke passes

- Owner runs runtime serial helper, reconnects missing V4, selects US on the three flashed nodes and confirms attached antennas. Runtime rules preserve access through USB re-enumeration. Newly reconnected V4 `!699ca878` is original 16MB/2MB PSRAM hardware on old `2.7.15.567b8ea`; 1200-baud touch reaches bootloader. Privately back up its configuration/full flash, then clean-install and independently verify stock factory/recovery/filesystem images. All four now run `v2.7.26.54e0d8d`; firmware source/submodule unchanged.
- Finish shared private channel and full saved profiles. Bench B001/B002 V4s have GPS enabled, 60-second acquisition, 120-second reporting, smart/fixed position off and measurement timestamp flag; G001/G002 V3s have no GPS and remain transmit-disabled. US initialization re-enables TX/generates keys; restore each intended role explicitly. First second-V4 readback catches partial setup; reapplication after initialization passes. Final independent reboot checks every specified field and all four bench labels/roles.
- Local encrypted text fixture smoke: each V4 reaches both V3s, four of four reception checks pass. No RAK, actual MQTT connection or fresh position event in this short run. Normal hop limit 3 does not establish direct-only paths. [Sanitized TEST-001/TEST-002 evidence](field-results.md#test-001--stock-heltec-provisioning); raw backups/configs/packets/key remain ignored/private.
- Wi-Fi/MQTT remain disabled while current endpoint/root/TLS/encrypted protobuf settings are staged. Bench host cannot reach authorized broker SSH via public or recorded private address from its current connection; no broker fault/configuration change inferred. Requested local private credential paths and Wi-Fi choice; no secrets requested in chat. Existing software MQTT confirmation remains valid; actual gateway delivery/portal adapter and GPS freshness/runtime remain to test.
- All four firmware/profile/role checks and local fixture reception pass. No ticket decisions, purchases, survey/SOS implementation, firmware patch, commit or push. Preserve unrelated in-progress broker records/scripts.

Next useful step: privately provision both V3s' selected Wi-Fi and fresh broker accounts; obtain/measure phone-free fresh GPS fixes with sky view, then verify their original measurement timestamps through actual MQTT packets. Portal ingestion and field/runtime tests remain separate.

## 2026-10-14 — Three Heltecs flashed; V3 profiles prepared

- Owner grants temporary serial access. Privately export configs/full original flash for original V4 `!699c2ed8` and V3s `!9ea13cc0` / `!849ad7a0`. Second V4 with USB serial ending `A878` is absent before inspection. Confirmed 16MB/2MB PSRAM V4 and 8MB V3 chips; frequency/antenna/current-location confirmation requested before RF enablement.
- Clean-install stock `v2.7.26.54e0d8d` on all three accessible boards from checksum-verified release archive and target-manifest partition offsets. Esptool independently verifies factory, recovery/OTA and filesystem images. First V3 no-reset connection attempt fails before erase; CP2102 default reset succeeds. Firmware submodule/source unchanged.
- Both V3s boot stock release and receive shared private-key uplink-only profiles. Region UNSET, transmit disabled, GPS not present, Wi-Fi/MQTT disabled; endpoint/root/TLS/encryption staged without credentials. Bulk config writes initially drop settings; single-write probe succeeds, private logs show UART0 buffer overflow, and 0.4-second pacing plus 3-second commit hold removes overflows and processes MQTT settings. Check saved fields and reboot rather than trusting host command success.
- Applied diagnosing-bugs skill to V4 serial failure: bounded probes time out, RTS reset leaves flasher accessible, watchdog reset re-enumerates as ACM0 and loses temporary ACL. Image verification passes; post-boot API/GPS/profile verification still awaits owner-local access. Prepared [runtime serial ACL helper](../scripts/bench/grant-heltec-serial-access.sh), limited to three observed hub sockets and missing V4 serial and expiring at reboot; owner root execution requested, not performed by agent.
- Final independent reboot verifies both V3 bench short names and complete profiles, including staged MQTT endpoint/root/TLS and shared private channel; all assertions pass. Shell/Python syntax and documentation whitespace pass, firmware checkout stays clean. Recorded inventory and [TEST-001](field-results.md#test-001--stock-heltec-provisioning). No RF/GPS/runtime/actual MQTT results, ticket decisions, firmware code changes, commit or push. Unrelated MQTT records/scripts preserved.

Next useful step: owner runs runtime access helper, reconnects missing V4 and confirms 915MHz/antennas/US location; finish V4 identification/setup, privately provision V3 Wi-Fi/current broker accounts, then begin phone-free GPS/RF/MQTT measurements.

## 2026-10-14 — Four Heltecs connected; bench flashing preparation

- Owner confirms MQTT tested and connects 2 V4 / 2 V3 boards, authorizing formatting/flashing as needed. Authenticated MQTT delivery/ACL evidence is already recorded in the following completed broker session; no broker re-test needed for initial preparation.
- Escalated read-only USB discovery confirms two native Espressif ports and two CP2102 ports. Sandbox hides the device nodes, and host serial opens fail with OS permissions: current user is not in dialout and noninteractive sudo requires a password. Requested owner-run temporary user ACL on exactly the four connected ports; physical frequency/antenna/location confirmation requested before enabling transmission.
- Installed esptool 5.5.0 / Meshtastic Python 2.7.11 in ignored project `.venv`; downloaded the official pinned `v2.7.26.54e0d8d` ESP32-S3 archive into ignored private storage. GitHub release SHA256 `339650ced8b8c859751f04be69c6af845fea96baca1327518f199afd2595a9d4` matches; V3/V4 factory image headers/checksums validate and specify 8MB/16MB respectively. Prepared private configuration inspection/backup helper; exact board identification precedes image selection.
- No serial configuration read, flash/erase, device configuration write or RF test yet. Existing project edits and clean firmware submodule preserved; no commit requested/made.

Next useful step: owner grants temporary serial access and confirms antenna/frequency/location; inspect/back up each board, flash matching pinned stock images only where needed, then save/read back a shared private bench configuration.

## 2026-10-14 — Authenticated public MQTT delivery and ACL checks pass

- Owner runs the uploaded public-check script with sudo and supplies all PASS lines. Existing V3 accounts publish non-retained synthetic messages through certificate-validated public TLS and the worker receives them. Anonymous/invalid logins, worker writes, gateway reads and JSON/unrelated-topic writes are denied. Credentials remain server-private and no broker configuration changes occur during the check.
- Closed the temporary SSH relay; independent SSH confirms no 18884 listener and active Mosquitto. Updated current broker/project/bench records to reflect successful authenticated software testing, preserving historical pending observations. No radio/GPS/reconnect/runtime or live portal ingestion claim.
- Documentation whitespace checked. No commit requested/made; other in-progress bench work preserved.

Next useful step: begin selected-build V4 GPS/V3 MQTT hardware bench using the recorded checklist, verify actual packet delivery and reconnect, and implement live portal ingestion when brought forward. Broker-side initial-uplink readiness is verified.

## 2026-10-14 — Authenticated public MQTT test prepared

- Owner asks how to verify valid-account delivery. Added/uploaded a read-only configuration check script reusing the established MQTT 5 protocol/ACL test helpers; reset entry point is never invoked. Reads server-private credentials only under owner-interactive sudo, sends non-retained synthetic fixtures and validates gateway publish/worker receipt and denied permissions over certificate-validated TLS.
- Broker-origin direct public endpoint probe times out, potentially due to router hairpin routing; cause unconfirmed. Opened a temporary reverse SSH relay bound to broker loopback 18884, routing through this external test host to public TLS 8883. SSH independently confirms loopback binding and the credential-free public TLS/anonymous-rejection check passes. Initial relay connection timed out; retry succeeds. No credentials read/transmitted yet, permanent service change or authenticated PASS claimed.
- Python syntax/upload checks and documentation whitespace checks pass. Preserved other in-progress bench records. No commit requested/made.

Next useful step: owner runs uploaded check script with sudo and relay options, shares status only; investigate any failure, then close the temporary relay. Record authenticated result before declaring external account/topic testing complete.

## 2026-10-14 — Heltec V3/V4 bench readiness verified against records and sources

- Owner requests bench readiness verification. Reviewed project/tracker, inventory, planned test criteria, MQTT handoff, worker and clean release-pinned firmware submodule. Prepared [bench checklist](../docs/operations/heltec-bench-checklist.md) and delegated [primary-source review](../docs/research/heltec-bench-source-check.md).
- Stock configuration supports a small V4 GPS / V3 receiver evaluation after exact revision/image, GPS wiring, power/antenna, radio settings and viewer checks. Two GPS-equipped V4s and nine GPS-less V3s are owner-reported stock; condition and availability at this session remain unverified. No mandatory GPS patch identified. The six-member field pilot still needs planned additions and later relay/runtime/outage evidence.
- Public TLS/broker rejection and local ACL evidence exist, but valid-account external delivery remains to test. Confirmed pinned MQTT source logs credentials, disables TLS certificate verification and gates other-node uplink at public-IP brokers by the packet's OK-to-MQTT flag. Recorded private-log/isolated-credential precautions and explicit member forwarding configuration.
- Full live portal bench requires MQTT/protobuf adapter work; worker remains simulation/replay-only. Initial broker ACLs still prevent portal downlink; survey responder/GUI remain deferred/unimplemented. No ticket claimed/resolved, hardware/inventory quantities changed, server changes, credentials read, firmware build/flash or measured bench results. No visible USB serial radios in the agent environment. Preserved existing unrelated edits; no commit requested/made.

Next useful step: identify one V4 revision/GPS connection and one V3 radio variant, select matching stock images and save/read back a private bench profile, then run phone-free GPS to local receiver before adding authenticated MQTT uplink.

## 2026-10-14 — Nginx-to-Mosquitto access restored and publicly verified

- Owner runs the guarded backend installer successfully. It retains loopback/accounts, adds broker LAN 1883, privately backs up configuration/firewall, and allows only Nginx's `192.168.12.254` source before blanket IPv4/IPv6 1883 deny. Owner supplies active UFW output and local anonymous-rejection PASS; SSH independently confirms active Mosquitto and both listeners.
- External `mqtt.snorr.org:8883` verifies TLS 1.3 and the matching certificate. Anonymous and invalid-account MQTT CONNECT requests receive not-authorized CONNACK in 0.11/0.12 seconds, replacing the earlier 10-second closes and confirming proxy-to-broker MQTT reachability. Public 1883 times out from the test origin.
- Valid-account publish/subscribe, external ACLs, unrelated-LAN denial, actual firmware/reconnect and certificate renewal remain untested. No credentials read/transmitted or operational packets published. Script syntax/checksum and documentation whitespace checks pass; no commit requested/made.

Next useful step: privately run authenticated synthetic publish/subscribe and ACL tests through public TLS, then integrate the selected gateway/worker when brought forward. Survey and other held work remain deferred.

Bench-readiness guidance — Owner asks whether more Mosquitto configuration is needed. Reviewed installed-template account/ACL design and current official Mosquitto/Meshtastic documentation. No additional broker configuration identified for initial passive-tracking uplink bench; authenticated public delivery/permission checks remain the next verification. Recorded V3 endpoint/root/settings and corrected legacy hostname in the handoff. Current ACLs intentionally block portal downlink and the existing portal worker remains simulation-only; those later integrations are separate from broker transport readiness. No account/ACL/device/server change or additional ticket resolution. Documentation whitespace checked; no commit requested/made.

## 2026-10-14 — Public MQTT endpoint tested after DNS/Nginx rollout

- Owner resumes endpoint testing and supplies root SSH on `mqtt.snorr.org:64582`. DNS resolves, TCP 8883 connects, and TLS 1.3 verifies a matching Let's Encrypt certificate expiring 2027-01-11.
- Two anonymous MQTT 3.1.1 CONNECT probes each close after about 10 seconds without CONNACK; initial 8-second probe times out. Public 1883 times out from this origin. TLS rollout is verified; Mosquitto forwarding/authentication/ACLs are not.
- Root SSH rejects available key/configured 1Password agent. Requested existing key/account information without secrets. No server changes, credentials read, authenticated traffic, real packets or hardware tests. Prior loopback-only listener is a possible separate-proxy obstacle, not a newly confirmed cause.
- Recorded sanitized results in sites and the connectivity ticket. No commit requested or made.

Next useful step: restore authorized SSH access, inspect current Mosquitto listener/firewall and Nginx stream upstream/error logs, then verify authenticated publish/subscribe and topic ACLs through public TLS. Survey and broader integration remain deferred.

Follow-up — Owner corrects SSH account to `setheth`; SSH succeeds. Active Mosquitto is reverified on loopback 1883 only, with anonymous local CONNECT returning not authorized immediately; Nginx is inactive on this host, which has no 8883 listener. A separate edge cannot reach the loopback backend. Sudo requires a password, so requested owner-run UFW status and Nginx private source/upstream details before configuring restricted LAN access. No remote changes or credentials read. Next useful step is the restricted backend listener/firewall configuration, followed by external MQTT auth/ACL verification.

Backend preparation — Owner supplies firewall rules and Nginx source `192.168.12.254`; broker LAN address is inspected as `192.168.12.51`. Added/uploaded guarded private-backend installer without resetting accounts; local/remote Python syntax and upload checksum match pass. Installer awaits owner-interactive sudo, checks active/default-deny UFW and expected configuration, backs up privately, restricts 1883 to proxy, preserves loopback and rolls configuration back on broker verification failure. No privileged changes executed. Next owner runs the uploaded installer, shares sanitized status and confirms Nginx upstream `192.168.12.51:1883`; then repeat external MQTT tests. No commit requested/made.

## 2026-10-13 — Portal LXC deployed through Cloudflare

- Owner confirms LXC creation, authorizes root SSH setup and chooses `meshlink.spp.lol`. Inspected Ubuntu 24.04.5 amd64 with 4 CPUs, 8 GiB RAM, 512 MiB swap and 64 GiB SSD-backed root filesystem; recorded virtual resources without altering radio counts or inventing costs. Portal hosting resumes; MQTT/survey holds remain.
- Added reproducible deployment source for static Nginx/PocketBase/Python simulation services, private persistent state, restricted public API routes, per-client proxy IP/throttling and Ubuntu security updates. Owner installed/configured the existing remotely managed Cloudflare connector; preserved it and verified four connections plus the loopback-8080 route. No second tunnel, router forwarding, MQTT adapter or Cloudflare protection change.
- Isolated the hosted worker under a separate OS account with only its own credential JSON; verified ingestion succeeds while admin credentials/database reads are denied. Native development retains its original credential path. Backend checks rerun after this worker-source change.
- Daily 02:30 Pacific root-private backups retain 14 local archives, quiescing the worker/API for consistent state and including matching source/build. Verified checksum, SQLite integrity, restored credentials/assignments/messages/incidents/events and retained history via a separate loopback API; live state was not replaced. Off-host/Proxmox backups remain pending owner-selected storage/access.
- Verification: existing 27 backend and 8 frontend tests, TypeScript/production build, Nginx/shell/Python syntax, loopback sign-in/role boundaries, independent client throttling, restart persistence, isolated restore and credential-free public HTTPS/certificate/API boundaries pass. Existing MapLibre bundle warning remains. Public DNS is correct; LAN DNS retains an older negative IPv4 result, blocking desktop browser review during setup. Cloudflare blocks Python's default user-agent; curl probes pass without altering protection.
- Automatic approval review rejected transmitting generated admin credentials through Cloudflare for a public sign-in test. Replaced that test with credential-free HTTPS probes and retained loopback authenticated checks; no credentials/tokens published. Owner public browser sign-in and actual reboot recovery remain unverified. Preserved unrelated battery-box model. Completed source/records checkpoint is committed/pushed to main; final response reports result.

Next useful step: owner opens the portal and signs in using privately viewed generated credentials after LAN DNS catches up; configure off-host Proxmox backups, then resume live MQTT integration only when the owner brings it forward.

## 2026-10-13 — Ubuntu LXC portal sizing

- Owner resumes portal hosting setup and selects Ubuntu LXC on Proxmox. Reviewed the current PocketBase/Python/static React stack and primary Proxmox/Ubuntu documentation; recommended 2 cores, 2 GiB RAM, 512 MiB swap allowance and 32 GiB SSD-backed storage in an unprivileged Ubuntu 24.04 LTS container, with direct services, a stable LAN address and start at boot. Recorded the proposed hosting configuration in sites; these are estimates, not confirmed allocations or measured capacity.
- No container created, service deployed, broker integration resumed or hardware count changed. MQTT and other held work remain held. Documentation whitespace checked; unrelated storage-box file preserved. No commit requested or made.

Next useful step: owner creates the container and supplies its Ubuntu version and LAN address privately as appropriate; then configure access, pinned runtimes, persistent services and a tested backup/restore before HTTPS rollout.

## 2026-10-13 — Project held and desktop handoff checkpoint

- Owner requests holding the survey issue, wrapping all current project progress and pushing it to GitHub for another desktop. Released the survey claim, left it open/deferred, recorded the project-wide hold in the map/project brief and added [desktop handoff](../docs/operations/desktop-handoff.md). Resume only at owner direction; no planning decision falsely marked complete.
- Checkpoint includes accumulated portal launcher/test/documentation work, broker maintenance/reset scripts and sanitized hosting/handoff research, hardware/field planning records and accepted RAK/Dell survey requirements. Firmware submodule remains clean at the published release pin; no survey firmware/GUI built or hardware-tested.
- Verification: all 27 backend tests pass with localhost sockets enabled (initial sandbox run could not create sockets). Portal tests, TypeScript checking and production build pass; existing large-map-bundle warning remains. Both server shell scripts pass `bash -n`; reset script passes Python compilation. Publication candidate secret-pattern scan finds no matches; Git excludes private credentials/databases/raw tracks, binaries, dependencies and generated output. Documentation diff check passes. Privileged server scripts were not rerun; external broker path and firmware/hardware behavior remain unverified.
- Owner-authorized commit/push checkpoint targets `main` on `origin`; final response reports commit and push result. GitHub contains reproducible source/planning, not the current ignored local database or credentials. New-desktop setup and private-data transfer limits are documented in the handoff.

Next useful step: clone/update recursively on the other desktop and read the handoff. Keep work held until owner resumes the selected task.

## 2026-10-13 — Survey GUI behavior accepted and live map added

- Owner accepts proposed scheduling, run controls, disconnect handling and automatic logging with optional labels/configuration segments. Added live GPS/signal map to active tester scope to help revisit dead spots during a run.
- Recorded success/timeout attempt markers, per-repeater inspection and an independent timestamped GPS stream as the map design direction. Distinguish failed round trips from directional loss and stale/no-fix locations from precise measurements. Offline basemap preparation remains to verify; map availability must not block logs/readouts.
- Survey draft/ticket updated; broad operations ticket remains claimed pending field/power requirements. No GUI/firmware implementation or hardware test. Documentation diff checked; unrelated edits preserved, no commit requested or made.

Next useful step: implement the touchscreen survey prototype and RAK responder, verifying selected-build GPS availability, PKI and direct-only exchanges; verify offline map preparation before field use.

## 2026-10-13 — Touchscreen multi-repeater survey GUI requirements

- Owner requires a simple touchscreen Dell GUI with large buttons, touch input pads, one-or-more repeater selection and interval/other parameters. Recorded accepted requirements in the survey draft/ticket.
- Proposed sequential round-robin scheduling with one outstanding ping and interval between individual attempts, configurable timeout/continuous or finite runs, automatic private logging with configuration labels, and pause/explicit resume after tester disconnection. These behavior choices await owner input; no UI built, firmware changed or hardware tested.
- Broader operations ticket remains claimed. Documentation diff checked; unrelated edits preserved, no commit requested or made.

Next useful step: settle scheduling, disconnect behavior and run labels, then implement the simple touchscreen tester alongside the pinned-release responder.

## 2026-10-13 — Always-available survey responder accepted

- Owner selects always-available response to authorized survey pings because RAK nodes will be placed in hard-to-reach locations. Recorded rationale and behavior in the repeater ticket and survey draft: no physical visit/per-survey enable step, Dell drives attempts, and RAK responds only to valid requests authorized by the separate survey public-key allowlist.
- First-prototype direction now includes RAK4631, Dell GUI and transferable V4 native-PKI keys. Broader field/power decisions remain open; operations ticket stays claimed. No implementation, provisioning, build, flash or RF test. Documentation diff check passed; unrelated edits preserved. No commit requested or made.

Next useful step: specify the minimal GUI/logging controls and implement the pinned-release responder/tester prototype, followed by direct-only and authorized/unauthorized bench checks when hardware is available.

## 2026-10-13 — Portable survey key accepted

- Owner accepts transferring the tester private key to the V4. Recorded native PKI with a separate survey public-key allowlist as the chosen authentication approach in the existing repeater ticket and survey draft. Replacement tester hardware requires keypair restoration and node/key discovery; no admin rights implied.
- RAK4631 target and Dell-driven GUI remain confirmed. Survey enablement and GUI defaults remain open; broader operations ticket not resolved. No secrets generated/read, provisioning, firmware changes, build or flash performed. Documentation diff check passed; unrelated edits preserved, no commit requested or made.

Next useful step: settle whether the authorized responder is always available or explicitly enabled, then prepare the minimal responder and Dell GUI bench prototype.

## 2026-10-13 — RAK target and GUI tester clarified

- Owner confirms RAK4631 cores and Dell-driven V4 testing with a GUI/readout; updated inventory without changing counts or claiming verified frequency variants/condition.
- Checked pinned firmware routing/admin key handling and primary cryptographic documentation, with a delegated read-only source check. Native survey public-key authorization is feasible; keys live on tester radios, can migrate to replacement hardware, and still need node/key discovery. Proposed a survey-only allowlist separate from admin privileges. Dell-held payload signatures are an alternative requiring additional implementation/replay design.
- Recorded accepted hardware/test-control direction and proposed authentication/GUI scope in the existing survey ticket/draft. No full operations decision resolved, key generated, firmware changed, build, flash or hardware test performed. Existing edits preserved; no commit requested or made.

Next useful step: owner chooses radio-held native PKI versus Dell-held signing key; then specify survey enablement and GUI controls before implementing the first bench prototype.

## 2026-10-13 — RAK survey firmware pre-build readiness

- Used owner-invoked Wayfinder and its grilling/domain-modeling guidance to review the existing repeater survey ticket, inventory, proposed exchange/logging contract and firmware workspace. Confirmed clean firmware checkout at the recorded release commit; preserved unrelated working-tree edits.
- Identified immediate prerequisites: exact RAK core/radio variant, owner choice of tethered versus autonomous tester, and survey enable/access policy. Recommended Dell-controlled V4 testing first and explicitly enabled responder access for a configured tester; these remain proposals. Site selection, solar endurance and field acceptance thresholds can follow the first bench prototype.
- Added the readiness review to [Define repeater operations and direct-link placement testing](../.scratch/pilot/issues/14-repeater-operations-survey.md). No decision resolved, firmware implementation, build, flash or RF test performed. No commit requested or made.

Next useful step: identify the selected RAK core and settle tester control/access, then verify the direct-only module/API paths against the pinned release before implementation.

## 2026-10-13 — Firmware fork added and RAK release branch published

- Owner requested adding `lfg-seth/firmware` as a submodule and creating a current-public-release RAK branch. Added `firmware/`, configured its tracked branch as `snorr/rak-survey`, and published that branch to the fork.
- Verified GitHub latest public release is `v2.7.26.54e0d8d` (title Beta, GitHub prerelease=false), commit `54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb`. New branch matches that release exactly; existing fork develop remains `76d5156e72d9d9aaa9722b7bbc1336335b685984`. No old customizations merged or history rewritten.
- Initialized the release-pinned protobufs and meshtestic submodules; verified clean firmware tree and remote branch SHAs. Added [workspace/setup notes](../docs/research/firmware-workspace.md). Exact owned RAK core remains unknown; no firmware build, flash, RF transmission or hardware test performed.
- Commit scope is submodule configuration/pointer, setup notes and this session entry. Existing portal/broker/repeater-planning working-tree changes are preserved outside this commit. No tracker decision resolved.

Next useful step: identify the RAK core, then check the dedicated direct-only ping/pong module design against this pinned release before implementing and building it.

## 2026-10-13 — Dedicated direct-link survey module reviewed

- Owner asks about firmware modifications/plugins, a dedicated packet type, addressed zero-hop exchanges and adjustable usage restrictions. Reviewed upstream primary module/port/routing/airtime/radio/API sources and appended [implementation findings](../docs/research/repeater-operations-survey.md#dedicated-firmware-module--follow-up-source-review) to the existing survey draft/ticket discussion.
- Recommended compiled-in RAK responder module on a private application port, explicit PING/PONG payload, zero-hop/no-ACK requests and replies, and client-controlled attempts. Noted generic reply/ACK hop rewriting, MQTT exclusion, duplicate handling and queue/actual-TX distinctions. Stock V4 with Dell API control is a candidate minimal prototype; autonomous V4 testing and precise radio-time logging may need client firmware.
- Distinguished configurable survey scheduling/congestion policies from regional radio constraints and hardware queue/half-duplex operation. No unrestricted RF operation, global restriction removal, final port number or implementation approved/inferred. Reviewed moving upstream sources only; revision lookup failed, so release/commit pinning remains before implementation.
- No firmware cloned, built/flashed, hardware tested, portal/MQTT work resumed or new decision resolved. Existing edits preserved. Documentation checks only; no commit requested or made.

Next useful step: identify target RAK core and V4 firmware/API versions, pin a firmware revision, and verify a minimal private-port responder plus Dell-controlled direct-only exchange on three nodes.

## 2026-10-13 — Repeater operations and placement survey opened

- Owner steps back from portal work and brings solar RAK repeater operations forward: 2–4 18650 cells, Muzi whip or fiberglass antenna, firmware ping/pong responder and GPS-equipped V4 testing node tethered to Dell log storage. Captured intended builds without changing stock counts or assuming installation permission.
- No installed `$wayfind` skill found after local search; used repository-defined Wayfinder tracker conventions. Created/claimed [Define repeater operations and direct-link placement testing](../.scratch/pilot/issues/14-repeater-operations-survey.md), retaining claim pending owner input. No non-research decision resolved; MQTT remains held.
- Reviewed primary RAK electrical documentation, Meshtastic range-test/role documentation and packet schema. Recorded [draft operations/survey plan](../docs/research/repeater-operations-survey.md): per-packet metrics in both directions, verified direct-only paths, timeout/GPS-age logging, controlled antenna comparisons and separate later GPS relay validation. Recorded power autonomy, cell/charger/cold-charge protection, recovery, mounting and service-access questions. No firmware built, hardware tested or coverage measured.
- Asked owner for prior-test candidate landmarks/routes and coverage gaps. Outstanding: exact RAK/core/cell/panel builds, no-sun endurance target, survey cadence/sample size and route acceptance thresholds. Existing unrelated working-tree edits preserved. Documentation checks only; no commit requested or made.

Next useful step: capture candidate sites and required routes, agree no-sun endurance, then identify one representative RAK power build and bench-check the direct-link responder/logging contract before a field survey.

## 2026-10-13 — Worker readiness review

- Owner asked what comes next and whether DNS completion makes the worker ready for Mosquitto. Inspected worker code, backend contract/tests and current broker handoff. The Python worker supports authenticated synthetic ingestion and normalized JSONL replay only; it has no MQTT connection/subscription, TLS/broker credential configuration or selected-firmware decoder. DNS completion alone will not enable live tracking.
- Fresh Mosquitto local authentication/ACL readiness is recorded, but its last verified listener is loopback-only. Separate-host Nginx requires restricted private access, followed by external TLS/auth/topic verification. No remote probes, broker changes, implementation or tests performed in this review; existing edits preserved.

Next useful step: implement a receive-only MQTT-to-normalized-ingestion adapter with explicit simulation/live modes, reconnect/outage handling and decoder tests using sanitized selected-build packets; verify the external broker path with Mike when ready. No commit requested or made.

## 2026-10-13 — Fresh pilot Mosquitto installed

- Owner ran adapted reset and supplied successful live authentication/ACL test output. Old broker configuration/accounts/data/logs and broker-specific renewal state archived privately at `/root/meshlink-archive/mqtt-legacy-20261013T204408Z`; fresh account credentials stored root-private on server, not read/published.
- SSH follow-up confirms active Mosquitto under its own account, loopback `127.0.0.1:1883` only, no VM 8883 listener, config/data/log directories mode 0750 and enabled scheduled-maintenance reboot timer. Updated current server/project/handoff records from prepared to installed. Unrelated backend/portal launcher edits preserved.
- Local broker accounts/ACLs are ready for tracking ingestion; no command publishing/downlink yet. Restricted separate-host Nginx access needs its private source IP. External TLS/DNS/proxy path, actual V3/worker adapters and SSH password hardening remain pending. No credentials, raw messages/tracks or archive contents accessed during verification.

Next useful step: Mike supplies Nginx private source IP, then enable only that proxy's private 1883 access and test public `mqtt.snorr.org:8883` when Mike is ready. Documentation diff checked; no commit requested or made.

## 2026-10-13 — Broker-only setup resumed and adapted

- Owner authorized making the fresh Mosquitto updates while Mike's external infrastructure remains pending. Inspected live service/private interface; no fresh marker found and sudo still requires local password. Preserved unrelated backend launcher/README/test edits visible in Git.
- Adapted/uploaded reset installer to private 1883, no broker certificates/hooks, intended client hostname `mqtt.snorr.org`, old MQTT archive plus broker-specific old renewal configuration archive, fresh per-gateway and worker credentials/ACLs. Default loopback-only because proxy source IP is unknown; LAN mode requires explicit addresses and active source-restricted UFW preflight.
- Private-backend isolated auth/ACL tests passed. Temporary-filesystem full-flow archive/credential and injected-startup-failure rollback tests use actual isolated Mosquitto with mocked privilege/service operations; real privileged execution remains pending. [Details](../docs/research/mqtt-server-maintenance.md#2026-10-13--private-backend-reset-adapted).

Next useful step: owner runs updated script with sudo, then verify live fresh broker/archive without exposing credentials. Enable restricted LAN listener once Mike supplies Nginx source IP; external infrastructure remains deferred. No live broker reset, firewall change, commit or push performed.

## 2026-10-13 — Combined local launcher

- Owner confirms no Proxmox VM or nodes are available and brought local launch cleanup forward. Added `python3 backend/launch.py` to supervise PocketBase, the synthetic Python worker and Vite in one foreground terminal on Linux/macOS/WSL. Updated backend/portal startup instructions; individual commands remain available for debugging.
- Launcher checks installed dependencies/initialized storage and Node version, refuses duplicate launches and occupied ports, waits for API/portal readiness, binds services to localhost and keeps per-process logs in ignored private storage. Ctrl+C/termination or a child exit shuts down its process groups, stopping the worker before the API; bounded escalation handles unresponsive children. It does not install/reset data or print credentials. Synthetic observations continue to be saved while running.
- Verification: existing twenty backend/installer tests passed. Seven launcher tests passed, including occupied-port preservation, duplicate refusal, startup failure, real child cleanup and forced termination. A disposable real PocketBase/worker/Vite run on temporary ports verified API proxying, ingestion, duplicate refusal, Ctrl+C cleanup, restart with saved data and worker-failure cleanup. Existing port-8090 service was left untouched. Linux verified; macOS/WSL runtimes remain untested. Documentation diff check passed; no commit requested or made, unrelated edits preserved.

Next useful step: stop the existing individual development terminals, run the combined launcher on the Dell and review the saved portal workflows. VM deployment and hardware integration await availability; MQTT remains on hold pending Mike and owner resumption.

## 2026-10-13 — Hypothetical SNORR companion-app forks

- Owner asked whether SNORR could fork the Meshtastic iOS/Android apps and what features would suit the project. Reviewed current primary [Apple source/README](https://github.com/meshtastic/Meshtastic-Apple), [Android source/README](https://github.com/meshtastic/Meshtastic-Android), [Android fork/rebrand guidance](https://github.com/meshtastic/Meshtastic-Android/blob/main/CONTRIBUTING.md#forks-and-rebrands) and [position configuration](https://meshtastic.org/docs/configuration/radio/position/). Both apps use GPLv3-family licenses; distribution requires applicable source/notices and distinct branding under the upstream conditions.
- Suggested hypothetical priorities: GPS measurement age and explicit stale/unknown states, prepared offline field maps, cached device/member assignments, simple member controls, clear local-radio versus dispatch-feed status, and later concise messaging with honest delivery/acknowledgment states. Keep phone-free GPS and device-only SOS in node firmware; an app cannot establish radio coverage or dispatch receipt without evidence.
- Recommended a small customization that preserves the Meshtastic protocol and upstream improvements, after stock-app pilot checks identify actual gaps. Apple/Android have separate UI stacks and ongoing maintenance needs. No app cloned, built or tested; feasibility is source/documentation review only. No active ticket, wishlist activation, firmware selection change, broker work, commit or push. Existing edits preserved.

Next useful step if the owner brings app work forward: compare stock apps on the pilot devices against freshness, offline map and reconnect requirements, then select one platform and a minimal scope. Passive GPS bench testing remains the first hardware priority.

## 2026-10-13 — Next-work review

- Reviewed project records, tracker and portal build checkpoints. Recommended tested backend backup/restore as the next independent software task, followed by VM service supervision and HTTPS deployment. Live MQTT integration remains on hold pending Mike and owner resumption.
- Passive GPS bench testing remains the first hardware priority when nodes are available. No implementation, ticket change, remote check or deployment performed; existing uncommitted work preserved. No commit requested or made.

Next useful step: implement private backend backup/restore and demonstrate recovery into a separate local instance, preserving accounts, assignments, observations and history.

## 2026-10-13 — MQTT issue held pending Mike

- Owner explicitly instructed holding the broker issue until Mike completes infrastructure work. Recorded `mqtt.snorr.org` as intended endpoint, with Mike updating DNS and placing the VM behind Nginx; certificate management belongs to Mike. Completion is unverified.
- Released the connectivity ticket claim and left it open/deferred; updated map, project brief, hosting record and handoff. No broker/proxy probes, implementation, hardening or reset performed after the hold. Earlier update/maintenance verification remains recorded.
- Fresh broker reset is prepared but not executed and needs adaptation for Nginx TLS termination/private port 1883. Firewall activation, SSH-password hardening, live ACL provisioning, actual firmware/client configuration and one-gateway dispatch downlink remain unverified. Documentation diff checked; no commit requested or made.

Resume only when owner brings this issue back after Mike's work is complete. First confirm `mqtt.snorr.org` TLS/proxy reachability, then adapt/archive/reset the broker and test gateway/worker access.

## 2026-10-13 — Nginx MQTT handoff prepared

- Owner reports Mike wants Nginx to own certificates and says certificate management is handled. Prepared [consolidated handoff](../docs/operations/mqtt-nginx-handoff.md) for TLS termination on public 8883, private broker TCP 1883 restricted to Nginx, DNS/client settings, existing SSH preservation and verification. No certificate-provisioning instructions or outreach.
- Recorded current direction over earlier passthrough proposal. Actual proxy/VM addresses, separate/same-host layout and deployed configuration remain unknown. Marked existing fresh-reset installer unsuitable unchanged because it provisions broker-side TLS/certificate handling; adaptation remains before running it for this topology.
- No live broker reset, proxy/firewall/DNS change, template runtime verification or completed security hardening claimed. Documentation diff checked; no commit requested or made.

Next useful step: Mike supplies private upstream/source addresses and validates Nginx configuration; adapt the archived fresh-broker setup for the chosen private 1883 listener, then test external TLS/auth/topic access and reconnects.

## 2026-10-13 — Nginx TCP proxy proposal documented

- Owner asked about fronting the VM with Nginx. Verified primary Nginx TCP stream/HTTP routing and Cloudflare proxy-port documentation. Prepared [configuration proposal](../docs/research/mqtt-nginx-proxy.md): separate Nginx edge forwards TLS 8883 and HTTP-01 challenges to the broker VM, keeping certificates/auth/ACLs at Mosquitto.
- Asked whether proxy is on a separate host or the broker VM. Same-VM option requires different backend listener and Certbot validation configuration; no topology/installation assumed. No Nginx, router, DNS or broker change made. Existing fresh reset remains prepared, not executed.

Next useful step: confirm proxy location/management interface and private upstream address, then adapt and validate configuration with Mike's existing routing. Examples are templates and not syntax-tested on an actual proxy. Documentation diff check passed; no commit requested or made.

## 2026-10-13 — Fresh MQTT reset prepared

- Owner authorized archiving all old MQTT state and setting up the host fresh for the new pilot. Prepared/uploaded a root installer that stops/flushed broker, moves old configuration/accounts/cert copies/persistence/logs to a root-private timestamped archive and creates an empty TLS-only broker with separate V3 uplink credentials and read-only worker credential. Initial root `snorr/pilot`; commands denied until designated gateway integration. Secrets/raw data remain on server.
- Installer creates private credentials, guards against accidental repeat reset, restores old trees on reset/startup/test failure, and installs a certificate copy/reload deploy hook scoped to the current hostname. Known expired cert still blocks external validating TLS; renewal pending port-80 routing.
- Python syntax checks and isolated installed-Mosquitto tests passed for valid/invalid/anonymous credentials, gateway publish/no-delivery, worker read/no-publish and command/unrelated-topic denial. Adjusted test to verify actual delivery because SUBACK may precede ACL filtering. Full root reset/rollback/hook not exercised; live old broker unchanged. [Details](../docs/research/mqtt-server-maintenance.md#2026-10-13--fresh-pilot-reset-authorized-and-prepared).

Next useful step: owner runs uploaded reset via local sudo and shares status without credentials; verify archive/fresh service, then renew TLS and configure actual gateways/worker. Firewall/SSH hardening remains pending. Documentation diff checked; no commit requested or made.

## 2026-10-13 — Privileged broker security audit received

- Owner output confirms inactive UFW and effective SSH password authentication enabled, correcting earlier inference from the readable main config. Root login is disabled and public-key login enabled. Eleven MQTT accounts exist; secrets/hashes not read.
- AppArmor loaded/enforcing selected profiles but no Mosquitto profile listed; no broker confinement claimed. Existing generic profiles do not establish installed apps.
- Prepared firewall rules preserving local SSH 22, MQTT TLS 8883 and HTTP-01 80; dormant rules need inspection. Asked whether Mike uses SSH keys before disabling passwords. No firewall/SSH/account changes performed, and update-policy dry-run remains pending.

Next useful step: inspect/activate UFW rules and verify a fresh SSH connection; confirm Mike's key access, then fix effective SSH password policy and design topic ACLs. Documentation diff checked; no commit requested or made.

## 2026-10-13 — Security checks while port-80 routing is pending

- Rechecked active SSH/Mosquitto, enabled maintenance timer and effective apt policy. Confirmed security/stable updates plus timer-controlled reboots. Running broker uses the mosquitto account; private-key/password-file modes are restrictive. UFW enabled state and installed AppArmor tool do not establish effective rules/profiles. Broker data-directory mode is 0755; local-user visibility needs file-permission review without reading tracks.
- Credential-free diagnostic TLS negotiated 1.3 and anonymous MQTT CONNECT was rejected with code 5. Expired certificate verification bypass was confined to this probe; no credentials, topic operations or payloads accessed. This is not validating TLS or ACL verification.
- Prepared next local-sudo audit commands for firewall, effective SSH, account names, AppArmor and update-policy dry-run. No server changes. [Evidence](../docs/research/mqtt-server-maintenance.md#2026-10-13--checks-while-http-01-routing-is-pending).

Next useful step: owner supplies privileged audit output, then define/install tested per-client topic restrictions while awaiting certificate repair. Documentation diff checked; no commit requested or made.

## 2026-10-13 — Enabled broker maintenance documented

- Owner supplied successful automation installer/timer output. Recorded enabled daily security/stable updates at 03:00 Pacific (up to ten minutes jitter) and required-only reboots at 04:00 Pacific with timezone/DST handling, busy-apt skip and no missed-window reboot catch-up in the server hosting and maintenance records. Logged-in users do not block scheduled reboots. No major release upgrades enabled.
- Recorded the server-local root-only configuration archive path without copying its sensitive contents. First shown next upgrade/reboot-check dates agree with the intended Pacific window. Updated project summary.
- Activation confirmed from owner output; no future automated run/reboot/reconnection or full backup restore observed. Certificate repair, MQTT topic permissions, firewall audit, unattended-upgrade dry-run and failure response remain outstanding. Documentation diff check passed; no commit requested or made.

Next useful step: complete the privileged update-policy dry-run and certificate renewal after Mike's port-80 routing change; then finish topic/firewall checks and observe the first maintenance run.

## 2026-10-13 — Broker updated/rebooted; scheduled maintenance prepared

- Owner supplied completed OS update output and rebooted the server. Reconnected and confirmed kernel 6.8.0-146, active SSH/Mosquitto and no remaining reboot-required flag. fwupd failed during update-time restart; after boot its unit reports inactive/success, but the prior failure cause is unverified.
- Owner requested automatic updates and scheduled reboots, reporting no active maintainer. Existing automation covers security updates. Prepared/uploaded a sudo installer adding same-release Ubuntu updates, a Pacific-time upgrade window and required-only reboot timer. Proposed 03:00 updates/04:00 reboot pending owner preference; timezone expression verified and shell syntax checks passed. [Details](../docs/research/mqtt-server-maintenance.md#2026-10-13--updatesreboot-completed-automation-prepared).
- Installer is not yet run as root or enabled. TLS certificate renewal, topic ACLs and privileged firewall/effective SSH audit remain outstanding. No claim of completed security hardening or verified future automatic reboot.

Next useful step: owner enables the maintenance schedule via local sudo and shares timer/dry-run output, then continue certificate and access-control repairs. No commit requested or made.

## 2026-10-13 — Broker update/security work started

- Owner authorized server updates and security work. Read-only checks found pending Ubuntu packages and an existing reboot-required flag. Readable SSH settings disable root/password/keyboard-interactive login; apt security automation is enabled. Effective SSH/firewall/topic-account checks remain privileged.
- Sudo still requires an interactive password. Prepared, syntax-checked and uploaded an OS update script to the owner's server home directory, with root-only configuration backup, no-removal package upgrade, health checks and no automatic reboot. [Maintenance record](../docs/research/mqtt-server-maintenance.md). Script has not been run as root; no packages updated or security settings changed.
- Requested privileged audit output without secrets; certificate repair, topic ACLs, firewall review, post-update validation and coordinated reboot remain. No non-research decision resolved or commit requested.

Next useful step: owner runs the uploaded script with sudo and supplies audit results; continue TLS/ACL changes from verified settings. Shell syntax check and upload passed; runtime untested until privileged execution.

## 2026-10-13 — Broker host and domain plans recorded

- Owner confirms Mike Rollins hosts the old-pilot broker, and the owner owns its current `mqtt.spp.lol` domain. Documented the hosted service in sites/inventory and the current project brief; physical host resources, costs, backup and maintenance details remain unknown.
- Mike plans to open/route port 80 shortly; completion and renewal success remain unverified. Recorded `mqtt.snorr.vegas` and `mqtt.snorr.org` as possible future hostnames, not selected or configured.
- Verified official Certbot/Let's Encrypt guidance: a new hostname needs certificate coverage and domain validation; a transition certificate can cover old plus chosen new hostname. Recorded DNS, HTTP-01 routing, certificate deployment/reload and client-address cutover prerequisites in the transport report. No DNS, certificate, server or radio changes, outreach, expense or non-research decision resolution.

Next useful step: once Mike's routing change is ready, verify renewal dry-run and repair broker certificate deployment/reload; choose a replacement hostname separately if desired. Documentation diff checked; no commit requested or made.

## 2026-10-13 — Old pilot MQTT server investigated

- Owner provided `mqtt.spp.lol` and authorized SSH inspection. Connected and performed read-only service/configuration/renewal-status checks plus external TCP/TLS probes; no credentials, password hashes, keys, member data or broker payloads read.
- Found enabled/active Mosquitto 2.0.18 with password-required TLS on 8883. External 8883 reachable; 1883 refused and has no local listener. Public certificate expired 2026-03-24; validating TLS rejected it. Latest Certbot run failed, standalone renewal configured, no renewal-hook files found; privileged logs unavailable and cause remains unknown. No topic ACL directive found in inspected configuration.
- Recorded [findings and reuse recommendation](../docs/research/dispatch-portal-transport.md#2026-10-13--existing-pilot-broker-inspected) and existing endpoint in site records. No server changes, service restart, broker publish/subscribe, hardware test, spending or hosting decision made.

Next useful step: inspect privileged certificate-renewal failure evidence and repair/verify renewal plus broker certificate installation/reload; then verify topic access and stock V3 integration. Noninteractive sudo was unavailable. Documentation diff checked; no commit requested or made.

## 2026-10-13 — MQTT broker discussion reopened

- Owner asked to revisit the broker issue. Claimed [Check Heltec MQTT over WebSockets for Tunnel hosting](../.scratch/pilot/issues/09-heltec-websocket-research.md) and lifted the connectivity-research deferral in current project/map notes; separate wishlist features remain parked.
- Rechecked official Cloudflare, Meshtastic source/configuration and Mosquitto documentation. Stock direct MQTT transport and published Tunnel TCP still need an adapter between them. Recorded home site VPN/bridge, separate reachable private broker and custom WSS candidates in the [transport report](../docs/research/dispatch-portal-transport.md#2026-10-13--broker-issue-revisited). Recommended Mosquitto for evaluation without recording owner acceptance.
- Hosting preference remains open: all-home requirement versus acceptable external private broker. Existing no-inbound-home-port-forwarding preference and one designated V3 downlink remain intact. No broker/VM deployed, firmware changed, external service purchased, real packets tested or non-research decision resolved.

Next useful step: settle hosting preference; for a home broker, inventory available site routers/computers before choosing an adapter. Then prepare a LAN broker test on identified/pinned gateway firmware and implement the real worker adapter. Documentation/source review only; no commit requested or made.

## 2026-10-13 — PocketBase installer running-file fix

- Owner reported `Errno 26: Text file busy` from installing over the running PocketBase executable. Replaced in-place truncating writes with same-directory staging and atomic replacement. Matching binaries stay untouched; a private verification receipt allows subsequent matching installs without another download. Older installs receive one archive/binary comparison without rewriting the executable.
- Locked replacements now preserve the existing binary, clean staged files and report how to stop/retry/restart the backend. Updated native setup instructions. No database/credential replacement or service restart is required for a matching reinstall.
- Verification: all twenty backend/installer tests passed, including a real running PocketBase reinstall, offline reuse, legacy installs without receipts, checksum rejection, tampered-binary replacement and locked-file preservation. Frontend is unchanged; Windows runtime/locking behavior remains untested (the error branch is exercised with a simulated lock).

Next useful step: repeat `python3 backend/manage.py install`, then continue backend sign-in/review. Keep existing local data and credentials; initialization remains a one-time command.

## 2026-10-13 — Local authenticated backend and connected portal built

- Owner approved backend development after reviewing the portal. Implemented PocketBase 0.40.5 migrations/hooks, the normalized [backend contract](../docs/research/portal-backend-contract.md), and a standard-library Python simulation/replay worker. Pinned official release checksums and Python 3.14.3; added native install/initialization/startup/account commands and GitHub-hosted backend CI. No VM, broker or hosted service provisioned.
- Added username/password admin/member accounts, a separate restricted worker account, locked direct collection writes and server-enforced permissions. Admin account creation/password reset/deactivation preserve earlier records. Transactional assignment/release/transfer and partial unique indexes protect one active member per tracker and one active tracker per member; dated attribution and separate latest-only simulated name jobs remain intact.
- Portal contact detail also remains visible for a device that has reported messages without a GPS fix; no location pin is invented.
- Persisted original GPS/sample timestamps and quality, first receipt time, separate contact time, every normalized receipt (including duplicates/rejections), position/history records, infrastructure observations, shared messages/send attempts and audited warnings/incidents. Older/unknown/future GPS data does not replace a newer known measurement. Simulated sends require a healthy feed and exactly one designated gateway; no radio receipt, publish or rename is claimed.
- Implemented supported-capability warning evaluation with device/per-report cadence, three-interval defaults/timeout overrides, shared battery defaults/device overrides, separate fresh recovery thresholds, acknowledgment, disabled-rule history, feed-loss suppression/reconnect grace and admin-resolved latched intrusion. Demo feed loss pauses synthetic observation production and retains prior readings/warnings.
- Connected all four portal pages to authenticated persisted snapshots/mutations, retaining standalone demo mode. Browser tokens remain in memory; reload requires login, while records persist. API failure retains the last snapshot and disables sending. Fixed pending sends so successful completion does not clear newly edited drafts, and converted PocketBase query slices to ordinary arrays before reversing histories to prevent repeated/misordered entries. History queries and point controls are bounded; storage retains all received pilot data.
- Verification: fourteen integration tests passed against the actual pinned binary in temporary databases, including authorization/bypass, accounts, concurrent claims, duplicate/delayed/invalid/future ingestion, ordered unique histories, outage/manual-send evidence, rules/incident lifecycle, stale name jobs and restart persistence. Fresh setup command passed in a disposable directory. Frontend tests (eight domain tests also run in single-process mode), strict types and production build passed. Connected browser checks cover login, saved assignments after reload, messages/drafts, rules/incidents, member permissions, mobile layout and API outage; the same connected flow passed against the production preview, including a deliberately delayed-send regression check and visual review. Private data/credentials/binaries remain ignored; Vite's existing map bundle-size warning remains.

Next useful step: owner tries backend sign-in on the Dell using the private generated credentials and reviews saved workflows. Then prepare backup/restore and deployment/supervision, or integrate sanitized packets from identified/pinned hardware builds when available. Live MQTT/firmware adapters, actual radio send/name execution, field/GPU performance, backup/restore and VM/HTTPS remain unverified. MQTT transport research and wishlist features stay deferred. No hardware/inventory, expense, site permission or field measurement changed.

## 2026-10-13 — Four-page synthetic portal and map built

- Owner requested continuing portal development with the remaining pages and map. Replaced the starter with responsive Map, Users, Messages and Infrastructure pages, using six fictional trackers, five fictional members and four illustrative infrastructure devices. No actual sites, member records, hardware changes or live packets are represented.
- Added MapLibre/USGS topo and aerial layers, selectable/searchable tracker list, measurement/receipt/contact times, aging and stale/unknown/never-seen states, optional infrastructure layer and opt-in recorded history. History shows measurement-time carriers, inspected points and dashed estimated connections broken across gaps over 15 minutes. Reduced motion and map/WebGL failure keep the tracking list usable. Rechecked official map/bundler guidance and explicitly bundled the MapLibre worker for Vite production builds.
- Added browser-memory assignment claim/release/admin transfer with dated history and stable short names, separate simulated long-name jobs and latest-job outcome controls. Shared messages include manual simulated sending, author prefixes, unread notifications and drafts preserved through page changes/outages without reconnect resend. Role previews are illustrative, not authentication.
- Added infrastructure role filtering, capability-specific readings, voltage history, declared hardware configuration, event/audit history, silent persistent badges and latched intrusion acknowledgment/admin resolution with a note. Battery rule configuration is a preview; automatic warning/recovery/missing-report/reconnect evaluation awaits ingestion. Demo sensor/voltage/configuration values do not establish hardware fitment or approved thresholds.
- Verification: npm checks, strict TypeScript and production build passed; all eight domain tests also passed with Node's single-process test mode. Browser checks passed against development and production at 1440px/390px, including topo/aerial tiles, layers/history, assignment/name jobs, outage draft/manual sending, notifications, incidents/rules and role previews. Additional checks passed for blocked tiles, unavailable WebGL, reduced motion, keyboard skip navigation, browser back and narrow layout overflow. Visually reviewed page captures. Map renderer size still produces Vite's default bundle-size warning (about 286 kB compressed plus a 508 kB uncompressed worker).

Next useful step: owner reviews the prototype on the Dell, then define the normalized persistence/ingestion contract and implement authenticated PocketBase operations with a Python simulation path. No backend, VM, live radio integration, offline-map readiness, field/GPU performance or automatic warning engine is verified. MQTT connectivity and wishlist features remain deferred.

## 2026-10-13 — Owner confirms Dell development works

- Owner confirms the frontend works and can be built on the Dell. This verifies the owner's development experience for the current starter; it does not establish full-stack, MapLibre or field-device performance.
- Reviewed the existing portal build plan. Next deliverable is the synthetic tracking screen: MapLibre/USGS map, six fictional trackers, searchable list and selectable device detail, with measurement age separate from last contact, stale/unknown/never-seen states and a simulated feed outage. Follow with opt-in history, then the remaining portal pages and backend integration.

Next useful step: implement and review the tracking screen on the Dell at desktop and narrow widths. Existing CI remains the automated check; no VM or live nodes are required. No new implementation or ticket decision in this status review.

## 2026-10-13 — Accepted portal stack and development/CI baseline

- Owner accepted React + TypeScript + Vite, PocketBase and Python worker, requesting simple TypeScript and explanations. Owner reports a desktop with WSL/Docker potentially available and no Proxmox VM yet; recorded development resources without assuming desktop access or readiness.
- Added the local frontend baseline, exact npm dependency lockfile, Node version, synthetic GPS freshness examples and developer instructions. Added GitHub-hosted CI for tests/type checking/build and seven-day main build artifacts; no deployment workflow or service credentials.
- Documented native Dell development now, optional desktop integration later and VM deployment after persistence/backup/rollback preparation. Checked official Vite, GitHub Actions, Microsoft WSL and PocketBase guidance. MQTT connectivity investigation stays deferred.
- Resolved [Establish the portal development and CI baseline](../.scratch/pilot/issues/13-portal-build-environment.md). Local lockfile install, four direct measurement-age tests, strict type checking, production build and whitespace checks passed. Dependencies/build output are ignored. No browser QA, desktop/Docker verification, backend or hosted portal; first remote CI execution awaits publication/verification.

Next useful step: build/review the four-page synthetic portal, starting with MapLibre map, tracker list and device detail. No VM needed for this step. Later pin backend/worker dependencies when their interfaces are implemented.

Publication/CI evidence: pushed baseline commit `cae58e5` to `origin/main`. The first [GitHub-hosted Portal CI job](https://github.com/lfg-seth/snorr-meshlink/actions/runs/38422409410) completed successfully, including lockfile installation, checks/build and artifact upload. No deployment occurred.

## 2026-10-13 — Portal work brought forward without nodes

- Owner has no nodes available for bench testing and requested moving forward with portal design and building. Reviewed the agreed portal, naming and infrastructure warning requirements; hardware testing is not a prerequisite for a synthetic prototype.
- Prepared the [portal build plan](../.scratch/pilot/portal-build-plan.md), including first-review screen behavior, build sequence, normalized data needs, meaningful verification and owner inputs needed now versus later.
- Asked whether to adopt the previously recommended React + TypeScript + Vite frontend with the planned PocketBase/Python backend. No stack acceptance inferred. MQTT connectivity investigation and wishlist features remain deferred.

Next useful step: confirm frontend direction and build the local responsive Map/Users/Messages/Infrastructure prototype with clearly labelled synthetic data. No app implementation, deployment, packet integration or hardware tests performed in this planning step.

## 2026-10-13 — Project status review

- Reviewed the project brief, session history, pilot map, tracker, inventory, wishlist and planned field criteria. Pilot approach and portal requirements are agreed; no bench/field results or deployed portal are recorded.
- Reconfirmed the planned six-V4 pilot includes only two on-hand V4s, with two purchases and two recoveries pending. Hardware identification, firmware/configuration pinning, passive GPS freshness, runtime and outage checks remain next.
- Recommended starting with the owned-hardware passive-tracking bench baseline; the next software step remains a synthetic-data four-page portal mockup. MQTT connectivity investigation and wishlist items stay deferred. No new decision, ticket claim, implementation or hardware test.

Next useful step: identify the two on-hand V4 revisions/GPS wiring, two undamaged RAK cores and two V3 variants, then prepare a repeatable stock-firmware bench configuration and test procedure.

## 2026-10-12 — Project setup

- Captured the owner's mission, priorities, existing-hardware preference, intended member devices, solar/18650 repeaters, backhaul possibilities, dashboard, content, and grant-reporting goals.
- Initialized local Git on `main` and established the project brief, agent instructions, glossary, local Wayfinder tracker, and record templates.
- Proposed the first planning checkpoint: a measurable field pilot using owned hardware. This checkpoint is provisional pending owner input.
- Requested rough hardware models/counts and pilot member count/acceptable position age.
- Owner supplied an initial scale of roughly 20 trackers, starting with as few as 5, and a tentative GPS target of 5–15 minutes. Recorded these without treating them as verified performance or final acceptance criteria.
- Completed a [primary-source protocol comparison](../docs/research/protocol-baseline.md) on `research/protocol-baseline` for incorporation into `main`; resolved the research ticket. Existing Meshtastic timing settings warrant evaluation before a fork; MeshCore passive GPS behavior requires build-specific verification. Firmware selection remains open.
- Verified local Markdown links, Git whitespace checks, and ignore rules for local secrets/operational data. The local issue tracker is tracked. No firmware or hardware tests performed.

Next: confirm a usable subset of owned radio boards, GPS hardware, and 18650 cells, then agree pilot requirements. No current equipment quantities, verified expenses, field outcomes, or installation permissions have been invented.

## 2026-10-12 — Purchase-list import

- Owner added `Mesh Purchase List - Purchase List.csv` and reports retaining most, but potentially not all, listed items.
- Preserved the source CSV unchanged and imported all 32 rows with stable hardware IDs and source row numbers. Listed quantities are distinct from unknown current counts.
- Used the bundled Python CSV reader and exact decimal arithmetic to check source structure and costs. All rows have 22 fields; all 32 item rows were accounted for.
- Reconciled listed extended costs to $1,989.79; $129.00 is explicitly outside the mesh project, leaving a $1,860.79 listed mesh subtotal. These are not booked cash transactions or current stock valuations.
- Prioritized confirming radio/core variants, GPS hardware, and cells. Kept inventory and firmware-choice tickets open pending that evidence.

## 2026-10-12 — High-value inventory reconciliation shortlist

- Owner requested a reconciliation pass focused on higher-dollar hardware, excluding the full kit and consumables.
- Selected the six mesh purchase-list lines above $100 in listed extended cost: fiberglass antennas, RAK WisBlock assemblies, Heltec V4 boards, whip antennas, the devices labelled “Tdfeck,” and Heltec V3 boards. Costs are historical source references, not current valuations.
- Current counts and condition remain unconfirmed; no stock quantities were changed. The $129 camera card is separately outside the mesh project.

Next: owner confirms remaining counts and known condition for those six groups, then exact radio/core models and fitted GPS for the board/device groups.

## 2026-10-12 — Owner-confirmed higher-value inventory

- Recorded 10 fiberglass antennas, 7 RAK units on hand, 9 Heltec V3, 2 Heltec V4 with GPS modules, 11 Muzi whip antennas, and 2 brand-new LILYGO T-Decks with GPS modules.
- Recorded 2 additional RAK units deployed remotely at Mount Charleston, with recovery deferred until replacement nodes are ready. Possible member-held Heltec V4s remain uncounted pending confirmation/reclamation.
- Preserved historical source quantities. RAK has 9 units accounted for against 10 listed; V3 has 5 more on hand than listed; whip antennas have 5 fewer on hand than listed. V4 has 2 on hand against 6 listed, with member-held stock uncertain. Differences do not establish losses or new expenses.
- GPS modules are owner-confirmed on 4 on-hand devices. Exact hardware variants, GPS on V3/RAK, most condition details, and working passive tracking remain unverified. No purchase or spending was recorded.

Next: identify RAK core modules/radio variants and whether V3 units have GPS, then bench-check a five-device pilot subset. Confirm member-held V4s before deciding any additional quantity to order.

## 2026-10-12 — First-pass inventory closed

- Owner confirms all 9 V3 units lack GPS, with 6 × 1100mAh batteries available for them; 2 × 3000mAh batteries are for V4 units. Both T-Decks have included batteries, capacity unconfirmed.
- Recorded proposed V3 silent internet/backhaul and possible repeater roles without treating them as verified capabilities or a firmware choice. Recorded the owner's concern about larger V4 batteries for later runtime evaluation.
- Owner directed planning from confirmed current stock only. The unresolved RAK may be a third mountain repeater or destroyed; it remains uncertain and excluded, alongside deployed RAKs and unconfirmed member-held V4s.
- Resolved “Inventory owned hardware for the pilot” with first-pass counts, explicit unknowns, and follow-up inspections. Updated the map; did not close other decisions or record purchases.

Next: agree pilot duration and position-age criteria, then identify exact builds and bench-check GPS reporting/runtime. Current stock includes four GPS-equipped devices; a five-member GPS pilot needs one more GPS-equipped device or a revised initial size. No runtime, firmware compatibility, or field tests performed.

## 2026-10-12 — Additional RAK and 18650 count

- Owner found 1 more RAK with a broken carrier board requiring replacement: now 8 on hand (1 damaged) plus 2 deployed, numerically reconciling the source-listed 10. Damaged unit excluded from ready-to-use stock; the other 7 remain untested.
- Recorded 88 × 18650 cells on hand. Owner estimates perhaps 4 cells per mountain repeater, about 8 across the 2 reported deployments; these are separate estimates and excluded from available stock. Cell identity, condition, and capacity remain unverified.
- Updated inventory, deployment notes, and the resolved inventory ticket without reopening it. No replacement purchase or expense recorded. Left the newly added storage-box 3MF file untouched.

Next: identify the damaged carrier board and compatible replacement, inspect cell labels/condition, and continue pilot build/runtime planning. No hardware tests performed.

## 2026-10-12 — Pilot requirements interview started

- Claimed “Define useful tracking for the first field pilot” at the owner's request.
- Read project context, tracker, and current inventory/session decisions; preserved existing uncommitted inventory work and the storage-box file.
- Started clarification of pilot size and maximum dispatch position age, distinguishing position measurement time from receipt time and broadcast frequency.

Outstanding: owner agreement on pilot size and position-age target, followed by duration and device-only workflow. Ticket remains claimed while awaiting input. No hardware tests or firmware decisions made.

## 2026-10-12 — Pilot hardware and reporting direction

- Owner plans 2 Heltec V4 purchases and 2 V4 recoveries, all with GPS and 3000mAh batteries. Recorded these separately from current stock and actual cash transactions; potential pool is 6 V4s plus the 2 existing T-Decks if included.
- Clarified that the tentative 5–15-minute range concerns stale position age. Recorded aggressive reporting followed by congestion-based tuning, with power-based modes and movement thresholds as options to evaluate.
- Kept exact stale cutoff, runtime, device-only workflow, and trial participant count open. No prices, orders, recoveries, performance results, or firmware capabilities assumed.

Next: agree stale cutoff and unplugged runtime, then minimum phone-free member workflow and final trial count. “Define useful tracking for the first field pilot” remains claimed awaiting owner input.

## 2026-10-12 — Tracking MVP requirements agreed

- Owner agreed a 15-minute stale-position threshold, clear stale indication and visible age at dispatch, a 4-hour minimum battery runtime with a 12-hour target, and automatic tracking after power-on for the MVP.
- Recorded larger batteries as an option subject to runtime evaluation; no capacity, cost, or purchase recorded.
- Created “Define a future device-only SOS workflow” at the owner's request and deferred it beyond passive tracking. No SOS implementation or gesture selected.
- Updated the project brief and planned field criteria. No field/bench results recorded. Whitespace checks passed.

Next: confirm whether the first trial uses 6 planned V4s alone or includes 2 T-Decks, then close the shared requirements summary and proceed to firmware/network selection. “Define useful tracking for the first field pilot” remains claimed for that final confirmation. No commit requested or made.

## 2026-10-12 — First-pilot requirements closed

- Owner confirmed V4-only scope to avoid T-Deck device/firmware complexity: 6 planned GPS-equipped V4s with 3000mAh batteries, comprising 2 on hand, 2 planned purchases, and 2 planned recoveries. Current stock counts are unchanged.
- Resolved “Define useful tracking for the first field pilot” with the agreed stale-display, battery-runtime, reporting direction, and power-on workflow requirements plus explicit remaining unknowns. Added its decision link to the map and updated the project, inventory, and planned field criteria.
- “Choose the pilot network and firmware approach” is now unblocked. SOS remains a future open ticket. No other non-research decision resolved in this session.
- Git whitespace checks passed; no hardware/firmware, runtime, or field validation performed. Changes remain uncommitted; no commit requested.

Next: choose a V4-compatible firmware/network approach and identify the exact hardware builds, then define bench checks and reporting settings against these requirements.

## 2026-10-12 — Pilot infrastructure clarified

- Owner clarified that the pilot includes RAK repeaters and 2 Heltec V3 receive-only internet backhauls alongside the 6 planned V4 member trackers. T-Decks remain excluded; V4-only was member-device scope, not total network scope.
- Updated the resolved requirements answer, approach-ticket comments, project brief, map, inventory allocation, planned field criteria, and site notes. Preserved the existing claimed approach ticket and its research; no additional decision resolved.
- RAK quantity/builds and locations remain open. V3 radio silence while forwarding to internet is a requirement to verify, not a demonstrated firmware capability. No stock counts, expenses, or deployment permissions changed.
- Git whitespace checks passed. No hardware, RF, internet forwarding, or field tests performed; changes remain uncommitted.

Next: select the pilot RAK count/builds and verify the chosen firmware supports V4 tracking, RAK relaying, and radio-silent V3 backhaul, then specify ingestion and bench checks.

## 2026-10-12 — Pilot approach interview started

- Claimed “Choose the pilot network and firmware approach” at the owner's request to continue to the next issue; inventory, requirements, and protocol research prerequisites are resolved.
- Read project context and tracker, preserved existing uncommitted work, and started current official-source verification of V4 support and passive GPS behavior for the firmware choice.
- Firmware selection, dispatch ingestion, and bench configuration remain open. No hardware tests, purchases, deployment, or commit performed.

Next: owner chooses a firmware to evaluate first, then agree the minimal dispatch data path and assumptions to verify on the bench. Ticket remains claimed while awaiting those decisions.

## 2026-10-12 — Meshtastic evaluation accepted; requirements refreshed

- Owner accepted Meshtastic as the first evaluation path and expects firmware modifications will likely be needed; stock sufficiency remains unproven.
- Reread the updated “Define useful tracking for the first field pilot”: 6 V4 member trackers plus owned RAK repeaters and 2 strictly receive-only V3 internet backhauls.
- Started checking V3 transmit-disable and uplink behavior against primary sources. The approach ticket remains claimed; no decision closed, hardware tested, or commit made.

Next: clarify anticipated modifications and local dispatch needs during internet outages, then choose a minimal ingestion path and RAK subset with explicit bench verification gates.

## 2026-10-12 — GPS fork review and offline viewing requirements

- Owner identified GPS behavior as the expected firmware-modification area and requested inspection of commits ahead in `lfg-seth/firmware`; started a primary-source commit/diff review.
- Owner confirmed local field command-post viewing and other-member location viewing in companion apps without internet backhaul. Updated the resolved requirements answer, project brief, map, approach discussion, and planned field criteria. Passive tracking remains phone-free.
- Source review supports evaluating V3 LoRa TX disable alongside MQTT uplink; exact build behavior and radio silence still require bench evidence. RAK cores remain unidentified.

Outstanding: finish the fork review, identify GPS changes worth evaluating against current upstream, and select local/remote ingestion arrangements plus a RAK subset. No firmware flashed, hardware tested, expenses changed, or commit made.

### Fork review completed

- Saved the [old firmware fork audit](../docs/research/old-firmware-fork.md), covering all 17 ahead commits (2 merges), net surviving changes, and a targeted comparison against pinned current upstream; fork is 1,887 behind.
- Found GPS timing preferences rather than a new GPS/position algorithm, a 30-minute periodic broadcast requiring revision for stationary freshness, and a source-level coordinate-shift defect in the full-precision MQTT map override. Do not transplant the old fork unchanged.
- Recorded offline app/map considerations and LoRa-silent gateway checks in the approach ticket. Public-history secret values were omitted from the report; do not reuse them for the private pilot.
- Git whitespace checks passed. No firmware builds, hardware/field tests, deployment, or commit performed.

Next: choose the command-post viewing device/connection and RAK subset, then define the current-release bench configuration and concrete GPS behavior gaps. “Choose the pilot network and firmware approach” remains claimed; no additional decision resolved.

## 2026-10-12 — Local viewer and RAK subset selected

- Owner selected both app and laptop/portal viewing, with the Meshtastic app acceptable for the first local-viewing MVP. Recorded 1 owned rugged Dell laptop/tablet running Linux as field equipment (HW-033); model/compatibility and runtime are unknown.
- Owner accepted 2 undamaged on-hand RAKs for initial relay evaluation, subject to core identification and operation checks; individual units remain unassigned. No radio stock counts changed.
- Prepared an approach summary in the claimed firmware/network ticket, including proposed private MQTT position-packet ingestion, local app viewing, and explicit bench prerequisites. Remote ingestion choice/final shared understanding remain pending; no decision resolved.
- Whitespace verification passed; no firmware builds, hardware tests, spending, installation, or commit performed.

Next: agree the approach summary/private MQTT path, then identify exact builds and prepare bench configuration and tests. Changes remain uncommitted; no commit requested.

## 2026-10-12 — Pilot network/firmware approach closed

- Owner accepted one private MQTT broker for both receive-only V3 uplinks and proposed compatible companion-app/cellular member uplinks only if multiple-backhaul behavior is acceptable.
- Completed [multiple-backhaul research](../docs/research/multiple-backhauls.md): documented phone proxy support, duplicate handling, downlink isolation, outage limits, and app/version caveats. No maximum gateway count or capacity result invented.
- Resolved “Choose the pilot network and firmware approach” with the agreed Meshtastic evaluation, hardware subset, local app-first/laptop viewing, private position-packet ingestion, and conditional staged member-phone backhauls. Added its decision link to the map and updated project/backhaul/test records. Only this non-research decision was resolved in this session.
- Exact builds, GPS settings, ingestion implementation, and hardware/field success remain open. Whitespace checks passed; no firmware build/flash, broker deployment, hardware tests, purchases, or commit performed.

Next useful step: identify the V4 revisions/GPS wiring, 2 RAK cores, and 2 V3 variants, then pin a current firmware release and prepare the bench configuration/test procedure. Keep SOS deferred until passive tracking is established. Changes remain uncommitted; no commit requested.

## 2026-10-12 — Future SOS requirements interview started

- Claimed “Define a future device-only SOS workflow” as the next open, unblocked tracker issue at the owner's request.
- Started a requirements-only interview with intended recipients and dispatch response ownership. SOS implementation remains deferred beyond passive tracking.
- Preserved existing uncommitted work. No decision resolved, firmware changed, hardware tested, or commit made.

Outstanding: agree recipients and response ownership, then activation, accidental-trigger handling, cancellation, acknowledgment, and outage behavior. Passive-tracking hardware identification and bench preparation remain the next implementation step.

## 2026-10-12 — Future SOS alerts and friendly areas

- Owner chose both dispatch and nearby-member SOS recipients, requested a Heltec OLED popup/flashing alert, and suggested an optional fitted buzzer. Recorded the hardware idea without assuming parts, compatibility, or spending.
- Recorded desired SOS content: member identity, friendly area name, and latitude/longitude. Owner proposes defining named Mount Charleston AO polygons in Google Earth; no boundaries supplied or inferred.
- Verified Google primary documentation for KML/KMZ export and named polygon geometry. Proposed an offline area lookup for discussion; device firmware/memory feasibility and boundary, overlap, unmatched, and stale/missing-GPS rules remain open.
- No SOS decision resolved, hardware/code changed, tests performed, or commit made. Whitespace verification passed.

Next: agree activation, then alert/cancellation/acknowledgment and response/outage behavior. “Define a future device-only SOS workflow” remains claimed; passive tracking remains the implementation priority.

## 2026-10-12 — Existing V4 button preferred for SOS

- Owner prefers a 5-second hold of the existing Heltec V4 button to activate SOS, replacing long-hold shutdown; no dedicated SOS button selected.
- Checked upstream user-button mapping and hold-event code. Shutdown conflicts warrant a firmware remap investigation; the owned board/button and installed-build behavior remain unverified.
- Proposed visible countdown, early-release abort, and one activation at the threshold for owner agreement. Cancellation and a replacement shutdown workflow remain open alongside acknowledgment/outage/area-lookup details.
- No decision resolved, code/firmware changed, hardware tested, or commit made. Whitespace verification passed.

Next: agree countdown/trigger behavior and how to cancel a sent SOS. Passive tracking remains the implementation priority; the SOS ticket remains claimed.

## 2026-10-12 — Active SOS interaction and GPS requirements

- Owner agreed the 5-second countdown/early-release activation and chose a separate subsequent 5-second hold to cancel/send cancellation. Recorded the need for release between holds and superseded the proposed menu cancellation.
- Recorded an obvious flashing/active SOS indication while incoming messages remain viewable, a new location attempt, a warning when no current fix is available, and last-known coordinates with their original age.
- Owner requested immediate new SOS transmissions when a location becomes available during SOS. Proposed grouping transmissions into one incident with ordered updates; every-fix versus recovery-only scope and no-new-fix repetitions remain for agreement.
- Proposed an explicit location-unavailable SOS when no fix has ever existed. No coordinates, timing guarantees, firmware support, or measured results assumed.
- No decision resolved, firmware/hardware changed, tests performed, or commit made. Whitespace verification passed.

Next: clarify SOS location-update scope and repetition, then acknowledgment/response, cancellation/outages, and remaining area/display rules. The SOS ticket remains claimed; implementation remains after passive tracking.

## 2026-10-12 — SOS text and position traffic separated

- Owner assumes a specially formatted Meshtastic text SOS and rejected an SOS message for every new GPS fix. Recorded faster ordinary position broadcasts during active SOS; exact rate and first-recovered-fix text behavior remain open.
- Recorded the need for retransmission without flooding even when recipients cannot acknowledge. OLED-only rescue followed by cancellation on the originating device is an intended workflow.
- Checked official Meshtastic acknowledgment/retransmission documentation and distinguished transport evidence from human response. Proposed spaced, bounded reminders that slow down independently of human acknowledgment, with optional human acknowledgment stopping text reminders but not active tracking; not yet agreed.
- No final retry policy, packet format, code change, hardware result, or decision resolution established. Whitespace verification passed; no commit made.

Next: agree reminder/acknowledgment behavior, then remaining receiver/cancellation/GPS/area rules. Passive tracking remains the implementation priority.

## 2026-10-12 — SOS acknowledgment deferred

- Owner removed human acknowledgment from the first SOS design and left cancellation to the originating member's separate 5-second hold.
- Superseded the proposal that human acknowledgment stops reminders. Active indication, faster ordinary tracking, and bounded text reminders continue until originating-device cancellation; numerical rates remain unselected.
- Preserved OLED-only response without acknowledgment. Underlying transport acknowledgment is not a condition for clearing SOS; recipient cancellation delivery is still unverified.
- No ticket resolved, firmware/hardware changed, tests performed, or commit made. Whitespace verification passed.

Next: agree behavior when no position has ever been acquired and after an unexpected reboot, then finish remaining requirements/prerequisites. “Define a future device-only SOS workflow” remains claimed; passive tracking remains the implementation priority.

## 2026-10-12 — SOS persistence and power-aware cadence

- Owner agreed SOS sends without any known position and active SOS survives an unexpected reboot until originating-member cancellation.
- Added requested battery status on the SOS screen and power-source-aware effort: maximum configured effort on external power even with low battery, taper on low battery only when battery-powered. Exact thresholds/rates remain open.
- Saved a primary-source [V4 power-detection check](../docs/research/v4-power-detection.md). Battery sensing is supported; reliable external-power detection for a low-battery V4 on a charger/power bank remains unverified and needs exact-board/build investigation plus bench tests.
- No ticket resolved, hardware/firmware changed, spending recorded, or hardware tests performed. Whitespace verification passed; no commit made.

Next: establish external-power detection and unknown-source behavior, then summarize the SOS requirements and remaining implementation prerequisites. Passive tracking remains the implementation priority.

## 2026-10-12 — Power detection pinned for follow-up

- Owner deferred the power-source investigation and proposed sustained battery-level trend over a configurable window, perhaps 1 minute, as an inferred-charging heuristic.
- Recorded the idea in the SOS ticket and power-detection research note without selecting an algorithm or treating trend as proof of external power. Unknown/flat behavior and exact cadence policy remain open.
- No tests, firmware/hardware changes, spending, ticket resolution, or commit. Whitespace verification passed.

Next: resume the remaining SOS workflow requirements and shared summary; keep power detection as a deferred implementation prerequisite. Passive tracking remains the implementation priority.

## 2026-10-12 — Future SOS workflow closed

- Owner accepted receiver short-press silencing with the incident retained, immediate local cancellation with bounded cancellation-delivery attempts through outages, and dispatch coordination when reachable with direct nearby-member response otherwise.
- Resolved “Define a future device-only SOS workflow” with a consolidated owner-agreed answer and linked it from the map. Recorded activation/cancellation, formatted text/ordinary position traffic, GPS age/unavailable fallback, OLED/battery status, reboot persistence, no human acknowledgment, and bounded reminders.
- Kept power detection/battery-trend evaluation pinned and message/rate/area/shutdown/firmware details as explicit implementation prerequisites. SOS implementation remains after passive tracking. Only this non-research decision resolved in this session.
- Whitespace verification passed. No firmware/hardware tests, purchases, deployment, or commit made; existing unrelated edits preserved.

Next useful step: identify the V4 revisions/GPS wiring, 2 undamaged RAK cores, and 2 V3 variants, then pin firmware and prepare the passive-tracking bench procedure. No open tickets remain in the current pilot tracker; create a focused bench-preparation follow-up when continuing implementation planning.

## 2026-10-12 — Charging display option captured

- Added the owner's configurable “keep display always on while charging” idea beside the battery-charge heuristic in the [power-detection note](../docs/research/v4-power-detection.md).
- No default, algorithm, or firmware change selected. The resolved SOS workflow remains closed; power detection stays deferred.
- Whitespace verification passed; no hardware tests or commit made.

Next useful step remains pilot hardware identification and passive-tracking bench preparation.

## 2026-10-12 — Dispatch portal interview started

- Owner redirected planning to a responsive Map/Users/Messages portal, MQTT-equipped V3s and possible V4s, an available Proxmox VM, Cloudflare Tunnel, simple locally managed accounts, and topo/aerial maps. Captured the proposal in the claimed [Define the dispatch portal MVP](../.scratch/pilot/issues/06-dispatch-portal.md) without choosing a stack or provisioning services.
- Recorded current-pin defaults, 15-minute stale display with measurement age, optional history showing measured points and uncertain connecting lines, all-incoming-data storage, shared-channel messages, and the proposed single dispatch transmit gateway. The prior receive-only approach remains recorded; the gateway change awaits agreement.
- Completed and resolved two primary-source research investigations: [broker/portal transport and backend options](../docs/research/dispatch-portal-transport.md), and [map sources/nonprofit access](../docs/research/dispatch-portal-maps.md). Cloudflare portal HTTPS is distinct from stock-device MQTT reachability; PocketBase is a pilot candidate with production-critical caveats and still needs ingestion. MapLibre plus USGS topo/aerial is a shortlist; coverage/age/zoom and offline use need verification. Preserved existing unrelated edits and hardware records; no purchase, publication, hardware test, service deployment, or commit performed.
- Asked the first independent design round: internet-outage workflow, account permissions, dispatch transmit gateway, retention, and dated device/member assignments. No non-research decision resolved.
- Git whitespace verification passed. Research is source-based, with moving firmware documentation/code; no selected release or hardware/backend/browser behavior tested.

Next useful step: owner answers the first round, then refine the map/user/message behavior and broker access path against the research findings. Hardware identification and passive-tracking bench preparation remain outstanding.

### First portal round answered

- Owner selected local Meshtastic fallback for v1, full operational access for registered users, one designated V3 transmitting portal replies, and retention of all pilot data with review before wider rollout.
- Owner proposed numeric device labels and portal member assignment by dispatch/admin or signed-in self-claim. Added device-number/assignment terminology; conflict/transfer/time-history rules remain under discussion.
- Amended current project, inventory allocation, planned field checks, sites, and the earlier approach answer to make the one-V3 transmit exception explicit. This does not select a hardware unit or establish transmission/forwarding success.
- Sent the next design round: assignment collisions; freshness bands; history window and gaps; sending during gateway outages; admin versus operational permissions. The portal ticket remains claimed pending these answers and eventual shared-summary agreement.

Next useful step: finish the portal behavior interview, then choose the broker connection/backend path and map evaluation prerequisites. No services deployed, hardware tests, spending, or commit.

### Second portal round answered

- Owner agreed unassigned-only self-claim with dispatch/admin transfers, preserved dated history, measurement-age breathing bands (under 2, 2–5, 5–15 minutes; stale at 15), separate last contact/unknown GPS, and no invented positions.
- Owner selected 4-hour initial history, measured points with dashed estimated connections and breaks over 15-minute gaps; manual send after outages with an unsent draft; and admin-only account/archive management with full operational access for registered users.
- Third round covers member/device list and unassigned pins, alert scope, shared-gateway author attribution, broker reachability, and pilot backend/map evaluation. Portal ticket remains claimed; no non-research ticket resolved or implementation performed.

Next useful step: answer that round and review a consolidated portal specification with any explicitly deferred infrastructure questions.

## 2026-10-12 — Portal list, alerts, author and evaluation stack agreed

- Owner selected the member/unassigned-device list and default tracker map, one-to-one active assignments, in-portal message toast/unread badges with optional sound, and author-name prefixes for outbound radio text.
- Owner approved a PocketBase/MQTT-worker/MapLibre/USGS pilot evaluation. No backend deployed or operational performance established.
- Owner requested clarification of why a broker VM's Cloudflare Tunnel hostname cannot directly serve stock Heltec MQTT. Rechecked official Cloudflare protocol documentation and current Meshtastic MQTT source; raw MQTT TCP/TLS is distinct from the Tunnel's WebSocket-wrapped TCP path requiring a client-side adapter. Domain use remains possible with a separately reachable broker.
- Portal ticket stays claimed pending the broker clarification and consolidated requirements review. Existing edits preserved; no purchase, publication, deployment, hardware test, or commit.
- Explained the hostname/Tunnel distinction using `mqtt.spp.lol`; documented DNS-only direct MQTT TLS and a WebSocket firmware/bridge candidate. Asked a simpler network question about VM location and router port forwarding. No actual domain, port, or firmware change performed. Git whitespace verification passed.

Next useful step: explain the `mqtt.spp.lol` example, identify a feasible broker connection path or explicitly defer it, and confirm the portal requirements summary.

## 2026-10-12 — No inbound forwarding; portal summary drafted

- Owner confirms the Proxmox VM is local and wants no inbound router port forwarding. Recorded this in the project/site notes and portal ticket; excluded the direct home-broker port-forward proposal.
- Started [Check Heltec MQTT over WebSockets for Tunnel hosting](../.scratch/pilot/issues/09-heltec-websocket-research.md). Compare a home WebSocket firmware/bridge route with a separate reachable private broker using outbound home connections; no route/provider/cost or firmware modification selected.
- Drafted a consolidated requirements summary in [Define the dispatch portal MVP](../.scratch/pilot/issues/06-dispatch-portal.md) for owner review. Asked whether home broker hosting is preferred or a separate broker is acceptable. The portal ticket stays claimed; no non-research decision resolved.
- No deployment, publishing, purchase, hardware tests, or commit. Preserve existing unrelated edits and raw-data ignore policy.

Next useful step: review the narrow transport findings, establish the hosting preference, and confirm the consolidated portal requirements with explicit implementation prerequisites.

### Connectivity investigation deferred by owner

- Owner explicitly stopped further connectivity investigation for now and asked us to assume a local MQTT broker reachable through Cloudflare with stock clients. Recorded that as an unverified planning assumption, without revising primary-source evidence or asserting operational support.
- Interrupted the research agent and released the WebSocket ticket claim. Do not resume connectivity investigation until requested. Updated the project, sites, map notes, and draft requirements accordingly.
- Portal requirements are ready for consolidated owner review. No service deployment, firmware change, field test, spending, or commit; unrelated edits preserved.

Next useful step: confirm the portal summary, then evaluate its map/user/message interface. Networking remains parked for the owner's later investigation.

## 2026-10-12 — Infrastructure monitoring added; portal baseline resolved

- Owner added repeaters/backhaul visibility by role, recorded battery charge/discharge, solar measurements, weather where equipped and intrusion detection where equipped.
- Owner selected a fourth Infrastructure page with device cards/details, telemetry charts and event log, optional infrastructure map layer, and configurable low-battery/missing-telemetry warnings and intrusion alerts.
- Resolved [Define the dispatch portal MVP](../.scratch/pilot/issues/06-dispatch-portal.md) with the consolidated interview answers and accepted addition; linked the answer from the map. Only this non-research decision resolved in this session. MQTT connectivity stays deferred under the owner's explicit planning assumption.
- Added infrastructure terminology, project direction and planned verification. Meshtastic docs establish capability categories, not sensor fitment, measured charging/solar behavior or alert reliability on owned builds. No stock counts or purchases changed.
- Created [Define infrastructure warning and intrusion handling](../.scratch/pilot/issues/10-infrastructure-warning-rules.md) for exact thresholds, permissions, acknowledgment/clearing and repeat behavior. This is separate from UI baseline selection and remains unclaimed.

Next useful step: choose infrastructure warning/event behavior or evaluate a map/infrastructure interface mockup. No firmware/UI implementation, deployment, hardware/sensor tests, spending or commit; existing unrelated edits preserved.

## 2026-10-12 — Device identity and remote naming interview

- Owner asks whether device selection/assignment can trigger OTA long/short-name changes, and whether a persistent device-specific identifier avoids using short names as unique database IDs.
- Completed/resolved [Check persistent device identity and remote name updates](../.scratch/pilot/issues/11-device-identity-research.md) with a [primary-source report](../docs/research/device-identity-admin.md), and claimed [Choose assignment-driven radio names and identity](../.scratch/pilot/issues/12-assignment-radio-names.md) for the owner policy.
- Current schema/source exposes a local hardware `device_id` on ESP32-S3, distinct from the mesh node number and editable names; actual boards/releases need provisioning checks. Remote admin requires authorized keys and a command-capable gateway integration; do not equate it with MQTT text downlink.
- Proposed stable short name S004 and carrier long name Seth [004] on assignment, with portal assignment independent of pending/confirmed/failed OTA naming. Owner choice is pending; no naming policy added to the resolved portal baseline yet.
- MQTT/Cloudflare connectivity stays parked under the owner's assumption. No actual name/admin key changes, device provisioning, flashing, implementation, hardware tests or commit.
- Verified source-level caveat: MQTT JSON text cannot rename and decoded admin payloads are rejected; encrypted PKI transport has a conditional path, so do not claim all MQTT admin is impossible. Recommend a trusted local radio API agent for the supported SDK route; portal execution/read-back remains to test. Git whitespace verification passed.

Next useful step: finish the capability check and owner naming choice, then record the assignment-name behavior and admin integration prerequisite.

## 2026-10-12 — Static device short names agreed

- Owner confirmed tracker short names remain static to device numbers. Resolved [Choose assignment-driven radio names and identity](../.scratch/pilot/issues/12-assignment-radio-names.md), linked it from the map, and amended the portal baseline/project/glossary.
- Recorded the separation of stable device identity, dated assignments and radio-name updates. Short names do not serve as database identity; long-name carrier updates are separate jobs with pending/confirmed/failed state and read-back. Exact formatting/release wording and the admin execution path remain implementation details to settle/verify.
- Only this non-research decision resolved in this session. Existing edits preserved; no actual names/admin keys changed, devices provisioned, UI/firmware implemented, hardware tested or deployment performed. MQTT connectivity stays parked.

Next useful step: define infrastructure warning/event behavior or review a map/infrastructure interface mockup. No commit requested or made.

## 2026-10-12 — Future feature wishlist captured

- Recorded the owner's [deferred feature wishlist](wishlist.md): a known-Wi-Fi table with automatic connection and MQTT-backhaul attempts, and browser-based flashing of project firmware for a small preselected subset of member-owned devices.
- Linked the wishlist from the project brief and pilot map, outside the active ticket frontier. Both ideas remain parked until the owner explicitly brings them forward; no research, design, implementation, or testing started.
- Supported devices, connection behavior and provisioning details remain future questions. Existing MQTT connectivity deferral and passive-tracking priority are preserved. Existing unrelated edits remain intact; no commit requested or made.

Next useful step: continue current pilot/portal planning when requested. Revisit these wishlist items only at the owner's direction.

## 2026-10-12 — Wishlist convention made persistent

- Owner clarified that future requests to “wishlist” an idea or feature refer to the deferred list in `records/wishlist.md`.
- Added the standing routing instruction to `AGENTS.md`: capture the idea outside the active ticket frontier and wait for explicit owner direction before starting work on it.

Next useful step: apply this convention to future wishlist requests. No feature work or commit performed.

## 2026-10-12 — Slack integration wishlisted

- Added Slack integration to the [deferred wishlist](wishlist.md), noting the owner's report that SNORR uses Slack heavily and possible dedicated-channel or app/plugin forms.
- Left use cases and integration mechanism open. No research, active ticket, Slack connection, channel creation, or implementation started; no commit made.

Next useful step: continue current project work when requested; revisit Slack integration only when the owner explicitly brings it forward.

## 2026-10-12 — Wishlist relevance clarified

- Owner clarified that deferred ideas should still be mentioned when relevant to future conversations. Updated `AGENTS.md` and the wishlist introduction to retain that context while keeping work deferred until explicit owner direction.
- Mentioning a wishlist item does not activate it. No feature work or commit performed.

Next useful step: consult the wishlist during related discussions and surface useful connections without starting deferred work.

## 2026-10-12 — Infrastructure warning interview started

- Owner requested work on infrastructure warnings and intrusion handling. Claimed [Define infrastructure warning and intrusion handling](../.scratch/pilot/issues/10-infrastructure-warning-rules.md).
- Started the policy interview covering permissions, notification scope, intrusion clearing and threshold configuration. Existing portal baseline and connectivity deferral remain in force.

Next useful step: collect owner answers, settle dependent repeat/outage/recovery behavior, and confirm the consolidated rules. No implementation, hardware tests, deployment or commit performed.

### First infrastructure round answered

- Owner accepted admin-only rule configuration, acknowledgment by all registered users, audited actions, and admin resolution of latched intrusion incidents with a note.
- Accepted persistent portal badges/cards and toasts, explicitly with no sound. Accepted shared defaults/per-device overrides and emphasized uneven sensor fitment; sensor rules apply only where configured/supported.

Next useful step: settle repeats, recovery, feed outages and missing-report timing, then confirm the consolidated decision. Ticket remains claimed; no implementation or tests performed.

### Second infrastructure round answered

- Owner selected persistent infrastructure badges only and logging of all events, superseding infrastructure toasts; no sound or repeat notifications.
- Accepted automatic health-warning recovery on fresh evidence, separate battery recovery thresholds, feed-outage visibility and preservation of existing alerts, and configurable missing-report timeouts starting at three expected reporting intervals.
- Consolidated policy awaits owner confirmation, including explicit proposals for reconnect grace and intrusion-event grouping. Battery values and sensor/cadence verification remain implementation prerequisites.

Next useful step: confirm the summary and resolve the infrastructure policy ticket. No implementation, hardware tests, deployment or commit performed.

## 2026-10-12 — Infrastructure warning policy resolved

- Owner confirmed the consolidated [infrastructure warning and intrusion policy](../.scratch/pilot/issues/10-infrastructure-warning-rules.md), including reconnect grace and intrusion-event grouping. Resolved this one non-research decision and linked it from the map and portal baseline.
- Added owner-requested device battery configuration metadata: type/chemistry, cell count and nominal mAh capacity with explicit per-cell/pack scope and arrangement where applicable. Unknowns remain explicit; no installed battery types, stock counts, measured capacity or runtime inferred.
- Updated project direction and planned verification. Silent badges replace infrastructure toasts; shared-message notification policy remains separate. Exact battery thresholds, sensor fitment/units and reporting cadence require verification. MQTT connectivity remains deferred; wishlist items remain parked.

Next useful step: review a portal interface mockup or identify and bench-check the owned pilot builds for passive tracking. No implementation, hardware/sensor tests, deployment, spending or commit performed; existing unrelated edits preserved.

## 2026-10-12 — Solar and antenna configuration added

- Owner added solar-panel configuration to device setup, explicitly leaving options for later definition.
- Added antenna configuration including Muzi whip and fiberglass choices, with unknown/unconfigured values explicit. Recorded both additions in the portal baseline and project brief; no installed hardware assignments, inventory counts, purchases or performance claims changed.

Next useful step: review the portal interface or bench-check owned pilot hardware. Solar configuration options remain open. No implementation, tests, deployment or commit performed.

## 2026-10-12 — Next-step review

- Reviewed project decisions, session history and tracker state. Portal requirements, naming and infrastructure warning policy are resolved; the remaining open connectivity research is explicitly deferred.
- Recommended identifying the owned pilot hardware and preparing a small passive-tracking bench test as the next step toward the primary GPS mission. A portal interface mockup remains the next software planning option.

Next useful step: identify the 2 on-hand V4 revisions/GPS wiring, 2 undamaged RAK cores and 2 V3 variants, then prepare firmware/configuration and a bench procedure. No new ticket claimed, implementation, hardware test or commit performed; existing edits preserved.

## 2026-10-12 — Portal development handoff for the night

- Owner requested a brief portal-development next-step review, then stopping for the night. Reviewed the resolved portal baseline; no additional requirements interview or implementation started.
- Recommended a local four-page mockup with synthetic data, emphasizing the tracking map, position age, stale/unknown states and feed outages. Next define the records and worker interface for device identity, dated assignments, observations, packet receipts, messages and infrastructure events, then implement a simulated ingestion-to-map slice before live hardware integration.
- Real integration still needs sanitized packet samples/pinned firmware, verified telemetry capabilities and units, message limits/delivery evidence, and VM/backup setup. MQTT connectivity research remains explicitly parked; it need not block a simulated local prototype.

Next useful portal step: build a local Map/Users/Messages/Infrastructure mockup using synthetic data, then review it before wiring the backend. No new ticket, deployment, publishing, hardware test or commit; existing edits preserved. Session ended at the owner's request.

### Portal stack recommendation

- Owner favors Python for the MQTT worker and is most familiar with React. Recommended React + TypeScript + Vite for the browser portal, retaining PocketBase and MapLibre. React's current official documentation includes a Vite-based setup; frontend choice remains a recommendation pending owner acceptance.
- Python worker preference recorded; no worker library, dependency versions or broker software selected. No implementation or deployment started.

Next useful step: confirm the frontend direction when resuming, then build the local synthetic-data mockup. No commit made.

### Hosting comparison

- Compared current official Vercel Hobby/function limits and PocketBase deployment guidance. Recommended retaining the owned Proxmox VM for the pilot: static React build, persistent PocketBase data, Python MQTT worker and private broker together.
- Vercel is a possible frontend-only host, but that split retains the VM/backend dependency and adds hosting configuration. Hobby functions are duration-limited and do not fit the intended continuous MQTT worker; plan eligibility remains to check if Vercel is considered.
- Home power/internet availability, service restarts and backups remain deployment checks. No hosting decision changed, service deployed or connectivity research resumed; no commit made.

### Portal bandwidth and client performance

- Owner reports a 100Mbps home uplink. Expected pilot bandwidth is manageable if browsers fetch USGS basemap tiles directly and receive small incremental operational updates; this is an architectural estimate, not a measured load test.
- Verified official Cloudflare caching guidance, USGS cached basemap services and MapLibre performance guidance. Recommend caching public versioned frontend assets, leaving authenticated operational responses uncached, and keeping map tiles off the home-origin path.
- Client checks should cover slow cellular connections, tile-provider latency, GPU/WebGL support on the rugged Dell and mobile devices, marker animation, bounded history queries and reconnect behavior. Concurrent viewers, actual payload sizes, VM resources and observed latency remain unmeasured.
- No deployment/configuration change, hosting decision or connectivity investigation performed. Next prototype should measure cold/repeat loading and live updates on actual field devices; no commit made.

## 2026-10-12 — Pre-bench firmware readiness review

- Owner asked whether firmware changes are needed before bench testing. Reviewed the agreed pilot approach, old-fork audit, future SOS requirements and deferred power/wishlist work. Recommend a stock Meshtastic baseline with deliberate configuration; no mandatory source patch identified for the initial passive-tracking tests. Stock sufficiency remains unproven until hardware tests.
- Rechecked official [position configuration](https://meshtastic.org/docs/configuration/radio/position/): acquisition cadence, periodic broadcasts, movement thresholds, configurable GPS pins and GPS-solution timestamp flags exist. Proposed an initial diagnostic profile of 60-second acquisition, 120-second periodic broadcasts and smart broadcasting off to isolate stationary reporting; these are unapproved/unmeasured trial suggestions, not operational settings or a freshness guarantee. Verify saved settings after reboot and measure actual fresh-fix transmissions.
- Official [Heltec support](https://meshtastic.org/docs/hardware/devices/heltec-automation/lora32/) distinguishes original V4 from V4-R8 firmware targets. Identify owned revisions/GPS wiring and RAK cores before pinning a release and matching per-board images. Do not reuse the old fork's 30-minute member broadcast preference.
- Existing [LoRa transmit disable](https://meshtastic.org/docs/configuration/radio/lora/#transmit-enabled) and [MQTT configuration](https://meshtastic.org/docs/configuration/module/mqtt/) warrant configuration-first gateway tests. Preserve the later amendment: one V3 may transmit portal replies; the other remains receive-only. Test continued uplink and silence through reboot/reconnect on the pinned build. No broker-connectivity investigation resumed.
- Portal measurement-age/stale display, assignments, deduplication and warnings are application/integration work. The agreed custom SOS button/countdown, incident persistence/cancellation, reminders, OLED handling and area lookup need later firmware implementation/evaluation; deferred charging heuristics and wishlist items remain parked.

Next useful step: identify boards and GPS connections, pin supported stock images, save a bench configuration, then test phone-free boot, stationary/moving GPS freshness, reboot persistence, relay/backhaul behavior and battery runtime. No firmware changed/flashed, hardware tests, ticket status changes or commit performed; prior unrelated edits preserved.

## 2026-10-12 — Project naming suggestions

- Owner requested a short umbrella name connecting SNORR, mesh networking and communications, understandable at a county meeting and suitable for a GitHub repository.
- Recommended SNORR Link, with the descriptor "Search and Rescue Tracking & Communications" and suggested repository name `snorr-link`. Alternatives: SNORR MeshLink, SNORR Connect and SNORR RescueNet. These are suggestions awaiting owner selection; the existing project/repository name remains in place.

Next useful step: owner selects a name. No repository rename, availability check, publishing or commit performed; existing edits preserved.

## 2026-10-12 — SNORR MeshLink GitHub publication

- Owner created `lfg-seth/snorr-meshlink`, supplied its SSH URL, authorized pushing the project there and requested a push after every commit. Adopted SNORR MeshLink in the project overview and saved the publication/push policy in AGENTS.md.
- Confirmed the remote is empty and SSH access works using Windows OpenSSH. Prepared the accumulated inventory, pilot decisions, portal/SOS requirements, research, wishlist and session records for a coherent publication checkpoint. The local Markdown tracker is mirrored with the repository; no GitHub Issues migration requested.
- Refreshed the README's outdated pilot summary. Kept the unrelated untracked battery-box 3MF model outside the commit. No hardware tests, implementation or operational deployment performed.

Next useful step: identify pilot boards/GPS wiring and prepare passive-tracking bench tests, or resume the synthetic-data portal mockup. Push each completed commit to origin and report failures; keep private operational data outside Git.

### Broker renewal diagnosis follow-up

- Owner asked whether closed inbound 443 explains renewal failure. Official [Certbot standalone documentation](https://eff-certbot.readthedocs.io/en/stable/using.html#standalone) confirms the configured standalone HTTP-01 method requires public inbound TCP 80; inbound 443 is not required for that method. Outbound HTTPS to the ACME service is separately required. Closed 80 is a possible cause, not confirmed without logs.
- Requested root-visible Certbot journal and the latest Let's Encrypt log error block. Renewal cause remains pending; no firewall change or renewal attempted. After renewal, separately verify deployment of the renewed certificate into Mosquitto's configured certificate files and reload behavior.

### HTTP-01 failure located

- Owner supplied root-visible Certbot failure evidence. Active HTTP-01 challenge request received 404 on public port 80; outbound ACME HTTPS succeeded. Read-only follow-up HTTP probe returned an nginx 404. A routing/proxy/challenge-serving mismatch is suspected; the precise destination remains to inspect. Closed inbound 443 is not the cause of this configured HTTP-01 failure.
- Recorded sanitized evidence in the transport report. Next inspect public port-80 forwarding/nginx routing, correct the selected challenge path and run a renewal dry-run before production renewal and broker certificate deployment. No remote changes or commit performed.

### Heltec port explanation

- Owner asked whether Heltecs specify a port and what 1883/8883 do. Verified current Meshtastic source parses `hostname:port`, choosing default 8883 with TLS and 1883 otherwise. Documented gateway settings `mqtt.spp.lol:8883` with TLS enabled and private proxy-to-broker 1883 role. Actual firmware remains unpinned/unverified; member LoRa trackers do not all need MQTT.
- Captured source-level credential-logging/certificate-verification checks for later provisioning without reading or publishing actual credentials. No device/server changes or commit performed. Next step remains adapting the fresh broker for Mike's TLS-termination layout and verifying actual endpoints/builds.
