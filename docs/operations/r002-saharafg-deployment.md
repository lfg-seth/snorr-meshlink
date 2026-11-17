# R002 SaharaFG configuration - 2026-11-17

Owner selects **SaharaFG / R002 / Case 11 / four 18650 cells / no solar /
fiberglass antenna** at **36.1465262259956, -115.11054976227331**. This records
configuration and assembly selection. The owner explicitly selects **CLIENT**
for a planned nearby comparison with **R009 / Sahara / Muzi antenna**. Physical
installation and measured antenna differences remain unverified.

## Identity and saved configuration

USB **397EBE4F36E1F126**, radio **!05237743** and hardware
`26f1e1364fbe7e3943772305d079efb7` independently identify the connected RAK4631
on COM14. Retain **rak4631-survey / 2.7.26.bcb22e0** without flashing or
replacing keys. Save **CLIENT**, fixed position **36.1465262, -115.1105498**
at radio precision and retain enabled **OK to MQTT**. No altitude was supplied
or invented.

Preserve radio names **SNORR Repeater 002 / R002**, individual identity/admin
keys and private channel, US/LongFast slot 35, TX 10 dBm, hop 3, LOCAL_ONLY,
ignore-MQTT, disabled power saving and existing network/Bluetooth settings.
Device/environment/power reporting remains enabled at **180 seconds**;
over-LoRa SNNS retains its saved device-report baseline and standard NeighborInfo
remains enabled at **21,600 seconds**. Position broadcast remains **21,600
seconds**; existing GPS settings are preserved. The fixed pin is owner supplied,
not a measured GNSS fix. INA219 is owner-confirmed and AHT21 was detected in
the earlier [batch acceptance](rak-batch-20261112.md); no new sensor calibration
or RF measurement is claimed.

An initial ROUTER step was superseded by the owner's CLIENT correction before
handoff. Restore CLIENT, its **300-second sleep-interval default** with power
saving disabled, and messaging availability. The intermediate role had installed
CORE_PORTNUMS_ONLY and reporting defaults; final LOCAL_ONLY,
device/environment/power and NeighborInfo settings match the original profile.

## Verification and equipment limits

The label watcher was stopped; the station OS lease guarded serial access.
The sandbox denied the first serial open before a profile read or write;
normal device access succeeded. Complete local/module/channel bytes,
owner/security/hardware identity, firmware metadata and exact integer coordinates
**361465262 / -1151105498** pass independent readback before and after an explicit
reboot. Final CLIENT role, restored messaging availability, individual identity,
keys and names are verified. **Serial is closed; ready to unplug.**

Complete backups, intended profiles, readbacks and serial evidence remain ignored
under `private/bench/r002-saharafg-20261117/`. They are local evidence references,
not committed credentials or public artifacts.

Case 11 intake records **v4 ASA / one SMA and one Type N port / no fitted panels /
two four-cell parallel holders**. The selected build uses **four cells and no
solar**, despite the case having eight holder slots. Cell capacity, actual wiring,
fiberglass antenna model/gain and mount details remain unmeasured. No purchase,
stock recount or installation is inferred.

Next: confirm placement near R009 and collect comparable signal observations;
record test conditions before drawing conclusions about the antennas. Sustained
cadence, forced-relay/coverage and battery-only runtime remain separate gates.

## Live portal and Activity roster

Owner subsequently requests the live roster update. At **18:41:35 UTC**,
update only existing R002 device record **8jx8c4mp7d5tzxp**, retaining its
physical identity, telemetry history and monitoring configuration. Save
**SaharaFG**, the exact owner-supplied pin, **Case 11 / four 18650 cells /
Fiberglass / No solar**. Solar equipment stays false. Add field-roster record
**4itwmbz7evwf24c** for **!05237743 / R002**, adjacent to R009 in the fixed-site
order. Existing device configurations and eleven roster rows compare unchanged.

The deployment lock serialized this edit after another server operation.
The Activity publisher picked up the added row without a restart by this task.
Authenticated portal state and Activity verify **12 roster entries/cards**;
the released placement selector verifies **11 fixed pins**, including SaharaFG's
exact coordinates and equipment. The released Activity renderer verifies one
SaharaFG card, its timers and stable card identity through refresh. All seven
services are active; anonymous Activity remains **401**. Final checks used the
then-current **MeshLink 0.4.14 / 095c2c9305b71074c2285715398e1b6aae7386ea**;
this task changed runtime data, not application source or firmware. R002's live
last-contact value advanced to **2026-11-17T18:41:58.358Z**. This is reception
evidence, not an antenna comparison or sustained field acceptance.

Before editing, a transaction-consistent online SQLite backup passed
`PRAGMA integrity_check`. Private backup:
`/root/r002-saharafg-20261117/before-data.db`, SHA-256
`09142ae02f67dc71b884633aa6af0d8c36f3e813f779cb56430728c59c56ad1e`.
Before/intended/after device and roster JSON plus verification summaries remain
in that root-private directory. For a targeted rollback, restore the saved
R002 configuration through the private API and remove only its added roster row;
preserve telemetry history and other rows.

Native handset appearance, physical placement and matched fiberglass/Muzi
observations remain to verify.
