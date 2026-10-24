# MeshLink application changelog

MeshLink versions cover portal and backend source together and are independent
of SNORR Firmware versions. The authoritative version is `meshlink-release.json`.

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
