# SNORR MeshLink

Search and Rescue Tracking & Communications

A project to equip SNORR members with passive GPS tracking and supporting communications for Search and Rescue on Mount Charleston, Nevada.

Priority order: member location awareness, member communications, and later support for law enforcement communications. Reuse existing hardware before buying more.

## Start here

- [Board flashing and configuration](docs/operations/board-flashing-handoff.md): new-chat entry point, pinned builds, preserved profiles, sensor wiring and portal verification gaps.
- [Local development](README.local.md): start commands, demo credentials, database dashboard and frontend builds.
- [Project brief](PROJECT.md): confirmed goals, constraints, and unresolved choices.
- [Wayfinder map](.scratch/pilot/map.md): decisions needed to reach a small field pilot.
- [Roadmap](docs/roadmap.md): checkpoints from inventory through deployment and reporting.
- [Protocol baseline](docs/research/protocol-baseline.md): official-source comparison of LoRaWAN, Meshtastic, and MeshCore; Meshtastic is selected for pilot evaluation, with hardware verification still pending.
- [Inventory](records/inventory.md): equipment on hand and its condition.
- [Finances](records/finances.md): expenses, contributions, receipts, and funding.
- [Candidate sites](records/sites.md): repeaters and possible internet backhaul.
- [Field results](records/field-results.md): test plans and measured outcomes.
- [Content and reporting](records/content.md): project documentation, social content, and grant evidence.
- [Session log](records/sessions.md): what changed and where to resume.
- [Portal development](portal/README.md): local React/TypeScript/Vite commands and CI baseline; currently synthetic data only.

## Working rhythm

1. Add new facts to the relevant record, marking estimates and unknowns.
2. Work the next unblocked decision in the Wayfinder map.
3. Record the decision and any evidence; update the affected records.
4. Commit each completed, coherent project change with a descriptive message and push it to `origin`.

Current state: planning for 6 GPS-equipped Heltec V4 member trackers, 2 owned RAK relays, and 2 owned V3 backhauls. Positions become stale at 15 minutes; member runtime must reach 4 hours, with a 12-hour target. Meshtastic is the pilot evaluation baseline. Tracking, future SOS, dispatch portal and infrastructure-warning requirements are recorded; hardware identification, bench tests and implementation remain outstanding. Planned purchases and recoveries are separate from confirmed stock. See the project brief and session log for current details.

Git history is the change record. The GitHub repository is [lfg-seth/snorr-meshlink](https://github.com/lfg-seth/snorr-meshlink), configured as `origin` using SSH. `main` tracks `origin/main`; push each completed commit. The Markdown tracker is maintained locally and mirrored to GitHub with the project records. Credentials and raw member location data belong in ignored `private/` or `local-data/`; keep summarized evidence and references here. Ignored operational data needs its own backup.
