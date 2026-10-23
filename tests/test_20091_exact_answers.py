"""20091 的锁数必须精确，平台曾用浮点除法生成错误答案。"""
import math
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "data/openjudge/tests/20000-29982"


class ExactLockCountTests(unittest.TestCase):
    def test_all_local_answers_are_exact_combinations(self):
        for name in ("20091_made", "20091_GMyhf"):
            for path in sorted((TESTS / name / "data").glob("*.in")):
                with self.subTest(directory=name, case=path.stem):
                    values = list(map(int, path.read_text().split()))
                    self.assertEqual(values[0], len(values) - 1)
                    expected = [str(math.comb(n, n // 2)) for n in values[1:]]
                    self.assertTrue(path.with_suffix(".out").read_text().split() == expected,
                                    "答案与精确组合数不一致")

    def test_reference_is_exact_across_the_statement_range(self):
        numbers = list(range(3, 1001))
        result = subprocess.run(
            [sys.executable, "-I", str(TESTS / "20091_made/samplecode.py")],
            input=str(len(numbers)) + "\n" + "\n".join(map(str, numbers)) + "\n",
            text=True, capture_output=True, timeout=10, check=True)
        self.assertTrue(result.stdout.split() ==
                        [str(math.comb(n, n // 2)) for n in numbers],
                        "参考解法在 3..1000 范围内存在不精确的答案")


if __name__ == "__main__":
    unittest.main()
