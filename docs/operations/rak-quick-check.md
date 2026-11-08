# RAK quick function check

Owner-approved scope, 2026-11-07: Windows desktop; RAK4631 core/carrier,
LoRa and fitted INA219/temperature sensors. Target under five minutes per board
after one-time reference setup, including ordinary operator steps. Failures are
recorded and the batch continues; troubleshooting, burn-in, Bluetooth,
enclosure work, wiping and reflashing stay separate. Elapsed time is recorded;
the five-minute target is not yet measured on hardware or a hard timeout that
could abandon configuration restoration.

Implementation: [check-rak.py](../../scripts/bench/check-rak.py).
Offline tests do not establish hardware acceptance. No board was connected,
configured or flashed during implementation; only COM1 enumerated on the desktop.

## Fixture and first run

1. Inspect each board unpowered yourself. Record smoke/reverse-polarity history,
   flex/pin damage or corrosion. A board that is not safe to power can receive
   a failed inspection report without opening its serial port; an unresponsive
   board can be recorded with `skip`. Neither produces a configuration backup.
2. Use the new RAK as the reference, already running compatible Meshtastic
   firmware and responding to its USB API. A factory/test/LoRaWAN image is not
   a compatible reference. This tool does not install firmware. Both radios
   must identify as RAK4631 and have distinct node IDs, hardware IDs and USB ports.
   Reversible triage requires an initialized US-region baseline, existing nonzero
   32-byte PKI keys, and expanded modem/default settings. An uninitialized board
   is backed up and reported inconclusive without writes; prepare it separately.
3. Use included **915 MHz RAK antennas**. Attach one to the reference and use the
   same second antenna on each suspect board. Keep both upright at marked
   positions several metres apart, with consistent cables/orientation. Start
   with an apparently undamaged board. Keep Muzi comparisons for separate work.
4. Have a healthy partially discharged compatible rechargeable battery, correct
   connector polarity, normal INA219 battery-path wiring and USB inline V/A meter
   ready. Record fitted sensors and shunt marking; do not infer them from config.
   The USB meter/cable must pass data for the serial portions of the test.
   Replugging may change COM numbers; the tool reconnects by USB serial identity.
5. Close Meshtastic apps and other serial tools. From the repository root in
   PowerShell, list ports without opening any:

   ```powershell
   .\.venv\Scripts\python.exe scripts/bench/check-rak.py --list-ports
   ```

   Dependencies already exist on this desktop: Python 3.14.3, Meshtastic 2.7.11
   and pyserial 3.5. For another environment use the pinned
   [requirements](../../scripts/bench/repeater-requirements.txt).

6. Substitute the reference's actual COM port. This starts the guided batch:

   ```powershell
   .\.venv\Scripts\python.exe scripts/bench/check-rak.py --peer COM5
   ```

   Enter each test board's COM port, or `skip` to record a board with no usable
   port. A blank port ends the batch and restores the reference. Labels may be
   R001–R006 or temporary labels; no inventory whitelist is imposed. To run only
   one selected board:

   ```powershell
   .\.venv\Scripts\python.exe scripts/bench/check-rak.py --peer COM5 --port COM9
   ```

   For a board with no battery connected, add `--usb-only`. Battery, charging
   and meter steps are skipped and recorded NOT_TESTED; no USB disconnect is
   requested. USB/config, radio, any fitted modules and restoration still run.

## What happens

The reference receives its own private original-config backup before changes.
Each test board is separately backed up before writes. The temporary profile
uses US region, LONG_FAST, frequency slot 20, configured 10 dBm, no relaying,
a random channel name and fresh random 256-bit PSK. Secondary channels are
temporarily disabled. Only device, LoRa, telemetry and channels are written;
hardware-specific FEM mode is retained. Identity/security/position settings
are preserved. Full intended profile readback gates testing.

Restoring a changed role can reset other firmware defaults. After the role is
read back, restoration may reapply observed differences in device, position,
power, display, telemetry and neighbor settings, plus the owner's message-status
flag. Before that corrective transaction, every remaining identity, key,
channel, owner and config field must match the backup. Unexpected differences
stop recovery; no ambiguous write is blindly retried. Names and license state
are preserved. Final full comparison still runs after an explicit reboot.

