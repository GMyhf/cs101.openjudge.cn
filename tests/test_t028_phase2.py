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
import t028_phase2_round20 as round20  # noqa: E402
import t028_phase2_round21 as round21  # noqa: E402
import t028_phase2_round22 as round22  # noqa: E402
import t028_phase2_round23 as round23  # noqa: E402

ROUNDS = ((15, round15), (16, round16), (17, round17), (18, round18),
          (19, round19), (20, round20), (21, round21), (22, round22),
          (23, round23))


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

    def test_reviewed_statement_bounds_stay_enforced(self):
        reviewed = {
            21458: round15,
            27625: round16,
            4100: round18,
            18106: round18,
            18159: round18,
            27122: round19,
            4044: round19,
        }
        for number, module in reviewed.items():
            for seed in range(2000):
                self.assertTrue(module.valid(number, module.generate(number, seed)),
                                (number, seed))
            round_number = next(r for r, candidate in ROUNDS if candidate is module)
            row = next(entry for entry in self.reports[round_number]["entries"]
                       if entry["local_number"] == number)
            self.assertEqual(module.INPUT_DOMAINS[number],
                             row["input_domain"]["statement_quote"])

    def test_reviewed_validator_holes_are_closed(self):
        bad_cases = {
            (round16, 27653): "1 x 2 3\n",
            (round16, 27103): "3 2\n1 2 1\nextra\n",
            (round16, 26978): "3 2\n1 2 3\nextra\n",
            (round16, 26971): "3\n1 2 3\nextra\n",
            (round16, 27104): "3\n1 2 3\nextra\n",
            (round16, 18146): "2 2\n1 2\nextra\n",
            (round19, 18155): "target\n1 2 3\n",
        }
        for (module, number), case in bad_cases.items():
            self.assertFalse(module.valid(number, case), number)

    def test_round19_exercises_ungrouped_queue_members(self):
        for seed in range(1, 101):
            lines = round19.generate(27925, seed).splitlines()
            group_count = int(lines[0])
            members = {int(value) for row in lines[1:1 + group_count]
                       for value in row.split()}
            enqueued = [int(row.split()[1]) for row in lines[1 + group_count:]
                        if row.startswith("ENQUEUE ")]
            self.assertTrue(any(value not in members for value in enqueued), seed)

    def test_28050_provenance_matches_project_authored_reference(self):
        row = next(entry for entry in self.reports[16]["entries"]
                   if entry["local_number"] == 28050)
        self.assertIn("project-authored", row["reference_source"])
        self.assertEqual("project-authored for this repository", row["license_status"])

    def test_round20_input_domains_and_project_reference_are_recorded(self):
        for row in self.reports[20]["entries"]:
            number = row["local_number"]
            self.assertEqual(round20.INPUT_DOMAINS[number],
                             row["input_domain"]["statement_quote"])
            self.assertIn("generated_extremes", row["input_domain"])
        h_index = next(row for row in self.reports[20]["entries"]
                       if row["local_number"] == 18105)
        self.assertEqual("53015094", h_index["submission_id"])
        self.assertIn("project-authored", h_index["reference_source"])

    def test_round22_filters_only_invalid_30172_archive_inputs(self):
        row = next(entry for entry in self.reports[22]["entries"]
                   if entry["local_number"] == 30172)
        cross = row["archive_cross_check"]
        self.assertEqual(13, cross["cases"])
        self.assertEqual([f"tests/30000-/30172/{index}.in" for index in range(13, 20)],
                         cross["excluded_invalid_inputs"])
        archive = ROOT / "data/openjudge/tests/30000-/30172"
        for relative in cross["excluded_invalid_inputs"]:
            self.assertFalse(round22.valid(30172, (archive / Path(relative).name).read_text()))

    def test_round23_keeps_valid_27631_oracles_and_names_broken_batches(self):
        row = next(entry for entry in self.reports[23]["entries"]
                   if entry["local_number"] == 27631)
        cross = row["archive_cross_check"]
        self.assertEqual(5, cross["cases"])
        self.assertEqual(20, len(cross["excluded_broken_oracles"]))
        self.assertTrue(all(item["input"].startswith("tests/20000-29982/27631/data/")
                            and item["reason"] for item in cross["excluded_broken_oracles"]))


if __name__ == "__main__":
    unittest.main()
