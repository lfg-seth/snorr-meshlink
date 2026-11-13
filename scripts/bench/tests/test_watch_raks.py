"""Read-only hot-plug identity checks; no real serial ports are opened."""
import importlib.util
import io
from pathlib import Path
from types import SimpleNamespace as NS
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("watch_raks", Path(__file__).parents[1] / "watch-raks.py")
watch = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(watch)


def port(usb="ABC", device="COM19", vid=0x239A, pid=0x8029):
    return NS(serial_number=usb, device=device, vid=vid, pid=pid)


def identity(p):
    return {"nodeId": "!12345678", "name": "R001", "role": "CLIENT", "port": p.device,
            "usbSerial": p.serial_number, "firmware": "2.7.26.test", "hardwareId": "01"}


class HotPlugTests(unittest.TestCase):
    def test_heltec_and_bootloader_are_not_opened(self):
        ports = [port(), port("V4", "COM31", 0x303A, 0x1001), port("BOOT", "COM20", pid=0x0029)]
        self.assertEqual(watch.candidates(ports, []), [ports[0]])

    def test_duplicate_or_missing_usb_is_never_guessed(self):
        self.assertEqual(watch.candidates([port(), port("abc", "COM20"), port(None)], []), [])

    def test_reference_exclusion_is_case_insensitive(self):
        self.assertEqual(watch.candidates([port("AbC")], ["abc"]), [])

    def test_each_new_port_prints_once_and_replug_refreshes(self):
        seen, output, opened = set(), [], []
        def probe(p):
            opened.append(p.device)
            return identity(p)
        watch.poll([port()], seen, [], probe, output.append)
        watch.poll([port()], seen, [], probe, output.append)
        self.assertEqual(opened, ["COM19"])
        watch.poll([], seen, [], probe, output.append)
        watch.poll([port(device="COM21")], seen, [], probe, output.append)
        self.assertEqual(opened, ["COM19", "COM21"])
        self.assertEqual(len(output), 2)
        self.assertTrue(output[0].startswith("!12345678"))

    def test_multiple_boards_map_by_usb_not_enumeration_order(self):
        seen, output = set(), []
        rows = watch.poll([port("B", "COM7"), port("A", "COM9")], seen, [], identity, output.append)
        self.assertEqual([(r["usbSerial"], r["port"]) for r in rows], [("B", "COM7"), ("A", "COM9")])

    def test_pause_stops_before_another_board_is_opened(self):
        opened = []
        def probe(p):
            opened.append(p.device)
            return identity(p)
        watch.poll([port(), port("B", "COM20")], set(), [], probe, lambda _: None, lambda: bool(opened))
        self.assertEqual(opened, ["COM19"])

    def test_error_body_never_reaches_console_and_board_is_retryable(self):
        seen, output = set(), []
        def broken(p):
            raise RuntimeError("secret password channel-key")
        watch.poll([port()], seen, [], broken, output.append)
        self.assertNotIn("secret", output[0])
        self.assertNotIn("password", output[0])
        self.assertFalse(seen)

    def test_terminal_controls_are_removed(self):
        self.assertEqual(watch.clean("R001\n\r\x1b\u202e"), "R001")


class IdentificationTests(unittest.TestCase):
    def make_interface(self, fail=False, model=9, node_id="!12345678"):
        role_enum = NS(values_by_number={0: NS(name="CLIENT")})
        value = NS(metadata=NS(hw_model=model, firmware_version="2.7.26.test", role=0,
                              DESCRIPTOR=NS(fields_by_name={"role": NS(enum_type=role_enum)})),
                   myInfo=NS(my_node_num=0x12345678, device_id=b"\x01"), closed=False)
        def connect():
            print("secret SDK material")
            if fail:
                raise RuntimeError("connection failed")
        value.connect = connect
        value.close = lambda: setattr(value, "closed", True)
        value.getMyNodeInfo = lambda: {"user": {"id": node_id, "shortName": "R001", "privateKey": "secret"}}
        return value

    def test_projected_identity_has_no_keys_and_port_is_closed(self):
        interface, log = self.make_interface(), io.StringIO()
        result = watch.identify(port(), log, factory=lambda **_: interface)
        self.assertTrue(interface.closed)
        self.assertEqual(result["nodeId"], "!12345678")
        self.assertEqual(result["role"], "CLIENT")
        self.assertNotIn("secret", str(result))
        self.assertIn("secret SDK material", log.getvalue())

    def test_connection_failure_still_closes_interface(self):
        interface = self.make_interface(fail=True)
        with self.assertRaises(RuntimeError):
            watch.identify(port(), io.StringIO(), factory=lambda **_: interface)
        self.assertTrue(interface.closed)

    def test_wrong_model_or_inconsistent_identity_is_rejected(self):
        for interface in (self.make_interface(model=99), self.make_interface(node_id="!abcdef01"),
                          self.make_interface(node_id="bad")):
            with self.subTest(interface=interface), self.assertRaises(ValueError):
                watch.identify(port(), io.StringIO(), factory=lambda **_: interface)
            self.assertTrue(interface.closed)

    def test_station_lock_is_exclusive_and_released(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "watch.lock"
            with watch.station_lease(path):
                with self.assertRaises(OSError):
                    with watch.station_lease(path):
                        self.fail("Concurrent watcher acquired the same station")
            with watch.station_lease(path):
                pass


if __name__ == "__main__":
    unittest.main()
