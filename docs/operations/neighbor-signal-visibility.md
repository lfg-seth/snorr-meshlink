# Neighbor signal visibility

Owner activation: 2026-10-21. [Hide stale neighbor signals and prevent cached reports refreshing link activity](https://github.com/lfg-seth/snorr-meshlink/issues/47) follows the [B002/G001 diagnosis](neighbor-report-freshness-20261021.md). The owner requests correcting misleading freshness and showing no neighbor signals two or more hours old anywhere on the portal. This activates the cutoff portion of [#43](https://github.com/lfg-seth/snorr-meshlink/issues/43); its separate name/strength/distance layout remains deferred.

## Visibility contract

- A signal appears only with a valid, explicitly zoned absolute hearing timestamp (`observedAt`), before or equal to its receipt and no more recent than the current clock. Receipt must also be valid and not in the future.
- Hide at **two hours exactly** since hearing. Recent receipt, ingestion, table publication or reappearance never refreshes the hearing clock. Hide unknown, invalid, future or inconsistent clocks.
- SNNS v1 hearing age is relative to encoding and excludes transport delay. It cannot prove a hard two-hour bound. Standard NeighborInfo supplies neither per-neighbor age nor an absolute clock. Both are hidden when `observedAt` is unknown, including a just-delivered zero-age SNNS report. No inferred hearing timestamp is written or displayed.
- One shared filter feeds main-map lines, node-card relationships, relationship readings and the Infrastructure neighbor table. The map recomputes as the existing one-second browser clock advances, including when polling fails. Expiring a selected relationship removes its details and minimap; individual expired directions stop affecting arrows and weakest-SNR color.
- No stored reports, observations, MQTT archives, receipts or configuration are deleted or rewritten. The API/archive can retain history even though the portal hides it.

The table and map help explain the cutoff and unknown-time exclusion. Empty node cards say **No recent neighbors with a known hearing time**. Relationship details label the separate clock **Report delivered**, with an explicit note that delivery does not refresh signal age. Hiding a row does not establish radio failure or an absent physical link.

## Current live consequence

Read-only inspection on October 21 finds **14,027 stored signal rows and zero populated hearing timestamps**, all with source `neighbor`. The correction therefore hides all current live neighbor signals, including B002/G001. This is intentional under the hard age limit; it is not a radio outage or data loss. Existing nine-device identity/configuration/history remains intact. Neither current report format establishes absolute hearing time, so useful verified current signals need a separate ingestion/firmware timestamp improvement. This change does not invent clocks, modify radios or claim that follow-up is complete.

## Verification and release state

Before the fix, four focused actual relationship-builder checks fail for the captured B002/G001 pattern, exact two-hour expiry, unknown/invalid/future clocks and newer cached reports displacing verified readings. A real MapPage/NeighborTable DOM test fails with four rows visible instead of one. After the fix, all five pass.

Desktop Node 25.6.0: **52 portal tests**, TypeScript and production build pass using `npm run check`. The DOM regression advances only `now`, preserving the same link/device array references while offline, and verifies removal from map lines, node cards, the selected relationship sheet and the table at the exact boundary. Fresh verified data reappears correctly. Existing signal tests retain directional/weakest-SNR behavior, late sequence ordering, unknown endpoints and missing coordinates for eligible timestamped observations. Positive fixtures describe timestamped inputs; they do not imply live SNNS timestamp support.

Production remains application **fa03550**; no deployment, schema, backend, radio or configuration change is performed in this implementation checkpoint. Native browser/mobile review and trustworthy radio hearing timestamps remain separate. Source and release evidence are tracked in #47.
