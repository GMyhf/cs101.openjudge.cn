import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# 迭代并查集写法（原外部 AC 代码递归找组，N=1e5 的长链会爆栈/超时，换成本解；小规模已与原 AC 代码和暴力模拟对拍一致）\nimport sys\ndef main():\n    d = sys.stdin.buffer.read().split(); n, m = int(d[0]), int(d[1])\n    adj = [[] for _ in range(n + 1)]\n    for i in range(m):\n        adj[int(d[2 + 2 * i])].append(int(d[3 + 2 * i]))\n    par = list(range(n + 1)); sz = [1] * (n + 1); members = [[v] for v in range(n + 1)]\n    queue = []\n    def find(x):\n        r = x\n        while par[r] != r: r = par[r]\n        while par[x] != r: par[x], x = r, par[x]\n        return r\n    def union(a, b):\n        a, b = find(a), find(b)\n        if a == b: return\n        if sz[a] < sz[b]: a, b = b, a\n        if sz[a] == 1: queue.append(a)\n        if sz[b] == 1: queue.append(b)\n        par[b] = a; sz[a] += sz[b]; members[a].extend(members[b]); members[b] = []\n    # 同一个点的所有出边终点两两开会，并成一组\n    for x in range(1, n + 1):\n        for y in adj[x][1:]: union(adj[x][0], y)\n    # 组大小>=2 时组内成团，组内任一点的出边终点都会被拉进组\n    while queue:\n        v = queue.pop()\n        for y in adj[v]: union(v, y)\n    ans = 0\n    for v in range(1, n + 1):\n        if par[v] == v and sz[v] >= 2: ans += sz[v] * (sz[v] - 1)\n        elif sz[find(v)] == 1: ans += len(adj[v])\n    print(ans)\nmain()\n'
SAMPLE='5 4\n1 2\n1 3\n4 3\n4 5\n'
GENERATOR_NAME='g21516'
N_MAX, M_MAX = 100000, 200000


def valid(text):
    """题面：第一行 N M（1<=N<=1e5，1<=M<=2e5）；接下来 M 行 A_i B_i，1<=A_i,B_i<=N，A_i!=B_i，有向边两两不同。"""
    try:
        lines = text.split('\n')
        while lines and lines[-1].strip() == '':
            lines.pop()
        if not lines:
            return False
        head = lines[0].split()
        if len(head) != 2:
            return False
        n, m = map(int, head)
        if not (1 <= n <= N_MAX and 1 <= m <= M_MAX) or len(lines) != m + 1:
            return False
        seen = set()
        for ln in lines[1:]:
            t = ln.split()
            if len(t) != 2:
                return False
            a, b = int(t[0]), int(t[1])
            if not (1 <= a <= n and 1 <= b <= n and a != b) or (a, b) in seen:
                return False
            seen.add((a, b))
        return True
    except ValueError:
        return False


def fmt(n, edges):
    return f"{n} {len(edges)}\n" + "".join(f"{a} {b}\n" for a, b in edges)


def g_small_both(r):
    """小图，边可双向（原随机组只有 a<b 的前向边）。"""
    n = r.randint(2, 30)
    pairs = [(a, b) for a in range(1, n + 1) for b in range(1, n + 1) if a != b]
    m = r.randint(1, min(len(pairs), r.choice([n // 2 + 1, n, 2 * n])))
    return fmt(n, r.sample(pairs, m))


def random_edges(r, n, m, lo=1, hi=None):
    hi = hi or n
    es, seen = [], set()
    while len(es) < m:
        a, b = r.randint(lo, hi), r.randint(lo, hi)
        if a != b and (a, b) not in seen:
            seen.add((a, b)); es.append((a, b))
    return es


def seeded_cases():
    out = []
    for s in range(1, 40):
        c = g21516(random.Random(s)); k = 1
        while c in out or c == SAMPLE:   # 原先有两组完全相同，重抽
            c = g21516(random.Random(s + 1000 * k)); k += 1
        out.append(c)
    return out


def specials():
    r = random.Random(21516)
    out = []
    out.append(fmt(2, [(2, 1)]))                                         # 最小规模（反向边）
    out.append(fmt(3, [(1, 2), (2, 1)]))                                 # 互指，无中介
    out.append(fmt(3, [(1, 2), (1, 3)]))                                 # 一次会议
    out.append(fmt(N_MAX, [(1, v) for v in range(2, N_MAX + 1)]))        # 星：答案约 1e10，卡 32 位溢出
    n = 75000
    out.append(fmt(n, [(1, 2), (1, 3)] + [(i, i + 1) for i in range(3, n)]))   # 组沿长链逐个吸收，答案超 2^31
    out.append(fmt(n, [(i, i + 1) for i in range(1, n)]))               # 纯长链，不发生会议；卡递归爆栈
    es = [(i, i + 1) for i in range(1, n)]; r.shuffle(es)
    out.append(fmt(n, [(1, n)] + es[: n - 2]))                           # 打乱顺序的长链 + 一条跨越边
    out.append(fmt(N_MAX, random_edges(r, N_MAX, 76000)))               # 随机稀疏：多数出度 0/1
    out.append(fmt(N_MAX, random_edges(r, N_MAX, 90000, 1, 9999)))     # 边集中在前 1e4 个点
    fun = [(v, r.randint(1, N_MAX)) for v in range(1, N_MAX + 1)]
    out.append(fmt(N_MAX, [(a, b) for a, b in fun if a != b][:76000]))  # 函数图：出度至多 1，不发生会议
    # 许多中等大小的组：每 50 个点一块，块内随机，块间少量边
    es, seen = [], set()
    for base in range(0, 20000, 50):
        for a, b in random_edges(r, 50, 60):
            es.append((base + a, base + b))
    out.append(fmt(20000, es))
    return out
def g21516(r):
    n = r.randint(2, 18)
    edges = [(a, b) for a in range(1, n + 1) for b in range(a + 1, n + 1) if r.random() < .18]
    if not edges:
        edges = [(1, 2)]
    return f"{n} {len(edges)}\n" + "\n".join(f"{a} {b}" for a, b in edges) + "\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=60)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+seeded_cases()+[g_small_both(random.Random(1000 + s)) for s in range(15)]+specials()
    assert all(valid(c) for c in cases) and len(set(cases)) == len(cases)
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
