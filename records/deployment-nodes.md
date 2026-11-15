# Current deployment node labels

## Fresh numbering - 2026-11-12

The owner restarts **all repeater/gateway labels** for the Sunday deployment.
This roster owns the new physical-device mapping. Older R/G assignments,
saved locations and number-based provisioning profiles are historical inputs,
not a way to select or configure these newly numbered units. Preserve each
physical radio's own identity/keys. Member-node labels were not reset.

**Bench policy: CLIENT until the owner selects deployment.** R001 is selected
for Cathedral Rock and R008 for Kyle Junction on 2026-11-15;
[ROUTER R001](../docs/operations/r001-cathedral-deployment.md),
[ROUTER R008](../docs/operations/r008-kyle-junction-deployment.md). The owner reserves the
selected repeaters' ROUTER switch for final placement Sunday; verify cadence
and full profile after that switch. [Batch label station](../docs/operations/rak-batch-station.md).

Only identified units and explicit holds below belong to this new roster;
acceptance differs by row. Do not infer additional units or gateway assignments
from the old R001-R006/G001-G006 lists.
Portal registry/history has not been reassigned by this board-preparation step.

| Fresh label / radio name | Physical identity | Assembly | Firmware / completed bench scope | Remaining deployment setup |
| --- | --- | --- | --- | --- |
| **R001 / SNORR Repeater 001** | USB **E93C5FF0F97DD76B**; radio **!f95b5501**; hardware **6bd77df9f05f3ce901555bf96d5ed7fc** | Owner-confirmed **RAK19007**, RAK4631 core, INA219/AHT21; **Case 01, eight cells, Muzi antenna**, Cathedral Rock selected 2026-11-15 | Retained **2.7.26.bcb22e0 / rak4631-survey**; **ROUTER**, owner-supplied fixed coordinates and complete intended profile verified through reboot; device/environment/power **180 s**, saved-baseline SNNS retained. No flash. [Deployment configuration](../docs/operations/r001-cathedral-deployment.md); [earlier CLIENT bench](../docs/operations/r001-commissioning-20261112.md). | Confirm actual installation/mount; obtain fresh reporting and forced-relay/end-to-end field evidence. Saved cadence is not measured delivery/runtime. |
| **R002 / SNORR Repeater 002** | USB **397EBE4F36E1F126**; radio **!05237743**; hardware `26f1e1364fbe7e3943772305d079efb7` | RAK4631; INA219 owner-confirmed; AHT21 detected | **4c96b9b / CLIENT**, complete reboot/profile pass; RF **3/3 TX, 3/3 RX**; CH1 voltage/current received. Board bench pass; assembly/site pending. [Batch evidence](../docs/operations/rak-batch-20261112.md). | Owner's Sunday case/power/location/ROUTER + cadence readback; holds must clear first. |
| **R003 / SNORR Repeater 003** | USB **1E1F729F05162A2E**; radio **!b4d6bc9f**; hardware `2e2a16059f721f1e9fbcd6b4f61e1bbc` | RAK4631; INA219 CH1 received; AHT21 not detected/unverified | **4c96b9b / CLIENT**, complete profile pass. Known-good cable keeps the session alive but direct RF remains **0/3 TX, 0/3 RX**; USB-closed radio queries also give no matched reply. **HOLD**; cause unisolated. [Retest](../docs/operations/rak-repair-retest-20261112.md). | Owner explicitly sets aside; diagnosis parked. Keep out of accepted deployment pile. |
| **R004 / SNORR Repeater 004** | USB **BEF65915B4E4F06C**; radio **!49ac6d7f**; hardware `6cf0e4b41559f6be7f6dac493cfb81d1` | RAK4631; INA219 owner-confirmed; AHT21 not detected / unverified | **4c96b9b / CLIENT**, complete reboot/profile pass; RF **3/3 TX, 3/3 RX**; CH1 voltage/current received. Board bench pass; assembly/site pending. [Batch evidence](../docs/operations/rak-batch-20261112.md). | Owner's Sunday case/power/location/ROUTER + cadence readback; holds must clear first. |
| **R005 / SNORR Repeater 005** | USB **AA474A4710B85C2C**; radio **!a65601b3**; hardware `2c5cb810474a47aab30156a671567827` | RAK4631; INA219 owner-confirmed; AHT21 not detected / unverified | **4c96b9b / CLIENT**, complete reboot/profile pass; RF **3/3 TX, 3/3 RX**; CH1 voltage/current received. Board bench pass; assembly/site pending. [Batch evidence](../docs/operations/rak-batch-20261112.md). | Owner's Sunday case/power/location/ROUTER + cadence readback; holds must clear first. |
| **R006 / SNORR Repeater 006** | USB **76642362C6FCE382**; radio **!638b9515**; hardware `82e3fcc66223647615958b63dd296ca1` | RAK4631; INA219 owner-confirmed; AHT21 detected | **4c96b9b / CLIENT**, complete reboot/profile pass; RF **3/3 TX, 3/3 RX**; CH1 voltage/current received. Board bench pass; assembly/site pending. [Batch evidence](../docs/operations/rak-batch-20261112.md). | Owner's Sunday case/power/location/ROUTER + cadence readback; holds must clear first. |
| **R007 / SNORR Repeater 007** | USB **BADB1E79E9739FC4**; radio **!b456f760**; hardware `c49f73e9791edbba60f756b42c43bbf3` | RAK4631; INA219 owner-confirmed; AHT21 not detected / unverified | **4c96b9b / CLIENT**, complete reboot/profile pass; RF **3/3 TX, 3/3 RX**; CH1 voltage/current received. Board bench pass; assembly/site pending. [Batch evidence](../docs/operations/rak-batch-20261112.md). | Owner's Sunday case/power/location/ROUTER + cadence readback; holds must clear first. |
| **R008 / SNORR Repeater 008** | USB **F4D0968336047CA0**; radio **!120b04fd**; hardware `a07c04368396d0f4fd040b12638298d4` | RAK4631; INA219/AHT21 previously detected; owner selects **Case 8 / eight cells / Muzi**, **Kyle Junction**, 2026-11-15 | Retained **2.7.26.bcb22e0 / rak4631-survey**; **ROUTER**, fixed coordinates and preserved complete profile verified through reboot; device/environment/power **180 s**, saved-baseline SNNS. No flash. [Deployment configuration](../docs/operations/r008-kyle-junction-deployment.md); [prior RF/sensors](../docs/operations/rak-repair-retest-20261112.md). | Confirm installation/mount, fresh reporting and forced-relay/end-to-end coverage/runtime; saved cadence is not measured delivery. |
| **R009 / SNORR Repeater 009** | USB **E9B12C5CA98FBCB8**; radio **!da581e5f**; hardware `b8bc8fa95c2cb1e95f1e58dafebb06cc` | RAK4631; INA219 owner-confirmed; AHT21 not detected / unverified; owner-confirmed RAK12501 GNSS | **4c96b9b / CLIENT**, complete reboot/profile pass; RF **3/3 TX, 3/3 RX**; CH1 voltage/current received. Board bench pass; assembly/site pending. [Batch evidence](../docs/operations/rak-batch-20261112.md). | GPS already enabled; ordinary image supports L76K; fresh fix pending. [GPS check](../docs/operations/r009-gps-20261112.md). Sunday case/power/location/ROUTER + cadence readback. |
| **R010 / SNORR Repeater 010** | USB **820C9B4F0C2D7675**; radio **!77fdb9f1**; hardware `75762d0c4f9b0c82f1b9fd774661875b` | RAK4631; INA219 and AHT21 detected after owner solder rework | Retained **4c96b9b / CLIENT**; complete power-cycle profile/keys pass; INA219 CH1 and temperature/RH received; RF **3/3 TX, 3/3 RX**. Solder hold cleared. [Retest](../docs/operations/rak-repair-retest-20261112.md). | Owner selects Sunday case/power/location/ROUTER, then cadence readback and forced-relay/end-to-end acceptance. |
| **R011 / SNORR Repeater 011** | USB **70DF102F58D2A034**; radio **!8737c2c9**; hardware `34a0d2582f10df70c9c237879e77e47a` | RAK4631, formerly REF1. Sensors unverified for this assignment. | **rak4631-survey / 2.7.26.bcb22e0**, CLIENT, LongFast slot 35. New owner names, individual keys, channel and profile checked after reboot. The original automatic buzzer pin reads as GPIO 21 on this build. | Retains zero-hop/no-rebroadcast bench settings. Tester pairing verified after reboot. Over-the-air survey check pending. |