| Check | Evidence and limits |
| --- | --- |
| USB/config | Complete API-visible local/module configs, every channel, serialized protobufs, identity, firmware metadata and self node information. No raw flash/bootloader/filesystem backup. Missing identity/channel data prevents writes. |
| Firmware/reboot | Available critical-error signatures retained privately. Recognized signatures fail the run; absent logs cannot prove absence of faults. Original config is compared after an explicit reboot at restoration. |
| Temperature/humidity | Request current environment telemetry locally for a physically fitted sensor. Missing/unsupported response is inconclusive. Returned finite data demonstrates availability, not calibration or exact sensor model. |
| INA219 | Request power telemetry locally, then compare current with USB connected and during battery-only operation. A matched change of at least 1 mA is a response check, not a tolerance specification. Raw firmware polarity and mA units are preserved. |
| LoRa TX and RX | Three unique PRIVATE_APP probes each direction; require the opposite USB radio to receive exact source/destination/packet ID/payload with zero-hop metadata. ACK/enqueue success is insufficient. Counts and supplied RSSI/SNR are recorded. Partial/missing reception fails this fixture check; it does not isolate the faulty component. |
| Charging | Operator records USB V/A and indicator state. Indicator on means charging activity observed, not charger-current accuracy or full-charge termination acceptance. |
| Battery power | Close the test board's serial connection, unplug only its USB, then request fresh device/power telemetry through the reference. Missing response is inconclusive because RF/firmware/power causes are not isolated. Reconnect USB for restoration. |

The private test channel separates application traffic from the production mesh;
it does not eliminate RF interference. PRIVATE_APP is also used by SNNS, but the
bench channel has an independent key and probes use a distinct `RAKCHECK1:` magic.
The new reference is a comparison peer, not a calibrated known-good RF standard.
Close-range packet success does not clear a PA potentially damaged by antenna-free
operation. RF power/sensitivity, range, intermittent flex faults, all GPIO/slots,
sensor accuracy, solar input, charger protection/termination, battery capacity
and runtime remain untested. Do not reproduce reverse-polarity or flex damage.

