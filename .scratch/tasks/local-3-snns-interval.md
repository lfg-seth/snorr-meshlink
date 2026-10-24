# LOCAL-3: saved SNNS reporting interval

## Outcome and inputs

Make RAK over-LoRa SNNS follow the saved device telemetry interval.
[LOCAL-3 section 1](../pilot/issues/25-production-firmware-readiness.md#1-remotely-configurable-snns-interval)
owns the full behavior and test matrix. Read the
[current rollout evidence](../../docs/operations/repeater-update.md#current-rollout-status)
when choosing the baseline; use the pinned firmware source, not an old binary's
runtime string, to identify the implementation input.

## Scope and ownership

Work in the firmware fork's RAK SNNS scheduling/module code and actual-source
tests; update profile guidance and the source pin here after publication on
`snorr/develop`. Preserve the gateway local-only cadence and disabled RF TX.
Shared reporting changes require an explicit compatibility check.

This assignment covers source, tests and affected-target builds. Remote-admin
provisioning, the neighbor freshness contract, release publication and individual
board rollout are later LOCAL-3/LOCAL-6 steps. Publishing source carries existing
authorization; this brief does not select a board to flash or deploy a server.

## Prerequisites

Identify the exact source and available build environment. No connected radio is
needed for portable behavioral tests. Record build-toolchain gaps explicitly;
continue independent implementation/checks when hardware is unavailable.

## Done and verification

Complete every section-1 criterion: saved interval with 180-second fallback and
minimum; long/extreme input safety; preserved scheduling, jitter and airtime
gates; interval changes, reboot, rollover and local/radio-mode behavior. Test the
module's behavior rather than a copy of its arithmetic. Build affected targets
and report results separately from portable checks.

Run the existing firmware behavioral checks discovered in that checkout plus
`python scripts/check-project.py bench firmware-release` here for affected updater
and packaging regressions. Those suites alone do not verify the scheduler.
Any test requiring a real board remains a named bench follow-up.

## Evidence and handoff

Record source/build evidence in the existing repeater-update operations record;
update LOCAL-3's tracker row and the session log. Link private logs without
publishing keys/profiles. Handoff: behavior changed, checks and missing evidence,
published source/pin, branch/commit, and next selected-board/admin step.
