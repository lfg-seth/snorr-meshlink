# B002/G001 neighbor report freshness

Read-only diagnosis, 2026-10-21 Pacific. Tracking: [Diagnose recent B002/G001 neighbor reports while radios are isolated](https://github.com/lfg-seth/snorr-meshlink/issues/47).

The owner reports physical isolation with no possible B002/G001 link, yet the relationship shows a report about 36 minutes old. Production database, authenticated state and privately decoded archived packets reproduce the recent receipt with no corresponding hearing timestamp. No radio, firmware, application or server configuration is changed.

## Measured evidence

- The latest B002 → G001 row is standard `neighbor-info`, received **2026-10-21 13:46:49.434 Pacific** (`20:46:49.434Z`), SNR **6.25 dB**, RSSI unknown and `observedAt = null`. Authenticated state contains this same row for the pair.
- G001's preceding standard report arrives at **07:46:49.230 Pacific**, also listing B002 at **6.25 dB**. Both packets identify G001 as sender, reporter and last sender, with different packet IDs. Both are non-retained/non-duplicate, and packet clocks are within about one second of MQTT receipt. This rules out an old retained/replayed packet or a different reporter as the explanation for these two receipts; it does not establish a fresh B002 reception.
- Both decoded standard reports advertise **21,600 seconds (six hours)** and omit B002's last-reception time and interval. The saved October 19 G001 profile independently records the same configured reporting interval; it is historical configuration evidence, not a new radio readback.
- The latest richer `snns-v1` B002 → G001 row arrives at **06:44:52.671 Pacific**, boot **380571083**, sequence **524**, uptime **39,486 seconds**. B002's hearing age is already **1,772 seconds (29m 32s)**, count **314**, RSSI **−51 dBm**, SNR **6.25 dB**. Preceding sequences 523/522 have the same count/readings and ages 1,697/1,622 seconds. There are no later stored B002/G001 SNNS rows in this inspection. No absolute last-heard clock is supplied; subtracting hearing age from MQTT receipt would assume transport timing and is not recorded as a measured clock.

## Cause and interpretation

The pinned [`NeighborInfoModule.cpp`](../../firmware/src/modules/NeighborInfoModule.cpp) periodically republishes its cached neighbor table. Its cleanup removes entries only after twice the neighbor's stored broadcast interval. An entry without a known advertised interval initially uses the observer's configured interval; at G001's six-hour setting that permits twelve-hour retention. The exact current per-entry interval is not available in these packets, so twelve hours is a source-supported mechanism, not a measured expiration deadline for this entry. Standard report encoding deliberately omits each entry's last-reception timestamp.

The separate richer [`NeighborSignals`](../../firmware/src/modules/SnorrNeighborSignals.h) collector expires entries after thirty minutes. Its growing B002 age with unchanged observation count, followed by no further B002 row, supports the cached-standard-entry explanation. The live capture does not expose G001's in-memory standard table or prove the precise physical last reception.

The portal preserves unknown hearing times, but [`signalConnections`](../../portal/src/signal-links.ts) chooses the latest row per receiver/heard node/source using receipt time when hearing time is unknown. Both standard and richer reports use source `neighbor`. Consequently, a later standard table publication replaces the older, richer reading in the displayed relationship. [`SignalLinkDetail`](../../portal/src/SignalLinkDetail.tsx) correctly labels its clock **Report received**, but the relationship's presence and refreshed report age can suggest current connectivity.

**The recent time means the portal received G001's neighbor table then. It does not mean G001 heard B002 then, and these reports supply no evidence of a new link during the isolation period.**

## Reproduction and limits

Read-only SQLite selection of the latest `observerDeviceId='g001'`, `heardDeviceId='b002'` row, ordered by descending `receivedAt`, produces the standard row above. Asserting a populated hearing clock fails with `REPRODUCED: B002/G001 has a recent report receipt but no corresponding hearing timestamp`. Independent authenticated `/api/meshlink/state` and encrypted archive decoding corroborate the same identities, SNR and receipt. The assertion demonstrates why recent receipt cannot certify recent hearing; unknown clocks are intentional, not a database validation defect.

This session answers the diagnosis only, so no implementation regression test or fix is claimed. Physical isolation is owner evidence; no RF/serial experiment is performed. Production application remains `fa03550`. Private keys, full payloads, credentials, locations and tracks remain outside Git.

The separately deferred [two-hour node-card cutoff request](https://github.com/lfg-seth/snorr-meshlink/issues/43) remains parked. When activated, it must distinguish hearing activity from table publication: a cutoff based only on `receivedAt` would refresh this stale relationship every six hours. A corrective implementation should also prevent a standard report with unknown hearing freshness from presenting an old signal as a newly measured link; exact behavior remains to select when authorized.
