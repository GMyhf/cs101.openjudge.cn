"""9202 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 9202
SAMPLE_IN = '2\n7 6\n1 2\n1 3\n2 4\n2 5\n3 6\n3 7\n12 13\n1 2\n2 3\n2 4\n3 5\n5 6\n4 6\n6 7\n7 8\n8 4\n7 9\n9 10\n10 11\n10 12\n'
SAMPLE_OUT = 'No\nYes\n'
REFERENCE_SOURCE = "# 蒋子轩 工院\nfrom collections import deque,defaultdict\ndef topo_sort(graph):\n    in_degree={u:0 for u in range(1,n+1)}\n    for u in graph:\n        for v in graph[u]:\n            in_degree[v]+=1\n    q=deque([u for u in in_degree if in_degree[u]==0])\n    topo_order=[]\n    while q:\n        u=q.popleft()\n        topo_order.append(u)\n        for v in graph[u]:\n            in_degree[v]-=1\n            if in_degree[v]==0:\n                q.append(v)\n    if len(topo_order)!=len(graph):\n        return 'Yes'\n    return 'No'\nfor _ in range(int(input())):\n    n,m=map(int,input().split())\n    graph=defaultdict(list)\n    for _ in range(m):\n        u,v=map(int,input().split())\n        graph[u].append(v)\n    print(topo_sort(graph))\n"

def g9202(r):
    n = r.randint(4, 25); edges = set()
    for i in range(1, n): edges.add((i, r.randint(1, i)))
    if r.random() < .5: edges.add((1, n)); edges.add((n, 1))
    return "1\n" + f"{n} {len(edges)}\n" + "\n".join(f"{a} {b}" for a, b in edges) + "\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g9202(random.Random(NUMBER + i + attempt * 1000))
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
