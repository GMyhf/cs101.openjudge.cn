import random
REFERENCE='# External reference: /practice/29677/statistics/\n# Accepted submission: 52733700\n# Source: http://cs101.openjudge.cn/practice/solution/52733700/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\ninput = sys.stdin.read\nsys.setrecursionlimit(1 << 25)\n\nclass DSU:\n    def __init__(self, n):\n        self.fa = list(range(n+1))\n    def find(self, x):\n        if self.fa[x] != x:\n            self.fa[x] = self.find(self.fa[x])\n        return self.fa[x]\n    def union(self, x, y):\n        fx = self.find(x)\n        fy = self.find(y)\n        if fx != fy:\n            self.fa[fy] = fx\n\ndef main():\n    data = list(map(int, input().split()))\n    ptr = 0\n    T = data[ptr]\n    ptr +=1\n    for _ in range(T):\n        N = data[ptr]\n        ptr +=1\n        t = data[ptr:ptr+N]\n        ptr +=N\n        d = data[ptr:ptr+N]\n        ptr +=N\n        dsu = DSU(N)\n        for i in range(1,N+1):\n            di = d[i-1]\n            p1 = i + di\n            if 1<=p1<=N:\n                dsu.union(i,p1)\n            p2 = i - di\n            if 1<=p2<=N:\n                dsu.union(i,p2)\n        ok = True\n        for idx in range(N):\n            pos = idx+1\n            tar = t[idx]\n            if dsu.find(pos) != dsu.find(tar):\n                ok = False\n                break\n        print("YES" if ok else "NO")\n\nif __name__ == "__main__":\n    main()'
SAMPLE='3\n5\n5 4 3 2 1\n1 1 1 1 1\n7\n4 3 5 1 2 7 6\n4 6 6 1 6 6 1\n7\n4 2 5 1 3 7 6\n4 6 6 1 6 6 1\n'
GENERATOR_NAME='g29677'
def g29677(r):
    rows = [str(r.randint(1, 4))]
    for _ in range(int(rows[0])):
        n = r.randint(2, 45); target = list(range(1, n + 1)); r.shuffle(target)
        distance = [r.randint(0, n) for _ in range(n)]
        rows.extend((str(n), " ".join(map(str, target)), " ".join(map(str, distance))))
    return "\n".join(rows) + "\n"

from pathlib import Path
import random, subprocess, sys, tempfile
REFERENCE = REFERENCE
def solve(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        result=subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()
