import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = 'n=int(input())\na=[0]+list(map(int,input().split()))\nb=[0]+list(map(int,input().split()))\nc=[0]+list(map(int,input().split()))\ndp=[[0]*(n+1) for _ in range(2)]\ndp[0][1],dp[1][1]=a[1],b[1]\nfor i in range(2,n+1):\n    dp[0][i]=max(dp[0][i-1]+b[i],dp[1][i-1]+a[i])\n    dp[1][i]=max(dp[0][i-1]+c[i],dp[1][i-1]+b[i])\nprint(dp[0][n])'
SAMPLE = '4\n1 2 2 4\n4 3 3 1\n2 1 1 2\n'
GENERATOR_NAME = 'g4150'
def g4150(r):
    n=r.randint(2,20); z=[[r.randint(1,30) for _ in range(n)] for _ in range(3)]
    return f"{n}\n"+"\n".join(" ".join(map(str,x)) for x in z)+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"
        p.write_text(REFERENCE, encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text, encoding="utf-8")
        (data/f"{i}.out").write_text(run(text), encoding="utf-8")
if __name__=="__main__": main()
