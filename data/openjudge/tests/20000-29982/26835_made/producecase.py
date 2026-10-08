# 26835 团结真的就是力量：最小生成树，输出总花费（两位小数）与按花费升序的边；不连通输出 NOT CONNECTED。
# 约束：0<n<100，0<m<5000，0<=w<100000，每对花费互不相同。
# 生成器额外保证：无自环、无重边、n>=2（n=1 时 m>=1 只能是自环）；
# 权值至多三位小数，且总花费的精确值不落在 .xx5 上，避免两位小数舍入方向的歧义。
import random
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAMPLE = '5 9\n0 1 10.0\n0 3 7.0\n0 4 25.0\n1 2 8.0\n1 3 9.0\n1 4 35.0\n2 3 11.0\n2 4 50.0\n3 4 24.0\n'


def _num_ok(tok):
    # 非负十进制数，可带小数部分
    if tok.count('.') > 1 or not tok:
        return False
    a, _, b = tok.partition('.')
    if not a.isdigit():
        return False
    if '.' in tok and not b.isdigit():
        return False
    return True


def valid(text):
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    head = lines[0].split(' ')
    if len(head) != 2 or not all(x.isdigit() for x in head):
        return False
    n, m = map(int, head)
    if not (0 < n < 100 and 0 < m < 5000):
        return False
    if len(lines) != m + 1:
        return False
    pairs, ws = set(), set()
    for ln in lines[1:]:
        p = ln.split(' ')
        if len(p) != 3 or not p[0].isdigit() or not p[1].isdigit() or not _num_ok(p[2]):
            return False
        s, e = int(p[0]), int(p[1])
        w = Decimal(p[2])
        if not (0 <= s < n and 0 <= e < n) or s == e:
            return False
        if not (0 <= w < 100000):
            return False
        key = (min(s, e), max(s, e))
        if key in pairs or w in ws:
            return False
        pairs.add(key)
        ws.add(w)
    return True


def mst_exact(text):
    """Prim（与参考解的 Kruskal 不同算法），用 Decimal 精确求和；返回 (总和 Decimal 或 None, 边列表)。"""
    lines = text.split('\n')
    n, m = map(int, lines[0].split())
    INF = None
    g = {}
    for ln in lines[1:m + 1]:
        s, e, w = ln.split()
        s, e, w = int(s), int(e), Decimal(w)
        g[(s, e)] = w
        g[(e, s)] = w
    intree = [False] * n
    best = [INF] * n
    frm = [-1] * n
    best[0] = Decimal(0)
    chosen = []
    total = Decimal(0)
    for _ in range(n):
        u = -1
        for v in range(n):
            if not intree[v] and best[v] is not None and (u == -1 or best[v] < best[u]):
                u = v
        if u == -1:
            return None, []
        intree[u] = True
        if frm[u] != -1:
            total += best[u]
            chosen.append((best[u], min(u, frm[u]), max(u, frm[u])))
        for v in range(n):
            w = g.get((u, v))
            if w is not None and not intree[v] and (best[v] is None or w < best[v]):
                best[v] = w
                frm[v] = u
    chosen.sort()
    return total, [(a, b) for _, a, b in chosen]


def tie(text):
    total, _ = mst_exact(text)
    if total is None:
        return False
    return (total * 1000) % 10 == 5


def fmt(w, style):
    if style == 0:
        return f'{w / 1000:.3f}'
    if style == 1:
        return f'{w // 1000}.0'
    return f'{w // 1000}'


def graph(r, n, pair_list, style, wmax=99999999):
    # 权值以千分之一为单位，取互不相同的整数
    ws = r.sample(range(0, wmax + 1, 1 if style == 0 else 1000), len(pair_list))
    lines = []
    for (a, b), w in zip(pair_list, ws):
        if r.random() < 0.5:
            a, b = b, a
        lines.append(f'{a} {b} {fmt(w, style)}')
    r.shuffle(lines)
    return f'{n} {len(lines)}\n' + '\n'.join(lines) + '\n'


def complete_pairs(nodes):
    return [(a, b) for i, a in enumerate(nodes) for b in nodes[i + 1:]]


