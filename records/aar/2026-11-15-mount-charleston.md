# Mount Charleston deployment AAR - 2026-11-15

## Purpose and overall result

Place repeaters and test the mesh. Departed home **07:00**, returned **18:00
Pacific**: **11 hours** out. Two people attended. The day was long but felt
productive; the owner considered the amount of time appropriate. Snacks,
drinks and water worked well and should be repeated.

Source: the owner's same-day account. Measurements below are owner-reported;
no raw logs, meter captures or photos were inspected for this AAR. Published
[node identities and saved pins](../sites.md#2026-11-15---published-deployment-setup-and-fixed-locations)
and earlier configuration evidence remain separate from these field observations.

## Stops and outcomes

| Stop / node | Owner-reported outcome | Follow-up / evidence limit |
| --- | --- | --- |
| Cathedral Rock / R001 | Placed. Solar performance was not tested beforehand. After returning to the car, observed about **16 mA net to the battery**, versus **160-250 mA** on other boards. A photo taken about **09:00** reportedly shows the panels in direct, head-on sun. | Review the **November 16 morning** behavior and inspect panels, connections and charge performance. The owner's estimate of **about 32 mA panel input** is an inference, not a measured input. Photo has not been reviewed; cause remains unknown. |
| Kyle Junction / R008 | Placement went well; no issue reported. | Sustained operation and link performance remain to measure. |
| Angel Peak Vegas Side / R005, replacing R011 | Missed **OK to MQTT** permission required pulling an already deployed node; otherwise went well. Earlier [diagnosis](../../docs/operations/r011-telemetry-diagnosis.md) and [replacement evidence](../../docs/operations/r005-angel-vegas-deployment.md) preserve the identities and correction. | Prevent recurrence with a prepared, tested configuration process and complete verification before mounting. |
| Angel Peak Mountain Side / R011 | Placement otherwise went well. Forgot to take a photo. | Capture a site/installation photo on the next opportunity. |
| Upper Bristlecone / R010 | Placement went well; no issue reported. | Sustained operation and link performance remain to measure. |
| Lee Fire Station / G001 | Unstable during the day with large panels described as **5 W**, connected over USB-C. Seemed to operate normally after dark. Lee Fire Wi-Fi is currently available. | Suspected solar-related power problem; brownout and low panel voltage have not been demonstrated. Preserve logs and compare power conditions before choosing a remedy. |
| Lee Junction / R006 | Initially appeared able to reach Lee Fire and Upper Bristlecone. Reception was present at the car, then lost while hiking; the owner now doubts those links. No cellular coverage or reach to the vehicle Starlink at the hiking location. | Return and move the node to a better position, using local reception feedback. Intended links remain unproven; a car reception alone does not establish the repeater path. |
| Kyle Fire Station | Stopped to check Wi-Fi but did not have access. | Follow up on access; Lee Fire is the only currently available station Wi-Fi backhaul. |
| Shady Hollow / G002 | Set up as an **offline SD recorder**. Owner hopes it hears the Kyle side and both Angel Peak nodes. | Recover/copy the card and inspect actual receptions. Desired coverage is not yet demonstrated; earlier [offline sync evidence](../../docs/operations/g002-shady-hollow-deployment.md) does not establish field reception. |
| Fletcher | Not reached. Owner wants to replace the node and retain this site. | Plan a dedicated outing; owner expects Fletcher may take an entire day. No replacement completed. |
| Sisters | Not reached. Owner needs to recover existing hardware and probably will not place another node there. | Arrange recovery and identify recovered hardware. This supersedes Sisters redeployment as an assumed next step; retirement is not yet final. |

After Lee Junction it became dark and the outing ended so the team could return
home. The table organizes stops and assignments; it is not a timestamped route log.

## Preparation and workflow lessons

- **Laptop:** the field laptop still has a broken touchscreen. Repair or
  replacement is desired for easier field use. Carrying the rugged Dell on a
  hike is possible but undesirable; no repair or purchase is selected.
- **Assembly:** building board sleds separately from cases and completing final
  assembly in the field added friction. Prepare complete assemblies before
  departure where practical. The current case design blocks USB-C access to
  every device with the board installed, so servicing access needs attention.
- **Flashing/configuration:** agent-driven field preparation felt slow and
  inconsistent; the missed MQTT permission created avoidable retrieval work.
  Prepare and test a repeatable script ahead of time, including all required
  settings and verification, then let chat reconcile project records afterward.
  This is a requested process improvement, not a claim that every board was
  flashed today; earlier records show several retained their firmware.
- **Packing:** the roof antenna for the car node was forgotten. Add it to the
  departure kit alongside the successful food/water supplies.
- **Daylight/time:** keep the productive day length, but complete preparation
  earlier and leave room for daylight-dependent placement, photos and tests.

## Suspected causes and proposed options

**G001:** the owner suspects the Heltec V4 browns out because the larger USB-C
solar panels supply a lower voltage under operating conditions. Daytime
instability and apparent recovery after dark are observations; voltage sag,
reset cause and charger behavior remain unmeasured. A **TP4056 or similar
external charger** is an owner-proposed option to investigate, not an approved
wiring design or verified fix. The owner intends to address G001's charging
on the return trip; the remedy still needs evidence and compatible parts.

**R001:** unexpectedly low reported charging warrants inspection. No cause is
established by the sunlit photo or comparison with other boards. A larger
**5 W panel** is a possible later option if the larger-panel charging issues
can be resolved. No panel replacement has occurred.

**Local field feedback:** the owner proposes pairing an existing Meshtastic
node such as **B003** to the phone/app to check reception while hiking without
internet. Pairing, offline operation and usefulness for the intended links
still need verification. A driving dashboard, potentially using the car node
and ping/pong, should help identify places with overlapping repeater reach.
Existing [survey work](../../docs/research/repeater-operations-survey.md) and
the [node dashboard](../../docs/operations/live-node-dashboard.md) are relevant
starting points; neither is accepted here as meeting this field need.

## Tests not completed

- No planned field **ping/pong survey** was completed. Earlier isolated
  configuration-session pings remain valid evidence for their limited scope.
- No close-together **fiberglass versus Muzi antenna** comparison was completed.
- No feedline comparison was completed: fiberglass with an approximately
  **6-inch Type-N-to-IPEX** lead versus an approximately **10-15-foot
  Type-N-to-SMA cable plus 6-inch SMA-to-IPEX** lead. Confirm exact connectors,
  cable and lengths before testing. The owner wants to learn whether the longer
  cable's loss is small enough to allow higher tree placement or better line of
  sight while solar panels face a different direction. No loss or antenna
  winner is established.

## Return visit and follow-ups

Owner intends to return **later in the week or on the weekend**; date and route
are not set. These are recorded intentions, with task status in the
[tracker](../../.scratch/TRACKER.md), not new implementation assignments.

1. Before departure, review available overnight/morning behavior from R001 and
   G001; prepare complete assemblies, verified profiles, a local reception tool,
   the roof antenna and food/water.
2. Address G001's charging after checking the suspected power problem; inspect
   R001's panels/charging and replace parts if the findings support it.
3. Revisit/reposition Lee Junction and verify the intended Lee Fire/Upper
   Bristlecone links while walking, without relying on cell or Starlink reach.
4. Place additional owner-selected nodes and collect SD-card logs, including
   G002's offline recording; preserve source cards and raw data privately.
5. Capture the missing Angel Peak Mountain Side photo and follow up on Kyle
   Fire Wi-Fi access.
6. Arrange Sisters hardware recovery. Plan Fletcher replacement as a separate
   potentially full-day effort.
7. Schedule the unfinished ping/pong and antenna/feedline comparisons when
   there is sufficient time; they have no results from this outing.

Friends in the northwest valley may be able to host a node with an apparent
straight shot to Angel Peak. This is a candidate opportunity; host permission,
actual radio path and any backhaul availability remain to confirm. No private
address or host identity is published.

Longer-term requests are captured in the [wishlist](../wishlist.md#field-preparation-and-service-access)
without starting research, implementation, purchases or hardware changes.
