# Change a RAK repeater's Meshtastic role

Prepared 2026-10-25 at the owner's request. R001–R006's last recorded saved
role is CLIENT. This procedure changes configuration; no firmware reflash or
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

Fetch and switch to the published branch with a clean working tree (preserve any
local changes first). Run from the repository root:

```sh
git fetch origin
git switch --track origin/codex/repeater-role-cli
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r scripts/bench/repeater-requirements.txt

# Connect R001 via USB; close other apps/serial tools using it.
# First inspect and back up without saving anything:
python scripts/bench/set-repeater-role.py R001

# Save ROUTER, reconnect and verify the full configuration through reboot:
python scripts/bench/set-repeater-role.py R001 --apply
```

If the branch already exists locally, use `git switch codex/repeater-role-cli`
and `git pull --ff-only`. If serial permission is denied on Debian/Ubuntu, add
your login to `dialout` with `sudo usermod -aG dialout "$USER"`, then log out
and back in. Run the script as your normal user.

Repeat individually for R002 through R006 as needed. The script locates the
recorded USB serial automatically and independently checks node ID, RAK4631
hardware, existing keys/private channel and enabled LoRa TX before a write.
An optional `--port /dev/ttyACM0` must still match that USB identity.
Default role is ROUTER; undo with:

```sh
python scripts/bench/set-repeater-role.py R001 --role CLIENT --apply
```

Only the `device` section is written, with only its role changed in memory.
Private backups, intended configuration, logs and readbacks are saved under
ignored `private/bench/R001-role-<timestamp>/` with restrictive Linux permissions.
The comparison requires exact config/module/channel bytes, keys and owner
identity to match the intended profile; only the user role announcement may
change. Firmware metadata must match too. An already selected role produces
a backup and no write. Never commit these private files.

If anything fails after a write, the role may already have saved. There is no
automatic retry or rollback. Inspect private evidence and read the role locally
before retrying. Keep the board accessible until a successful saved readback.
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

There is no fleet broadcast role update here. Admin enrollment requires existing
authorized access to each target; this script does not enroll keys or enable
MQTT downlinks. Current fleet admin enrollment is not verified. R006's temporary
B002 authorization was explicitly removed after the
[admin bench](repeater-update.md#r006-and-gateway-admin-bench---2026-10-24).
That bench found `ADMIN_BAD_SESSION_KEY` responses even when a rebooting write
executed. Do not treat a failed ACK as proof the role stayed unchanged, or
blindly repeat the mutation. USB is the prepared path; these remote CLI examples
have not been accepted on the current fleet or through a forced relay. This is
a settings update, distinct from any over-the-air firmware update.
