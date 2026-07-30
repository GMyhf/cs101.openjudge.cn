"""T-028 phase 2 must keep priority, generators, and evidence mechanically aligned."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import t028_phase2_round15 as round15  # noqa: E402
import t028_phase2_round16 as round16  # noqa: E402
import t028_phase2_round17 as round17  # noqa: E402
import t028_phase2_round18 as round18  # noqa: E402
import t028_phase2_round19 as round19  # noqa: E402

ROUNDS = ((15, round15), (16, round16), (17, round17), (18, round18),
          (19, round19))


class T028Phase2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.candidates = json.loads((ROOT / "collab/t028-phase2-candidates.json").read_text())
        cls.manifests = {number: json.loads((ROOT / f"collab/t028-round{number}-manifest.json").read_text()) for number, _ in ROUNDS}
        cls.reports = {number: json.loads((ROOT / f"collab/t028-round{number}-report.json").read_text()) for number, _ in ROUNDS}
        cls.platforms = {number: json.loads((ROOT / f"collab/t028-round{number}-platform.json").read_text()) for number, _ in ROUNDS}
        cls.locals = {number: json.loads((ROOT / f"collab/t028-round{number}-localjudge.json").read_text()) for number, _ in ROUNDS}

    def test_candidate_snapshot_and_round15_priority_are_complete(self):
        self.assertEqual(208, self.candidates["count"])
        self.assertEqual([15, 25], self.candidates["round_range"])
        for number, module in ROUNDS:
            start = (number - 15) * 20 + 1
            self.assertEqual(list(range(start, start + 20)),
                             [row["priority"] for row in self.manifests[number]["entries"]])
            self.assertEqual(module.NUMBERS,
                             {int(row["local_number"]) for row in self.manifests[number]["entries"]})

    def test_generators_satisfy_named_contracts_and_counterexamples_fail(self):
        for _, module in ROUNDS:
            self.assertEqual(len(module.NUMBERS), len(set(module.LABELS.values())))
            self.assertEqual(len(module.NUMBERS), len(set(module.INVALID.values())))
            for number in module.NUMBERS:
                self.assertFalse(module.valid(number, module.INVALID[number]), number)
                for seed in range(1, 101):
                    self.assertTrue(module.valid(number, module.generate(number, seed)),
                                    (number, seed))

    def test_round15_report_platform_and_local_judge_are_green(self):
        for round_number, _ in ROUNDS:
            report, platform, local = self.reports[round_number], self.platforms[round_number], self.locals[round_number]
            self.assertEqual([], report["failed"])
            self.assertEqual(20, platform["accepted"])
            self.assertEqual([], platform["not_accepted"])
            self.assertEqual(20, local["accepted"])
            self.assertEqual([], local["not_accepted"])
            by_number = {int(row["local_number"]): row for row in platform["results"]}
            for row in report["entries"]:
                number = int(row["local_number"])
                self.assertEqual("passed", row["status"])
                self.assertEqual("Accepted", row["platform_verdict"])
                self.assertEqual(by_number[number]["solution_id"], row["submission_id"])
                self.assertEqual("passed", row["merged_judge"]["status"])
                self.assertEqual([], row["self_audit"]["failed"])


if __name__ == "__main__":
    unittest.main()
