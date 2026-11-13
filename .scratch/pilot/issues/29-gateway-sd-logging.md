# LOCAL-10 - Comprehensive gateway SD logging and offline reconstruction

Requested 2026-10-31. Current status belongs to the local tracker. Ticket capture
and requirements interview only; implementation, wiring and flashing await a
selected assignment. The 2026-11-12 section below selects one V4's build brief;
the broader fleet scope remains separate. Owner confirms two newly purchased screenless Heltec V4s
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
- Initial capacity target: 30 days, subject to measured traffic/record size and
  capacity. The 2026-11-12 clarification below rules out an age cap: retain all
  history that fits and rotate only when space is needed. Report actual retained
  span and gaps; do not promise retention on an untested card.
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

## Selected screenless V4 gateway - 2026-11-12

Owner requests a build-and-flash prompt after the requirements interview.
[Dispatch brief](../../tasks/local-10-screenless-v4-gateway.md) defines execution
and verification; this interview does not itself build or flash firmware.

- Selected board is screenless S3R2 V4 **F8:5B:1B:BF:06:38**, 2 MB PSRAM /
  16 MB flash, with verified INA219/32 GB SD connections in the
  [peripheral bench record](../../../docs/operations/heltec-v4-peripherals.md).
  G007 is an acceptable temporary name; owner plans later renaming. Preserve
  hardware/security identity independently of the display name.
- Upload received traffic through private Wi-Fi/MQTT and transmit own reports.
  Disable mesh relaying and portal/MQTT downlinks. Both external Wi-Fi and LoRa
  antennas are owner-confirmed attached.
- Device/battery, INA219 power, passive SNNS neighbor signals and SNGH backhaul
  health use a **300-second baseline**, subject to airtime/jitter. Logging is
  continuous. Keep Wi-Fi/LoRa awake; optional sleep support remains disabled.
  Active discovery and custom automatic sleep policy are outside this build.
- **Retention is capacity-driven, with no age limit.** If six months fits,
  retain six months. Delete oldest owned closed segments only when space is
  needed to continue writing. Preserve unrelated files; no automatic format,
  30-day expiry, arbitrary quota or early percentage threshold. Continue gateway
  operation through SD faults and record/report gaps.
- Use **NTP; no GPS is required on this gateway**. Preserve truthful unknown
  UTC/boot/uptime and received GPS measurement times separately. This overrides
  the earlier GPS-first time preference for this selected board.
- Deliver portable versioned logs and a local browser reader with CSV/JSON
  export. Preserve raw bytes and decoded data; process copied files locally.
- Send **one custom SD-health packet per day**, superseding the proposed text
  message. Integrate with MeshLink ingestion/API/existing device card: whole-card
  used percent, used/total bytes, logging state, dropped-log count and report age.
  Missing/invalid capacity stays unknown. Daily storage freshness is separate
  from five-minute backhaul health. Existing wire contracts remain compatible.
- Intended power: **8 or 12 existing project 18650 cells**, **one or two
  5 V / 5 W panels**. Charger/protection/topology, installed allocation, INA219
  shunt/path and calibration remain unverified. Firmware acceptance does not
  establish solar endurance or approve pack wiring.
- Provision owner-supplied Wi-Fi and authorized MQTT/channel secrets privately,
  outside saved prompts/source/diagnostics. Other V4/V3 boards and automatic
  historical portal backfill remain separate assignments.

## Remaining engineering and broader-fleet decisions

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
