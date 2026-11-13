# Current deployment node labels

## Fresh numbering - 2026-11-12

The owner restarts **all repeater/gateway labels** for the Sunday deployment.
This roster owns the new physical-device mapping. Older R/G assignments,
saved locations and number-based provisioning profiles are historical inputs,
not a way to select or configure these newly numbered units. Preserve each
physical radio's own identity/keys. Member-node labels were not reset.

**Bench policy: CLIENT for every prepared board.** The owner reserves the
selected repeaters' ROUTER switch for final placement Sunday; verify cadence
and full profile after that switch. [Batch label station](../docs/operations/rak-batch-station.md).

Only identified units accepted below belong to this new roster; do not infer
additional units or gateway assignments from the old R001-R006/G001-G006 lists.
Portal registry/history has not been reassigned by this board-preparation step.

| Fresh label / radio name | Physical identity | Assembly | Firmware / completed bench scope | Remaining deployment setup |
| --- | --- | --- | --- | --- |
| **R001 / SNORR Repeater 001** | USB **E93C5FF0F97DD76B**; radio **!f95b5501**; hardware **6bd77df9f05f3ce901555bf96d5ed7fc** | Owner-confirmed **RAK19007**, RAK4631 core, INA219 and AHT21 | Retained **2.7.26.4c96b9b**, **CLIENT**; device/environment/power 180 s, saved-baseline SNNS; full reboot/profile and both sensor readings pass; final CLIENT paced RF TX/RX **3/3 each**. [Evidence](../docs/operations/r001-commissioning-20261112.md). | Case, battery/solar, actual location and final ROUTER switch selected by owner Sunday; old fixed location cleared. Recheck reporting cadence after switching role. Forced relay/end-to-end field acceptance separate. |

Physical tag: **R001**. Match USB suffix **D76B** when distinguishing it from
the temporary reference. Next repeater label is **R002** after identifying that
physical board independently. No fresh gateway number is assigned here.

## Bench reference - excluded from deployment numbering

**REF1 / SNORR RF Reference**: USB **70DF102F58D2A034**, radio **!8737c2c9**,
hardware **34a0d2582f10df70c9c237879e77e47a**. Owner explicitly authorizes a
full factory reset without an old-settings backup. Retains compatible
**2.7.15.567b8ea**, generates its own distinct keys, and has a reboot-verified
CLIENT/no-rebroadcast, zero-hop, US/LONG_FAST/slot-35/10 dBm private reference
profile. It is ready to remain connected for subsequent paired checks; it is
not a numbered deployment repeater or gateway. V4/SD work stays with its other
chat; this session never opens COM31.
