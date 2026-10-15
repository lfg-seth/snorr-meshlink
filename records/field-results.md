# Field testing and tangible results

Updated: 2026-10-14. Software broker, firmware provisioning, local radio and actual two-gateway MQTT fixture tests are recorded below. A short GPS delivery/freshness observation is now recorded; sustained delivery, battery-runtime and field results remain unmeasured. Agree numerical acceptance criteria before using those tests to claim success.

## Test index

### TEST-006 — Stock RAK pilot repeater preparation

- 2026-10-14: owner authorizes stock firmware/reset/configuration on two connected RAKs and confirms suitable 915 MHz antennas attached. Identify R001 `!a65601b3` on COM8 and R002 `!b456f760` on COM9, both firmware-reported RAK4631. Private before-state exports preserve previous profiles; stock `2.7.26.54e0d8d` target/package hashes and the post-reset serial recovery are recorded in [setup](../docs/operations/rak-pilot-setup.md). Recovery succeeds through the matching official Nordic serial firmware package; the timeout's precise cause remains unresolved.
- Configure visible `ROUTER` roles, `LOCAL_ONLY` rebroadcast, the existing private pilot channel/key, US/LONG_FAST, slot 35, hop limit 3 and 10 dBm transmit. MQTT/Wi-Fi off; no channel downlinks/uplinks on the RAKs. Clear old fixed positions/admin keys, create fresh device keypairs, disable GPS pending hardware/location identification, and set device telemetry to 900 seconds. Role-change defaults require a second profile application; independent readback on each board verifies the explicit values.
- Predetermine reception criterion: one distinct harmless encrypted zero-hop text fixture from each RAK must reach the other RAK and both V3s, identified by matching packet IDs. All six of six checks pass. Both existing gateways are independently identified and still report transmit disabled; no gateway configuration written. Raw fixture events/readbacks remain ignored under `private/bench/`.
- Explicit reboot requests disconnect both USB APIs; independent reconnection/readback then passes the complete profile on each board. The Python client's close routine reports an already-disconnected-stream error after each reboot request; subsequent device readbacks succeed. This is not a battery power-cycle or endurance test.
- Follow-up: owner completes an earlier double-reset request after setup, exposing two RAK4631 UF2 drives. Reinstall the same checksum-verified stock UF2 without configuration erase. Both normal serial APIs return and complete pilot-profile readbacks pass again; direct reception was not rerun for this unchanged-image recovery.
- Battery-reporting correction: owner asks about battery voltage. Pinned stock `DeviceTelemetry.cpp` requires `device_telemetry_enabled`; the initial profile only set its 900-second interval, leaving broadcasts disabled. Enable the flag on both RAKs, retain the interval and independently verify the complete profiles after configuration reboot. Update private provisioning/verification helpers to require the flag. Stock metrics contain voltage and level (101 means charging/no battery); no actual battery calibration, timed automatic RF-report observation or portal battery ingestion is claimed.
- Limits: this is direct close-bench transmit/receive evidence, not a forced relay-path test, coverage result, measured RF-silence result or sustained delivery rate. V4s are not connected during this run; no new GPS/portal/outage/runtime test. Battery/solar assemblies, exact antenna models, fitted sensors and site permission remain unverified. Existing portal provisioning remains unchanged; RAK telemetry is not integrated into the portal.

## Software MQTT public-endpoint access test — 2026-10-14

Owner-supplied PASS output from [public MQTT check](../scripts/server/check-mqtt-public.py), using MQTT 5 software clients with existing pilot accounts and certificate/hostname validation for `mqtt.snorr.org:8883`. A temporary loopback-only reverse SSH relay routed encrypted TLS through the external test host to the public endpoint, avoiding the broker-origin direct-route timeout. Both V3 accounts published non-retained synthetic audit messages received by the worker. Anonymous/invalid logins, worker writes, gateway reads, and JSON/unrelated-topic writes were denied. No configuration change or retained message was created by this test. Relay closed afterward; independent SSH confirms no port-18884 listener and active Mosquitto. This verifies broker transport/authentication/topic permissions, not physical gateway, GPS, radio, runtime, reconnect or live portal ingestion behavior.

