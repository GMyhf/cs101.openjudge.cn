"""20449 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001d
生成器与循环取自 scripts/build_001d.py（批次 001d），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 20449
SAMPLE_IN = '011\n'
SAMPLE_OUT = '100\n'
REFERENCE_SOURCE = "def binary_divisible_by_five(binary_string):\n    result = ''\n    num = 0\n    for bit in binary_string:\n        num = (num * 2 + int(bit)) % 5\n        if num == 0:\n            result += '1'\n        else:\n            result += '0'\n    return result\n\nbinary_string = input().strip()\nprint(binary_divisible_by_five(binary_string))\n"

# 题面：输入一个由 0 和 1 组成的字串（未给长度上限）。


def valid(text):
    import re
    return re.fullmatch(r"[01]+\n", text) is not None


_EDGE = ["0", "1", "101", "1010", "0000000000", "1111111111", "000101", "110010110", "11110000"]


def g20449(r, i):
    if i <= len(_EDGE):
        return _EDGE[i - 1] + "\n"
    if i <= 12:        # 原来的形状
        return "".join(r.choice("01") for _ in range(r.randint(1, 30))) + "\n"
    if i <= 14:        # 中等长度、带前导 0
        return "0" * r.randint(1, 50) + "".join(r.choice("01") for _ in range(r.randint(500, 5000))) + "\n"
    if i <= 16:        # 长串：逐位把整个前缀当大整数算（不取模）会平方级变慢
        return "".join(r.choice("01") for _ in range(r.choice((100000, 300000)))) + "\n"
    if i == 17:        # 多数位为 1，能被 5 整除的前缀稀少
        return "".join("1" if r.random() < .9 else "0" for _ in range(500000)) + "\n"
    if i == 18:        # 周期 1010…：每 4 位出现一次 1010=10
        return "1010" * 250000 + "\n"
    return "".join(r.choice("01") for _ in range(1000000)) + "\n"   # 满 1MB

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g20449(random.Random(NUMBER + i + attempt * 1000), i)
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
    return cases

def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=120, check=True)
    return result.stdout


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
