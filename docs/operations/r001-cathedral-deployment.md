# R001 Cathedral Rock deployment configuration

Owner selects Cathedral Rock on 2026-11-15: **R001**, **Case 01**, **eight
cells**, **Muzi antenna**, ROUTER role and the supplied fixed coordinates.
This is the fresh radio **!f95b5501**, USB **E93C5FF0F97DD76B**, hardware
**6bd77df9f05f3ce901555bf96d5ed7fc**, RAK19007/RAK4631 with INA219/AHT21.
Exact coordinates and complete profiles remain in ignored private evidence.

## Configuration and verification

USB identity and complete backup confirm installed **2.7.26.bcb22e0**, the
previously recorded `rak4631-survey` image. **No firmware flash, rebuild,
factory reset or key replacement.** Direct SDK configuration replaces the
historical number-based role script, whose R001 mapping refers to a different
physical radio.

Save ROUTER and fixed position using the owner's decimal coordinates, encoded
as integer degrees × 10^7. Retain existing altitude, without inventing site
elevation. Reassert the original complete affected sections after the role
write because firmware installs role defaults:

- Preserve **LOCAL_ONLY** rebroadcast, private channels, US/LongFast slot 35,
  hop limit 3, TX enabled at 10 dBm, names, individual PKI/admin keys,
  survey enrollment, network, Bluetooth and disabled power saving.
- Retain enabled device/environment/INA219 power telemetry at **180 seconds**,
  passive SNNS using that saved baseline and standard NeighborInfo at
  **21,600 seconds**. Position cadence remains **21,600 seconds**.
- Accept the firmware's ROUTER owner `isUnmessagable=true` announcement and
  role-derived API `power.ls_secs=86400`; power saving remains disabled.

First full-node-list verification times out; no settings are retried.
A bounded `noNodes=True` connection then verifies exact complete local/module/
channel bytes, identity, owner fields and fixed coordinates against the
intended profile, with only the documented role effects. Firmware metadata is
unchanged except its reported role. An explicit reboot is issued after a
second matching readback. The first post-reboot connection also times out;
a subsequent read-only connection passes the same exact comparison. No write
or reboot is retried. Complete profile and exact fixed coordinates therefore
pass both before and after explicit reboot. The connection-timeout cause is
unisolated; this is not a USB-stability acceptance result.

Private backup, intended profile, independent readbacks, local configuration
commands and serial logs: `private/bench/R001-deploy-20261115/`. The local
commands acquire the station lease and select only the matching USB serial.
Serial handles close after each operation.

## Assembly and remaining evidence

Case 01/eight cells/Muzi are owner-reported deployment allocations, not new
purchases. The [case intake](../../records/inventory.md) identifies Case 1 as
v4 PETG, one SMA port, two fitted 160 mA panels and two four-cell parallel
holders. No new panel specification, cell capacity, inter-holder wiring,
antenna gain or measured runtime is inferred.

Saved cadence is configuration evidence, not measured delivery intervals.
No RF, MQTT, portal, forced-relay, coverage, solar or sustained battery-only
acceptance is claimed by this configuration. Physical placement/mount and
installation completion remain to be confirmed. This survey image retains its
900-second autonomous-report quiet window after an accepted survey PING;
quiet time and airtime admission can defer its own reports. Ordinary relaying
and reporting must be evaluated separately in the field. No portal change is
part of the owner's mesh-configuration request.
