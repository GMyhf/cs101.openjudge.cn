"""T-028 phase 2 must keep priority, generators, and evidence mechanically aligned."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import t028_phase2_round15 as round15  # noqa: E402


class T028Phase2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.candidates = json.loads((ROOT / "collab/t028-phase2-candidates.json").read_text())
        cls.manifest = json.loads((ROOT / "collab/t028-round15-manifest.json").read_text())
        cls.report = json.loads((ROOT / "collab/t028-round15-report.json").read_text())
        cls.platform = json.loads((ROOT / "collab/t028-round15-platform.json").read_text())
        cls.local = json.loads((ROOT / "collab/t028-round15-localjudge.json").read_text())

    def test_candidate_snapshot_and_round15_priority_are_complete(self):
        self.assertEqual(208, self.candidates["count"])
        self.assertEqual([15, 25], self.candidates["round_range"])
        self.assertEqual(list(range(1, 21)),
                         [row["priority"] for row in self.manifest["entries"]])
        self.assertEqual(round15.NUMBERS,
                         {int(row["local_number"]) for row in self.manifest["entries"]})

    def test_generators_satisfy_named_contracts_and_counterexamples_fail(self):
        self.assertEqual(len(round15.NUMBERS), len(set(round15.LABELS.values())))
        self.assertEqual(len(round15.NUMBERS), len(set(round15.INVALID.values())))
        for number in round15.NUMBERS:
            self.assertFalse(round15.valid(number, round15.INVALID[number]), number)
            for seed in range(1, 101):
                self.assertTrue(round15.valid(number, round15.generate(number, seed)),
                                (number, seed))

    def test_round15_report_platform_and_local_judge_are_green(self):
        self.assertEqual([], self.report["failed"])
        self.assertEqual(20, self.platform["accepted"])
        self.assertEqual([], self.platform["not_accepted"])
        self.assertEqual(20, self.local["accepted"])
        self.assertEqual([], self.local["not_accepted"])
        platform = {int(row["local_number"]): row for row in self.platform["results"]}
        for row in self.report["entries"]:
            number = int(row["local_number"])
            self.assertEqual("passed", row["status"])
            self.assertEqual("Accepted", row["platform_verdict"])
            self.assertEqual(platform[number]["solution_id"], row["submission_id"])
            self.assertEqual("passed", row["merged_judge"]["status"])
            self.assertEqual([], row["self_audit"]["failed"])


if __name__ == "__main__":
    unittest.main()
