# R009 Sahara configuration - 2026-11-17

## Portal and Activity update

Owner subsequently requests the live portal and Activity cards be updated.
**MeshLink 0.4.11 / fbf161aa7bc53fd9187174ffa929daea26a421c3** adds Sahara
to the shared placements. The live registry keeps R009's existing record ID
and radio identity, records the exact owner-supplied display pin, Case 12,
eight 18650 cells, Muzi and the inventoried panel description. Monitoring policy,
telemetry history and other device configurations are preserved. Installation
remains unverified; no new radio write was performed for this portal update.

The clean merged release passes **71 portal tests**, typecheck/live build,
**95 backend tests** and **44 dashboard tests** on the LXC. PR and main CI pass.
All ten files served over public HTTPS match the build. The live sampler and
released Activity renderer show **11 cards**, including **R009 / Sahara**;
all have readings and timers. Seven production services and a fresh MQTT
archive receipt pass. The receipt proves ingestion is running, not a new
Sahara radio reception. Handset visual acceptance remains separate.

Rollback files are under `/opt/meshlink-rollback-field-fbf161a`; R009's prior
configuration and private deployment evidence are in `/root/sahara-0411/`.
See the [session record](../../records/sessions.md) for backup/recovery results.

## Radio configuration and assembly selection

Owner selects **Sahara / R009 / Case 12 / eight 18650 cells / Muzi antenna**
at **36.14484090826288, -115.11061987480886**. This is configuration and
assembly selection; installation and field acceptance remain separate.

USB **E9B12C5CA98FBCB8**, radio **!da581e5f** and hardware
`b8bc8fa95c2cb1e95f1e58dafebb06cc` independently identify the connected RAK4631.
Retain **rak4631-survey / 2.7.26.bcb22e0** without flashing or replacing keys.
Set **ROUTER**, fixed position **36.1448409, -115.1106199** at radio precision,
and retain enabled **OK to MQTT**. No altitude was supplied or invented.

Preserve R009's own private channel, identity/admin keys, radio names
**SNORR Repeater 009 / R009**, US/LongFast slot 35, TX 10 dBm, hop 3,
LOCAL_ONLY, ignore-MQTT, disabled power saving and network/Bluetooth settings.
Keep device/environment/power reporting at **180 seconds**, existing SNNS
baseline and NeighborInfo settings. GPS remains **ENABLED**, receiver update
**120 seconds**, position broadcast **3,600 seconds**, smart reporting enabled,
flags **811**. The fixed pin is owner supplied, not a measured GNSS fix.

ROUTER initialization changes rebroadcast mode and screen timeout; restore the
intended complete profile and retain the role's 86,400-second API sleep default
with power saving disabled. Station OS lease guards serial access. Complete
before/intended/readback profiles and serial evidence stay ignored in
`private/bench/r009-sahara-20261117/`.

Complete intended local/module/channel bytes, owner/security identity, firmware
metadata and exact integer coordinates pass independent readback before and
after explicit reboot. ROUTER owner role/unmessagable flags and metadata role
are expected firmware changes. SDK close encountered its known already-closed
stream during the first reboot; subsequent verification handles only that
closed-stream condition and passes. Serial is closed; ready to unplug.

Case 12's historical intake records v4 PETG, one SMA port, two 160 mA panels
and two four-cell parallel holders. Eight cells and Muzi are owner selected;
cell capacity, antenna gain, actual wiring and panel output are unmeasured.
Fresh RF/MQTT/portal receipts, physical placement/mount, sustained cadence,
coverage/forced relay and battery/solar runtime remain unverified.
