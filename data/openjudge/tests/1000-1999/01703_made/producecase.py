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
 for i,x in enumerate([SAMPLE]+[generate(NUMBER,s) for s in range(1,21)]):
  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))
if __name__=='__main__':main()
