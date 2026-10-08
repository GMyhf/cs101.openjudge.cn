import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/21727/\n# Accepted submission: 51529747\n# Source: http://cs101.openjudge.cn/practice/solution/51529747/\n# License: not declared on the submission page; no license is inferred.\n\n# 21727: 湾仔码头\n# 贪心：优先装体积最小的砖\n\nN, M = map(int, input().split())\nbricks = list(map(int, input().split()))\n\ntotal = 0\ncount = 0\n\nfor w in bricks:\n    if total + w <= M:\n        total += w\n        count += 1\n    else:\n        break\n\nprint(count)\n'
SAMPLE='3 100\n2 3 99\n'
GENERATOR_NAME='g21727'
def valid(text):
    """题面：第一行 N M（0<N<=100，0<M<=1000）；第二行 N 个正整数 wi，
    砖的体积各不相同且按升序给出（即严格递增）。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 2:
        return False

    def ints(line):
        toks = line.split(" ")
        if any(not t.isdigit() or (len(t) > 1 and t[0] == "0") for t in toks):
            return None
        return list(map(int, toks))

    a = ints(lines[0]); w = ints(lines[1])
    if a is None or w is None or len(a) != 2:
        return False
    n, m = a
    if not (1 <= n <= 100 and 1 <= m <= 1000) or len(w) != n:
        return False
    if w[0] < 1 or any(w[i] >= w[i + 1] for i in range(n - 1)):
        return False
    return True

def _fmt(m, w):
    return f"{len(w)} {m}\n" + " ".join(map(str, w)) + "\n"

def g21727(r, s):
    k = s - 1
    if k == 0:
        return _fmt(1, [1])                                  # 最小规模，恰好装下
    if k == 1:
        return _fmt(1, [2])                                  # 一块都装不下，答案 0
    if k == 2:
        return _fmt(5, [6, 7, 100, 999, 1000])               # 答案 0
    if k == 3:
        return _fmt(1000, list(range(1, 101)))               # 前 44 块和 990，答案 44
    if k == 4:
        w = list(range(1, 45)); w += [r.randint(1000, 5000)]
        return _fmt(sum(range(1, 45)), sorted(set(w)))       # 总和恰等于 M
    if k == 5:
        w = sorted(r.sample(range(1, 11), 10)); return _fmt(1000, w)   # 全部装下，答案 N
    if k == 6:
        w = sorted(r.sample(range(1, 21), 20)); return _fmt(sum(w), w) # 恰好全部装下
    if k == 7:
        w = sorted(r.sample(range(1, 21), 20)); return _fmt(sum(w) - 1, w)
    if k == 8:
        return _fmt(1000, list(range(901, 1001)))            # n=100，只能装 1 块
    # 其余：严格递增、互不相同的随机体积
    n = r.choice([100, r.randint(1, 100)])
    hi = r.choice([1000, 300, 2000, n + r.randint(0, 50)])
    hi = max(hi, n)
    w = sorted(r.sample(range(1, hi + 1), n))
    m = r.choice([1000, r.randint(1, 1000), min(1000, sum(w[:r.randint(1, n)]))])
    return _fmt(m, w)

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+(['8\n','9\n'] if GENERATOR_NAME == 'g22007' else [])+[g21727(random.Random(s), s) for s in range(1, 40)]
    for i,c in enumerate(cases):
        assert valid(c), i
        (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
