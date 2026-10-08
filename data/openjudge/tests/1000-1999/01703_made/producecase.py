import random,subprocess,sys,tempfile
from pathlib import Path
def fence_counts(n):
    if n == 1:
        return 1
    count = [[[0, 0] for _ in range(n + 1)] for _ in range(n + 1)]
    count[1][1] = [1, 1]
    for size in range(2, n + 1):
        for first in range(1, size + 1):
            count[size][first][0] = sum(count[size - 1][second][1]
                                            for second in range(first, size))
            count[size][first][1] = sum(count[size - 1][second][0]
                                            for second in range(1, first))
    return sum(sum(count[n][first]) for first in range(1, n + 1))
def generate(number, seed):
    r = random.Random(number * 1_000_003 + seed)
    if number == 1258:
        cases = []
        for _ in range(r.randint(1, 3)):
            n = r.randint(3, 18)
            matrix = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(i + 1, n):
                    matrix[i][j] = matrix[j][i] = r.randint(1, 100000)
            cases.append(str(n) + "\n" + "\n".join(" ".join(map(str, row)) for row in matrix))
        return "\n".join(cases) + "\n"
    if number == 1661:
        cases = []
        for _ in range(r.randint(1, 4)):
            n = r.randint(1, 12); y = r.randint(2, 200); max_drop = y
            platforms = []
            for height in r.sample(range(1, y), min(n, y - 1)):
                left = r.randint(20, 1000); platforms.append((left, left + r.randint(1, 30), height))
            while len(platforms) < n:
                left = 1100 + len(platforms) * 40; platforms.append((left, left + 10, 1))
            cases.append(f"{n} 0 {y} {max_drop}\n" + "\n".join("%d %d %d" % p for p in platforms))
        return str(len(cases)) + "\n" + "\n".join(cases) + "\n"
    if number == 1664:
        values = [(r.randint(1, 10), r.randint(1, 10)) for _ in range(r.randint(1, 20))]
        return str(len(values)) + "\n" + "\n".join(f"{m} {n}" for m, n in values) + "\n"
    if number == 1703:
        cases = []
        for _ in range(r.randint(1, 4)):
            n = r.randint(3, 80); gangs = [0, 1] + [r.randrange(2) for _ in range(n - 2)]; ops = []
            for _ in range(r.randint(3, 100)):
                a, b = r.sample(range(n), 2)
                if r.random() < .55:
                    while gangs[a] == gangs[b]: b = r.randrange(n)
                    ops.append(f"D {a+1} {b+1}")
                else: ops.append(f"A {a+1} {b+1}")
            cases.append(f"{n} {len(ops)}\n" + "\n".join(ops))
        return str(len(cases)) + "\n" + "\n".join(cases) + "\n"
    if number == 1958:
        return ""
    if number == 2812:
        rows, cols = r.randint(5, 40), r.randint(5, 40); planted_row = r.randint(1, rows)
        points = {(planted_row, col) for col in range(1, cols + 1)}
        target = r.randint(max(3, cols), min(rows * cols, cols + 80))
        while len(points) < target: points.add((r.randint(1, rows), r.randint(1, cols)))
        points = list(points); r.shuffle(points)
        return f"{rows} {cols}\n{len(points)}\n" + "\n".join(f"{x} {y}" for x, y in points) + "\n"
    if number == 1042:
        cases = []
        for _ in range(r.randint(1, 3)):
            n = r.randint(2, 8); h = r.randint(1, 5)
            fish = [r.randint(0, 100) for _ in range(n)]; decreases = [r.randint(0, 20) for _ in range(n)]
            travel = [r.randint(1, min(12, h * 12)) for _ in range(n - 1)]
            cases.append("\n".join((str(n), str(h), " ".join(map(str, fish)),
                                     " ".join(map(str, decreases)), " ".join(map(str, travel)))))
        return "\n".join(cases) + "\n0\n"
    if number == 2226:
        rows, cols = r.randint(1, 18), r.randint(1, 18)
        grid = ["".join(r.choice("***...") for _ in range(cols)) for _ in range(rows)]
        return f"{rows} {cols}\n" + "\n".join(grid) + "\n"
    if number == 1064:
        n, k = r.randint(1, 80), r.randint(1, 500)
        lengths = [r.randint(100, 10_000_000) for _ in range(n)]
        return f"{n} {k}\n" + "\n".join(f"{x//100}.{x%100:02d}" for x in lengths) + "\n"
    if number == 1185:
        rows, cols = r.randint(1, 25), r.randint(1, 10)
        return f"{rows} {cols}\n" + "\n".join("".join(r.choice("PPPH") for _ in range(cols)) for _ in range(rows)) + "\n"
    if number == 2229:
        return f"{r.randint(1, 1_000_000)}\n"
    if number == 2533:
        values = [r.randint(0, 10000) for _ in range(r.randint(1, 200))]
        return f"{len(values)}\n" + " ".join(map(str, values)) + "\n"
    if number == 2659:
        rows, cols, count = r.randint(1, 30), r.randint(1, 30), r.randint(1, 30)
        bombs = [(r.randint(1, rows), r.randint(1, cols), r.randrange(1, 100, 2), r.randint(0, 1))
                 for _ in range(count)]
        return f"{rows} {cols} {count}\n" + "\n".join("%d %d %d %d" % b for b in bombs) + "\n"
    if number == 2946:
        value, count = r.randint(-100, 100), r.randint(1, 30); operations = []
        for _ in range(count): operations.append((r.choice(("plus", "minus", "multiply")), r.randint(-5, 5)))
        return f"{value} {count}\n" + "\n".join(f"{op} {x}" for op, x in operations) + "\n"
    if number == 1037:
        values = []
        for _ in range(r.randint(1, 8)):
            n = r.randint(1, 10); values.append((n, r.randint(1, fence_counts(n))))
        return str(len(values)) + "\n" + "\n".join(f"{n} {c}" for n, c in values) + "\n"
    if number == 1160:
        villages = sorted(r.sample(range(1, 10001), r.randint(1, 100)))
        return f"{len(villages)} {r.randint(1, min(30, len(villages)))}\n" + " ".join(map(str, villages)) + "\n"
    if number == 1944:
        n = r.randint(2, 80); all_pairs = [(a, b) for a in range(1, n + 1) for b in range(a + 1, n + 1)]
        pairs = r.sample(all_pairs, r.randint(1, min(200, len(all_pairs))))
        return f"{n} {len(pairs)}\n" + "\n".join(f"{a} {b}" for a, b in pairs) + "\n"
    if number == 2385:
        total, walks = r.randint(1, 200), r.randint(1, 30)
        return f"{total} {walks}\n" + "\n".join(str(r.randint(1, 2)) for _ in range(total)) + "\n"
    if number == 2711:
        heights = [r.randint(130, 230) for _ in range(r.randint(2, 100))]
        return f"{len(heights)}\n" + " ".join(map(str, heights)) + "\n"
    if number == 2797:
        words = set(); target = r.randint(2, 60)
        while len(words) < target:
            words.add("".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(r.randint(1, 20))))
        words = sorted(words); r.shuffle(words)
        return "\n".join(words) + "\n"
    raise KeyError(number)

