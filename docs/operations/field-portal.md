# Field portal and activity

The [November 15 site table](../../records/sites.md#2026-11-15---published-deployment-setup-and-fixed-locations)
owns the fixed locations. The portal and its activity sampler share
[the seven placements](../../portal/src/placements.json). Match physical radio IDs before
applying site names and map pins. The map shows saved field coordinates.
Shady Hollow records locally and has no scheduled backhaul, Wi-Fi or remote SD
watchdog. Ordinary radio observations can still arrive through another gateway.
The live registry continues to collect the full fleet. Users retains member
assignments. The public demo uses its separate synthetic database.

## Serving Activity

The portal serves the field dashboard from the Activity tab after live sign-in.
The existing [desktop dashboard](https://github.com/lfg-seth/snorr-meshlink/tree/8cfd518/scripts)
supplies the card layout, ordering, receipt highlights, health filters and
watchdog calculations. The portal polls every three seconds and keeps the last
cards visible on a disconnect.

Install the release's `scripts/portal-activity.py`, `scripts/watch-nodes.py`,
`scripts/server/node_readings.py`, `scripts/node-cadence.json` and
`portal/src/placements.json` under `/opt/meshlink` at the same relative paths.
Install [the service](../../deploy/portal/meshlink-activity.service) in
`/etc/systemd/system`, reload systemd, and enable and start
`meshlink-activity.service`. It reads the local live database in query-only
mode and atomically publishes the selected cards to
`/run/meshlink-activity/snapshot.json`. The existing live API checks the
account role before returning it. The demo API rejects this route.

After the [normal release checks](meshlink-releases.md), verify that the live
map and Infrastructure show six repeaters plus G002 and that Activity returns
the same seven physical IDs in roster order, including silent radios. Verify
fresh snapshot timestamps, demo isolation and an anonymous request denial.
For rollback, stop and disable the sampler and restore the previous application
and static build under the deployment lock. The release writes no roster or
telemetry migrations.
