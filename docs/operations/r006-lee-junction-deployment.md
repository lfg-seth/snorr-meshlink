# R006 Lee Junction deployment - 2026-11-15

**Publication update, 2026-11-15:** owner approves publishing the exact fixed
location in the [deployment table](../../records/sites.md#2026-11-15---published-deployment-setup-and-fixed-locations). Earlier privacy wording below describes the original evidence handling;
complete profiles and raw logs remain ignored.

Owner selects **R006 / Case 3 / eight cells / Muzi antenna** for **Lee
Junction**, supplying exact coordinates. Coordinates and full profiles remain
private. Configuration only; stop if flashing is needed.

## Identity and configuration

Fresh USB backup confirms **76642362C6FCE382**, radio **!638b9515**, hardware
**82e3fcc66223647615958b63dd296ca1**, RAK4631 and installed
**2.7.26.bcb22e0 / rak4631-survey**. Retain firmware without flashing, factory
reset, rebuild or key replacement. INA219/AHT21 were previously measured;
new field readings remain separate.

Set **ROUTER** and exact fixed coordinates as integer degrees × 10^7, retaining
existing altitude or leaving it unspecified. Preserve own identity/keys/admin,
channels/names, LOCAL_ONLY, US/LongFast slot 35, enabled TX at 10 dBm, hop 3,
RX boost/FEM, already-enabled **OK to MQTT**, ignore-MQTT, disabled power
saving, network/Bluetooth, timezone, triple-click and Fahrenheit settings.
Keep enabled device/environment/power **180 seconds**, saved-baseline SNNS,
**21,600-second NeighborInfo and position**. Preserve this unit's GPS
**NOT_PRESENT**, 86,400-second receiver interval, position flags 10 and smart
position disabled; do not copy another board's GPS/smart settings.
Reassert sections affected by firmware role defaults, accepting ROUTER owner
flag and API sleep default 86,400 seconds while power saving stays off.

Station lease and USB/radio/hardware/full-initial-profile guards precede writes.
Explicit DTR asserted / RTS deasserted is used for nRF52 serial. Private
commands, full before/intended/readback profiles and logs:
`private/bench/R006-lee-junction-20261115/`.
Complete intended local/module/channel bytes, owner/identity, firmware metadata
and exact integer coordinates pass independent readback **before and after
one explicit reboot**. All serial sessions succeed without retry and close.
Additional comparison confirms only planned role/fixed-position/API-default
changes; module/channel bytes and individual keys remain unchanged. Saved
position cadence is added to the CLI baseline and verified against readback.
Ready to unplug; no live delivery is implied by these configuration checks.

## Assembly and acceptance limits

Case 3 historical intake is **v4 ASA, one SMA port, two 160 mA panels and two
four-cell parallel holders**. Owner confirms eight cells/Muzi. No purchase,
stock recount, cell-capacity, holder-wiring, antenna-gain or panel-output claim.

New sensor/CLI/portal receipts, sustained cadence, installation/mount,
forced relay, coverage and runtime remain unverified by configuration. No
B003/ping is involved. Saved reporting settings are not measured delivery.
Survey quiet may defer reports after an accepted ping or reboot with its marker.
