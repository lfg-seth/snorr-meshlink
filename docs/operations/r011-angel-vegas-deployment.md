# R011 Angel Peak Vegas-side deployment

**Later same-day update:** owner reuses R011 / Case 6 at
[Angel Peak Mountain Side](r011-angel-mountain-deployment.md), with a new
fixed pin and reboot-verified MQTT permission enabled. R005 remains Vegas Side.
The swap-time R011 state below is historical.

**Superseded later 2026-11-15:** owner replaces this assignment with
[R005](r005-angel-vegas-deployment.md) after the
[MQTT-permission diagnosis](r011-telemetry-diagnosis.md). R011 is not repaired
or reset by that swap; the original configuration evidence below is historical.

Owner selects **Angel Peak Vegas Side**, **R011**, **Case 6**, **eight cells**
and **Muzi antenna** on 2026-11-15, then supplies the exact fixed coordinates.
Exact coordinates and raw profiles remain private.

## Identity and intended configuration

USB **70DF102F58D2A034**, radio **!8737c2c9**, hardware
**34a0d2582f10df70c9c237879e77e47a**, RAK4631, former REF1.
Live backup confirms retained **2.7.26.bcb22e0 / rak4631-survey**.
**No flash, rebuild, reset, key replacement or portal change.**

The former reference profile is CLIENT, rebroadcast NONE, hop limit zero,
3,600-second device telemetry, disabled environmental/power measurement and
no enabled NeighborInfo. It already has the same private primary channel
name/key as deployment R008. The ordinary deployment step must therefore
replace these reference restrictions, rather than only switch the role.

Set ROUTER and exact fixed position (integer degrees × 10^7; existing altitude
or unspecified, without inventing elevation). Apply **LOCAL_ONLY**, **hop 3**,
enabled device/environment/power measurement at **180 seconds**, enabled
NeighborInfo over LoRa at **21,600 seconds** and saved-baseline SNNS. Reassert
affected sections after firmware installs role defaults, as with
[R001](r001-cathedral-deployment.md). Preserve original identity, names,
individual PKI/admin allowlist, channel bytes, US/LongFast slot 35, TX enabled
at 10 dBm, other radio/network/Bluetooth and disabled power saving. Retain
this board's **900-second smart position** cadence and GPS mode/pins/settings.
Accept ROUTER's `isUnmessagable=true` owner flag and role-derived API sleep
value of 86,400 seconds; power saving stays disabled.

Private before/intended/readback snapshots, local SDK commands and serial logs
are under `private/bench/R011-deploy-20261115/`. The worker acquires the station
lease and validates USB/radio/hardware identity before any write. Complete
intended local/module/channel bytes, metadata/owner/identity and exact fixed
coordinates pass independent comparison **before and after explicit reboot**.
The first verification connection hits USB I/O errors; a read-only retry passes
and issues the one explicit reboot. Final post-reboot verification passes after
a settling wait. No configuration or reboot is repeated. Serial is closed;
these observations do not establish sustained USB stability. The dashboard
monitoring baseline now includes R011 with its saved intervals.

## Equipment and remaining evidence

Case 6 intake is **v4 ASA**, **one SMA port**, **two 200 mA panels** and **two
four-cell parallel holders**. Owner supplies case/eight cells/Muzi allocation;
no new purchase or cell-capacity, inter-holder-wiring, antenna-gain or solar
output measurement is inferred. All deployment RAKs have INA219 per owner;
R011's actual local INA219/AHT21 readings remain unverified in this assignment.
Enabling measurement does not prove fitted sensor function.

Saved intervals do not establish actual RF cadence. No ping, RF/MQTT/portal,
forced-relay, physical-mount, sustained coverage or battery-only runtime
acceptance is part of this configuration. B003 is not attached in the USB
inventory. Survey PINGs can renew the retained 900-second autonomous-report
quiet window. Next: owner-selected B003 ping, fresh sensor/telemetry delivery
and field placement/acceptance.
