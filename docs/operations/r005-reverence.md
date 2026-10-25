# R005 Reverence placement — 2026-10-25

Owner requests **R005 `!f95b5501`** at supplied private coordinates, named
**Reverence** in Meshtastic and the database/portal, preserving short name
**R005**, with ROUTER, fixed position and B002 admin enrollment using the
[prepared script](repeater-role-change.md). No firmware update requested.

## Database and portal

Completed: replace the previous display name Showgirl with Reverence, save
the exact supplied latitude/longitude and owner-supplied location provenance.
The R005 record identity, number, short name, equipment and reporting settings
are preserved. Every other device's identity/configuration remains unchanged.
Authenticated live portal state includes Reverence. This verifies saved portal
metadata, not a newly received radio position or field coverage.

Private audit: `/root/r005-reverence-20261025T191836Z/` on the portal host,
including consistent SQLite backup, intended/before/after records and
authenticated portal state. Full pre-change backup
`meshlink-20261025T191836Z.tar.gz`, SHA256
`9a5db8584be9c3d54ef38a431465d1a402ec25e4f3c699a64225d98a29e868c7`.
Backup archive hash verified before mutation. Coordinates remain private.

## Radio access and remaining acceptance

Host USB enumeration matches recorded R005 serial **E93C5FF0F97DD76B** at
`/dev/ttyACM1`. The read-only script attempt stops at serial open with Linux
`PermissionError`, before reading or writing configuration. Evidence:
`private/bench/R005-role-20261025T191749590482Z/failure.log`.
No radio configuration or firmware change has occurred in this attempt.

Next: owner grants this account serial access; run the prepared script's
read-only backup, then `--apply` with the supplied coordinates. Independently
save Reverence as the long name, preserving R005 and all other owner/security
fields, and compare the full profile and coordinates through reboot. Verify
fresh gateway/portal delivery separately. Physical placement is owner-reported;
installation completion, RF coverage, forced relaying and runtime are unmeasured.
