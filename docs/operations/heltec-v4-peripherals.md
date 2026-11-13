# Screenless Heltec V4 peripheral initialization

## Completed bench check - 2026-11-12

Owner selects one screenless V4 with INA219 and an inserted 32 GB FAT32 card.
After USB connection, Windows identifies **COM31 / F8:5B:1B:BF:06:38**.
Esptool independently identifies **ESP32-S3 revision v0.2, embedded 2 MB PSRAM,
16 MB quad flash**, MAC **f8:5b:1b:bf:06:38**. This supports the original
S3R2 V4 target, not V4-R8; exact PCB subrevision remains unverified. No
historical device number, Meshtastic identity or gateway assignment is inferred.

The installed program initially emits LoRa TX/RX test messages and does not
complete a Meshtastic API handshake. A complete private flash backup succeeds
with esptool's transfer-digest check at 460800 baud after a first 921600-baud
attempt fails with truncated USB data. The failed attempt is not a usable
backup. Successful 16 MB read takes **384.2 seconds**.

### Owner-confirmed wiring

| Module connection | Heltec GPIO / supply |
| --- | --- |
| INA219 VCC / GND | 3V3 / GND |
| INA219 SDA / SCL | 17 / 18 |
| SD adapter 3v3 / GND | 3V3 / GND |
| SD CLK / MOSI / MISO / CS | 47 / 48 / 6 / 4 |

Matched against the manufacturer's [V4.2 schematic](https://resource.heltec.cn/download/WiFi_LoRa_32_V4/Schematic/WiFi_LoRa_32_V4.2.pdf)
and [V4.3 schematic](https://resource.heltec.cn/download/WiFi_LoRa_32_V4/Schematic/HTIT-WB32LAF_V4.3.pdf).
The diagnostic uses a separate SD SPI bus and the stated I2C pins; it does not
initialize the LoRa radio, Wi-Fi or Bluetooth. Sensor register units follow
the [TI INA219 datasheet](https://www.ti.com/lit/ds/symlink/ina219.pdf).

### Installed image and preservation

Installed **SNORR Peripheral Diagnostic v1**, from
[source and build instructions](../../scripts/bench/heltec-v4-peripherals/README.md).
This is standalone bench firmware, not Meshtastic or gateway logging firmware.
PlatformIO Espressif32 **6.13.0**, Arduino ESP32 **2.0.17**, esptool **4.11.0**.
Build passes: **19,324 bytes RAM**, **344,977 bytes program**;
generated binary **345,344 bytes**.

| Artifact | SHA256 |
| --- | --- |
| Original 16 MB flash | `1af5e2dc5b1de0d88b7e11f0458ae401f5288743f9d1101c85377f7c75559014` |
| Installed diagnostic binary | `b2febd332857116de81687978656bbff3bbb5b7017f0d22db6ad747aeb68ec41` |

Original partition table: NVS `0x9000/0x5000`, OTA data `0xe000/0x2000`,
app0 `0x10000/0x140000`, app1 `0x150000/0x140000`, SPIFFS
`0x290000/0x160000`, coredump `0x3f0000/0x10000`. OTA sequence 1 selects
app0; app1 is blank. Only **app0 at 0x10000** is written, and esptool verifies
the written-data hash. Existing bootloader, partition table, NVS, OTA data,
app1 and filesystem are not written. No full-chip erase or factory reset.

Private recovery/evidence directory:
`private/bench/v4-peripherals-20261112/`, containing the complete
`original-flash.bin`, extracted `original-app0.bin`, `backup-manifest.json`,
`api-probe.log`, `passive-serial.bin`, `backup-retry.log`, `build.log`,
`flash.log`, `diagnostic-serial.txt` and `diagnostic-summary.json`.
The built ELF/binary remain in `private/bench/v4-peripherals-build/`.
To recover the old application on this exact board, the original app0 image
can be written back at 0x10000 after reidentification and owner selection;
the complete backup also retains all original bytes. Recovery was not run.

### Measured results

| Check | Result |
| --- | --- |
| INA219 I2C | **PASS**, sole responder in 0x40-0x4f range at **0x40** |
| INA219 register/configuration | **PASS**, five register sets; test `0x399f` configuration readback and original `0x399f` restoration verified |
| INA219 bus voltage | **4.220-4.224 V** across the five samples |
| INA219 shunt voltage | **0.000-0.020 mV** in initial samples; subsequent health samples **-0.040-0.000 mV** |
| INA219 calibration | Register `0x0000`, no overflow; calibrated current not claimed |
| SD mount | **PASS**, SDHC, separate SPI at **1 MHz**, formatting disabled |
| Card-reported capacity | **31,914,983,424 bytes**, about **31.9 GB / 29.7 GiB** |
| Mounted filesystem | **31,902,400,512 bytes** total; **65,536 bytes** used before the diagnostic file |
| SD write/read | **PASS**, **16,384 bytes written and verified** after flush/close, unmount/remount and reopen |
| Test-file removal | **PASS**; random test path did not overwrite an existing file |
| Final startup verdict | `SUMMARY ina=PASS sd=PASS` |

Four subsequent health records through **22.3 seconds uptime** retain readable
INA bus/shunt registers. Serial closes at handoff; diagnostic remains installed.
The health field `sd_test_passed=1` retains the startup verdict and is not a
continuous card-health check.

### Limits and next step

The owner reports FAT32; successful filesystem mount/write/read is measured,
but FAT type and full physical capacity were not independently audited.
INA219-compatible register behavior passes; manufacturer authenticity, shunt
resistance, calibrated current, charge/discharge polarity and battery-path
accounting remain unverified. Nearly zero shunt voltage is not a diagnosis
of missing load or faulty wiring. No external meter comparison was performed.

No Meshtastic/private-network provisioning, GPS/time, RF/backhaul, portal,
full-card test, sustained logging, power-loss recovery or field acceptance is
claimed. The requested peripheral connectivity check is complete. Next useful
work is owner-selected gateway/recorder firmware and assignment; broader
[LOCAL-10 logging](../../.scratch/pilot/issues/29-gateway-sd-logging.md) remains
deferred beyond this separate bench check.
