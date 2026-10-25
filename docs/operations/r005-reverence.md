# R005 Reverence placement — 2026-10-25

Owner requests **R005 `!f95b5501`** at supplied private coordinates, named
**Reverence** in Meshtastic and the database/portal, preserving short name
**R005**, with ROUTER, fixed position and B002 admin enrollment using the
[prepared script](repeater-role-change.md). No firmware update requested.

## Database and portal

Completed: replace the previous display name Showgirl with Reverence, save
the exact supplied latitude/longitude and owner-supplied location provenance.
The R005 record identity, number, short name, equipment and reporting settings
are preserved. Every other device's identity/configuration remains unchanged.
Authenticated live portal state includes Reverence. This verifies saved portal
metadata, not a newly received radio position or field coverage.

Private audit: `/root/r005-reverence-20261025T191836Z/` on the portal host,
including consistent SQLite backup, intended/before/after records and
authenticated portal state. Full pre-change backup
`meshlink-20261025T191836Z.tar.gz`, SHA256
`9a5db8584be9c3d54ef38a431465d1a402ec25e4f3c699a64225d98a29e868c7`.
Backup archive hash verified before mutation. Coordinates remain private.

## Radio completion and persistent USB access

Host USB enumeration matches recorded R005 serial **E93C5FF0F97DD76B** at
`/dev/ttyACM1`. Initial read-only attempt stops with Linux `PermissionError`.
After the owner's one-time ACL grant, read-only backup succeeds at
`private/bench/R005-role-20261025T192131573379Z/`, showing CLIENT. Apply evidence
is at `private/bench/R005-role-20261025T192145657389Z/`. The transaction saves
ROUTER, fixed position and B002 enrollment, but its reboot removes that initial
ACL and verification times out. The write is not blindly repeated.

Owner then authorizes persistent access for repeated node work. Install
`/etc/udev/rules.d/99-snorr-usb-serial.rules` using
[`grant-usb-serial-access.sh`](../../scripts/bench/grant-usb-serial-access.sh)
with desktop administrator authentication. Access is restricted to the project
radio USB interfaces, not every USB serial device. Installed rule and ACLs
verify R005 access while the unrelated u-blox receiver gets no named-user ACL.
R005 access survives its subsequent explicit reboot; no host reboot performed.
The rule is durable on disk and reloads through udev at boot.

Readback finds firmware role defaults reset rebroadcast mode, reporting
intervals, sleep default and the owner messaging flag. Restore only the changed
settings against the saved intended profile once ROUTER is already active;
set long name **Reverence** while preserving short name **R005** and the
original owner flags. Original security identity/private channel, LOCAL_ONLY,
180-second device/environment/power intervals, telemetry enablement and
21600-second standard neighbor interval are preserved. No firmware flash.

The USB PhoneAPI dump substitutes a role-dependent `power.ls_secs` (86400 for
ROUTER), so compare the actual saved power config through an independent admin
get-config response instead. Metadata now advertises ROUTER as expected.
Full intended local/module/channel bytes, owner identity except requested name
and role announcement, exact coordinates and firmware metadata pass before
and after explicit reboot. Evidence: `final-admin-verified-3.json` and
`final-reboot-admin-verified-3.json` in the apply directory. The reboot interrupts
the first verification process with SIGHUP; a separate read-only connection
completes the post-reboot check. Serial handles are closed.

Before commissioning another node with the prepared role script, correct its
handling of role-reset defaults, role metadata, PhoneAPI sleep substitution and
SDK raw-position protobuf evidence. The original script correctly fails its
strict comparison, but does not yet preserve all role-reset settings itself.
The subsequent [script correction](repeater-role-change.md#preservation-correction-and-verification-limits---2026-10-25)
implements those fixes with offline lifecycle and captured-R004 replay checks;
complete automatic hardware acceptance remains unverified.

Fresh RF/MQTT/portal delivery remains unverified: the database's latest R005
accepted G001 receipt is **2026-10-25T18:45:40.547Z**, before these settings
writes. Physical placement is owner-reported; installation completion, coverage,
forced relaying and runtime are unmeasured.

## Owner-confirmed equipment

Owner confirms **four 18650 cells, three solar panels and a fiberglass
antenna**. Live configuration now records those details, sets solar equipment
present and preserves all other equipment flags/configuration. Cell chemistry,
per-cell/pack capacity, wiring, panel ratings and antenna model/gain remain
unverified; no total capacity, runtime or measured solar input inferred.
Exact equipment strings and location/name pass authenticated portal readback;
all other devices and R005 short name are preserved.

Private equipment audit: `/root/r005-equipment-20261025T192210Z/`.
Pre-change backup `meshlink-20261025T192210Z.tar.gz`, SHA256
`99ec421f26b1ec33208940e69f19af8c38bb19aeee8478f5e1efcd32282390d1`.
