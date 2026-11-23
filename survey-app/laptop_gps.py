"""Read the laptop's USB GNSS without sending receiver commands."""

import math
import re
import time


def coordinate(value, hemisphere, positive, negative, limit):
    degrees, minutes = divmod(float(value), 100)
    result = degrees + minutes / 60
    if not 0 <= minutes < 60 or not 0 <= result <= limit:
        raise ValueError("Invalid NMEA coordinate")
    if hemisphere == negative:
        return -result
    if hemisphere == positive:
        return result
    raise ValueError("Invalid NMEA hemisphere")


def optional_number(value):
    try:
        number = float(value)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


GPS_MAX_AGE_MS = 3000
DAY_MS = 86_400_000


def gga_utc_ms(epoch, wall_ms):
    """Resolve GGA's time of day against the laptop clock, including midnight rollover."""
    whole, _, fraction = epoch.partition(".")
    hour, minute, second = int(whole[:2]), int(whole[2:4]), int(whole[4:6])
    if hour > 23 or minute > 59 or second > 59:
        return None
    time_of_day = (hour * 3600 + minute * 60 + second) * 1000 + int(fraction[:3].ljust(3, "0"))
    age = (wall_ms - time_of_day + DAY_MS // 2) % DAY_MS - DAY_MS // 2
    if -1000 <= age <= GPS_MAX_AGE_MS:
        return wall_ms - age
    return None


def parse_gga(line):
    body, marker, checksum = line.strip().partition(b"*")
    if not marker or len(checksum) != 2 or not re.match(rb"\$[A-Z]{2}GGA,", body):
        return None
    actual = 0
    for byte in body[1:]:
        actual ^= byte
    try:
        if actual != int(checksum, 16):
            return None
        fields = body.decode("ascii").split(",")
        epoch = fields[1]
        quality = int(fields[6] or "0")
        satellites = int(fields[7]) if fields[7] else None
        valid = quality in (1, 2, 4, 5) and bool(
            re.fullmatch(r"[0-9]{6}(?:\.[0-9]+)?", epoch)
        )
        return epoch, {
            "valid": valid,
            "quality": quality,
            "satellites": satellites,
            "hdop": optional_number(fields[8]) if valid else None,
            "altitude_m": optional_number(fields[9]) if valid and fields[10] == "M" else None,
            "lat_deg": coordinate(fields[2], fields[3], "N", "S", 90) if valid else None,
            "lon_deg": coordinate(fields[4], fields[5], "E", "W", 180) if valid else None,
        }
    except (ValueError, IndexError):
        return None


class LaptopGPS:
    def __init__(self, device):
        self.device = device
        self.port = None
        self.buffer = b""
        self.epoch = None
        self.reading = {}
        self.fix_at = None
        self.fix_utc_ms = None
        self.next_open = 0

    def poll(self, now):
        if self.port is None:
            if now < self.next_open:
                return
            self.next_open = now + 3000
            from serial import Serial

            try:
                self.port = Serial(str(self.device), 9600, timeout=0, exclusive=True)
            except OSError:
                return
            self.epoch = None
            self.fix_at = self.fix_utc_ms = None
            self.buffer = b""
        try:
            chunk = self.port.read(4096)
        except OSError:
            self.close()
            return
        lines = (self.buffer + chunk).split(b"\n")
        self.buffer = lines.pop()[-256:]
        for line in lines:
            sample = parse_gga(line)
            if sample is None:
                continue
            epoch, reading = sample
            if reading["valid"] and epoch != self.epoch:
                wall_ms = time.time_ns() // 1_000_000
                self.fix_utc_ms = gga_utc_ms(epoch, wall_ms)
                age = wall_ms - self.fix_utc_ms if self.fix_utc_ms is not None else 0
                self.fix_at = now - max(0, age)
            self.epoch = epoch
            self.reading = reading

    def snapshot(self, now=None):
        if now is None:
            now = int(time.monotonic() * 1000)
        age = None if self.fix_at is None else now - self.fix_at
        valid = bool(
            self.port and self.reading.get("valid") and age is not None and age <= GPS_MAX_AGE_MS
        )
        sample = self.reading | {
            "connected": self.port is not None, "valid": valid, "fix_age_ms": age,
            "fix_utc_ms": self.fix_utc_ms if valid else None,
        }
        if not valid:
            sample.update(lat_deg=None, lon_deg=None, altitude_m=None, hdop=None, satellites=None)
        return sample

    def close(self):
        port, self.port = self.port, None
        self.reading = {}
        if port is not None:
            try:
                port.close()
            except OSError:
                pass
