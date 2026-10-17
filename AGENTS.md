# Working in SNORR MeshLink

## At the start of a session

Read `PROJECT.md`, `records/sessions.md`, and `.scratch/pilot/map.md`. Run `git status` before editing. Read `.scratch/TRACKER.md` and inspect relevant GitHub issues before choosing work. Read `CONTEXT.md` when interpreting project terminology.

This repository is the durable project record. Preserve the user's priority order: passive member GPS tracking first, communications second, law enforcement expansion later. Keep planning simple and reuse inventoried hardware before proposing purchases.

## When doing work

- Board flashing or radio configuration: read `docs/operations/board-flashing-handoff.md` for board/source selection, preserved profiles, portal gaps and verification criteria. Routine RAK flashing downloads and verifies the pinned prerelease; rebuilding is a separate development task.
- Wishlist: read `records/wishlist.md` when capturing a wishlist request or discussing a related topic. Capture requested ideas as deferred GitHub issues and link the durable wishlist record. Mention relevant parked ideas when useful; mentioning or migrating one does not activate it. Research, design, implementation, and testing wait until the owner explicitly brings it forward.
- Inventory or hardware changes: update `records/inventory.md`; distinguish confirmed quantities, estimates, and unknowns.
- Spending, donations, or funding: update `records/finances.md` with dated amounts and evidence references. Never invent balances, prices, or donated values.
- Sites or backhaul: update `records/sites.md`; candidate locations are not permission to install.
- Field testing: use `records/field-results.md`; distinguish planned criteria from measured results.
- Social or grant work: use `records/content.md`; connect claims to recorded measurements and expenses.
- Technical decisions: use `.scratch/pilot/` and `docs/research/`. Verify current technical and regulatory facts against primary sources. A private network or member consent does not settle radio compliance or publication permission.

Do not assume LoRaWAN, Meshtastic, and MeshCore are interchangeable. Keep firmware and protocol selection open until hardware and pilot requirements support a choice. Keep member GPS freshness, backhaul outages, and operation without a phone central to design.

## Progress tracking

GitHub Issues owns current work status, bugs, verification follow-ups and deferred ideas. Follow `docs/operations/github-tracking.md` when creating, claiming, updating or closing work. Search before creating, claim authorized work before starting, and leave evidence and the next action at handoff. Use issue titles with links in conversation. Keep decision answers and measurements in the repository; `.scratch/pilot/` is the historical decision record, not a second active queue. Resolve at most one non-research decision per Wayfinder session unless the user changes scope.

## Finishing a session

Update `records/sessions.md` with completed work, outstanding questions, and the next useful step. Commit coherent completed changes as requested by the user; stage explicit paths and preserve unrelated edits. Do not amend or rewrite existing history unless requested. Report the commit and material verification limits.

The owner has authorized publishing project records to `git@github.com:lfg-seth/snorr-meshlink.git` (remote `origin`) and migrated progress tracking to GitHub on 2026-10-17. Keep this repository updated and push every completed commit to its corresponding branch on `origin`; report any failed push. Track `main` against `origin/main`. Do not force-push or rewrite remote history without explicit authorization. Markdown remains the durable decision/evidence record; link it from GitHub issues.

The owner explicitly authorized the Meshtastic firmware fork `git@github.com:lfg-seth/firmware.git` on 2026-10-16. Publish pilot firmware source on its existing `snorr/rak-survey` branch and pin published commits through this repository's `firmware` submodule. Publishing source does not itself authorize flashing hardware.

Keep secrets, identifiable member rosters, and raw location tracks out of Git using `private/` or `local-data/`. Track sanitized summaries and evidence references. Publication to the GitHub repositories above is authorized; other publishing and external outreach require authorization.
