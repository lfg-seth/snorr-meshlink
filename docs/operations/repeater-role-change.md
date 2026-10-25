# Set a RAK repeater's role, fixed location and B002 admin

Prepared 2026-10-25 at the owner's request. R001–R006's last recorded saved
role is CLIENT. The owner also requests a prompted static location and B002
admin enrollment. This procedure changes configuration; no firmware reflash or
factory reset is needed. No board was changed while preparing this tool.

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

Fetch and switch to main with a clean working tree (preserve any
local changes first). Run from the repository root:

```sh
git fetch origin
git switch main
git pull --ff-only
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r scripts/bench/repeater-requirements.txt

# Connect R001 via USB; close other apps/serial tools using it.
# First enter decimal coordinates and back up without saving anything:
python scripts/bench/set-repeater-role.py R001

# Enter coordinates again; save ROUTER, fixed location and B002 admin:
python scripts/bench/set-repeater-role.py R001 --apply
```

If main does not exist locally, use `git switch --track origin/main`.
If serial permission is denied on Debian/Ubuntu, add
your login to `dialout` with `sudo usermod -aG dialout "$USER"`, then log out
and back in. Run the script as your normal user.

Repeat individually for R002 through R006 as needed. The script locates the
recorded USB serial automatically and independently checks node ID, RAK4631
hardware, existing keys/private channel and enabled LoRa TX before a write.
An optional `--port /dev/ttyACM0` must still match that USB identity.
Every run prompts for **latitude, then longitude in decimal degrees**, using a
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

The script uses a settings transaction for the role, fixed-position setting,
coordinates and B002 admin enrollment, then commits/reboots. The only changed
config fields are `device.role`, `position.fixed_position` and the admin
allowlist; the fixed coordinate values live in the node database separately.
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
identity to match the intended profile; only the user role announcement may
change. Firmware metadata and saved fixed coordinates must match too, both
after save and after an explicit reboot. When role, fixed location and B002
admin already match, the script backs up and makes no write. Never commit
these private files. Selecting CLIENT is not a full rollback: fixed position
and admin enrollment remain intentional parts of this script's operation.

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
