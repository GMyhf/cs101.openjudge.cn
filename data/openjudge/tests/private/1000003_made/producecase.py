#!/usr/bin/env python3
"""1000003 论文投稿前的关键路径：确定性造数据。

答案由 oracle() 计算：迭代 DFS 判环并求最长路（与参考实现的 Kahn 拓扑排序是不同算法），
最迟开始时间同样用 DFS 后序在反向依赖上求。第 0 组是题面样例，build() 里逐字断言。
"""
import random
from pathlib import Path

SAMPLE_IN = """8 9
2 1 5 3 4 6 3 2
1 3
2 3
3 4
3 5
2 6
4 7
5 7
6 7
7 8
"""
SAMPLE_OUT = "16\n1 3 5 7 8\n"


def valid(text):
    """照题面：1≤n≤10000，0≤m≤50000，1≤t≤1000，1≤u,v≤n，u≠v，(u,v) 不重复；行数与字段数严格。"""
    lines = text.split('\n')
    if lines and lines[-1] == '':
        lines.pop()
    try:
        head = lines[0].split()
        if len(head) != 2:
            return False
        n, m = int(head[0]), int(head[1])
        if not (1 <= n <= 10000 and 0 <= m <= 50000) or len(lines) != 2 + m:
            return False
        t = lines[1].split()
        if len(t) != n or not all(1 <= int(x) <= 1000 for x in t):
            return False
        seen = set()
        for line in lines[2:]:
            p = line.split()
            if len(p) != 2:
                return False
            u, v = int(p[0]), int(p[1])
            if not (1 <= u <= n and 1 <= v <= n) or u == v or (u, v) in seen:
                return False
            seen.add((u, v))
    except (ValueError, IndexError):
        return False
    return True


def oracle(n, t, edges):
    succ = [[] for _ in range(n + 1)]
    for u, v in edges:
        succ[u].append(v)
    # 后序 DFS：白 0 / 灰 1 / 黑 2，遇到灰点即有环；ef[u] 先算后继的“最早完成依赖”，再反推
    color = [0] * (n + 1)
    post = []
    for s in range(1, n + 1):
        if color[s]:
            continue
        stack = [(s, 0)]
        color[s] = 1
        while stack:
            u, k = stack[-1]
            if k < len(succ[u]):
                stack[-1] = (u, k + 1)
                v = succ[u][k]
                if color[v] == 1:
                    return "-1\n"
                if color[v] == 0:
                    color[v] = 1
                    stack.append((v, 0))
            else:
                color[u] = 2
                post.append(u)
                stack.pop()
    topo = post[::-1]
    es = [0] * (n + 1)
    for u in topo:
        for v in succ[u]:
            if es[u] + t[u] > es[v]:
                es[v] = es[u] + t[u]
    total = max(es[i] + t[i] for i in range(1, n + 1))
    # 后序本身就是“后继先于前驱”的顺序：ls[u] = min(后继 ls) − t[u]，无后继时 total − t[u]
    ls = [0] * (n + 1)
    for u in post:
        lf = min((ls[v] for v in succ[u]), default=total)
        ls[u] = lf - t[u]
    crit = [i for i in range(1, n + 1) if es[i] == ls[i]]
    return f"{total}\n{' '.join(map(str, crit))}\n"


def render(n, t, edges):
    return f"{n} {len(edges)}\n{' '.join(map(str, t[1:]))}\n" + ''.join(f"{u} {v}\n" for u, v in edges)


def relabel(n, t, edges, rng):
    """打乱编号与边序，避免“编号小的先做”之类的假设。"""
    perm = list(range(1, n + 1))
    rng.shuffle(perm)
    mp = {i + 1: perm[i] for i in range(n)}
    nt = [0] * (n + 1)
    for i in range(1, n + 1):
        nt[mp[i]] = t[i]
    ne = [(mp[u], mp[v]) for u, v in edges]
    rng.shuffle(ne)
    return n, nt, ne


def random_dag(rng, n, m, tmax):
    order = list(range(1, n + 1))
    rng.shuffle(order)
    rank = {v: i for i, v in enumerate(order)}
    edges = set()
    while len(edges) < m:
        a, b = rng.sample(range(1, n + 1), 2)
        if rank[a] > rank[b]:
            a, b = b, a
        edges.add((a, b))
    t = [0] + [rng.randint(1, tmax) for _ in range(n)]
    return n, t, sorted(edges, key=lambda e: rng.random())