## Heltec bench readiness review — 2026-10-14

[Staged checklist](../docs/operations/heltec-bench-checklist.md) and [current primary-source check](../docs/research/heltec-bench-source-check.md) prepared. Stock firmware supports starting a small local V4 GPS / V3 receiver evaluation after revision, image, wiring, power, antenna and radio configuration checks. Public broker transport has recorded TLS/rejection evidence; subsequent owner-run valid-account synthetic delivery and ACL checks through public TLS pass. Live portal ingestion and custom survey implementation remain unfinished. No radio connected to the agent environment was identified, and no firmware flash, GPS/radio/MQTT hardware run or battery measurement occurred. This is a readiness review, not a measured test result.

## Planned direct-link repeater survey — 2026-10-13

Owner requests a firmware ping/pong responder on solar RAKs, with a GPS-equipped Heltec V4 testing node and Dell log storage; compare repeater and testing-node antennas separately. [Draft procedure and metrics](../docs/research/repeater-operations-survey.md), under [Define repeater operations and direct-link placement testing](../.scratch/pilot/issues/14-repeater-operations-survey.md).

Record repeater-measured ping RSSI/SNR and V4-measured pong RSSI/SNR, direct-path evidence, every attempt/timeout, GPS fix time/age, antenna mounting/feedline, firmware/radio settings and transport discontinuities. Proposed repeated checkpoint sampling is exploratory, not an agreed acceptance criterion. Round-trip success cannot separately establish directional delivery rates. Later GPS relay/outage tests remain separate. Owner mentions previous testing but has not supplied evidence; no measured results, preferred site, antenna winner or completed test is recorded here. Raw GPS logs remain ignored/private.

## Agreed pilot criteria — 2026-10-12

Source: owner responses in [Define useful tracking for the first field pilot](../.scratch/pilot/issues/02-pilot-needs.md). These are planned criteria; no measured results exist.

- Dispatch visibly distinguishes stale locations and displays position age; stale threshold is 15 minutes since GPS measurement. Backfilled positions retain their original measurement age.
- Member nodes track for at least 4 hours on battery; 12 hours is the target. Record runtime under the tested GPS/reporting configuration.
- Power-on starts passive GPS broadcasting without phone use or repeated member interaction. SOS is deferred beyond this MVP.
- Evaluate aggressive reporting and dial back using measured congestion; plugged-in/battery modes and movement thresholds remain candidate options. Numerical settings and congestion criteria are not yet agreed.
- Planned trial count: 6 Heltec V4s only, with GPS and 3000mAh batteries; 2 are on hand, 2 purchases and 2 recoveries are pending. T-Decks are excluded. Routes, trial duration, acceptable stale/missing-position frequency, and backhaul outage acceptance criteria remain open. A 15-minute display threshold alone does not define a network delivery pass rate.
- Infrastructure: RAK repeaters (count/builds to select) and 2 Heltec V3 internet backhauls. Portal-planning amendment permits one designated V3 to transmit shared-channel replies; the other stays receive-only. Verify V4-to-RAK-to-V3-to-dispatch delivery, designated-gateway command behavior, and the receive-only V3's radio silence while internet forwarding is active. Record both backhauls' receipt times separately from GPS measurement times; duplicate handling and outage/recovery checks need a defined procedure. No relay/backhaul measurements exist yet.
- Disconnect internet backhaul and verify local field command-post viewing plus other-member locations on connected companion apps. Distinguish radio delivery, app connection, available offline map data, and position age; do not treat an internet outage as a radio outage. Phone-free tracking must continue. No offline viewing or map tests performed.
- Start relay evaluation with 2 undamaged on-hand RAKs after core identification/operation checks. The Meshtastic app is acceptable for first local-viewing MVP; both app and laptop/portal viewing are intended. The owned rugged Linux Dell is a field-computing candidate, not a verified offline viewer. Record actual viewer platform, version, connection, map preparation, and measurement-age behavior during testing.
- Multi-backhaul evaluation: establish the 2-V3 private-MQTT baseline first, then add 1 companion-app/cellular uplink and increase only if measured behavior is acceptable. Permit portal-message downlink only on the designated V3; keep other tracking gateways from accepting internet-to-LoRa commands. Measure duplicate deliveries, unique position completeness/age, gateway identities, broker/client load, reconnect bursts, phone battery/background behavior, and radio airtime. Confirm delayed duplicates do not reset freshness or replace newer fixes. No acceptable gateway count, saturation limit, or app-proxy reliability established.

