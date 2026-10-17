# R003 AHT compatibility build

Built and flashed 2026-10-14 at the owner's request. **R003 now supplies temperature and humidity through both V3 gateways.** R001/R002 remain on their previously prepared stock firmware; the original two-repeater field allocation is unchanged.

For a new RAK update, use the [current released-image flashing handoff](board-flashing-handoff.md) and download its pinned prerelease. The build commands and cc5907b artifacts below are historical reproduction/recovery evidence, not the default for routine flashing. The newer release retains this AHT fix and adds neighbor reporting; no newer hardware flash is claimed here.

## Source and scope

- Release baseline: `54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb` (`2.7.26.54e0d8d`).
- Final source: [`cc5907b1fc7b4c200e23f43e10baa54c39aeaf25`](https://github.com/lfg-seth/firmware/commit/cc5907b1fc7b4c200e23f43e10baa54c39aeaf25), branch `snorr/rak-survey`. Functional patch is in preceding commit [`b0aa05b41`](https://github.com/lfg-seth/firmware/commit/b0aa05b41); the final commit only shortens its explanation. Both are published; no history rewritten.
- Port the relevant behavior from the owner's [`e617a4dcf` AHT fix](https://github.com/lfg-seth/firmware/commit/e617a4dcfd95500c73f570c583f3ea6d02aa4881): remove the RAK4631 `HAS_NCP5623` definition so the existing scanner includes AHT detection. The optional NCP5623 RGB controller is consequently unavailable in this build. No AHT driver patch, forced telemetry cadence, old broker defaults, survey code or other old-fork changes carried forward.
- Firmware version: **`2.7.26.cc5907b`**, target `rak4631`, SoftDevice S140 6.1.1 board/linker definition.
- R003: `!05237743`, normal Windows COM14, USB serial `397EBE4F36E1F126`. Owner tentatively identifies its fitted sensor as AHT21/0x38; successful AHT-family readings do not independently verify the printed model or calibration.

## Build and artifacts

Windows native PlatformIO **6.1.19**, `nordicnrf52@10.11.0`, pinned GCC ARM toolchain `1.90301.200702`, framework `1.10601.0` at `9ddcbc9568b12f102f9e88bd4d1b88ea789213a4`. Nested firmware dependencies remain pinned. No private channel/broker configuration baked into source.

Build from the recorded firmware checkout:

```sh
git submodule update --init --recursive
cd firmware
pio run -e rak4631
```

The desktop uses `C:/Users/Setheth/.platformio/penv/Scripts/platformio.exe`. The first compiler download stalled; the identical official archive was downloaded separately, checked against registry SHA256 `4e7ffd129a0cb187677de801acf37b1167fd8df85ca03cdb08502fa68e9cd79d`, and installed through PlatformIO's package manager. Remaining dependencies installed normally. Build succeeds in 350.68 seconds after compiler preparation. Flash use is 757,812/815,104 bytes (93.0%); RAM 105,244/248,832 bytes (42.3%). Vendor-library warnings remain, including INA3221 array-bound warnings; no new library fixes or full native/MCP regression-suite result claimed.

`trunk fmt` was attempted but Trunk is unavailable on this Windows host. The changed line passes scoped `clang-format 16.0.3` with no replacements; Git whitespace checks pass. Existing unrelated whole-file formatting differences were not reformatted.

Artifacts and build log are retained under ignored `private/bench/`, including `R003-aht-cc5907b/checksums.json`. Exact build hashes:

| Artifact | Bytes | SHA256 |
| --- | --- | --- |
| `firmware-rak4631-2.7.26.cc5907b.uf2` | 1,516,032 | `9a6e3f2ae33385c1618fd4bf7c89011596a56f842afcc12db9dbc322e8da96ba` |
| `firmware-rak4631-2.7.26.cc5907b.zip` (Nordic OTA package) | 758,770 | `268d194304375c14b481eda3d02fbfd4e4a8759fc52d3a94619381364a53de7b` |

## Flash and verification

Privately snapshot R003's current profile and keys. Identity-check COM14, request DFU, confirm its USB serial on COM16 and single RAK4631 drive, verify `INFO_UF2.TXT` identifies WisBlock RAK4631, then copy the checksum-verified custom UF2. It returns to COM14 without a factory reset or bootloader change.

Independent API readback verifies custom version, stable node identity, private pilot channel, US/LONG_FAST slot 35, hop limit 3, 10 dBm, ROUTER/local-only and device/environment telemetry enabled at **900 seconds each**. Entire `localConfig`, `moduleConfig` and channel arrays match the pre-flash snapshot exactly, including keys and debug API off. No gateway configuration changed.

- Local sensor response: **22.90535°C, 35.01892% RH**.
- New automatic device packet `1993071474` reaches both G001/COM6 and G002/COM7: voltage **4.267 V**, level 101 (charging/external-power/no-battery status), uptime 66 seconds.
- New automatic environmental packet `2012857203` reaches both gateways: **22.97821°C, 34.962845% RH**. Four of four expected new device/environment gateway receipts pass. Older packets drained from gateway queues on connection are excluded from that count.
- Initial custom-build telemetry time fields are 66/91, not valid Unix wall-clock timestamps. Future portal telemetry must handle clock validity and gateway receipt time explicitly; no telemetry age guarantee follows from these samples.

This proves a short sensor-read/radio-delivery check and configuration preservation across the flash reboot. It does not measure sensor calibration, sustained 15-minute delivery, battery/solar runtime, required relay paths or field coverage. The portal still ingests GPS only; no battery/environment display integration was performed. [TEST-008](../../records/field-results.md#test-008--r003-custom-aht-build-and-radio-telemetry).
