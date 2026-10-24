# Installed backup recovery verifiers - 2026-10-24

Owner requests correction of the installed device-count and bounded-history
assumptions, followed by live/demo backup recovery. This completes the selected
[GH-39 acceptance](../../records/tracking-import/github-39.md) and the live
member-count follow-up found during the [0.1.2 deployment](device-card-battery-summary.md#meshlink-012-deployment---2026-10-24).
Historical GitHub issues/imports are unchanged.

## Corrected checks

The prior live check required B001/B002 even after the owner's separate B001
decommissioning. The demo check required untruncated history even when its
long-running database legitimately exceeded the API's 50,000-sample cap.
Both exact failures reproduce through the real verifier call sites in 0.18
seconds before the fix. They are assertion assumptions, not evidence of a bad
backup. Version-controlled regression fixtures now cover the evolving inventory
and longer-lived demo instead of relying solely on the small initial seed.

- [Live verifier](../../deploy/portal/verify.py) reads exact member/infrastructure
  identities from the provisioned database through a read-only connection.
  API lists must match, without duplicates. Active infrastructure must still
  have a gateway/repeater mapping; retired mappings can remain for archived
  interpretation. The backup and restored API must retain those same identities.
- [Demo verifier](../../deploy/portal/verify-demo.py) uses the same identity
  checks. Its restored 24/168/720-hour responses must equal the exact newest
  saved rows, including voltage, order and clock provenance. The cap remains
  **50,000**, and `truncated` must equal whether more saved rows exist.
- [Shared assertions](../../deploy/portal/recovery_checks.py) fetch at most the
  capped expected rows plus a count, rather than loading all history. They
  preserve receipt-clock fallback and the API's measured/receipt tie ordering.
  Since the API computes its window internally, only exact possible windows
  between request start/end are accepted, including rows crossing a boundary;
  no clock tolerance or widened window can hide a missing/wrong reading.
- Missing expected history, changed values, missing/duplicate devices, wrong
  ordering, oversized responses and incorrect truncation still fail. Existing
  archive checksum/integrity, protected routes, authentication throttling,
  live/demo token/OS separation and isolated restore checks remain in place.

No API, ingestion, history, radio, schema, configuration or frontend behavior
changes. The application stays **MeshLink 0.1.2 / `359e6ba`**; its immutable tag
and static assets are unchanged. This is operational verifier maintenance.

## Source, installation and checks

Fix **`b738d73b7d92e713c32bf334940b93c9089c33da`**, merged through
[PR #61](https://github.com/lfg-seth/snorr-meshlink/pull/61) as **`340feba`**.
Eight focused regressions pass locally; the full Linux backend scope passes
**83 tests** in the isolated `/opt/meshlink-recovery-check-b738d73` source tree.
[Backend CI](https://github.com/lfg-seth/snorr-meshlink/actions/runs/40126746088)
also passes on the fixed PR head. No frontend check/build is needed for these
operational scripts and backend-only regression additions.

Install the three checked files together under `/opt/meshlink/deploy/portal`,
with the shared helper first and atomic replacements. Retain both prior
verifiers root-private at `/opt/meshlink-recovery-rollback-b738d73`. Hold
`/run/lock/meshlink-deploy.lock`; do not overlap another intentional live change
or another verifier using the fixed isolated recovery ports. Backend hooks,
migrations, application identity, served version and private configuration hashes
are identical across installation. `/opt/meshlink/VERIFIER_COMMIT` records the
checked verifier commit separately from application `SOURCE_COMMIT`.

Installed SHA-256 values:

| File | SHA-256 |
| --- | --- |
| `verify.py` | `fd330a194abfd3b63a8b7de4817c2f610d2b27c17ca3087710eb23defdca98d0` |
| `verify-demo.py` | `b51b068e0c22ee8595fb058c187db630465ed16a33ba3d5c5b8b083207ab70e0` |
| `recovery_checks.py` | `5db3916169c344708e5667250d03b5e400cfdd92dcafc7004991635fb4602978` |

Future updates must carry the shared helper with both verifiers. The ordinary
backup includes their complete `release/deploy/portal` directory. Installation
does not replace the backup helper or the live database. The normal commands
now pass directly, without a task-local replacement verifier:

```sh
python3 /opt/meshlink/deploy/portal/verify.py --public
python3 /opt/meshlink/deploy/portal/verify-demo.py
```

## Fresh installed recovery evidence

Fresh backup **`meshlink-20261024T194543Z.tar.gz`**, **235,982,579 bytes**, SHA-256
`20b0b3fc24b29b8fbaa5ab53d0d85e60af294caa4cbc6873aa1c2f1bd3c91d40`,
stays root-private in `/var/backups/meshlink`. The installed backup briefly
quiesces/restarts the APIs/workers. Both installed verifiers then pass against
that archive under the deployment lock, including exact live provisioned and
restored identities (**one member / nine infrastructure**), checksum/integrity,
credentials/records, public protection, token/OS separation and isolated APIs.

The restored demo's exact history results are:

| Window | Returned / saved in window | Correct truncation |
| --- | --- | --- |
| 24 hours | 17,056 / 17,056 | false |
| 7 days | 50,000 / 65,531 | true |
| 30 days | 50,000 / 68,843 | true |

No history is pruned or API limit expanded. All six services are active after
recovery. Four fresh MQTT archive receipts pass the follow-up; the newest 200
envelopes validate and the pending queue is empty. Private installation proof,
backup receipt and live/demo recovery logs remain in the isolated check directory.
Changed-document links and whitespace pass. The root checkout's unrelated bench
and hardware changes are preserved.

The installed-verifier follow-up is complete. Existing off-host disaster
recovery remains GH-7; owner-phone/card acceptance and physical current accuracy
remain their existing separate gates.
