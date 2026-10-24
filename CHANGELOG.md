# MeshLink application changelog

MeshLink versions cover portal and backend source together and are independent
of SNORR Firmware versions. The authoritative version is `meshlink-release.json`.

## 0.1.4 - 2026-10-24

Add INA219 sensor-path current history and a separate average of unique readings
in the latest 30 minutes to equipped device cards and Infrastructure detail.
Current and battery-voltage graphs both gain 30-minute and six-hour ranges.
Retain the existing periods, signed/zero current, source selection, timestamp
provenance and gaps for missing reports. Empty, ambiguous, incomplete or expired
averages remain Unknown.

Compatibility: existing Meshtastic telemetry, SNNS v1 and gateway-health v1.
Read existing observations with the established positive-charging API convention;
no firmware change, schema migration, data rewrite or configuration update.
The average is a sample mean, not a time-weighted estimate across missing data.
Rollback restores the previous matching backend/portal/root release metadata
from the verified backup. Calibration, whole-battery accounting and native
owner-phone acceptance remain separate gates. Manual deployment is selected
by the owner for PR #64.

## 0.1.3 - 2026-10-24

Add private SNGH v1 gateway health reports, independently of SNNS neighbor
changes. Display Wi-Fi/MQTT state and fresh radio receipt through another
gateway, with persistent backhaul outage/recovery warnings. Expire cached
badges and reject delayed, duplicate, retired-boot and unordered recovery.

Compatibility: existing Meshtastic telemetry and SNNS v1 remain supported.
Gateway health requires the matching SNORR gateway firmware and enabled private
LoRa reporting. No schema migration; health history uses existing observations.
Unknown/future source clocks cannot establish current health or clear warnings.
Reporting follows the saved device interval, with a 180-second minimum, jitter
and airtime admission. MQTT connection state is device-reported, not proof of
end-to-end application delivery. Rollback restores the matching backend and
portal from the pre-deployment backup; old firmware ignores the new feature.
Hardware calibration, sustained reconnect/runtime and field acceptance remain
separate from this bench rollout.

## 0.1.2 - 2026-10-24

Consolidate device-card battery presentation (LOCAL-8, PR #60). Member,
repeater/router and gateway details show one top summary of estimated battery
percentage, device voltage, charging/discharging state and current. Remove the
entire sensor-power section and duplicate current readings. Member GPS quality
sits beside percentage; preserve the battery icon, environment readings,
history/graphs and configuration controls.

Compatibility: existing Meshtastic telemetry and SNNS v1. Reuse existing battery
profiles and the 0.1.1 normalized-current convention. Measured current identifies
its sensor path and requires the explicit polarity marker for direction;
voltage-trend direction remains an estimate. Missing/ambiguous sources remain
unknown, with independent battery/current freshness. No migration, ingestion,
stored-history, radio or live-configuration change is required.

Rollback: restore the previous matching portal source/build and root release
metadata using the verified backup procedure. Backend behavior and schema are
unchanged. Calibration, whole-battery accounting and owner-phone acceptance
remain separate gates. Deployment follows the selected manual release procedure.

## 0.1.1 - 2026-10-24

Correct fleet sensor-current polarity in the authenticated API and portal.
All environment and PowerMetrics channels now use positive for charging and
negative for discharging, following owner-confirmed common wiring: R002/R004/
R006 charge while G003 discharges. Previously the API passed through the
opposite sensor sign. Existing cached readings and new reports use the same
conversion once; API current readings retain `rawValue` and declare
`currentConvention: "positive-charging"`. Voltage, clocks and freshness are
unchanged. The portal explains the convention and shows explicit positive signs.

Compatibility: existing Meshtastic telemetry and SNNS v1; firmware is unchanged.
No schema migration, history rewrite or packet replay is required. MQTT bytes,
worker envelopes, queued packets, saved observations and latest-reading caches
retain their original sensor signs. Direct database consumers must apply the
documented conversion; API consumers must not invert it again. Calibration and
sensor-path versus whole-battery current remain separate questions.

Rollback: restore the matching previous backend hooks and portal build using
the normal verified backup procedure. Stored evidence needs no reverse migration.
Source publication does not deploy production; rollout remains manual.

## 0.1.0 - 2026-10-23

Initial application development release, recording existing GPS/member tracking,
battery/environment/power reporting, SNNS v1 neighbor ingestion and relative-age
expiry, separate demo/live data and authenticated portal behavior.

This release adds generated portal `version.json` and HTML version/source metadata,
plus build validation of package/lockfile/changelog/tag identity. The existing
cutover test now closes its SQLite inspection connection before cleanup, fixing
a repeatable Windows test failure. Repository-local
tracking is accepted as the permanent workflow. Firmware development moves to
`snorr/develop`; radio binaries and on-device profiles are unchanged.

Compatibility: existing Meshtastic telemetry and SNNS v1. No new SNNS timestamp
payload is introduced. Source clock loss retains the recorded receipt fallback;
unknown upstream neighbor delay is not resolved. Review LOCAL-3/LOCAL-4/LOCAL-6
for outstanding firmware and deployment gates.

No new database migration is introduced by the versioning change itself. The
release incorporates the trial's previously deployed neighbor-current-state
migration; upgrade existing installations using the established backup/migration
and recovery procedure. See `docs/operations/portal-lxc.md`. Rolling back to
older application/schema combinations requires their matching backup/recovery
procedure, not merely copying an old frontend.

Source publication/build validation is distinct from production deployment;
the running server is not upgraded by creating this release.