## Planned infrastructure-portal verification — 2026-10-12

Source: [Define the dispatch portal MVP](../.scratch/pilot/issues/06-dispatch-portal.md). No results recorded.

- Identify fitted sensors and actual readings on selected RAK/V3 builds; verify battery level/voltage, charging/discharging and solar measurements where available, with correct units and labelled measurement points. Distinguish direct readings from calculated trends.
- Check environmental/detection reports only where equipped. Verify recording, duplicate handling, per-reading timestamps/freshness, historical charts and event logs. Unavailable/stale intrusion data must not show an all-clear.
- Exercise configurable low-battery/missing-telemetry/intrusion warnings after thresholds and acknowledgment/clearing rules are agreed. Keep infrastructure telemetry cadence separate from member-GPS freshness; measure any added radio traffic against passive-tracking priorities.
- Apply the [agreed infrastructure warning policy](../.scratch/pilot/issues/10-infrastructure-warning-rules.md): verify silent persistent badges, audited permissions, capability-specific timeouts, fresh-data recovery, latched/grouped intrusion incidents, replay/duplicate handling and feed-outage/reconnect grace. Check battery configuration distinguishes type, count, capacity scope and pack arrangement from measured health. These checks are planned; none passed yet.

## Test records

| Test ID | Date | Bench / field | Objective / route | Configuration / firmware commit | Evidence reference | Outcome |
| --- | --- | --- | --- | --- | --- | --- |
| TEST-001 | 2026-10-14 | Bench | Stock Heltec firmware/configuration preparation | `v2.7.26.54e0d8d`, commit `54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb` | Ignored `private/bench/`; sanitized details below | Follow-up completes four stock installs and full profile/role reboot checks |
| TEST-002 | 2026-10-14 | Bench | Each V4 fixture received by both V3s | Same release; private channel, US LONG_FAST, slot 35, configured 10dBm, hop limit 3 | Ignored `private/bench/radio-smoke-20261014T180221Z.json` | All four reception checks pass; no GPS or MQTT claim |
| TEST-003 | 2026-10-14 | Bench / software | Hotspot association, broker subscriber, MQTT fixture delivery | Same stock firmware and private channel | Ignored `private/bench/connection-status.json`, `mqtt-saved/`, `mqtt-radio-smoke-20261014T183218Z.json` | Initial 0/4 before password correction; subsequent actual encrypted gateway MQTT delivery 4/4 PASS |
| TEST-004 | 2026-10-14 | Bench | Automatic GPS positions from both V4s through both V3s | Same stock build/channel; replacement hotspot | Ignored `private/bench/gps-mqtt-20261015T002434Z.json`, `gps-herrera/`, `herrera-saved/` | 4/4 GPS member/gateway paths PASS; fix ages about 21–35 seconds |

### TEST-001 — Stock Heltec provisioning

