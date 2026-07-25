"""判题核心回归测试。

夹具自带在 `tests/fixtures/mirror/` 下并已入库，不依赖 `data/openjudge/tests/**`
（那批抓取数据按人拍板决策不入库），因此新克隆的仓库也能跑通交接闸门。
"""
import unittest
from pathlib import Path
from unittest import mock

import judge as judge_module
from judge import judge


FIXTURE_MIRROR = Path(__file__).resolve().parent / "fixtures" / "mirror"
BOOK = "t001"
PROBLEM = "SUM2"          # 两组数据：1 2 -> 3、10 20 -> 30
SUM_SOURCE = "a, b = map(int, input().split())\nprint(a + b)\n"


class JudgeCoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        patcher = mock.patch.object(judge_module, "MIRROR", FIXTURE_MIRROR)
        patcher.start()
        cls.addClassCleanup(patcher.stop)

    def test_accepts_token_equivalent_output(self):
        # 正确解法，但输出裹上多余空白：token 比对语义应判 AC，且两组数据都要跑到。
        source = "a, b = map(int, input().split())\nprint('  ', a + b, '  ')\n"
        result = judge(BOOK, PROBLEM, "python", source)
        self.assertEqual(result["status"], "Accepted")
        self.assertEqual(result["cases"], 2)

    def test_wrong_answer_reports_the_failing_case(self):
        # 第 1 组正确、第 2 组错误：必须报出错在第 2 组，而不是笼统的 WA。
        source = "a, b = map(int, input().split())\nprint(3 if a == 1 else 0)\n"
        result = judge(BOOK, PROBLEM, "python", source)
        self.assertEqual(result["status"], "Wrong Answer")
        self.assertEqual(result["case"], 2)

    def test_compile_error_is_distinct_from_runtime_error(self):
        result = judge(BOOK, PROBLEM, "python", "def broken(:\n    pass\n")
        self.assertEqual(result["status"], "Compile Error")

    def test_runtime_error(self):
        result = judge(BOOK, PROBLEM, "python", "raise RuntimeError('T001')\n")
        self.assertEqual(result["status"], "Runtime Error")
        self.assertEqual(result["case"], 1)

    def test_wall_clock_timeout_is_reported_as_tle(self):
        # 只睡不烧 CPU，RLIMIT_CPU 不会触发，确定性地走墙钟超时分支。
        result = judge(BOOK, PROBLEM, "python", "import time\ntime.sleep(30)\n")
        self.assertEqual(result["status"], "Time Limit Exceeded")
        self.assertIn("5 秒", result["message"])

    def test_cpu_limit_kill_is_reported_as_tle(self):
        # RLIMIT_CPU 与 5 秒墙钟是竞争关系，忙等无法稳定命中 CPU 分支；
        # 直接自发 SIGXCPU 才能确定性地钉住信号分类那一行。
        source = "import os, signal\nos.kill(os.getpid(), signal.SIGXCPU)\n"
        result = judge(BOOK, PROBLEM, "python", source)
        self.assertEqual(result["status"], "Time Limit Exceeded")
        self.assertIn("CPU", result["message"])

    def test_output_limit_is_enforced(self):
        source = "print('x' * (2 * 1024 * 1024 + 1))\n"
        result = judge(BOOK, PROBLEM, "python", source)
        self.assertEqual(result["status"], "Output Limit Exceeded")

    def test_problem_without_test_data_is_reported(self):
        result = judge(BOOK, "NODATA", "python", SUM_SOURCE)
        self.assertEqual(result["status"], "No Test Data")


if __name__ == "__main__":
    unittest.main()
