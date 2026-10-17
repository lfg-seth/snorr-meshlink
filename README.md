# SNORR MeshLink

Search and Rescue Tracking & Communications

A project to equip SNORR members with passive GPS tracking and supporting communications for Search and Rescue on Mount Charleston, Nevada.

Priority order: member location awareness, member communications, and later support for law enforcement communications. Reuse existing hardware before buying more.

## Start here

- [Board flashing and configuration](docs/operations/board-flashing-handoff.md): new-chat entry point, pinned builds, preserved profiles, sensor wiring and portal verification gaps.
- [Local development](README.local.md): start commands, demo credentials, database dashboard and frontend builds.
- [Project brief](PROJECT.md): confirmed goals, constraints, and unresolved choices.
- [GitHub Issues](https://github.com/lfg-seth/snorr-meshlink/issues): current work, bugs, verification and deferred ideas.
- [Project board](https://github.com/users/lfg-seth/projects/2): owner-private status board and saved work/verification/bug/wishlist views.
- [Tracking workflow](docs/operations/github-tracking.md): status views, session handoffs and completion criteria.
- [Decision map](.scratch/pilot/map.md): historical pilot questions and durable decision answers.
- [Roadmap](docs/roadmap.md): checkpoints from inventory through deployment and reporting.
- [Protocol baseline](docs/research/protocol-baseline.md): official-source comparison of LoRaWAN, Meshtastic, and MeshCore; Meshtastic is selected for pilot evaluation, with hardware verification still pending.
- [Inventory](records/inventory.md): equipment on hand and its condition.
- [Finances](records/finances.md): expenses, contributions, receipts, and funding.
- [Candidate sites](records/sites.md): repeaters and possible internet backhaul.
- [Field results](records/field-results.md): test plans and measured outcomes.
- [Content and reporting](records/content.md): project documentation, social content, and grant evidence.
- [Session log](records/sessions.md): what changed and where to resume.
- [Portal development](portal/README.md): React/TypeScript/Vite commands and CI baseline; local synthetic development is separate from the hosted live service.

## Working rhythm

1. Add new facts to the relevant record, marking estimates and unknowns.
2. Read the relevant GitHub issue, check prerequisites and claim authorized work.
3. Record the decision and evidence in the repository; update the issue with status, validation and the next action.
4. Commit each completed, coherent project change with a descriptive message and push it to `origin`.

Current state (2026-10-17): two member trackers deliver bench GPS through two gateways to the deployed authenticated portal; RAK neighbor and signed sensor-power ingestion are deployed. Sustained GPS freshness/runtime, forced relaying, local viewing through outages, sensor accuracy and field readiness remain unverified. The planned six-member pilot is separate from confirmed available hardware. Positions become stale at 15 minutes; runtime minimum is four hours, with a 12-hour target. See the [roadmap](docs/roadmap.md) for evidence checkpoints and GitHub Issues for current work. Passive tracking remains first, communications second, law-enforcement expansion later.

Git history is the change record. The GitHub repository is [lfg-seth/snorr-meshlink](https://github.com/lfg-seth/snorr-meshlink), configured as `origin` using SSH. `main` tracks `origin/main`; push each completed commit. GitHub Issues owns current execution status; Markdown preserves durable decisions and measured evidence. Credentials and raw member location data belong in ignored `private/` or `local-data/`; keep summarized evidence and references here. Ignored operational data needs its own backup.
