# Gateway battery graph investigation - 2026-10-21

Tracking: [Populate gateway battery graphs from reported voltage](https://github.com/lfg-seth/snorr-meshlink/issues/42).

The owner confirms G001 and G002 each have one installed **1000 mAh LiPo** and reports visible portal voltage with an empty battery graph. Record these assignments in [inventory](../../records/inventory.md); nominal capacity does not establish actual capacity or runtime.

## Reproduction and cause

The original gateway provisioning in `deploy/portal/live-cutover.js` sets `cadenceMinutes: 0`, battery monitoring disabled and battery setup unverified. Today's G002 telemetry enablement changes only the radio profile, not this portal configuration. Current production configuration/history must still be read back; SSH hostname `meshlink.int.spp.lol` returns NXDOMAIN from this desktop, including a direct DNS check.

The actual React `BatteryChart` reproduces the reported empty graph with two valid measured voltage samples, a successful history loader and the original zero cadence. A control using the same loader/readings and positive cadence renders a curve even with an unknown battery profile. Zero cadence splits every sample into an isolated segment; the curve builder omits single points and the chart previously rendered only when a curve existed. One initial sample or isolated samples after outages were hidden too. Pack chemistry/capacity does not gate the voltage graph.

Reproduction command from `portal/`:

```sh
node --experimental-strip-types --test --test-name-pattern="gateway voltage samples" tests/infrastructure.test.mjs
```

Before the fix, two runs fail with `received gateway history must populate the graph`. Afterward, the test passes: unknown cadence shows exact measured dots with no connecting curve; a first single sample also appears. Known cadence retains existing curves and outage breaks. No missing timestamp is replaced by receipt time, no voltage is invented and no reporting cadence is inferred.

## Verification and remaining release work

All **47 portal tests**, TypeScript and the production build pass through `npm run check` on desktop Node **25.6.0** with lockfile-installed dependencies. The repository pins Node **22.23.1**; that runtime is not installed locally. CI on the pinned runtime and native/mobile review remain separate checks. No backend, radio or schema changes are needed for this rendering correction.

No production application or metadata change has been made. Once host access is restored, take the normal verified backup, inspect authenticated gateway state/history, and set the owner-confirmed battery setup/profile/capacity (`lipo-1s`, `1000` mAh) while preserving other metadata. Set G002's battery-specific expected cadence to five minutes only after confirming its current profile; G001's cadence remains unknown until separately enabled/verified. Preserve existing warning enablement. Release the reviewed frontend with normal rollback/recovery checks, and verify each gateway's real measured samples render. An absent or unknown measurement timestamp remains a distinct possible reason for empty history and must be checked in production.
