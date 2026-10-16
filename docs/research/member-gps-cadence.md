# Stock member GPS cadence options

2026-10-15. Read-only investigation; no device settings changed. Scope: B001/B002's stock Meshtastic `2.7.26.54e0d8d`, upstream commit `54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb`. This is configuration research, not a measured field or battery result.

## Recorded baseline

B001/B002 have **60-second GPS acquisition attempts, 120-second periodic position broadcasts, smart broadcasting disabled**, fixed position disabled and GPS-solution timestamps enabled. Both are `CLIENT` role in the private independent reboot summaries (`private/bench/reboot-verified-summary.json`; role fields inspected without copying credentials or coordinates). They use one private primary channel with full position precision. The tracked [bench evidence](../../records/field-results.md#test-001--stock-heltec-provisioning) establishes saved settings; subsequent tests establish GPS delivery through both gateways, not sustained cadence or runtime.

## Stock controls and behavior

Stock firmware exposes separate controls for GPS acquisition attempts (`gps_update_interval`), periodic broadcasts (`position_broadcast_secs`), smart enable, minimum displacement in meters and minimum elapsed time in seconds. A quicker radio interval alone cannot create a newer GPS fix. [Official position configuration](https://meshtastic.org/docs/configuration/radio/position/).

**Faster settings are available without a fork.** Explicit 60-second or 30-second periodic intervals are not clamped by the pinned source's default-channel protection on this private profile. The protection applies when the position-bearing channel is detected as a default channel; for non-router roles it clamps nonzero periodic intervals to 3,600 seconds and smart intervals to 300 seconds. This describes firmware configuration behavior, not a capacity or regulatory approval. [Pinned NodeDB enforcement](https://github.com/meshtastic/firmware/blob/54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb/src/mesh/NodeDB.cpp#L348-L365), [pinned defaults](https://github.com/meshtastic/firmware/blob/54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb/src/mesh/Default.h#L16-L22).

**Smart broadcasting supplements the periodic baseline.** The scheduled send path considers an earlier movement report when both minimum displacement **and** minimum time since the last send are satisfied. Distance is straight-line displacement from the last transmitted coordinates, not accumulated walking distance; returning toward that point can delay a report despite substantial travel. The periodic timer remains active and movement sends reset the shared last-send timer. [Pinned PositionModule](https://github.com/meshtastic/firmware/blob/54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb/src/modules/PositionModule.cpp#L407-L466), [distance calculation](https://github.com/meshtastic/firmware/blob/54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb/src/modules/PositionModule.cpp#L513-L532).

**Pinned-release caveat:** GPS publication also calls `handleNewPosition()` whenever GPS mode is enabled. That handler tests displacement and elapsed time but does **not** test the smart-enabled flag or repeat the scheduled path's channel-utilization check. This applies to GPS-enabled roles generally, including these `CLIENT` nodes. Thus smart disabled is a saved setting, not proof that all movement-triggered transmissions are disabled; actual stationary/moving behavior must be observed. This is a source finding, not an observed device fault. [GPS caller](https://github.com/meshtastic/firmware/blob/54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb/src/gps/GPS.cpp#L1072-L1087), [movement handler](https://github.com/meshtastic/firmware/blob/54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb/src/modules/PositionModule.cpp#L535-L561).

GPS intervals of **10 seconds or less keep the receiver from entering the normal sleep path**; shorter intervals and more transmissions may cost battery. Exact V4 power cost is unmeasured. [Pinned GPS power handling](https://github.com/meshtastic/firmware/blob/54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb/src/gps/GPS.cpp#L1024-L1069).

## Provisional comparison to test

| Profile | Periodic setting | GPS attempt setting | Smart settings | Purpose |
| --- | --- | --- | --- | --- |
| Faster periodic | 60 s | 30 s | Disabled; verify caveat above | Simple first comparison against the current baseline |
| Hybrid | 120 s | 30 s | Enabled; minimum 30 s and 50 m | More detail during movement while retaining stationary reports |
| More aggressive periodic | 30 s | 15 s | Disabled; verify caveat above | Later comparison if measured airtime/delivery/runtime support it |

These are suggestions, not applied or validated profiles. Movement mode may improve moving-track detail and use fewer packets than a continuously aggressive interval, but does not inherently improve radio reception, stationary freshness or GPS accuracy. A threshold too small can react to GPS wander. At nominal timing, 20 trackers generate about 10/20/40 original periodic reports per minute at 120/60/30 seconds, before relays and other traffic; this arithmetic is not measured capacity.

Set explicit values and verify readback after reboot. Current official docs identify themselves as version 2.8 and give inconsistent smart-default values; the pinned build uses a **300-second smart fallback**. Do not rely on zero/default for the proposed 30-second smart interval. [Pinned threshold initialization](https://github.com/meshtastic/firmware/blob/54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb/src/modules/PositionModule.h#L68-L77).

Next useful check: compare stationary and walking receipt gaps, GPS measurement ages, airtime and runtime on the owned nodes. Firmware scheduling, GPS acquisition, RF loss and backhaul outages can all lengthen dispatch freshness; neither settings profile guarantees an arrival interval.
