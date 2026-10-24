# LOCAL-4 - Heltec V3 gateway hardware and production readiness

Created 2026-10-23. Status: Next; owner requests ticket creation and scope.
Plan and characterize existing Heltec V3 gateways before mountain placement.
No hardware installation, purchase, flash, print or field result is claimed.

## Owner-selected hardware direction

- Heltec V3, with INA219 sensing and a Muzi whip antenna.
- Four or eight 18650 cells per gateway; count, capacity, pack topology,
  protection, charge controller and actual allocation remain to be selected.
- Power option A: two 60 x 100 mm solar panels per gateway.
- Power option B: an external larger 5 V USB solar charger advertised as 6 W.
  Model and measured sustained output are unknown; 6 W is an advertised rating.
- Design and 3D print a gateway case that supports the selected power option.

This is a planned configuration, not a claim that G001/G002 have been rebuilt.
Their last confirmed installed packs remain one 1000 mAh LiPo each.
[Hardware page](../../../docs/hardware/heltec-v3-gateway.md),
[inventory](../../../records/inventory.md).

## A. Measure power and select the supply

- [ ] Identify board revision, cells/holders, panel electrical ratings, USB
  charger model, antenna model/connector and INA219 module/shunt from available
  stock. Record confirmed quantities separately from alternatives/unknowns.
- [ ] Draw the full battery/charging/load path before selecting pack topology.
  Verify compatible input voltages, polarity, cell protection, charge behavior,
  reverse-current behavior and temperature limits against primary vendor data.
  Four/eight cells does not establish series versus parallel wiring.
- [ ] Characterize battery-side and USB-input power separately, with a reference
  meter and known INA219 placement/polarity/calibration. A single branch sensor
  does not automatically measure both solar production and net battery current.
- [ ] Measure idle RX plus Wi-Fi/MQTT connected, normal forwarding/SNNS,
  Wi-Fi association/retry, broker outage/reconnect/queue drain, cold boot and
  display/Bluetooth configurations. Capture average Wh/day, current peaks and
  brownouts, not just one instantaneous mA reading. Preserve receive-only RF.
- [ ] Compare four/eight-cell usable energy using verified capacity and measured
  load; agree autonomy/night/no-sun and recovery criteria before acceptance.
  Measure both solar options through the actual charging path under recorded
  conditions, including shade/intermittent input, depleted-pack recovery and
  charging while operating. Do not infer output from panel area or a 6 W label.
- [ ] Record measured energy margin and selected supply in field results and
  inventory. Wi-Fi draw is a hypothesis to characterize; solar sufficiency and
  unattended runtime are currently unknown.

## B. Gateway enclosure and 3D print

- [ ] Measure real board, four/eight-cell holders, INA219, charging electronics,
  connectors, antenna bulkhead and panels before CAD. Select a common enclosure
  with interchangeable mounts/lids or separate variants based on measured fit.
- [ ] Provide service access to USB/reset, protected cable routing and strain
  relief, secure batteries/PCB, antenna clearance, mounting and panel attachment.
  Support two small panels or a sealed external USB solar-input connection.
- [ ] Select print material and wall/seal/fastener design for expected sun,
  temperature and weather; address condensation, drainage/venting, heat and
  battery service. Printed geometry alone does not establish an IP rating.
- [ ] Save editable CAD, dimensioned drawings, print orientation/settings and
  STL/3MF. Print a fit prototype, inspect assembled clearances, then test mounting,
  cable retention, weather exposure and operating temperature against agreed
  criteria. Iterate before calling it field ready.

## C. Firmware, configuration and security

One firmware repository supports both device families, but separate targets
produce separate binaries: RAK4631 uses nRF52840; Heltec V3 uses ESP32-S3.
The existing `heltec-v3-gateway` target extends ordinary `heltec-v3` and enables
`USERPREFS_SNORR_NEIGHBOR_SIGNALS=1`. Gateway behavior also needs saved Wi-Fi,
MQTT, channel, telemetry and local-only neighbor settings. A RAK image cannot
be installed on a Heltec. The sniffer target intentionally excludes Wi-Fi/MQTT
and is not a gateway image.

- [ ] Build the gateway target from the reviewed shared source and verify INA219
  driver inclusion, board-specific I2C pins/address and fitted-sensor detection.
  Retain corrected channel-1 power telemetry and failed-read handling; independently
  verify signed readings against the reference meter. Do not enable RAK-only
  diagnostic/dummy-load flags.
- [ ] Remove MQTT credential logging and replace insecure direct TLS with
  verified broker identity, documented trust/time provisioning and renewal.
  Test valid and invalid certificates/identity and cold-start behavior.
- [ ] Diagnose unattended Wi-Fi/MQTT reconnect using the existing GH-40 evidence;
  verify repeated AP/broker outages, queue drain, memory stability and recovery
  without manual restart. Patch demonstrated defects; do not assume resets solve
  the cause. Preserve fresh GPS delivery and source timestamps.
- [ ] Implement the gateway side of LOCAL-3's shared SNNS freshness contract;
  retain local-only reporting and source timing when forwarding RAK reports.
  Test delayed/duplicate reports with the portal. No timestamp design is yet
  selected. Gateway local cadence must not accidentally inherit RAK RF cadence.
- [ ] Define device/power/SNNS cadence and portal metadata from energy/traffic
  measurements. Verify G001 and G002 battery/INA219 data independently. Preserve
  LoRa TX disabled unless a separate transmit/admin-path decision is made.
- [ ] Publish target-specific verified artifacts, source pin, checksums and
  rollback procedure. Back up each board's full flash/profile/keys, identify
  before flashing, verify intended profile through reboot and test cold recovery.

## D. End-to-end release and deployment gates

- [ ] Record per-gateway fresh GPS, battery/power and own SNNS receipts through
  MQTT/archive/authenticated portal, plus deduplication of repeater copies.
- [ ] Complete an agreed battery/solar soak with Wi-Fi/broker interruptions and
  power cycling; record actual duration, packet gaps, reset counts, energy and
  temperatures. Separate bench reception from forced-relay/field acceptance.
- [ ] Coordinate GH-2/GH-3/GH-18 GPS freshness, relay/offline and field gates,
  site permissions and actual antenna/radio configuration review. Existing
  hardware comes first; candidate locations are not installation permission.
- [ ] Update sanitized hardware/setup photos, wiring, build/profile versions,
  enclosure files and measured limitations in the hardware documentation.

## Ownership and dependencies

Gateway-specific TLS/logging/reconnect and release acceptance move from LOCAL-3
section 4 to this ticket. GH-40's remaining reconnect acceptance is consumed
here; its [immutable import](../../../records/tracking-import/github-40.md) and
[outage evidence](../../../docs/operations/node-update-outage-20261020.md) remain.
No issue is marked technically resolved by consolidation and GitHub stays unchanged.

[LOCAL-3](25-production-firmware-readiness.md) owns the common SNNS timing
contract (including former GH-51/GH-52) and RAK readiness. GH-4 INA219 and GH-8
utilization remain independent evidence dependencies. GH-42 native battery-graph
presentation remains separate. LOCAL-5 owns public Markdown publishing and
per-node documentation presentation; this ticket owns truthful gateway content.

Next: inventory exact power components and agree the measurement run, then use
measured energy/physical dimensions to select supply and enclosure. Implementation,
printing and individual hardware operations follow when selected, not from this
ticket capture alone.
