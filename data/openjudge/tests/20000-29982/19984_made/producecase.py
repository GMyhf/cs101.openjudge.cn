import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/19984 statistics, Accepted solution 22475453.\n# Source: http://cs101.openjudge.cn/practice/solution/22475453/\n# Statistics: http://cs101.openjudge.cn/practice/19984/statistics/\n# License: not declared on submission page; no license inferred\nn=int(input())\nf=[-1]*(n+1)\np=[]\nf[0]=float(input())\nfor i in range(n):\n    p.append(tuple(map(float,input().split())))\nf[1]=(2*f[0]+100)/p[0][0]\nb=[0]*n\nfor i in range(1,n):\n    for j in range(i+1):\n        if p[i][j]==0:\n            continue\n        if f[i+1]==-1:\n            f[i+1]=(f[i]+f[j]+100-(1-p[i][j])*f[i-1])/p[i][j]\n            b[i]=j\n        elif f[i+1]>(f[i]+f[j]+100-(1-p[i][j])*f[i-1])/p[i][j]:\n            f[i+1]=(f[i]+f[j]+100-(1-p[i][j])*f[i-1])/p[i][j]\n            b[i]=j\nprint(\' \'.join(map(str,b)))\nprint("%.2f" % f[n])\n'
SAMPLE='2\n100\n1\n0.8 0.95\n'
GENERATOR_NAME='g19984'
def g19984(r):
    n = r.randint(2, 8)
    rows = []
    for i in range(n):
        rows.append(" ".join(f"{r.uniform(.15, .95):.4f}" for _ in range(i + 1)))
    return f"{n}\n{r.randint(50, 500)}\n" + "\n".join(rows) + "\n"

def _routes(n, f0, p):
    """按题意逐级求最低成本；返回 (每级候选成本列表, 价格表)。p==0 的反应不可用。"""
    f = [float(f0)] + [None] * n
    f[1] = (2 * f[0] + 100) / p[0][0]
    cands = []
    for i in range(1, n):
        c = [((f[i] + f[j] + 100 - (1 - p[i][j]) * f[i - 1]) / p[i][j], j)
             for j in range(i + 1) if p[i][j] > 0]
        if not c:
            return None, None
        cands.append(c)
        f[i + 1] = min(c)[0]
    return cands, f

def valid(text):
    """题面契约：n（1<=n<=20，n=0 无意义）；物质 0 的价格为整数；随后 n 行，第 i 行
    i 个实数 0<=p<=1。另核题面「保证最优路线唯一」：每级最优辅助试剂唯一（相对差 >1e-9），
    且 p[0][0]>0、每级至少有一个可用反应（否则无路线可言）。"""
    import re
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) < 2 or not re.fullmatch(r"[1-9]\d*", lines[0]) or not re.fullmatch(r"-?\d+", lines[1]):
        return False
    n = int(lines[0])
    if n > 20 or len(lines) != n + 2:
        return False
    p = []
    for i, ln in enumerate(lines[2:]):
        tok = ln.split(" ")
        if len(tok) != i + 1 or not all(re.fullmatch(r"\d+(\.\d+)?", x) for x in tok):
            return False
        row = [float(x) for x in tok]
        if not all(0 <= x <= 1 for x in row):
            return False
        p.append(row)
    if p[0][0] <= 0:
        return False
    cands, f = _routes(n, int(lines[1]), p)
    if cands is None:
        return False
    for c in cands:
        c = sorted(c)
        if len(c) > 1 and c[1][0] - c[0][0] <= 1e-9 * abs(c[0][0]):
            return False
    return True

def gfull(r, n, zero_rate, one_rate):
    """追加组：n 级，p 里混入 0（反应不可用）与 1（无副产物）；
    重抽直到满足唯一最优且答案远离两位小数的舍入边界。"""
    while True:
        rows = []
        for i in range(n):
            row = []
            for j in range(i + 1):
                x = r.random()
                row.append("0" if x < zero_rate and (i, j) != (0, 0) else "1" if x < zero_rate + one_rate
                           else f"{r.uniform(.05, .99):.4f}")
            rows.append(" ".join(row))
        text = f"{n}\n{r.randint(1, 1000)}\n" + "\n".join(rows) + "\n"
        if not valid(text):
            continue
        _, f = _routes(n, int(text.split("\n")[1]), [[float(x) for x in ln.split()] for ln in rows])
        frac = (f[n] * 100) % 1
        if abs(frac - 0.5) > 1e-4:
            return text

EXTRA = [  # (种子, n, p=0 比例, p=1 比例)
    (401, 1, 0, 0), (402, 1, 0, 1),
    (403, 20, 0, 0), (404, 20, .2, .05), (405, 20, .4, 0), (406, 20, 0, .15),
    (407, 15, .3, .1), (408, 12, .1, 0), (409, 3, .5, .2), (410, 2, 0, 0),
]

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        src=Path(d)/'main.py'; src.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(src)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 30)]  # 尾部 10 组让给下面的定制组，总数仍为 40（catalog 按文件列组）
    cases+=[gfull(random.Random(sd), n, z, o) for sd, n, z, o in EXTRA]
    assert len(cases) == 40 and len(set(cases)) == 40 and all(valid(c) for c in cases)
    for i,text in enumerate(cases):
        (data/f'{i}.in').write_text(text); (data/f'{i}.out').write_text(run(text))
if __name__=='__main__': main()
