import random, subprocess, sys, tempfile
from pathlib import Path
def g1384(r):
    out = [str(r.randint(1, 4))]
    for _ in range(int(out[0])):
        empty = r.randint(0, 300); target = empty + r.randint(1, 600); n = r.randint(1, 12)
        out += [f"{empty} {target}", str(n)]
        out += [f"{r.randint(1,100)} {r.randint(1,80)}" for _ in range(n)]
    return "\n".join(out) + "\n"

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
    cases=[SAMPLE]+[globals()[GENERATOR](random.Random(seed)) for seed in range(1,21)]
    for i,case in enumerate(cases):
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()