def cases():
    rng = random.Random(1000003)
    yield SAMPLE_IN
    yield render(1, [0, 7], [])                                            # 单任务
    yield render(2, [0, 3, 5], [])                                         # 无依赖、长者关键
    yield render(10, [0] + [4] * 10, [])                                   # 全部并列关键
    # 小环：1→2→1，外加一条正常链
    yield render(5, [0, 1, 2, 3, 4, 5], [(1, 2), (2, 1), (3, 4), (4, 5)])
    # 深链 10000（递归 DFS 会爆栈）
    n = 10000
    yield render(n, [0] + [rng.randint(1, 1000) for _ in range(n)], [(i, i + 1) for i in range(1, n)])
    # 菱形两支等长：两支都关键
    yield render(6, [0, 2, 3, 4, 5, 2, 1], [(1, 2), (1, 4), (2, 3), (4, 5), (3, 6), (5, 6)])
    # 网格 DAG，单位耗时：大量等长路径
    side = 40
    ids = lambda r, c: r * side + c + 1
    edges = [(ids(r, c), ids(r + 1, c)) for r in range(side - 1) for c in range(side)]
    edges += [(ids(r, c), ids(r, c + 1)) for r in range(side) for c in range(side - 1)]
    yield render(*relabel(side * side, [0] + [1] * (side * side), edges, rng))
    # 大 DAG 里藏一个长度 500 的环
    n, t, e = random_dag(rng, 8000, 30000, 1000)
    cyc = rng.sample(range(1, n + 1), 500)
    extra = [(cyc[i], cyc[(i + 1) % 500]) for i in range(500)]
    es = set(e)
    yield render(n, t, list(dict.fromkeys(e + [x for x in extra if x not in es])))
    # 环在一个孤立分量里，其余是正常 DAG
    n, t, e = random_dag(rng, 3000, 6000, 50)
    yield render(n + 3, t + [3, 3, 3], e + [(n + 1, n + 2), (n + 2, n + 3), (n + 3, n + 1)])
    # 孤立任务 + 一条长链
    chain = 300
    t = [0] + [5] * chain + [rng.randint(1, 900) for _ in range(500)]
    yield render(*relabel(chain + 500, t, [(i, i + 1) for i in range(1, chain)], rng))
    # 星形：一个源点通向许多汇点，其中几个汇点最长且并列
    k = 2000
    t = [0, 10] + [rng.randint(1, 500) for _ in range(k)]
    for j in rng.sample(range(2, k + 2), 7):
        t[j] = 999
    yield render(*relabel(k + 1, t, [(1, j) for j in range(2, k + 2)], rng))
    # 最大规模随机 DAG
    yield render(*random_dag(rng, 10000, 50000, 1000))
    # 最大规模、全部耗时 1：大量并列
    yield render(*random_dag(rng, 10000, 50000, 1))
    # 稀疏随机 DAG
    yield render(*random_dag(rng, 5000, 6000, 100))
    # 边按逆拓扑序给出（u 大 v 小居多）
    n = 6000
    order = list(range(n, 0, -1))
    e = set()
    while len(e) < 20000:
        a, b = sorted(rng.sample(range(n), 2))
        e.add((order[a], order[b]))
    yield render(n, [0] + [rng.randint(1, 300) for _ in range(n)], list(e))
    # 中等随机 DAG，耗时差异大：许多任务有后继空闲（样例的第 2 号任务就是这种情形）
    n, t, e = random_dag(rng, 2000, 5000, 1000)
    yield render(n, t, e)
    # 中等随机 DAG，再加一条回边成环
    n, t, e = random_dag(rng, 4000, 12000, 200)
    u, v = e[0]
    yield render(n, t, e + [(v, u)])
    # 无依赖 10000 个任务，最大值唯一
    t = [0] + [rng.randint(1, 999) for _ in range(10000)]
    t[rng.randint(1, 10000)] = 1000
    yield render(10000, t, [])
    # 两个大分量，各有自己的最长路，一长一短
    n1, t1, e1 = random_dag(rng, 3000, 9000, 100)
    n2, t2, e2 = random_dag(rng, 3000, 9000, 120)
    yield render(n1 + n2, t1 + t2[1:], e1 + [(u + n1, v + n1) for u, v in e2])
    # 最大规模、耗时全取 1000：总工期接近上界
    n, _, e = random_dag(rng, 10000, 50000, 1)
    yield render(n, [0] + [1000] * n, e)


def parse(text):
    a = list(map(int, text.split()))
    n, m = a[0], a[1]
    t = [0] + a[2:2 + n]
    e = [(a[2 + n + 2 * i], a[3 + n + 2 * i]) for i in range(m)]
    return n, t, e


def build():
    data = Path(__file__).parent / 'data'
    data.mkdir(exist_ok=True)
    seen = set()
    for index, text in enumerate(cases()):
        assert valid(text), index
        assert text not in seen, index
        seen.add(text)
        answer = oracle(*parse(text))
        if index == 0:
            assert text == SAMPLE_IN and answer == SAMPLE_OUT, answer
        (data / f'{index}.in').write_text(text, encoding='utf-8')
        (data / f'{index}.out').write_text(answer, encoding='utf-8')
    assert len(seen) == 21, len(seen)
    print(f'generated {len(seen)} cases')


if __name__ == '__main__':
    build()
