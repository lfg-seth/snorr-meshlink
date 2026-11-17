import csv
import importlib.util
import io
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("site_survey", Path(__file__).parents[1] / "site-survey.py")
survey = importlib.util.module_from_spec(spec)
spec.loader.exec_module(survey)


class RecordedHandheld(survey.Handheld):
    def __init__(self, status="interrupted", counters=(8, 8)):
        self.status = status
        self.counters = iter(counters)

    def info(self):
        return {"counter": next(self.counters), "slots": 128}

    def request(self, command):
        replies = {
            "NEXT 0": f"NEXT 0 8 {self.status} 36 0",
            "ROW 0 0": f"ROW 8,{self.status},1,1,R004,!49ac6d7f,0,4501,timeout,,,,,",
            "ROW 0 1": f"ROW 8,{self.status},1,2,R007,!b456f760,4502,,unknown,,,,,",
            "ROW 0 2": "END",
            "NEXT 1": "END",
        }
        return replies[command]


class USBExportTests(unittest.TestCase):
    def test_interrupted_and_timeout_rows_are_distinct_and_repeatable(self):
        outputs = []
        for _ in range(2):
            stream = io.StringIO()
            self.assertEqual(RecordedHandheld().export(csv.writer(stream)), (1, 2))
            outputs.append(stream.getvalue())
        self.assertEqual(*outputs)
        rows = list(csv.DictReader(io.StringIO(outputs[0])))
        self.assertEqual([r["outcome"] for r in rows], ["timeout", "unknown"])
        self.assertTrue(all(all(r[k] == "" for k in survey.COLUMNS[9:]) for r in rows))

    def test_incomplete_complete_site_rejected(self):
        with self.assertRaisesRegex(ValueError, "missing attempts"):
            RecordedHandheld("complete").export(csv.writer(io.StringIO()))

    def test_changed_counter_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "counter changed"):
            RecordedHandheld(counters=(8, 9)).export(csv.writer(io.StringIO()))
