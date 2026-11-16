# G002 Shady Hollow offline SD recorder - 2026-11-15

**Publication update, 2026-11-15:** owner approves publishing the exact fixed
location in the [deployment table](../../records/sites.md#2026-11-15---published-deployment-setup-and-fixed-locations). Earlier privacy wording below describes the original evidence handling;
complete profiles and raw logs remain ignored.

Owner selects **G002 / Case 7 / eight cells / Muzi** for **Shady Hollow**, with
exact supplied coordinates. Purpose is local SD recording without Wi-Fi;
CLIENT or ROUTER is authorized. Keep existing **CLIENT / rebroadcast NONE**,
which supports recording without introducing a new routing role. Identity
and label remain G002; no portal reassignment is requested. Exact coordinates,
raw packet logs and full profiles stay private.

## Configuration

Fresh USB backup independently identifies **F8:5B:1B:BF:0A:B8**, radio
**!1bbf0ab8**, hardware **bfd67fc07c1161ce8fae291933705196**, HELTEC_V4 and
installed **2.7.26.f6cdbeb / heltec-v4-sd-gateway-survey**. The installed
recorder supports offline logging; no firmware flash, factory reset or rebuild.
[Original commissioning](g002-screenless-gateway.md) remains historical.

Disable **Wi-Fi and MQTT**; retain saved credentials privately for future use.
Save the owner-supplied fixed coordinates as integer degrees × 10^7, retaining
existing altitude or leaving it unspecified. Preserve own keys/admin list,
channels/names, CLIENT/NONE, radio/power/Bluetooth, enabled device/INA219 power
**300 seconds**, saved-baseline SNNS, standard NeighborInfo **21,600 seconds**,
GPS NOT_PRESENT and own **3,600-second smart-position** settings. Leave the
recorder's card, files, rotation policy and private survey pairing intact.

Station lease/full fresh-profile guard precede writes. Complete intended
local/module/channel bytes, owner/identity, hardware/firmware metadata and exact
fixed coordinates pass before and after the one explicit reboot. Temporary
structured USB logging is restored to its original setting; the final
independent full-profile read verifies that restoration. Serial closes.
Private commands and evidence:
`private/bench/G002-shady-hollow-20261115/`.

## SD writes verified with networking disabled

Two successful local sync diagnostics show segment **23**, frames **123 → 151**, **zero drops**, **4,208 / 31,149,056 KiB** used/total.
The first 135-second observation obtains one healthy sync but no proven frame
growth. A second observation retains every sync and requests one telemetry
read addressed only to G002 itself over USB; newly generated local records
are included in the successful growth check. This is not an RF ping or field
reception/coverage trial. The full offline profile and connection-status replies confirm Wi-Fi
and MQTT disabled throughout this observation. SD writes continue without an
internet uplink. No card erase, destructive diagnostic or file rotation-policy
change. Physical copied-file integrity/endurance remain separate checks.
Observation timestamps and raw diagnostic references remain private.

## Offline recording and monitoring

Pinned `f6cdbeb` `SnorrRecorder.cpp` starts the writer independently of Wi-Fi
and MQTT. Incoming raw RF, decoded/local packets and recorder events feed its
queue; successful diagnostics follow `f_sync` and capacity refresh. Recording
uses boot/sequence/monotonic values and records clock quality, including unknown
UTC. USB-set time does not prove clock acquisition on a field cold start.

The same firmware gates SNSD/SNGH on Wi-Fi/MQTT enablement. With both disabled,
absence of those remote health reports is expected and is not a card-failure
verdict. CLI baseline disables gateway/Wi-Fi/SD-report deadlines for this
selected offline use, retaining ordinary radio/position baselines. No production
portal/server/gateway service changes or downlinks are made.

## Assembly and remaining checks

Case 7 intake is **v4 PETG, one SMA, two 200 mA panels, one four-cell parallel
holder/four-cell capacity**. Owner now explicitly allocates **eight cells**;
that newer count supersedes the earlier count, without inferring a second
holder, wiring or physical fit. No purchase, stock recount, capacity/runtime,
antenna-gain or solar-output claim.

Physical copied-card file inspection, sustained recording/power-loss recovery,
calibration, completed installation, field reception/coverage and battery/solar
runtime remain separate checks. No ping or relay acceptance is implied.
