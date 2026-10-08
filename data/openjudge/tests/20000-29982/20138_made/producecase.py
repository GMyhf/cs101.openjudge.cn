import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/20138 statistics, Accepted solution 52543271.\n# Source: http://cs101.openjudge.cn/practice/solution/52543271/\n# Statistics: http://cs101.openjudge.cn/practice/20138/statistics/\n# License: not declared on submission page; no license inferred\nimport sys\nfrom collections import defaultdict, deque, Counter\nfrom itertools import accumulate, permutations, combinations\nfrom heapq import heappush, heappop, heapify\nfrom bisect import bisect_left, bisect_right\nfrom functools import lru_cache\nfrom copy import deepcopy\nfrom fractions import Fraction\nfrom math import gcd\n\nsys.setrecursionlimit(2000000)\n\ninput = sys.stdin.readline\n\n\ndef lcm(a: int, b: int):\n    return a * b // gcd(a, b)\n\n\nn = int(input())\ncoef = [list(map(float, input().split())) for _ in range(n)]\n\nans = [0] * n\n\nfor i in range(n):\n    for j in range(i, n):\n        if coef[j][i] != 0:\n            coef[j], coef[i] = coef[i], coef[j]\n            break\n\n    for j in range(i + 1, n):\n        if coef[j][i] == 0:\n            continue\n        d = coef[j][i] / coef[i][i]\n        for k in range(i, n + 1):\n            coef[j][k] -= coef[i][k] * d\n\n\nfor i in range(n - 1, -1, -1):\n    b = coef[i][n]\n    for j in range(i + 1, n):\n        b -= coef[i][j] * ans[j]\n    ans[i] = b / coef[i][i]\n\n\nfor i, x in enumerate(ans):\n    print(f"x{i+1} = {float(x):.2f}")\n'
SAMPLE='3\n2 3 1 6\n1 -1 2 -1\n1 2 -1 5\n'
GENERATOR_NAME='g20138'

# 题面：2<=n<=300；接下来 n 行，每行 n+1 个整数（增广矩阵）；方程组保证有唯一解。
_PRIMES = (1000000007, 998244353)


def _rank_full_mod(rows, n, p):
    a = [[v % p for v in row[:n]] for row in rows]
    for c in range(n):
        piv = next((i for i in range(c, n) if a[i][c]), None)
        if piv is None:
            return False
        a[c], a[piv] = a[piv], a[c]
        inv = pow(a[c][c], p - 2, p)
        for i in range(c + 1, n):
            if a[i][c]:
                f = a[i][c] * inv % p
                ai, ac = a[i], a[c]
                for k in range(c, n):
                    ai[k] = (ai[k] - f * ac[k]) % p
    return True


def _det_nonzero(rows, n):
    if any(_rank_full_mod(rows, n, p) for p in _PRIMES):
        return True
    from fractions import Fraction
    a = [[Fraction(v) for v in row[:n]] for row in rows]
    for c in range(n):
        piv = next((i for i in range(c, n) if a[i][c] != 0), None)
        if piv is None:
            return False
        a[c], a[piv] = a[piv], a[c]
        for i in range(c + 1, n):
            f = a[i][c] / a[c][c]
            for k in range(c, n):
                a[i][k] -= f * a[c][k]
    return True


def valid(text):
    import re
    if not text.endswith("\n") or text.endswith("\n\n"):
        return False
    lines = text[:-1].split("\n")
    if not re.fullmatch(r"[1-9]\d*", lines[0]):
        return False
    n = int(lines[0])
    if not 2 <= n <= 300 or len(lines) != n + 1:
        return False
    rows = []
    for line in lines[1:]:
        toks = line.split(" ")
        if len(toks) != n + 1 or not all(re.fullmatch(r"-?(0|[1-9]\d*)", t) for t in toks):
            return False
        rows.append([int(t) for t in toks])
    return _det_nonzero(rows, n)


def _build(r, n, perm=False, sparse=False, denoms=(1,), lo=1, hi=20):
    """构造 B（严格对角占优）和非零整数 y，A=B·diag(d)，b=B·y，真解 x_j=y_j/d_j。
    d∈{1,2,4} 让答案是 .00/.25/.50/.75，保留两位小数没有舍入歧义；x 不取 0，避开 -0.00。"""
    y = [r.randint(lo, hi) * r.choice((-1, 1)) for _ in range(n)]
    d = [r.choice(denoms) for _ in range(n)]
    rows = []
    for i in range(n):
        b = [0 if (sparse and r.random() < .7) else r.randint(-5, 5) for _ in range(n)]
        b[i] = 0
        b[i] = (sum(abs(v) for v in b) + r.randint(1, 9)) * r.choice((-1, 1))
        rhs = sum(b[j] * y[j] for j in range(n))
        rows.append([b[j] * d[j] for j in range(n)] + [rhs])
    if perm:
        r.shuffle(rows)
    return f"{n}\n" + "\n".join(" ".join(map(str, row)) for row in rows) + "\n"


def g20138(r, seed):
    if seed <= 3:      # 原有的小规模随机组（对角线固定 10、整数解），保留一部分
        n = r.randint(2, 7)
        x = [r.randint(1, 5) * r.choice((-1, 1)) for _ in range(n)]
        matrix = []
        for i in range(n):
            row = [r.randint(-2, 2) for _ in range(n)]
            row[i] = 10
            row.append(sum(row[j] * x[j] for j in range(n)))
            matrix.append(row)
        return f"{n}\n" + "\n".join(" ".join(map(str, row)) for row in matrix) + "\n"
    if seed <= 6:      # 最小规模 n=2，含需要换行的情形
        return _build(r, 2, perm=seed != 4, denoms=(1, 2, 4))
    if seed <= 18:     # 小规模，行打乱 + 稀疏：对角线上常出现 0，不换主元直接除会出错
        return _build(r, r.randint(3, 10), perm=True, sparse=True, denoms=(1, 2, 4))
    if seed <= 26:     # 中等规模，小数解
        return _build(r, r.randint(11, 60), perm=seed % 2 == 0, sparse=seed % 3 == 0, denoms=(1, 2, 4))
    if seed <= 33:     # 较大规模
        return _build(r, r.choice((100, 150, 200, 250, 280, 299, 300)), perm=seed % 2 == 0,
                      sparse=seed % 3 == 0, denoms=(1, 2, 4), hi=100)
    return _build(r, 300, perm=seed % 2 == 1, sparse=seed == 36, denoms=(1, 2, 4), hi=1000)

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        src=Path(d)/'main.py'; src.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(src)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[g20138(random.Random(seed), seed) for seed in range(1, 40)]
    for i,text in enumerate(cases):
        (data/f'{i}.in').write_text(text); (data/f'{i}.out').write_text(run(text))
if __name__=='__main__': main()
