import random, subprocess, sys, tempfile
from pathlib import Path

def valid(text):
    # 题面：多组，每组首行 "n m"（0<n<=30000, 0<=m<=500），随后 m 行，每行 k 后跟 k 个学生编号（0..n-1），
    # 同行整数以至少一个空格分隔；以 "0 0" 结束（其后不再有数据）。
    lines = text.split("\n")
    if lines and lines[-1] == "": lines.pop()
    i = 0
    while True:
        if i >= len(lines): return False
        p = lines[i].split(); i += 1
        if len(p) != 2 or not all(t.isdigit() for t in p): return False
        n, m = map(int, p)
        if n == 0 and m == 0: return i == len(lines)
        if not (0 < n <= 30000 and 0 <= m <= 500): return False
        if i + m > len(lines): return False
        for ln in lines[i:i + m]:
            q = ln.split()
            if not q or not all(t.isdigit() for t in q): return False
            k = int(q[0])
            if len(q) != k + 1 or any(int(t) >= n for t in q[1:]): return False
        i += m

def block(n, groups, r=None):
    rows = [f"{len(g)} " + " ".join(map(str, g)) if g else "0" for g in groups]
    return f"{n} {len(groups)}\n" + "".join(x + "\n" for x in rows)

def rnd_groups(r, n, m, kmax, p0=0.85):
    gs = [r.sample(range(n), r.randint(1, min(n, kmax))) for _ in range(m)]
    # 多数情况下让 0 落进某个组，避免答案大多是 1
    if gs and r.random() < p0:
        g = r.choice(gs)
        if 0 not in g: g[r.randrange(len(g))] = 0
    return gs

def chain(r, n, m, k, reverse=True):
    # 0 -> a1 -> a2 ... 逐组传染；组顺序倒过来，逐遍扫描直到不变的写法要扫 m 遍
    ids = list(range(1, n)); r.shuffle(ids)
    path = [0] + ids[:m]
    rest = ids[m:]
    groups = []
    for j in range(m):
        g = [path[j], path[j + 1]] + r.sample(rest, min(len(rest), k - 2))
        r.shuffle(g); groups.append(g)
    if reverse: groups.reverse()
    return groups

def build_cases():
    r = random.Random(1611)
    cases = []
    # 边界：n=1、m=0、0 不在任何组、所有人一组、单人组、组内只有 0
    cases.append(block(1, []) + block(1, [[0]]) + block(5, []) + block(5, [[1, 2], [3, 4]]) +
                 block(3, [[0, 1, 2]]) + block(4, [[3], [2], [0]]) + "0 0\n")
    cases.append(block(30000, []) + block(30000, [list(range(30000))]) + "0 0\n")
    cases.append(block(30000, [r.sample(range(1, 30000), 60) for _ in range(500)]) + "0 0\n")
    # 原数据量级的小随机
    for _ in range(10):
        bl = []
        for _ in range(r.randint(1, 4)):
            n = r.randint(1, 80); bl.append(block(n, rnd_groups(r, n, r.randint(0, 30), 10)))
        cases.append("".join(bl) + "0 0\n")
    # 中等
    for _ in range(6):
        bl = []
        for _ in range(r.randint(1, 3)):
            n = r.randint(100, 5000); bl.append(block(n, rnd_groups(r, n, r.randint(1, 500), r.choice([2, 5, 20]))))
        cases.append("".join(bl) + "0 0\n")
    # 满规模随机：n=30000、m=500，组大小不同（答案从 1 到接近 n）
    for kmax in (2, 10, 60, 120):
        cases.append(block(30000, rnd_groups(r, 30000, 500, kmax)) + "0 0\n")
    # 满规模链：要沿 500 组逐级传染
    cases.append(block(30000, chain(r, 30000, 500, 60)) + block(30000, chain(r, 30000, 500, 2)) + "0 0\n")
    cases.append(block(30000, chain(r, 30000, 500, 100)) + "0 0\n")
    cases.append(block(30000, chain(r, 30000, 500, 30, reverse=False)) + block(29999, rnd_groups(r, 29999, 500, 30)) + "0 0\n")
    # 多组大数据
    cases.append("".join(block(30000, rnd_groups(r, 30000, 500, 20)) for _ in range(3)) + "0 0\n")
    # 很多小组
    cases.append("".join(block(n, rnd_groups(r, n, r.randint(0, 5), 4)) for n in [r.randint(1, 20) for _ in range(300)]) + "0 0\n")
    while len(cases) < 39:
        n = r.randint(10000, 30000)
        cases.append(block(n, rnd_groups(r, n, 500, r.randint(2, 80))) + "0 0\n")
    return cases

