import random, subprocess, sys, tempfile
from pathlib import Path
def g1611(r):
    blocks = []
    for _ in range(r.randint(1, 3)):
        n, m = r.randint(1, 80), r.randint(0, 30); rows = []
        for _ in range(m):
            members = r.sample(range(n), r.randint(1, min(n, 10)))
            rows.append(str(len(members)) + " " + " ".join(map(str, members)))
        blocks.append(f"{n} {m}\n" + ("\n".join(rows) + "\n" if rows else ""))
    return "".join(blocks) + "0 0\n"

REFERENCE='# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md\n# Heading: 1611: The Suspects\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/01611/\n# License: not declared in source collection; no license is inferred.\n"""\nuse a technique called Disjoint-set Union (DSU) or Union-Find, which is a data structure that\nprovides efficient methods for grouping elements into disjoint (non-overlapping) sets and\nfor determining whether two elements are in the same set.\n"""\nclass UnionFind:\n    def __init__(self, n):\n        self.parent = list(range(n))  # Each student initially in their own set\n        self.rank = [0] * n  # Rank of each node for path compression\n\n    def find(self, x):\n        # Find the representative (root) of the set that x is in\n        if self.parent[x] != x:\n            self.parent[x] = self.find(self.parent[x])  # Path compression\n        return self.parent[x]\n\n    def union(self, x, y):\n        # Union the sets that x and y are in\n        root_x = self.find(x)\n        root_y = self.find(y)\n        if root_x != root_y:\n            if self.rank[root_x] < self.rank[root_y]:\n                self.parent[root_x] = root_y\n            elif self.rank[root_y] < self.rank[root_x]:\n                self.parent[root_y] = root_x\n            else:\n                self.parent[root_y] = root_x\n                self.rank[root_x] += 1\n\ndef find_suspects(n, groups):\n    uf = UnionFind(n)\n    for group in groups:\n        for student in group[1:]:\n            uf.union(group[0], student)  # Union the first student in the group with all others\n\n    suspect_set = set()\n    for i in range(n):\n        if uf.find(0) == uf.find(i):  # If student is in the same set as the initial suspect\n            suspect_set.add(i)\n\n    return len(suspect_set)\n\ndef main():\n    while True:\n        n, m = map(int, input().split())\n        if n == 0 and m == 0:\n            break\n        groups = [list(map(int, input().split()))[1:] for _ in range(m)]\n        print(find_suspects(n, groups))\n\nif __name__ == "__main__":\n    main()\n'
SAMPLE='100 4\n2 1 2\n5 10 13 11 12 14\n2 0 1\n2 99 2\n200 2\n1 5\n5 1 2 3 4 5\n1 0\n0 0\n'
GENERATOR='g1611'

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as folder:
        script=Path(folder)/"main.py"; script.write_text(REFERENCE)
        result=subprocess.run([sys.executable,"-I",str(script)],input=text,text=True,capture_output=True,timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    for old in data.glob("*"): old.unlink()
    cases=[SAMPLE]+[globals()[GENERATOR](random.Random(seed)) for seed in range(1,21)]
    for i,case in enumerate(cases):
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()
