# Field testing and tangible results

Updated: 2026-10-12. No bench or field results have been recorded. Agree numerical acceptance criteria before using a test to claim success.

## Test index

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
