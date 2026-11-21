# R008 deployment configuration

## 2026-11-21 - Escarpment Trail reassignment

The owner reassigns **R008 / !120b04fd** from Kyle Junction to **Escarpment
Trail (36.26491, -115.59496)**. Bench USB serial **F4D0968336047CA0** and
hardware ID **a07c04368396d0f4fd040b12638298d4** identify the RAK4631.
The starting readback and private backup confirm **ROUTER**, fixed position and
**OK to MQTT enabled** (`lora.config_ok_to_mqtt=true`).

The only write was the new fixed position. Independent USB sessions read back
the exact integer coordinates **362649100 / -1155949600** before and after an
explicit reboot with observed USB disconnect and re-enumeration. Altitude,
owner and complete local, module and channel configuration matched the backup,
including firmware **2.7.26.bcb22e0**, keys and 180-second telemetry settings.
Serial is closed. Private backup and readbacks are in
`private/bench/R008-escarpment-20261121/`.

The read-only MQTT archive shows three fresh, non-retained packets from R008
via **G003 / !849ad7a0** after reboot. Node info arrived at **10:30:57 Pacific**,
the exact new fixed position at **10:30:58**, and device telemetry at
**10:31:13**. The fixed position packet had no GPS measurement timestamp.
Physical installation, receipt from Escarpment Trail, sustained reporting,
portal display, coverage and runtime remain pending.

## 2026-11-15 - Kyle Junction configuration history

**Publication update, 2026-11-15:** owner approves publishing the exact fixed
location in the [deployment table](../../records/sites.md#2026-11-15---published-deployment-setup-and-fixed-locations). Earlier privacy wording below describes the original evidence handling;
complete profiles and raw logs remain ignored.

Owner selects **Kyle Junction**, **R008**, **Case 8**, **eight cells** and
**Muzi antenna** on 2026-11-15, continuing the configuration-only deployment
sequence. Exact supplied coordinates stay in private evidence and mesh config.

## Identity and configuration

USB **F4D0968336047CA0**, radio **!120b04fd**, hardware
**a07c04368396d0f4fd040b12638298d4**, RAK4631 with previously detected
INA219/AHT21. Live readback confirms retained **2.7.26.bcb22e0**, recorded
`rak4631-survey` image. **No flash, rebuild, reset or key replacement.**

Back up the complete individual profile before writing. Set **ROUTER** and
fixed position with integer coordinates (degrees × 10^7), retaining existing
altitude without inventing site elevation. As with
[R001](r001-cathedral-deployment.md), reassert original affected configuration
sections after firmware installs role defaults:

- Preserve names, individual PKI/admin allowlist, channels, LOCAL_ONLY
  rebroadcast, US/LongFast slot 35, TX enabled at 10 dBm, hop limit 3,
  network/Bluetooth and disabled power saving.
- Preserve enabled device/environment/INA219 power **180-second** settings,
  saved-baseline SNNS and **21,600-second** standard NeighborInfo.
- Retain this board's own **43,200-second** smart position reporting and GPS
  mode/pins/settings; fixed coordinates are now enabled. Do not copy R001's
  different position cadence or flags.
- Accept ROUTER's owner `isUnmessagable=true` announcement and role-derived
  API `power.ls_secs=86400`, with power saving still disabled.

Direct SDK operations select only the matching USB serial, validate hardware,
radio identity and existing private profile, and acquire the station lease.
Complete intended local/module/channel bytes, owner/identity, firmware metadata
and exact coordinates pass independent comparison **before and after explicit
reboot**. The first verification open hits USB I/O errors; the next read passes
and issues the one explicit reboot. An early post-reboot open sees the port
disappear; after settling, a read-only retry passes. No configuration or reboot
is repeated. USB stability is not established. Handles close after every
operation.
Private snapshots, local commands and serial logs:
`private/bench/R008-deploy-20261115/`.

## Assembly and remaining evidence

Case 8's historical intake records **v4 ASA**, **two SMA ports**, **two
160 mA panels** and **two four-cell parallel holders**. Case/eight cells/Muzi
are owner-confirmed allocations of existing equipment, not new purchases.
Cell model/capacity, inter-holder wiring, antenna model/gain, mount and solar
output are not inferred from that allocation.

Saved cadence is not measured delivery. No ping, RF/MQTT/portal acceptance,
forced relay, sustained coverage, battery-only runtime or completed physical
installation is claimed by this configuration. B003 is not attached in this
USB enumeration. The retained survey responder can defer autonomous reports
for 900 seconds after the latest accepted survey PING. Next: confirm placement
and obtain owner-selected fresh radio/portal and field evidence.
