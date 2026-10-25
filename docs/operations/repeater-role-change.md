# Set a RAK repeater's long name, role, fixed location and B002 admin

Prepared 2026-10-25 at the owner's request, initially for CLIENT repeaters.
R004/R005 now retain ROUTER after their separately recorded recoveries.
The owner also requests a prompted static location and B002
admin enrollment. Updated to prompt for a Meshtastic long name while preserving
the existing short name, and write a private text log for later portal database
reconciliation. This procedure changes configuration; no firmware reflash or
factory reset is needed. No board was changed while preparing this tool.
The October 25 preservation correction below is offline-tested; its complete
automatic flow still needs a selected-board acceptance run. R004/R005's
separate manual recoveries are recorded in their operations evidence.

CLIENT already rebroadcasts eligible traffic. ROUTER gives infrastructure
rebroadcast priority; placement still determines whether it helps coverage.
Use this for selected RAK relays, not a blanket change of gateways or member
trackers. Retain CLIENT on the Wi-Fi/MQTT gateways and member nodes.
Upstream distinguishes these behaviors in its
[device configuration](https://meshtastic.org/docs/configuration/radio/device/).
ROUTER can reduce local app/Bluetooth availability, depending on platform;
retain USB access while commissioning. Do not select the deprecated REPEATER
role for this task.

## Linux laptop over USB

Use a checkout containing the preservation correction. Until it is integrated
into main, fetch and switch to **`codex/router-profile-preservation`** with a
clean working tree (preserve local changes first). Run from the repository root:

```sh
git fetch origin
git switch codex/router-profile-preservation
git pull --ff-only
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r scripts/bench/repeater-requirements.txt

# Connect R001 via USB; close other apps/serial tools using it.
# First enter the long name and decimal coordinates; back up without saving:
python scripts/bench/set-repeater-role.py R001

# Enter name/coordinates again; save long name, ROUTER, location and B002 admin:
python scripts/bench/set-repeater-role.py R001 --apply
```

If the branch does not exist locally, use
`git switch --track origin/codex/router-profile-preservation`.
If serial permission is denied on Debian/Ubuntu, add
your login to `dialout` with `sudo usermod -aG dialout "$USER"`, then log out
and back in. Run the script as your normal user.

On the owner's Linux workstation (`setheth`, UID 1000), persistent access for
the project radio USB interfaces can instead be installed once:

```sh
sudo bash scripts/bench/grant-usb-serial-access.sh
```

This installs `/etc/udev/rules.d/99-snorr-usb-serial.rules` and immediately
reapplies permissions to connected serial devices. Named-user read/write ACLs
cover RAK4631 `239a:8029`, ESP32-S3 native USB `303a:1001` and CP210x
`10c4:ea60` serial interfaces. It covers future nodes with those interfaces
across reconnects, node reboots and host reboots; other USB IDs require a
separate rule. IDs identify interfaces, not a trusted radio identity: retain
the configuration script's USB serial/node checks. No world-writable ports,
group changes or sudo-policy grants. Remove that rule and reload udev to stop
future grants; existing ACLs last until unplugging. Installation requires
administrator authentication; ordinary bench operations run as the owner.

Repeat individually for R002 through R006 as needed. The script locates the
recorded USB serial automatically and independently checks node ID, RAK4631
hardware, existing keys/private channel and enabled LoRa TX before a write.
An optional `--port /dev/ttyACM0` must still match that USB identity.
Every run first prompts for the **Meshtastic long name**. The existing short
name and owner flags are preserved. Enter a nonblank name of at most 39 UTF-8
bytes (the firmware's string capacity); longer names and control characters
are rejected rather than silently truncated. Surrounding whitespace is removed.
Then it prompts for **latitude, then longitude in decimal degrees**, using a
dot as the decimal separator. Use negative longitude for west and negative
latitude for south. Latitude must be -90 through 90, longitude -180 through
180; invalid input is prompted again. Coordinates are rounded to Meshtastic's
seven decimal places and sent as integer units to avoid float truncation.
The script enables `position.fixed_position` and sets the entered coordinates
using the SDK's fixed-position admin command. Existing altitude is retained,
or left 0/unspecified when absent; no elevation is invented. GPS mode/pins,
position cadence and telemetry remain unchanged. See upstream
[fixed-position configuration](https://meshtastic.org/docs/configuration/radio/position/).
Coordinates stay in private evidence, never in tracked project files.

Default role is ROUTER. To select CLIENT instead, while still setting the
prompted fixed location and B002 admin:

```sh
python scripts/bench/set-repeater-role.py R001 --role CLIENT --apply
```

The script backs up the complete actual saved profile, then uses a settings
transaction for the long name, role, fixed-position setting, coordinates and
B002 admin enrollment, and commits/reboots. If the role changes, firmware can
reset reporting, rebroadcast, sleep/display/GPS intervals and the owner
messaging flag. The script reconnects, validates identity/role/point, and makes
one planned restoration of those known reset fields to the original intended
profile while keeping the new role active. This may require another settings
reboot before full verification and the final explicit reboot check.

The result retains the original telemetry cadence, including **180 seconds**
on the current three-minute profiles; it does not impose 180 seconds on a
device that started with another cadence. Enablement and fitted-sensor choices
stay as backed up. Intentional config changes remain `device.role`,
`position.fixed_position` and the admin allowlist; fixed coordinates live in
the node database separately. A changed key/channel/name, wrong role/point,
firmware difference or configuration change outside the known reset fields
stops restoration before another write. Failed/ambiguous writes are never
retried automatically.
Existing admins are preserved, B002 is not duplicated, and a full three-key
allowlist without B002 stops before any device write.

B002 `!699ca878`'s public key is pinned in the script:

```text
l5VRR8C6wnkeSNP1KiYKPYEBv/Of10/4rU+VHmlq2ks=
```

It matches B002's private `B002-update-20261024/before.json`, both final
`verified-*.json` reboot readbacks and the admin bench's final B002 readback.
Only the public key is included; B002's private key stays private. Enrollment
authorizes that radio identity, so use B002 as the connected remote controller.
If B002's key pair is ever regenerated, update this pin against a fresh verified
readback before commissioning more RAKs.

Private backups, intended configuration, logs and readbacks are saved under
ignored `private/bench/R001-role-<timestamp>/` with restrictive Linux permissions.
The comparison requires exact config/module/channel bytes, keys and owner
identity to match the intended profile, including the requested long name and
unchanged short name; only the user role announcement may
change. Only the requested role announcement may differ in firmware metadata;
all other metadata and saved fixed coordinates must match too, both
after save and after an explicit reboot. When long name, role, fixed location and B002
admin already match, the script backs up and makes no write. Never commit
these private files. Selecting CLIENT is not a full rollback: fixed position
and admin enrollment remain intentional parts of this script's operation.

Each run also writes **`reconciliation.txt`** in that same private directory,
and prints its path before connecting. It records UTC start/finish times, device
number, node ID, USB serial, old/new long name, preserved short name, requested
role and exact fixed coordinates, firmware version and separate save/reboot
verification results. It contains no channel or identity keys. Read-only runs,
already-matched runs, failures and verified saves have distinct outcomes; an
interrupted process may leave an `IN PROGRESS` log. Only completed checks are
marked passed, even if readback JSON exists from a failed comparison. Keep this
local file for later reconciliation; the script does not update the portal DB.
The log contains private location data, so keep it under ignored `private/`.
`role-defaults.json` records the state before planned restoration and
`restoration-plan.json` lists its configuration sections. The text log records
whether restoration was needed/saved/verified, separately from final results.

## Preservation correction and verification limits - 2026-10-25

The [R005 run](r005-reverence.md) and [R004 recovery](r004-three-minute.md#router-and-three-minute-profile-restoration---2026-10-25)
demonstrated role-default resets. The correction restores their known fields
after the new role takes effect, compares the requested role in metadata, and
uses an independent admin power response for actual saved sleep settings
instead of the role default substituted by USB PhoneAPI. SDK raw-position
protobufs are excluded from JSON evidence while exact integer coordinates
are retained. Absent/false optional owner messaging flags are compared with
their same effective false value; true/false changes remain verified.

All **72 offline bench tests** pass. A lifecycle regression reproduces
180-to-43,200-second resets across fresh USB sessions, then verifies restoration
and explicit-reboot comparison. Other cases check owner flags, additional reset
intervals, power reads, raw-position JSON, unexpected-change rejection and no
retry after an ambiguous restoration write. Offline replay of R004's actual
failed readback produces the exact intended local/module bytes and the same
device/power/telemetry/neighbor restoration sections as its measured recovery.

No radio was changed while implementing the correction. End-to-end automatic
hardware acceptance and fresh RF/gateway/portal cadence remain unverified.
A failed run must not be treated as a verified configuration or reconciled
into the portal as one. Keep the selected board accessible for independent
readback. Historical failed runs still require inspection against their saved
intended profile; rerunning creates a new baseline from the current state.

## Failures and follow-up

If anything fails after a write, some or all settings may already have saved. There is no
automatic retry or rollback. Inspect private evidence and read the role locally
before retrying. Inspect position/security too; keep the board accessible until
a successful saved readback.
Afterwards confirm fresh telemetry/SNNS and member GPS delivery through the
required gateways; configuration verification does not establish RF coverage,
runtime, forced relaying or portal acceptance. Record actual board changes in
inventory and field/operation records after the laptop run.

The older `update-repeater.py` profile sets CLIENT deliberately. Running that
updater again will set CLIENT again; reapply this role step after it if ROUTER
is still intended. This tool leaves that existing updater policy unchanged.

## Direct Meshtastic CLI and remote administration

With the same virtual environment, the basic local commands are:

```sh
meshtastic --port /dev/ttyACM0 --get device.role
meshtastic --port /dev/ttyACM0 --set device.role ROUTER
# Wait for reboot, then independently read again:
meshtastic --port /dev/ttyACM0 --get device.role
```

These raw commands lack the script's identity guard, private full backup and
full profile comparison. Double-check the connected board.

Remote configuration over LoRa is supported when the target already trusts the
connected controller's public key in its security admin allowlist and both
nodes have a working RF path. A shared private channel alone is insufficient.
See upstream [remote administration](https://meshtastic.org/docs/configuration/remote-admin/).
For an already authorized controller on USB, for example R001 as target:

```sh
meshtastic --port /dev/ttyACM0 --dest '!a65601b3' --get device.role
meshtastic --port /dev/ttyACM0 --dest '!a65601b3' --set device.role ROUTER
# Wait for target reboot; independently read the target again:
meshtastic --port /dev/ttyACM0 --dest '!a65601b3' --get device.role
```

There is no fleet broadcast role update here. This script enrolls B002 over USB
on the selected RAK only; it does not enable MQTT downlinks. Fleet enrollment
remains unverified until the owner runs it on each selected board. R006's temporary
B002 authorization was explicitly removed after the
[admin bench](repeater-update.md#r006-and-gateway-admin-bench---2026-10-24).
That bench found `ADMIN_BAD_SESSION_KEY` responses even when a rebooting write
executed. Do not treat a failed ACK as proof the role stayed unchanged, or
blindly repeat the mutation. USB is the prepared path; these remote CLI examples
have not been accepted on the current fleet or through a forced relay. This is
a settings update, distinct from any over-the-air firmware update.
