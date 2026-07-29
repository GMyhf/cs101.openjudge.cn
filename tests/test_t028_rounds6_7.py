import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import t028_rounds6_7


class T028RoundsSixSevenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifests = [json.loads((ROOT / "collab" / f"t028-round{r}-manifest.json").read_text()) for r in (6, 7)]
        cls.reports = [json.loads((ROOT / "collab" / f"t028-round{r}-report.json").read_text()) for r in (6, 7)]
        cls.platform = [json.loads((ROOT / "collab" / f"t028-round{r}-platform.json").read_text()) for r in (6, 7)]
        cls.local = [json.loads((ROOT / "collab" / f"t028-round{r}-localjudge.json").read_text()) for r in (6, 7)]

    def test_priority_ranges_and_global_identity(self):
        self.assertEqual([x["priority"] for x in self.manifests[0]["entries"]], list(range(81, 101)))
        self.assertEqual([x["priority"] for x in self.manifests[1]["entries"]], list(range(101, 121)))
        rows = sum((x["entries"] for x in self.manifests), [])
        self.assertEqual(len({x["global_number"] for x in rows}), 40)
        self.assertTrue(all(x["submit_group"] == "practice" for x in rows))

    def test_problem_specific_constraints_and_counterexamples(self):
        rows = sum((x["entries"] for x in self.manifests), [])
        labels = [t028_rounds6_7.LABELS[x["local_number"]] for x in rows]
        counterexamples = [t028_rounds6_7.INVALID[x["local_number"]] for x in rows]
        self.assertEqual(len(set(labels)), 40)
        self.assertEqual(len(set(counterexamples)), 40)
        for row in rows:
            number = row["local_number"]
            for seed in range(100):
                self.assertTrue(t028_rounds6_7.valid(number, t028_rounds6_7.generate(number, seed)), (number, seed))
            self.assertFalse(t028_rounds6_7.valid(number, t028_rounds6_7.INVALID[number]), number)

    def test_source_selection_follows_human_then_platform_rule(self):
        rows = sum((x["entries"] for x in self.manifests), [])
        for row in rows:
            source = (ROOT / "data" / "openjudge" / row["made_dir"] / "samplecode.py").read_text()
            if row["local_number"] in t028_rounds6_7.PLATFORM_SOURCES:
                self.assertIn("# Accepted submission:", source)
                self.assertIn("# External reference: statistics page", source)
            else:
                self.assertIn("# Source collection:", source)
                self.assertIn("# Fenced code block index:", source)

    def test_reports_platform_and_local_judge_are_green(self):
        for report, platform, local in zip(self.reports, self.platform, self.local):
            self.assertEqual(report["failed"], [])
            self.assertEqual(platform["accepted"], 20)
            self.assertEqual(local["accepted"], 20)
            self.assertTrue(all(x["status"] == "passed" and x["platform_verdict"] == "Accepted"
                                and x["merged_judge"]["verdict"] == "Accepted"
                                and x["archive_cross_check"]["status"] == "passed"
                                for x in report["entries"]))

    def test_truck_history_excludes_only_the_mislabeled_archive(self):
        row = next(x for x in self.reports[1]["entries"] if x["local_number"] == 1789)
        self.assertEqual(row["archive_cross_check"]["cases"], 1)
        self.assertEqual(len(row["archive_cross_check"]["excluded"]), 1)
        self.assertIn("unrelated German encoding archive", row["archive_cross_check"]["excluded"][0])


if __name__ == "__main__":
    unittest.main()
