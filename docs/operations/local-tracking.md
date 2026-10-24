# Permanent local tracking

Owner accepted the trial on 2026-10-23. `.scratch/TRACKER.md` is the single current task queue on `main`, with decisions/evidence in existing records. GitHub hosts source, CI and useful PRs; historical issues/Project remain unchanged. Automated GitHub tracking provisioning is disabled.

## Daily work

1. Check the branch and working tree. Pull the branch with `git pull --ff-only` when the tree is clean; preserve unrelated edits and concurrent worktrees.
2. Read the tracker and the newest session entry. Open the selected task's linked requirements or evidence as needed, rather than loading the entire project history. Work follows the owner's request and priority order: passive member GPS, communications, later law-enforcement expansion.
3. Do the authorized work. Keep measurements, decisions and procedures in their existing records. Use a short `session/machine; awaiting ...` note in Current only if another session could overlap; the solo workflow needs no separate claim ceremony.
4. At handoff, update the affected tracker entry with its remaining action, blocker and evidence link. Add a brief dated entry at the top of `records/sessions.md`, including validation and material limits. Move completed work out of the queue; its session/evidence record and Git history preserve the result.
5. Stage explicit coherent paths, commit and push to the matching branch on `origin`. Source publication alone does not deploy the portal or authorize hardware work. Application/firmware changes continue to use useful PRs and existing CI; documentation can be committed directly. Target ordinary project PRs at `main`.

No routine GitHub issue reads/writes or Project reconciliation are required. Existing issue numbers remain useful historical references, not a second status to maintain. Old log entries mentioning pending board synchronization describe the previous workflow and create no current task.

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
