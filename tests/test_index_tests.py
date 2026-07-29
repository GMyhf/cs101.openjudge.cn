"""索引器对 2008 存档目录的排除规则。

为什么值得单独一条：这条规则**决定学生的代码被哪些数据判**。排错方向都很难看 ——
排多了，题目静默变成「无测试数据」；排少了，2008 年的私人压力测试文件继续参与判题，
学生在平台上能过的代码在这里挂（01384 就是这么被撞见的）。
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import index_tests


class ArchiveExclusionTests(unittest.TestCase):
    def test_archive_buckets_are_excluded_but_generated_data_is_not(self):
        for bucket in ("1000-1999", "2000-2999", "3000-3682"):
            self.assertTrue(index_tests.is_archive(bucket, "1384"), bucket)
            # 同一个桶里我们自己生成的数据必须留下 —— 这正是 T-028 在补的东西
            self.assertFalse(index_tests.is_archive(bucket, "1384_made"), bucket)
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


if __name__ == "__main__":
    unittest.main()
