# Show neighbor signal connections on the map

Type: task
Status: resolved
Assignee: map-neighbor-signals-session-2026-10-16
Parent: ../map.md
Blocked by: none

## Request

Add a toggle matching and adjacent to Fit area. When enabled, connect mapped radio neighbors with colored lines and signal labels. Selecting a line opens a card with the directional relationship, readings, measurement/report times and related context.

## Comments

2026-10-16 — Owner requests two endpoint buttons on the relationship card, each opening its node card. Reopened for this navigation refinement and verification.

2026-10-16 — Owner requests a refinement: remove all line labels, keep only the legend by default with its explanation behind an info button that resizes only the legend, preserve node-click selection and list compact relationship/pill rows in node cards linking to relationship details. Reopened for implementation and checks.

2026-10-16 — Owner brings this map feature forward using the existing database-backed signal observations. Preserve unrelated working-tree changes and leave firmware/reporting improvements parked. Implementation and interaction checks are in progress; production deployment is outside this request.

## Answer

2026-10-16 — Implemented locally with the existing API observations. The toggle starts off, sits immediately after Fit area, shares its styling and exposes pressed state. Enabled mode draws one line per mapped pair plus a native button label showing direction and weakest known latest SNR. Line clicks or keyboard/touch label selection open the existing responsive sheet pattern; selected connections are emphasized. Turning the layer off removes lines/labels and closes only a selected signal sheet. Basemap recreation and live updates preserve the enabled layer; feed loss retains saved observations with an offline notice.

- A mapped pair requires distinct, known observer/heard-node identities and valid coordinates for both. Never substitute `originalSourceDeviceId` for an unknown heard node. Unmappable observations are counted in the legend. Colocated labels receive offsets without changing endpoint coordinates.
- Keep observations grouped by pair and choose the latest per direction and report source using hearing time when supplied, otherwise receipt time; use receipt time and record ID to break ties. Delayed receipts with older known hearing times cannot replace newer known measurements. Do not carry an older signal into a latest reading whose value is absent.
- The display metric is the minimum finite SNR across those latest readings. Green ≥5 dB, amber 0–<5 dB, red <0 dB and gray unknown are explicit UI bands chosen for this overlay, not technical receiver thresholds, calibrated coverage or delivery reliability. RSSI is shown in the card independently. Negative/zero SNR remains a real value. Reverse arrows require recorded reverse observations.
- The card retains directional SNR/RSSI, source, direct/relayed/unknown path, original sender, separate observed/received dates and uncapped relative ages, loaded observation count and endpoint location context. Missing hearing timestamps stay unknown. Tracker endpoints use last saved GPS, and infrastructure uses configured locations with planned status disclosed. Lines are geographic connectors, not measured RF propagation paths or endpoint locations at hearing time.
- Source/layer interactions follow the official [MapLibre click-event example](https://maplibre.org/maplibre-gl-js/docs/examples/display-a-popup-on-click/); a transparent wider line target supports easier pointer selection, and native label buttons provide keyboard access without a remote glyph service.

Full frontend tests, TypeScript/default live build and explicit database-demo build pass. Unit checks cover grouping/direction/source handling, delayed/missing readings, zero/negative/nonfinite signals and invalid/unmapped endpoints. React DOM checks cover toggle placement/state, line and label selection, weaker reverse color, card times/values, live updates, basemap recreation, empty data, retained offline readings, exclusive tracker/signal selection and desktop/mobile dialog APIs. Whitespace checks pass. Browser inventory is empty, so actual WebGL rendering, touch/focus and responsive visual placement remain unverified; the existing MapLibre bundle warning remains. No live signal ingestion, deployment, firmware/database change, service start, commit or push performed.

### Owner-requested refinement — 2026-10-16

This supersedes the initial line-label and toggle-dismissal behavior above. The map draws only colored lines; no signal label markers remain. Its legend shows the color key, with an accessible info button to disclose explanatory text. The legend is positioned outside the toolbar's layout flow at a fixed width constrained to available space, and toolbar items align at the top. Help expands only the legend's own height, without resizing the other controls.

Tracker and infrastructure map cards now include a Relationships list. Each selectable row contains only its directional relationship and colored SNR pill, with all measurements/context retained in the separate relationship sheet. Node marker clicks stop propagation, and line click handlers ignore events originating from node markers, preserving node selection where lines meet pins. Relationship rows also provide keyboard access to details. Lists and detail selection are independent of the overlay toggle; hiding the layer leaves the selected card open. Known endpoint relationships survive missing/invalid coordinates, while drawing a line still requires valid locations for both; missing final-hop identities remain omitted rather than substituted from original-source metadata.

Frontend tests, typecheck, default live build and explicit demo build pass. Updated grouping tests distinguish known unmapped relationships from drawable connections. React checks cover absence of line labels, info disclosure/CSS isolation, tracker and infrastructure marker precedence, compact row contents, row-to-detail selection with the overlay off, live measurement updates, mobile/desktop dialog APIs, missing GPS, unknown locations, empty lists and retained cards through layer hiding. Native browser rendering/layout remains unverified and the existing MapLibre bundle warning remains. No service, deployment, database, firmware or Git-history changes performed.

### Relationship endpoint navigation — 2026-10-16

Add two buttons at the top of each relationship card, labelled Open plus the endpoint's radio/node label. Each replaces the relationship sheet with that endpoint's tracker or infrastructure card. Tracker selection shares the marker selection handler, preserving parent selection and existing trail-clearing behavior. The node's Relationships list can reopen the relationship; no extra stacked sheet is introduced. Buttons use a two-column layout with 44px minimum height and accessible node-card labels.

Full frontend tests, TypeScript and default live build pass. Existing interaction checks now exercise both endpoint buttons, exactly one open card, return through the Relationships list, overlay-off navigation and desktop/mobile dialog APIs. Native browser visual review remains unverified; existing MapLibre bundle warning remains. No deployment, service start, database/firmware change, commit or push performed.

### Deployment follow-up — 2026-10-16

Owner authorizes publishing/deploying all accumulated changes. Application source `3ca3a94` is pushed to `origin/main` and deployed to the LXC, including these frontend/backend/worker changes and the separate hosted database demo. Local/server frontend and backend checks, exact public assets, protected live/demo API separation and isolated live/demo backup recovery pass. Live signal rows remain empty pending real ingestion; no synthetic rows enter live state. Native browser/WebGL/mobile and field verification remain outstanding. [Release evidence](../../../docs/operations/portal-lxc.md#gps-neighbor-maps-battery-history-and-database-demo-release--2026-10-16).
