import random, subprocess, sys, tempfile
from pathlib import Path
def g1384(r):
    out = [str(r.randint(1, 4))]
    for _ in range(int(out[0])):
        empty = r.randint(1, 300); target = empty + r.randint(1, 600); n = r.randint(1, 12)
        out += [f"{empty} {target}", str(n)]
        out += [f"{r.randint(1,100)} {r.randint(1,80)}" for _ in range(n)]
    return "\n".join(out) + "\n"


def valid(text):
    """题面契约：首行 T；每组 E F（1<=E<=F<=10000），N（1<=N<=500），N 行 P W（1<=P<=50000，1<=W<=10000）。"""
    lines = [ln.split() for ln in text.split("\n") if ln.strip()]
    try:
        if not lines or len(lines[0]) != 1:
            return False
        T = int(lines[0][0]); i = 1
        if T < 1:
            return False
        for _ in range(T):
            if i + 2 > len(lines) or len(lines[i]) != 2 or len(lines[i + 1]) != 1:
                return False
            E, F = map(int, lines[i]); N = int(lines[i + 1][0]); i += 2
            if not (1 <= E <= F <= 10000 and 1 <= N <= 500) or i + N > len(lines):
                return False
            for k in range(N):
                if len(lines[i + k]) != 2:
                    return False
                P, W = map(int, lines[i + k])
                if not (1 <= P <= 50000 and 1 <= W <= 10000):
                    return False
            i += N
        return i == len(lines)
    except ValueError:
        return False


def _case1384(E, F, coins):
    return [f"{E} {F}", str(len(coins))] + [f"{p} {w}" for p, w in coins]


def g1384_v2(r, seed):
    cs = []
    if seed == 1:     # 边界：E==F（0）；单枚硬币恰好/除不尽；答案 4.9995e8（INF 取 1e8/1e9 不够或刚好）
        cs.append(_case1384(5, 5, [(7, 3)]))
        cs.append(_case1384(1, 10000, [(50000, 1)]))
        cs.append(_case1384(1, 10000, [(50000, 2)]))
        cs.append(_case1384(1, 10000, [(1, 10000)]))
        cs.append(_case1384(1, 10001 - 1, [(50000, 9999)]))
        cs.append(_case1384(10000, 10000, [(1, 1)]))
    elif seed <= 20:  # 随机中小规模，含无解（重量都是某数倍数）
        for _ in range(r.randint(2, 8)):
            E = r.randint(1, 5000); F = r.randint(E, min(10000, E + r.choice([10, 100, 1000, 3000])))
            n = r.randint(1, 30); g = r.choice([1, 1, 2, 3, 7])
            coins = [(r.randint(1, 50000), g * r.randint(1, max(1, 300 // g))) for _ in range(n)]
            cs.append(_case1384(E, F, coins))
    elif seed <= 32:  # 满规模：F-E=9999，N=500
        E = r.randint(1, 1); F = 10000
        g = 1 if seed % 4 else r.choice([2, 3])
        coins = [(r.randint(1, 50000), g * r.randint(1, 10000 // g)) for _ in range(500)]
        if seed % 3 == 0:  # 大面额轻币，答案很大
            coins = [(r.randint(40000, 50000), r.randint(1, 20)) for _ in range(500)]
        cs.append(_case1384(E, F, coins))
    else:             # 两组较大规模
        for _ in range(2):
            E = r.randint(1, 2000); F = r.randint(E + 4000, 10000)
            coins = [(r.randint(1, 50000), r.randint(1, 10000)) for _ in range(r.randint(200, 500))]
            cs.append(_case1384(E, F, coins))
    return "\n".join([str(len(cs))] + [ln for c in cs for ln in c]) + "\n"

REFERENCE='# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 1384: Piggy-Bank\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024fallroutine/01384/\n# License: not declared in source collection; no license is inferred.\nINF = float("inf")\nTC = int(input())\nfor _ in range(TC):\n    E, F = map(int, input().split())\n    N = int(input())\n    coins = []\n    for _ in range(N):\n        p, w = map(int, input().split())\n        coins.append((p, w))\n\n    amount = F - E\n    dp = [0] + [INF]*amount\n\n    for i in range(N):\n        p, w = coins[i]\n        for j in range(w, amount+1):\n            if dp[j-w] != INF:\n                dp[j] = min(dp[j], dp[j-w] + p)\n\n    #print(dp)\n    if dp[-1] != INF:\n        print(f"The minimum amount of money in the piggy-bank is {dp[-1]}.")\n    else:\n        print(f"This is impossible.")\n'
SAMPLE='3\n10 110\n2\n1 1\n30 50\n10 110\n2\n1 1\n50 30\n1 6\n2\n10 3\n20 4\n'
GENERATOR='g1384'

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as folder:
        script=Path(folder)/"main.py"; script.write_text(REFERENCE)
        result=subprocess.run([sys.executable,"-I",str(script)],input=text,text=True,capture_output=True,timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    for old in data.glob("*"): old.unlink()
    cases=[SAMPLE]+[g1384_v2(random.Random(seed), seed) for seed in range(1, 40)]
    for i,case in enumerate(cases):
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()
