# Portal development

React + TypeScript + Vite with MapLibre. The four-page portal supports both a labelled synthetic development scenario and authenticated persistent backend records. The [backend](../backend/README.md) includes a receive-only live Meshtastic GPS worker; see [live deployment](../docs/operations/live-mqtt.md). Native standalone demo changes still reset on refresh.

Build the hosted real-device portal with `VITE_PORTAL_MODE=live npm run check`. It opens at sign-in with a **View demo** button for the fictional browser-only scenario. Demo needs no account and makes no backend requests; its header says Demo and **Exit demo** returns to sign-in. Refresh returns to sign-in. Operational records require authentication, and simulation controls/radio sending remain disabled when the backend reports live mode. Running the default native development commands below keeps the standalone demonstration available.

## Run on the Dell or desktop WSL

Use Node **22.23.1**, recorded in the root `.nvmrc`. If you already use nvm, run `nvm install` and `nvm use` from the repository root. Then:

```sh
cd portal
npm ci
npm run dev
```

Open the localhost address Vite prints. Stop with Ctrl+C. The dev server binds to localhost; no VM, Docker, broker or tunnel is required. The map fetches public USGS tiles directly and needs internet access. To verify before committing:

```sh
npm run check
```

This runs the measurement-age, assignment and history tests, TypeScript checking and a production build into ignored `dist/`. `npm run preview` serves that build locally for review, not as the production server. `npm ci` installs the exact lockfile; use `npm install` only when intentionally changing dependencies and commit the resulting lockfile.

For the authenticated portal with saved records, complete the one-time [backend setup](../backend/README.md), then run `python3 backend/launch.py` from the repository root. It starts the API, simulation worker and portal in one terminal. Open `http://127.0.0.1:5173`, navigate to **Users** and choose **Backend sign in**; Ctrl+C stops the three processes together. Private per-process logs live under ignored `local-data/backend/logs/`. The standalone `npm run dev` command above remains useful for frontend-only work.

## Review the prototype

Navigation uses `#map`, `#users`, `#messages` and `#infrastructure`, including browser back/forward and direct links. The common role selector previews Admin and Member (Demo Casey); it is not authentication or access enforcement. The feed toggle simulates availability, without generating fresh GPS or telemetry observations on reconnect.

In the standalone demo, Demo Avery (S001) has 100% battery and a stationary simulated GPS fix refreshed each minute from the current clock, keeping its GPS age below two minutes even after leaving the page open. Its Last Heard advances with that simulated fix; the other demo trackers retain their aging examples. Authenticated backend observations are unaffected.

- **Map:** fills the available space below shared logo/navigation on mobile and beside navigation on desktop. Select a device pin for a scrollable bottom sheet that fits its contents up to 85% of the mobile viewport, or a compact desktop overlay. The tracker header shows device type/radio name, status and a small colored battery icon. Area and copyable five-decimal Coordinates share a row; Last GPS/Last Heard retain separate clocks with whole-minute ages capped at `+2hrs`. First Seen, Last Heard and Time Active for the latest available GPS session stay visible below them. **Show Recorded Trail** only toggles the latest session's map dots/dashed connections; it adds no controls, point details or explanatory copy to the card. Sessions split at gaps greater than two hours (exactly two hours stays together). Closing a card keeps its trail visible, and trail preference is shared with Users for the current login. Selecting a different map tracker clears the previous trail. USGS topo/aerial and fit-area controls overlay the map. Infrastructure is always visible and old visibility cookies are ignored. Live tiles still require WebGL/network access; feed outages retain observations with a small on-map notice.
- **Users:** member-tracking summary counts and the searchable tracker list now live here (all devices, positions under 15 minutes, stale positions, unknown/never seen). Select any tracker, including one without a GPS fix, for the same responsive device sheet. Members choose/change their own map shortname (1–5 letters, numbers, underscores or dashes) on Users; owner-run account setup accepts the same choice. Recorded coordinates remain accessible here when WebGL is unavailable. Claim/release/transfer tracker assignments and inspect dated history. Member preview can self-claim only free devices and release its own device; Admin can transfer, closing conflicts on both sides. Radio short names remain fixed; assigned map pins use the member-chosen shortname, falling back to the device radio label until one is set. Assignment/release produces a separate simulated long-name job; only the latest job per device can simulate read-back or failure. Transfers also create a release-name job for a carrier's previous tracker.
- **Messages:** chronological shared channel, author-prefixed simulated sends, incoming-message notification and unread badge across pages. Drafts survive page navigation and feed outages within the same browser session. Reconnect never sends a draft automatically. Gateway submission is explicitly unconfirmed radio/human receipt; live payload limits and expiry remain open. Use the footer's incoming-message control to try notifications from another page.
- **Infrastructure:** filter four fictional devices by role; inspect capability-specific current, stale, awaiting-first-reading and not-equipped states, voltage observations, event/audit history and declared battery/solar/antenna configuration. Acknowledge an intrusion without clearing it, or resolve it as Admin with a note. Later normal sensor readings do not clear the latched incident. Admin can record illustrative voltage thresholds with a higher recovery threshold. Rules are configuration previews; automatic low-battery/missing-report/reconnect evaluation and fresh-evidence recovery await ingestion. Infrastructure alerts use silent persistent badges, with no toasts or sound.

