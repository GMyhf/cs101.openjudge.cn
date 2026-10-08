import random
REFERENCE='# External reference: /practice/30022/statistics/\n# Accepted submission: 52733303\n# Source: http://cs101.openjudge.cn/practice/solution/52733303/\n# License: not declared on the submission page; no license is inferred.\n\nfrom collections import deque\nimport sys\n\ndef bfs(start, n, adj):\n    dist = [-1] * n\n    q = deque()\n    q.append(start)\n    dist[start] = 0\n    while q:\n        u = q.popleft()\n        for v in range(n):\n            if adj[u][v] == 1 and dist[v] == -1:\n                dist[v] = dist[u] + 1\n                q.append(v)\n    return dist\n\ndef main():\n    n, k, s = map(int, sys.stdin.readline().split())\n    adj = []\n    for _ in range(n):\n        row = list(map(int, sys.stdin.readline().split()))\n        adj.append(row)\n    \n    d1 = bfs(k, n, adj)\n    d2 = bfs(s, n, adj)\n    \n    min_len = float(\'inf\')\n    for u in range(n):\n        if d1[u] == -1 or d2[u] == -1:\n            continue\n        if d1[u] == d2[u]:\n            if d1[u] < min_len:\n                min_len = d1[u]\n    \n    print(min_len if min_len != float(\'inf\') else -1)\n\nif __name__ == "__main__":\n    main()'
SAMPLE='5 0 4\n0 1 0 0 1\n1 0 1 0 0\n0 1 0 1 0\n0 0 1 0 1\n1 0 0 1 0\n'
GENERATOR_NAME='g30022'
import re as _re

