"""4005 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4005
SAMPLE_IN = '3\n92 83 71\n95 87 74\n2\n20 20\n20 20\n2\n20 19\n22 18\n0\n'
SAMPLE_OUT = '9 5\n4 4\n4 4\n'
REFERENCE_SOURCE = 'def get_max_profit(a1, a2):\n    la1 = 0\n    ra1 = len(a1) - 1\n    la2 = 0\n    ra2 = len(a2) - 1\n    ans_max = 0\n    ans_min = 0\n\n    while la2 <= ra2:\n        if a2[la2] > a1[la1]:\n            ans_max += 3\n            ans_min += 1\n            la1 += 1\n            la2 += 1\n        elif a2[ra2] > a1[ra1]:\n            ans_max += 3\n            ans_min += 1\n            ra1 -= 1\n            ra2 -= 1\n        else:\n            if a2[la2] < a1[ra1]:\n                ans_max += 1\n                ans_min += 3\n            elif a2[la2] == a1[ra1]:\n                ans_max += 2\n                ans_min += 2\n\n            la2 += 1\n            ra1 -= 1\n\n    return ans_max, ans_min\n\n\nwhile True:\n    n = int(input())\n    if n == 0:\n        break\n\n    *C, = map(int, input().split())\n    *S, = map(int, input().split())\n    C.sort()\n    S.sort()\n\n    ans_max, _ = get_max_profit(C, S)\n    _, ans_min = get_max_profit(S, C)\n\n    print(ans_max, ans_min)\n'

def g4005(r):
    lines = []
    for _ in range(r.randint(2, 5)):
        n = r.randint(1, 12)
        lines += [str(n), " ".join(str(r.randint(1, 100)) for _ in range(n)), " ".join(str(r.randint(1, 100)) for _ in range(n))]
    return "\n".join(lines + ["0"]) + "\n"

def build_cases():
    return [SAMPLE_IN] + [g4005(random.Random(NUMBER + i)) for i in range(1, 20)]

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
