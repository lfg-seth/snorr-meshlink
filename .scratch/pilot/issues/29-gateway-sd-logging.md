# LOCAL-10 - Comprehensive gateway SD logging and offline reconstruction

Requested 2026-10-31. Current status belongs to the local tracker. Ticket capture
and requirements interview only; implementation, wiring and flashing await a
selected assignment. Owner confirms two newly purchased screenless Heltec V4s
with external Wi-Fi antenna connections, intended as primary gateways, one per
fire department. Two existing V3s will be repurposed as recording devices;
other future uses remain unspecified. Exact identities/revisions remain to
verify; screenless does not establish the V4-R8 target. Do not infer assignments
from historical G004 records or silently reconfigure existing gateways.

## Owner requirements

- Log "everything" needed to reconstruct operation later from physically
  retrieved cards, including outbound data even when the destination cannot
  be reached. Owner accepts capturing both radio and MQTT/server attempts with
  explicit success/failure/unknown states.
- Operate locally through backhaul outages and handle log rotation.
- Optional later enhancement: broadcast storage capacity as infrastructure
  health. Do not make this a required first-release feature.
- Owner has reused 4/32/64 GB cards, now formatted FAT32, and adapters exposing
  3v3, CS, MOSI, CLK, MISO and GND. Counts, adapter model, card test results and
  assignment to devices remain unknown. No purchase is requested.
- Deliver verified V3/V4 wiring pinouts, matched to exact board variants and
  existing GPS/INA219/display/radio wiring before installation.

## Accepted capture contract - 2026-10-31

Owner accepts first-round recommendations: capture the categories below,
overwrite oldest closed segments when full while recording discarded history,
continue essential device operation through card failures, and deliver an
offline searchable reconstruction/export first. Historical MeshLink import and
automatic backfill are separate follow-ups, not initial acceptance requirements.

Capture received raw radio payloads and metadata, decoded records when possible,
duplicates, locally generated telemetry, outbound radio and MQTT payloads,
queue/drop/retry decisions and transport outcomes, connection transitions,
reboots and relevant diagnostics. Preserve opaque packets when undecodable.
Capture outbound records before network availability checks can discard them.
Do not claim to capture packets the radio never received or prove server
ingestion merely from a local send result.

Each record should retain device identity, boot/session identity, monotonic
sequence/time, wall-clock value and validity/source, original packet timestamps,
direction and correlation identifiers. Record firmware/schema version and
non-secret configuration sufficient to interpret retained data. Keep private
keys, passwords and channel secrets out of logs by default; raw member/location
data stays private and out of Git.

## Recorder role, retention and time - accepted 2026-10-31

- V3 recorders are passive receive-only: no RF forwarding, acknowledgements,
  discovery, telemetry or other automatic transmissions. Capture all observed
  packets within the configured receiver/channel capability; this is not a claim
  to monitor every frequency simultaneously. Optional future storage-health
  broadcasts must not silently override this passive requirement.
- Target 30 days of retained logs on each assigned card, subject to measured
  traffic/record size and capacity. Rotate oldest closed files when full. Report
  actual retained span and gaps; do not promise 30 days on every card untested.
- Owner is not especially concerned about abrupt power loss. Use approximately
  five seconds as a provisional flush target, not a hard maximum-loss guarantee.
  Measure the lost tail and recovery behavior; prioritize reliable recording
  and normal device operation over elaborate zero-loss power hardware.
- Use valid GPS-derived time for log event timestamps when available. Store
  source, validity and synchronization state; distinguish directly attached GPS
  time from radio-derived or other clock sources. GPS hardware/time availability
  on the selected boards is not yet confirmed.
- Preserve a packet's original GPS measurement timestamp separately from the
  recorder's reception/event timestamp. An old position's timestamp must never
  become the current log clock merely because that packet arrived now.
- Start recording immediately at boot even without valid UTC. Always retain
  monotonic uptime, per-boot sequence and a unique boot/session identifier.
  Mark unknown wall time explicitly; record time-acquisition/correction events
  with UTC/uptime anchors. Offline inferred pre-sync timestamps must be labelled
  reconstructed, not silently rewritten as observed GPS times.
- Emit an explicit boot record for every startup, including device/boot identity,
  firmware/schema version, reset reason when available and initial clock/storage
  state. Preserve the boot marker when SD becomes writable; missing-card/data
  gaps must remain visible rather than implying continuous recording.

## Decisions still open

1. Physical board identities/revisions, attached peripherals and verified pinouts.
2. Available GPS/time sources and card assignments; validate retention capacity.
3. Engineering details for the implementation brief: file format, segment limits,
   corruption recovery, retrieval procedure and performance/power measurements.

## Acceptance to develop

- Verify pin assignments and 3.3 V electrical/power suitability for both variants.
- Full card write/read verification plus sustained on-device logging under load.
- Verify V3s emit no RF traffic, including after boot and on received messages.
- Verify boot records, GPS time acquisition/loss/correction, unknown-clock startup,
  and offline reconstruction across multiple boots without merging their uptimes.
- Correlate known RX/TX/telemetry events and unavailable-backhaul outbound records
  with reconstructed output; preserve duplicates and truthful delivery states.
- Validate reboot/unknown clock, card missing/full/removed, write errors, rotation
  and interrupted-power recovery; measure any lost tail and dropped-log counters.
- Verify logging cannot silently block essential radio/gateway work; quantify
  memory, airtime, latency and power effects. Test the actual card sizes used.
- Offline reader must detect gaps/corruption and preserve original observation
  times. Any future import must not present historical positions as fresh.
- Optional health design can include total/used/free bytes, mount/write status
  and loss counters; interval and RF cost remain undecided.

Related: LOCAL-4 gateway readiness, LOCAL-6 firmware releases, GH-3 outage/local
viewing. Existing sniffer tooling may supply reusable framing/replay concepts;
reuse is to be assessed, not assumed compatible.
