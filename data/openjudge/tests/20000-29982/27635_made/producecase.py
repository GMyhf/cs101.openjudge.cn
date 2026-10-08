import random, re, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = '#王昊 光华管理学院\nn, m = list(map(int, input().split()))\nedge = [[]for _ in range(n)]\nfor _ in range(m):\n    a, b = list(map(int, input().split()))\n    edge[a].append(b)\n    edge[b].append(a)\ncnt, flag = set(), False\n\n\ndef dfs(x, y):\n    global cnt, flag\n    cnt.add(x)\n    for i in edge[x]:\n        if i not in cnt:\n            dfs(i, x)\n        elif y != i:\n            flag = True\n\n\nfor i in range(n):\n    cnt.clear()\n    dfs(i, -1)\n    if len(cnt) == n:\n        break\n    if flag:\n        break\n\nprint("connected:"+("yes" if len(cnt) == n else "no"))\nprint("loop:"+("yes" if flag else \'no\'))\n'
SAMPLE_IN = '3 2\n0 1\n0 2\n'
SAMPLE_OUT = 'connected:yes\nloop:no\n'
INT_LINE = re.compile(r"(0|[1-9][0-9]*) (0|[1-9][0-9]*)")


def valid(text):
    """题面：第一行 n m（1<=n<=110, 1<=m<=10000），接下来恰好 m 行，每行两个顶点编号 u v，编号在 0..n-1。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not lines or not INT_LINE.fullmatch(lines[0]):
        return False
    n, m = map(int, lines[0].split())
    if not (1 <= n <= 110 and 1 <= m <= 10000) or len(lines) != m + 1:
        return False
    for line in lines[1:]:
        if not INT_LINE.fullmatch(line):
            return False
        u, v = map(int, line.split())
        if not (u < n and v < n):
            return False
    return True


def random_tree(r, verts):
    """在给定顶点集上造随机生成树（随机父亲 / 链 / 菊花混合）。"""
    verts = verts[:]
    r.shuffle(verts)
    style = r.random()
    edges = []
    for i in range(1, len(verts)):
        if style < .2:
            p = i - 1                      # 长链
        elif style < .3:
            p = 0                          # 菊花
        else:
            p = r.randrange(i)
        edges.append((verts[i], verts[p]))
    return edges


def extra_edges(r, verts, k, allow_dup=True):
    out = []
    while len(out) < k:
        u, v = r.sample(verts, 2)
        out.append((u, v))
    return out


def emit(r, n, edges):
    edges = [(v, u) if r.random() < .5 else (u, v) for u, v in edges]
    r.shuffle(edges)
    assert 1 <= len(edges) <= 10000 and all(u != v for u, v in edges)
    return f"{n} {len(edges)}\n" + "".join(f"{u} {v}\n" for u, v in edges)


def components(r, n, sizes):
    """把 0..n-1 随机划分成若干块，sizes 为每块大小。"""
    perm = list(range(n)); r.shuffle(perm)
    out, at = [], 0
    for s in sizes:
        out.append(perm[at:at + s]); at += s
    assert at == n
    return out


def gen(r, kind):
    # 不出现自环（题面没说，n=1 时 m>=1 必须用自环，故 n 取 >=2），允许重边（m 上限 10000 超过 110 点简单图的边数）
    if kind == "tree":                    # 连通、无环
        n = r.randint(2, 110)
        return emit(r, n, random_tree(r, list(range(n))))
    if kind == "tree+cycle":              # 连通、有环（多为长度>=3 的环）
        n = r.randint(3, 110)
        e = random_tree(r, list(range(n)))
        return emit(r, n, e + extra_edges(r, list(range(n)), r.randint(1, 3)))
    if kind == "tree+dup":                # 连通、唯一的环是一条重边
        n = r.randint(2, 110)
        e = random_tree(r, list(range(n)))
        return emit(r, n, e + [r.choice(e)])
    if kind == "forest":                  # 不连通、无环；m 可能恰好 n-2
        n = r.randint(3, 110)
        c = r.randint(2, min(5, n - 1))
        cut = sorted(r.sample(range(1, n), c - 1))
        sizes = [b - a for a, b in zip([0] + cut, cut + [n])]
        e = []
        for comp in components(r, n, sizes):
            e += random_tree(r, comp)
        if not e:
            return None
        return emit(r, n, e)
    if kind == "disc+cycle":              # 不连通、有环，且 m >= n-1（卡“按边数判连通”）
        n = r.randint(5, 110)
        a = r.randint(3, n - 1)
        big, rest = components(r, n, [a, n - a])
        e = random_tree(r, big) + random_tree(r, rest)
        need = n - 1 - len(e) + r.randint(0, 3)
        e += extra_edges(r, big, max(1, need))
        return emit(r, n, e)
    if kind == "cycle+isolated":          # 一个小环加很多孤立点：有环但 m 远小于 n
        n = r.randint(10, 110)
        k = r.randint(3, min(8, n))
        vs = r.sample(range(n), k)
        e = [(vs[i], vs[(i + 1) % k]) for i in range(k)]
        return emit(r, n, e)
    if kind == "dense":                   # 满规模 m=10000，大量重边
        n = r.randint(100, 110)
        e = random_tree(r, list(range(n)))
        return emit(r, n, e + extra_edges(r, list(range(n)), 10000 - len(e)))
    if kind == "dense-disc":              # m=10000 但有一个孤立点
        n = r.randint(100, 110)
        iso = r.randrange(n)
        vs = [v for v in range(n) if v != iso]
        e = random_tree(r, vs)
        return emit(r, n, e + extra_edges(r, vs, 10000 - len(e)))
    if kind == "path110":                 # n=110 的长链，递归深度最大
        n = 110; p = list(range(n)); r.shuffle(p)
        return emit(r, n, [(p[i], p[i + 1]) for i in range(n - 1)])
    if kind == "cycle110":                # n=110 的大环
        n = 110; p = list(range(n)); r.shuffle(p)
        return emit(r, n, [(p[i], p[(i + 1) % n]) for i in range(n)])
    if kind == "n110m1":
        u, v = r.sample(range(110), 2)
        return emit(r, 110, [(u, v)])
    raise ValueError(kind)


FIXED = ["2 1\n0 1\n", "2 1\n1 0\n", "2 2\n0 1\n1 0\n", "3 1\n2 1\n",
         "4 2\n0 1\n2 3\n", "3 3\n0 1\n1 2\n2 0\n", "4 3\n0 1\n1 2\n2 0\n"]
PLAN = ["tree"] * 4 + ["tree+cycle"] * 4 + ["tree+dup"] * 3 + ["forest"] * 4 + ["disc+cycle"] * 4 + \
       ["cycle+isolated"] * 3 + ["dense", "dense", "dense-disc", "dense-disc", "path110", "cycle110", "n110m1"]


def build_cases():
    cases = [SAMPLE_IN] + FIXED
    for i, kind in enumerate(PLAN):
        for attempt in range(100):
            c = gen(random.Random(27635 * 100 + i * 1000 + attempt), kind)
            if c is not None and c not in cases:
                break
        else:
            raise AssertionError("insufficient diversity")
        cases.append(c)
    return cases


def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        for index, content in enumerate(build_cases()):
            assert valid(content), index
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            if index == 0:
                assert result.stdout == SAMPLE_OUT
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