- Owner authorizes formatting/flashing 2 V4 and 2 V3 units. USB initially shows four units; V4 with USB serial ending `A878` disappears before serial inspection and is not flashed.
- Remaining chips identified: original V4 `!699c2ed8`, 16MB flash / 2MB embedded PSRAM; V3 `!9ea13cc0` and V3 `!849ad7a0`, each 8MB flash. Exact frequency variants, attached antennas and current US test location still await confirmation before RF enablement.
- Full original flash/configuration backups remain private. All three receive clean stock installs from the official ESP32-S3 release archive; SHA256 matches GitHub (`339650ced8b8c859751f04be69c6af845fea96baca1327518f199afd2595a9d4`). Target image sizes/hashes match manifests. Factory, recovery/OTA and filesystem images are written at target-manifest offsets and independently verified against flash.
- Both V3s boot stock `2.7.26.54e0d8d`. Private bench profile uses a shared random-key `SNORRbench` primary channel, full position precision, uplink on/downlink off, `config_ok_to_mqtt` on, MQTT-originated radio traffic ignored, slot 35 and proposed 10dBm power. Region UNSET, transmit disabled, GPS not present, Wi-Fi/MQTT disabled. Endpoint `mqtt.snorr.org:8883`, TLS, root `snorr/pilot` and encrypted protobuf mode are staged without credentials; no hardware MQTT delivery claimed.
- Bulk serial writes initially fail to persist parts of the profiles. A single transmit-disable write succeeds; longer post-commit hold improves persistence, but complete validation still detects a missed MQTT config. Private logs show UART0 buffer-full errors. Spacing config/channel writes by 0.4 seconds and holding serial open 3 seconds after commit produces no buffer-full errors and processes MQTT config. Saved-profile checks and independent reboot/readbacks distinguish actual state from successful host sends.
- V4 flash verification passes, but bounded API probes time out after RTS reset while the flasher remains reachable. Watchdog reset re-enumerates it as ACM0 and removes the temporary owner-granted ACL. V4 post-boot API/GPS/profile verification awaits restored access. [Runtime access helper](../scripts/bench/grant-heltec-serial-access.sh) prepared/syntax checked; no agent-root execution.
- Final independent reboot checks both bench short names (G001/G002) and every specified saved-profile field; both pass, including staged MQTT endpoint/root/TLS and matching private channel keys. Result: three image installs verified and both V3 profiles pass; overall four-board provisioning incomplete. No fresh GPS fixes, RF delivery/silence measurements, hardware MQTT/reconnect, battery runtime or offline viewing tests collected. Raw backups/configurations/logs and channel key remain ignored/private.

2026-10-14 follow-up — Owner runs runtime access helper, reconnects the second V4, reports selecting US on the three flashed devices and confirms attached antennas. Runtime ACLs survive native USB reset. Newly reconnected V4 `!699ca878` is confirmed original V4, 16MB flash/2MB PSRAM, running old `2.7.15.567b8ea`; 1200-baud touch enters its bootloader. Private full-flash/configuration backup, clean stock install and independent factory/recovery/filesystem verification pass. All four devices now boot the same release. First US initialization regenerates PKI keys and enables transmit; receive-only V3 settings are restored and each final role is explicitly checked. Initial second-V4 profile readback catches missing settings; reapplying after initialization succeeds. No internal cause beyond incomplete first application is established.

Final independent reboot/readback verifies every specified profile field and these bench labels/roles:

| Bench label | Hardware node ID | Board | Region / preset / slot / configured power | LoRa transmit | GPS |
| --- | --- | --- | --- | --- | --- |
| B001 | `!699c2ed8` | Original V4, 16MB / 2MB PSRAM | US / LONG_FAST / 35 / 10dBm | Enabled | Enabled, RX39/TX38/enable34 |
| B002 | `!699ca878` | Original V4, 16MB / 2MB PSRAM | US / LONG_FAST / 35 / 10dBm | Enabled | Enabled, RX39/TX38/enable34 |
| G001 | `!9ea13cc0` | V3, 8MB | US / LONG_FAST / 35 / 10dBm | Disabled | Not present |
| G002 | `!849ad7a0` | V3, 8MB | US / LONG_FAST / 35 / 10dBm | Disabled | Not present |

