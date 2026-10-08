import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'class Solution:\n    def intToRoman(self, num: int) -> str:\n        roman_numerals = [\n            (1000, \'M\'), (900, \'CM\'), (500, \'D\'), (400, \'CD\'),\n            (100, \'C\'), (90, \'XC\'), (50, \'L\'), (40, \'XL\'),\n            (10, \'X\'), (9, \'IX\'), (5, \'V\'), (4, \'IV\'), (1, \'I\')\n        ]\n\n        result = []\n        for value, symbol in roman_numerals:\n            while num >= value:\n                result.append(symbol)\n                num -= value\n            if num == 0:\n                break\n\n        return \'\'.join(result)\n\nif __name__ == "__main__":\n    sol = Solution()\n    n = int(input())\n    print(sol.intToRoman(n))\n'
SAMPLE_IN = '3749\n'
import re
SEED_BASE = 29411

def valid(text):
    """题面未写数值范围；规则规定 M 最多连写 3 次、罗马数字无 0，故可表示的整数为 1..3999。只认一行一个整数。"""
    if not text.endswith('\n'): return False
    L = text[:-1].split('\n')
    if len(L) != 1 or not re.fullmatch(r'[1-9][0-9]{0,3}', L[0]): return False
    return 1 <= int(L[0]) <= 3999

def generate_case(r):
    return f"{r.randint(1, 3999)}\n"

def extra_cases():
    # 边界与各减法形式：1、3999、最长串 3888、每一位上的 4/9、整千整百等
    vals = [1, 2, 3, 4, 5, 9, 10, 14, 40, 44, 49, 90, 99, 400, 444, 499, 900, 999, 1000, 1994, 3000, 3888, 3999, 1666, 2421, 58, 3449]
    return [f"{v}\n" for v in vals]

def build_cases():
    seen = [SAMPLE_IN]
    cases = []
    for index in range(40):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(SEED_BASE + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content); cases.append(content)
    for content in extra_cases():
        if content not in cases: cases.append(content)   # 与随机组重复的边界值跳过
    for content in cases:
        assert valid(content), content[:80]
    return cases

def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        for index, content in enumerate(build_cases()):
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=60, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()
