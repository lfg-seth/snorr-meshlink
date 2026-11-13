# Heltec V4 INA219 / SD bench diagnostic

Standalone Arduino diagnostic for the owner-selected screenless **ESP32-S3R2
Heltec V4 (16 MB flash / 2 MB PSRAM)**. This is a bench application, not the
Meshtastic gateway or the deferred LOCAL-10 logging implementation. It holds
the LoRa radio in reset and does not initialize Wi-Fi/Bluetooth.

| Peripheral | GPIO |
| --- | --- |
| INA219 SDA / SCL | 17 / 18 |
| SD SCK / MOSI / MISO / CS | 47 / 48 / 6 / 4 |

Owner connects both modules to 3V3 and GND. Do not apply this target to another
board/variant without checking its wiring. The installed toolchain is pinned to
PlatformIO Espressif32 6.13.0 / Arduino ESP32 2.0.17; only built-in libraries are
used. Build from the repository root:

```powershell
& "$env:USERPROFILE/.platformio/penv/Scripts/python.exe" -m platformio run --project-dir scripts/bench/heltec-v4-peripherals
```

Output goes to ignored `private/bench/v4-peripherals-build/`. Build success does
not establish hardware operation. Before flashing, identify the USB/chip and
privately back up and verify its existing flash. Inspect its partition table;
write only the selected application slot when compatible. Do not run a factory
erase or overwrite another board. Flashing is a separate owner-authorized step.

The diagnostic scans only the INA219 address range, requires one responder,
tests configuration write/readback, reads five bus/shunt/calibration register
sets, then restores and verifies the original configuration. INA219 has no
unique device-ID register: this establishes INA219-compatible behavior, not
manufacturer authenticity. Current calibration and charge/discharge polarity
are deliberately unclaimed without verified shunt and power-path information.

The card mounts at 1 MHz with formatting disabled. A new randomly named root
file receives a deterministic 16 KB pattern; the program flushes/closes it,
unmounts/remounts, reopens it and compares every byte before removing that file.
Existing files are not opened or listed. A failed operation can leave the
diagnostic file on the card; it is named in the remount-failure output. One
short comparison does not validate full capacity, endurance, power-loss
recovery or sustained logging. The reported card capacity is controller-reported.

The serial output is 115200 baud, including `INA_RESULT`, `SD_RESULT`,
`SUMMARY`, then five-second health lines. `sd_test_passed` retains the startup
test verdict; it is not continuous card polling. The test runs once per boot.

Primary references: Heltec [V4.2 schematic](https://resource.heltec.cn/download/WiFi_LoRa_32_V4/Schematic/WiFi_LoRa_32_V4.2.pdf),
[V4.3 schematic](https://resource.heltec.cn/download/WiFi_LoRa_32_V4/Schematic/HTIT-WB32LAF_V4.3.pdf),
and TI [INA219 register specification](https://www.ti.com/lit/ds/symlink/ina219.pdf).
