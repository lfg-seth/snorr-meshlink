# Local issue tracker

This repository uses the Wayfinder local Markdown tracker. `.scratch/` is committed to Git.

- Map: `.scratch/<effort>/map.md`, labelled `wayfinder:map`.
- Tickets: `.scratch/<effort>/issues/NN-title.md`, one question per file.
- Ticket metadata: `Type: research|prototype|grilling|task`; `Status: open|claimed|resolved`; `Assignee: unassigned` or the claiming session; `Parent: ../map.md`; `Blocked by: none` or comma-separated ticket numbers.
- A ticket is unblocked when all listed blockers have `Status: resolved`. The frontier is open, unblocked, unassigned tickets in number order.
- Claim before work by setting status and assignee. A session awaiting owner input may retain its claim; record that state in comments. Release the claim explicitly if handing off.
- Resolve by appending an `## Answer`, marking resolved, and adding a title-link with a one-line gist to the map. Keep answer details in the ticket.
- Append discussion under `## Comments`; do not erase useful decision history.
- Create ticket files first, then wire blockers once the referenced files exist.

Find state with `rg '^(Status|Assignee|Blocked by):' .scratch/pilot/issues`. Use ticket titles in human-facing references. The current map is [Define an owned-hardware field pilot](pilot/map.md).