def random_connected_pairs(r, n, m):
    perm = list(range(n))
    r.shuffle(perm)
    pairs = set()
    for i in range(1, n):
        a, b = perm[i], perm[r.randrange(i)]
        pairs.add((min(a, b), max(a, b)))
    allp = complete_pairs(list(range(n)))
    r.shuffle(allp)
    for p in allp:
        if len(pairs) >= m:
            break
        pairs.add(p)
    return list(pairs)


def no_tie(r, make):
    while True:
        t = make(r)
        if not tie(t):
            return t


def build_cases():
    r = random.Random(26835)
    cases = [SAMPLE]
    # 满规模：n=99、完全图 4851 条边
    cases.append(no_tie(r, lambda r: graph(r, 99, complete_pairs(list(range(99))), 0)))
    cases.append(no_tie(r, lambda r: graph(r, 99, complete_pairs(list(range(99))), 2)))
    # 满规模但不连通：两块完全图 / 一个孤立点
    nodes = list(range(99))
    r.shuffle(nodes)
    cases.append(graph(r, 99, complete_pairs(nodes[:50]) + complete_pairs(nodes[50:]), 0))
    cases.append(graph(r, 99, complete_pairs(nodes[:98]), 1))
    # 一条链（树），n=99
    chain = list(range(99))
    r.shuffle(chain)
    cases.append(no_tie(r, lambda r: graph(r, 99, [(chain[i], chain[i + 1]) for i in range(98)], 0)))
    # 边界
    cases.append('2 1\n0 1 0.0\n')
    cases.append('2 1\n1 0 99999.999\n')
    cases.append('3 1\n0 1 5.5\n')                       # NOT CONNECTED
    cases.append('3 2\n2 1 3\n0 2 4.25\n')
    cases.append('3 3\n0 1 1.0\n1 2 2.0\n0 2 3.0\n')
    cases.append('4 2\n0 1 1.0\n2 3 2.0\n')              # 两块、NOT CONNECTED
    cases.append('4 6\n0 1 0.001\n0 2 0.002\n0 3 0.003\n1 2 99999.997\n1 3 99999.998\n2 3 99999.999\n')
    # 中等随机：连通 / 不连通，三种权值格式
    for i in range(30):
        n = r.randint(2, [8, 30, 99][i % 3])
        maxm = n * (n - 1) // 2
        style = (i // 3) % 3
        if i % 5 == 4 and n >= 3:
            k = r.randint(1, n - 1)
            nodes = list(range(n))
            r.shuffle(nodes)
            A, B = nodes[:k], nodes[k:]
            pa = complete_pairs(A)
            pb = complete_pairs(B)
            r.shuffle(pa)
            r.shuffle(pb)
            pl = pa[:r.randint(0, len(pa))] + pb[:r.randint(0, len(pb))]
            if not pl:
                pl = [tuple(sorted((A[0], B[0])))]
                # 只有这一条边时恰好连通两块；若 n>2 仍不连通
            cases.append(no_tie(r, lambda r, pl=pl, n=n, s=style: graph(r, n, pl, s)))
        else:
            m = r.randint(n - 1, min(maxm, 4999))
            pl = random_connected_pairs(r, n, m)
            cases.append(no_tie(r, lambda r, pl=pl, n=n, s=style: graph(r, n, pl, s)))
    return cases


def run_ref(text):
    x = subprocess.run([sys.executable, str(HERE / 'samplecode.py')], input=text,
                       text=True, capture_output=True, timeout=120)
    if x.returncode:
        raise SystemExit(x.stderr)
    return x.stdout


def expected(text):
    total, edges = mst_exact(text)
    if total is None:
        return 'NOT CONNECTED\n'
    return f'{total:.2f}\n' + ''.join(f'{a} {b}\n' for a, b in edges)


def main():
    cases = build_cases()
    assert len(set(cases)) == len(cases), '存在重复组'
    d = HERE / 'data'
    d.mkdir(exist_ok=True)
    for i, c in enumerate(cases):
        assert valid(c), f'第 {i} 组不合法'
        assert not tie(c), f'第 {i} 组总和落在舍入边界'
        out = run_ref(c)
        assert out == expected(c), f'第 {i} 组参考解与 Prim 精确解不一致'
        (d / f'{i}.in').write_text(c)
        (d / f'{i}.out').write_text(out)


if __name__ == '__main__':
    main()
