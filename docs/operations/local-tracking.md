# Permanent local tracking

Owner accepted the trial on 2026-10-23. `.scratch/TRACKER.md` is the single current task queue on `main`, with decisions/evidence in existing records. GitHub hosts source, CI and useful PRs; historical issues/Project remain unchanged. Automated GitHub tracking provisioning is disabled.

## Daily work

1. Check the branch and working tree. Pull the branch with `git pull --ff-only` when the tree is clean; preserve unrelated edits and concurrent worktrees.
2. Read the tracker and the newest session entry. Open the selected task's linked requirements or evidence as needed, rather than loading the entire project history. Work follows the owner's request and priority order: passive member GPS, communications, later law-enforcement expansion.
3. Select one bounded outcome using the dispatch rules below. Complete the authorized implementation and appropriate checks; keep measurements, decisions and procedures in their existing records. Continue independent work when access or hardware blocks a separate verification step.
4. At handoff, update the affected tracker entry with its remaining action, blocker and evidence link. Add a brief dated entry at the top of `records/sessions.md`, including validation and material limits. Move completed work out of the queue; its session/evidence record and Git history preserve the result.
5. Stage explicit coherent paths, commit and push to the matching branch on `origin`. Source publication alone does not deploy the portal or authorize hardware work. Application/firmware changes continue to use useful PRs and existing CI; documentation can be committed directly. Target ordinary project PRs at `main`.

No routine GitHub issue reads/writes or Project reconciliation are required. Existing issue numbers remain useful historical references, not a second status to maintain. Old log entries mentioning pending board synchronization describe the previous workflow and create no current task.

## Task dispatch and context

Use one coordination thread to select priorities, resolve material choices and
review handoffs. Each implementation assignment gets one observable outcome,
its canonical requirements, write scope, prerequisites, verification and finish
authority. Use [the assignment template](task-template.md) when those details do
not fit the request or existing ticket; store briefs under `.scratch/tasks/`.
Briefs and parent execution tables describe scope, not a second status queue.

Default to one implementation assignment at a time. Split large readiness
tickets at independently verifiable outcomes: code/tests, release publication,
selected-board readback, live receipts and sustained/field acceptance. Parent
criteria remain authoritative; finishing a step cannot waive a later gate.
Record a brief's unresolved prerequisite in its tracker row and continue work
that does not depend on it. Preparing a task does not activate deferred work.

Read the tracker/newest handoff, then only the selected brief, its requirements
section and evidence needed for that outcome. Use `PROJECT.md` for enduring
direction. Historical brief/session/import files are consulted when a specific
question needs them. Link canonical facts and evidence rather than copying
histories or command output into startup documents. Keep the existing glossary
for domain language; task and measurement details stay in their own records.

## Software and bench work

The tracker uses **Software** and **Bench** lanes within its existing sections.
Keep an executable software outcome and a bench preparation/run available when
their prerequisites permit. Plan preparation can proceed without attached
hardware; running the plan needs the agreed devices, criteria and access.
These lanes are work types, not separate queues or new authorization.

Batch hands-on work into a bench session with identified devices, available
time, agreed measurements and private evidence destinations. One session owns
each board, serial port, transmitting controller and intentional live-service
mutation. When sessions could overlap, add a short owner/machine/resource note
to the affected Current row and clear it on handoff. Close serial handles before
handing a board to another session. Board preparation follows the
[flashing handoff](board-flashing-handoff.md); application deployment follows
[release operations](meshlink-releases.md).

## Parallel work and review

Use subagents or additional tasks when the owner explicitly requests delegation,
independent review or parallel execution. Give each worker a bounded question,
inputs and expected result. Keep dependent steps with the implementation worker.
For independent source changes, use separate short-lived branches/checkouts and
name each worker's write scope; worktrees isolate files, not hardware or servers.
Coordinate shared interfaces and serialize overlapping edits. The implementation
owner integrates results and updates shared tracker/session files once at handoff.
Read-only reviewers return findings without competing edits to those records.

For substantial firmware, security or data changes, include an independent
review in the proposed assignment and request delegation if it is not already
authorized. Review a fixed commit/diff against its requirements; report concrete
findings and missing evidence. Review does not substitute for target builds,
live receipts or field measurements. Small documentation changes need ordinary
link/diff review, without a mandatory extra agent or approval ceremony.

