"""Regression for the real SDK auto-close race after a requested reboot."""
import importlib.util
import io
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock

SPEC = importlib.util.spec_from_file_location("rak_close", Path(__file__).parents[1] / "check-rak.py")
rak = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(rak)


class RebootCloseTests(unittest.TestCase):
    def test_sdk_already_closed_stream_after_reboot(self):
        interface = SimpleNamespace(stream=None, close=Mock(side_effect=AttributeError("NoneType has no flush")))
        radio = rak.Radio(SimpleNamespace(device="COM19"), io.StringIO())
        radio.interface = interface
        radio.close()
        self.assertIsNone(radio.interface)
        interface.close.assert_not_called()

    def test_real_close_errors_propagate_and_owner_is_released(self):
        interface = SimpleNamespace(stream=object(), close=Mock(side_effect=OSError("real failure")))
        radio = rak.Radio(SimpleNamespace(device="COM19"), io.StringIO())
        radio.interface = interface
        with self.assertRaises(OSError):
            radio.close()
        self.assertIsNone(radio.interface)


if __name__ == "__main__":
    unittest.main()
