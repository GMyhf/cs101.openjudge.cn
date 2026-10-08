import random, subprocess, sys, tempfile
from pathlib import Path

REFERENCE = '# External reference: statistics page /practice/28012/\n# Accepted submission: 52741406\n# Source: http://cs101.openjudge.cn/practice/solution/52741406/\n# License: not declared on the submission page; no license is inferred.\n\nfrom collections import defaultdict, deque\n\ndef reachableNodes(n, edges, restricted):\n    # 建图\n    graph = defaultdict(list)\n    for a, b in edges:\n        graph[a].append(b)\n        graph[b].append(a)\n\n    restricted_set = set(restricted)\n\n    # BFS 从节点 0 开始\n    visited = set()\n    queue = deque([0])\n    visited.add(0)\n\n    while queue:\n        u = queue.popleft()\n        for v in graph[u]:\n            if v not in visited and v not in restricted_set:\n                visited.add(v)\n                queue.append(v)\n\n    return len(visited)\n\n\nif __name__ == "__main__":\n    # 读取输入\n    n = int(input().strip())\n    edges = []\n    for _ in range(n - 1):\n        a, b = map(int, input().split())\n        edges.append([a, b])\n    restricted = list(map(int, input().split()))\n\n    # 计算结果并输出\n    result = reachableNodes(n, edges, restricted)\n    print(result)'

SAMPLE = '7\n0 1\n1 2\n3 1\n4 0\n0 5\n5 6\n4 5\n'
SAMPLE2 = '7\n0 1\n0 2\n0 5\n0 4\n3 2\n6 5\n4 2 1\n'


def _int(s):
    return s.isdigit() and (s == '0' or s[0] != '0')


def valid(text):
    """题面（LeetCode 2368）：2≤n≤1000；n-1 行边构成 0..n-1 上的树；
    最后一行若干个（≥1 且 <n）互不相同的受限节点，不含 0。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    if not _int(lines[0]):
        return False
    n = int(lines[0])
    if not (2 <= n <= 1000) or len(lines) != n + 1:
        return False
    par = list(range(n))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for ln in lines[1:n]:
        p = ln.split(' ')
        if len(p) != 2 or not all(_int(t) for t in p):
            return False
        a, b = map(int, p)
        if not (0 <= a < n and 0 <= b < n) or a == b:
            return False
        fa, fb = find(a), find(b)
        if fa == fb:
            return False
        par[fa] = fb
    rs = lines[n].split(' ')
    if not rs or not all(_int(t) for t in rs):
        return False
    rs = list(map(int, rs))
    return 1 <= len(rs) < n and len(set(rs)) == len(rs) and all(1 <= x < n for x in rs)


def fmt(n, edges, restricted):
    return f"{n}\n" + "\n".join(f"{a} {b}" for a, b in edges) + "\n" + " ".join(map(str, restricted)) + "\n"


def relabel(r, n, edges, restricted_old, keep0=True):
    """随机重编号（0 号固定为原 0 号）、随机边方向与顺序。"""
    perm = list(range(1, n)); r.shuffle(perm); perm = [0] + perm
    e = [(perm[a], perm[b]) if r.random() < .5 else (perm[b], perm[a]) for a, b in edges]
    r.shuffle(e)
    rs = [perm[x] for x in restricted_old]; r.shuffle(rs)
    return fmt(n, e, rs)


def rand_tree(r, n, kind):
    if kind == 'rand':
        return [(i, r.randrange(i)) for i in range(1, n)]
    if kind == 'deep':
        return [(i, r.randrange(max(0, i - 3), i)) for i in range(1, n)]
    if kind == 'bin':
        return [(i, (i - 1) // 2) for i in range(1, n)]
    if kind == 'star':
        return [(i, r.randrange(min(i, 3))) for i in range(1, n)]


def build_cases():
    r = random.Random(28012)
    N = 1000
    cases = [SAMPLE, SAMPLE2]
    chain = [(i - 1, i) for i in range(1, N)]
    cases.append(fmt(N, chain, [N - 1]))                         # 链长 999，答案 999（卡递归深度）
    cases.append(fmt(N, chain[::-1], [N - 1, 500]))              # 答案 500
    # 0 在链中间
    m = [(i, i + 1) for i in range(1, N - 1)]
    m.remove((499, 500)); m += [(499, 0), (0, 500)]
    cases.append(relabel(r, N, m, [1], keep0=True))
    cases.append(fmt(N, [(0, i) for i in range(1, N)], [r.randrange(1, N)]))  # 以 0 为中心的星，答案 n-1
    cases.append(fmt(N, [(i, 7) for i in range(N) if i != 7], [7]))           # 中心是 7 且受限，答案 1
    cases.append(fmt(N, [(0, i) for i in range(1, N)], list(range(1, N))))     # 除 0 外全部受限，答案 1
    # 0 的所有邻居都受限
    e = rand_tree(r, N, 'rand')
    nb = sorted({b for a, b in e if a == 0} | {a for a, b in e if b == 0})
    cases.append(relabel(r, N, e, nb))
    for kind in ['rand', 'deep', 'bin']:
        e = rand_tree(r, N, kind)
        cases.append(relabel(r, N, e, r.sample(range(1, N), r.randint(1, 20))))
    e = rand_tree(r, N, 'rand')
    cases.append(relabel(r, N, e, r.sample(range(1, N), N // 2)))
    # 小边界
    cases += [fmt(2, [(0, 1)], [1]), fmt(2, [(1, 0)], [1]), fmt(3, [(0, 1), (1, 2)], [2]),
              fmt(3, [(0, 1), (1, 2)], [1]), fmt(3, [(1, 0), (2, 0)], [2]), fmt(3, [(2, 1), (0, 2)], [1, 2])]
    while len(cases) < 41:
        n = r.choice([r.randint(2, 10), r.randint(11, 100), r.randint(101, N)])
        e = rand_tree(r, n, r.choice(['rand', 'deep', 'bin', 'star']))
        k = r.randint(1, min(n - 1, r.choice([3, 15, n])))
        c = relabel(r, n, e, r.sample(range(1, n), k))
        if c not in cases:
            cases.append(c)
    return cases


def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p = Path(d) / 'main.py'; p.write_text(REFERENCE)
        x = subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=90)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout


def main():
    d = Path('data'); d.mkdir(exist_ok=True)
    cases = build_cases()
    assert len(cases) == len(set(cases)), '组间有重复'
    for i, c in enumerate(cases):
        assert valid(c), f'第 {i} 组不合题面'
        (d / f'{i}.in').write_text(c); (d / f'{i}.out').write_text(run(c))


if __name__ == '__main__':
    main()
