# Working in SNORR MeshLink

## At the start of a session

Run `git status` before editing. Read `.scratch/TRACKER.md` and the newest entry in `records/sessions.md`; follow only the records relevant to the requested work. Read `PROJECT.md` for mission/constraints, `.scratch/pilot/map.md` for a pilot decision, and `CONTEXT.md` when interpreting project terminology. Older session entries and imported issue discussions are reference material, read when the current task needs them.

For task dispatch, concurrent workers or bench ownership, follow `docs/operations/local-tracking.md`. Use one bounded outcome per implementation assignment; `.scratch/tasks/` holds briefs, while the tracker alone owns status. Default to one implementation worker. Delegate independent work or review only when requested, and keep one session in control of a board/serial port or live mutation. For repeated local checks, use the documented scopes of `scripts/check-project.py`; hardware and deployment acceptance remain separate.

This repository is the durable project record. Preserve the user's priority order: passive member GPS tracking first, communications second, law enforcement expansion later. Keep planning simple and reuse inventoried hardware before proposing purchases.

## When doing work

- Board flashing or radio configuration: read `docs/operations/board-flashing-handoff.md` for board/source selection, preserved profiles, portal gaps and verification criteria. Routine RAK flashing downloads and verifies the pinned prerelease; rebuilding is a separate development task.
- Wishlist: read `records/wishlist.md` when capturing a wishlist request or discussing a related topic. Add the requested idea there and a short Deferred entry in `.scratch/TRACKER.md`. Mention relevant parked ideas when useful; mentioning or migrating one does not activate it. Research, design, implementation, and testing wait until the owner explicitly brings it forward.
- Inventory or hardware changes: update `records/inventory.md`; distinguish confirmed quantities, estimates, and unknowns.
- Spending, donations, or funding: update `records/finances.md` with dated amounts and evidence references. Never invent balances, prices, or donated values.
- Sites or backhaul: update `records/sites.md`; candidate locations are not permission to install.
- Field testing: use `records/field-results.md`; distinguish planned criteria from measured results.
- Social or grant work: use `records/content.md`; connect claims to recorded measurements and expenses.
- Application releases: follow `docs/operations/meshlink-releases.md`; `meshlink-release.json` owns the MeshLink version, independently of SNORR Firmware.
- Technical decisions: use `.scratch/pilot/` and `docs/research/`. Verify current technical and regulatory facts against primary sources. A private network or member consent does not settle radio compliance or publication permission.

Do not assume LoRaWAN, Meshtastic, and MeshCore are interchangeable. Keep firmware and protocol selection open until hardware and pilot requirements support a choice. Keep member GPS freshness, backhaul outages, and operation without a phone central to design.

## Progress tracking

Permanent local tracking was accepted on 2026-10-23. `.scratch/TRACKER.md` owns current work, next steps, verification and deferred ideas. Follow `docs/operations/local-tracking.md` when changing the workflow or resolving a tracking ambiguity. Update the relevant entry once at handoff with its next action and evidence link; completed work lives in the session log. Use a brief session/machine note only when concurrent work needs coordination. Historical GitHub issues and the Project board remain unchanged unless separately requested; routine issue searches, claims, label changes and board synchronization are unnecessary. Imported requirements are in `records/tracking-import/`, read only for the selected task. Keep decisions and measurements in their existing records; `.scratch/pilot/` preserves decision history. Resolve at most one non-research decision per Wayfinder session unless the user changes scope.

## Finishing a session

Update `records/sessions.md` with completed work, outstanding questions, and the next useful step. Commit coherent completed changes as requested by the user; stage explicit paths and preserve unrelated edits. Do not amend or rewrite existing history unless requested. Handoff changed behavior, checks/results and unverified gates, commit/branch and the next action.

The owner has authorized publishing project records to `git@github.com:lfg-seth/snorr-meshlink.git` (remote `origin`) and accepted permanent repository-local tracking on 2026-10-23. Keep this repository updated and push every completed commit to its corresponding branch on `origin`; report any failed push. Track `main` against `origin/main`; use short-lived branches for changes. The pre-acceptance main is preserved at `archive/pre-local-tracking-20261023`. Do not force-push or rewrite remote history without explicit authorization. Markdown owns task status and durable decision/evidence record; GitHub continues to host source, CI and useful PRs.

The owner explicitly authorized the Meshtastic firmware fork `git@github.com:lfg-seth/firmware.git` on 2026-10-16. Publish pilot firmware source on `snorr/develop` (owner-selected on 2026-10-23) and pin published commits through this repository's `firmware` submodule. Publishing source does not itself authorize flashing hardware.

Keep secrets, identifiable member rosters, and raw location tracks out of Git using `private/` or `local-data/`. Track sanitized summaries and evidence references. Publication to the GitHub repositories above is authorized; other publishing and external outreach require authorization.
