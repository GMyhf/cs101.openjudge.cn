"""04011 Chase 测试数据生成器：固定种子，重跑可逐字节复现 data/。

答案由同目录 samplecode_ac.cpp 编译后给出；生成时另用 Python 版同一 DP 算出高精度值，
落在四舍五入边界附近（距 xx.xx5 不到 1e-6 个百分点）的组换种子重抽，免得浮点误差左右答案。

题面约束（原页 HTML 里的完整版，镜像纯文本被 `<N` 吃掉了一段）：
N<=100，M<=10000；每条路 a b c，0<=a,b<N，0<c<=10000，可以有重边和自环；
从 0 到任何点的最短路唯一；0<P<=50；PT 为 N 行、每行 P 个 [0,1] 内的实数（PT(i,1..P)）；以 "0 0" 结束。

PT 一律按 j 单调不减生成：题面说「all agents are deployed」，若 PT 不单调，
「恰好派完 P 人」和「至多派 P 人」（AC 代码做了前缀 max）两种读法答案会不同；单调时两者一致。
"""
import heapq
import random
import re
import subprocess
import tempfile
from pathlib import Path

SAMPLE_IN = '4 4\n0 1 1\n0 2 2\n1 3 3\n2 3 1\n2\n0.01 0.1\n0.5 0.8\n0.5 0.8\n0.7 0.9\n0 0\n'
SAMPLE_OUT = '60.00\n'
REAL = re.compile(r"\d+(\.\d+)?")


def _dijkstra(n, edges):
    adj = [[] for _ in range(n)]
    for a, b, c in edges:
        adj[a].append((b, c))
        adj[b].append((a, c))
    dist = [None] * n
    dist[0] = 0
    pq = [(0, 0)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, w in adj[u]:
            if dist[v] is None or d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (d + w, v))
    return dist


