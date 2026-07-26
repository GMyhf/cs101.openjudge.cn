import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='n = int(input())\na = [*map(int, input().split())]\ndp = [1] * n\nmaxn = -1\nfor i in range(n):\n    for j in range(i):\n        if a[j] >= a[i]:\n            dp[i] = max(dp[i], dp[j] + 1)\n    maxn = max(maxn, dp[i])\nprint(maxn)'
SAMPLE='8\n389 207 155 300 299 170 158 65\n'
GENERATOR_NAME='g8780'
def g8780(r):
    n=r.randint(1,15); return f"{n}\n"+" ".join(str(r.randint(1,30000)) for _ in range(n))+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"; p.write_text(REFERENCE,encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text,encoding="utf-8")
        (data/f"{i}.out").write_text(run(text),encoding="utf-8")
if __name__=="__main__": main()