# ---- 题面契约与 1703 专用生成器 ----
def _parity_dsu(n):
    par = list(range(n + 1)); rel = [0] * (n + 1)   # rel: 与父节点是否不同团伙
    def find(x):
        path = []
        while par[x] != x:
            path.append(x); x = par[x]
        root = x; acc = 0
        for y in reversed(path):
            acc ^= rel[y]; rel[y] = acc; par[y] = root
        return root
    return par, rel, find

def _cases(text):
    tok = text.split(); p = 1; out = []
    for _ in range(int(tok[0])):
        n, m = int(tok[p]), int(tok[p + 1]); p += 2
        ops = [(tok[p + 3 * k], int(tok[p + 3 * k + 1]), int(tok[p + 3 * k + 2])) for k in range(m)]; p += 3 * m
        out.append((n, ops))
    return out

def _solve_text(text):
    """独立解：带奇偶权的并查集（非递归），D 信息自相矛盾时抛异常。"""
    res = []
    for n, ops in _cases(text):
        par, rel, find = _parity_dsu(n)
        for op, a, b in ops:
            ra, rb = find(a), find(b)
            if op == 'D':
                if ra == rb:
                    if rel[a] ^ rel[b] != 1: raise ValueError('contradiction')
                else:
                    par[ra] = rb; rel[ra] = rel[a] ^ rel[b] ^ 1
            else:
                if ra != rb: res.append("Not sure yet.")
                elif rel[a] == rel[b]: res.append("In the same gang.")
                else: res.append("In different gangs.")
    return "\n".join(res) + ("\n" if res else "")

