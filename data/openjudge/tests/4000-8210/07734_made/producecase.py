"""7734 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 7734
SAMPLE_IN = '2\n3 3\n1 2\n2 3\n1 3\n4 2\n1 2\n3 4\n'
SAMPLE_OUT = 'Scenario #1:\nSuspicious bugs found!\n\nScenario #2:\nNo suspicious bugs found!\n'
REFERENCE_SOURCE = 'import sys\nsys.setrecursionlimit(1000000)\n\n\ndef solve():\n    T = int(input())\n\n    for case in range(1, T + 1):\n        n, m = map(int, input().split())\n\n        # 扩展域：1~n 表示性别A，n+1~2n 表示性别B\n        parent = list(range(2 * n + 1))\n\n        def find(i):\n            if parent[i] == i:\n                return i\n            parent[i] = find(parent[i])\n            return parent[i]\n\n        def union(i, j):\n            root_i = find(i)\n            root_j = find(j)\n            if root_i != root_j:\n                parent[root_i] = root_j\n\n        suspicious = False\n        for _ in range(m):\n            u, v = map(int, input().split())\n            if suspicious: continue\n\n            # 如果 u 和 v 已经在同一个性别域里，说明他们是同性！\n            if find(u) == find(v):\n                suspicious = True\n            else:\n                # u 恋爱对象必须是 v 的异性分身\n                union(u, v + n)\n                # v 恋爱对象必须是 u 的异性分身\n                union(v, u + n)\n\n        print(f"Scenario #{case}:")\n        if suspicious:\n            print("Suspicious bugs found!")\n        else:\n            print("No suspicious bugs found!")\n        print()\n\n\nsolve()\n'

def g7734(r):
    cases = []
    for _ in range(r.randint(1, 3)):
        n = r.randint(3, 20); edges = set()
        for i in range(1, n):
            edges.add((i, r.randint(1, i)))
        if r.random() < .5:
            edges.update({(1, 2), (2, 3), (1, 3)})
        cases.append(f"{n} {len(edges)}\n" + "\n".join(f"{a} {b}" for a, b in edges))
    return str(len(cases)) + "\n" + "\n".join(cases) + "\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g7734(random.Random(NUMBER + i + attempt * 1000))
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
