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

## What happens

The reference receives its own private original-config backup before changes.
Each test board is separately backed up before writes. The temporary profile
uses US region, LONG_FAST, frequency slot 20, configured 10 dBm, no relaying,
a random channel name and fresh random 256-bit PSK. Secondary channels are
temporarily disabled. Only device, LoRa, telemetry and channels are written;
hardware-specific FEM mode is retained. Identity/security/position settings
are preserved. Full intended profile readback gates testing.

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
