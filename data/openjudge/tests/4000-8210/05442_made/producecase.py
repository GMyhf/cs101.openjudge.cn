"""5442 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001b
生成器与循环取自 scripts/build_001b.py（批次 001b），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 5442
SAMPLE_IN = '9\nA 2 B 12 I 25\nB 3 C 10 H 40 I 8\nC 2 D 18 G 55\nD 1 E 44\nE 2 F 60 G 38\nF 0\nG 1 H 35\nH 1 I 35\n'
SAMPLE_OUT = '216\n'
REFERENCE_SOURCE = "import heapq\n\ndef prim(graph, start):\n    mst = []\n    used = set([start])\n    edges = [\n        (cost, start, to)\n        for to, cost in graph[start].items()\n    ]\n    heapq.heapify(edges)\n\n    while edges:\n        cost, frm, to = heapq.heappop(edges)\n        if to not in used:\n            used.add(to)\n            mst.append((frm, to, cost))\n            for to_next, cost2 in graph[to].items():\n                if to_next not in used:\n                    heapq.heappush(edges, (cost2, to, to_next))\n\n    return mst\n\ndef solve():\n    n = int(input())\n    graph = {chr(i+65): {} for i in range(n)}\n    for i in range(n-1):\n        data = input().split()\n        star = data[0]\n        m = int(data[1])\n        for j in range(m):\n            to_star = data[2+j*2]\n            cost = int(data[3+j*2])\n            graph[star][to_star] = cost\n            graph[to_star][star] = cost\n    mst = prim(graph, 'A')\n    print(sum(x[2] for x in mst))\n\nsolve()\n"

def g5442(r):
    n = r.randint(4, 20); edges = {(i, i + 1): r.randint(1, 99) for i in range(n - 1)}
    degree = [0] * n
    for i in range(n - 1):
        degree[i] += 1; degree[i + 1] += 1
    for i in range(n):
        for j in range(i + 2, n):
            if len(edges) >= 75 or degree[i] >= 15 or degree[j] >= 15 or r.random() >= .18: continue
            edges[(i, j)] = r.randint(1, 99)
            degree[i] += 1; degree[j] += 1
    rows = []
    for i in range(n - 1):
        later = [(j, w) for (a, j), w in edges.items() if a == i]
        rows.append(" ".join([chr(65 + i), str(len(later))] + [x for pair in later for x in (chr(65 + pair[0]), str(pair[1]))]))
    return str(n) + "\n" + "\n".join(rows) + "\n"

def build_cases():
    return [SAMPLE_IN] + [g5442(random.Random(NUMBER + i)) for i in range(1, 20)]

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
