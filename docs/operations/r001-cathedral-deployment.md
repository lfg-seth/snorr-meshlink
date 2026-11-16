# R001 Cathedral Rock deployment configuration

**Publication update, 2026-11-15:** owner approves publishing the exact fixed
location in the [deployment table](../../records/sites.md#2026-11-15---published-deployment-setup-and-fixed-locations). Earlier privacy wording below describes the original evidence handling;
complete profiles and raw logs remain ignored.

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

## B003 direct ping check - 2026-11-15

Owner connects B003 **!699c2ed8**, installed survey tester **2.7.26.7b766e6**,
and requests one simple R001 ping. Existing local survey service already owns
USB **90:70:69:9C:2E:D8**; the direct open correctly fails its exclusive lock,
with no command sent. Use that service's live command API rather than compete
for serial ownership or stop the service.

One authenticated **zero-hop** attempt to **!f95b5501** succeeds: **1/1**, reply
matched to session/attempt/target, **2,460 ms** TX-start-to-reply round trip.
R001 measures uplink **-89 dBm / 5.25 dB SNR**; B003 measures downlink
**-69 dBm / 5.5 dB SNR**. Local/remote utilization is **12% / 11%**. Production
LongFast slot 35 / 10 dBm remains selected. Explicit bench mode avoids making
GPS freshness an interlock for this simple radio check; raw GPS stays private.

Stop after the first result, restore original timing and independently confirm
idle/stopped state. The original target list was empty; R001 remains selected
because the interface cannot clear a target list. No firmware or persistent
mesh configuration change. Existing survey service retains its serial handle;
no competing direct handle remains. Private result, API transcript and final
state: `private/bench/B003-R001-ping-20261115/`.

This verifies the requested direct ping round trip, not forced relaying,
portal delivery, sustained coverage or runtime. An accepted survey PING renews
the 900-second autonomous-report quiet window on hearing responders.
