"""3532 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的数据（0..19 原批次，20 起为边界/满规模组）。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import re
import subprocess
import tempfile
from pathlib import Path

NUMBER = 3532
SAMPLE_IN = '7\n1 7 3 5 9 4 8\n'
SAMPLE_OUT = '18\n'
REFERENCE_SOURCE = 'import copy\nn = int(input())\na = list(map(int, input().split()))\ndp = copy.deepcopy(a)\nfor i in range(n):    \n    for j in range(i):        \n        if a[j] < a[i]:            \n            dp[i] = max(dp[j] + a[i], dp[i])\n\nprint(max(dp))\n'

def g3532(r):
    n = r.randint(1, 100); a = [r.randint(1, 1000) for _ in range(n)]
    return f"{n}\n" + " ".join(map(str, a)) + "\n"

def valid(text):
    """题面契约：第一行 N（1 <= N <= 1000），第二行恰好 N 个 0..10000 的整数。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 2 or not re.fullmatch(r"\d+", lines[0]):
        return False
    n = int(lines[0])
    toks = lines[1].split()
    if not 1 <= n <= 1000 or len(toks) != n:
        return False
    return all(re.fullmatch(r"\d+", t) and int(t) <= 10000 for t in toks)


def fmt(a):
    return f"{len(a)}\n" + " ".join(map(str, a)) + "\n"


def extra_cases(r):
    inc = sorted(r.sample(range(10001), 1000))
    return [
        fmt([0]),                                   # N=1，取值下界
        fmt([10000]),                               # N=1，取值上界
        fmt([7] * 1000),                            # 全相等：严格上升，答案 7（<= 写法得 7000）
        fmt([0] * 1000),                            # 全 0
        fmt(list(range(10000, 9000, -1))),          # 严格下降：答案为最大元素
        fmt(inc),                                   # 严格上升 N=1000：答案为总和
        fmt([100, 1, 2, 3] + [r.randint(0, 3) for _ in range(996)]),  # 最长上升 != 最大和
        fmt([r.randint(0, 10000) for _ in range(1000)]),
        fmt([r.randint(0, 20) for _ in range(1000)]),  # 大量重复
        fmt([x + r.randint(-50, 50) if 50 <= x <= 9950 else x for x in sorted(r.randint(0, 10000) for _ in range(1000))]),
        fmt([5000 - abs(500 - i) * 10 for i in range(1000)]),  # 先升后降
    ]


def build_cases():
    return ([SAMPLE_IN] + [g3532(random.Random(NUMBER + i)) for i in range(1, 20)]
            + extra_cases(random.Random(NUMBER * 1000 + 1)))

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
        assert valid(content), index
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
