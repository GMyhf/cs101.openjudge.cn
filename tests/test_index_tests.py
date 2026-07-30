"""索引器对 2008 存档目录的排除规则。

为什么值得单独一条：这条规则**决定学生的代码被哪些数据判**。排错方向都很难看 ——
排多了，题目静默变成「无测试数据」；排少了，2008 年的私人压力测试文件继续参与判题，
学生在平台上能过的代码在这里挂（01384 就是这么被撞见的）。
"""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import index_tests
import update_t028_candidate_globals


class ArchiveExclusionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT / "data" / "openjudge" / "catalog.json")
                                 .read_text(encoding="utf-8"))
        cls.per_entry, cls.practice = index_tests.catalog_global_numbers(cls.catalog)

    def test_archive_buckets_are_excluded_but_generated_data_is_not(self):
        for bucket in ("1000-1999", "2000-2999", "3000-3682"):
            self.assertTrue(index_tests.is_archive(bucket, "1384"), bucket)
            # 同一个桶里我们自己生成的数据必须留下 —— 这正是 T-028 在补的东西
            self.assertFalse(index_tests.is_archive(bucket, "1384_made"), bucket)
            self.assertTrue(index_tests.is_archive(bucket, "1384_GMyhf"), bucket)
            self.assertFalse(index_tests.is_archive(bucket, "2442-6648_made"), bucket)
        for bucket in ("4000-8210", "10000-19963", "20000-29982", "30000-"):
            self.assertFalse(index_tests.is_archive(bucket, "20025"), bucket)

    def test_catalog_carries_no_case_from_an_archive_bucket(self):
        """产物本身也要检：规则写对了但忘了重跑索引器，catalog 里照样留着旧引用。"""
        catalog = json.loads((ROOT / "data" / "openjudge" / "catalog.json")
                             .read_text(encoding="utf-8"))
        offenders = []
        for problem in catalog["problems"]:
            for case in problem.get("test_cases", []):
                parts = case["input"].split("/")
                if len(parts) > 2 and index_tests.is_archive(parts[1], parts[2]):
                    offenders.append(case["input"])
        self.assertEqual(offenders[:5], [], f"catalog 里还引着 {len(offenders)} 条存档数据")

    def test_generated_data_replaces_legacy_data_for_the_same_global_problem(self):
        offenders = []
        by_global = {}
        for problem in self.catalog["problems"]:
            by_global.setdefault(problem["global_number"], problem.get("test_cases", []))
        for global_number, cases in by_global.items():
            has_made = any(case["input"].split("/")[2].endswith("_made") for case in cases)
            if has_made:
                legacy = [case["input"] for case in cases
                          if not case["input"].split("/")[2].endswith("_made")]
                offenders.extend((global_number, path) for path in legacy)
        self.assertEqual([], offenders[:5],
                         f"已有自产数据的全局题仍混入 {len(offenders)} 条旧数据")

    def test_problem_pages_supply_global_identity(self):
        self.assertEqual(self.per_entry[("pctbook", "E02676")], 1678)
        self.assertEqual(self.per_entry[("practice", "02676")], 1678)

    def test_equal_local_suffix_does_not_override_global_identity(self):
        """后缀相同但其实是两道题 —— 这条判据从「钉住那一对」改成「钉住这条规则」。

        原来它断言 `routine/02746`→1747、`practice/02746`→1748。人 2026-07-29 拍板
        删掉了 `routine/02746` 那个别名（显示器在 `practice/02745` 保留），
        于是那一对不存在了。**但规则本身仍然要守**：如果哪次重新抓取又引进一对
        后缀相同、全局题号不同的条目，按后缀共享数据就会让一道题拿到另一道题的数据 ——
        这正是重构前「显示器拿约瑟夫问题的数据判」的成因。
        所以断言改成扫全库：**同一后缀不得对应多个全局题号。**
        """
        import collections
        by_suffix = collections.defaultdict(set)
        for (book, problem_id), global_number in self.per_entry.items():
            suffix = re.search(r"(\d+)$", problem_id).group(1).lstrip("0")
            by_suffix[suffix].add(global_number)
        clashes = {s: sorted(v) for s, v in by_suffix.items() if len(v) > 1}
        self.assertEqual(clashes, {}, f"后缀冲突会让题目拿到别人的数据：{clashes}")
        # 被删掉的那个别名不该再出现在 catalog 里
        self.assertNotIn(("routine", "02746"), self.per_entry)

    def test_different_local_ids_can_share_one_global_problem(self):
        self.assertEqual(self.per_entry[("2024fallroutine", "03253")], 2255)
        self.assertEqual(self.per_entry[("practice", "03254")], 2255)

    def test_sub_book_only_id_maps_only_when_unambiguous(self):
        directories = index_tests.test_directory_global_numbers(self.per_entry, self.practice)
        self.assertEqual(directories[2707], 1709)
        self.assertEqual(directories[2746], 1748)  # practice wins over routine's 1747

    def test_every_catalog_entry_carries_its_parsed_global_number(self):
        missing = []
        wrong = []
        for problem in self.catalog["problems"]:
            key = (problem["book"], problem["id"])
            if "global_number" not in problem:
                missing.append(key)
            elif problem["global_number"] != self.per_entry[key]:
                wrong.append(key)
        self.assertEqual(missing[:5], [], f"{len(missing)} catalog entries lack global_number")
        self.assertEqual(wrong[:5], [], f"{len(wrong)} catalog entries have stale global_number")

    def test_t028_candidates_use_global_identity_and_practice_entry(self):
        candidates = json.loads((ROOT / "collab" / "t028-candidates.json")
                                .read_text(encoding="utf-8"))["entries"]
        by_global = {row["global_number"]: row for row in candidates}
        self.assertEqual(len(by_global), len(candidates))
        self.assertEqual(by_global[1678]["practice_id"], "02676")
        self.assertNotIn("routine", by_global[1748]["books"])
        # 1747（显示器）原本挂在 routine/02746 与 practice/02745 两处；
        # routine/02746 已按人拍板删除（与约瑟夫问题后缀冲突），只剩 practice。
        self.assertEqual(by_global[1747]["books"], ["practice"])
        self.assertEqual(by_global[1747]["ids"], ["02745"])
        self.assertEqual(by_global[2255]["priority"], 47)
        self.assertIn(249, by_global[2255]["retired_priorities"])
        self.assertNotIn(30947, by_global)  # practice/30947 already has 21 cases


if __name__ == "__main__":
    unittest.main()
