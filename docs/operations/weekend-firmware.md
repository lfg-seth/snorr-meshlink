# Weekend repeater and screenless V4 firmware

Owner selects RAK repeaters and screenless V4 gateways for Sunday deployment,
with two bench windows beforehand. This procedure covers firmware preparation
and its remaining checks, not a claim of accepted mountain coverage/endurance.
GH-4 is [resolved by replacement INA219 boards](ina219-audit.md#current-disposition---2026-11-12).

## Firmware ownership and files

This session prepares RAK install/recovery inputs. The other active chat owns
the screenless V4/SD implementation and its board; do not mix its unfinished
source/build with the RAK candidate. [Detailed ownership/checklist](../../.scratch/tasks/weekend-infrastructure-firmware.md).

Use the already bench-proven ordinary **rak4631 / 2.7.26.4c96b9b** from published
source **4c96b9ba0360f01752892a41d09ccacda82747bb**. The
[fixed deployment manifest](repeater-deployment-image.json) names the exact
UF2 and application-only OTA ZIP used in the
[October 24 bench](repeater-update.md#r006-and-gateway-admin-bench---2026-10-24).
The source is published; these binaries remain an explicit local bundle, not
a published release or SNORR 1.0.0. The manifest's `hardwareVerified: false`
preserves build-provenance semantics; linked per-board evidence is separate.

The private local bundle contains only `build-manifest.json`, `SHA256SUMS`,
`firmware-rak4631-2.7.26.4c96b9b.uf2` and
`firmware-rak4631-2.7.26.4c96b9b-ota.zip`, under
`private/bench/releases/weekend-rak-4c96b9b/` in the prepared checkout. A copy
must retain all four files byte-for-byte. The updater verifies the exact set,
manifest bytes, sizes, SHA256 and application-only nRF52840 UF2 bounds before
using it. The older `repeater-production-image.json`/`local-0634b77` bundle is
retained as historical evidence and is no longer the updater's selected local
candidate. The default public release pin remains unset, with no automatic
fallback to local or older firmware.

The original checkout also has
`private/bench/releases/weekend-rak-4c96b9b-offline-kit.zip`. Extract this outer
transport archive before use and supply its directory to `--local-bundle`;
only the inner `-ota.zip` is a Nordic OTA package. The outer archive contains
no credentials or device profiles. Its SHA256 is
`f7c4ab1d6c3aa3924df9bccd952b305bc07ce9734ce9b8931dc60fe721f83eb1`.

## RAK bench order

Use the existing Python environment with `scripts/bench/repeater-requirements.txt`.
Run from this prepared checkout; connect one selected R001-R006 and close other
serial users. Replace R001 below with that unit's recorded identity.

```sh
# Read-only image/profile plan; no serial connection:
python scripts/bench/update-repeater.py --number R001 --show-plan --local-bundle private/bench/releases/weekend-rak-4c96b9b

# Verify assets and privately identify/back up the board; no saved writes:
python scripts/bench/update-repeater.py --number R001 --dry-run --local-bundle private/bench/releases/weekend-rak-4c96b9b
```

Inspect the private original/readback against that physical unit. If it already
has the matching image and intended telemetry profile, a new flash is not
needed. If the exact image is installed but the 180-second/fitted-sensor profile
needs application, use `--config-only`. If an image update is required, omit
`--dry-run` and `--config-only` to run the identified UF2 update. Both write
paths require explicit selection of the connected board and preserve its own
keys/channels. Unknown/new boards require separate provisioning; never borrow
another board's identity to pass the guard.

**Run the role/location/admin step after any updater write.** The updater
intentionally saves CLIENT. Use the existing helper to apply the selected
infrastructure role, actual decimal fixed coordinates and B002 admin, then
verify them through reboot:

```sh
python scripts/bench/set-repeater-role.py R001
python scripts/bench/set-repeater-role.py R001 --apply
```

Default role is ROUTER; `--role CLIENT` is the explicit alternative. Retain the
selected policy for each site. See [the helper procedure](repeater-role-change.md)
for key provenance, identity checks, prompts and partial-write handling. Do not
blindly repeat a remote write after an ambiguous ACK: independently read the
target's result and reboot state first.

## Before the firmware freeze

- Verify each selected RAK's complete profile/keys after reboot, intended role,
  fixed position/admin, and fresh device/fitted-sensor/SNNS delivery. Keep raw
  coordinates and config evidence private. Verify the connected B002 controller
  still has the enrolled identity.
- Force an actual relay path excluding direct reception, including remote
  read/change/readback and interrupted-command recovery. Show member GPS still
  reaches the selected V4 and dispatch path; record GPS measurement age.
- Have the V4 owner supply exact source/image/checksums and boot/profile/SD
  evidence, credential-log removal, verified broker TLS identity and cold-clock
  behavior, Wi-Fi/broker loss recovery, and non-blocking SD failure behavior.
  Preserve its selected 300-second reports, suppressed relaying/downlinks and
  existing wire compatibility. These are checks to complete, not claimed passes.
- Retain exact passing artifacts, per-device results and recovery inputs before
  departure. Report remaining failures/unverified gates to the owner. Source
  packaging or a few fresh cycles do not establish sustained unattended operation.
