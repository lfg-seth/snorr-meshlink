import unittest
from datetime import datetime, timezone
from unittest.mock import Mock, patch

from laptop_gps import LaptopGPS, parse_gga


def sentence(body):
    check = 0
    for value in body:
        check ^= value
    return b"$" + body + f"*{check:02X}\r\n".encode("ascii")


FIX = b"GNGGA,180102.00,3615.00000,N,11539.00000,W,1,12,1.10,2300.5,M,0.0,M,,"
NO_FIX = b"GNGGA,180103.00,,,,,0,00,99.99,,,,,,"


class LaptopGpsTests(unittest.TestCase):
    def test_gga_checksum_and_optional_fix_statistics(self):
        epoch, fix = parse_gga(sentence(FIX))
        self.assertEqual(epoch, "180102.00")
        self.assertTrue(fix["valid"])
        self.assertEqual((fix["lat_deg"], fix["lon_deg"]), (36.25, -115.65))
        self.assertEqual((fix["satellites"], fix["hdop"], fix["altitude_m"]), (12, 1.1, 2300.5))
        self.assertIsNone(parse_gga(sentence(FIX).replace(b"2300.5", b"3300.5")))
        self.assertFalse(parse_gga(sentence(NO_FIX))[1]["valid"])

    def test_repeated_epoch_does_not_refresh_and_no_fix_clears_position(self):
        gps = LaptopGPS("unused")
        gps.port = Mock()
        line = sentence(FIX)
        gps.port.read.side_effect = [line[:30], line[30:], line, sentence(NO_FIX)]
        gps.poll(900)
        with patch('laptop_gps.time.time_ns', return_value=0):
            gps.poll(1000)
        with patch("laptop_gps.time.monotonic", return_value=1.3):
            self.assertTrue(gps.snapshot()["valid"])
            self.assertEqual(gps.snapshot()["fix_age_ms"], 300)
        gps.poll(4001)
        with patch("laptop_gps.time.monotonic", return_value=4.001):
            self.assertFalse(gps.snapshot()["valid"])
            self.assertIsNone(gps.snapshot()["lat_deg"])
        gps.poll(4200)
        self.assertFalse(gps.reading["valid"])

    def test_buffered_time_and_midnight_rollover(self):
        gps = LaptopGPS("unused")
        gps.port = Mock()
        delayed = FIX.replace(b"180102.00", b"235959.750")
        old = FIX.replace(b"180102.00", b"235955.000")
        gps.port.read.side_effect = [sentence(delayed), sentence(old)]
        midnight = int(datetime(2026, 11, 24, tzinfo=timezone.utc).timestamp() * 1000)
        with patch("laptop_gps.time.time_ns", return_value=(midnight + 250) * 1_000_000):
            gps.poll(4000)
            self.assertEqual(gps.snapshot(4000)["fix_utc_ms"], midnight - 250)
            self.assertEqual(gps.snapshot(4000)["fix_age_ms"], 500)
            gps.poll(4010)
            self.assertIsNone(gps.snapshot(4010)["fix_utc_ms"])
