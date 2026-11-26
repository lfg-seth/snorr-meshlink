# A shorter MeshLink development and release cycle

Proposed November 25, 2026. The goal is for the owner to keep one URL open on
a phone, request a change, refresh to try it, and say “ship this version.”
Codex owns the steps between those actions. Start with the existing application,
Git history, Linux services and checks. The proposed first milestone ends at
phone review. Production still follows the [accepted release procedure](meshlink-releases.md).

## Where time goes today

| Observation | Change worth making |
| --- | --- |
| The 0.4.16 release ran PR, main and tag CI, then 101 backend, 72 portal and 55 script tests plus a build on the host. Portal CI retains static files for seven days on main/tag pushes. Backend CI checks source. Neither workflow delivers a complete candidate to staging. [Release evidence](field-portal.md#november-23-member-tracker-activity-deployment) | Give each tested candidate a commit, a complete package and a digest. Run host-specific checks on the host. Reuse test results and artifacts for the same inputs. |
| The records workflow checks out the firmware submodule and runs the scripts test suite even for a session note. Conversely, an isolated change to `scripts/server/` or `scripts/portal-activity.py` matches none of the four workflow path lists on main, although the Activity service executes project Python code. | Give prose a lightweight link/whitespace job. Route script implementations and tests together. Cover runtime scripts in the deployable package. |
| GitHub tracking setup already validates historical configuration only. The PR template still asks for issue references. One tracker, a session log, briefs and release/field records are available. There were 58 registered worktrees on the desktop at review time. | Keep one active application change and one queue. Use the owner’s request as the brief for small changes. Link the CI run and deployment result once at handoff. Retire finished worktrees after checking their contents and branch integration. |
| The [desktop preview](../../records/sessions.md#2026-11-16---desktop-staging-for-iphone-review) proved iPhone access. Its per-build setup under ignored local data proxied allowlisted reads to the live API and blocked writes. The [portal LXC](portal-lxc.md) already uses Nginx and cloudflared. | Reuse the serving pattern with persistent, writable fictional state so we can try sign-in, assignments, stale GPS and message flows end to end. |

## The day-to-day loop

1. Codex starts one short-lived branch from current main. Open one PR for the
   whole change if needed for CI or merge policy. Keep the branch through the
   feedback rounds. The owner needs only the staging URL.
2. Codex selects that branch for the single shared stage. Each push to it runs
   affected checks, packages the app and updates stage automatically. Use the
   same URL from either development machine. Serialize activation, discard stale
   jobs and keep serving the previous healthy build on failure. Show **STAGING**,
   the short commit and deployment time so a refresh is unambiguous.
3. Owner tests, gives feedback, repeats. One wording change should take one
   edit and push. No release tag, new brief or changelog entry per iteration.
   For the first three changes record push-to-visible time and owner actions.
   Aim for under two minutes on a warm portal-only change and zero owner
   deployment steps. That is a target to measure.
4. When feedback is complete, Codex prepares the version and changelog once,
   using the existing root manifest and package version checks. Stage the final
   release candidate. If the merge method makes a new SHA, stage the actual
   merged main artifact before offering promotion. Confirm CI, stage and
   candidate digest agree. One explicit “ship this version” selects the
   displayed candidate. A later push cannot change an in-flight promotion.

## Where stage runs

Use a small dedicated Linux LXC on existing always-on Proxmox capacity if
available. It can follow the production service layout and remain reachable
when the desktop sleeps or the owner switches to the Dell. Host capacity and
permission to provision that guest still need confirmation. If the desktop is
the available host, run the same isolated Linux service there with automatic
startup. The hostname survives a later host move. Desktop sleep or loss of
connectivity takes that origin offline.

Create a Cloudflare Access application limited to the owner before publishing
`meshlink-stage.spp.lol`. Use a stage-specific named tunnel to a loopback Nginx
listener and enable Access token validation. Keep MeshLink login behind Access
so both member and dispatch roles can be exercised. Keep deployment control
on the management side. An outbound pull of successful artifacts for the
explicitly selected repository branch lets the stage host stay off the public
SSH network. CI can run on hosted runners without production credentials.
[Cloudflare self-hosted application setup](https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/self-hosted-public-app/)

Use stage-only service identities, PocketBase database, credentials, synthetic
member positions and simulated gateway/worker traffic. Seed once and offer an
explicit fixture reset. Route outbound dispatch messages to a test sink.
Restrict stage service access to production databases and brokers at the
network/credential boundary. Rehearse migrations on stage. Keep private
recovery tests and selected physical radio checks in their existing environments.

## What runs for each change

| Changed area | Routine verification | Release consequence |
| --- | --- | --- |
| Project records or planning | Changed links and Git whitespace | Publish records only |
| Portal | Existing portal unit tests, typecheck and production-mode build | Refresh the stage candidate, verify sign-in and changed screen |
| Backend, ingestion, Activity or deploy files | PocketBase integration and affected script tests, then exercise the installed route/service with synthetic traffic | Include matching backend, hooks, migrations, worker/service files and runtime scripts in the candidate |
| Shared release metadata or cross-component contract | Both application suites and compatibility checks | Prepare a complete matching candidate |
| Bench tooling, firmware pin or firmware release | Relevant bench/manifest checks and target build in the authorized firmware repo as appropriate | Track physical flash, readback, RF delivery and field measurements separately |
| MeshMonitor, broker or infrastructure | Component-specific config/restore checks and a selected maintenance operation | Independent of ordinary portal refreshes |

Start by reusing the current suites and narrow their triggers. Keep the
historical tracking validator on its narrow paths. Automate version propagation
from the existing manifest. Keep one small PR summary. Put durable field
measurements and operational decisions in their existing records. At handoff
use the tracker for the remaining action and the session log for the outcome.

## Implementation order and proof

1. **Deliver the shared stage.** Provision the origin, fixture credentials and
   access policy. Deploy one known main commit. Verify Access denies a
   signed-out caller, the owner can sign in on a phone, a fixture edit persists
   after restart and a simulated outbound message reaches only the sink.
2. **Connect the feedback loop.** Publish an immutable package with a manifest
   of component versions, SHA and hashes from trusted runs. Deploy two
   successive commits from one branch and demonstrate a failed build leaves
   the last good one available. Revert stage to the previous package, switch
   machines and confirm the URL and SHA. Measure the loop here.
3. **Promote the tested package.** Keep a durable release copy beyond CI
   artifact expiry. Give Codex one operator command taking the approved SHA
   and digest. Under the production release lock, verify the package, take a
   recoverable backup, apply migrations once, switch assets and services,
   then verify public version, backend identity, authentication, fresh
   ingestion and GPS timestamp behavior. Check the affected feature and
   post-release recovery. Retain prior assets for open tabs. Rehearse rollback
   on stage first. For incompatible migrations, coordinate database recovery
   and reconcile packets received since backup before resuming ingestion.
4. **Trim process after the trial.** Use the measured runs to remove duplicate
   builds and handoffs, amend the release policy and PR template, and review
   old branches/worktrees individually. Preserve the existing release path
   during the trial. The pending 0.5.0 messaging release has its own decision
   and physical acceptance work.