All use only one enabled primary channel (`SNORRbench`) with a shared private random key and full position precision. V4 profiles use 60-second GPS acquisition, 120-second periodic reports, smart broadcasting off, fixed position off and GPS-solution timestamp flag on; phone-free fresh-fix behavior remains to measure. V3 channel uplink is on; all downlinks are off and MQTT-originated radio traffic ignored. Both V3s remain transmit-disabled through reboot. Wi-Fi/MQTT stay disabled on all four; current broker endpoint, TLS, root and encrypted protobuf settings are staged. Bench labels identify devices, not member assignments. Result: stock firmware/local-radio preparation complete; GPS acquisition/freshness and gateway networking remain unverified. Broker accounts/Wi-Fi access require private provisioning; owner asked for private file paths, not secrets in chat.

### TEST-002 — Local encrypted radio fixture reception

- Started 2026-10-14 18:02:21 UTC (11:02:21 Pacific). Two V4s and two V3s; firmware and settings as above. No RAK relays or internet gateway connections active.
- Criterion set before the run: a distinct harmless encrypted bench text fixture from each V4 must arrive at each V3. Both V4 fixtures reach both receive-only V3s: four of four checks pass. Private event records retain origin/packet ID, receiver, host receipt time and available radio metrics. V4s use normal configured hop limit 3; this does not prove direct-only paths or resume the deferred survey module.
- Available SNRs: 7.0 / 6.5dB for B001 at G002/G001; 6.25 / 6.0dB for B002 at G001/G002. RSSI is recorded as -9dBm for B001 at G001 and -16dBm for B002 at G002; absent on the other two events, not invented. These close-bench measurements do not establish range, field coverage or sustained delivery rates.
- No position events collected during this short fixture test, and no GPS fix is claimed. V3 transmit-disabled configuration is verified, not measured RF silence. MQTT software checks remain separately confirmed; no real gateway MQTT, portal ingestion, reconnect, runtime or offline-map result.

### TEST-003 — First real MQTT gateway provisioning attempt