**Survey firmware update, 2026-11-14.** R001, R002 and R004 through R011 run `rak4631-survey / 2.7.26.bcb22e0` on LongFast slot 35. R004, R005 and R007 returned direct survey PONGs. R001, R002, R006, R008, R009, R010 and R011 received USB reboot and profile verification. All seven subsequently saved the original tester’s pairing and verified it after reboot. RF tests for these seven remain deferred. R009 retained enabled GPS at a 120-second interval. Earlier ordinary-image results in these rows remain historical. The Heltec tester (`2.7.26.7b766e6`) retained G002 and accepted the ten RAKs in one USB selection after reboot.

Prior ordinary-image board-level passes: **R001, R002, R004, R005, R006, R007, R008,
R009 and R010**. **R003 alone remains held** for radio/connection acceptance.
R008 is now configured and accepted; R010 passes after owner solder rework.
All eleven repeater numbers are assigned. The next unused number is **R012**.

## Former bench reference

Former **REF1 / SNORR RF Reference** (`!8737c2c9`) served on `2.7.15.567b8ea`.
On 2026-11-14 the owner reassigned that physical radio to **R011**. No replacement reference was designated.

## Gateway addition - 2026-11-14

Fresh **G002 / SNORR Pilot Gateway G002** is the screenless V4
**F8:5B:1B:BF:0A:B8 / !1bbf0ab8**, with INA219 and SD, published
**heltec-v4-sd-gateway-survey / 2.7.26.f6cdbeb**, CLIENT and G001-style
300-second settings. Full reboot/profile, peripherals, private uplink and
authenticated portal registration pass; existing survey tester is enrolled.
Old V3 !849ad7a0 retains its portal history as legacy-v3-849ad7a0.
Case/battery/solar/site, peer-gateway/outage and sustained/field acceptance
remain separate. [Measured evidence](../docs/operations/g002-screenless-gateway.md).

## Mobile gateway G003 - 2026-11-14

Fresh **G003 / SNORR Gateway G003** is Heltec V3 **!849ad7a0**, hardware
**47af7bdcb7950e6e07f8ef108ef19fab**, USB **0001** / COM6; former G002 V3.
Full no-backup erase and checked **heltec-v3-gateway / 2.7.26.6fea6aa**
factory/filesystem flash, new own keys and complete CLIENT/private pilot
profile through reboot pass. Supplied vehicle Wi-Fi saved; mobile/no fixed
position, external sensors unconfirmed/disabled. Association/direct uplink
and vehicle runtime untested; portal unchanged at owner request.
[Evidence](../docs/operations/g003-mobile-gateway.md).