Map sheets scroll independently and keep their close button visible; mobile dialogs use native focus containment and an inert background. Native dialogs restore focus on close, and opening one device replaces the previous detail. Marker breathing follows the agreed age bands, stops for stale/unknown fixes, and respects reduced motion. Status text remains available without animation or color.

Shared branding uses the owner-supplied [SNORR logo](https://snorr.vegas/wp-content/uploads/2021/12/cropped-SNORR-Final-Logo.png), stored unchanged at `src/assets/snorr-logo.png` and bundled locally. The mobile map retains the shared logo/navigation and fills the remaining area. The two environment/feed banners appear only on other pages; the breadcrumb/clock bar is removed throughout the portal. Mobile device sheets shrink to fit their contents with an `85dvh` maximum, bottom/safe-area padding and a sticky close control when scrolling.

## Source files and TypeScript

`.ts` contains ordinary JavaScript plus types; `.tsx` also contains React markup. Types describe expected data and disappear from the production JavaScript. They do not validate network input. For example, `measuredAt: string | null` means a timestamp can be a string or explicitly unknown; `import type` brings in a type without runtime code.

- `src/main.tsx`: React entry point; `src/App.tsx`: shared shell, sign-in/demo entry and browser-memory state (assignments, drafts, incidents and events).
- `src/MapPage.tsx`, `UsersPage.tsx`, `MessagesPage.tsx`, `InfrastructurePage.tsx`: page components.
- `src/TrackingMap.tsx`: MapLibre lifecycle, raster basemaps and geographic overlays; loaded on demand.
- `src/demo.ts`: labelled scenario fixtures and plain assignment/history/cadence functions.
- `src/position.ts`: measurement-age and GPS freshness rules, independent of receipt time.

Prefer plain record types, functions and components, inferred types where obvious, and comments explaining domain rules. Avoid advanced generics, type puzzles and broad `any` shortcuts. Keep strict checking enabled to catch timestamp/null mistakes early. The built-in Node test runner keeps the test setup small; tests use only TypeScript syntax Node can strip.

## Verification and limits

Prototype review on 2026-10-13 used local headless Chromium at 1440px and 390px widths, including navigation, topo/aerial tile loading, pins/history, assignment transfer and name jobs, outage drafts/manual sends, unread notifications, incident acknowledgment/resolution, rule configuration and role previews. Checks also cover reduced motion, narrow panel/table overflow, keyboard skip navigation, browser back, blocked tile requests and unavailable WebGL. Both development and production builds were exercised. This does not establish rugged Dell/mobile GPU performance, imagery currency, offline map availability or live radio behavior; review those on the intended devices.

The map renderer is a separate lazy-loaded bundle (approximately 286 kB compressed, plus a 508 kB worker before compression at this checkpoint). Vite reports its size above the default warning threshold. No prefetch, offline-download feature or tile proxy is implemented. Browser map tiles are not the agreed internet-outage field fallback; use the local Meshtastic viewing path, whose field behavior still requires verification.

Map configuration follows the [MapLibre raster source example](https://maplibre.org/maplibre-gl-js/docs/examples/add-a-raster-tile-source/) and the official [USGS Topo](https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer) / [USGS Imagery Only](https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer) cached services, rechecked 2026-10-13. The Vite worker follows the [official MapLibre bundler setup](https://github.com/maplibre/maplibre-gl-js/blob/main/docs/index.md). Attribution stays visible. Aerial imagery is not live imagery; source dates and useful zoom remain in the [map evaluation](../docs/research/dispatch-portal-maps.md).

## Environments and delivery

See [the environment plan](../docs/research/portal-build-environment.md). GitHub Actions runs the same `npm ci` / `npm run check` commands for portal changes. A successful main push uploads a seven-day static build artifact named with its commit SHA. There is no deployment workflow or external preview hosting yet.

Connected mode uses server-enforced roles, transactional assignments and validated normalized ingestion. Choose **Backend sign in** after starting the local backend and worker; browser tokens stay in memory. Never put credentials in frontend configuration: browser-visible build variables are public. Real data, secrets and backups remain in ignored `private/` or `local-data/`; generated output and dependencies stay out of Git. MQTT connectivity research remains deferred.

## Connected backend checkpoint — 2026-10-13

The backend adds username/password login, server records for all four pages, a two-second authenticated snapshot poll, warning acknowledgment and saved mutations. The role selector remains only in standalone demo mode. Saved assignments/messages survive reload and backend restarts; sign in again after reload. Worker/backend outages retain the last snapshot, age its observations and disable sending. Drafts are preserved through reconnect and through edits while an earlier send is pending. API access rules are tested separately from visible controls. Account creation/password reset/deactivation are available through owner-run backend commands; no account-management form is added here. See the [backend setup and limits](../backend/README.md).

## Battery detail — 2026-10-15

Infrastructure details and map sheets show **Estimated battery percentage** without the voltage-estimate warning copy. Charging/discharging/steady direction remains available from the latest uninterrupted hour of voltage observations (at least three reports spanning ten minutes, split at the battery timeout; below 5 mV/hour internally is steady), but no slope is displayed. Current uses mA; absent measured current displays `— mA`. The optional frontend `batteryCurrentMa` field uses positive for charging and negative for discharging. Live ingestion does not populate it yet: the owner's planned INA219 installations, sign/wiring and end-to-end current telemetry still require verification. Never convert a voltage slope into a current reading. Stale readings and feed outages retain historical indications.

The chart offers 1h/6h/24h/all-loaded views, adaptive voltage bounds, actual time spacing, selectable keyboard-accessible readings and an exact-reading table. Net change and min/max describe the selected loaded range; direction uses its independent recent window. Unknown-time/invalid/future samples are not plotted. The existing live snapshot supplies up to 40 recent infrastructure observations (including non-battery observations), so chart ranges may be incomplete. No server retention or telemetry contract changed.

Infrastructure map pins show full device labels and open the shared responsive device sheet. Colocated devices keep their recorded coordinates and receive separate screen offsets for selection. The sheet shows power direction/current availability, available temperature/RH and receipt-based last heard, retaining stale/offline/unknown indications. Owner-confirmed EVE repeaters now show an approximate voltage-derived charge percentage; other unconfigured profiles remain unknown. See [the estimate profile and limits](../docs/research/battery-charge-estimate.md). Map interaction tests use a small DOM marker adapter; they do not verify WebGL, tile rendering or visual layout.

EVE charge estimates are rounded to 5% using an approximate nonlinear reference discharge curve. These are frontend estimates, not backend-reported percentages or remaining runtime. The same display is used in Infrastructure detail and map quick stats.

Map sheet regression checks exercise actual React components with DOM markers, media-query/dialog API adapters and synthetic data. They cover exclusive selection, mobile modal versus desktop nonmodal API calls, latest-session trail toggling without card expansion, close/cancel/Escape, focus restoration, offline status, always-visible infrastructure despite old off cookies/page remounts, and infrastructure-only maps. The Users list also exercises inspection of never-seen devices and shortname saving. No browser surfaces were available for this update, so native modal focus/gesture behavior, animation, WebGL and mobile/desktop visual layout remain unverified.

Tracker status uses GPS measurement age: Active under 2 minutes, Recent from 2–15 minutes, Stale from 15 minutes through 2 hours, and No Location after 2 hours or with missing/invalid/future GPS time. These are provisional presentation thresholds chosen pending owner feedback; the existing 15-minute stale requirement still applies to tracking summaries. No Location preserves any last recorded map pin and coordinates. Map marker widths accommodate up to five chosen characters. Copy uses the browser clipboard API and reports an actionable failure when access is unavailable.

Area displays a supplied `position.areaName`; absent a resolved name it shows “Unknown area.” No owner KML/KMZ boundary dataset or configured area resolver was found, so live friendly-name lookup is not implemented and no area is guessed. Device type comes from declared configuration, with a generic “Device” fallback. Demo member devices and verified B001/B002 use Heltec V4; the additive migration fills missing type metadata for those two registered devices and new live provisioning records it.

Shortnames require the additive backend migration `1792110000_member_shortnames.js` and profile hook before deployment. Existing member shortnames remain blank until chosen. No public signup is added; `backend/accounts.py create` prompts for the optional member-chosen value, and authenticated members with a member association can save it through `POST /api/meshlink/profile`. Alias changes do not write radio names or assignment history. The old `MemberBattery` component/estimator and backend voltage/configuration API remain available in source; they are no longer rendered in user-device cards.

## Compact tracker card and recorded sessions — 2026-10-15

Battery sits immediately right of the status pill, at 90% of the pill’s full height, with the battery SVG’s 30:14 aspect ratio preserved. The smaller digits use centered horizontal/vertical anchors in the battery body. Reported integers 00–19 are red, 20–39 amber and 40–99 green, with the outline and digits matching; 100 is a solid green battery with no visible digits. Unknown/invalid values use a neutral outline/dash, never a false zero. Fractional reports are floored for two-digit presentation. A screen-reader label/title retains the full percentage. Inline outline icons follow the owner's [battery](https://lucide.dev/icons/battery), [copy](https://lucide.dev/icons/copy) and [copy-check](https://lucide.dev/icons/copy-check) references without a new runtime dependency.

The coordinate text and adjacent copy symbol form one clickable control. Successful copying shows a check and brief scale/color feedback for 1.6 seconds, with a screen-reader announcement; failure gives a compact manual-copy message. Reduced-motion preferences suppress animation. Area may wrap inside its column while coordinates retain one line.

Session UI currently derives First Seen from the earliest loaded GPS measurement in the latest continuous group and displays its clock time without a relative age; Last Heard uses the device's separate stored contact/receipt time; Time Active is the observed first-to-last GPS span, so silence does not accrue activity. The fixed “Based on loaded GPS points” note is present regardless of the trail checkbox. Invalid/future/unknown clocks are excluded from trail grouping; no points means unknown session start/duration. Duplicate measurement times collapse and the current known position can supplement history.

PocketBase has no session summary yet and snapshots contain only the latest 500 points within 12 hours. Long sessions/trails and their first-seen/active span can therefore be incomplete. A later backend snapshot change should return the complete latest two-hour-gap session and authoritative session start/contact/end/duration metadata. Existing observations are retained, so this need not require a new collection; no backend/API/schema changes are made for this UI update. Friendly-area mapping remains pending the owner boundaries/resolver.

Session clarity/distance follow-up: First Seen is a clock time; Time Active remains the span between the first and last recorded GPS points, so time since the latest point is excluded. For example, a first point 99 minutes ago and last point 12 minutes ago yield 1h 27m active. Distance Travelled sits beside Time Active as one-decimal miles (`1.4 mi`). It sums great-circle distances between consecutive points in the latest session, never connecting across the session's >2-hour gap. The spherical estimate uses a mean Earth radius of 6,371,008.8 m and 1,609.344 m/mile. It excludes elevation/path detail and may be affected by GPS noise or missing points. A single available point shows `0.0 mi`; no timed points shows Unknown. The same 500-point/12-hour snapshot limit can truncate distance along with session duration/start; backend completeness work remains deferred.
