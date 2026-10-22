# Neighbor signal visibility

Owner activation: 2026-10-21. [Hide stale neighbor signals and prevent cached reports refreshing link activity](https://github.com/lfg-seth/snorr-meshlink/issues/47) follows the [B002/G001 diagnosis](neighbor-report-freshness-20261021.md). The owner requests correcting misleading freshness and showing no neighbor signals two or more hours old anywhere on the portal. This activates the cutoff portion of [#43](https://github.com/lfg-seth/snorr-meshlink/issues/43); its separate name/strength/distance layout remains deferred.

**Approach under review, later October 21: PR #50 is a draft, not a complete deployable solution.** Its absolute-time filter hides every current live signal. The owner now questions that design and requests simpler alternatives. Absolute source timestamps are one option, not an established requirement for fixing the misleading cached-table behavior. The simpler-options discussion below supersedes the timestamp-only recommendation; no replacement design is selected. The earlier release-ready handoff remains superseded.

## Draft absolute-time visibility contract (not an approved final design)

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

Published application source **a9ae4b9** is reviewed in [PR #50](https://github.com/lfg-seth/snorr-meshlink/pull/50). An isolated server stage at `/opt/meshlink-stage-neighbor-a9ae4b9` passes lockfile installation, all **52 tests**, TypeScript and the live production build on pinned **Node 22.23.1**. No production files/services are changed. The application's build files match the desktop build names. After incorporating concurrent record-only main commit b645012, [Portal CI](https://github.com/lfg-seth/snorr-meshlink/actions/runs/39682109808) passes for merge commit **4615069**; source remains identical to the staged application.

A private authenticated production snapshot contains the API's latest **2,000 signal rows**, including one B002/G001 row. Replaying those rows through the actual staged filter on pinned Node yields **zero visible rows**, removes the B002/G001 relationship, and leaves all input rows byte-for-byte unchanged. A separately timestamped positive control remains visible before its exact two-hour cutoff and disappears at it. This checks the intended strict visibility consequence on real data without inventing timestamps for those rows.

Production remains application **fa03550**; no deployment, schema, backend, radio or configuration change is performed in this implementation checkpoint. Native browser/mobile review and trustworthy radio hearing timestamps remain separate. Source and release evidence are tracked in #47.

## Current firmware compatibility check

The owner asks whether installed device firmware supports the correction. The custom SNNS collector on the RAK reporters and G001/G002 already supplies per-neighbor **hearing age at encoding**, reporter **boot ID**, **sequence**, **uptime**, and a **thirty-minute collector expiry**. These fields support relative freshness and prevent treating the standard table's publication as a fresh reception. They do not by themselves establish an absolute source hearing clock through delayed delivery. Standard NeighborInfo omits each entry's hearing age and last-reception clock.

Private live archive inspection confirms that both gateways' own local SNNS envelopes also have plausible Unix `rx_time` clocks, within about one second of receipt in the sampled packets. An initial interpretation of these as packet-creation clocks was too broad. [`Router::allocForSending`](../../firmware/src/mesh/Router.cpp) initially stamps a clock, but [`sendLocal`](../../firmware/src/mesh/Router.cpp) processes broadcast packets through `handleReceived`, which **overwrites `rx_time`** after payload encoding. Forwarded reports acquire the receiving gateway's clock there as well. MQTT queues preserve the serialized envelope afterward; that does not restore the reporter's original encoding clock or establish a general delay bound. Neither the current packet metadata nor the SNNS payload justifies treating every such clock as the original reporter's encoding time.

For an absolute cutoff that accounts for transport delay while retaining valid signals, the reporting receiver needs to supply a trustworthy source hearing timestamp or an encoding timestamp tied to its relative hearing ages, with unknown/invalid clock quality explicit. Ingestion must preserve that provenance, and the portal must expire on that evidence. This is a firmware/report-contract and ingestion prerequisite, not just a display filter. Member nodes such as B002 do not need to report neighbors for a gateway/repeater to observe them; this does not imply a required member-node firmware update.

No source firmware, device settings or hardware are changed during this compatibility review. The bounded frontend implementation remains available in draft PR #50, with its earlier passing tests accurately scoped to visibility behavior. No compatible timestamp pipeline or complete end-to-end fix is claimed. The owner has not approved deployment of the hide-all checkpoint, and it remains undeployed.

## Firmware follow-up tickets

On October 21 the owner requests separate tickets for the gateway and repeater firmware fixes:

- [Fix gateway firmware neighbor timestamps for reliable signal expiry #51](https://github.com/lfg-seth/snorr-meshlink/issues/51): G001/G002, dedicated Heltec V3 gateway target, source timing preserved through local routing and MQTT queue/reconnect; preserve LoRa TX disabled and each board's profile.
- [Fix repeater firmware neighbor timestamps across relay and backhaul delays #52](https://github.com/lfg-seth/snorr-meshlink/issues/52): R001–R005 RAK4631, source timing that survives LoRa forwarding and gateway delay, with unknown/changed clocks explicit. Preserve R004's separate INA219 diagnostic state until a specifically authorized rollout.

Both are Ready corrective follow-ups, unassigned and unclaimed; ticket creation does not start implementation or authorize builds/flashing. They must coordinate the same bounded, versioned report contract. Each records source/build tests and separately authorized hardware/receipt verification, preserving keys/configuration and distinguishing measured evidence from planned acceptance criteria.

[#47](https://github.com/lfg-seth/snorr-meshlink/issues/47) retains backend ingestion/provenance, portal behavior and final end-to-end acceptance; its useful completion depends on the source-timing capability in #51/#52. Draft PR #50 remains undeployed. The firmware tickets do not request member-node changes or activate #43's deferred card layout.

## Simpler alternatives raised by the owner

The owner questions the timestamp-first design and asks whether stale readings can simply be excluded from storage. This is discussion, not authorization to implement a new design or delete history. The firmware tickets now mark their initial timestamp criteria as a proposal under review. Their current GitHub status supersedes the creation-time Ready statement above.

The measured B002/G001 failure is a cached **standard NeighborInfo** table admitted as new current-link evidence. A missing absolute timestamp does not prove that synchronized device clocks are the only fix. The existing custom collector already removes entries at **thirty minutes**, using unsigned elapsed `millis()` time in `NeighborSignals::expire`; it also exports relative hearing age, boot ID, sequence and counts. Standard encoding deliberately omits per-entry last-reception clocks. [Official NeighborInfo documentation](https://meshtastic.org/docs/configuration/module/neighbor-info/) independently describes periodic table publication, with the default six-hour interval; the project's installed source is authoritative for its exact behavior.

| Option | Benefit | Remaining boundary |
| --- | --- | --- |
| Exclude standard cached tables from current signal state; use custom SNNS age/observation evidence and a two-hour portal expiry | Smallest direct fix for B002/G001; existing custom firmware already supplies relative age | Receipt plus relative age does not include unseen transport delay; label that uncertainty until the transport bound is established |
| Expire source entries and queued neighbor snapshots using monotonic elapsed durations; discard expired/backlogged snapshots and produce fresh passive reports after reconnect | Prevent old data entering the live path without requiring synchronized device clocks | Must test/bound every buffering path that can delay these reports, including radio, gateway MQTT and worker retries; observation/boot/sequence handling must prevent stale reactivation |
| Add absolute source hearing/encoding timestamps and explicit clock quality | Allows delayed historical reports to retain their source-time meaning | Adds source clock acquisition, validity, step/reboot handling and format/ingestion changes |

Simply deleting database rows older than two hours does not solve the original bug: a newly received standard table can insert the same old signal again. Prefer a small **current neighbor state** that only eligible new hearing evidence can update; preserve the separately authorized raw archive/history. The current-state row can expire or be removed without erasing raw receipts.

For ordinary online display, relative age at encoding plus elapsed time since the original receipt gives a useful age estimate; repeated table publication, duplicate delivery or a higher report sequence alone must not reset it. A boot-scoped last-hearing uptime can be derived from report uptime minus hearing age, with integer rounding/rollover and entry-reset handling tested. This is relative evidence, not an invented measured UTC timestamp. First receipt of a report delayed by hours still cannot establish current hearing: dropping stale transport backlog or bounding its residence is necessary for a strict hearing-age limit.

In particular, synchronized device clocks are **not mathematically necessary** when a verified end-to-end transport-delay bound exists. A conservative expiry can subtract both hearing age at encoding and the verified maximum transport delay from the allowed two-hour lifetime. No such bound is established by the current short bench captures; do not claim the strict limit from receipt age alone. Alternatively, absolute source clocks can carry the missing source-time information. The trade-off is between clock handling and transport-expiry guarantees.

Recommendation for owner review: first stop standard tables refreshing current relationships; use the existing custom relative evidence; scope firmware work around stale queue/source expiry before requiring a new UTC payload. Keep PR #50 undeployed and do not claim this recommendation already passes outage/replay acceptance. No application/firmware changes or new measurements are performed during this comparison.
