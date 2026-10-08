import random, subprocess, sys, tempfile
from pathlib import Path
def valid(text):
    """题面：第1行组数n，后跟n行，每行一个正整数k (1 <= k < 1000000)。"""
    if not text.endswith("\n"): return False
    lines = text[:-1].split("\n")
    def num(x):
        return x.isdigit() and (x == "0" or x[0] != "0")
    if not lines or not num(lines[0]): return False
    n = int(lines[0])
    if n < 1 or len(lines) != n + 1: return False
    for line in lines[1:]:
        if not num(line) or not 1 <= int(line) < 1000000: return False
    return True

def extra_cases():
    """补充：边界 k=1,2,3,999999，以及大量查询的满规模组（卡逐个查询重算 O(k) 的写法）。"""
    r = random.Random(2786)
    cases = ["4\n1\n2\n3\n999999\n", "1\n999999\n", "3\n999998\n2\n1\n"]
    vals = [r.randint(1, 999999) for _ in range(100000)]
    vals[0], vals[-1] = 1, 999999
    cases.append(f"{len(vals)}\n" + "\n".join(map(str, vals)) + "\n")
    vals = [r.randint(900000, 999999) for _ in range(100000)]
    cases.append(f"{len(vals)}\n" + "\n".join(map(str, vals)) + "\n")
    return cases

def g2786(r):
    values = [r.randint(1, 999999) for _ in range(r.randint(1, 20))]
    return str(len(values)) + "\n" + "\n".join(map(str, values)) + "\n"

REFERENCE='# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 2786: Pell数列\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024fallroutine/02786/\n# License: not declared in source collection; no license is inferred.\ndp = [0]*(1000000+1)\ndp[1], dp[2] = 1, 2\nfor i in range(3, 1000000+1):\n    dp[i] = (2*dp[i-1] + dp[i-2])%32767\n\nfor _ in range(int(input())):\n    k = int(input())\n    print(dp[k])\n'
SAMPLE='2\n1\n8\n'
GENERATOR='g2786'

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as folder:
        script=Path(folder)/"main.py"; script.write_text(REFERENCE)
        result=subprocess.run([sys.executable,"-I",str(script)],input=text,text=True,capture_output=True,timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    for old in data.glob("*"): old.unlink()
    cases=[SAMPLE]+[globals()[GENERATOR](random.Random(seed)) for seed in range(1, 40)]+extra_cases()
    for i,case in enumerate(cases):
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()