def valid(text):
    """题面契约：多组，每组 N M / M 行 a b c / P / N 行各 P 个实数，以 "0 0" 结束；
    0<N<=100，0<=M<=10000，0<=a,b<N，0<c<=10000，0<P<=50，0<=PT<=1；
    结构保证：从 0 到每个点都有且只有一条最短路（重边里并列最短也算两条）。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    p = 0
    groups = 0

    def ints(line, cnt):
        toks = line.split(" ")
        if len(toks) != cnt or not all(t.isdigit() and (t == "0" or t[0] != "0") for t in toks):
            return None
        return list(map(int, toks))

    while True:
        if p >= len(lines):
            return False
        head = ints(lines[p], 2)
        p += 1
        if head is None:
            return False
        n, m = head
        if n == 0 and m == 0:
            break
        if not (1 <= n <= 100 and 0 <= m <= 10000) or p + m + 1 + n > len(lines):
            return False
        edges = []
        for line in lines[p:p + m]:
            e = ints(line, 3)
            if e is None or not (e[0] < n and e[1] < n and 1 <= e[2] <= 10000):
                return False
            edges.append(tuple(e))
        p += m
        pl = ints(lines[p], 1)
        p += 1
        if pl is None or not 1 <= pl[0] <= 50:
            return False
        for line in lines[p:p + n]:
            toks = line.split(" ")
            if len(toks) != pl[0] or not all(REAL.fullmatch(t) and float(t) <= 1 for t in toks):
                return False
        p += n
        dist = _dijkstra(n, edges)
        if any(d is None for d in dist):
            return False
        tight = [0] * n
        for a, b, c in edges:
            if a != b:
                if dist[a] + c == dist[b]:
                    tight[b] += 1
                if dist[b] + c == dist[a]:
                    tight[a] += 1
        if tight[0] != 0 or any(t != 1 for t in tight[1:]):
            return False
        groups += 1
    return p == len(lines) and groups >= 1


def solve_float(text):
    """与 AC 代码同一 DP 的 Python 版，返回每组的百分数（不舍入），只用来查舍入边界。"""
    a = text.split()
    p = 0
    res = []
    while True:
        n, m = int(a[p]), int(a[p + 1]); p += 2
        if n == 0 and m == 0:
            return res
        edges = [tuple(map(int, a[p + 3 * i:p + 3 * i + 3])) for i in range(m)]; p += 3 * m
        P = int(a[p]); p += 1
        pt = []
        for i in range(n):
            row = [0.0] + [float(x) for x in a[p:p + P]]; p += P
            for j in range(1, P + 1):
                row[j] = max(row[j], row[j - 1])
            pt.append(row)
        dist = _dijkstra(n, edges)
        ch = [[] for _ in range(n)]
        for x, y, c in edges:
            if x != y:
                if dist[x] + c == dist[y]:
                    ch[x].append(y)
                if dist[y] + c == dist[x]:
                    ch[y].append(x)
        f = [None] * n
        for u in sorted(range(n), key=lambda v: -dist[v]):
            if not ch[u]:
                f[u] = pt[u][:]
                continue
            g = [0.0] + [-1.0] * P
            for v in ch[u]:
                ng = [-1.0] * (P + 1)
                for used in range(P + 1):
                    if g[used] < 0:
                        continue
                    for add in range(P + 1 - used):
                        s = g[used] + f[v][add]
                        if s > ng[used + add]:
                            ng[used + add] = s
                g = ng
            d = len(ch[u])
            f[u] = [max(pt[u][k] + (1 - pt[u][k]) * g[q - k] / d for k in range(q + 1)) for q in range(P + 1)]
        res.append(f[0][P] * 100)


def safe(text):
    for v in solve_float(text):
        frac = (v * 100) % 1
        if abs(frac - 0.5) < 1e-6:
            return False
    return True


def make_tree(r, n, shape):
    """返回以 0 为根的树的父亲数组（标号已打乱，0 固定为根）。"""
    order = list(range(1, n))
    r.shuffle(order)
    order = [0] + order
    par = [None] * n
    for idx in range(1, n):
        if shape == "path":
            pi = idx - 1
        elif shape == "star":
            pi = 0
        elif shape == "binary":
            pi = (idx - 1) // 2
        elif shape == "caterpillar":
            spine = max(1, n // 4)
            pi = idx - 1 if idx < spine else r.randrange(spine)
        elif shape == "deep":
            pi = r.randrange(max(0, idx - 3), idx)
        else:
            pi = r.randrange(idx)
        par[order[idx]] = order[pi]
    return par


def make_group(r, n, extra, P, shape, wmax=1000, digits=2):
    par = make_tree(r, n, shape)
    dist = [0] * n
    # 按父亲先于儿子的次序求深度距离
    done = {0}
    tree = []
    pending = [v for v in range(1, n)]
    w = {}
    while pending:
        rest = []
        for v in pending:
            if par[v] in done:
                w[v] = r.randint(1, wmax)
                dist[v] = dist[par[v]] + w[v]
                done.add(v)
                tree.append((par[v], v, w[v]))
            else:
                rest.append(v)
        pending = rest
    edges = []
    for a, b, c in tree:
        edges.append((a, b, c) if r.random() < 0.5 else (b, a, c))
    tries = 0
    while len(edges) < n - 1 + extra and tries < extra * 20:
        tries += 1
        kind = r.random()
        if kind < 0.08:
            a = r.randrange(n)
            edges.append((a, a, r.randint(1, 10000)))       # 自环
            continue
        if kind < 0.2 and tree:
            a, b, c = r.choice(tree)                         # 重边：比树边长
        else:
            a, b = r.randrange(n), r.randrange(n)
            if a == b:
                continue
        lo = abs(dist[a] - dist[b]) + 1
        if lo > 10000:
            continue
        c = r.randint(lo, min(10000, lo + r.choice([0, 1, 5, 100, 10000])))
        edges.append((a, b, c) if r.random() < 0.5 else (b, a, c))
    r.shuffle(edges)
    rows = []
    for _ in range(n):
        kind = r.random()
        if kind < 0.08:
            vals = [0.0] * P
        elif kind < 0.11:
            vals = [1.0] * P
        elif kind < 0.3:
            # 第一个人就有一定概率、之后增长很慢（边际收益递减，逼着把人分散到各点）
            base = r.random() * 0.6
            vals = [min(1.0, base + 0.01 * j * r.random()) for j in range(P)]
        else:
            # 每个点有自己的上限，P 很大时也不会「全堆在起点就接近 100%」
            cap = r.uniform(0.05, 0.85)
            vals = sorted(r.random() * cap for _ in range(P))
        q = 10 ** digits
        vals = [int(v * q) / q for v in vals]
        vals = [max(vals[:j + 1]) for j in range(P)]
        rows.append(" ".join(f"{v:.{digits}f}" for v in vals))
    lines = [f"{n} {len(edges)}"] + [f"{a} {b} {c}" for a, b, c in edges] + [str(P)] + rows
    return "\n".join(lines) + "\n"


def make_case(r, specs):
    while True:
        text = "".join(make_group(r, *s) for s in specs) + "0 0\n"
        if safe(text):
            return text


def build_cases():
    r = random.Random(40110)
    shapes = ["random", "path", "star", "binary", "caterpillar", "deep"]
    cases = [SAMPLE_IN]
    # 小规模：多组拼在一起，便于暴力核对
    for i in range(17):
        specs = [(r.randint(1, 7), r.randint(0, 6), r.randint(1, 4), r.choice(shapes)) for _ in range(r.randint(1, 4))]
        cases.append(make_case(r, specs))
    # 中等规模
    for i in range(12):
        specs = [(r.randint(10, 60), r.randint(0, 300), r.randint(1, 50), shapes[i % len(shapes)], 1000, r.choice([2, 3, 4]))
                 for _ in range(r.randint(1, 3))]
        cases.append(make_case(r, specs))
    # 满规模：N=100，M 取到 10000，P=50
    for shape in shapes:
        cases.append(make_case(r, [(100, 10000 - 99, 50, shape, 90 if shape in ("path", "deep") else 1000, 3)]))
    cases.append(make_case(r, [(100, 0, 50, "random"), (100, 500, 50, "binary"), (100, 9901, 1, "star")]))
    # 边界：N=1、P=1、全 0 概率、单点自环
    cases.append("1 0\n1\n0.50\n0 0\n")
    cases.append("1 2\n0 0 5\n0 0 10000\n3\n0.00 0.00 0.00\n2 2\n0 1 7\n1 0 9\n1\n0.00\n1.00\n0 0\n")
    cases.append(make_case(r, [(100, 2000, 1, "random"), (2, 0, 50, "path")]))
    return cases


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN
    assert len(set(cases)) == len(cases)
    root = Path(__file__).parent
    with tempfile.TemporaryDirectory() as folder:
        binary = Path(folder) / "reference"
        subprocess.run(["g++", "-std=c++17", "-O2", str(root / "samplecode_ac.cpp"), "-o", str(binary)], check=True)
        for i, c in enumerate(cases):
            assert valid(c), i
            p = subprocess.run([str(binary)], input=c, text=True, capture_output=True, check=True)
            if i == 0:
                assert p.stdout == SAMPLE_OUT
            (root / "data" / f"{i}.in").write_text(c)
            (root / "data" / f"{i}.out").write_text(p.stdout)


if __name__ == "__main__":
    main()
