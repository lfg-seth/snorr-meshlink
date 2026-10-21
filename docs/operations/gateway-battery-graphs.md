# Gateway battery graph investigation - 2026-10-21

Tracking: [Populate gateway battery graphs from reported voltage](https://github.com/lfg-seth/snorr-meshlink/issues/42).

The owner confirms G001 and G002 each have one installed **1000 mAh LiPo** and reports visible portal voltage with an empty battery graph. Record these assignments in [inventory](../../records/inventory.md); nominal capacity does not establish actual capacity or runtime.

## Reproduction and cause

The original gateway provisioning in `deploy/portal/live-cutover.js` sets `cadenceMinutes: 0`, battery monitoring disabled and battery setup unverified. Today's G002 telemetry enablement initially changes only the radio profile, not this portal configuration. Initial SSH access fails with NXDOMAIN; the owner restores connectivity and authorizes deployment later the same day. Live readback then confirms zero cadence on both gateways, **47 valid measured G002 voltage samples** and **zero G001 battery reports**. This establishes the original zero-cadence reproduction against production metadata.

The actual React `BatteryChart` reproduces the reported empty graph with two valid measured voltage samples, a successful history loader and the original zero cadence. A control using the same loader/readings and positive cadence renders a curve even with an unknown battery profile. Zero cadence splits every sample into an isolated segment; the curve builder omits single points and the chart previously rendered only when a curve existed. One initial sample or isolated samples after outages were hidden too. Pack chemistry/capacity does not gate the voltage graph.

Reproduction command from `portal/`:

```sh
node --experimental-strip-types --test --test-name-pattern="gateway voltage samples" tests/infrastructure.test.mjs
```

Before the fix, two runs fail with `received gateway history must populate the graph`. Afterward, the test passes: unknown cadence shows exact measured dots with no connecting curve; a first single sample also appears. Known cadence retains existing curves and outage breaks. No missing timestamp is replaced by receipt time, no voltage is invented and no reporting cadence is inferred.

## Verification and deployment

All **47 portal tests**, TypeScript and the production build pass through `npm run check` on desktop Node **25.6.0** with lockfile-installed dependencies. [Portal CI](https://github.com/lfg-seth/snorr-meshlink/actions/runs/39675958265) also passes on pinned Node **22.23.1** for application source **`c15859a`**, published in [PR #46](https://github.com/lfg-seth/snorr-meshlink/pull/46). Native/mobile review remains separate. No backend, radio or schema changes are needed for this rendering correction.

Merged [PR #46](https://github.com/lfg-seth/snorr-meshlink/pull/46), application **`fa035509dfc2fd1492c8ae01618d99269c9a4f92`**, is deployed. Isolated `/opt/meshlink-release-fa03550` also passes all 47 tests, TypeScript and the live build on server Node 22.23.1. All fourteen backend hook/migration files match the previous deployment after line-ending normalization; none is replaced. Publish frontend source and hashed assets, then atomically replace the index. Retain old assets for open tabs and prior frontend source/static/markers at root-private `/opt/meshlink-rollback-fa03550`.

Quiesced live/demo database hashes and private configuration/credential hashes remain exactly unchanged during frontend promotion. Separately, trusted loopback administration sets **both gateways** to `batteryProfile: lipo-1s`, `batteryCapacityMah: 1000` and an owner-confirmed pack description. G002 gets only the battery-specific expected cadence of **5 minutes**; G001 retains unknown cadence. Independent readback preserves all nine identities, every other configuration field and existing monitoring/warning enablement. No radio, backend, schema or demo-data change.

Actual React rendering with authenticated live state/history passes: **48 G002 samples** produce a measured curve and **approximately 80%** at about **3.996 V**. The same real samples also render as exact dots when cadence is unknown. G001 correctly shows awaiting valid voltage/history, rather than fabricated data. Its telemetry enablement remains a separately authorized later action. These are snapshot readings, not capacity/calibration/runtime measurements.

The first public asset check catches HTTP 403: staged build files inherited root-only permissions. Correct only the nine public build files to mode 0644 and rerun every HTTPS byte comparison successfully. Future promotions must set public file modes explicitly before replacing the index. Private evidence retains restrictive modes. Public index SHA-256: `d9823444c74104b577fd0af647c0cc3589531c8a75d7559d1baae9eeeaa6f4cc`.

Private backup evidence:

- Verified pre-release `meshlink-20261021T211006Z.tar.gz`, SHA-256 `3338d8960fe557d6aeaffeeb6d209b1efb6f6b063bdab5b0821b2c495d1dfaf2`.
- Final post-release, with corrected public modes: `meshlink-20261021T211612Z.tar.gz`, SHA-256 `fb860eb96bac9f8ba2cf48227d251c86e8f1211245186b1872c8f958332070ac`.

Both pass checksum, isolated live database/API and synthetic demo database/API/history recovery. Public TLS/protected routes, per-client sign-in throttling, live/demo token and OS isolation, all nine public build files and all six services pass. Fresh MQTT archive reception, the latest 200 envelope checks and an empty durable queue pass. No native browser/mobile review or field-performance result is claimed; issue #42 remains Verify without a retained claim for presentation confirmation. Raw state/history, build/render evidence and configuration snapshots remain root-private under `/root/gateway-battery-release-20261021/`.
