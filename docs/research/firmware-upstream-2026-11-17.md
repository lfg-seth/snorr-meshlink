# SNORR firmware against Meshtastic releases, 2026-11-17

Meshtastic's latest non-prerelease is **2.7.26.54e0d8d Beta**, the exact upstream release on which SNORR builds. The newest published prerelease is **2.8.2.d5f1619 Alpha**. Upstream published it November 4 UTC after revoking the November 2 build for an environmental telemetry crash. [Beta](https://github.com/meshtastic/firmware/releases/tag/v2.7.26.54e0d8d), [replacement alpha](https://github.com/meshtastic/firmware/releases/tag/v2.8.2.d5f1619).

## Distance and merge results

Git 2.52 compared both published source commits with the two release tags in a disposable checkout with the upstream protobuf history available. Counts below are commits or unique conflicted paths. [MeshLink main at the time of comparison](https://github.com/lfg-seth/snorr-meshlink/tree/af7e19358a42c0d7a89428f49bac3dec87cfedaa), [published fork tip](https://github.com/lfg-seth/firmware/commit/2dbf0a65af9058d91df5a49827b846588a9a0063).

| SNORR source | Commits ahead / behind beta | Commits only on alpha | Direct merge conflicts | Conflicts applying only SNORR changes to alpha |
| --- | ---: | ---: | ---: | ---: |
| MeshLink firmware pin `5bd4923` | 23 / 0 | 1,174 | 85 | 10 |
| Published `snorr/develop` tip `2dbf0a6` | 31 / 0 | 1,174 | 86 | 12 |

The tip is eight commits beyond the pin and can be reached by fast-forward. Those eight include survey enrollment and radio controls, the G002 SD gateway responder and the button-operated V3 site survey. Individual radios have their own installation records. For example, G001 runs `5bd4923` and G002 runs `f6cdbeb`. [Eight-commit comparison](https://github.com/lfg-seth/firmware/compare/5bd4923...2dbf0a6), [board handoff](../operations/board-flashing-handoff.md).

The alpha and beta histories diverged at `82aefd1af`. A direct tip-to-alpha comparison counts 102 commits on the SNORR side, including 71 upstream beta-line commits and 31 fork commits. Using the beta release as the explicit three-way base models carrying the net changes in those 31 fork commits onto the alpha tree. Both alpha simulations returned Git exit 1. The protobuf submodule fast-forwards with its history present.

For the fork tip, the 12 remaining paths cover startup, GPS, serial/stream handling, next-hop routing, radio and SX126x handling, MQTT, the generated mesh protobuf header, the Heltec V4 target and the release-channel workflow. The header carries SNORR recorder metadata. A port needs to preserve that data and the fork's release safeguards. Git's path count only measures textual conflicts.

To reproduce in an isolated firmware checkout with both release tags, the two SNORR commits and initialized protobuf history:

```sh
git rev-list --left-right --count 2dbf0a6...v2.7.26.54e0d8d
git rev-list --left-right --count 2dbf0a6...v2.8.2.d5f1619
git merge-tree --write-tree --name-only --no-messages 2dbf0a6 v2.8.2.d5f1619
git merge-tree --write-tree --name-only --no-messages --merge-base=v2.7.26.54e0d8d v2.8.2.d5f1619 2dbf0a6
```

The first line from each merge command is the result tree ID. The remaining lines name the conflicted paths. Substitute `5bd4923` for the project-pin measurements.

## Field implications and recommendation

Keep the current 2.7.26 images for the field pilot. The 2.8.2 LoRa receive and SX126x transmit fixes make a bench port worth evaluating, particularly for a mixed RAK/Heltec relay path. Start from the release tag, bring over the SNORR changes, and revisit field rollout after upstream designates a 2.8 beta and the bench reproduces the pilot behavior. This assessment covers source and release history. Compilation, runtime, RF interoperability and deployment remain unverified. [Upstream radio fixes](https://github.com/meshtastic/firmware/releases/tag/v2.8.2.d5f1619).

- **Member GPS and identity.** 2.8 derives radio numbers from public keys. Verify that a known tracker still reports phone-free positions under its existing MeshLink device and assignment history after its radio ID changes. Position and telemetry default off in 2.8, and first-time US region selection on the device screen defaults to LongTurbo. Verify the private US LongFast slot 35 profile and reporting after reboot. [Upstream migration notes](https://github.com/meshtastic/firmware/releases/tag/v2.8.1.8e6a88d), [alpha identity code](https://github.com/meshtastic/firmware/blob/d5f16191ca28b01b5024f590f04a67f25d66f1b1/src/mesh/NodeDB.cpp#L4938), [SNORR profile](../operations/r001-cathedral-deployment.md), [MeshLink identity](../../.scratch/pilot/issues/12-assignment-radio-names.md).
- **Gateway and mixed-version traffic.** The alpha supports authenticated AES-CCM per channel. MeshLink's MQTT adapter and field sampler decrypt encrypted channel packets using AES-CTR. Selecting CCM requires decoder work. Prove a phone-free fix reaches the portal through a forced relay with the retained channel settings while 2.7 and 2.8 nodes share the bench. [Alpha channel encryption](https://github.com/meshtastic/firmware/blob/d5f16191ca28b01b5024f590f04a67f25d66f1b1/src/mesh/Router.cpp#L1333), [MQTT adapter](../../backend/mqtt_adapter.py), [field sampler](../../scripts/server/node_readings.py).
- **SNORR-specific behavior.** Verify neighbor RSSI/SNR, power and environmental telemetry through the gateway, offline SD recording and replay, and enrolled direct-hop survey after identity migration. Use the existing board-specific profile and recovery evidence before considering a field rollout. [Board handoff](../operations/board-flashing-handoff.md), [G002 offline recording](../operations/g002-shady-hollow-deployment.md).
