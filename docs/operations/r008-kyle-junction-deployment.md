# R008 Kyle Junction deployment configuration

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
