import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: cs101.openjudge.cn practice/20004 statistics, Accepted solution 43218123.\n# Source: http://cs101.openjudge.cn/practice/solution/43218123/\n# Statistics: http://cs101.openjudge.cn/practice/20004/statistics/\n# License: not declared on submission page; no license inferred\nr=[float(i[:-1])/100 for i in input().split()]\nt=[1+r[0]]\nfor i in r[1:]:\n    t.append(t[-1]*(1+i))\nl=len(t)\nmmin=[(t[-1],l-1)]\nfor i in range(1,len(r)):\n    if t[l-i-1]<mmin[i-1][0]:\n        mmin.append((t[l-i-1],l-i-1))\n    else:\n        mmin.append(mmin[i-1])\nans,pos=0,0\nfor i in range(len(t)):\n    if ans<(t[i]-mmin[l-i-1][0])/t[i]:\n        ans=(t[i]-mmin[l-i-1][0])/t[i]\n        pos=mmin[l-i-1][1]-i\nprint(f'{-1*ans*100:.1f}% {pos}')\n"
SAMPLE='3.5407% -7.1619% -6.8417% -5.6495% 9.0260% 7.7859% -0.6648% -0.8765% -0.5759% -7.8740%\n'
GENERATOR_NAME='g20004'
def g20004(r):
    return " ".join(f"{r.uniform(-9.9, 9.9):.4f}%" for _ in range(r.randint(11, 30))) + "\n"

def valid(text):
    """题面契约：一行涨跌幅序列，长度 x 满足「10<x<10^6」，每项形如 3.5407%，空格分隔。
    注意：题面样例 1 恰有 10 项，与严格的 10<x 冲突；只对样例 1 原文放宽，其余组仍按 10<x<10^6。"""
    import re
    if not text.endswith("\n") or "\n" in text[:-1]:
        return False
    tok = text[:-1].split(" ")
    return (10 < len(tok) or text == SAMPLE) and len(tok) < 10**6 and all(re.fullmatch(r"-?\d+(\.\d+)?%", x) for x in tok)

def drawdown(rates):
    """独立线性算法：从前往后维护历史最高净值（不含买入前的 1.0，与样例 2 一致），
    返回 (最大回撤, 周期, 与「周期不同的次优回撤」的差距)。"""
    best = {}  # 周期 -> 该周期下最大回撤
    v = 1.0; peak = None; peak_i = 0; out = (0.0, 0)
    navs = []
    for x in rates:
        v *= 1 + x / 100; navs.append(v)
    # 后缀最小值（取最靠后的最小位置，与参考解一致；随机数据下不会有相等）
    n = len(navs); suf = [0] * n; m = n - 1
    for i in range(n - 1, -1, -1):
        if navs[i] < navs[m]: m = i
        suf[i] = m
    for i in range(n):
        d = (navs[i] - navs[suf[i]]) / navs[i]; per = suf[i] - i
        if d > best.get(per, -1): best[per] = d
    ranked = sorted(best.items(), key=lambda kv: -kv[1])
    gap = ranked[0][1] - ranked[1][1] if len(ranked) > 1 else 1.0
    return ranked[0][1], ranked[0][0], gap

def gseries(r, n, amp, drift, crash=None):
    """追加组：n 天，日涨跌幅 uniform(-amp, amp)+drift（单位 %），可在某处插一段连续下跌；
    重抽直到有回撤、最优回撤唯一（与次优差 >1e-9）、且百分数离 0.05 舍入边界 >1e-6。"""
    while True:
        xs = [r.uniform(-amp, amp) + drift for _ in range(n)]
        if crash:
            at, length, size = crash
            for k in range(at, min(n, at + length)): xs[k] = -r.uniform(0, size)
        toks = [f"{x:.4f}%" for x in xs]
        d, per, gap = drawdown([float(t[:-1]) for t in toks])
        pct = d * 1000
        if d > 0 and per > 0 and gap > 1e-9 and abs(pct - round(pct - 0.5) - 0.5) > 1e-3:
            return " ".join(toks) + "\n"

SAMPLE2 = "-4.4227% 0.3100% -1.9724% 0.5938% -2.9325% 0.6950% 4.1658% -8.9873% -6.3635% -8.4438% -6.3405% -4.8910%\n"
EXTRA = [  # (种子, 天数, 振幅%, 漂移%, 连续下跌段)
    (601, 11, 9.9, 0, None),               # 题面允许的最短 x=11
    (602, 100000, 0.5, 0.002, None),       # 满额（受 1MB 输入约束）：卡 O(x^2)
    (603, 100000, 0.3, 0.01, None),
    (604, 100000, 1.0, 0.006, (70000, 300, 0.6)),   # 后段一段阴跌
    (605, 100000, 0.4, 0.0, (5, 20, 3.0)),          # 开局就暴跌
    (606, 100000, 0.2, 0.004, (99990, 10, 5.0)),    # 收尾暴跌
    (607, 20000, 2.0, 0.03, None),
    (608, 2000, 9.9, 0.3, None),
]

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        src=Path(d)/'main.py'; src.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(src)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 31)]  # 尾部 9 组让给下面的定制组，总数仍为 40（catalog 按文件列组）
    cases+=[SAMPLE2]+[gseries(random.Random(sd), n, a, dr, c) for sd, n, a, dr, c in EXTRA]
    assert len(cases) == 40 and len(set(cases)) == 40 and all(valid(c) for c in cases)
    for i,text in enumerate(cases):
        (data/f'{i}.in').write_text(text); (data/f'{i}.out').write_text(run(text))
if __name__=='__main__': main()
