# MeshLink application changelog

MeshLink versions cover portal and backend source together and are independent
of SNORR Firmware versions. The authoritative version is `meshlink-release.json`.

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
