import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))
spec = importlib.util.spec_from_file_location("verifier", Path(__file__).with_name("verify.py"))
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class RegisteredInfrastructure(unittest.TestCase):
    def test_additional_gateway_is_required_from_the_verified_worker_config(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            mqtt, repeaters = root / "mqtt.json", root / "repeaters.json"
            mqtt.write_text(
                json.dumps(
                    dict(
                        gateways={"!1": "g001", "!2": "g002", "!3": "g003"},
                        infrastructure={"!4": "r006", "!1": "g001"},
                    )
                )
            )
            repeaters.write_text(json.dumps({"devices": [{"key": "r001"}, {"key": "r006"}]}))
            self.assertEqual(
                verifier.expected_infrastructure(mqtt, repeaters),
                {"g001", "g002", "g003", "r001", "r006"},
            )
            mqtt.write_text(json.dumps({"gateways": {"!1": "g001"}}))
            self.assertEqual(verifier.expected_infrastructure(mqtt, root / "absent"), {"g001"})

    def test_missing_gateway_configuration_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            mqtt = root / "mqtt.json"
            mqtt.write_text("{}")
            with self.assertRaises(RuntimeError):
                verifier.expected_infrastructure(mqtt, root / "absent")


if __name__ == "__main__":
    unittest.main()
