# Working in SnorrMesh

## At the start of a session

Read `PROJECT.md`, `records/sessions.md`, and `.scratch/pilot/map.md`. Run `git status` before editing. Read `CONTEXT.md` when interpreting project terminology.

This repository is the durable project record. Preserve the user's priority order: passive member GPS tracking first, communications second, law enforcement expansion later. Keep planning simple and reuse inventoried hardware before proposing purchases.

## When doing work

- Inventory or hardware changes: update `records/inventory.md`; distinguish confirmed quantities, estimates, and unknowns.
- Spending, donations, or funding: update `records/finances.md` with dated amounts and evidence references. Never invent balances, prices, or donated values.
- Sites or backhaul: update `records/sites.md`; candidate locations are not permission to install.
- Field testing: use `records/field-results.md`; distinguish planned criteria from measured results.
- Social or grant work: use `records/content.md`; connect claims to recorded measurements and expenses.
- Technical decisions: use `.scratch/pilot/` and `docs/research/`. Verify current technical and regulatory facts against primary sources. A private network or member consent does not settle radio compliance or publication permission.

Do not assume LoRaWAN, Meshtastic, and MeshCore are interchangeable. Keep firmware and protocol selection open until hardware and pilot requirements support a choice. Keep member GPS freshness, backhaul outages, and operation without a phone central to design.

## Local tracker

Read `.scratch/TRACKER.md` before creating, claiming, blocking, or resolving tickets. Refer to tickets by their titles. Keep decisions in ticket answers; the map links to them. Resolve at most one non-research decision per Wayfinder session unless the user changes scope.

## Finishing a session

Update `records/sessions.md` with completed work, outstanding questions, and the next useful step. Commit coherent completed changes as requested by the user; stage explicit paths and preserve unrelated edits. Do not amend or rewrite existing history unless requested. Report the commit and material verification limits.

Keep secrets, identifiable member rosters, and raw location tracks out of Git using `private/` or `local-data/`. Track sanitized summaries and evidence references. The user has requested local setup; do not create a remote or publish content without authorization.
