# Local tracking trial

Authorized on 2026-10-21 for `trial/local-tracking`. This branch uses [the repository tracker](../../.scratch/TRACKER.md) as the single current queue. `main` retains the earlier GitHub workflow until the owner accepts the trial. GitHub still hosts source, CI and useful PRs. Issues and the Project board are preserved unchanged during the trial.

## Daily work

1. Check the branch and working tree. Pull the branch with `git pull --ff-only` when the tree is clean; preserve unrelated edits and concurrent worktrees.
2. Read the tracker and the newest session entry. Open the selected task's linked requirements or evidence as needed, rather than loading the entire project history. Work follows the owner's request and priority order: passive member GPS, communications, later law-enforcement expansion.
3. Do the authorized work. Keep measurements, decisions and procedures in their existing records. Use a short `session/machine; awaiting ...` note in Current only if another session could overlap; the solo workflow needs no separate claim ceremony.
4. At handoff, update the affected tracker entry with its remaining action, blocker and evidence link. Add a brief dated entry at the top of `records/sessions.md`, including validation and material limits. Move completed work out of the queue; its session/evidence record and Git history preserve the result.
5. Stage explicit coherent paths, commit and push to the matching branch on `origin`. Source publication alone does not deploy the portal or authorize hardware work. Application/firmware changes continue to use useful PRs and existing CI; documentation can be committed directly. During the trial, target trial-specific PRs at `trial/local-tracking` to keep the workflow out of `main` until accepted.

No routine GitHub issue reads/writes or Project reconciliation are required. Existing issue numbers remain useful historical references, not a second status to maintain. Old log entries mentioning pending board synchronization describe the previous workflow and create no trial task.

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

Imported deferred ideas and blocked work retain their holds. Importing an issue does not accept a design, authorize work, close it on GitHub or overwrite an active session. The existing neighbor-signal draft PR and firmware decisions remain separate from this tracking trial.

## Try, keep or roll back

The trial starts from `origin/main` commit `0713f7ea60d7bd839d246630655d6d9f70a736db`. The original desktop branch is `docs/telemetry-release-record` at the same baseline. Both remain available; this trial creates no archive, merge or deletion yet.

- **Try on another machine:** fetch `origin`, switch to `trial/local-tracking`, confirm it tracks `origin/trial/local-tracking`, and pull with `--ff-only`. Commit/push before switching machines. Keep credentials, databases and raw locations in ignored private storage with their separate backups.
- **Roll back the trial:** commit/push useful trial work, then switch to `main` in an available checkout. On this desktop, `main` is already checked out in another worktree; switching this checkout back to `docs/telemetry-release-record` restores the original baseline workflow. Keep the trial branch so its new records can be reconciled if needed. A branch switch changes repository instructions, not GitHub issue/Project state; these were left untouched. Any ordinary source changes made during the trial need their own normal merge/reconciliation.
- **Accept later:** after explicit owner acceptance, preserve the then-current pre-merge `main` commit with an archive branch or tag, reconcile any concurrent `main` work, and merge the trial normally into `main`. Keep `main` tracking `origin/main`; push both the archive reference and updated `main`. Retiring the old issues/board is a separate, explicit migration step after acceptance, using a final comparison for work added elsewhere during the trial.

Compare the number of tracking calls and amount of startup reading during actual tasks. No measured time, token or cost saving is claimed by this migration.
