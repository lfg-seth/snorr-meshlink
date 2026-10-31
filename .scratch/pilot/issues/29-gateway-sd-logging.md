# LOCAL-10 - Comprehensive gateway SD logging and offline reconstruction

Requested 2026-10-31. Current status belongs to the local tracker. Ticket capture
and requirements interview only; implementation, wiring and flashing await a
selected assignment. Targets: gateway Heltec V4 devices (count/identities to
confirm) and two Heltec V3 devices. Do not infer current gateway assignments
from historical G004 records.

## Owner requirements

- Log "everything" needed to reconstruct operation later from physically
  retrieved cards, including outbound data even when the destination cannot
  be reached. Clarify whether "gateway" here means MQTT/server or another radio.
- Operate locally through backhaul outages and handle log rotation.
- Optional later enhancement: broadcast storage capacity as infrastructure
  health. Do not make this a required first-release feature.
- Owner has reused 4/32/64 GB cards, now formatted FAT32, and adapters exposing
  3v3, CS, MOSI, CLK, MISO and GND. Counts, adapter model, card test results and
  assignment to devices remain unknown. No purchase is requested.
- Deliver verified V3/V4 wiring pinouts, matched to exact board variants and
  existing GPS/INA219/display/radio wiring before installation.

## Proposed capture contract - awaiting interview answers

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

1. Reconstruction scope and destination meaning; raw/decoded/debug boundaries.
2. Physical board identities/revisions and existing attached peripherals.
3. When capacity is exhausted: overwrite oldest closed segments, or stop logging
   and preserve history? Required retention duration and maximum acceptable loss.
4. Manual offline reconstruction/export only, or later automated backfill?
5. Card/write failure behavior and acceptable performance/power overhead.
6. File format, segment limits, flush policy, corruption detection and recovery,
   retrieval workflow and privacy/access requirements, after scope is settled.

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