def valid(text):
    """题面：第一行 n∈[1,1000], k,s∈[0,n-1]；随后 n 行每行 n 个 0/1；矩阵对称、对角为 0。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    if not lines or not _re.fullmatch(r'\d+ \d+ \d+', lines[0]):
        return False
    n, k, s = map(int, lines[0].split())
    if not (1 <= n <= 1000 and 0 <= k < n and 0 <= s < n):
        return False
    if len(lines) != n + 1:
        return False
    mat = []
    for line in lines[1:]:
        toks = line.split(' ')
        if len(toks) != n or any(t not in ('0', '1') for t in toks):
            return False
        mat.append(toks)
    for i in range(n):
        if mat[i][i] != '0':
            return False
        for j in range(i + 1, n):
            if mat[i][j] != mat[j][i]:
                return False
    return True

def _fmt(n, k, s, edges):
    m = [[0] * n for _ in range(n)]
    for u, v in edges:
        if u != v:
            m[u][v] = m[v][u] = 1
    return f"{n} {k} {s}\n" + "\n".join(" ".join(map(str, row)) for row in m) + "\n"

def _random_graph(r, n, p):
    return [(i, j) for i in range(n) for j in range(i + 1, n) if r.random() < p]

def _relabel(r, n, k, s, edges):
    perm = list(range(n)); r.shuffle(perm)
    return n, perm[k], perm[s], [(perm[u], perm[v]) for u, v in edges]

def _path(n):
    return [(i, i + 1) for i in range(n - 1)]

def _cycle(n):
    return _path(n) + [(n - 1, 0)]

def _grid(a, b):
    e = []
    for i in range(a):
        for j in range(b):
            x = i * b + j
            if j + 1 < b: e.append((x, x + 1))
            if i + 1 < a: e.append((x, x + b))
    return e

def _bipartite(r, a, b, p):
    return [(i, a + j) for i in range(a) for j in range(b) if r.random() < p]

def g30022(r):
    # 旧版随机图（逐格独立取 0/1，矩阵不对称），仅保留函数名；新数据见 build_cases()
    n = r.randint(2, 45); k, s = r.sample(range(n), 2)
    return _fmt(n, k, s, _random_graph(r, n, .35))

def build_cases():
    r = random.Random(30022)
    cases = [SAMPLE, '2 0 1\n0 1\n1 0\n', '2 1 1\n0 1\n1 0\n']
    cases.append('1 0 0\n0\n')                                   # n=1，最小规模
    cases.append(_fmt(3, 0, 2, []))                              # 无边，k≠s → -1
    cases.append(_fmt(4, 2, 2, []))                              # 无边，k=s → 0
    cases.append(_fmt(*_relabel(r, 9, 0, 8, _path(9))))          # 路径偶距离 → 4
    cases.append(_fmt(*_relabel(r, 10, 0, 9, _path(10))))        # 路径奇距离 → -1
    cases.append(_fmt(*_relabel(r, 7, 0, 3, _cycle(7))))         # 奇环：两条路径
    cases.append(_fmt(*_relabel(r, 8, 0, 3, _cycle(8))))         # 偶环奇距离 → -1
    # 陷阱：两人都到不了的点 d1=d2=-1，同时存在真正的会合点
    e = _path(5) + [(5, 6), (6, 7)]
    cases.append(_fmt(*_relabel(r, 8, 0, 4, e)))
    e = _path(6) + [(6, 7)]                                       # 奇距离且有两人都到不了的点 → -1
    cases.append(_fmt(*_relabel(r, 8, 0, 5, e)))
    # k、s 不连通，但各自分量里有别的点
    cases.append(_fmt(*_relabel(r, 12, 0, 6, _random_graph(random.Random(1), 6, .6) + [(6 + u, 6 + v) for u, v in _random_graph(random.Random(2), 6, .6)])))
    # 网格（二分图）：曼哈顿距离偶 / 奇
    cases.append(_fmt(*_relabel(r, 30, 0, 29, _grid(5, 6))))       # 距离 9 奇 → -1
    cases.append(_fmt(*_relabel(r, 30, 0, 28, _grid(5, 6))))       # 距离 8 → 4
    # 小规模随机（含 k=s、不连通、稠密、稀疏）
    for t in range(12):
        n = r.randint(2, 40); p = r.choice([.03, .06, .1, .2, .5])
        k = r.randrange(n); s = k if t % 7 == 0 else r.choice([x for x in range(n) if x != k])
        cases.append(_fmt(n, k, s, _random_graph(r, n, p)))
    # 中等规模二分图：大概率 -1
    a, b = 60, 70
    E = _bipartite(r, a, b, .05)
    cases.append(_fmt(*_relabel(r, a + b, 0, a, E)))
    cases.append(_fmt(*_relabel(r, a + b, 0, 1, E)))
    # 大规模：只保留 3 组 n=700（.in 约 0.98MB）真正压满读入与 O(n^2) BFS，其余用 n=350 控制总体积 ≤ 10MB
    N = 700; M = 350
    cases.append(_fmt(*_relabel(r, M, 0, M - 1, _path(M))))       # 长路径距离 349 奇 → -1
    cases.append(_fmt(*_relabel(r, N, 0, N - 2, _path(N))))       # 满规模：长路径 698 → 349（BFS 层数最深）
    cases.append(_fmt(*_relabel(r, M, 0, M // 2, _cycle(M - 1)))) # 奇环
    cases.append(_fmt(*_relabel(r, M, 3, 3, _random_graph(r, M, .02))))  # k=s
    for p in (.006, .012, .04):
        k, s = r.sample(range(M), 2)
        cases.append(_fmt(M, k, s, _random_graph(r, M, p)))
    k, s = r.sample(range(N), 2)
    cases.append(_fmt(N, k, s, _random_graph(r, N, .3)))           # 满规模稠密随机图
    # 网格 + 少量孤立点（二分图）
    e = _grid(20, 30)
    cases.append(_fmt(*_relabel(r, N, 0, 599, e)))                 # 满规模：距离 19+29=48 → 24
    e = _grid(15, 20)
    cases.append(_fmt(*_relabel(r, M, 0, 298, e)))                 # 距离 14+18=32 → 16
    # 两个大分量，k、s 分属不同分量
    h = M // 2
    e = [(u, v) for u, v in _random_graph(r, h, .04)] + [(h + u, h + v) for u, v in _random_graph(r, h, .04)]
    cases.append(_fmt(*_relabel(r, M, 0, h, e)))
    assert len(cases) == 40, len(cases)   # catalog.json 登记了 0..39 共 40 组
    return cases

from pathlib import Path
import random, subprocess, sys, tempfile
REFERENCE = REFERENCE
def solve(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        result=subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=build_cases()
    assert all(valid(c) for c in cases)
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()