- Owner supplies credentials and resets hotspot in compatibility mode. Laptop NetworkManager confirms actual SSID rather than its interface-labelled connection name. Both V3s associate and obtain IPs; saved credential equality is checked privately. LoRa transmit remains disabled. Credentials/captures stay ignored/private; no passwords published.
- Existing read-only worker subscriber authenticates through public certificate/hostname-validated TLS and subscribes to `snorr/pilot/2/e/#`. Two harmless encrypted V4 fixtures yield zero of four expected member/gateway MQTT receipts; V3 readback shows MQTT still disabled and account settings unapplied.
- Prerequisite failure: generated gateway passwords are 48 UTF-8 bytes; pinned NanoPB MQTT password storage is 32 bytes including termination (31 usable). That config cannot fit stock V3s despite valid software-client authentication. This is not a broker transport/ACL defect. [Source/prepared fix](../docs/operations/mqtt-nginx-handoff.md#heltec-connection-settings).
- Two gateway password replacements are prepared, not applied. Isolated real-broker tests verify 30-byte replacements authenticate, old values fail, worker password/hash and ACL are preserved, rerun is idempotent, and injected verification failure restores original files/authentication. Owner sudo execution of the guarded fix remains required before private export retrieval and device provisioning.
- Result: hotspot/subscriber pass; actual gateway MQTT remains blocked/unverified. No GPS freshness, portal ingestion, runtime or reconnect claim.


2026-10-14 successful follow-up — Owner runs the guarded compatibility fix. Retrieved owner-private export has two 30-byte gateway passwords and the unchanged 48-byte worker credential. Both V3s persist endpoint/account/root/TLS/encrypted-protobuf settings; password and Wi-Fi equality checks pass privately. Both connect to Wi-Fi and MQTT. At 18:54:46 UTC (11:54:46 Pacific), each V4 sends a distinct harmless bench text fixture. The certificate/hostname-validating read-only subscriber receives and decrypts both fixtures from both gateway identities: all four member/gateway checks pass, all four payloads encrypted, no parser errors. Evidence: ignored `private/bench/mqtt-compatible/` and `mqtt-radio-smoke-20261014T185446Z.json`. No position events collected; no GPS freshness or portal ingestion claim. Settings retain uplink-only channels and disabled V3 LoRa transmit; configured silence is not a measured RF-silence test.

Independent gateway reboot follow-up — Both saved profiles, including exact private credentials, pass readback after reboot. Initial status checks precede MQTT connection; subsequent checks show both Wi-Fi/MQTT connections restored. Fresh encrypted V4 fixtures again reach both restarted gateways and the worker subscriber (4/4 PASS). Evidence: ignored `private/bench/mqtt-reboot/`, `connection-status.json` and `mqtt-radio-smoke-20261014T185601Z.json`. This tests gateway reboot recovery, not hotspot/proxy/broker outages or sustained reliability.

### TEST-004 — Automatic GPS positions through both MQTT gateways

- Owner reports satellites after reconnecting the nodes, then supplies replacement hotspot credentials. Restore owner-granted serial access; apply new Wi-Fi to both V3s. Private readback verifies exact Wi-Fi equality and unchanged MQTT configurations/credentials, with LoRa transmit still disabled. Both gateways reconnect to Wi-Fi/MQTT after initial transitional disconnected states.
- Observation starts 2026-10-15 00:24:34 UTC (2026-10-14 17:24:34 Pacific), with a certificate/hostname-validating read-only MQTT subscriber. No synthetic position, manual send-position command, phone app or firmware change is used. Watch automatic reports for at most 260 seconds, stopping after all four member/gateway paths contain recent GPS measurement timestamps. This is an exploratory bench check, not an agreed field delivery-rate threshold.
- B001 `!699c2ed8`: one unique encrypted GPS report received through both G001/G002; 9 satellites, original GPS measurement age 21.13 seconds at each subscriber receipt.
- B002 `!699ca878`: one unique encrypted GPS report received through both G001/G002; 8 satellites, original GPS measurement age 35.40/35.41 seconds at subscriber receipt. Four source/gateway paths pass, no decoding errors. Duplicate gateway receipts are not four independent fixes or a sustained reliability rate.
- Private evidence: `private/bench/gps-mqtt-20261015T002434Z.json`; direct V4 snapshots in `gps-herrera/` show internal-GPS positions, and `herrera-saved/` verifies gateway settings. An earlier capture `gps-mqtt-20261015T002003Z.json` spans the hotspot transition and contains only B001 through both gateways (11 satellites, ages 50.81/58.76 seconds); superseded by the complete observation, not hidden as a successful four-path run. Raw coordinates stay ignored/private.
- Result: both real GPS sources automatically reach MQTT through both gateways on the replacement hotspot. The temporary subscriber saves test evidence and then exits; no continuous recorder or real portal ingestion worker is installed. Startup without a phone, sustained freshness/completeness, outage handling, runtime and field coverage remain to test. Heltec direct-TLS identity caveat remains unchanged.

### TEST-005 — Live portal GPS ingestion

- Date: 2026-10-14, America/Los_Angeles. Native Windows development and the existing Ubuntu LXC; two original V4s B001/B002 and two receive-only V3 gateways G001/G002 on stock `2.7.26.54e0d8d`. No RAK, additional hardware, firmware patch or outbound radio command.
- Owner replaces gateway Wi-Fi; both V3 saved network settings match privately and MQTT/LoRa configurations remain byte-for-byte unchanged, including transmit disabled. Owner restores B001 reporting after a quiet period. Initial 150-second no-traffic/partial windows and a failed all-tracker window are retained as failures, not counted as all-path passes. No live cutover occurs while those checks fail.
- Timestamp correction: the early adapter used `Position.time`, which source review establishes is a device/transmit clock. Those early small ages are **not** GPS freshness evidence. The final adapter uses `Position.timestamp` plus bounded millisecond adjustment and never substitutes device/receipt clocks. A regression test proves a recent transmit clock cannot refresh an old GPS solution.
- Final strict five-minute preflight: two reports from each tracker observed through each gateway, eight receipts across all four source/gateway paths, zero decoder rejections. Actual GPS-solution ages at receipt: 22.62/22.63, 6.31/6.31, 36.40/36.40 and 74.82/74.82 seconds. Source transmit-attempt denominator is unmeasured, so this is not a packet-delivery percentage or sustained freshness guarantee.
- Before cutover, private backup `meshlink-20261015T023712Z.tar.gz` passes checksum/integrity and isolated API recovery. The expected fictional dataset is transactionally archived/replaced by four verified devices; demo member accounts are disabled, real members/assignments remain empty and admin credentials are preserved. Simulation is explicitly disabled. The hosted service runs `mqtt_worker.py`, under `meshlink-worker`, with TLS hostname/certificate verification and a private durable receipt queue.
- Live portal API/storage verification: initially two positions and four receipts (two accepted/two duplicate), with one receipt for each source/gateway pair and one displayed observation per original packet. Latest stored GPS measurement ages at that check: B001 58.26 seconds, B002 155.26 seconds. After worker restart, three positions/six receipts remain available (three accepted/three duplicate); both trackers retain two-gateway deduplication and the authenticated feed returns online. No raw coordinates/keys appear in tracked evidence.
- New live backup `meshlink-20261015T024051Z.tar.gz` passes checksum, SQLite integrity and isolated API recovery: four accounts, four devices, zero members/assignments/messages/infrastructure observations/incidents/events, three positions and six packet receipts. Expanded backups include private worker configuration, queue and service definitions. Local API/proxy authentication boundaries, per-client throttling and credential-free public HTTPS/certificate/protected-route checks pass. The public browser entry renders the new sign-in-only page; authenticated live map/history browser review is still outstanding.
- Software checks: 36 backend tests pass on the LXC's Python 3.12 runtime with the isolated pinned MQTT dependencies, including encrypted-wire decoding, API retries, durable queue restart, subscription/outage state, transactional cutover rollback and stale timestamp behavior. Eight frontend tests, TypeScript and production build pass on pinned Node 22.23.1; existing MapLibre bundle-size warning remains. Shell/service/Python syntax and Git whitespace checks pass.
- Limits: no sustained field reliability, runtime, RF coverage, broker/Wi-Fi outage hardware test, phone-free cold start, full browser/device matrix or off-host backup demonstrated. Radio messaging, remote naming, member battery and infrastructure telemetry remain unintegrated. This completes receive-only bench GPS integration, not operational deployment readiness.

## Copy for each test

### TEST-NNN — title

- Date and time zone:
- Question being tested:
- Acceptance criteria agreed before the run:
- Location/route and relevant weather:
- Member-node count and hardware IDs:
- Repeater and backhaul IDs:
- Firmware versions/commits and configuration reference:
- Test duration; who collected measurements:
- Positions expected / measured at source / received by dispatch:
- Position age at dispatch (distribution and worst observed; use measurement timestamps):
- Missing/duplicate positions and time windows without updates:
- Phone-free operation result:
- Communication attempts and acknowledgments, if tested:
- Internet outage and recovery observations, if tested:
- Battery start/end and power measurements:
- Raw evidence reference and sanitized summary:
- Result: pass / fail / inconclusive, with limits:
- Follow-up decision or corrective action:

## Reporting measures

Track member-device participation, coverage along tested routes, position age, delivery completeness, message delivery, mission runtime, repeater uptime during observed periods, and supported expenses. State the sample size and test conditions with each claim. An untested route or unobserved period has no measured result.
