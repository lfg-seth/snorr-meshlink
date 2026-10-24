# R004 obsolete channel 3 cleanup - 2026-10-24

The owner requests purging the wrong readings after R004's battery card reports
`No unambiguous current source`. The deployed selector finds both fresh INA219
channel 1 and historical channel 3 current values in the device's readings.
The four channel 3 observations were received on October 17 UTC (October 16
Pacific); no current channel 3 telemetry is present.

## Completed scope

At **12:47 Pacific**, acquire `/run/lock/meshlink-deploy.lock` after the concurrent
backup/recovery operation releases it. Briefly stop the live worker and API,
take and integrity-check a consistent private SQLite backup, then transactionally:

- Delete exactly four R004 observations containing only `power3CurrentMa` and
  `power3Voltage`.
- Remove those two metrics from R004's cached device readings.
- Preserve all remaining R004 readings, device configuration and identities,
  other devices, history, receptions and raw MQTT archive. Leave demo state,
  application source and radio configuration unchanged.

Private rollback/evidence directory:
`/var/lib/meshlink/private-telemetry-cleanups/r004-channel3-20261024T194712Z/`.
It contains `before.db`, the removed observations/cache values in
`purged-records.json`, transaction summary and authenticated verification.
Historical raw envelopes remain archival evidence; this cleanup does not replay
them or introduce an ingestion filter.

## Verification

Before committing, compare protected-state SHA-256 digests for all **29** user
tables, excluding only the four selected observation rows and two selected
cached metrics. Every digest matches. SQLite integrity passes before/after.
The live API and worker restart successfully. An immediate API read encounters
the startup interval; a separate read after startup verifies the committed
result without repeating the purge.

At **12:47:24 Pacific**, authenticated state contains only channel 1 among R004
power-current channels, satisfying the deployed card's single-source selection.
It reports **+237.6 mA** in the portal's positive-charging convention (raw
**-237.6 mA**), measured **12:46:13**, and battery **3.654 V**. No channel 3
observation or cached metric remains. Both services are active.

This removes the stale-channel ambiguity. It does not establish sensor accuracy,
physical current direction, battery accounting or runtime. Existing INA219
calibration/field gates remain open. Future raw archive replay could restore
these historical fields unless separately filtered; no such replay is performed.
