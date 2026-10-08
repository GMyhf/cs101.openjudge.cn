"""5442 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 34 组数据（第 20 组起为边界组与 n=26 / 75 条边的满规模组）。

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

def valid(text):
    """题面：第一行 n（不大于 26），星星为前 n 个大写字母；接着 n-1 行依次以 A、B…开头，
    「字母 k」后跟 k 条边「字母 权值」，另一端是字母表中更靠后的星星，权值为小于 100 的正整数，字段间单个空格；
    网络连通；边数不超过 75；每颗星星连出的边不超过 15 条。"""
    lines = text.split("\n")
    if len(lines) < 2 or lines[-1] != "":
        return False
    lines = lines[:-1]
    if not lines[0].isdigit() or not 1 <= int(lines[0]) <= 26:
        return False
    n = int(lines[0])
    if len(lines) != n:
        return False
    edges = set(); degree = [0] * n; parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x

    for i, line in enumerate(lines[1:]):
        parts = line.split(" ")
        if len(parts) < 2 or parts[0] != chr(65 + i) or not parts[1].isdigit():
            return False
        k = int(parts[1])
        if len(parts) != 2 + 2 * k:
            return False
        for j in range(k):
            to, w = parts[2 + 2 * j], parts[3 + 2 * j]
            if len(to) != 1 or not i < ord(to) - 65 < n or not w.isdigit() or not 1 <= int(w) < 100:
                return False
            t = ord(to) - 65
            if (i, t) in edges:
                return False
            edges.add((i, t)); degree[i] += 1; degree[t] += 1
            parent[find(i)] = find(t)
    if len(edges) > 75 or max(degree) > 15:
        return False
    return len({find(x) for x in range(n)}) == 1


def g5442_big(r, n, target_edges, wmax=99):
    """随机生成树打底（不再总是 A-B-C… 链），再随机加边到 target_edges，守住 75 条边、度数 15 的上限。"""
    order = list(range(n)); r.shuffle(order)
    edges = {}; degree = [0] * n
    for idx in range(1, n):
        u, v = order[idx], order[r.randrange(idx)]
        a, b = min(u, v), max(u, v)
        if degree[a] >= 15 or degree[b] >= 15:
            v = next(order[j] for j in range(idx) if degree[order[j]] < 15)
            a, b = min(u, v), max(u, v)
        edges[(a, b)] = r.randint(1, wmax); degree[a] += 1; degree[b] += 1
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    r.shuffle(pairs)
    for a, b in pairs:
        if len(edges) >= target_edges: break
        if (a, b) in edges or degree[a] >= 15 or degree[b] >= 15: continue
        edges[(a, b)] = r.randint(1, wmax); degree[a] += 1; degree[b] += 1
    rows = []
    for i in range(n - 1):
        later = sorted((j, w) for (a, j), w in edges.items() if a == i)
        if r.random() < .5: r.shuffle(later)
        rows.append(" ".join([chr(65 + i), str(len(later))] + [x for j, w in later for x in (chr(65 + j), str(w))]))
    return str(n) + "\n" + "".join(row + "\n" for row in rows)


EDGE_CASES = [
    "1\n",                       # 只有一颗星，答案 0
    "2\nA 1 B 99\n",            # 两颗星，权值取上界 99
    "3\nA 2 B 1 C 1\nB 1 C 1\n",  # 等权三角形
    "3\nA 1 C 7\nB 1 C 3\n",    # A 不直接连 B，靠 C 中转
]


def build_cases():
    cases = [SAMPLE_IN] + [g5442(random.Random(NUMBER + i)) for i in range(1, 20)] + EDGE_CASES
    r = random.Random(544200)
    for n, m, wmax in ((26, 75, 99), (26, 75, 99), (26, 25, 99), (26, 75, 3), (26, 50, 99),
                       (25, 75, 99), (26, 75, 1), (12, 66, 99), (26, 40, 10), (16, 75, 99)):
        cases.append(g5442_big(r, n, m, wmax))
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
    assert all(valid(c) for c in cases), "有数据越出题面约束"
    assert len(set(cases)) == len(cases), "有重复组"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
