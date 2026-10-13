# SnorrMesh

A project to equip SNORR members with passive GPS tracking and supporting communications for Search and Rescue on Mount Charleston, Nevada.

Priority order: member location awareness, member communications, and later support for law enforcement communications. Reuse existing hardware before buying more.

## Start here

- [Project brief](PROJECT.md): confirmed goals, constraints, and unresolved choices.
- [Wayfinder map](.scratch/pilot/map.md): decisions needed to reach a small field pilot.
- [Roadmap](docs/roadmap.md): checkpoints from inventory through deployment and reporting.
- [Protocol baseline](docs/research/protocol-baseline.md): official-source comparison of LoRaWAN, Meshtastic, and MeshCore; no firmware selected yet.
- [Inventory](records/inventory.md): equipment on hand and its condition.
- [Finances](records/finances.md): expenses, contributions, receipts, and funding.
- [Candidate sites](records/sites.md): repeaters and possible internet backhaul.
- [Field results](records/field-results.md): test plans and measured outcomes.
- [Content and reporting](records/content.md): project documentation, social content, and grant evidence.
- [Session log](records/sessions.md): what changed and where to resume.

## Working rhythm

1. Add new facts to the relevant record, marking estimates and unknowns.
2. Work the next unblocked decision in the Wayfinder map.
3. Record the decision and any evidence; update the affected records.
4. Commit each completed, coherent project change with a descriptive message.

Current state: project initialized on 2026-10-12. Start with as few as 5 trackers toward roughly 20, with a tentative 5–15 minute GPS target. The owner's historical purchase CSV is imported; current stock and precise field criteria are still open. No firmware, deployment, new purchases, or site permissions have been selected or completed.

Git history is the change record. No remote repository is configured yet. Credentials and raw member location data belong in ignored `private/` or `local-data/`; keep summarized evidence and references here. Git history alone is not an off-device backup.
