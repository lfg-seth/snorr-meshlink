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

## Decisions still open

1. Physical board identities/revisions, attached peripherals and verified pinouts.
2. V3 recorder radio role: passive receive-only versus ordinary participating
   mesh node. Repurposing as a recorder does not by itself select RF behavior.
3. Required retention between card retrievals and tolerable abrupt-power-loss
   tail; these determine capacity, rotation and flush policy.
4. File format, segment limits, corruption recovery and card retrieval procedure;
   acceptable performance/power overhead to specify before implementation.

## Acceptance to develop

- Verify pin assignments and 3.3 V electrical/power suitability for both variants.
- Full card write/read verification plus sustained on-device logging under load.
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
