"""5902 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 5902
SAMPLE_IN = '2\n5\n1 2\n1 3\n1 4\n2 0\n2 1\n6\n1 1\n1 2\n1 3\n2 0\n2 1\n2 0\n'
SAMPLE_OUT = '3\nNULL\n'
REFERENCE_SOURCE = "from collections import deque\n\nfor _ in range(int(input())):\n    n=int(input())\n    q=deque([])\n    for i in range(n):\n        a,b=map(int,input().split())\n        if a==1:\n            q.append(b)\n        else:\n            if b==0:\n                q.popleft()\n            else:\n                q.pop()\n    if q:\n        print(*q)\n    else:\n        print('NULL')\n"

def g5902(r):
    cases = []
    for _ in range(r.randint(1, 3)):
        ops = []; size = 0
        for _ in range(r.randint(6, 30)):
            if not size or r.random() < .65:
                ops.append(f"1 {r.randint(-1000, 1000)}"); size += 1
            else:
                ops.append(f"2 {r.randint(0, 1)}"); size -= 1
        cases.append(str(len(ops)) + "\n" + "\n".join(ops))
    return str(len(cases)) + "\n" + "\n".join(cases) + "\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g5902(random.Random(NUMBER + i + attempt * 1000))
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
