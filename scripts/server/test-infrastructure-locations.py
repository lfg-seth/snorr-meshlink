import copy
import importlib.util
from pathlib import Path
import random
import unittest

spec = importlib.util.spec_from_file_location(
    "locations", Path(__file__).with_name("infrastructure-locations.py")
)
locations = importlib.util.module_from_spec(spec)
spec.loader.exec_module(locations)


class LocationPolicy(unittest.TestCase):
    def test_only_missing_infrastructure_gets_a_stable_labelled_point(self):
        for kind in ("repeater", "backhaul"):
            original = dict(
                key="node",
                kind=kind,
                number="G003",
                configuration=dict(
                    name="G003",
                    downlink=False,
                    deploymentStatus="bench",
                    batterySetup="Unknown",
                    firmware="verified",
                ),
            )
            before = copy.deepcopy(original)
            result = locations.place_missing(original, random.Random(16))
            self.assertEqual(original, before)
            config = result["configuration"]
            for field, bounds in locations.BOUNDS.items():
                self.assertTrue(bounds[0] <= config[field] <= bounds[1])
            self.assertEqual(config["locationSource"], locations.SOURCE)
            self.assertIn("Random Las Vegas", config["name"])
            self.assertIn("not a measured location", config["locationLabel"])
            for field in ("downlink", "deploymentStatus", "batterySetup", "firmware"):
                self.assertEqual(config[field], before["configuration"][field])
            self.assertEqual(locations.place_missing(result), result)

    def test_existing_and_member_locations_are_preserved(self):
        for kind, config in [
            ("member", {}),
            ("member", {"latitude": 1}),
            ("repeater", {"latitude": 0, "longitude": 0}),
            ("backhaul", {"latitude": 36.1, "longitude": -115.2}),
        ]:
            original = dict(key="node", kind=kind, configuration=config)
            self.assertEqual(locations.place_missing(original), original)

    def test_invalid_or_incomplete_pairs_are_replaced_together(self):
        for value in (None, True, "36.1", float("nan"), 91):
            original = dict(
                key="node", kind="repeater", configuration={"latitude": value, "longitude": -115}
            )
            result = locations.place_missing(original, random.Random(24))
            self.assertTrue(locations.has_location(result["configuration"]))
            self.assertNotEqual(result["configuration"]["longitude"], -115)


if __name__ == "__main__":
    unittest.main()