def _nat(s):
    return s.isascii() and s.isdigit() and s == str(int(s))

def valid(text):
    """T（1..20）；每组 N M（1<=N<=100000，0<=M<=100000），其后恰 M 行 “D a b” 或 “A a b”，1<=a,b<=N；
    每起案件属于 A、B 之一，故 D 信息必须能被某种二染色满足（D 的 a≠b、无奇环矛盾）。"""
    try:
        if not text.endswith('\n') or '\r' in text: return False
        lines = text[:-1].split('\n')
        if any(ln != ln.strip() or '  ' in ln or not ln for ln in lines): return False
        if not _nat(lines[0]): return False
        t = int(lines[0])
        if not 1 <= t <= 20: return False
        p = 1
        for _ in range(t):
            if p >= len(lines): return False
            hd = lines[p].split(' '); p += 1
            if len(hd) != 2 or not all(_nat(x) for x in hd): return False
            n, m = map(int, hd)
            if not (1 <= n <= 100000 and 0 <= m <= 100000) or p + m > len(lines): return False
            for ln in lines[p:p + m]:
                f = ln.split(' ')
                if len(f) != 3 or f[0] not in ('A', 'D') or not (_nat(f[1]) and _nat(f[2])): return False
                a, b = int(f[1]), int(f[2])
                if not (1 <= a <= n and 1 <= b <= n): return False
                if f[0] == 'D' and a == b: return False
            p += m
        if p != len(lines): return False
        _solve_text(text)   # D 信息矛盾会抛异常
        return True
    except Exception:
        return False

