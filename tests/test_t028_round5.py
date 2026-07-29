import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import t028_round5


class T028Round5Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT / "collab" / "t028-round5-manifest.json").read_text())
        cls.report = json.loads((ROOT / "collab" / "t028-round5-report.json").read_text())
        cls.platform = json.loads((ROOT / "collab" / "t028-round5-platform.json").read_text())
        cls.local = json.loads((ROOT / "collab" / "t028-round5-localjudge.json").read_text())

    def test_priority_range_and_global_identity_are_recorded(self):
        entries = self.manifest["entries"]
        self.assertEqual([row["priority"] for row in entries], list(range(61, 81)))
        self.assertEqual(len({row["global_number"] for row in entries}), 20)
        self.assertTrue(all(row["submit_group"] == "practice" for row in entries))

    def test_generators_obey_their_problem_specific_predicates(self):
        for row in self.manifest["entries"]:
            number = row["local_number"]
            for seed in range(200):
                self.assertTrue(t028_round5.valid(number, t028_round5.generate(number, seed)),
                                (number, seed))
            self.assertFalse(t028_round5.valid(number, t028_round5.INVALID[number]), number)

    def test_reference_sources_are_the_human_solution_collection(self):
        for row in self.manifest["entries"]:
            made = ROOT / "data" / "openjudge" / row["made_dir"]
            source = (made / "samplecode.py").read_text(encoding="utf-8")
            self.assertIn("# Source collection:", source)
            self.assertIn("# Fenced code block index: 2", source)

    def test_reports_and_real_verdicts_are_all_green(self):
        self.assertEqual(self.report["failed"], [])
        self.assertTrue(all(row["status"] == "passed" for row in self.report["entries"]))
        self.assertTrue(all(row["archive_cross_check"]["status"] == "passed"
                            for row in self.report["entries"]))
        self.assertEqual(self.platform["accepted"], 20)
        self.assertEqual(self.local["accepted"], 20)
        self.assertTrue(all(row["platform_verdict"] == "Accepted" and
                            row["merged_judge"]["verdict"] == "Accepted"
                            for row in self.report["entries"]))


if __name__ == "__main__":
    unittest.main()
