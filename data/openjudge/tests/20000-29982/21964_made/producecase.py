import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/21964/\n# Accepted submission: 52244442\n# Source: http://cs101.openjudge.cn/practice/solution/52244442/\n# License: not declared on the submission page; no license is inferred.\n\nn,m=map(int,input().split())\nneed=[]\nvalue=[]\nfor i in range(n):\n    a,b=map(int,input().split())\n    need.append(a)\n    value.append(b)\ndp=[0]*(m+1)\nfor i in range(n):\n    w=need[i]\n    for j in range(m,w-1,-1):\n        dp[j]=max(dp[j],dp[j-w]+value[i])\nprint(dp[m])'
SAMPLE='5 1000\n144 990\n487 436\n210 673\n567 58\n1056 897\n'
GENERATOR_NAME='g21964'
def g21964(r):
    n, m = r.randint(1, 30), r.randint(20, 1000)
    return f"{n} {m}\n" + "\n".join(f"{r.randint(1, min(200000, m))} {r.randint(0, 1000)}" for _ in range(n)) + "\n"

def valid(text):
    """题面：首行正整数 N、M（N<=500，M<=1e5）；随后 N 行，每行两个整数 need、value（need<=2e5，value<=1e3）。"""
    try:
        if not text.endswith("\n"): return False
        lines = text[:-1].split("\n")
        head = lines[0].split(" ")
        if len(head) != 2 or not all(t.isdigit() for t in head): return False
        n, m = map(int, head)
        if not (1 <= n <= 500 and 1 <= m <= 100000) or len(lines) != n + 1: return False
        for line in lines[1:]:
            t = line.split(" ")
            if len(t) != 2 or not all(x.isdigit() for x in t): return False
            a, b = map(int, t)
            if not (0 <= a <= 200000 and 0 <= b <= 1000): return False
        return True
    except Exception:
        return False

def extra_cases():
    """补充：满规模/边界/贪心陷阱组（追加在原 40 组之后，参考解单组 < 5s）。"""
    def fmt(m, items): return f"{len(items)} {m}\n" + "".join(f"{a} {b}\n" for a, b in items)
    r = random.Random(219640)
    out = []
    # 大规模 N=400, M=1e5，need 取满值域 [1, 2e5]（约一半物品放不进）；
    # 原为 N=500（约 1.34e7 次内层循环，参考解在负载下 5s+，超过 Python 单组 10s 时限的一半），取前 400 件，随机流不变
    out.append(fmt(100000, [(r.randint(1, 200000), r.randint(0, 1000)) for _ in range(500)][:400]))
    # N=500, M=1e5，need 都很大：只能挑 1 件，含 need>M 的物品
    out.append(fmt(100000, [(r.randint(40000, 200000), r.randint(0, 1000)) for _ in range(500)]))
    # N=500, M=2e4，need 小：容量充分利用
    out.append(fmt(20000, [(r.randint(1, 2000), r.randint(0, 1000)) for _ in range(500)]))
    # N=100, M=1e5，need 中等
    out.append(fmt(100000, [(r.randint(1, 5000), r.randint(1, 1000)) for _ in range(100)]))
    # 贪心（按性价比）陷阱：重复若干组 (6,1000)+(5,830)x2 型
    items = []
    for _ in range(100): items += [(6, 1000), (5, 830), (5, 830)]
    r.shuffle(items)
    out.append(fmt(1004, items))   # 贪心：100 件 6 + 80 件 5 = 1004 剩 4 → 166400；最优 99 件 6 + 82 件 5 = 167060
    # 最小规模、放不下、恰好装满、价值全 0
    out.append(fmt(1, [(1, 1000)]))
    out.append(fmt(1, [(200000, 1000)]))
    out.append(fmt(100000, [(200000, r.randint(1, 1000)) for _ in range(500)]))
    out.append(fmt(1500, [(i, 1000) for i in range(1, 51)] + [(1, 0)] * 50))
    out.append(fmt(100000, [(r.randint(1, 200000), 0) for _ in range(150)]))
    # 所有物品恰好全部装下（总 need = M）
    needs = [r.randint(1, 60) for _ in range(500)]
    out.append(fmt(sum(needs), [(a, r.randint(0, 1000)) for a in needs]))
    return out

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+(['8\n','9\n'] if GENERATOR_NAME == 'g22007' else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1, 40)]
    if GENERATOR_NAME == 'g21964': cases += extra_cases()
    assert all(valid(c) for c in cases)
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
