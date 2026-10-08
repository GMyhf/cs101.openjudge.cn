import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'from collections import deque\n\nn, m = map(int, input().split())\ngraph1 = [set() for _ in range(n+1)]\nfor _ in range(m):\n    a, b = map(int, input().split())\n    graph1[a].add(b)\n    graph1[b].add(a)\n\nunvisited = set(range(1, n+1))\ncomponents = 0\n\nwhile unvisited:\n    start = unvisited.pop()\n    components += 1\n    queue = deque([start])\n    while queue:\n        u = queue.popleft()\n        good = unvisited - graph1[u]  # 所有未访问且与 u 有 0-边的点\n        for v in good:\n            queue.append(v)\n        unvisited -= good\n\nprint(components - 1)\n'
# 题面样例给了两组（用 "===========" 分隔），但输入格式只有一组：第 0 组取样例一，样例二作第 1 组。
SAMPLE_IN = '6 11\n1 3\n1 4\n1 5\n1 6\n2 3\n2 4\n2 5\n2 6\n3 4\n3 5\n3 6\n'
SAMPLE2_IN = '3 0\n'
MAX_N = 100000          # 提示 Subtask2: n <= 100000
MAX_M = 200000          # m <= min{200000, n(n-1)/2}


def valid(text):
    """题面：第一行 n m，m <= min(200000, n(n-1)/2)，n <= 100000；随后 m 行 a b，1 <= a < b <= n，边两两不同。"""
    lines = text.split('\n')
    if lines[-1] != '':
        return False
    lines = lines[:-1]
    def ints(line, k):
        toks = line.split(' ')
        if len(toks) != k or any(not t.isdigit() or t != str(int(t)) for t in toks):
            return None
        return list(map(int, toks))
    if not lines:
        return False
    first = ints(lines[0], 2)
    if first is None:
        return False
    n, m = first
    if not 1 <= n <= MAX_N or m > min(MAX_M, n * (n - 1) // 2) or len(lines) != m + 1:
        return False
    seen = set()
    for line in lines[1:]:
        e = ints(line, 2)
        if e is None:
            return False
        a, b = e
        if not 1 <= a < b <= n or (a, b) in seen:
            return False
        seen.add((a, b))
    return True


def fmt(n, edges):
    return f"{n} {len(edges)}\n" + "".join(f"{a} {b}\n" for a, b in edges)


def norm(e):
    a, b = e
    return (a, b) if a < b else (b, a)


def small_random(r, n_lo, n_hi):
    n = r.randint(n_lo, n_hi); all_edges = [(i, j) for i in range(1, n + 1) for j in range(i + 1, n + 1)]
    r.shuffle(all_edges); m = r.randint(0, len(all_edges)); edges = sorted(all_edges[:m])
    return fmt(n, edges)


def dense_random(r, n, keep_zero):
    # 完全图里只留 keep_zero 条 0 边，其余都是 1 边，补图稀疏 -> 连通块多
    all_edges = [(i, j) for i in range(1, n + 1) for j in range(i + 1, n + 1)]
    r.shuffle(all_edges)
    edges = all_edges[keep_zero:]
    r.shuffle(edges)
    return fmt(n, edges)


def multipartite(r, sizes, extra_zero=0, shuffle_labels=True):
    # 组间全是 1 边，组内全是 0 边 -> 补图连通块数 = 组数；再挖掉 extra_zero 条组间 1 边让块合并
    n = sum(sizes)
    lab = list(range(1, n + 1))
    if shuffle_labels:
        r.shuffle(lab)
    groups, k = [], 0
    for s in sizes:
        groups.append(lab[k:k + s]); k += s
    edges = []
    for x in range(len(groups)):
        for y in range(x + 1, len(groups)):
            for a in groups[x]:
                for b in groups[y]:
                    edges.append(norm((a, b)))
    r.shuffle(edges)
    edges = edges[extra_zero:]
    return fmt(n, edges)


def universal(r, n, k, hub_pool=None):
    # k 个点与所有点之间都是 1 边 -> 答案 k（若 n > k）；hub_pool 限定中心点编号（控制文件体积）
    lab = list(range(1, (hub_pool or n) + 1)); r.shuffle(lab)
    hubs = lab[:k]
    es = set()
    for h in hubs:
        for v in range(1, n + 1):
            if v != h:
                es.add(norm((h, v)))
    edges = list(es); r.shuffle(edges)
    return fmt(n, edges)


def sparse_random(r, n, m):
    es = set()
    while len(es) < m:
        a, b = r.randint(1, n), r.randint(1, n)
        if a != b:
            es.add(norm((a, b)))
    edges = list(es); r.shuffle(edges)
    return fmt(n, edges)


def chain_zero(r, n):
    # 0 边只构成一条哈密顿路（其余全是 1 边），补图连通但很“细”，答案 0
    perm = list(range(1, n + 1)); r.shuffle(perm)
    path = {norm((perm[i], perm[i + 1])) for i in range(n - 1)}
    edges = [(i, j) for i in range(1, n + 1) for j in range(i + 1, n + 1) if (i, j) not in path]
    r.shuffle(edges)
    return fmt(n, edges)


def build_cases():
    r = random.Random(27351)
    cases = [SAMPLE_IN, SAMPLE2_IN,
             '1 0\n',                     # 最小规模
             '2 1\n1 2\n',                # 答案 1
             '2 0\n',
             fmt(5, [(i, j) for i in range(1, 6) for j in range(i + 1, 6)]),   # m = n(n-1)/2，答案 4
             ]
    for _ in range(10):                  # 小图随机（n <= 12），可与暴力对拍
        cases.append(small_random(r, 4, 12))
    for _ in range(4):                   # Subtask1 规模
        cases.append(small_random(r, 200, 300))
    cases.append(dense_random(r, 300, 150))
    cases.append(multipartite(r, [1] * 300))                     # n=300 完全图，答案 299
    cases.append(multipartite(r, [r.randint(1, 30) for _ in range(20)]))
    cases.append(multipartite(r, [r.randint(1, 8) for _ in range(60)], extra_zero=30))
    cases.append(chain_zero(r, 300))
    # 大规模（.in 需 <= 1MB，m 达不到 200000，取在体积内的最大）；data/ 合计须 <= 10MB，
    # 只留 n=470 完全图、n=1e5 中心点、m=120000 三组贴近体积上限，其余中等规模
    cases.append(multipartite(r, [1] * 470))                     # n=470 完全图，m=110215，答案 469
    cases.append(dense_random(r, 380, 400))
    cases.append(multipartite(r, [r.randint(1, 4) for _ in range(140)]))
    cases.append(chain_zero(r, 380))
    cases.append(f"{MAX_N} 0\n")                                 # n=1e5，全 0，答案 0
    cases.append(universal(r, MAX_N, 1, hub_pool=9))                        # 一个点与所有点都是 1 边，答案 1
    cases.append(universal(r, 12000, 4))                         # 答案 4
    cases.append(universal(r, 7000, 9))                         # 答案 9
    cases.append(sparse_random(r, MAX_N, 50000))
    cases.append(sparse_random(r, 1000, 120000))
    cases.append(sparse_random(r, 50000, 60000))
    cases.append(multipartite(r, [80] * 5))                      # 5 个 80 点的组，组间全 1 边，答案 4
    cases.append(sparse_random(r, 3, 2))
    cases.append(small_random(r, 13, 40))
    cases.append(multipartite(r, [3, 1, 2, 4, 1], extra_zero=1))
    assert len(cases) == 40, len(cases)
    return cases


def main():
    cases = build_cases()
    assert len(set(cases)) == len(cases)
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        for index, content in enumerate(cases):
            assert valid(content), index
            assert len(content.encode()) <= 1 << 20, (index, len(content))
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=120, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
