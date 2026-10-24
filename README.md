# SNORR MeshLink

Search and Rescue Tracking & Communications

A project to equip SNORR members with passive GPS tracking and supporting communications for Search and Rescue on Mount Charleston, Nevada.

Priority order: member location awareness, member communications, and later support for law enforcement communications. Reuse existing hardware before buying more.

## Start here

- [Local tracker](.scratch/TRACKER.md): current work, next actions, verification and deferred ideas on `main`.
- [Latest session entry](records/sessions.md): the most recent handoff; read older entries when the task needs their history.
- [Board flashing and configuration](docs/operations/board-flashing-handoff.md): new-chat entry point, pinned builds, preserved profiles, sensor wiring and portal verification gaps.
- [Local development](README.local.md): start commands, demo credentials, database dashboard and frontend builds.
- [Project brief](PROJECT.md): mission, priorities and constraints; consult when choosing work or interpreting scope.
- [Tracking workflow](docs/operations/local-tracking.md): bounded assignments, software/bench lanes, concurrency and handoff.
- [Assignment template](docs/operations/task-template.md): outcome, scope, prerequisites and verification for a focused worker.
- [Repeatable checks](scripts/README.md): local documentation, updater, release-tooling and application checks.
- [Imported tracking history](records/tracking-import/index.md): preserved GitHub issue snapshots; existing issues and the Project board remain historical references.
- [Private monitoring](docs/operations/meshmonitor-lxc.md): internal MeshMonitor and the existing Grafana/Prometheus integration, credentials handoff, retention and recovery.
- [Decision map](.scratch/pilot/map.md): historical pilot questions and durable decision answers.
- [Roadmap](docs/roadmap.md): checkpoints from inventory through deployment and reporting.
- [Protocol baseline](docs/research/protocol-baseline.md): official-source comparison of LoRaWAN, Meshtastic, and MeshCore; Meshtastic is selected for pilot evaluation, with hardware verification still pending.
- [Inventory](records/inventory.md): equipment on hand and its condition.
- [Finances](records/finances.md): expenses, contributions, receipts, and funding.
- [Candidate sites](records/sites.md): repeaters and possible internet backhaul.
- [Field results](records/field-results.md): test plans and measured outcomes.
- [Content and reporting](records/content.md): project documentation, social content, and grant evidence.
- [Portal development](portal/README.md): React/TypeScript/Vite commands and CI baseline; local synthetic development is separate from the hosted live service.

## Working rhythm

1. Add new facts to the relevant record, marking estimates and unknowns.
2. Check the local tracker for the relevant task, prerequisites and owner authorization.
3. Record decisions and evidence in the relevant document; update the tracker when status or the next action changes, linking the evidence.
4. Commit each completed, coherent project change with a descriptive message and push it to `origin`.

Use the [local tracker](.scratch/TRACKER.md) for current status and the
[roadmap](docs/roadmap.md) for evidence checkpoints. The [project brief](PROJECT.md)
holds enduring requirements; dated development details remain in
[session history](records/sessions.md) and linked operations records.

Git history is the change record. The GitHub repository is [lfg-seth/snorr-meshlink](https://github.com/lfg-seth/snorr-meshlink), configured as `origin` using SSH. `main` tracks `origin/main`; push each completed commit to its corresponding branch. The local tracker permanently owns current execution status on `main`. Markdown preserves durable decisions and measured evidence. Credentials and raw member location data belong in ignored `private/` or `local-data/`; keep summarized evidence and references here. Ignored operational data needs its own backup.

## Releases and tracking

MeshLink application **0.1.0** is versioned independently of SNORR Firmware.
See [release operations](docs/operations/meshlink-releases.md),
[changelog](CHANGELOG.md) and [firmware releases](records/firmware-releases/README.md).
Builds emit `version.json` with source/version/compatibility metadata.
[Repository-local tracking](docs/operations/local-tracking.md) is permanent on
`main`; firmware source development uses `snorr/develop`.