## Repeatable checks

Run `python scripts/check-project.py --help` for local check scopes. The default
checks changed Markdown links and Git whitespace; it needs only Python and Git.
Use `--base origin/main` to check the whole working branch, including untracked
Markdown. Select `bench`, `firmware-release`, `portal` or `backend` explicitly
when those components change. The runner reuses their existing suites and never
installs dependencies, flashes boards or connects to production.

Prefer an existing verifier to another manual transcript. The updater already
compares complete intended profiles privately; firmware release tooling verifies
manifests/checksums. Reuse those paths and extend them only for demonstrated
gaps. Live receipt/cadence automation needs a selected assignment with a private
input contract and measurement criteria; local fixture suites do not establish
authenticated live delivery. See [check commands and limits](../../scripts/README.md).

## Completion and handoff

Finish authorized implementation, appropriate checks, records and source
publication before handing back the result. Use this compact handoff in the
session log and final report:

- Changed behavior or completed outcome, with its evidence link.
- Checks run and results; name unavailable inputs and unverified acceptance stages.
- Commit and branch, including push result.
- Next action, its prerequisite and who needs to supply it if applicable.

Keep source/build, release, deployment, board readback, live receipts, sustained
operation and field acceptance distinct. Move a completed software outcome out
of active work; retain its hardware/live follow-up explicitly in Next or Verify.
Use read-only status conversations without rewriting unchanged records.

## Tracker format

Keep one short entry per outcome, linking detailed acceptance criteria and evidence instead of copying them. Use four sections:

- **Current:** owner-selected work actively underway; leave empty when no task is underway.
- **Next:** available follow-ups or work awaiting a stated prerequisite. An entry is not blanket authorization to act.
- **Verify:** implementation/preparation exists, with a concrete remaining acceptance check.
- **Deferred:** owner-held ideas. Mentioning, importing, moving or unblocking an entry does not activate research, design, implementation or testing.

Preserve imported `GH-N` identifiers so old references remain traceable. For new work, use the next unused `LOCAL-N` identifier if a stable reference helps; a small task completed in the same session needs only the session record. Search this tracker before adding an entry. Write new wishlist details in `records/wishlist.md` and link a Deferred entry; create a separate task note only if its acceptance criteria cannot fit clearly in the entry or an existing record.

Completion means the task's scoped acceptance criteria pass. Separate source/build, deployment, radio readback, live receipts and field acceptance. If a separate test remains, leave a Verify entry with its evidence and next action. Record unknowns and failures plainly. Existing purchase, deployment, flashing, site, publication and outreach boundaries still apply.

## Imported work

The [one-time GitHub import](../../records/tracking-import/index.md) preserves every open issue's requirements, labels and discussion as of migration. The tracker carries the current local status; imported files are a historical baseline, read only when needed for that task. Existing durable records can supersede an older imported claim or acceptance checkbox when dated evidence supports it; preserve the explanation at handoff. Completed/closed issue history remains available on GitHub and is not loaded at startup.

Imported deferred ideas and blocked work retain their holds. Importing an issue does not accept a design, authorize work, close it on GitHub or overwrite an active session. The existing neighbor-signal draft PR and firmware decisions remain separate from local tracking.

## Acceptance and recovery

The trial started at `0713f7ea60d7bd839d246630655d6d9f70a736db`.
Owner acceptance on 2026-10-23 promotes the trial history into `main` with a
normal merge. Pre-acceptance `origin/main` is preserved on
`archive/pre-local-tracking-20261023`; the trial branch remains historical.
Fetched `origin/main` had no changes absent from the trial, so no concurrent
main work needed reconciliation. GitHub issue/board retirement remains a
separate request; imported evidence and all existing holds are preserved.

Other machines: fetch origin, preserve local changes, switch to main and pull
with `--ff-only`. Track main against origin/main. Firmware development follows
`snorr/develop`; initialize/update the pinned submodule rather than fetching its
latest branch head implicitly. Keep raw evidence and credentials private.

Recovery uses the archived reference for inspection and deliberate new commits;
do not reset published main or rewrite remote history. Restoring source does
not itself restore production application data or radio settings.
