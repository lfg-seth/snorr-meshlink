# Progress tracker

On 2026-10-17 the owner migrated the active work queue to [GitHub Issues](https://github.com/lfg-seth/snorr-meshlink/issues). Read [the GitHub tracking workflow](../docs/operations/github-tracking.md) before creating, claiming, blocking or closing work.

- GitHub issue state, status labels, assignees and dependencies own current execution status.
- `.scratch/pilot/issues/` preserves historical Wayfinder questions, discussion and decision answers. Existing `Status`, `Assignee` and `Blocked by` fields are migration-time snapshots, not the current frontier.
- The [pilot map](pilot/map.md) indexes durable decisions. Resolved questions remain resolved only within their stated scope; they do not establish implementation, deployment or field acceptance.
- The three formerly open tickets link to their successor GitHub issues. Keep later decision answers here when they extend those discussions, and link the answer from the GitHub issue.
- Put new work in GitHub. Create a repository decision note only when there is a durable decision to preserve; link it from the issue and map as appropriate.
- If GitHub is unavailable, record a dated pending update in `records/sessions.md`, identify the issue and reconcile on the next connected session. Keep deferred work parked while offline.

Historical format: one question per `.scratch/<effort>/issues/NN-title.md`; `Type: research|prototype|grilling|task`; `Status: open|claimed|resolved`; a session assignee; parent map; numbered blockers; discussion under `## Comments`; resolution under `## Answer`. Preserve useful history and refer to questions by title.
