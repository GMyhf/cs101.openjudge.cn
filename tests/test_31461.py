"""课程组自出题 31461：官方数据、公开样例与进制转换判题。"""
import hashlib
import json
from pathlib import Path
import unittest

import judge
import server

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/openjudge/tests/30000-/31461_GMyhf"
PAGE = ROOT / "data/openjudge/pages/practice__31461.html"
DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SAMPLE_INPUT = """7
1a 16 10
-1011 2 16
00 36 2
-z 36 10
0255 10 16
-120 3 7
1 2 2
"""
SAMPLE_OUTPUT = """26
-B
0
-35
FF
-21
1
"""
REFERENCE = r'''import sys
D = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
tokens = sys.stdin.buffer.read().decode().split()
n = int(tokens[0])
pos = 1
out = []
for _ in range(n):
    s, a, b = tokens[pos], int(tokens[pos + 1]), int(tokens[pos + 2])
    pos += 3
    negative = s.startswith("-")
    if negative:
        s = s[1:]
    value = 0
    for char in s:
        value = value * a + D.index(char.upper())
    if negative:
        value = -value
    if value == 0:
        out.append("0")
        continue
    sign = "-" if value < 0 else ""
    value = abs(value)
    converted = ""
    while value:
        value, rem = divmod(value, b)
        converted = D[rem] + converted
    out.append(sign + converted)
sys.stdout.write("\n".join(out) + ("\n" if out else ""))
'''


def oracle(s, a, b):
    value = int(s, a)
    if not value:
        return "0"
    sign = "-" if value < 0 else ""
    value = abs(value)
    converted = ""
    while value:
        value, rem = divmod(value, b)
        converted = DIGITS[rem] + converted
    return sign + converted


class BaseConversion31461Tests(unittest.TestCase):
    def test_official_data_source_and_catalog(self):
        source = json.loads((DATA / "SOURCE.json").read_text(encoding="utf-8"))
        self.assertEqual(source["owner"], "GMyhf")
        self.assertEqual(source["problem_source"], "2026TA-zzy")
        self.assertIn("官方测试数据可直接使用", source["authorization_evidence"])
        self.assertEqual(len(source["files"]), 3)
        for record in source["files"]:
            for kind in ("input", "output"):
                path = DATA / "data" / f"{record['case']}.{'in' if kind == 'input' else 'out'}"
                payload = path.read_bytes()
                self.assertEqual(len(payload), record[f"{kind}_bytes"])
                self.assertEqual(hashlib.sha256(payload).hexdigest(), record[f"{kind}_sha256"])
        item = judge.catalog_item("practice", "31461")
        self.assertTrue(item["tests"])
        self.assertEqual(item["global_number"], 31461)
        self.assertEqual(item["test_count"], 3)
        limits = judge.problem_limits(31461)
        self.assertEqual(limits["total_ms"], 300)
        self.assertEqual(limits["memory_kb"], 10000)

    def test_every_official_answer_matches_independent_oracle(self):
        total = 0
        for path in sorted((DATA / "data").glob("*.in"), key=lambda p: int(p.stem)):
            lines = path.read_text(encoding="utf-8").splitlines()
            count = int(lines[0])
            self.assertEqual(len(lines), count + 1, path.name)
            expected = []
            for line in lines[1:]:
                s, a, b = line.split()
                a, b = int(a), int(b)
                self.assertTrue(2 <= a <= 36 and 2 <= b <= 36)
                value = int(s, a)
                self.assertTrue(-(1 << 63) <= value < (1 << 63))
                expected.append(oracle(s, a, b))
            actual = path.with_suffix(".out").read_text(encoding="utf-8").splitlines()
            self.assertEqual(actual, expected, path.name)
            total += count
        self.assertEqual(total, 14704)

    def test_public_sample_and_int64_boundaries(self):
        handler = object.__new__(server.Handler)
        payload = handler.sample_payload(PAGE, "practice", "31461")
        self.assertEqual(payload["input"], SAMPLE_INPUT.rstrip("\n"))
        self.assertEqual(payload["output"], SAMPLE_OUTPUT.rstrip("\n"))
        result = judge.run_sample("practice", "31461", "python", REFERENCE, SAMPLE_INPUT)
        self.assertEqual((result["status"], result["stdout"]), ("OK", SAMPLE_OUTPUT))
        boundary_input = """4
9223372036854775807 10 16
-9223372036854775808 10 16
-000 10 2
000z 36 36
"""
        boundary_output = "7FFFFFFFFFFFFFFF\n-8000000000000000\n0\nZ\n"
        result = judge.run_sample("practice", "31461", "python", REFERENCE, boundary_input)
        self.assertEqual((result["status"], result["stdout"]), ("OK", boundary_output))

    def test_reference_accepted_and_decimal_only_answer_rejected(self):
        result = judge.judge("practice", "31461", "python", REFERENCE)
        self.assertEqual(result["status"], "Accepted", result)
        decimal_only = r'''import sys
tokens = sys.stdin.read().split()
out = []
for i in range(int(tokens[0])):
    s, a = tokens[1 + 3 * i], int(tokens[2 + 3 * i])
    out.append(str(int(s, a)))
sys.stdout.write("\n".join(out))
'''
        result = judge.judge("practice", "31461", "python", decimal_only)
        self.assertEqual(result["status"], "Wrong Answer", result)


if __name__ == "__main__":
    unittest.main()
