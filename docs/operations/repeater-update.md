# Repeater firmware and three-minute profile updater

Owner request, 2026-10-23: prepare R001–R006 to report available statistics
every three minutes, provide a reusable firmware/configuration updater, and
place R006 at its owner-provided map location. R006 remains **INA219 only, with
no temperature sensor**. Exact coordinates and private radio material stay in
ignored storage.

## Current rollout status

- LOCAL-3's saved-interval source work is recorded in
  [the software verification record](#saved-snns-interval-software-verification).
  The owner-selected [October 24 bench](#r006-and-gateway-admin-bench---2026-10-24)
  installs `4c96b9b` on R006 and both gateways. The production download pointer
  remains unset; earlier installed-image results below are historical.
- Firmware source **`0634b775f65804968f5a18a7e8824db415556db2`** is built for
  ordinary `rak4631`, including the INA219 fixes and the RAK-specific
  180-second passive-neighbor cadence. Source/build success is separate from
  release verification and installed hardware.
- Published release CI/download verification is pending. The updater's
  [production profile pointer](../../scripts/bench/repeater-profiles.json)
  deliberately has `releaseTag: null`; its default public-download mode stops
  until a verified published release is pinned there. The manifest must
  certify `snorrNeighborLoraIntervalSeconds: 180`.
- An explicit local-build fallback is staged at ignored
  `private/bench/releases/local-0634b77/`. Its
  [fixed tracked manifest](repeater-production-image.json) records the real
  source/image hashes with **`publishedArtifact: false`** and
  **`hardwareVerified: false`**. This bundle is available only when explicitly
  selected with `--local-bundle`; no public-release or CI provenance is
  inferred. The tag in that manifest is a planned release label. Its hardware
  flag records pre-bench build provenance; the later installed-board result
  is recorded separately below.
- **Previous R006 updater run:** the corrected native Windows UF2 path passes at
  **2026-10-24 00:51:19 UTC / October 23 17:51:19 Pacific**. Ordinary
  `rak4631 / 2.7.26.0634b77`, device/power **180 seconds**, environment off,
  private SNNS compiled at 180 seconds and standard NeighborInfo 21,600
  seconds pass complete intended profile/identity/key readback through
  explicit reboot. Serial is closed. The earlier serial-only DFU failure
  was recovered with the verified application-only OTA package before this
  successful corrected UF2 retry. Only R006 is connected; **R001–R005 remain
  unchanged and require physical connection**.
- R006's requested map change is pending; no portal map write has occurred
  because the current host cannot resolve the server. The supplied location
  is retained privately. Firmware installation does not establish a map change.
- Thirty-four offline updater checks pass, including identity matching,
  application-only UF2 validation, fitted-sensor settings, configuration/key
  preservation, immutable backups, exact local-bundle checks and explicit
  unpublished-build selection. Native Windows flashing and reboot/profile
  verification pass on R006; Linux hardware remains untested. Three automatic
  cycles of device, power and SNNS reports pass through both gateways, as
  measured below. Authenticated portal receipt remains unverified.

The owner authorizes this repeater rollout. Every other repeater still needs
its own physical connection and independent identity/backup checks. This tool
supports RAK4631 repeaters R001–R006; member trackers and Heltec gateways keep
their separate update procedures.

## R006 and gateway admin bench - 2026-10-24

The owner selects R006, G001 and G002 for flashing and B002 as the transmitting
admin controller. One worker owns all four serial/API connections under the
[bench assignment](../../.scratch/tasks/local-3-admin-bench.md). This run uses
reviewed source **`4c96b9ba0360f01752892a41d09ccacda82747bb`**, already published
on `snorr/develop`. These are explicitly selected local build images, not new
published release assets or a changed production download pointer.

### Application images and recovery

| Selected board | Installed target / version | Application image and SHA256 |
| --- | --- | --- |
| R006 `!da581e5f` | Ordinary `rak4631` / `2.7.26.4c96b9b` | UF2, 1,519,104 bytes; `f83039d32c8637beff30f1a8d06e8addd106ad817f611dbc440b9bac04c65206` |
| G001 `!9ea13cc0`, G002 `!849ad7a0` | Dedicated `heltec-v3-gateway` / `2.7.26.4c96b9b` | BIN, 2,110,992 bytes; `1fbe3acf8f91d8d9ae563cbeef8b412c17b58e830ebc79f96ee60767612e8cfe` |

The RAK image is the exact saved ordinary build from the reviewed software
assignment. UF2 application bounds and matching USB identity pass; API-driven
DFU/UF2 update preserves the bootloader and stored configuration. The retained
application-only Nordic OTA ZIP is 760,310 bytes, SHA256
`09ecab0ce889d5b7b5001644f61384882973f346e30e535d485fa0366f9c84e3`.

The gateway target is rebuilt successfully from the clean pinned source using
the project PlatformIO environment and temporary Windows package-cache drive
mapping: **357.361 seconds**, static RAM **132,096/327,680 bytes**, reported
flash **2,110,561/3,342,336 bytes**. These are build statistics, not peak memory
or runtime measurements. Each original 8,388,608-byte flash is privately backed
up. Original partition bytes match the build and OTA sequence 1 selects app0;
write only **0x10000**, within its **0x330000-byte** allocation. Independent
esptool verification passes for each application. Original full-flash SHA256:
G001 `3d91a591bb24f4d205c14448aa6dfb34482c97bf993f1d934693d3b7d64055ee`;
G002 `8b1c09a03aa6cf66e1d8739d724c6e2ad9e0f61b871990ad2235063428e14f1f`.

Fresh independent API snapshots verify the installed version and complete
per-board local/module/channel profile, owner identity and keys, including
after explicit reboot. Both V3s retain CLIENT, LoRa TX disabled, local-only
neighbor reporting and their individual Wi-Fi/MQTT credentials. G001 retains
disabled device telemetry and its saved 2,147,483,647-second value; G002 retains
enabled 300-second device telemetry. B002 remains stock `2.7.26.54e0d8d`.
R006 retains INA219-only, device/power 180 seconds and environment off.

### Controller and session handling

Use B002 **`!699ca878` / original HELTEC_V4** on its existing private channel
and key pair. Before temporary enrollment, an encrypted telemetry-config read
returns **`ADMIN_PUBLIC_KEY_UNAUTHORIZED`**: channel membership alone is
insufficient. Append only B002's existing public key to R006's originally empty
admin allowlist through the identified local serial recovery connection.
Independent full-profile comparison permits only this deliberate difference.
The authorized encrypted remote read then returns the actual 180-second setting.

The installed Meshtastic Python SDK is **2.7.11**. Two-second remote reboot
requests return **`ADMIN_BAD_SESSION_KEY`** in the initial helper, an SDK
`requestConfig`/`reboot` probe and a later dedicated-key attempt. The controller
requests **`SESSIONKEY_CONFIG` immediately before each mutation**, verifying
the encrypted target response and eight-byte key. This permits the measured
same-boot edits, but does not alone remove the reboot acknowledgment problem.
A **15-second remote reboot** returns a successful acknowledgment and recovers
the original saved value after an uncommitted edit.

The automatically rebooting 900-second save also returns the session-key error;
independent encrypted/local readback nevertheless finds 900, and a distinct
new SNNS boot identifies the restarted node. The save executed despite the
negative acknowledgment. A retry reaching the restarted node with an expired
key is consistent with this result; the exact transport cause remains
unproven. Do not blindly repeat a rebooting write after such an error: read the
result and verify boot/profile independently. Preserve the failed/ambiguous
attempts. No firmware fix, arbitrary app/CLI compatibility or unattended admin
readiness is claimed; physical serial recovery remains required.

Before recovery, identify R006 by node/hardware/USB identity, not an old COM
number. Stop the controller and gateway capture handles. The private rollback
helper restores R006's original telemetry and security sections in a local
settings transaction, commits/reboots, reconnects independently and compares
the entire original profile. Concealed complete rollback profiles for all
four boards and the observer credentials are stored in 1Password
**SNORR MeshLink — Pilot** as `SNORR_BENCH_20261024_*` variables. Raw profiles,
full flash images, API/console evidence and captures remain ignored under
`private/bench/local-3-admin-20261024/`; secret values and locations are omitted
from this record.

### Live cadence measurement method

The serial collector listens on B002 and both receive-only gateways; an
independent read-only MQTT subscriber uses hostname/certificate-validating TLS
and the real backend wire adapter. Capture only selected SNNS/device/power
observations, excluding location content. Match R006 observer/boot/sequence
and payload hashes across gateways; duplicate gateway copies are one source
report. Use SNNS source uptime for cooldown comparisons and monotonic host
receipt gaps separately. Unknown absolute source clocks stay unknown.

To keep passive observations dirty during the long intervals, B002 broadcasts
its existing NodeInfo at BACKGROUND priority every 45 seconds while the bench
controller runs. This is an intentional fixture/load, not a new configuration,
synthetic GPS track or production delivery-rate denominator. Reported channel
utilization and timing describe this close bench and its existing traffic.
Same-boot interval changes use an open settings transaction; saved-interval
tests commit and independently reconnect after reboot. Every readback checks
the complete original local/module/channel profile, allowing only the test
device interval and temporary B002 admin authorization.

The same-boot source sequence is consecutive, with identical payload copies
through both gateways:

| Transition / condition | Required minimum | Measured source-uptime gap |
| --- | --- | --- |
| Saved 180 seconds after remote reboot | 180 s | 195 s |
| Lengthen to 300 in the open edit transaction | 300 s | 315 s |
| Shorten to 180 while the 300-second cooldown is outstanding | 300 s | 315 s |
| Following cycle uses the new 180-second value | 180 s | 195 s |
| Saved 900 seconds, distinct reboot and next same-boot report | 900 s | 915 s |
| Restore saved 180, distinct reboot and two periodic cycles | 180 s | 195 / 195 s |

The first report after the initial remote reboot is sequence 1 at source
uptime **80 seconds**. A temporary uncommitted 300-second edit is then
interrupted by the 15-second remote reboot: encrypted readback returns the
saved **180**, full intended profile comparison passes, and a distinct new
boot starts at sequence 1 / uptime **67 seconds**. This tests interruption of
an open edit, not RF-path or backhaul outage recovery. The subsequent saved
900-second write passes complete readback and starts another distinct boot at
sequence 1 / uptime **77 seconds**; its next source report is sequence 2 at
uptime **992 seconds**, a **915-second** gap. Startup remains separate from
the long periodic baseline. A complete 900-second device-telemetry gap is not
claimed from this SNNS observation.

### Final receipts, restoration and limits

All seven measured periodic gaps have consecutive source sequences, identical
payload hashes on G001/G002 and corresponding MQTT copies through both. The
gateway serial receipt gaps, in table order, are **195.410/195.427,
315.196/315.169, 314.830/314.840, 195.039/195.040, 915.590/915.591,
195.772/195.773 and 194.486/194.486 seconds** (G001/G002). Source uptime is
quantized separately from host receipt clocks; an individual receipt gap is
not the scheduler baseline or an upstream hearing-age bound.

The main SNNS MQTT capture contains **13 distinct R006 reports through each
gateway**, plus **39 own-observer reports from each gateway**. Each gateway
spans two observed boot identities, around serial reconnection: all **37
consecutive within-boot pairs** are **75 seconds (32 pairs)** or **76 seconds
(five pairs)**, with no skipped captured sequence within those boots. G001's
disabled/extreme device interval and G002's enabled 300-second interval do not
replace their separate local SNNS cadence. Fresh R006 DeviceMetrics source
uptimes **186 → 486 → 666 → 846 → 1026** also show the 300-second then
180-second device gaps during the same-boot edits. These captures are not a
transmit-attempt denominator, sustained uptime or delivery percentage.

At **2026-10-24T15:48:14Z**, final local transaction/reboot verification restores
R006's complete original owner/security/channel/local/module profile,
including device/power **180 seconds**, environment off and its **empty admin
allowlist**. A separate final pass independently compares all four original
profiles and expected installed versions; both V3s remain TX-disabled/local-only
and B002 is unchanged. A final encrypted B002 admin request is rejected again
as **`ADMIN_PUBLIC_KEY_UNAUTHORIZED`**. All serial/subscriber sessions close;
the temporary package-cache drive mapping is removed. Nine concealed
1Password variables preserve four original profiles, four final profiles and
the observer configuration. No new keys or shared profiles are substituted.

Private `summarize.py --final` writes `sanitized-summary.json` and requires all seven gaps,
both serial/MQTT paths, interrupted-edit recovery, final board comparisons and
the successful restored follow-up run. The first two runtime attempts stop on
the reboot/session error and independently restore the original profile; both
failed verdicts remain alongside the successful focused remainder. Existing
project-environment checks pass again: **34 updater tests and 10 release
tests**. The reviewed source is unchanged; actual-module extreme/rollover/gate
coverage remains the earlier software evidence, not a physical 49-day test.

Fixed capture references under `private/bench/local-3-admin-20261024/`:

| Evidence | Bytes | SHA256 |
| --- | --- | --- |
| `runtime-events.jsonl` | 120,115 | `ccd212bcc51d5c173b42eddcd6ccd5fd7dc0831646adce38e417a1a8b833602d` |
| `mqtt-events.jsonl` | 109,131 | `c4ffac63f422e54f86e3c2944b8a54f373dd2b0dc84e473dd6c6b26e81c48f40` |

The next required bench test is **remote administration through a forced relay
path**, using an identified transmitting intermediate and proof excluding direct
reception. B002/R006 are the two controlled transmitters here; receive-only
V3s are not repurposed. Include interrupted/lost commands and robust
read-after-error handling before accepting an operator tool or inaccessible
deployment. This run does not pass authenticated portal receipt/map metadata,
backhaul-outage freshness, gateway TLS/reconnect acceptance, independent RF
silence, INA219 calibration, battery-only soak, release publication or field
coverage. Continue the independent software freshness/release work while those
bench/access gates remain open.

## Saved SNNS interval software verification

LOCAL-3 section 1 implements the saved-interval contract in the firmware fork.
The implementation input is pinned source `b23f09d5b`, not R006's installed
runtime string. Reviewed source
[`4c96b9ba0360f01752892a41d09ccacda82747bb`](https://github.com/lfg-seth/firmware/commit/4c96b9ba0360f01752892a41d09ccacda82747bb)
is published by fast-forward on `origin/snorr/develop` and pinned through this
repository's `firmware` submodule. This is software evidence, separate from
all installed-board results in this record.

- The actual-module regression fails against the old implementation and passes
  after the change. `python3 test/test_snorr_neighbor_signals/run.py` compiles
  the real module and `src/mesh/Throttle.cpp` with GCC, AddressSanitizer and
  UndefinedBehaviorSanitizer. Both 180/300-second fallback builds pass the
  unset, 1/179/180/300/900/3601/86400-second settings, saturation boundary,
  overflowing-millisecond input and uint32 maximum cases. The harness also
  covers shorter/longer settings, retained jitter, no catch-up, reboot
  reconstruction, rollover including a report at zero, local/radio transitions,
  TX-disabled local operation, report fields, empty/expired observations and
  airtime/channel/role gates. Collector capacities 32/10 pass the existing wire,
  rotation, eviction, zero-SNR and expiry checks.
- Existing actual-source INA219 checks pass at multipliers 1 and 10 using
  cached RAK dependencies and emulated I2C. The project environment
  `.venv/Scripts/python.exe scripts/check-project.py bench firmware-release`
  passes **34 updater tests and 10 release tests**. These checks preserve
  sensor/profile/release behavior; they do not verify actual admin access.
- The module harness observes constructor startup delay and returned scheduler
  delays with a fake scheduler boundary. Reboot reconstruction retains the
  saved configuration fixture and resets module state. Actual scheduler
  execution, flash persistence, remote admin authorization/session handling,
  RF/MQTT/portal delivery and measured airtime remain bench/live gates.
- Full Trunk is unavailable on this Windows host. The changed C++ files pass
  the repository's configured clang-format **16.0.3**; workflow YAML and Python
  syntax parse, and Git whitespace checks pass.
- One independent read-only reviewer checks the fixed diff
  `b23f09d5b..4c96b9ba0` against every section-1 criterion and reports **no
  actionable findings**. The reviewer independently reruns the sanitized module
  and collector matrix successfully, checks actual Throttle/admin paths and
  confirms the clean firmware worktree. No review edits or extra workers are used.

Both full target builds pass on clean source `4c96b9ba0` using installed
Windows PlatformIO **6.1.19**. RAK uses Nordic platform 10.11.0/GCC 9.3.1;
gateway uses Espressif platform 6.13.0/GCC 8.4.0. These are build checks only.

| Target / command | RAM used / available | Flash used / available | Result |
| --- | --- | --- | --- |
| `pio run -e rak4631` | 105,252 / 248,832 bytes (42.3%) | 759,352 / 815,104 bytes (93.2%) | Pass, 136.04 s |
| `pio run -e heltec-v3-gateway` | 132,096 / 327,680 bytes (40.3%) | 2,110,561 / 3,342,336 bytes (63.1%) | Pass, 301.40 s |

The initial gateway build hits Windows GCC's command expansion length limit
(`CreateProcess`). A temporary `subst P:` mapping of the existing
`C:/Users/Setheth/.platformio/packages` cache, selected with process-local
`PLATFORMIO_PACKAGES_DIR=P:/`, shortens framework/compiler paths and resolves
it without source/toolchain changes. An overlapping retry invalidates shared
PlatformIO output; both final builds run sequentially with the same package
path. The mapping is removed at handoff. Existing dependency/compiler warnings
remain; no warning-free or hardware acceptance claim is made.

PR #57's first Linux record check passes all eight runner regression tests but
fails three links into the uninitialized firmware submodule. The read-only
record workflow now checks out the pinned submodule before validating links;
it does not build firmware or follow the development branch head.

Private logs are under ignored `private/bench/local-3-snns-interval/`:
`behavior-tests.log`, `sensor-tests.log`, `project-checks.log` and target build
logs (`rak-reviewed-build.log`, `gateway-short-path-build.log`, plus initial
failed-attempt logs). They contain build/test evidence only; no radio profiles or keys were
read or published. The release manifest/schema, production pointer and existing
binary provenance stay unchanged for the separate release-integration outcome.

Next required bench check: select and identify one RAK and an authorized
transmitting controller under LOCAL-3 section 2. Preserve its complete profile
and keys, install an independently verified selected image, read/change/read
the device interval through authorized admin, verify unauthorized-key rejection,
save/reboot persistence, fresh device/SNNS cadence through both gateways, then
restore and verify the intended profile. Include relay-path and interrupted
command recovery. G001/G002 remain receive-only; no gateway downlink, board
flash or remote-admin provisioning is performed by this assignment.

## Run from the repository root

Pull the appropriate project branch normally and initialize its pinned
firmware submodule with `git submodule update --init firmware`. Use the
published image selected by the project, or explicitly select the fixed
local bundle below, without rebuilding during a routine update. Close
serial monitors and other device writers, then connect
one requested repeater with its antenna attached.

On Windows, create the environment once and install the pinned helper
dependencies:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r scripts\bench\repeater-requirements.txt
```

The single update command prompts for **R001–R006**:

```powershell
.\.venv\Scripts\python.exe scripts\bench\update-repeater.py
```

On Linux, use normal access to the serial device and desktop automount for
the UF2 mass-storage volume:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r scripts/bench/repeater-requirements.txt
.venv/bin/python scripts/bench/update-repeater.py
```

Numbers such as `6` or `R006` are accepted. An explicit port is optional;
port selection always requires the recorded USB serial. For an unattended
selection, preview or dry run, use the equivalent interpreter on the current
machine:

```sh
python scripts/bench/update-repeater.py --number R006 --port COM21
python scripts/bench/update-repeater.py --number R006 --show-plan
python scripts/bench/update-repeater.py --number R006 --port COM21 --dry-run
```

`COM21` is an example, never a stored board identity. Linux ports commonly
look like `/dev/ttyACM0`. `--show-plan` opens no hardware. `--dry-run` verifies
the release, reads and privately backs up the connected radio, and saves an
intended profile without flashing or writing saved configuration. Optional
`--output-dir private/bench/<new-directory>` selects a new private evidence
directory; existing directories are rejected to preserve earlier backups.

The download-only helper follows the same production pin:
`python scripts/bench/download-rak-release.py`. Explicit `--tag` selects a
known historical release for verification; it does not change the updater's
production pin or flash hardware.

## Explicit local bundle while public publication is pending

On the current Windows bench, the prepared bundle can be selected directly:

```powershell
.\.venv\Scripts\python.exe scripts\bench\update-repeater.py --local-bundle private\bench\releases\local-0634b77
```

It prompts for the repeater number. For R006 with automatic USB port
identification and a read-only dry run:

```powershell
.\.venv\Scripts\python.exe scripts\bench\update-repeater.py --number R006 --local-bundle private\bench\releases\local-0634b77 --dry-run
```

Remove `--dry-run` for the authorized update. Use `.venv/bin/python` and
forward-slash paths on Linux. The bundle is ignored by Git, so another
machine needs a private copy of its complete four-file directory. The
updater verifies its exact `build-manifest.json` bytes against the tracked
manifest, exact `SHA256SUMS`, exact asset names/sizes and both real hashes.
The assets are the application UF2 and unchanged Nordic application ZIP
renamed with `-ota.zip`. Additional, missing or changed files stop the run.

The same board identity, application-only UF2, full profile/key preservation
and reboot checks apply. Default mode never selects this directory
automatically. The success evidence explicitly records
`publishedArtifact: false`; successful local installation does not prove
public release publication or CI verification.

## Intended profile and preservation

| Repeater | Device/battery | Temperature/environment | INA219 power | Passive SNNS |
| --- | --- | --- | --- | --- |
| R001–R005 | Enabled, 180 s | Enabled, 180 s | Disabled | Enabled, 180 s baseline |
| R006 | Enabled, 180 s | Disabled; interval remains dormant at 180 s | Enabled, 180 s | Enabled, 180 s baseline |

These are the existing owner-selected sensor profiles with the new cadence.
Enabling a temperature measurement does not prove that a sensor is fitted or
working; require a fresh reading. R006's INA219 reports preserve channel 1
and signed current. Battery-inline current is separate from USB-input current;
physical calibration and battery-only behavior remain unverified.

The saved role is **CLIENT**. The updater enables neighbor reporting over
LoRa and keeps standard NeighborInfo at **21,600 seconds**. Standard
NeighborInfo has a **14,400-second minimum**; setting its interval to 180
would be clamped and would not control the separate project-private SNNS
reports. The existing `0634b77` image compiles SNNS's radio baseline to 180
seconds. The newer LOCAL-3 source instead reads saved
`telemetry.device_update_interval`: zero/unset falls back to 180 seconds,
nonzero values below 180 clamp to 180, and longer values are supported up to
a saturated baseline of 2,147,468 seconds (about 24.85 days). Saturation occurs
before millisecond conversion, reserving room for jitter below half the timer
range. Device telemetry and radio SNNS now share the selected baseline;
environment and power keep separate settings. The updater's intended device
setting stays 180 seconds; its legacy manifest checks and production pointer
remain unchanged until the separate release-integration assignment certifies
the saved-interval contract.

Initial SNNS opportunities begin about 60–75 seconds after boot;
later reports add jitter and scheduler delay and retain airtime admission
checks. Empty neighbor reports are suppressed. Device and sensor reports
also retain normal firmware scheduling, congestion and airtime limits.
Three minutes is a requested baseline, not guaranteed end-to-end delivery.

On the new source, shortening an interval preserves the previous report's
baseline plus sampled jitter once. Lengthening extends that cooldown with the
same jitter. The next report starts a fresh cooldown; missed opportunities
never produce catch-up bursts. Telemetry admin writes change in-memory
configuration, then save/reboot normally outside an edit transaction (or on
commit). A reboot uses saved configuration and a fresh 60–75-second startup
opportunity; the prior boot's cooldown is not persisted. Validate actual admin
persistence and delivery on the separately selected bench board.

Gateway local SNNS remains 60 seconds plus jitter regardless of this device
setting; preserve local-only mode and disabled LoRa TX. Standard NeighborInfo,
wire format, expiry, rotation, background priority and airtime gates retain
their existing behavior. See the pinned [firmware contract](../../firmware/SNORR_NEIGHBORS.md).

Before any flash, the updater matches the requested repeater's recorded USB
serial, radio node ID and RAK4631 hardware model. It requires an existing
PKI identity, private primary channel, configured region and enabled LoRa
transmitter. Unknown or mismatched boards stop without a device write.
No private channel key, member record or map coordinate is embedded in the
tracked script/profile.

The complete owner, local/module configuration, channel keys and security
identity are backed up under ignored `private/bench/`. Exact release assets,
manifest, sizes and SHA256 checksums must pass. UF2 blocks must target only
the nRF52840 application region, preserving the bootloader, SoftDevice and
stored configuration. The USB serial must match again on the UF2 volume,
whose Board-ID must be `WisBlock-RAK4631-Board`, and on the application port
after reboot. A changed COM/tty name alone never selects a different board.

## Native DFU failure and correction

The initial native R006 attempt completed its private backups but used a
1200-baud serial touch for DFU entry. The same USB identity reappeared as
`239A:002A` on COM26 with no mass-storage volume; the guarded writer timed
out without copying an application image. This changed the board's boot
mode and requires recovery; it was not a read-only check.

The updater now requests `localNode.enterDFUMode()` through the verified,
still-open Meshtastic API after both full backups are saved and native
storage enumeration passes. It then closes serial and only waits for the
matching UF2 volume. It never uses a 1200-baud touch. Dry-run and config-only
modes never request DFU. Offline regressions check those mode boundaries,
backup/DFU/close order and refusal to enter DFU after backup or storage
failure. The bootloader's documented
[serial-only DFU mechanism](https://github.com/meshtastic/Adafruit_nRF52_Bootloader_OTAFIX#notes-on-single-button-boards-t1000-e-and-meshtracker-x1)
is consistent with the observed missing-volume mode; the local R006
observation establishes this failure for the actual bench board.

Recovery succeeds using `adafruit-nrfutil` and the same checksum-verified
application-only OTA ZIP: application type 4, **759,304 application bytes**,
zero SoftDevice/bootloader bytes, **45.03 seconds** transfer and
`Device programmed` completion. The application API returns, and the full
corrected UF2 updater subsequently passes. Neither recovery nor the corrected
UF2 path erases saved configuration or installs a bootloader/SoftDevice.

## R006 installed verification

At **2026-10-24T00:51:19Z**, the full corrected updater exits successfully on
R006 `!da581e5f` / hardware `b8bc8fa95c2cb1e95f1e58dafebb06cc` / USB
`E9B12C5CA98FBCB8`. The installed ordinary image is
**2.7.26.0634b77**, source
**0634b775f65804968f5a18a7e8824db415556db2**, UF2 SHA256
**0734127c43d85ef846caff0f161590183aea964268fcf8fdf1649142970cc9ba**.
Full intended local/module/channel configuration and owner/key identity
match after explicit reboot: CLIENT, device/power telemetry at 180 seconds,
environment disabled, SNNS compiled at 180 seconds and standard NeighborInfo
at 21,600 seconds. Private acceptance evidence is
`private/bench/R006-local-0634b77-verified/finalverified-radio.json` and its
complete snapshots. Independent cross-recovery comparison also passes:
the original pre-failure protected profile equals the corrected run's
pre-update profile, and the intended final profile equals post-reboot
readback. Original configuration, identity/keys and channels survive the
recovery; only the intended cadence/profile changes remain. Evidence is
`private/bench/R006-local-0634b77-verified/recovery-chain-verification.json`.

Independent subscribe-only MQTT observation after the final clock gate captures
three distinct nonretained packets of each device, power and SNNS type through
**each G001/G002**: nine source packets and 18 gateway copies, received between
**2026-10-24T00:52:07.802Z and 00:58:53.068Z**. Device measurement clocks are
00:52:05 / 00:55:05 / 00:58:05; power clocks are 00:52:32 / 00:55:32 / 00:58:32.

| Report | Two measurement/report gaps | G001 receipt gaps | G002 receipt gaps |
| --- | --- | --- | --- |
| Device/battery | 180 / 180 s | 179.952 / 180.455 s | 179.963 / 180.449 s |
| INA219 power | 180 / 180 s | 179.992 / 180.008 s | 179.985 / 180.014 s |
| Private SNNS | 195 / 195 s, same boot and consecutive sequences | 195.329 / 195.126 s | 195.329 / 195.127 s |

SNNS's observed 195-second cadence includes the configured 180-second baseline
plus jitter/scheduling. Its uptime clock is relative, not a calendar hearing
timestamp. Latest device voltage is 4.164 V; signed INA219 channel 1 is
4.196 V / -0.2 mA. External-power battery flag 101 is not 101 percent charge.
No temperature/environment packet is observed. Retained packets are excluded;
12 overlapping observer copies and two unsupported packets are excluded from
these counts. The final observer runs 00:51:43–01:00:03 UTC with verified TLS,
both gateway subscriptions and zero connection/decode errors; both observers
finish and disconnect normally. MQTT observation does
not prove production database ingestion or an upstream queue-age bound.
Private evidence is
`private/bench/repeater-cadence-20261023/r006-mqtt-final-summary.json` and the
referenced raw captures. This is short bench cadence evidence; physical
current accuracy, battery-only behavior, sustained runtime and field coverage
remain unverified.
The public release/pin remains pending, and the R006 map write remains
blocked by server DNS. R001–R005 are unchanged; Linux hardware is untested.

The updater independently reads back the pinned ordinary firmware version,
the complete intended profile and all protected identity/key/channel fields,
then repeats the comparison after an explicit reboot. It sets the current
clock and closes serial. No factory reset, region replacement, key rotation,
other-board write or remote configuration occurs. An unexpected migration
or profile difference stops for inspection of the private snapshots.

Successful runs emit private `finalverified-radio.json` only after the full
post-reboot checks pass. It records actual hardware identity, pinned source
and image, verified profile and separate telemetry/SNNS/standard-neighbor
cadences. It contains no keys or coordinates. `--config-only` can resume
configuration only when the exact pinned ordinary `rak4631` firmware is
already installed; retain and inspect the previous run's evidence first.

## Acceptance after each board

Require new automatic device, fitted-sensor and SNNS packets through each
required gateway and the authenticated portal. Check source identity,
measurement/report/receipt clocks, signed power channel and expected absent
sensors separately from local profile readback. Repeat observations to
establish cadence; boot packets and one successful receipt do not establish
sustained three-minute operation, runtime, coverage or calibration.

Record each completed board in inventory, field results and the session log.
Keep unconnected boards pending. Portal map/health metadata changes require
their own saved-state and backup/recovery verification; a successful radio
update alone does not pass those checks.

## Pending R006 portal handoff

Application **443ba03** remains deployed. No portal metadata or map write has
occurred: the internal server hostname remains unresolved. Keep the supplied
point in ignored `owner-request.json`; it records an owner-provided point,
with installation unverified.

The combined private helpers are in
`private/bench/repeater-cadence-20261023/`. Their gate is the actual successful
`private/bench/R006-local-0634b77-verified/finalverified-radio.json`: full
post-reboot identity/key/profile verification, device/power 180 seconds,
environment disabled, SNNS 180 seconds and standard NeighborInfo 21,600
seconds. Copy that evidence into the helper directory only after checking
its identity/source against the installed board. The private stage pins the
SHA256 of the exact reviewed
[manual migration source](../../deploy/portal/update-r006-metadata.js).
It is outside automatic application migrations and contains no coordinates.

An independent location-only helper bundle is retained in
`private/bench/repeater-location-20261023/`. It can record the point without
changing existing firmware, cadence, sensors or deployment status. Either
route first requires live preflight, a complete pre-change checkpoint and
isolated live/demo recovery, then isolated transaction/idempotence checks,
writer quiescence, exact protected-state comparison and retained rollback.
Verify authenticated portal state and take a post-change recovery checkpoint.
The known bounded-demo verifier limitation requires the independent exact
bounded-history recovery check. Other repeaters' applied metadata stays
unchanged until each board is actually updated.

Public release automation is separately blocked: the SSH source push and
the external-app comment retry **5c2c1ad** produced zero workflow runs; the
new workflow remained unregistered at the latest check. GitHub documents
that push workflows use the event's source ref, so a default-branch merge is
not a documented prerequisite. Authenticated Actions settings remain to
inspect; no settings or default-branch changes were made.
[Workflow trigger behavior](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows),
[trigger troubleshooting](https://docs.github.com/en/actions/how-tos/troubleshoot-workflows).
