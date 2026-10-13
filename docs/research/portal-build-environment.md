# Portal development, CI and deployment environment

2026-10-13. Sources checked against official documentation. Owner accepts React + TypeScript + Vite, PocketBase and a Python worker, while requesting approachable TypeScript. Owner has a low-powered Dell, a home desktop with WSL/Docker potentially available, and no Proxmox VM yet.

## Development now

Use native Node/npm on the Dell for frontend work. The inspected execution environment reports 16 GiB class RAM, four logical CPUs, Node 22.23.1 and ample free disk. This supports trying the small frontend locally; it is not a measured full-stack or browser-map performance result. Docker/gh executables were not found in this environment. No installation is needed to begin frontend work.

Pin Node in `.nvmrc`, exact direct package versions in `portal/package.json`, and resolved dependencies in `portal/package-lock.json`. Node 22.23.1 satisfies Vite's [current Node requirements](https://vite.dev/guide/). Build with the same lockfile in CI. Document purposeful version upgrades and rerun the checks.

The desktop is an optional development/integration host for Docker Compose once PocketBase and the worker exist. Keep a separate clone in WSL's Linux filesystem (for example `~/repos/snorr-meshlink`), following [Microsoft's filesystem guidance](https://learn.microsoft.com/en-us/windows/wsl/filesystems). Move work between machines through Git branches/commits, not copied `node_modules`, databases or credentials. Its specs, access and Docker operation remain unverified. No desktop CI runner is needed initially.

Use synthetic data in development and CI. Later introduce a reproducible Compose definition for persistent PocketBase, Python worker and a local test broker; do not require that service stack for routine frontend edits. Keep named volumes/ignored data separate from source. PocketBase has [no official Docker image](https://pocketbase.io/docs/going-to-production/); pin a chosen release in a project-owned image when implementing it. Worker runtime and dependencies are to be pinned when the worker is introduced, rather than choosing packages before its interface is defined.

## Continuous integration now

The tracked workflow uses GitHub-hosted Linux runners, read-only repository permission, SHA-pinned official actions and no deployment secrets. Portal changes on pull requests and pushes to main run:

1. `npm ci` from the lockfile.
2. Focused measurement-age tests using Node's test runner.
3. TypeScript checking and Vite production build through `npm run check`.
4. On successful main pushes, retain a static build artifact for seven days, labelled with the source commit SHA.

No linting or heavy browser suite is added to this baseline. Add meaningful ingestion/access tests as those components exist, and limited browser checks when interactive screens exist. Documentation-only pushes do not build the frontend. If a mandatory branch-protection check is later enabled, revisit path filtering so skipped workflows cannot strand unrelated pull requests.

Current [GitHub billing guidance](https://docs.github.com/en/billing/concepts/product-billing/github-actions) says standard hosted-runner usage is free for public repositories; private repositories use their plan allowances. Artifact storage has separate billing considerations. This plan is not a booked expense or a claim about account settings. Short retention limits unnecessary storage. Actions availability, branch protection and the first hosted run must be verified separately.

Official action contracts: [checkout](https://github.com/actions/checkout), [setup-node](https://github.com/actions/setup-node), [upload-artifact](https://github.com/actions/upload-artifact), and [workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax). Retain exact source/build identity and keep deploy authority separate from pull-request execution.

## Delivery after the VM exists

The first deployment should be deliberate and manual: use a tested build identified by commit SHA, configure backend services and persistent storage, establish HTTPS via the intended Cloudflare Tunnel, then verify restarts and backup/restore. No VM is needed to reach the local prototype review.

Later automate promotion of tested artifacts through a restricted deployment route, with serialized deployments, a health check and a previous-version rollback. Select the route once VM/network access is known; a pull-based deployment may avoid inbound ports. Do not assume GitHub runners can reach the private VM. Source approval authorizes repository publication, not a new hosted service or desktop access.

Keep PocketBase data outside replaceable containers/build directories. Database migrations and backups require a separate recovery plan: rolling back frontend code does not roll back database state. PocketBase's [pre-1.0 compatibility/production caveat](https://pocketbase.io/docs/) makes pinned versions and tested upgrade/restore procedures relevant before operational use. No production readiness claim is made for this prototype.

Proxmox VM sizing, service composition, hostname, deployment access and backup destination remain later implementation choices. Owner-deferred MQTT transport research stays parked; local synthetic ingestion does not validate the assumed Cloudflare/broker route.
