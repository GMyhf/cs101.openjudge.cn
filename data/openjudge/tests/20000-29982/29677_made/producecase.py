import random
REFERENCE='# External reference: /practice/29677/statistics/\n# Accepted submission: 52733700\n# Source: http://cs101.openjudge.cn/practice/solution/52733700/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\ninput = sys.stdin.read\nsys.setrecursionlimit(1 << 25)\n\nclass DSU:\n    def __init__(self, n):\n        self.fa = list(range(n+1))\n    def find(self, x):\n        if self.fa[x] != x:\n            self.fa[x] = self.find(self.fa[x])\n        return self.fa[x]\n    def union(self, x, y):\n        fx = self.find(x)\n        fy = self.find(y)\n        if fx != fy:\n            self.fa[fy] = fx\n\ndef main():\n    data = list(map(int, input().split()))\n    ptr = 0\n    T = data[ptr]\n    ptr +=1\n    for _ in range(T):\n        N = data[ptr]\n        ptr +=1\n        t = data[ptr:ptr+N]\n        ptr +=N\n        d = data[ptr:ptr+N]\n        ptr +=N\n        dsu = DSU(N)\n        for i in range(1,N+1):\n            di = d[i-1]\n            p1 = i + di\n            if 1<=p1<=N:\n                dsu.union(i,p1)\n            p2 = i - di\n            if 1<=p2<=N:\n                dsu.union(i,p2)\n        ok = True\n        for idx in range(N):\n            pos = idx+1\n            tar = t[idx]\n            if dsu.find(pos) != dsu.find(tar):\n                ok = False\n                break\n        print("YES" if ok else "NO")\n\nif __name__ == "__main__":\n    main()'
SAMPLE='3\n5\n5 4 3 2 1\n1 1 1 1 1\n7\n4 3 5 1 2 7 6\n4 6 6 1 6 6 1\n7\n4 2 5 1 3 7 6\n4 6 6 1 6 6 1\n'
GENERATOR_NAME='g29677'

def valid(text):
    """题面契约：T<=20；每组 N<=10000，t 为 1..N 的排列，d 为 N 个正整数；每组恰三行。"""
    import re
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    tok = re.compile(r'^[0-9]+$')
    def ints(line):
        parts = line.split(' ')
        if any(not tok.match(p) or (len(p) > 1 and p[0] == '0') for p in parts):
            return None
        return [int(p) for p in parts]
    if not lines:
        return False
    h = ints(lines[0])
    if h is None or len(h) != 1:
        return False
    T = h[0]
    if not 1 <= T <= 20 or len(lines) != 1 + 3 * T:
        return False
    for k in range(T):
        a = ints(lines[1 + 3 * k]); t = ints(lines[2 + 3 * k]); d = ints(lines[3 + 3 * k])
        if a is None or t is None or d is None or len(a) != 1:
            return False
        n = a[0]
        if not 1 <= n <= 10000 or len(t) != n or len(d) != n:
            return False
        if sorted(t) != list(range(1, n + 1)):
            return False
        if any(x < 1 for x in d):
            return False
    return True


def _components(n, d):
    # 独立于参考解的连通分量（BFS），用于构造 YES/NO
    adj = [[] for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in (i + d[i - 1], i - d[i - 1]):
            if 1 <= j <= n:
                adj[i].append(j); adj[j].append(i)
    comp = [0] * (n + 1); c = 0
    for s in range(1, n + 1):
        if comp[s]:
            continue
        c += 1; comp[s] = c; st = [s]
        while st:
            u = st.pop()
            for v in adj[u]:
                if not comp[v]:
                    comp[v] = c; st.append(v)
    return comp

def _one(r, n, kind, want_yes):
    if kind == 'ones':
        d = [1] * n
    elif kind == 'small':
        d = [r.randint(1, 3) for _ in range(n)]
    elif kind == 'const':
        k = r.randint(2, max(2, min(50, n))); d = [k] * n
    elif kind == 'huge':
        d = [r.randint(n, 10 ** 9) for _ in range(n)]
    elif kind == 'half':
        d = [r.randint(max(1, n // 2), n) for _ in range(n)]
    elif kind == 'sparse':
        # 大部分位置的 d 超出书架，只有少数位置能交换
        d = [r.randint(1, n) if r.random() < 0.3 else r.randint(n, 2 * n) for _ in range(n)]
    else:
        d = [r.randint(1, n) for _ in range(n)]
    comp = _components(n, d)
    groups = {}
    for i in range(1, n + 1):
        groups.setdefault(comp[i], []).append(i)
    t = [0] * (n + 1)
    for g in groups.values():
        h = g[:]; r.shuffle(h)
        for p, b in zip(g, h):
            t[p] = b
    if not want_yes and len(groups) >= 2:
        # 跨两个分量交换一对书 -> 必然 NO
        ks = list(groups); a, b = r.sample(ks, 2)
        p = r.choice(groups[a]); q = r.choice(groups[b])
        t[p], t[q] = t[q], t[p]
    return n, t[1:], d

def g29677(r, idx):
    cases = []
    kinds = ['ones', 'small', 'const', 'huge', 'half', 'sparse', 'rand']
    if idx == 1:
        # 最小规模
        cases = [(1, [1], [1]), (1, [1], [10 ** 9]), (2, [2, 1], [1, 1]), (2, [2, 1], [5, 5]), (2, [1, 2], [3, 3])]
    elif idx <= 8:
        # 满规模：N=10000
        T = 8
        for _ in range(T):
            cases.append(_one(r, 10000, r.choice(kinds), r.random() < 0.5))
    elif idx <= 12:
        T = 20
        for _ in range(T):
            cases.append(_one(r, r.randint(2000, 4000), r.choice(kinds), r.random() < 0.5))
    elif idx <= 24:
        T = r.randint(1, 20)
        for _ in range(T):
            cases.append(_one(r, r.randint(1, 10), r.choice(kinds), r.random() < 0.5))
    else:
        T = r.randint(1, 20)
        for _ in range(T):
            cases.append(_one(r, r.randint(1, 300), r.choice(kinds), r.random() < 0.5))
    rows = [str(len(cases))]
    for n, t, d in cases:
        rows.extend((str(n), " ".join(map(str, t)), " ".join(map(str, d))))
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
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed), seed) for seed in range(1, 40)]
    for i, case in enumerate(cases):
        assert valid(case), i
        assert len(case) <= 1 << 20, i
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()
