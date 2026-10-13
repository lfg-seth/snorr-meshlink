# Protocol baseline for the SNORR tracking pilot

Checked 2026-10-12 against primary sources. This is a research baseline, not a firmware selection or field result.
Owner input: roughly 20 member trackers eventually, possibly 5 to start; tentative GPS freshness of 5–15 minutes. Hardware models and quantities remain unknown.

## What the names mean

- **LoRaWAN** normally connects end devices through gateways to network/application servers in a star-of-stars architecture. Gateway packets reach the network server over an IP backbone. [Architecture](https://www.thethingsnetwork.org/docs/lorawan/architecture/), [LoRa Alliance backend](https://resources.lora-alliance.org/home/lorawan-back-end-interfaces-v1-0).
- **Meshtastic** is a radio mesh with managed flooding and next-hop routing behavior; it defines its own packet handling and forwarding. [Mesh algorithm](https://meshtastic.org/docs/overview/mesh-algo/).
- **MeshCore** provides multi-hop packet routing and distinct companion, repeater, room-server, and sensor applications. [Project README](https://github.com/meshcore-dev/MeshCore).
- **Project inference:** sharing LoRa radios does not establish compatibility. Evaluate these as separate network choices; do not plan cross-firmware relaying without a specifically verified bridge.

## Capability comparison

| Pilot need | LoRaWAN | Meshtastic | MeshCore |
| --- | --- | --- | --- |
| Passive dedicated-GPS reporting | Available in tracker products; behavior belongs to the chosen device/firmware, rather than a universal tracker setting. Example: Dragino LGT-92 automatically acquires and uploads GPS. [Manufacturer manual](https://www.dragino.com/downloads/downloads/LGT_92/LGT-92_LoRa_GPS_Tracker_UserManual_v1.6.8.pdf). | Radio GPS and automatic position broadcasts are documented; GPS acquisition and broadcast intervals are separate settings. [Position configuration](https://meshtastic.org/docs/configuration/radio/position/). | GPS settings exist in current companion source, but the official FAQ describes companion advertisements as user initiated. Autonomous periodic transmission must be verified for the specific build. [Companion source](https://raw.githubusercontent.com/meshcore-dev/MeshCore/main/examples/companion_radio/MyMesh.cpp), [FAQ §2.4](https://docs.meshcore.io/faq/). |
| Operation without a phone | Automatic tracker uploads are demonstrated by the LGT-92 manual; human messaging controls remain product-specific. [Manufacturer manual](https://www.dragino.com/downloads/downloads/LGT_92/LGT-92_LoRa_GPS_Tracker_UserManual_v1.6.8.pdf). | Onboard GPS supplies location; canned messages can be sent through supported buttons/keyboards. Device interaction still depends on hardware. [Position](https://meshtastic.org/docs/configuration/radio/position/), [Canned messages](https://meshtastic.org/docs/configuration/module/canned-message/). | The FAQ lists T-Deck and other Ultra devices for communication without a phone; companion firmware uses an external client. GPS tracking behavior needs separate verification. [FAQ §1.2](https://docs.meshcore.io/faq/). |
| Radio relaying | Standard gateway architecture is not a general member mesh. LoRaWAN has a separate standardized relay mechanism; support cannot be presumed in owned hardware. [Architecture](https://www.thethingsnetwork.org/docs/lorawan/architecture/), [TS011 relay](https://resources.lora-alliance.org/technical-specifications/ts011-1-0-0-relay), [revision](https://resources.lora-alliance.org/home/ts011-1-0-1-relay). | Nodes forward mesh packets subject to routing and rebroadcast rules. [Mesh algorithm](https://meshtastic.org/docs/overview/mesh-algo/). | Repeaters provide multi-hop routing; README describes companion nodes as non-repeating. [README](https://github.com/meshcore-dev/MeshCore). |
| Dispatch integration/backhaul | Gateway → network/application server → integration. The Things Stack exposes application uplinks through MQTT. [Architecture](https://www.thethingsnetwork.org/docs/lorawan/architecture/), [MQTT server](https://www.thethingsindustries.com/docs/integrations/other-integrations/mqtt/). | Internet-capable nodes forward packets through MQTT; client proxy can use a phone's network connection. Custom broker and channel uplink/downlink settings exist. [MQTT configuration](https://meshtastic.org/docs/configuration/module/mqtt/). | Companion connections support BLE, USB, or Wi-Fi depending on build, with NodeJS/Python clients listed upstream. A host integration is a plausible path; these sources do not establish a complete dispatch service. [README](https://github.com/meshcore-dev/MeshCore), [Companion protocol](https://docs.meshcore.io/companion_protocol/). |

## Reporting interval and achieved freshness

These are different project measures:

1. **GPS acquisition interval:** how often the device tries to obtain a fix.
2. **Transmission interval:** how often it attempts to send position information.
3. **Delivery delay/missing reports:** what reaches the receiving system, and when.
4. **Position age:** current time minus the time the GPS position was measured.

**Project inference:** a 15-minute transmission timer cannot by itself guarantee positions less than 15 minutes old. Lost packets, an old fix, or unavailable backhaul can increase displayed position age. Measure all four; dispatch should preserve measurement and receipt times separately.

- Meshtastic exposes `gps_update_interval`, `position_broadcast_secs`, and movement-based smart-broadcast controls. It also documents a positional timestamp flag. [Position configuration](https://meshtastic.org/docs/configuration/radio/position/).
- Meshtastic's mesh documentation describes traffic throttling and scaling of intervals in larger meshes; role affects scaling. Therefore a configured timer is not proof of achieved delivery. [Mesh algorithm](https://meshtastic.org/docs/overview/mesh-algo/).
- Meshtastic **MQTT map reports** are a separate feature with a documented one-hour minimum. A 5–15-minute tracking portal should evaluate position-packet ingestion rather than equating map-report publication with member reporting. This is a project inference from the documented distinction. [MQTT configuration](https://meshtastic.org/docs/configuration/module/mqtt/).
- MeshCore's companion source stores `gps`/`gps_interval` settings when GPS support is compiled in. That establishes configuration support, not automatic radio reporting. The FAQ distinguishes local zero-hop adverts from flooded adverts and describes client adverts as user initiated. [Source](https://raw.githubusercontent.com/meshcore-dev/MeshCore/main/examples/companion_radio/MyMesh.cpp), [FAQ §2.4](https://docs.meshcore.io/faq/).
- MeshCore repeater/sensor CLI documentation has GPS sharing policy and separate local/flood advert timers. Those role-specific controls should not be assumed to apply to every member device. [CLI commands](https://docs.meshcore.io/cli_commands/).
- LoRaWAN tracker timing is device-specific: the LGT-92 manual documents configured uplink periods and motion-dependent behavior. It is an example, not evidence about the owner's inventory. [Manufacturer manual](https://www.dragino.com/downloads/downloads/LGT_92/LGT-92_LoRa_GPS_Tracker_UserManual_v1.6.8.pdf).

## Is a firmware fork necessary now?

**Provisional inference: not established.** Meshtastic already exposes broadcast timing settings. MeshCore's documented default companion advert behavior raises a specific question for passive tracking, but a different supported build, telemetry workflow, or integration may satisfy it. Inventory and a small bench test should identify an actual missing behavior before committing to a fork. [Meshtastic position settings](https://meshtastic.org/docs/configuration/radio/position/), [MeshCore FAQ](https://docs.meshcore.io/faq/), [MeshCore source](https://raw.githubusercontent.com/meshcore-dev/MeshCore/main/examples/companion_radio/MyMesh.cpp).

Do not confuse automatic GPS acquisition, local advertising, flooded reporting, and dispatch delivery when describing a customization requirement.

## Small next evaluation

Proposed project steps; these are not completed tests or selected firmware:

1. Inventory exact boards/revisions, radio variants, GPS modules, displays/controls, and power supplies. Compare models with the official supported-device lists. [Meshtastic devices](https://meshtastic.org/docs/hardware/devices/), [MeshCore flasher](https://flasher.meshcore.io/).
2. For compatible owned hardware, bench-test one GPS member node and one receiver. Remove the phone after setup; reboot and confirm passive reports continue with fresh fixes.
3. Record acquisition time, transmission/receipt time, GPS validity, displayed age, and power consumption while stationary and moving. Try the tentative 5–15-minute behavior without assuming it is an acceptance criterion yet.
4. Add a relay and an internet ingestion host; interrupt backhaul and restore it. Observe stale/missing data and reconnect behavior before designing multiple backhauls.
5. Start field evidence with as few as 5 member nodes if available. Treat scaling to about 20 as a separate measurement checkpoint.

## Limits and recheck points

- No owned hardware was inspected, flashed, or tested; no coverage, battery life, capacity, or reliability is established.
- Online docs and GitHub `main` are moving references, not a pinned deployment release. Record firmware/build versions during bench testing and recheck behavior against that source version.
- Meshtastic position and mesh pages give differing default-interval descriptions. This report deliberately relies on named configurable settings, not a universal default; verify effective behavior on the selected release. [Position page](https://meshtastic.org/docs/configuration/radio/position/), [Mesh page](https://meshtastic.org/docs/overview/mesh-algo/).
- MeshCore README/FAQ descriptions are broad; current source also exposes restricted client-repeat controls. Do not infer that arbitrary companion nodes relay by default. This report does not recommend enabling that feature. [README](https://github.com/meshcore-dev/MeshCore), [Companion source](https://raw.githubusercontent.com/meshcore-dev/MeshCore/main/examples/companion_radio/MyMesh.cpp).
- This comparison does not assess radio compliance, installation permission, member-data retention, or publication consent. No operating frequencies, power levels, or purchases are prescribed.
