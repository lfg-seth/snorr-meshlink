# Repeater firmware and three-minute profile updater

Owner request, 2026-10-23: prepare R001–R006 to report available statistics
every three minutes, provide a reusable firmware/configuration updater, and
place R006 at its owner-provided map location. R006 remains **INA219 only, with
no temperature sensor**. Exact coordinates and private radio material stay in
ignored storage.

## Current rollout status

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
- **R006 passes the corrected native Windows UF2 updater** at
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
reports. The selected RAK firmware compiles SNNS's radio baseline to 180
seconds. Initial SNNS opportunities begin about 60–75 seconds after boot;
later reports add jitter and scheduler delay and retain airtime admission
checks. Empty neighbor reports are suppressed. Device and sensor reports
also retain normal firmware scheduling, congestion and airtime limits.
Three minutes is a requested baseline, not guaranteed end-to-end delivery.

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
