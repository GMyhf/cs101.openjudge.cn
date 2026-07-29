import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import t028_rounds11_14


class T028RoundsElevenToFourteenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rounds = range(11, 15)
        cls.manifests = {
            number: json.loads((ROOT / "collab" / f"t028-round{number}-manifest.json").read_text())
            for number in cls.rounds
        }
        cls.reports = {
            number: json.loads((ROOT / "collab" / f"t028-round{number}-report.json").read_text())
            for number in cls.rounds
        }

    def test_priority_ranges_are_complete_with_explicit_exclusions(self):
        ranges = {11: range(181, 201), 12: range(201, 221),
                  13: range(221, 241), 14: range(241, 253)}
        for number, expected in ranges.items():
            manifest = self.manifests[number]
            priorities = [row["priority"] for row in manifest["entries"]]
            priorities += [row["priority"] for row in manifest["selection_exclusions"]]
            self.assertEqual(sorted(priorities), list(expected))
        self.assertEqual([self.manifests[number]["count"] for number in self.rounds], [20, 19, 20, 7])

    def test_generators_and_counterexamples(self):
        labels = []
        counterexamples = []
        for manifest in self.manifests.values():
            for row in manifest["entries"]:
                number = row["local_number"]
                labels.append(t028_rounds11_14.LABELS[number])
                counterexamples.append(t028_rounds11_14.INVALID[number])
                for seed in range(1, 101):
                    self.assertTrue(t028_rounds11_14.valid(
                        number, t028_rounds11_14.generate(number, seed)), (number, seed))
                self.assertFalse(t028_rounds11_14.valid(number, t028_rounds11_14.INVALID[number]), number)
        self.assertEqual(len(labels), len(set(labels)))
        self.assertEqual(len(counterexamples), len(set(counterexamples)))

    def test_reports_platform_and_merged_judge_are_green(self):
        for number in self.rounds:
            report = self.reports[number]
            platform = json.loads((ROOT / "collab" / f"t028-round{number}-platform.json").read_text())
            local = json.loads((ROOT / "collab" / f"t028-round{number}-localjudge.json").read_text())
            self.assertEqual(platform["accepted"], platform["total"])
            self.assertEqual(local["accepted"], local["total"])
            self.assertEqual(report["failed"], [])
            for row in report["entries"]:
                self.assertEqual(row["status"], "passed")
                self.assertEqual(row["platform_verdict"], "Accepted")
                self.assertEqual(row["archive_cross_check"]["status"], "passed")
                self.assertEqual(row["merged_judge"]["verdict"], "Accepted")

    def test_special_judge_and_identity_exclusions_stay_recorded(self):
        exclusions = {
            row["priority"]: row
            for manifest in self.manifests.values()
            for row in manifest["selection_exclusions"]
        }
        self.assertEqual(set(exclusions), {218, 246, 248, 249, 250, 252})
        self.assertEqual(exclusions[218]["status"], "requires-special-judge")
        self.assertEqual(exclusions[248]["status"], "requires-special-judge")
        for priority in (246, 249, 250, 252):
            self.assertEqual(exclusions[priority]["status"], "retired-by-global-identity")


if __name__ == "__main__":
    unittest.main()
