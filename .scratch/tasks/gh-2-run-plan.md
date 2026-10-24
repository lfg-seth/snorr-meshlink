# GH-2: phone-free GPS and runtime run plan

## Outcome and inputs

Prepare one executable bench plan for B001/B002. The
[GH-2 import](../../records/tracking-import/github-2.md#acceptance-criteria)
owns acceptance; use the [Heltec checklist](../../docs/operations/heltec-bench-checklist.md)
and [recorded GPS bench result](../../records/field-results.md#test-005--live-portal-gps-ingestion).

## Scope and ownership

Add the planned procedure to `records/field-results.md`, clearly marked planned.
Read inventory and existing profiles to identify available devices and packs.
Keep this preparation separate from running the test, changing profiles, opening
serial ports or interrupting live gateways. Preserve the 15-minute stale
threshold and four-hour minimum/12-hour target.

## Prerequisites

List the exact devices, battery allocations, observers, gateway/portal access
and available runtime window. Proposed sampling and acceptable stale/missing
rates must be agreed before the run; unknowns remain explicit. Preparation can
proceed while hardware/access is unavailable. This brief does not invent those
choices or claim the plan is already agreed.

## Done and verification

The plan specifies power-on without phones, battery-only start/end conditions,
GPS measurement age separately from receipt age, both-gateway delivery,
sampling, missing packets, interruptions and stop conditions. Define the private
raw-evidence location and sanitized result fields, including each tracker's
four-hour result and comparison with the 12-hour target.

Check the procedure against every GH-2 criterion. List the remaining owner
choices as a concise decision request. Do not claim a measured result from plan
preparation. Forced relay and outages belong to GH-3's separate run.

## Evidence and handoff

Link the planned entry from GH-2's tracker row and record the handoff in the
session log: plan/evidence paths, unresolved choices, commit/branch and the next
available bench window. Keep tracks and identifiable locations private.
