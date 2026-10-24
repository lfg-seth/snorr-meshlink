# Gateway outage health and four-board rollout

Owner selects one outcome on 2026-10-24: a gateway with lost Wi-Fi reports its
own health, telemetry and neighbor observations through another online gateway,
and the portal distinguishes the backhaul outage from fresh radio evidence.
Flash the four attached gateways with latest matching firmware and a 180-second
device/active-sensor/SNNS baseline. User authorizes one read-only review agent;
one implementation session controls all board/serial/live-service mutations.

Canonical contract and evidence: [gateway health](../../docs/operations/gateway-backhaul-health.md),
[board handoff](../../docs/operations/board-flashing-handoff.md),
[warning policy](../pilot/issues/10-infrastructure-warning-rules.md),
[manual release procedure](../../docs/operations/meshlink-releases.md).

Write scope: SNORR gateway health firmware/tests; MeshLink decoder, ingestion,
warning and gateway presentation/tests; selected matching manual deployment;
four application-only flashes and explicit configuration verification; relevant
records. Preserve other hardware work and all gateway identities/secrets.

Acceptance: target builds and module/wire/backend/portal checks; fresh full
backups; per-board image digest and full intended profile through reboot;
automatic three-minute telemetry/SNNS/health through peer gateways; controlled
outage badge and recovery with configuration restored. A test that supplies
time over serial must record that clock source rather than imply autonomous
unknown-clock freshness. Calibration/runtime/field coverage are separate gates.
