import random
# 原内嵌参考解（提交 52723659，即 samplecode.py）枚举子集的子集要 3^n，n=16 时约 9s；
# 换成「下一批必含编号最小的未过桥者」的等价 DP，只走可达状态，n=16 约 1.5s。samplecode.py 仍用来对拍。
REFERENCE='import sys\ndef main():\n    d = sys.stdin.read().split()\n    W, n = int(d[0]), int(d[1])\n    t = [int(d[2 + 2 * i]) for i in range(n)]; w = [int(d[3 + 2 * i]) for i in range(n)]\n    size = 1 << n\n    sw = [0] * size; mt = [0] * size\n    for s in range(1, size):\n        lb = s & -s; i = lb.bit_length() - 1; p = s ^ lb\n        sw[s] = sw[p] + w[i]; mt[s] = mt[p] if mt[p] > t[i] else t[i]\n    full = size - 1\n    INF = 1 << 60\n    dp = [INF] * size; dp[0] = 0\n    for mask in range(size - 1):\n        base = dp[mask]\n        if base == INF: continue\n        rem = full ^ mask\n        lb = rem & -rem\n        rest = rem ^ lb\n        sub = rest\n        while True:\n            g = sub | lb\n            if sw[g] <= W:\n                v = base + mt[g]\n                nm = mask | g\n                if v < dp[nm]: dp[nm] = v\n            if sub == 0: break\n            sub = (sub - 1) & rest\n    print(dp[full])\nmain()\n'
SAMPLE='100 3\n24 60\n10 40\n18 50\n'
GENERATOR_NAME='g30192'
CPP=False
def valid(text):
    # 题面：第一行 W n；接着 n 行 t w；100<=W<=400，1<=n<=16，1<=t<=50，10<=w<=100
    if not text.endswith('\n'): return False
    lines = text[:-1].split('\n')
    try:
        rows = [[int(x) for x in ln.split(' ')] for ln in lines]
    except ValueError: return False
    if len(rows[0]) != 2: return False
    W, n = rows[0]
    if not (100 <= W <= 400 and 1 <= n <= 16) or len(rows) != n + 1: return False
    return all(len(r) == 2 and 1 <= r[0] <= 50 and 10 <= r[1] <= 100 for r in rows[1:])

def fmt(W, ppl):
    return f"{W} {len(ppl)}\n" + "\n".join(f"{t} {w}" for t, w in ppl) + "\n"

def g30192(r):
    # 题面：100 <= W <= 400，1 <= n <= 16，1 <= t <= 50，10 <= w <= 100。
    n = r.randint(1, 7)
    return f"{r.randint(100, 400)} {n}\n" + "\n".join(f"{r.randint(1,50)} {r.randint(10,100)}" for _ in range(n)) + "\n"

def extra_cases():
    # 原数据 n 只到 7，补 n=16 满规模与边界
    r = random.Random(30192)
    out = []
    out.append(fmt(100, [(50, 100)]))                      # n=1，重量恰好等于 W
    out.append(fmt(400, [(r.randint(1, 50), 10) for _ in range(16)]))   # 全员可一起过：答案 = max t
    out.append(fmt(100, [(r.randint(1, 50), 100) for _ in range(16)]))  # 只能一个个过：答案 = sum t
    out.append(fmt(400, [(50, 10)] * 16))
    out.append(fmt(100, [(1, 50), (50, 50), (1, 50), (50, 50)]))     # 恰好凑满 W
    for W in (100, 150, 200, 250, 300, 350, 400, 400, 400, 237):
        out.append(fmt(W, [(r.randint(1, 50), r.randint(10, 100)) for _ in range(16)]))
    for _ in range(4):
        out.append(fmt(r.randint(100, 400), [(r.randint(1, 50), r.randint(10, 40)) for _ in range(16)]))
    for n in (15, 14, 12, 10, 9, 8):
        out.append(fmt(r.randint(100, 400), [(r.randint(1, 50), r.randint(10, 100)) for _ in range(n)]))
    return out

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
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1, 40)]+extra_cases()
    assert all(valid(c) for c in cases) and len(set(cases))==len(cases)
    for i,c in enumerate(cases): (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
