# GitHub progress tracking

Adopted by the owner on 2026-10-17. [GitHub Issues](https://github.com/lfg-seth/snorr-meshlink/issues) owns the current work queue. Repository Markdown owns durable decisions, measured evidence and operating procedures. Keep one status in GitHub and link the supporting record instead of copying its history.

## Find work

- [Project board — All work](https://github.com/users/lfg-seth/projects/2/views/1) (owner-private)
- [Project — Current work](https://github.com/users/lfg-seth/projects/2/views/2)
- [Project — Verification](https://github.com/users/lfg-seth/projects/2/views/3)
- [Project — Bugs](https://github.com/users/lfg-seth/projects/2/views/4)
- [Project — Deferred wishlist](https://github.com/users/lfg-seth/projects/2/views/5)

The Project retains its default private visibility; repository issues remain public. The issue filters below work without Project access.

- [Ready and unblocked](https://github.com/lfg-seth/snorr-meshlink/issues?q=is%3Aissue%20is%3Aopen%20label%3Astatus%3Aready%20-label%3Ablocked)
- [In progress](https://github.com/lfg-seth/snorr-meshlink/issues?q=is%3Aissue%20is%3Aopen%20label%3Astatus%3Ain-progress)
- [Awaiting verification](https://github.com/lfg-seth/snorr-meshlink/issues?q=is%3Aissue%20is%3Aopen%20label%3Astatus%3Averify)
- [Bugs](https://github.com/lfg-seth/snorr-meshlink/issues?q=is%3Aissue%20is%3Aopen%20label%3Abug)
- [Deferred ideas](https://github.com/lfg-seth/snorr-meshlink/issues?q=is%3Aissue%20is%3Aopen%20label%3Astatus%3Adeferred)
- [Blocked work](https://github.com/lfg-seth/snorr-meshlink/issues?q=is%3Aissue%20is%3Aopen%20label%3Ablocked)
- [Milestones](https://github.com/lfg-seth/snorr-meshlink/milestones)

Choose work in the owner's order: passive member GPS tracking, communications, later law-enforcement expansion. High priority means important within that order, not permission to bypass it. Prefer existing hardware. A ready issue is a prepared next step, not blanket authorization for deployments, flashing, purchases or outreach.

## Status and labels

Each open issue has exactly one `status:*` label. Replace the old status label when transitioning; preserve its other labels. Closed issues have no `status:*` label: closed means Done, with a closure reason distinguishing completion from retirement or duplication.

| Status | Meaning |
| --- | --- |
| `status:triage` | Captured; scope, priority, prerequisites or acceptance criteria need review |
| `status:ready` | Bounded next step with acceptance criteria, subject to its stated authorization |
| `status:in-progress` | Claimed by a named session/person doing authorized work |
| `status:verify` | Implementation or preparation exists; specified acceptance checks remain |
| `status:deferred` | Parked; owner activation is required before research, design, implementation or testing |

Use one type (`bug`, `feature`, `task`, `research`, `field-test`), relevant `area:*` labels (`portal`, `firmware`, `hardware`, `backhaul`, `project`), and optionally `priority:high` or `priority:normal`. A `blocked` label supplements status: the issue body names the prerequisite issue(s) or external condition. An issue can be ready but blocked on access/hardware. Neither blocker removal nor milestone assignment activates a deferred issue.

Label names/colors and checkpoint definitions live in [tracking configuration](../../.github/tracking.json). The [Tracking setup workflow](../../.github/workflows/tracking-setup.yml) validates that configuration, provisions labels/milestones and applies the initial milestone mapping only to issues without a milestone. It uses the repository's built-in token with `issues: write`, no new credential or application deployment access. Rerunning setup deliberately reapplies that initial mapping to unassigned issues. It does not change work statuses, close issues or create a user Project.

## During a session

1. Read the startup records and relevant GitHub issues. Run `python3 scripts/github/sync-project.py --apply` when CLI Project access is available to reconcile the board. Search for existing work before creating an issue. Check blockers, owner holds and another session's claim; preserve unfinished local edits.
2. Capture one concrete outcome per issue, with acceptance criteria, evidence links, dependencies and scope. Bugs include observed/expected behavior, reproduction or capture steps, versions and uncertainty. Field tests distinguish planned criteria from measured results. Feature suggestions default to Deferred until the owner activates them.
3. Claim authorized work by setting In progress, assigning the responsible GitHub user when appropriate, and recording the actual agent session/machine in the body or a short comment. Keep at most one or two issues in progress. The assignee alone is not a unique session lock; reconcile concurrent claims before changing shared work.
4. Link commits and PRs. Record implementation, tests, deployment, hardware readback and field evidence separately. Use `Refs #N` for changes whose merge does not meet every acceptance criterion. Reserve automatic closing references for issues fully completed by that merge.
5. Move prepared work to Verify while acceptance checks remain. After issue creation or status changes, run `python3 scripts/github/sync-project.py --apply` to update the derived board. Record what passed, what remains, blockers and the next useful action at handoff. Release a session claim when handing off; a retained claim must say what it awaits.
6. Close only when the issue's scoped acceptance criteria pass, linking the decision/evidence and published source as applicable. Use `completed`, `not_planned` or `duplicate` accurately. For a verified implementation with a genuinely separate remaining test scope, create/link that follow-up before closing the implementation issue. Remove the open status label when closing; restore the appropriate status when reopening.
7. Update `records/sessions.md` and affected durable records, commit explicit coherent paths and push completed commits. If GitHub is unavailable, record the pending issue update locally and reconcile next session. Report failed publication or unverified acceptance explicitly.

Small record/documentation changes can be committed directly when coherent and authorized. Use linked PRs for application/firmware changes to make review and existing CI visible; PR creation or merging does not authorize deployment or hardware flashing. No additional review approval policy is introduced here.

## Decisions, wishlist and historical tickets

The `.scratch/pilot/` map and 23 original tickets remain the decision archive. Their metadata is a migration snapshot, not an active frontier. Twenty resolved historical questions were not imported as new open tasks. Extend an existing ticket's answer when a later decision belongs there; use a linked research/decision note for a new question. Preserve useful discussion. The one-non-research-decision-per-Wayfinder-session rule still applies unless the owner changes scope.

Formerly open questions now have these live records:

| Historical question | GitHub successor | Migration treatment |
| --- | --- | --- |
| Private monitoring scope and pilot stack | [Choose monitoring scope](https://github.com/lfg-seth/snorr-meshlink/issues/10) | Triage; research prerequisite completed, no deployment accepted |
| Repeater operations and direct-link placement | [Held survey](https://github.com/lfg-seth/snorr-meshlink/issues/11) | Deferred under the owner's hold |
| Heltec MQTT over WebSockets | [WebSockets alternative](https://github.com/lfg-seth/snorr-meshlink/issues/12) | Deferred alternative to the working TCP/TLS route; no unsupported research resolution |

[The wishlist](../../records/wishlist.md) preserves the owner's requested ideas and deferral decisions, linking their GitHub issues. Capture future requested ideas in both the durable wishlist and a Deferred issue. Mentioning an idea, moving records or listing it in a milestone never activates it.

## Checkpoints and Project board

Milestones group scoped issues under **Reliable bench tracking**, **Measured field pilot**, and **Repeatable member rollout**, without invented dates. Their issue-completion percentage counts closed work; it is not an operational readiness score. The [roadmap](../roadmap.md) states the evidence required to pass each checkpoint. A prerequisite test can expose more work, so review evidence before accepting a milestone.

The [SNORR MeshLink Project](https://github.com/users/lfg-seth/projects/2) is linked to this repository, with Triage, Ready, In progress, Verify, Done and Deferred columns. All work, Current work and Verification are boards grouped by Status; Bugs and Deferred wishlist are filtered tables. The seven owner-held/deferred issues remain Deferred. [Board setup evidence](https://github.com/lfg-seth/snorr-meshlink/issues/19) records configuration and verification.

Issue status labels remain authoritative; Project Status is derived. Change an issue's label rather than dragging its card to request a status change. `python3 scripts/github/sync-project.py` checks alignment without writes; add `--apply` to import missing repository issues and update their board statuses. Closed issues map to Done, and open issues must have exactly one recognized status label. The command leaves issue labels, assignees, holds and evidence unchanged, preserves unrelated Project items and verifies updates with bounded read retries for API consistency. Project identifiers and label mapping live in [project configuration](../../.github/project.json).

The native Item closed → Done and Auto-add sub-issues workflows remain enabled. Newly created default Auto-close issue, Item added, Pull request linked and Pull request merged rules were removed to keep status changes under the label workflow and prevent board moves/PR activity from closing unverified work. No application deployment automation is added.

Full-repository native auto-add cannot be configured through the exposed CLI/GraphQL controls; its creation/toggle requires a GitHub UI. The sync command supplies issue import and reconciliation during sessions. There is no unattended full-repository auto-add or continuous label-to-board synchronization configured; a future request can add that with separately reviewed access. Record a pending board update in the session log if CLI access is unavailable.

## Management tooling

GitHub CLI 2.102.0 was downloaded from the [official release](https://github.com/cli/cli/releases/tag/v2.102.0), verified against published SHA-256 checksums and installed at `/home/setheth/.local/bin/gh` on this workstation. The owner authorized a separate CLI login with Project scope; credentials are in the system keyring, outside Git. Check access with `gh auth status` and `gh project view 2 --owner lfg-seth`; never print or copy the token into project records.

On another machine, install official GitHub CLI and complete its own `gh auth login --hostname github.com --git-protocol ssh --skip-ssh-key --scopes project --web` if Project access is absent. This preserves existing SSH keys. The MCP connection remains available for issue operations but exposes no Project-management tools. Board API readback and saved-view definitions were verified; native browser visual review was unavailable in this session.

## Publication boundaries

This repository and its issues are public. Publish sanitized evidence summaries and references; keep credentials, keys, rosters, raw MQTT/location data and identifiable operational screenshots in ignored private storage with separate backups. Use the existing record for inventory, finances, sites, field results and content. Candidate sites remain unapproved for installation. Tracking work creates no authority for purchases, hardware changes, operational deployment or external outreach.

Source references: [GitHub Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects), [built-in Project automation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations), [milestones](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones).
