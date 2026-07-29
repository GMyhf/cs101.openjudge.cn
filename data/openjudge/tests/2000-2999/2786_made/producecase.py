import random, subprocess, sys, tempfile
from pathlib import Path
def g2786(r):
    values = [r.randint(1, 1000000) for _ in range(r.randint(1, 20))]
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
    cases=[SAMPLE]+[globals()[GENERATOR](random.Random(seed)) for seed in range(1,21)]
    for i,case in enumerate(cases):
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()
