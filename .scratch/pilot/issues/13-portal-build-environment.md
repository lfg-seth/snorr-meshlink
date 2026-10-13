# Establish the portal development and CI baseline

Type: task
Label: wayfinder:task
Status: resolved
Assignee: portal-environment-session-2026-10-13
Parent: ../map.md
Blocked by: none

## Question

How can the accepted React/TypeScript/Vite frontend, PocketBase backend and Python worker be developed on the owner's Dell, with reproducible checks and a path to later VM hosting?

## Comments

2026-10-13 — Owner accepts the stack and asks that TypeScript remain approachable. Owner reports a home desktop with WSL/Docker potentially available and no Proxmox VM yet. Prepare a lightweight native frontend baseline and GitHub-hosted CI; keep desktop full-stack testing and deployment as later steps. Do not assume desktop access or VM readiness.

## Completion evidence

Document the development commands and environment strategy; provide a reproducible frontend build and CI workflow; record actual local checks and any remote verification limits.

## Answer

2026-10-13 — Added `portal/` with React/TypeScript/Vite, exact dependency versions and npm lockfile, Node 22.23.1 in `.nvmrc`, readable position types, synthetic freshness-state starter and development instructions. Plain types/components and small domain comments follow the owner's TypeScript preference.

Added SHA-pinned GitHub-hosted CI for pull requests/main pushes affecting portal code. It installs from the lockfile, runs focused age tests/type checking/build, and retains successful main build artifacts for seven days. No deployment credentials, VM or Docker required. See the [environment plan](../../../docs/research/portal-build-environment.md) for native Dell development, optional desktop WSL/Docker integration and later manual-first VM deployment with persistence/backup/rollback checks.

Local verification: lockfile installation, all four direct measurement-age tests, strict TypeScript check and Vite production build passed. Generated assets/dependencies are ignored; whitespace checks passed. No browser layout QA, remote desktop check, Docker services, authenticated backend or deployed portal verified. First GitHub-hosted CI execution remains to verify after publication. This resolves the development baseline task, not the four-page portal implementation or deployment.
