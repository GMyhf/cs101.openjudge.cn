"""4036 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 30 组数据。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4036
SAMPLE_IN = '1 1 3 1 2\n'
SAMPLE_OUT = '3\n'
REFERENCE_SOURCE = 'import math\na, b, k, n, m = map(int, input().split());\nprint((pow(a, n, 10007) * pow(b, m, 10007) * math.comb(k, m)) % 10007)\n'

def valid(text):
    """题面契约：一行 5 个整数 a b k n m，单空格分隔；0<=k<=1000，0<=n,m<=k，n+m=k，0<=a,b<=1,000,000。"""
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    parts = text[:-1].split(" ")
    if len(parts) != 5:
        return False
    try:
        a, b, k, n, m = map(int, parts)
    except ValueError:
        return False
    if any(x != str(int(x)) for x in parts):
        return False
    return 0 <= k <= 1000 and 0 <= n <= k and 0 <= m <= k and n + m == k and 0 <= a <= 10 ** 6 and 0 <= b <= 10 ** 6


def g4036(r, kind):
    A = 10 ** 6
    if kind == "small":
        a, b, k = r.randint(0, 100), r.randint(0, 100), r.randint(0, 20)
    elif kind == "one":            # 50% 数据 a=b=1：答案就是组合数
        a, b, k = 1, 1, r.randint(1, 1000)
    elif kind == "big":            # a、b 顶到 1e6，乘积不取模会溢出
        a, b, k = r.randint(A - 1000, A), r.randint(A - 1000, A), r.randint(900, 1000)
    elif kind == "mod0":           # a 或 b 是 10007 的倍数
        a, b, k = 10007 * r.randint(1, 99), r.randint(1, A), r.randint(1, 1000)
        if r.random() < 0.5:
            a, b = b, a
    else:
        a, b, k = r.randint(0, A), r.randint(0, A), r.randint(0, 1000)
    n = r.randint(0, k)
    return f"{a} {b} {k} {n} {k-n}\n"


FIXED = [
    "0 0 0 0 0\n",              # k=0：系数为 1
    "1000000 1000000 0 0 0\n",
    "0 5 3 0 3\n",              # a=0 但 n=0
    "0 5 3 1 2\n",              # a=0 且 n>0：0
    "1000000 1000000 1000 1000 0\n",
    "1000000 1000000 1000 0 1000\n",
    "1000000 999999 1000 500 500\n",
    "1 1 1000 500 500\n",       # 最大组合数
    "10007 1 5 0 5\n",          # a≡0 但 n=0
    "10007 1 5 2 3\n",
]
KINDS = ["small"] * 4 + ["one"] * 4 + ["big"] * 4 + ["mod0"] * 3 + ["rand"] * 4


def build_cases():
    cases = [SAMPLE_IN] + FIXED
    for i, kind in enumerate(KINDS):
        r = random.Random(NUMBER * 1000 + i)
        c = g4036(r, kind)
        while c in cases:
            c = g4036(r, kind)
        cases.append(c)
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
        assert valid(content), index
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
