# R010 Upper Bristle deployment - 2026-11-15

Owner selects **R010 / Case 4 / eight cells / Muzi antenna** for **Upper
Bristle**, with a supplied exact coordinate pair. Exact coordinates and full
profiles stay private. This is configuration only; stop if flashing is needed.

## Identity and intended configuration

Fresh USB backup independently confirms **820C9B4F0C2D7675**, radio
**!77fdb9f1**, hardware **75762d0c4f9b0c82f1b9fd774661875b**, RAK4631 and
installed **2.7.26.bcb22e0 / rak4631-survey**. Retain installed firmware;
no flash, factory reset, rebuild or key replacement. INA219 and AHT21 were
previously measured after owner solder rework; new field readings are separate.

Set **ROUTER** and exact fixed position as integer degrees × 10^7, preserving
existing altitude or leaving it unspecified. Preserve own identity/keys/admin,
channels/names, LOCAL_ONLY, US/LongFast slot 35, enabled TX at 10 dBm, hop 3,
RX boost/FEM settings, already-enabled **OK to MQTT**, ignore-MQTT, disabled
power saving, network/Bluetooth and this board's own GPS/position settings.
Keep enabled **180-second device/environment/power**, saved-baseline SNNS,
**21,600-second NeighborInfo** and own **21,600-second smart position** cadence.
Preserve Fahrenheit display, timezone and triple-click setting. Reassert
sections affected by firmware role defaults; accept ROUTER owner
`isUnmessagable=true` and API sleep default 86,400 seconds, with power saving off.

Station lease, runtime USB/radio/hardware and complete fresh-profile guards
precede settings writes. Explicit DTR asserted / RTS deasserted is used for
nRF52 serial sessions. Private evidence: `private/bench/R010-upper-bristle-20261115/`.
Complete intended local/module/channel bytes, owner/identity, firmware metadata
and exact integer coordinates pass independent readback **before and after
one explicit reboot**. All serial sessions succeed without retry. Serial closes;
ready to unplug. Dashboard baseline adds this saved position cadence, and
private full-profile/key/channel/cadence assertions pass. No live delivery is
implied by those checks.

## Assembly and acceptance limits

Existing Case 4 intake: **v4 ASA, two SMA ports, two 200 mA panels, two
four-cell parallel holders**. Owner selects eight cells and Muzi. No new
purchase, cell-capacity, holder-wiring, antenna-gain or panel-output inference.

Configuration does not establish fresh sensor/CLI/portal delivery, sustained
cadence, completed mount/installation, forced relay, coverage or runtime.
B003 is absent; no ping is requested or run. Prior CLI server access is
unavailable from this laptop; trusted monitoring access must be restored
before claiming new ordinary receipts. Survey quiet may delay autonomous
reports for 900 seconds after a ping or reboot with its marker present.
