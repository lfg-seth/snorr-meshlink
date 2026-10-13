# Firmware workspace

Established 2026-10-13 at the owner's request. The project includes the owner's [Meshtastic firmware fork](https://github.com/lfg-seth/firmware) as the Git submodule at `firmware/`.

## RAK branch and release baseline

- Fork branch: [`snorr/rak-survey`](https://github.com/lfg-seth/firmware/tree/snorr/rak-survey).
- Official latest public GitHub release verified on 2026-10-13: [Meshtastic 2.7.26.54e0d8d Beta](https://github.com/meshtastic/firmware/releases/tag/v2.7.26.54e0d8d). GitHub marks it latest and `prerelease=false`; the release title still calls it Beta. This is the published release baseline, not upstream development head.
- Release tag: `v2.7.26.54e0d8d`.
- Initial branch/submodule commit: `54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb`.
- Initial branch tree is exactly the public release tree. No custom survey module or project preferences have been added. Existing fork `develop` remains unchanged at `76d5156e72d9d9aaa9722b7bbc1336335b685984`; its [old customizations](old-firmware-fork.md) were not merged into this branch.
- Firmware remotes: `origin` is `git@github.com:lfg-seth/firmware.git`; local `upstream` is `https://github.com/meshtastic/firmware.git`.
- Nested dependencies initialized at release-pinned commits: protobufs `6b1ded439633cd03d4af85b44231b91d1d106278`, meshtestic `dcac7e5673005f4d8a2b1f0f6e06877b689d7519`.

The outer repository records an exact firmware commit. The `.gitmodules` branch setting identifies the development branch for explicit remote updates; ordinary submodule initialization follows the recorded commit, not the latest branch tip.

## Clone and develop

From the MeshLink repository root:

```sh
git submodule update --init --recursive
git -C firmware switch snorr/rak-survey
```

Fresh clones normally start submodules detached at the pinned commit. If the local branch does not yet exist:

```sh
git -C firmware fetch origin
git -C firmware switch --track origin/snorr/rak-survey
```

The upstream remote is local configuration and is not inherited by a fresh clone. Add it once when needed:

```sh
git -C firmware remote add upstream https://github.com/meshtastic/firmware.git
```

Read `firmware/AGENTS.md` and its referenced `.github/copilot-instructions.md` before firmware changes. Commit and push firmware changes inside `firmware/` first, then commit/push the updated gitlink in this repository. This avoids publishing an outer pointer to an unavailable firmware commit. Do not use automatic remote updates to silently change the pilot baseline.

The local checkout was initialized shallowly; fetch additional upstream history if a later merge/comparison requires it. Recheck the official release when updating, inspect differences, and record the new exact baseline. Do not rewrite the existing fork's branches or carry old embedded secrets into new configuration.

## Verification and next step

Verified exact release/branch SHA, clean firmware tree, initialized nested dependency pins and publication of `snorr/rak-survey`. No firmware build, flash or hardware test performed. The exact owned RAK core remains unidentified; `rak4631` is a candidate target only if inspection confirms that core.

Next: identify the RAK core and prepare the requested dedicated direct-link ping/pong responder, after checking behavior against this pinned release rather than the earlier moving-source review. Setup does not implement the responder or alter radio restrictions.
