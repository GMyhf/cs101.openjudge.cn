import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/20138 statistics, Accepted solution 52543271.\n# Source: http://cs101.openjudge.cn/practice/solution/52543271/\n# Statistics: http://cs101.openjudge.cn/practice/20138/statistics/\n# License: not declared on submission page; no license inferred\nimport sys\nfrom collections import defaultdict, deque, Counter\nfrom itertools import accumulate, permutations, combinations\nfrom heapq import heappush, heappop, heapify\nfrom bisect import bisect_left, bisect_right\nfrom functools import lru_cache\nfrom copy import deepcopy\nfrom fractions import Fraction\nfrom math import gcd\n\nsys.setrecursionlimit(2000000)\n\ninput = sys.stdin.readline\n\n\ndef lcm(a: int, b: int):\n    return a * b // gcd(a, b)\n\n\nn = int(input())\ncoef = [list(map(float, input().split())) for _ in range(n)]\n\nans = [0] * n\n\nfor i in range(n):\n    for j in range(i, n):\n        if coef[j][i] != 0:\n            coef[j], coef[i] = coef[i], coef[j]\n            break\n\n    for j in range(i + 1, n):\n        if coef[j][i] == 0:\n            continue\n        d = coef[j][i] / coef[i][i]\n        for k in range(i, n + 1):\n            coef[j][k] -= coef[i][k] * d\n\n\nfor i in range(n - 1, -1, -1):\n    b = coef[i][n]\n    for j in range(i + 1, n):\n        b -= coef[i][j] * ans[j]\n    ans[i] = b / coef[i][i]\n\n\nfor i, x in enumerate(ans):\n    print(f"x{i+1} = {float(x):.2f}")\n'
SAMPLE='3\n2 3 1 6\n1 -1 2 -1\n1 2 -1 5\n'
GENERATOR_NAME='g20138'
def g20138(r):
    n = r.randint(2, 7)
    x = [r.randint(-5, 5) for _ in range(n)]
    matrix = []
    for i in range(n):
        row = [r.randint(-2, 2) for _ in range(n)]
        row[i] = 10
        row.append(sum(row[j] * x[j] for j in range(n)))
        matrix.append(row)
    return f"{n}\n" + "\n".join(" ".join(map(str, row)) for row in matrix) + "\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        src=Path(d)/'main.py'; src.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(src)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f'{i}.in').write_text(text); (data/f'{i}.out').write_text(run(text))
if __name__=='__main__': main()
