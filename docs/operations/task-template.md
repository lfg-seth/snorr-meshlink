# Bounded assignment template

Use this when a selected task needs more detail than its tracker entry or
existing acceptance section. Keep the brief under `.scratch/tasks/`, named for
its parent and outcome. A brief describes scope; the [tracker](../../.scratch/TRACKER.md)
owns status. Fill the fields below and link requirements rather than copying them.
Small tasks can use the same fields directly in the request.

```text
# PARENT-ID: concrete outcome

## Outcome and inputs
State one result that can be finished and reviewed independently.
Link the parent acceptance section and only the evidence needed for this step.

## Scope and ownership
Name the code/documents this worker may change, the branch/checkouts involved,
and any shared interfaces. Name what belongs to a later assignment.
Carry forward existing authorization; distinguish source publication from
deployment, board configuration/flashing and other physical operations.

## Prerequisites
List required inputs, access, hardware and unresolved owner decisions.
Separate work that can proceed now from verification awaiting those inputs.

## Done and verification
State observable completion criteria, commands or measurements, and expected
failure cases. Link the parent's criteria; preserve every applicable gate.
Specify which evidence stage this assignment can establish: source/build,
release, deployment, board readback, live receipts, sustained or field acceptance.

## Evidence and handoff
Name the existing records for results and private evidence paths.
Report changed behavior, checks/results and limits, commit/branch, and next action.
```

Dispatch example:

> Complete `.scratch/tasks/local-3-snns-interval.md`. Implement and verify the
> scoped software outcome, update its existing records, and commit/push on a
> short-lived branch. Carry forward existing authorization and identify any
> hardware verification still pending. Pause dependent work only for missing
> access, a material unresolved decision or an operation outside that scope.

For an independent review, name the fixed commit/diff, relevant requirements and
expected report. Request findings with file locations and missing acceptance
evidence; let the implementation worker integrate fixes and publish the handoff.
