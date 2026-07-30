import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import audit_gmyhf_data


class AdminProblemParserTests(unittest.TestCase):
    def test_only_operation_edit_link_proves_ownership(self):
        page = """
        <a href="?page=3">3</a>
        <table>
          <tr><td class="number">27150</td><td class="title">Eight</td>
              <td class="author">GMyhf</td><td class="operation"></td></tr>
          <tr><td class="number">30921</td><td class="title">Blocks</td>
              <td class="author">someone else</td><td class="operation">
              <a href="/admin/problems/edit/?id=30921">编辑</a></td></tr>
        </table>
        """
        rows, pages = audit_gmyhf_data.parse_admin_page(page)
        self.assertEqual({3}, pages)
        self.assertEqual([30921], [row["global_number"] for row in rows])
        self.assertEqual("someone else", rows[0]["author"])


class GMyhfDataArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = json.loads(audit_gmyhf_data.AUDIT.read_text(encoding="utf-8"))
        cls.localjudge = json.loads((ROOT / "collab/gmyhf-localjudge.json")
                                    .read_text(encoding="utf-8"))
        cls.catalog = json.loads((audit_gmyhf_data.OPENJUDGE / "catalog.json")
                                 .read_text(encoding="utf-8"))["problems"]

    def test_audit_decisions_match_active_catalog(self):
        materialized = {int(row["global_number"]) for row in self.audit["entries"]
                        if row.get("materialized_dir")}
        problems = {int(row["global_number"]) for row in self.audit["entries"]
                    if row["status"] == "original_problem"}
        self.assertEqual(159, len(materialized))
        self.assertEqual({18159, 27631, 27699, 28050, 28190, 28203, 30172,
                          30179, 30550, 30720, 30908, 30921, 30937}, problems)
        for item in self.catalog:
            number = int(item["global_number"])
            paths = [case["input"] for case in item.get("test_cases", [])]
            if number in materialized:
                self.assertTrue(paths and all("_GMyhf/" in path for path in paths), number)
            elif number in problems:
                self.assertTrue(paths and all("_made/" in path for path in paths), number)

    def test_materialized_files_match_recorded_hashes(self):
        checked = 0
        for row in self.audit["entries"]:
            if not row.get("materialized_dir"):
                continue
            directory = ROOT / row["materialized_dir"]
            provenance = json.loads((directory / "SOURCE.json").read_text(encoding="utf-8"))
            for item in provenance["files"]:
                input_path = directory / "data" / f"{item['case']}.in"
                output_path = directory / "data" / f"{item['case']}.out"
                self.assertEqual(item["input_sha256"], audit_gmyhf_data.sha256(input_path))
                self.assertEqual(item["output_sha256"], audit_gmyhf_data.sha256(output_path))
                checked += 1
        self.assertEqual(3309, checked)

    def test_partial_copies_record_every_excluded_pair(self):
        partial = {int(row["global_number"]): row for row in self.audit["entries"]
                   if row["status"] == "partial_eligible"}
        self.assertEqual({27103, 27150, 28046}, set(partial))
        self.assertEqual(20, len(partial[27103]["excluded_pairs"]))
        self.assertEqual(1, len(partial[28046]["excluded_pairs"]))
        self.assertEqual(1, len(partial[27150]["excluded_pairs"]))
        exemption = partial[27150]["multi_answer_exemption"]
        self.assertEqual((19, 12, 7), (exemption["kept_cases"],
                                      exemption["unique_yes_cases"],
                                      exemption["no_answer_cases"]))

    def test_runtime_margin_rejections_stay_on_made_data(self):
        rejected = {int(row["global_number"]): row for row in self.audit["entries"]
                    if any(issue.get("status") == "insufficient_runtime_margin"
                           for issue in row.get("issues", []))}
        self.assertEqual({28190, 30179, 30908, 30937}, set(rejected))
        for row in rejected.values():
            issue = next(issue for issue in row["issues"]
                         if issue.get("status") == "insufficient_runtime_margin")
            self.assertGreater(issue["ratio"], issue["required_max_ratio"])

    def test_every_active_reference_has_per_case_runtime_margin(self):
        report = self.localjudge
        self.assertEqual((159, 159, []),
                         (report["count"], report["accepted"], report["failed"]))
        self.assertEqual(159, len(report["entries"]))
        for row in report["entries"]:
            timing = row.get("timing_audit", {})
            self.assertEqual("passed", timing.get("status"), row["global_number"])
            self.assertLessEqual(timing["max_case"]["ratio"],
                                 timing["required_max_ratio"], row["global_number"])
            self.assertEqual(row["cases"], len(timing["cases"]), row["global_number"])


if __name__ == "__main__":
    unittest.main()
