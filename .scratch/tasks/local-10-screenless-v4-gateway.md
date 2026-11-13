# LOCAL-10: build and flash one screenless V4 logging gateway

## Outcome and authority

Implement, review, build and flash the selected screenless Heltec V4 as a
Wi-Fi/MQTT gateway with comprehensive SD recording, an offline log reader, and
a daily custom SD-health packet consumed by MeshLink's backend/API/device card.
This brief is ready to dispatch; preparing it did not build or flash firmware.

The [selected-board owner decisions](../pilot/issues/29-gateway-sd-logging.md#selected-screenless-v4-gateway---2026-11-12)
own scope. Carry forward the parent's capture, timestamp, boot, recovery and
reconstruction contract. Other V4/V3 boards remain separate assignments. Use
one implementation worker and one independent read-only reviewer; keep all
serial/live mutation with the worker.

When this brief is dispatched, source publication and flashing this exact board
are authorized. Prepare the MeshLink changes using the
[application release workflow](../../docs/operations/meshlink-releases.md);
production portal deployment remains a separately selected checked release.
Continue independent software work if hardware/deployment access is unavailable.

## Start and hardware gate

1. Run Git status in both checkouts. Read project instructions, tracker/newest
   session, parent requirements and the
   [flashing handoff](../../docs/operations/board-flashing-handoff.md). Preserve
   unrelated edits. Use short-lived project branches, publish firmware on
   `snorr/develop`, and pin the published commit through the submodule. Inspect
   pinned source rather than silently switching to latest upstream firmware.
2. Use [peripheral bench evidence](../../docs/operations/heltec-v4-peripherals.md)
   for recovery and board identity: **F8:5B:1B:BF:06:38**, ESP32-S3/S3R2,
   **2 MB PSRAM / 16 MB flash**. Reidentify before writing; COM31 is historical.
   Both antennas are owner-confirmed attached. Verify actual external Wi-Fi
   routing against the exact board/manufacturer record if needed.
3. Preserve INA219 **SDA17/SCL18, 0x40** and SD **SCK47/MOSI48/MISO6/CS4**,
   both 3V3/GND. Add a screenless target based on the correct V4 base and audit
   PSRAM, radio/FEM/control pins, buses and partitions. Existing OLED gateway
   secondary I2C uses GPIO4, conflicting with SD CS4; it is unsuitable unchanged.
   Generic SD flags alone do not configure this verified independent SPI bus.
4. Verify the private original 16 MB backup and preserve useful current
   identity/configuration before installation. Original diagnostic app0 is
   **0x140000 bytes**; check image/partition fit before choosing installation
   method. Preserve this board's own identity/keys where present, otherwise
   generate its own first-install identity. Reuse only authorized private radio/
   network settings from other profiles, never another node's security identity.

## Gateway, recording and offline reader

- Apply the selected-board role, five-minute reports, NTP and disabled sleep.
  Explicitly suppress mesh relaying and test it: CLIENT alone does not establish
  that other traffic will not be forwarded. Retain appropriate region/RF/channel
  settings, allow own reports, disable portal/MQTT downlinks and active neighbor
  discovery. Optional sleep support remains off; automatic sleep policy is later.
- Inspect `SnorrNeighborModule.cpp`, `FSCommon.cpp`, radio receive/routing and
  MQTT paths. Capture available raw RX before deduplication, opaque bytes and
  metadata; correlate decoded data without inventing additional receptions.
  Capture local/outbound events before early discard paths. Keep transport
  attempts/outcomes truthful: local send success is not server ingestion.
  Document capture boundaries and unavailable categories.
- Use bounded queues/memory and keep filesystem work off timing-critical radio/
  network callbacks. Record loss/gaps during card absence, write failure and
  overflow. Bound retries and prevent recursive diagnostics or backhaul blocking.
- Choose documented, versioned portable segments with recoverable framing,
  corruption detection and boot/time/configuration provenance. Record before UTC
  synchronization; use per-boot sequence/uptime through clock corrections.
- Implement **capacity-driven deletion only**. Use available card space for
  months of history if it fits; no age expiry, 30-day cap, arbitrary quota or
  percentage-based early deletion. Reclaim only the oldest owned closed segment
  when the next bounded write/allocation needs space. Document minimal filesystem
  headroom, preserve unrelated files, and record eviction ranges/counters. Order
  by durable recording sequence rather than corrected UTC or filesystem mtime;
  treat malformed/foreign files conservatively.
- Deliver a browser reader for copied files with local processing, no uploads/
  CDN dependencies, time/node/event filters and CSV/JSON export. Expose raw bytes,
  duplicates, gaps, corruption, boot boundaries and observed versus reconstructed
  timestamps. Bound memory for multi-month archives and escape received text.

## Daily SD packet and portal integration

Add a separate versioned PRIVATE_APP payload, provisionally **SNSD v1**, alongside
SNNS/SNGH. Preserve **SNGH v1's exact 32-byte contract** and five-minute
connectivity semantics. Document a bounded binary layout and cross-language
golden vectors.

Send once per **86,400 seconds**, allowing admission/jitter/retry while preventing
reboot-driven duplicate bursts. Include source/boot/report identity, sequence,
uptime, UTC/source validity, report interval, card present/mounted/write state,
**whole-filesystem used and total bytes**, and dropped-log count with explicit
counter scope. Preserve 64-bit capacities. Derive percentage only from valid
counts with positive total; unavailable storage is unknown, never fabricated 0%.
Use mounted-filesystem counts consistently; raw physical card size is a different
quantity. Full-but-healthy rotating storage is not automatically a fault.
Archive the node's own SD-health reports too.

Carry this report through private LoRa and encrypted MQTT envelopes; verify
direct own-gateway MQTT and peer-gateway reception. Local-send MQTT can still be
bypassed by earlier airtime admission; test the actual path rather than claiming
guaranteed delivery. Keep its daily schedule independent of SNGH.

Extend existing MQTT adapter parsing, ingest/persistence, deduplication, state API
and infrastructure cards. Start at `backend/mqtt_adapter.py`,
`backend/pb_hooks/{ingest,meshlink,gateway-health}.js`, and
`portal/src/InfrastructurePage.tsx`; inspect current storage/migration patterns.
Validate version/framing/flags, registered sender provenance, field ranges,
duplicates and out-of-order reports. Preserve per-gateway receipts for one
generation; handle reboot/unknown clocks without stale state replacing newer
observations. Keep existing devices and SNGH/SNNS wire formats compatible.

Show **SD used %**, used/total space, logging status, dropped-record count and
last-report age in the existing card. Preserve explicit Unknown/error/last-known
states. Apply daily freshness separately from five-minute connectivity and GPS
freshness; follow the existing cadence-aware health convention. Supply synthetic
demo states. Live portal deployment follows the separately selected release gate.

## Verification and handoff

1. Test meaningful capture boundaries, duplicates/opaque/outbound events, truthful
   outcomes, queue loss, boot/time corrections, corruption recovery and rotation.
   Prove that six-month-old logs survive while free space remains, oldest owned
   closed segments are reclaimed under capacity pressure, and unrelated files
   survive. Simulate full storage in a disposable fixture rather than filling or
   formatting the owner's card. Exercise missing/removed/write-failed storage.
2. Test daily scheduling across reboot/clock acquisition, wire golden vectors,
   malformed/foreign reports, multi-gateway dedup, old arrivals, absent card,
   zero capacity, byte counts above 4 GiB and portal freshness states. Check the
   viewer with large archives and untrusted received text.
3. Run appropriate `scripts/check-project.py` scopes, target build and affected
   backend/portal/release checks. Have the independent reviewer inspect a fixed
   diff for requirements, data loss, blocking, compatibility, privacy and flash
   safety. Resolve substantive findings before flashing.
4. Flash only the identified board with verified image hashes and partition
   plan. Privately provision Wi-Fi from ignored
   `private/bench/v4-gateway-20261112/provisioning.json` and authorized existing
   MQTT/channel inputs; never print/commit credentials. If private inputs are
   unavailable on another machine, request them through the private provisioning
   path while continuing independent work.
   Keep raw location/packet evidence under ignored `private/` or `local-data/`.
5. Through reboot verify complete intended profile/identity, INA219/SD, NTP and
   unknown-time startup, Wi-Fi/TLS MQTT recovery, relay/downlink suppression and
   at least three automatic five-minute cycles. Correlate RX/own reports with
   SD and MQTT evidence. Test daily scheduling offline; if using a temporary
   bench interval for live validation, restore/reboot-verify 86,400 seconds.
   Record failed/unavailable stages. Fixtures do not establish live deployment,
   full physical card integrity, 24-hour operation or solar endurance.
6. Update tracker, sessions, inventory/operations evidence and release records.
   Commit explicit coherent paths and push every completed commit to origin.
   Report hashes, flashed identity, checks/review, push result and unverified
   gates. Close serial handles at handoff.

Battery/solar wiring, charger selection, INA219 calibration, sustained autonomy/
harvest acceptance, automatic historical backfill and other boards remain
separate. Keep optional sleep disabled until coverage tradeoffs are selected.
