# 28327 相遇地点 测试数据生成器
# 用法：在本目录下 python3 producecase.py；答案由同目录 samplecode.py 生成。
import random
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAMPLE = '4\n1 2\n2 3\n2 4\n1\n1 2\n'
SAMPLE2 = '5\n1 2\n2 3\n3 4\n4 5\n2\n1 3\n1 5\n'
SAMPLE3 = ('9\n2 3\n5 6\n4 8\n8 9\n4 5\n3 4\n1 9\n3 7\n9\n7 9\n2 5\n2 6\n4 6\n2 4\n'
           '5 8\n7 8\n3 6\n5 6\n')


def valid(text):
    """严格照题面核输入：2<=N<=2000；N-1 条边 1<=a<b<=N 且构成一棵树；
    1<=Q<=2000；每个询问 1<=c,d<=N 且 c!=d。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    num = r'[1-9]\d*'
    if not re.fullmatch(num, lines[0]):
        return False
    n = int(lines[0])
    if not 2 <= n <= 2000 or len(lines) < n + 1:
        return False
    parent = list(range(n + 1))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for row in lines[1:n]:
        m = re.fullmatch(rf'({num}) ({num})', row)
        if not m:
            return False
        a, b = int(m[1]), int(m[2])
        if not 1 <= a < b <= n:
            return False
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        parent[ra] = rb
    if not re.fullmatch(num, lines[n]):
        return False
    q = int(lines[n])
    if not 1 <= q <= 2000 or len(lines) != n + 1 + q:
        return False
    for row in lines[n + 1:]:
        m = re.fullmatch(rf'({num}) ({num})', row)
        if not m:
            return False
        c, d = int(m[1]), int(m[2])
        if not (1 <= c <= n and 1 <= d <= n and c != d):
            return False
    return True


def build(n, edges, queries, r, relabel=True):
    """edges 用 0..n-1 的结构编号；relabel 时随机重新编号。边一律输出 (小, 大)。"""
    perm = list(range(1, n + 1))
    if relabel:
        r.shuffle(perm)
    es = [tuple(sorted((perm[u], perm[v]))) for u, v in edges]
    r.shuffle(es)
    qs = [(perm[c], perm[d]) for c, d in queries]
    return (f'{n}\n' + ''.join(f'{a} {b}\n' for a, b in es) + f'{len(qs)}\n'
            + ''.join(f'{c} {d}\n' for c, d in qs))


def rand_queries(r, n, q):
    return [tuple(r.sample(range(n), 2)) for _ in range(q)]


def tree_random(r, n):
    return [(i, r.randrange(i)) for i in range(1, n)]


def tree_chain(n):
    return [(i, i - 1) for i in range(1, n)]


def tree_star(n):
    return [(i, 0) for i in range(1, n)]


def tree_binary(n):
    return [(i, (i - 1) // 2) for i in range(1, n)]


def tree_caterpillar(r, n, spine):
    return [(i, i - 1) for i in range(1, spine)] + [(i, r.randrange(spine)) for i in range(spine, n)]


def tree_deep(r, n, window):
    """父亲取最近 window 个点之一，树很深。"""
    return [(i, r.randrange(max(0, i - window), i)) for i in range(1, n)]


def tree_broom(n, handle):
    """长柄扫帚：前 handle 个点成链，其余挂在链尾。"""
    return [(i, i - 1) for i in range(1, handle)] + [(i, handle - 1) for i in range(handle, n)]


def cases():
    r = random.Random(28327)
    out = [SAMPLE, SAMPLE2, SAMPLE3]
    # N=2 最小：两个方向都问
    out.append('2\n1 2\n2\n1 2\n2 1\n')
    # 30% 小数据：N,Q<=10
    for _ in range(4):
        n = r.randint(3, 10)
        out.append(build(n, tree_random(r, n), rand_queries(r, n, r.randint(1, 10)), r))
    out.append(build(10, tree_chain(10), [(c, d) for c in range(10) for d in range(10) if c != d][:10], r, relabel=False))
    # 中等规模
    for _ in range(3):
        n = r.randint(50, 300)
        out.append(build(n, tree_random(r, n), rand_queries(r, n, r.randint(50, 300)), r))
    # 满规模：链（编号顺序，递归 DFS 会爆栈），询问两端附近，距离奇偶都有
    n = 2000
    qs = [(r.randrange(0, 20), r.randrange(n - 20, n)) for _ in range(2000)]
    qs = [(c, d) if i % 2 else (d, c) for i, (c, d) in enumerate(qs)]
    out.append(build(n, tree_chain(n), qs, r, relabel=False))
    # 满规模：链，随机编号
    out.append(build(n, tree_chain(n), rand_queries(r, n, 2000), r))
    # 满规模：长柄扫帚，询问柄端到扫帚头
    qs = [(r.randrange(0, 5), r.randrange(1500, n)) for _ in range(2000)]
    out.append(build(n, tree_broom(n, 1500), qs, r))
    # 满规模：深树
    out.append(build(n, tree_deep(r, n, 3), rand_queries(r, n, 2000), r))
    # 满规模：随机树
    out.append(build(n, tree_random(r, n), rand_queries(r, n, 2000), r))
    # 满规模：菊花（距离只有 1 和 2）
    out.append(build(n, tree_star(n), rand_queries(r, n, 2000), r))
    # 满规模：二叉树
    out.append(build(n, tree_binary(n), rand_queries(r, n, 2000), r))
    # 满规模：毛毛虫
    out.append(build(n, tree_caterpillar(r, n, 1000), rand_queries(r, n, 2000), r))
    # 相邻点询问（全是 Road）与距离 2 询问（全是 City）
    n = 1500
    es = tree_random(r, n)
    qs = [(u, v) if r.random() < .5 else (v, u) for u, v in r.sample(es, 1000)]
    out.append(build(n, es, qs, r))
    n = 1500
    es = tree_deep(r, n, 2)
    par = {u: v for u, v in es}
    qs = [(u, par[par[u]]) for u in range(n) if u in par and par[u] in par][:1500]
    out.append(build(n, es, qs, r))
    # 其余随机组，规模各异
    while len(out) < 30:
        n = r.randint(2, 2000)
        kind = r.randrange(4)
        if kind == 0:
            es = tree_random(r, n)
        elif kind == 1:
            es = tree_deep(r, n, r.randint(1, 10))
        elif kind == 2:
            es = tree_caterpillar(r, n, r.randint(1, n))
        else:
            es = tree_binary(n)
        out.append(build(n, es, rand_queries(r, n, r.randint(1, 2000)), r))
    return out


def run(text):
    x = subprocess.run([sys.executable, str(HERE / 'samplecode.py')], input=text,
                       text=True, capture_output=True, timeout=120)
    if x.returncode:
        raise SystemExit(x.stderr)
    return x.stdout


def main():
    d = HERE / 'data'
    d.mkdir(exist_ok=True)
    cs = cases()
    assert len(set(cs)) == len(cs), '组间重复'
    for i, c in enumerate(cs):
        assert valid(c), f'第 {i} 组不合法'
        (d / f'{i}.in').write_text(c)
        (d / f'{i}.out').write_text(run(c))


if __name__ == '__main__':
    main()