RAK specifies **350 mA nominal charging** for both
[RAK19007](https://docs.rakwireless.com/product-categories/wisblock/rak19007/datasheet/#battery-connector)
and [RAK19003](https://docs.rakwireless.com/product-categories/wisblock/rak19003/datasheet/#battery-connector).
Actual current varies with battery state. USB input supplies the board and
charger, while the INA219 measures its fitted branch; their current readings
are not expected to match. Accuracy needs a reference measurement in the same
branch or across the known shunt; see the
[TI INA219 datasheet](https://www.ti.com/lit/ds/symlink/ina219.pdf) and existing
[project calibration limitations](ina219-audit.md).

## Evidence, failures and recovery

Everything generated stays in ignored `private/bench/rak-check-<UTC>/`:

- `sdk.log`: private SDK/serial output across the session.
- `reference/original.json`, `diagnostic.json`, `restored.json`: peer records.
- `board-<UTC>/original.json`, `diagnostic.json`, `restored.json`: board records.
- Per-board `report.json` and readable `report.md`: outcomes, measurements,
  observed module/power conditions, supplied fault notes and elapsed time.
- `batch.json`: labels, USB identities and verdicts for completed board reports.

Backups/logs can contain keys and saved positions. Keep these files private;
publish only manually sanitized summaries. Windows file mode bits are not an
ACL guarantee; these files inherit the user's private workspace permissions.
The backup is an API snapshot of the running config, not byte-exact flash.

Verdicts are PASS for the tested subset, FAIL for a failed check, or INCONCLUSIVE
when a required result cannot be established. NOT_FITTED and NOT_TESTED remain
explicit per-check statuses. A failure finishes the board report and moves on;
configuration restoration is attempted even after failure or Ctrl+C. Restoration
failures are prominent and retain the original backup. Unplugging/killing the
process or losing power can prevent cleanup; never discard the saved originals.

Recover a board using its own backup and current COM port:

```powershell
.\.venv\Scripts\python.exe scripts/bench/check-rak.py --recover "private\bench\rak-check-<UTC>\board-<UTC>\original.json" --port COM9
```

For the reference use `reference\original.json`. Recovery requires matching
USB/hardware/node identity, restores only the sections this tool can change,
and compares the complete config after reboot. It never retries an ambiguous
recovery write automatically. If verification fails, retain the unit as
unresolved before wiping/reflashing separately. Exit codes: 0 tested subset
passed/no units, 1 failure, 2 inconclusive results without failures.

Next acceptance: run one apparently healthy board through the complete fixture,
inspect the private original/restored comparison and actual wall-clock time,
then begin the suspect-board batch. Burn-in remains future work.

## Reference prepared - 2026-11-07

Owner identifies the sole connected RAK as the reference and confirms its
included antenna is attached. USB **70DF102F58D2A034**, node **!8737c2c9**, on
**COM27**, identifies as RAK4631 and reports **2.7.15.567b8ea**. Carrier model
is not established by the USB/API identity. Firmware was retained; no flash.

Reference now has CLIENT/no-relay, US, LONG_FAST (250 kHz / SF11 / CR5), slot 20,
configured 10 dBm, a random private bench channel, disabled secondary channels,
hourly device telemetry and disabled environment/power telemetry. Complete
intended-config comparison and a second explicit reboot/readback pass. Fresh
requested device telemetry passes; local-stats response was not obtained.
Serial is closed; leave the reference connected while attaching the next board.

The initial unconfigured snapshot had no PKI key material, unset region and
unexpanded preset values. First region setup/reboot generated the board's keys
and expanded defaults; strict raw comparison correctly rejected that as a
restoration of the original snapshot. Subsequent checks use the initialized
baseline and preserve its new keys. The script now explicitly supplies all
LONG_FAST values and stops before writes on uninitialized triage units, keeping
key/channel comparisons strict. A factory snapshot is evidence of the starting
state, not a promise that generated identity/defaults can be undone by this tool.

Private factory/initialization records:
`private/bench/reference-setup-20261107T214624394618Z/`.
Verified preparation, initialized recovery baseline and local telemetry:
`verified-setup-20261108T011046061350Z/` beneath that directory.
`private/bench/rak-reference.json` records the current reference identity and
private snapshot/recovery pointers. The batch command is now:

```powershell
.\.venv\Scripts\python.exe scripts/bench/check-rak.py --peer COM27
```

The batch temporarily selects its own channel and restores the prepared
reference profile at completion. No second board, bidirectional RF test,
sensor/charging test or per-board five-minute measurement has yet been run.

## rak01 USB-only check - 2026-11-07

Owner assigns **rak01** solely within this bench context, independently of saved
radio/profile names and historical project assignments. Owner identifies a
**RAK19003 carrier with no modules**, USB only, and directs that antenna attachment
be assumed for this testing session. USB **AA474A4710B85C2C**, node **!a65601b3**,
on **COM8** identifies as RAK4631 and retains **2.7.26.4c96b9b**. No historical
profile is selected by the test label and no persistent device rename occurs.

| Check | Measured result |
| --- | --- |
| USB/backup and intended test profile | Pass; complete original snapshot saved before temporary writes. |
| Radio reception at rak01 | 3/3 direct reference probes; RSSI -13 dBm, SNR 6.25 / 5.75 / 6.25 dB. |
| Radio transmission from rak01 | 0/3 matching direct receptions at the reference; failed fixture check. |
| Requested local device metrics | No matching response; inconclusive. |
| Temperature and INA219 | Not fitted, owner-reported. |
| Battery/charging/meter | Not tested; no battery or supplied meter readings. |
| Original board profile and reference restoration | Both pass full comparison through explicit reboot. Serial handles closed. |
| Duration | 317.6 seconds including operator wait and the canceled power prompt; five-minute acceptance not met. |

Result: **FAIL on the transmit check**, not a confirmed diagnosis of damaged
radio silicon. Board, firmware, antenna path and reference/fixture causes are
not isolated. Owner's fail-and-move-on policy applies; no further probes or
component diagnosis were performed.

The original CLI did not support skipping the battery workflow. It was stopped
at its power prompt after the owner specified USB-only; raw report preserves
the resulting EOFError. A separate scoped report retains all measured results,
explicitly records the intentional stop and marks power checks NOT_TESTED.
Added `--usb-only` plus an offline regression ensuring no battery query or USB
disconnect prompt occurs. Its complete live flow awaits the next selected unit.

Private evidence: `private/bench/rak-check-20261108T011619258740Z/`, board
`board-20261108T011708487298Z/` (`report.json`, `scoped-report.json`,
`scoped-report.md`, `original.json`, `restored.json`). Fresh test-label/antenna
instructions are retained in `private/bench/rak-test-context.json`.

## rak02 reboot and USB failure - 2026-11-07

Next bench-only label **rak02** identifies USB **820C9B4F0C2D7675**, node
**!77fdb9f1**, initially on **COM17**, RAK4631 with retained reported firmware
**2.7.26.4c96b9b**. Owner identifies this as the suspected reverse-polarity
damaged unit, with INA219, AHT21 and an attached battery estimated at about
3.2 V. Carrier model, INA219 path/shunt, USB meter readings and charging
indicator were not reported at this checkpoint. Antenna connected per owner.

Initial USB/API connection and full original backup pass. After temporary test
settings and the reboot/reconnect attempt, the board no longer enumerates as a
USB serial port. The bounded reconnect fails; the restoration reconnect also
fails. The original board configuration is backed up, but **restoration remains
UNVERIFIED**. Reference profile restoration/reboot verification passes and all
serial handles are closed. No firmware is flashed and no historical profile is
selected by the test label.

Result: **FAIL on reboot/USB availability**, with no isolated hardware diagnosis.
Radio TX/RX, INA219 readings, AHT21 readings, battery-only operation and charging
were **NOT TESTED** because the run stopped before their execution. No absent
sensor response or radio result is inferred. Failed-run duration **147.7 s**;
this does not establish complete-function or five-minute passing acceptance.

Private evidence: `private/bench/rak-check-20261108T013351230604Z/`, board
`board-20261108T013437782527Z/`: `original.json`, unchanged raw `report.json`,
`scoped-report.json` and `scoped-report.md`; root `sdk.log` and reference records.
Read-only preflight is separately retained in
`private/bench/rak02-preflight-20261108T013315891113Z/`.

Owner has been asked to unplug/reconnect only the suspect unit's USB for an
original-settings recovery attempt, leaving the reference connected. If heat or
a burning smell is observed, leave it disconnected instead. This is a recovery
gate, not another function-test run. Do not mark the unit restored until a fresh
USB readback verifies it. Further board diagnosis/retesting remains owner-selected.

### Original configuration recovered - 2026-11-07

USB-only replug while the battery remained connected did not return a port.
After the owner disconnected both power sources and reconnected USB with no
battery, **rak02 returned on COM17**. Recovery writes and reboots now retained
USB access, but full comparison exposed firmware role-default side effects:
rebroadcast mode, GPS/position intervals, neighbor interval and the message-status
flag differed. Channels, keys and hardware identity already matched.

Source inspection of `AdminModule::handleSetConfig` and
`NodeDB::installRoleDefaults` establishes that changing back to the saved role
installs those defaults. Reapplied the original affected sections/status flag
with the role unchanged; **complete original config, owner, channels, keys and
saved fixed position now match through explicit reboot**. Serial closed; no
flashing or function-test repetition. This supersedes the initial restoration
warning, while the original USB/reboot test failure and untested functions remain.

Final private evidence:
`private/bench/rak02-role-recovery-20261108T015055471250Z/`
(`before.json`, `corrected.json`, `reboot-verified.json`, `result.json`). Earlier
recovery snapshots are retained. Scoped result/context now point to this verified
recovery. The script's restoration path now handles observed role defaults,
with a regression reproducing the exact failure and guards against changing
keys, channels, other owner fields or hardware identity. Next: move to the next
owner-selected test unit; physical fault diagnosis remains separate.
