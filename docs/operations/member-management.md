# Member creation in MeshLink

Admins use **Users → Add member** to enter a full name, username, initial
password (at least 12 characters) and optional map shortname. MeshLink creates
the person and login together, generates the stable internal member key, and
selects the new person in the tracker assignment form. Choose a tracker and
save the assignment. Members can also claim an available tracker themselves.

The internal key links the login, person and dated assignments. It remains
stable when the person changes trackers. Existing-member provisioning remains
available through `backend/accounts.py create --member-key EXISTING_KEY`;
ordinary `create` generates the member automatically for the member role.
Account creation is admin-only; public registration is not enabled. Password
reset and account deactivation remain owner-run backend commands.

## MeshLink 0.1.5 deployment - 2026-10-25

Owner explicitly selects deployment after merging [PR #66](https://github.com/lfg-seth/snorr-meshlink/pull/66)
as `9bad77c`. Release metadata/changelog advance together in
**`b3eba74139bb519068631aeaf88358179415d262`**, published on `main` and immutable
annotated **`meshlink-v0.1.5`**. The separate SNORR Firmware version is unchanged.

- Exact clean source in `/opt/meshlink-release-member-b3eba74` passes **90 backend
  tests**, **63 portal tests**, TypeScript and a live production build using
  server Node 22.23.1. All migration files match installed production after
  normalizing line endings; no migration runs.
- Hold `/run/lock/meshlink-deploy.lock` during promotion. Verify the complete
  pre-release backup and isolated live/demo recovery before replacing source.
  Retain prior source/root metadata/static assets in
  `/opt/meshlink-rollback-member-b3eba74`. Publish hashed assets before atomically
  replacing the index; earlier assets remain available to open tabs.
- With both APIs/workers stopped, exact hashes of live/demo databases,
  credentials, worker receipt queue and `/etc/meshlink` are unchanged across
  source replacement. Installed backend/portal files match the release source.
  No operational member/login or assignment is created by acceptance checks.
- A separately running B003 registration overlaps the initial post-backup
  verification: the API/database inventory changes, then the backup predates
  that change. Preserve the registration and retain the failed evidence. Take
  a fresh final backup after the registration; final live and demo isolated
  recovery both pass against the current inventory. No source rollback or
  inventory reversal is needed.
- Recovery uses the existing installed verifiers plus the prior narrowly scoped
  private allowance for exactly R005/R007/R008/R009 planned infrastructure.
  Check planned status, absent radio identity and disabled monitoring before
  allowing these placeholders outside the radio mappings. The installed
  verifier and production configuration remain unchanged.
- All **ten** build files match both loopback and public HTTPS. Served
  `/version.json` and installed `SOURCE_COMMIT` identify **0.1.5 / b3eba74**,
  live mode and `trackedChanges: false`. Public index SHA-256:
  `a9436d96b11b54314a69e18f157cbb339ca81ba1225181ba99342ce1592c38d9`.
- Authenticated live state/feed, unchanged operational account/member/assignment
  rows and rejection of an invalid creation request pass. An isolated copy of
  the final production backup verifies actual member/login creation with an
  automatically generated key, successful login/node assignment, duplicate
  username rollback and denial of account creation to ordinary members.
  The temporary isolated API/database are removed after the test.
- Public protected routes, per-client sign-in throttling, backup checksums,
  database integrity, saved history and live/demo separation pass. All six
  services are active. Four new MQTT receipts arrive during the successful
  observation window; the latest **200** envelopes validate. The first
  45-second window had no packet; the follow-up three-minute window succeeds.

### Backup and rollback evidence

Private evidence remains under `/root/member-release-20261025` on the LXC.

| Phase | Archive | SHA-256 |
| --- | --- | --- |
| Before | `meshlink-20261025T181919Z.tar.gz` | `2277b76095de398c995c375b0d7a437872029d7729fadc1e475327981c651d73` |
| Final after B003 registration | `meshlink-20261025T182339Z.tar.gz` | `896f807d5a964f2404f1205d5ed8ffad320e7545c0987473cacd9c691b8007df` |

The initial post-release archive, preceding completion of B003 registration,
is retained as `meshlink-20261025T182101Z.tar.gz`; its SHA-256 is
`115f13eb3b7e8410ebecece67dc9c3ad8c7e6bbb0330abf1f02b8c02ff92c527`.
Exact release-source archive SHA-256:
`52704e306c26911be7b1b606ca96d4b34026bd0f1af51919eb2aca8f45421851`.
Build/protected-state manifests, pre/final recovery logs, acceptance results and
fresh-receipt checks remain private. Backups share this LXC disk; off-host
recovery remains a separate open gate. Source rollback restores matching
backend/portal/root metadata and preserves any accounts created since release;
no database rollback is required for this migration-free change.

Next: authenticated owner-phone acceptance of **Users → Add member**, followed
by selection and assignment of an appropriate member node. No real member
credentials, roster or raw location data are added to Git.
