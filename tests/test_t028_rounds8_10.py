import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import t028_rounds8_10


class T028RoundsEightToTenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifests = {r: json.loads((ROOT / "collab" / f"t028-round{r}-manifest.json").read_text()) for r in (8, 9, 10)}
        cls.reports = {r: json.loads((ROOT / "collab" / f"t028-round{r}-report.json").read_text()) for r in (8, 9, 10)}

    def test_priority_ranges_are_complete_with_explicit_exclusions(self):
        for round_number, expected in ((8, range(121,141)),(9,range(141,161)),(10,range(161,181))):
            manifest=self.manifests[round_number]
            priorities=[x["priority"] for x in manifest["entries"]]+[x["priority"] for x in manifest["excluded"]]
            self.assertEqual(sorted(priorities),list(expected))
            self.assertEqual(manifest["count"],19)
        excluded={x["local_number"] for m in self.manifests.values() for x in m["excluded"]}
        self.assertEqual(excluded,{0,1729,2982})

    def test_generators_and_counterexamples(self):
        rows=[x for manifest in self.manifests.values() for x in manifest["entries"]]
        labels=[];counterexamples=[]
        for row in rows:
            number=row["local_number"];labels.append(t028_rounds8_10.LABELS[number]);counterexamples.append(t028_rounds8_10.INVALID[number])
            seeds=(1,) if number in t028_rounds8_10.NO_INPUT else range(1,101)
            for seed in seeds:self.assertTrue(t028_rounds8_10.valid(number,t028_rounds8_10.generate(number,seed)),(number,seed))
            self.assertFalse(t028_rounds8_10.valid(number,t028_rounds8_10.INVALID[number]),number)
        self.assertEqual(len(labels),len(set(labels)))
        self.assertEqual(len(counterexamples),len(set(counterexamples)))

    def test_reference_selection_and_native_language_files(self):
        selection=json.loads((ROOT/"collab/t028-rounds8-10-reference-selection.json").read_text())
        self.assertEqual(len(selection["platform_references"]),45)
        for manifest in self.manifests.values():
            for row in manifest["entries"]:
                suffix="py" if row["reference_language"]=="Python3" else "cpp"
                source=(ROOT/"data/openjudge"/row["made_dir"]/f"samplecode.{suffix}").read_text()
                if row["solution_collection"]:self.assertIn("# Source collection:",source)
                else:self.assertIn("Accepted submission:",source)

    def test_reports_are_green_and_archive_sources_are_auditable(self):
        for round_number,report in self.reports.items():
            platform=json.loads((ROOT/"collab"/f"t028-round{round_number}-platform.json").read_text())
            local=json.loads((ROOT/"collab"/f"t028-round{round_number}-localjudge.json").read_text())
            self.assertEqual((platform["accepted"],platform["total"]),(19,19))
            self.assertEqual((local["accepted"],local["total"]),(19,19))
            self.assertEqual(report["failed"],[])
            for row in report["entries"]:
                self.assertEqual(row["status"],"passed")
                self.assertEqual(row["platform_verdict"],"Accepted")
                self.assertEqual(row["archive_cross_check"]["status"],"passed")
                self.assertTrue("dirs" in row["archive_cross_check"] or "no_archive_reason" in row["archive_cross_check"])
                self.assertEqual(row["merged_judge"]["verdict"],"Accepted")


if __name__ == "__main__":
    unittest.main()
