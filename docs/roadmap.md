# Roadmap

Evidence checkpoints updated 2026-10-17 from recorded evidence, not a new live-service or hardware inspection. These are acceptance checkpoints, not promised dates. On `trial/local-tracking`, the [local tracker](../.scratch/TRACKER.md) owns current work status under the [local workflow](operations/local-tracking.md); `main` retains the prior workflow.

| Checkpoint | Recorded state | Evidence still needed |
| --- | --- | --- |
| Project record and tracking | Repository records and local decisions established; compact local tracking under trial on a separate branch, with imported issue history | Record meaningful status changes and the next action in the local tracker; keep evidence in its existing records; leave GitHub issues and the Project board untouched during the trial |
| Inventory and pilot requirements | First inventory and pilot needs decisions complete; two member trackers used in bench integration | Confirm condition/availability of additions before treating the planned six-member set as ready; reuse stock first |
| Network and firmware evaluation | Meshtastic pilot baseline; real GPS/MQTT path and selected RAK fork work recorded | Broader readiness depends on measured relay, outage, freshness and power evidence; protocols remain distinct |
| Reliable bench tracking | Two-tracker/two-gateway GPS ingestion, worker restart and isolated recovery recorded; neighbor/power portal integration deployed | Sustained phone-free freshness/runtime; forced relaying; local viewing/outage recovery; fresh G002 neighbor/power path; accurate power diagnosis; off-host recovery |
| Measured field pilot | No accepted six-member field-readiness claim | Agree available devices, route, access and stale/missing delivery criteria; measure field coverage, GPS age, runtime and recovery after bench prerequisites |
| Repeatable member rollout | Not ready for wider distribution | Accepted pilot evidence, repeatable provisioning/assignment, handout/training, maintenance and support |
| Repeater installation | Prepared radios and candidate/planned sites are recorded | Site permission, measured coverage, environmental design, battery/solar endurance and maintenance acceptance |
| Communications | Requirements recorded; real portal downlink and remote administration unfinished | Owner-activated scope after tracking priorities, one designated reply gateway, delivery and permissions testing |
| Reporting and funding | Capture records throughout | Dated expenses and measured outcomes supporting each public/grant claim; no promised funding |
| Law enforcement expansion | Later | Separate stakeholder requirements, authorization and interoperability scope |

## Current evidence and next useful step

[Bench GPS](../records/field-results.md#test-005--live-portal-gps-ingestion), [RAK relay preparation](operations/rak-pilot-setup.md), [deployed neighbor/power integration](operations/radio-report-ingestion.md), [INA219 uncertainty](operations/ina219-audit.md), and [session history](../records/sessions.md) describe what was actually checked. Local demo improvements remain separate from hosted deployment; a resolved design question or successful code test is not field acceptance.

Use the [local tracker](../.scratch/TRACKER.md) for the next authorized action. Bench priorities remain the phone-free freshness/runtime trial and relay/outage verification, after agreeing their run plans and hardware availability. The [INA219 investigation](operations/ina219-audit.md) remains important before drawing power-design conclusions. Preserve the 15-minute stale threshold, four-hour runtime minimum and 12-hour target; agree other thresholds before testing. Original task details are preserved in the [tracking import](../records/tracking-import/index.md).

The original [GitHub milestones](https://github.com/lfg-seth/snorr-meshlink/milestones) grouped work under Reliable bench tracking, Measured field pilot and Repeatable member rollout. Their counts reflect issue closure before the trial, not current progress or an operational-readiness percentage. Deferred wishlist features, held survey work and later expansion remain parked until explicitly activated.
