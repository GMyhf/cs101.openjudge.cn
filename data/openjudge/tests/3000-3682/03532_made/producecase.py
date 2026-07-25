"""3532 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
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

def build_cases():
    return [SAMPLE_IN] + [g3532(random.Random(NUMBER + i)) for i in range(1, 20)]

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
