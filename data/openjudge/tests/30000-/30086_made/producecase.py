import random
REFERENCE='# External reference: /practice/30086/statistics/\n# Accepted submission: 52211740\n# Source: http://cs101.openjudge.cn/practice/solution/52211740/\n# License: not declared on the submission page; no license is inferred.\n\nn,d=[int(i) for i in input().split()]\nl=[int(i) for i in input().split()]\nl.sort()\nstatus="Yes"\nfor i in range(n):\n    a=l[2*i]\n    b=l[2*i+1]\n    if abs(a-b)>d:\n        status="No"\n        break\nprint(status)'
SAMPLE='6 4\n22 15 32 36 16 30 42 30 39 23 17 18\n'
GENERATOR_NAME='g30086'
CPP=False
import re as _re

def valid(text):
    """题面只给格式、未给数据范围：第一行两个整数 N,D；第二行 2N 个整数。
    这里额外只要求 N ≥ 1、D ≥ 0、身高为非负整数（身高差/身高的自然含义）。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    if len(lines) != 2 or not _re.fullmatch(r'[1-9]\d* (0|[1-9]\d*)', lines[0]):
        return False
    n = int(lines[0].split()[0])
    toks = lines[1].split(' ')
    return len(toks) == 2 * n and all(_re.fullmatch(r'0|[1-9]\d*', t) for t in toks)

def g30086(r):
    # 旧版生成器：N ≤ 30、身高 ≤ 100；新数据见 build_cases()
    n, d = r.randint(1, 30), r.randint(0, 20)
    a = [r.randint(0, 100) for _ in range(2*n)]
    return f"{n} {d}\n{' '.join(map(str,a))}\n"

def _fmt(d, a):
    return f"{len(a) // 2} {d}\n" + " ".join(map(str, a)) + "\n"

def _pairs(r, n, d, lo, hi, bad=0):
    """构造 n 对差 ≤ d 的身高（再打乱）；bad>0 时把其中 bad 对改成差恰为 d+1 且与其他值隔开。"""
    a = []
    for i in range(n):
        x = r.randint(lo, hi)
        a += [x, x + r.randint(0, d)]
    if bad:
        top = max(a) + d + 10 ** 3
        for k in range(bad):
            a[2 * k], a[2 * k + 1] = top, top + d + 1
            top += 2 * d + 10 ** 3
    r.shuffle(a)
    return a

def build_cases():
    r = random.Random(30086)
    cases = [SAMPLE]
    cases += [_fmt(0, [5, 5]), _fmt(0, [5, 6]), _fmt(3, [1, 4]), _fmt(3, [1, 5]),
              _fmt(0, [7, 3, 3, 7]), _fmt(1, [1, 2, 3, 4]), _fmt(1, [1, 3, 2, 4]),
              _fmt(2, [1, 2, 5, 6, 9, 10]),                     # 对内近、对间远 → Yes（卡“所有相邻差都 ≤ D”）
              _fmt(2, [1, 4, 5, 8]),                            # 相邻配对 1-4 不行 → No
              _fmt(10 ** 9, [1, 10 ** 9]),                      # 大 D
              _fmt(0, [10 ** 9, 10 ** 9, 1, 1])]
    N = 40000                                                    # 2N 个 ≤1e9 的数约 0.88MB
    cases.append(_fmt(0, [r.randint(1, 10 ** 9)] * (2 * N)))
    cases.append(_fmt(0, _pairs(r, N, 0, 1, 10 ** 9)))                     # D=0，全部成对相等 → Yes
    cases.append(_fmt(0, _pairs(r, N, 0, 1, 10 ** 9, bad=1)))              # D=0，一对相差 1 → No
    cases.append(_fmt(10 ** 9, [r.randint(1, 10 ** 9) for _ in range(2 * N)]))  # D 极大 → Yes
    cases.append(_fmt(1000, _pairs(r, N, 1000, 1, 10 ** 9 - 1000)))
    cases.append(_fmt(1000, _pairs(r, N, 1000, 1, 10 ** 9 - 10 ** 7, bad=1)))
    cases.append(_fmt(5, _pairs(r, N, 5, 1, 10 ** 6)))
    cases.append(_fmt(5, _pairs(r, N, 5, 1, 10 ** 6, bad=3)))
    cases.append(_fmt(10 ** 4, sorted(_pairs(r, N, 10 ** 4, 1, 10 ** 8))))         # 已排序输入
    cases.append(_fmt(10 ** 4, sorted(_pairs(r, N, 10 ** 4, 1, 10 ** 8), reverse=True)))
    cases.append(_fmt(25000, [r.randint(1, 10 ** 9) for _ in range(2 * N)]))     # 纯随机大概率 Yes/No 皆可
    # 小规模随机（可暴力核对），Yes/No 各半
    for t in range(10):
        n = r.randint(1, 6); d = r.randint(0, 10)
        cases.append(_fmt(d, _pairs(r, n, d, 1, 60, bad=t % 2)))
    for t in range(7):
        n = r.choice([100, 1000, 10000, N]); d = r.randint(0, 10 ** 6)
        cases.append(_fmt(d, _pairs(r, n, d, 1, 10 ** 8, bad=t % 2)))
    assert len(cases) == 40, len(cases)   # catalog.json 登记了 0..39 共 40 组
    return cases

from pathlib import Path
import subprocess, sys, tempfile
def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/('main.cpp' if CPP else 'main.py'); p.write_text(REFERENCE)
        if CPP:
            exe=Path(d)/'main'; c=subprocess.run(['g++','-O2','-std=c++17',str(p),'-o',str(exe)],capture_output=True,text=True,timeout=30)
            if c.returncode: raise SystemExit(c.stderr)
            cmd=[str(exe)]
        else: cmd=[sys.executable,str(p)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=build_cases()
    assert all(valid(c) for c in cases)
    for i,c in enumerate(cases): (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