REFERENCE='# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md\n# Heading: 1611: The Suspects\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/01611/\n# License: not declared in source collection; no license is inferred.\n"""\nuse a technique called Disjoint-set Union (DSU) or Union-Find, which is a data structure that\nprovides efficient methods for grouping elements into disjoint (non-overlapping) sets and\nfor determining whether two elements are in the same set.\n"""\nclass UnionFind:\n    def __init__(self, n):\n        self.parent = list(range(n))  # Each student initially in their own set\n        self.rank = [0] * n  # Rank of each node for path compression\n\n    def find(self, x):\n        # Find the representative (root) of the set that x is in\n        if self.parent[x] != x:\n            self.parent[x] = self.find(self.parent[x])  # Path compression\n        return self.parent[x]\n\n    def union(self, x, y):\n        # Union the sets that x and y are in\n        root_x = self.find(x)\n        root_y = self.find(y)\n        if root_x != root_y:\n            if self.rank[root_x] < self.rank[root_y]:\n                self.parent[root_x] = root_y\n            elif self.rank[root_y] < self.rank[root_x]:\n                self.parent[root_y] = root_x\n            else:\n                self.parent[root_y] = root_x\n                self.rank[root_x] += 1\n\ndef find_suspects(n, groups):\n    uf = UnionFind(n)\n    for group in groups:\n        for student in group[1:]:\n            uf.union(group[0], student)  # Union the first student in the group with all others\n\n    suspect_set = set()\n    for i in range(n):\n        if uf.find(0) == uf.find(i):  # If student is in the same set as the initial suspect\n            suspect_set.add(i)\n\n    return len(suspect_set)\n\ndef main():\n    while True:\n        n, m = map(int, input().split())\n        if n == 0 and m == 0:\n            break\n        groups = [list(map(int, input().split()))[1:] for _ in range(m)]\n        print(find_suspects(n, groups))\n\nif __name__ == "__main__":\n    main()\n'
SAMPLE='100 4\n2 1 2\n5 10 13 11 12 14\n2 0 1\n2 99 2\n200 2\n1 5\n5 1 2 3 4 5\n1 0\n0 0\n'
LANGUAGE='Python3'

def run_all(cases):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp); src = tmp/('s.py' if LANGUAGE == 'Python3' else 's.cpp'); src.write_text(REFERENCE)
        cmd = [sys.executable, '-I', str(src)]
        if LANGUAGE != 'Python3':
            exe = tmp/'s'; subprocess.run(['g++', '-std=c++20', '-O2', '-pipe', str(src), '-o', str(exe)], check=True); cmd = [str(exe)]
        outs = []
        for x in cases:
            q = subprocess.run(cmd, input=x, text=True, capture_output=True, timeout=120, check=True)
            outs.append('\n'.join(line.rstrip() for line in q.stdout.rstrip().splitlines()) + '\n')
        return outs

def main():
    cases = [SAMPLE] + build_cases()
    for i, x in enumerate(cases):
        assert valid(x), f"第 {i} 组不满足题面约束"
    outs = run_all(cases)
    out = Path('data'); out.mkdir(exist_ok=True)
    for p in out.glob('*'): p.unlink()
    for i, (x, y) in enumerate(zip(cases, outs)):
        (out/f'{i}.in').write_text(x); (out/f'{i}.out').write_text(y)

if __name__ == '__main__':
    main()
