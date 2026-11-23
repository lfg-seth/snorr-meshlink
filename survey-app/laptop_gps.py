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
                self.fix_at = now
            self.epoch = epoch
            self.reading = reading

    def snapshot(self):
        age = None if self.fix_at is None else int(time.monotonic() * 1000) - self.fix_at
        valid = bool(
            self.port and self.reading.get("valid") and age is not None and age <= 3000
        )
        sample = self.reading | {
            "connected": self.port is not None, "valid": valid, "fix_age_ms": age,
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
