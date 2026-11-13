#include <Arduino.h>
#include <SD.h>
#include <SPI.h>
#include <Wire.h>

constexpr uint8_t SDA_PIN = 17, SCL_PIN = 18;
constexpr uint8_t SD_CLK = 47, SD_MOSI = 48, SD_MISO = 6, SD_CS = 4;
constexpr size_t TEST_BYTES = 16384;
SPIClass cardSPI(FSPI);
uint8_t inaAddress = 0;
bool sdPassed = false;

bool readRegister(uint8_t address, uint8_t reg, uint16_t &value)
{
    Wire.beginTransmission(address);
    Wire.write(reg);
    if (Wire.endTransmission(false) || Wire.requestFrom(address, uint8_t(2)) != 2)
        return false;
    uint8_t high = Wire.read();
    uint8_t low = Wire.read();
    value = (uint16_t(high) << 8) | low;
    return true;
}

bool writeRegister(uint8_t address, uint8_t reg, uint16_t value)
{
    Wire.beginTransmission(address);
    Wire.write(reg);
    Wire.write(value >> 8);
    Wire.write(value & 0xff);
    return Wire.endTransmission() == 0;
}

bool checkINA()
{
    unsigned count = 0;
    for (uint8_t address = 0x40; address <= 0x4f; ++address) {
        Wire.beginTransmission(address);
        if (Wire.endTransmission() == 0) {
            Serial.printf("I2C_ACK address=0x%02x\n", address);
            inaAddress = address;
            ++count;
        }
    }
    if (count != 1) {
        Serial.printf("INA_FAIL expected_one_candidate found=%u\n", count);
        inaAddress = 0;
        return false;
    }
    uint16_t original = 0, actual = 0;
    if (!readRegister(inaAddress, 0, original))
        return false;
    // Exercise writable configuration without guessing the fitted shunt value.
    bool passed = writeRegister(inaAddress, 0, 0x399f) && readRegister(inaAddress, 0, actual) && actual == 0x399f;
    delay(100);
    for (unsigned i = 0; i < 5; ++i) {
        uint16_t bus = 0, shunt = 0, calibration = 0;
        bool ok = readRegister(inaAddress, 2, bus) && readRegister(inaAddress, 1, shunt) &&
                  readRegister(inaAddress, 5, calibration);
        passed &= ok;
        Serial.printf("INA_SAMPLE n=%u ok=%u bus_V=%.3f shunt_mV=%.3f config=0x%04x calibration=0x%04x overflow=%u\n",
                      i + 1, ok, (bus >> 3) * 0.004, int16_t(shunt) * 0.01, actual, calibration, bus & 1);
        delay(100);
    }
    bool restored = writeRegister(inaAddress, 0, original) && readRegister(inaAddress, 0, actual) && actual == original;
    passed &= restored;
    Serial.printf("INA_RESULT pass=%u address=0x%02x original_config=0x%04x restored=%u current_calibrated=0\n",
                  passed, inaAddress, original, restored);
    return passed;
}

uint8_t pattern(size_t offset)
{
    return uint8_t((offset * 37U) ^ (offset >> 3U) ^ 0xa5U);
}

bool checkSD()
{
    cardSPI.begin(SD_CLK, SD_MISO, SD_MOSI, SD_CS);
    if (!SD.begin(SD_CS, cardSPI, 1000000, "/sd", 5, false)) {
        Serial.println("SD_FAIL mount_at_1MHz format_attempted=0");
        return false;
    }
    Serial.printf("SD_MOUNT type=%u card_bytes=%llu filesystem_bytes=%llu used_bytes=%llu spi_hz=1000000\n",
                  SD.cardType(), SD.cardSize(), SD.totalBytes(), SD.usedBytes());
    char name[48];
    bool unique = false;
    for (unsigned n = 0; n < 100; ++n) {
        snprintf(name, sizeof(name), "/snorr-test-%08lx.bin", (unsigned long)esp_random());
        if (!SD.exists(name)) {
            unique = true;
            break;
        }
    }
    if (!unique)
        return false;
    File file = SD.open(name, FILE_WRITE);
    if (!file) {
        Serial.println("SD_FAIL create_test_file");
        return false;
    }
    bool passed = true;
    uint8_t block[512];
    size_t written = 0;
    for (size_t offset = 0; offset < TEST_BYTES; offset += sizeof(block)) {
        for (size_t i = 0; i < sizeof(block); ++i)
            block[i] = pattern(offset + i);
        size_t result = file.write(block, sizeof(block));
        written += result;
        if (result != sizeof(block)) {
            passed = false;
            break;
        }
    }
    file.flush();
    file.close();
    SD.end();
    bool remounted = SD.begin(SD_CS, cardSPI, 1000000, "/sd", 5, false);
    if (!remounted) {
        Serial.printf("SD_FAIL remount test_file=%s\n", name);
        return false;
    }
    file = SD.open(name, FILE_READ);
    size_t verified = 0;
    if (!file || file.size() != TEST_BYTES) {
        passed = false;
    } else {
        for (size_t offset = 0; offset < TEST_BYTES; offset += sizeof(block)) {
            int count = file.read(block, sizeof(block));
            if (count != int(sizeof(block))) {
                passed = false;
                break;
            }
            for (size_t i = 0; i < sizeof(block); ++i) {
                if (block[i] != pattern(offset + i))
                    passed = false;
                else
                    ++verified;
            }
        }
    }
    if (file)
        file.close();
    bool removed = SD.remove(name);
    passed &= written == TEST_BYTES && verified == TEST_BYTES && removed;
    Serial.printf("SD_RESULT pass=%u written=%u verified=%u remounted=%u test_file_removed=%u\n",
                  passed, unsigned(written), unsigned(verified), remounted, removed);
    return passed;
}

void setup()
{
    // Keep the radio in reset; this diagnostic does not initialize radio or Wi-Fi.
    digitalWrite(12, LOW);
    pinMode(12, OUTPUT);
    Serial.begin(115200);
    unsigned long started = millis();
    while (!Serial && millis() - started < 10000)
        delay(10);
    delay(1000);
    Serial.printf("SNORR_PERIPHERAL_DIAGNOSTIC v1 chip=%s flash_bytes=%u\n", ESP.getChipModel(), ESP.getFlashChipSize());
    Serial.println("PINS ina_sda=17 ina_scl=18 sd_sck=47 sd_mosi=48 sd_miso=6 sd_cs=4");
    Wire.begin(SDA_PIN, SCL_PIN, 100000);
    Wire.setTimeOut(100);
    bool inaPassed = checkINA();
    sdPassed = checkSD();
    Serial.printf("SUMMARY ina=%s sd=%s\n", inaPassed ? "PASS" : "FAIL", sdPassed ? "PASS" : "FAIL");
}

void loop()
{
    delay(5000);
    uint16_t bus = 0, shunt = 0;
    bool readable = inaAddress && readRegister(inaAddress, 2, bus) && readRegister(inaAddress, 1, shunt);
    Serial.printf("HEALTH uptime_ms=%lu ina_readable=%u bus_V=%.3f shunt_mV=%.3f sd_test_passed=%u\n",
                  millis(), readable, (bus >> 3) * 0.004, int16_t(shunt) * 0.01, sdPassed);
}
