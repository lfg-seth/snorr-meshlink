# SNORR MeshLink language

Terms used for the SNORR member-tracking and communications project.

## Language

**Member node**:
A device carried by a SNORR member for dedicated GPS tracking and supporting communications.
_Avoid_: Client when it could mean a person or a software client.

**Device number**:
A stable human-readable label for a physical member node, independent of who carries it.

**Radio short name**:
The compact displayed label of a member node, tied to its device number across changes of carrier.
_Avoid_: Hardware identifier or database identity.

**Device assignment**:
The association between a numbered member node and the member carrying it during a recorded period. Reassignment preserves earlier associations rather than relabelling old tracks.

**Recorded position**:
A member node's reported GPS measurement at a stated time. A connecting line between recorded positions is an estimate, not a measured route.

**Repeater**:
A fixed or temporarily placed radio node intended to relay member traffic across the operating area. The exact relay behavior depends on the network selected.

**Backhaul**:
An internet connection that carries radio-network information to remote systems, such as dispatch.

**Dispatch portal**:
The planned web interface for dispatch and authorized members to view node locations and status.

**Infrastructure node**:
A radio device serving a repeater or internet-backhaul role rather than being assigned as a member tracker.

**Infrastructure health**:
The recorded operational condition of an infrastructure node, including its power supply, communications and fitted environmental or security sensors.

**Passive tracking**:
Location reporting from a member node without the member repeatedly operating a phone or device.

**Position age**:
The time elapsed since a member node measured the GPS position being displayed, distinct from the time dispatch received it.

**Field pilot**:
A limited, measured trial used to decide whether a design is ready for wider deployment.
