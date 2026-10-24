# MeshLink application releases

`meshlink-release.json` owns the application version and firmware/wire
compatibility contract. Portal and backend source share that version; SNORR
Firmware has its own version. Start at **0.1.0**, use patches for fixes and minor
increments for development milestones, then **1.0.0** for accepted production.
Versions use numeric major.minor.patch without beta suffixes.

For a new release:

1. Update the root release JSON, `portal/package.json` and both root-version
   fields of `portal/package-lock.json`. Add a dated `CHANGELOG.md` entry with
   affected components, compatibility, migrations, rollback and known limits.
2. Run `npm run check` in `portal` and `.venv/Scripts/python.exe backend/manage.py check` on Windows (or the project Python environment on Linux) when
   preparing a combined release. Windows also needs `tzdata` in that environment.
   Builds reject mismatched versions, missing
   changelog entries and mismatched `meshlink-v*` CI tags.
3. Commit reviewed changes to `main`. Build from the clean release commit;
   generated `portal/dist/version.json` identifies product/version, source SHA,
   tracked-dirty state, mode and compatibility. HTML carries version/source meta
   tags. CI saves the checked portal artifact for main/tag builds.
4. Create an immutable annotated `meshlink-vX.Y.Z` tag on that exact commit and
   push it to origin. Tag workflows run portal and backend checks. Do not move a
   published tag or silently replace shipped assets. Keep checksums with any
   subsequently distributed/deployed archive; the Git tag identifies source.
5. Deploy only when selected, using the existing backup/recovery procedure.
   Verify the served `/version.json` against the intended commit and separately
   verify backend checkout/migrations and fresh end-to-end receipts. Portal
   metadata alone does not establish the running backend's version.

The source tree must include Git metadata for versioned builds. Dirty local
builds are marked; they are not clean release artifacts. The existing API does
not acquire a new public backend endpoint. Record server deployment evidence in
the session/operations log rather than equating a source tag with deployment.

Local tracking is permanent on `main`; `.scratch/TRACKER.md` owns task status.
GitHub hosts source, CI and useful PRs. The GitHub repository rename to `meshlink`
has not yet occurred as of this implementation; remote/link migration follows
the actual rename rather than assuming a new destination exists.
