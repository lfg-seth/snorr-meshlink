# Repeatable local checks

Run from any directory using the path to `check-project.py`. It finds the
repository root itself. Use the project Python environment for component suites;
the default documentation check needs only Python and Git.

```sh
python scripts/check-project.py
python scripts/check-project.py docs --base origin/main
python scripts/check-project.py bench firmware-release
python scripts/check-project.py portal
python scripts/check-project.py backend
python scripts/check-project.py --list
```

| Scope | What it runs / establishes |
| --- | --- |
| `docs` (default) | Git whitespace plus local inline Markdown file/heading links in changed and untracked Markdown. Default comparison is HEAD (staged and unstaged); `--base origin/main` includes committed branch changes. External URLs are skipped. |
| `bench` | Existing offline updater tests: identity selection, image/profile preservation and update sequencing with hardware mocked. |
| `firmware-release` | Existing packaging/provenance/checksum tests in the pinned firmware submodule. Requires that checkout; no artifact downloads/publication. |
| `portal` | Existing `npm run check`: portal tests, typecheck and build. Requires installed Node/npm/dependencies and writes local build output. |
| `backend` | Existing `backend/manage.py check`: backend suite using isolated local services/databases. Requires installed project dependencies/PocketBase; may bind local test ports. |

Failures return nonzero; a selected failed scope stops the run. Missing tools,
dependencies and submodules are failures, not skipped passes. The runner does
not install/download dependencies, open serial devices or connect to production.
These checks do not establish scheduler behavior, native UI acceptance, live
receipts, sensor accuracy, runtime or field readiness. Run checks appropriate to
the change once; repeat after relevant changes or failures.

The Markdown check covers inline links, including images, and ATX (`#`) heading
anchors. It ignores fenced code and external URLs. Reference-style links and
explicit HTML anchors need review separately; this is not a full Markdown parser.
The project-record CI runs the regression tests and checks changed documents on
main/PRs; it does not deploy anything. For runner regression tests:

```sh
python -m unittest discover -s scripts/tests -v
```

Existing operation tools remain separate entry points:

- [RAK role change](../docs/operations/repeater-role-change.md) uses
  `bench/set-repeater-role.py` to back up, prompt for a long name (preserving the
  short name), select ROUTER or CLIENT, prompt for a decimal fixed location and
  enroll B002 as admin over USB. It checks the intended profile/coordinates
  through reboot and saves private `reconciliation.txt` results; see the
  procedure's preservation correction and hardware verification limits before
  another board run. No firmware flash.
- [Board updater](../docs/operations/repeater-update.md) privately compares the
  complete intended profile through reboot and verifies image provenance.
- [Release download helper](../docs/operations/board-flashing-handoff.md)
  downloads/verifies the pinned artifacts only when that operation is selected.
- [Receipt evidence](../docs/operations/repeater-gateway-check-20261019.md) and
  [MQTT operations](../docs/operations/live-mqtt.md) define live provenance and
  clock distinctions. A reusable live receipt collector needs its own selected
  scope/private input contract; local tests are not an authenticated receipt.

Reuse these tools before creating another verifier. Add new automation alongside
the component that owns its behavior and record measured limits in its existing
operations record.
