"""私有题库 1000001 筛选法建最小堆交换次数的数据与参考实现测试。"""
import unittest
from pathlib import Path
from judge import judge

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/openjudge/tests/private/1000001_made/data"
REFERENCE = (DATA.parent / "samplecode.py").read_text(encoding="utf-8")


def oracle(text):
    fields = list(map(int, text.split()))
    n, values = fields[0], fields[1:]
    heap = [0] + values
    swaps = 0
    for root in range(n // 2, 0, -1):
        pos = root
        while 2 * pos <= n:
            child = 2 * pos
            if child < n and heap[child + 1] < heap[child]:
                child += 1
            if heap[pos] <= heap[child]:
                break
            heap[pos], heap[child] = heap[child], heap[pos]
            swaps += 1
            pos = child
    return f"{swaps}\n"


class Problem1000001Tests(unittest.TestCase):
    def test_sample_answer(self):
        self.assertEqual(oracle((DATA / "0.in").read_text()), "6\n")

    def test_every_output_matches_oracle(self):
        cases = sorted(DATA.glob("*.in"), key=lambda p: int(p.stem))
        self.assertEqual(len(cases), 21)
        for path in cases:
            self.assertEqual(path.with_suffix(".out").read_text(), oracle(path.read_text()), path.name)

    def test_reference_accepted(self):
        self.assertEqual(judge("private", "1000001", "python", REFERENCE)["status"], "Accepted")


if __name__ == "__main__":
    unittest.main()