def _gen_case(r, n, m, kind):
    color = [0] + [r.randrange(2) for _ in range(n)]
    byc = [[i for i in range(1, n + 1) if color[i] == c] for c in (0, 1)]
    if not byc[0] or not byc[1]:
        color[1] ^= 1; byc = [[i for i in range(1, n + 1) if color[i] == c] for c in (0, 1)]
    ops = []
    def diffpair():
        a = r.choice(byc[0]); b = r.choice(byc[1])
        return (a, b) if r.random() < .5 else (b, a)
    def anypair():
        a = r.randint(1, n); b = r.randint(1, n - 1)
        return a, b + (b >= a)
    if kind == 'chain':
        # 按 1-2-3-…-n 的顺序连成一条链（相邻颜色不同），不按秩合并、不压缩路径的并查集会退化成 O(n) 一次 find
        perm = list(range(1, n + 1))
        if r.random() < .5: perm.reverse()
        color = [0] * (n + 1)
        for i, v in enumerate(perm): color[v] = i & 1
        links = min(n - 1, m * 2 // 3)
        for i in range(links): ops.append(f"D {perm[i]} {perm[i + 1]}" if r.random() < .5 else f"D {perm[i + 1]} {perm[i]}")
        while len(ops) < m:
            a, b = perm[0], perm[r.randint(1, links)] if links else perm[-1]
            if r.random() < .3: a, b = anypair()
            ops.append(f"A {a} {b}")
        return f"{n} {len(ops)}\n" + "\n".join(ops)
    pd = {'sparse': .2, 'dense': .6, 'mixed': .45}[kind]
    for _ in range(m):
        if r.random() < pd:
            a, b = diffpair(); ops.append(f"D {a} {b}")
        else:
            a, b = anypair(); ops.append(f"A {a} {b}")
    return f"{n} {m}\n" + "\n".join(ops)

def gen_file(seed):
    r = random.Random(1703 * 1_000_003 + seed)
    if seed == 1:
        cs = [_gen_case(r, 2, 3, 'mixed'), "2 2\nA 1 2\nA 2 1", "3 4\nD 1 2\nA 1 2\nD 3 2\nA 3 1"]
    elif seed <= 10:
        cs = [_gen_case(r, r.randint(2, 12), r.randint(1, 40), r.choice(['sparse', 'dense', 'mixed', 'chain'])) for _ in range(r.randint(1, 20))]
    elif seed <= 22:
        cs = [_gen_case(r, r.randint(50, 3000), r.randint(100, 1200), r.choice(['sparse', 'dense', 'mixed', 'chain'])) for _ in range(r.randint(2, 20))]
    # 只保留 3 组满载（seed 23 链式 N=1e5 卡不压缩路径、24 随机 N=1e5、29 M=98000），其余同类构造缩小 M 控制总体积
    elif seed <= 28:
        cs = [_gen_case(r, 100000, 65000 if seed in (23, 24) else 6000, ['mixed', 'dense', 'chain'][seed % 3])]       # N 取上限
    elif seed <= 33:
        cs = [_gen_case(r, 999, 98000 if seed == 29 else 7000, ['mixed', 'sparse', 'chain', 'dense', 'mixed'][seed % 5])]  # M 接近上限
    else:
        cs = [_gen_case(r, r.randint(5000, 100000), 300, r.choice(['mixed', 'dense', 'chain'])) for _ in range(20)]  # T=20
    return f"{len(cs)}\n" + "\n".join(cs) + "\n"

REFERENCE='# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md\n# Heading: 1703: 发现它，抓住它\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md\n# Upstream problem: http://cs101.openjudge.cn/practice/01703/\n# License: not declared in source collection; no license is inferred.\nimport sys\nclass UnionFind:\n    def __init__(self, n):\n        self.parent = list(range(n))\n        self.rank = [0] * n\n\n    def find(self, x):\n        if self.parent[x] != x:\n            self.parent[x] = self.find(self.parent[x])\n        return self.parent[x]\n\n    def union(self, x, y):\n        rootX = self.find(x)\n        rootY = self.find(y)\n        if rootX != rootY:\n            if self.rank[rootX] > self.rank[rootY]:\n                self.parent[rootY] = rootX\n            elif self.rank[rootX] < self.rank[rootY]:\n                self.parent[rootX] = rootY\n            else:\n                self.parent[rootY] = rootX\n                self.rank[rootX] += 1\n\ndef solve():\n    n, m = map(int, input().split())\n    uf = UnionFind(2 * n)  # 初始化并查集，每个案件对应两个节点\n    for _ in range(m):\n        operation, a, b = input().split()\n        a, b = int(a) - 1, int(b) - 1\n        if operation == "D":\n            uf.union(a, b + n)  # a与b的对立案件合并\n            uf.union(a + n, b)  # a的对立案件与b合并\n        else:  # "A"\n            if uf.find(a) == uf.find(b) or uf.find(a + n) == uf.find(b + n):\n                print("In the same gang.")\n            elif uf.find(a) == uf.find(b + n) or uf.find(a + n) == uf.find(b):\n                print("In different gangs.")\n            else:\n                print("Not sure yet.")\n\nT = int(input())\nfor _ in range(T):\n    solve()\n'
NUMBER=1703
SAMPLE='1\n5 5\nA 1 2\nD 1 2\nA 1 2\nD 2 4\nA 1 4\n'
def run(x):
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'m.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)
  if q.returncode:raise SystemExit(q.stderr)
  return q.stdout.rstrip()+'\n'
def main():
 d=Path('data');d.mkdir(exist_ok=True)
 for p in d.glob('*'):p.unlink()
 for i,x in enumerate([SAMPLE]+[gen_file(s) for s in range(1, 40)]):
  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))
if __name__=='__main__':main()
