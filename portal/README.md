# Portal development

React + TypeScript + Vite with MapLibre. This is a responsive four-page **synthetic prototype**. All members, observations, sites and actions are fictional. Changes live in browser memory and reset on refresh. The [local PocketBase backend and Python simulation worker](../backend/README.md) now provide authentication and persistent observations/assignments/messages. A live radio feed is not connected. Standalone demo mode still resets on refresh.

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

For the authenticated portal with saved records, complete the one-time [backend setup](../backend/README.md), then run `python3 backend/launch.py` from the repository root. It starts the API, simulation worker and portal in one terminal. Open `http://127.0.0.1:5173` and choose **Backend sign in**; Ctrl+C stops the three processes together. Private per-process logs live under ignored `local-data/backend/logs/`. The standalone `npm run dev` command above remains useful for frontend-only work.

## Review the prototype

Navigation uses `#map`, `#users`, `#messages` and `#infrastructure`, including browser back/forward and direct links. The common role selector previews Admin and Member (Demo Casey); it is not authentication or access enforcement. The feed toggle simulates availability, without generating fresh GPS or telemetry observations on reconnect.

- **Map:** six fictional trackers; searchable list; select a list row or pin to inspect measurement time, receipt time, last contact, coordinates and reported battery separately. GPS age updates every second and becomes stale at 15 minutes. Unknown-age positions remain explicitly unknown; never-seen devices have no pin. Switch between USGS topo and aerial imagery, fit the training area, or enable the illustrative infrastructure layer. Opt-in history starts at four hours, offers one/twelve-hour windows, and shows measured points with inspectable times and the carrier at measurement time. Dashed estimated connections break at gaps over 15 minutes. A failed basemap or unavailable WebGL leaves the list and recorded coordinates available.
- **Users:** claim/release/transfer tracker assignments and inspect dated history. Member preview can self-claim only free devices and release its own device; Admin can transfer, closing conflicts on both sides. Short names remain fixed. Assignment/release produces a separate simulated long-name job; only the latest job per device can simulate read-back or failure. Transfers also create a release-name job for a carrier's previous tracker.
- **Messages:** chronological shared channel, author-prefixed simulated sends, incoming-message notification and unread badge across pages. Drafts survive page navigation and feed outages within the same browser session. Reconnect never sends a draft automatically. Gateway submission is explicitly unconfirmed radio/human receipt; live payload limits and expiry remain open. Use the footer's incoming-message control to try notifications from another page.
- **Infrastructure:** filter four fictional devices by role; inspect capability-specific current, stale, awaiting-first-reading and not-equipped states, voltage observations, event/audit history and declared battery/solar/antenna configuration. Acknowledge an intrusion without clearing it, or resolve it as Admin with a note. Later normal sensor readings do not clear the latched incident. Admin can record illustrative voltage thresholds with a higher recovery threshold. Rules are configuration previews; automatic low-battery/missing-report/reconnect evaluation and fresh-evidence recovery await ingestion. Infrastructure alerts use silent persistent badges, with no toasts or sound.

On narrow screens, use **Hide/Show trackers & detail** to give the map more room. Marker breathing follows the agreed age bands, stops for stale/unknown fixes, and respects reduced motion. Status text remains available without animation or color.

## Source files and TypeScript

`.ts` contains ordinary JavaScript plus types; `.tsx` also contains React markup. Types describe expected data and disappear from the production JavaScript. They do not validate network input. For example, `measuredAt: string | null` means a timestamp can be a string or explicitly unknown; `import type` brings in a type without runtime code.

- `src/main.tsx`: shared shell and browser-memory state (assignments, drafts, incidents and events).
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
