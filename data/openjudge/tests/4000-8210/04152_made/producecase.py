import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = "import sys\ncontent=sys.stdin.read().split()\nptr=0\nwhile ptr<len(content):\n    m=int(content[ptr])\n    num=content[ptr+1]\n    ptr+=2\n    #dp[i][j]表示放i个加号，前j+1位数的最小和，dp[i][j]=max(dp[i][j],dp[i-1][j-t]+int(num[j-t:j]))\n    dp=[[float('inf')]*len(num) for _ in range(m+1)]\n    for j in range(len(num)):\n        dp[0][j]=int(num[:j+1])\n    for i in range(1,m+1):\n        for j in range(len(num)):\n            for t in range(1,j-i+2):\n                dp[i][j]=min(dp[i][j],dp[i-1][j-t]+int(num[j-t+1:j+1]))\n    print(dp[m][len(num)-1])"
SAMPLE = '2\n123456\n1\n123456\n4\n12345\n'
GENERATOR_NAME = 'g4152'
def g4152(r):
    z=[]
    for _ in range(r.randint(1,3)):
        s="".join(str(r.randint(0,9)) for _ in range(r.randint(4,10)))
        z += [str(r.randint(1,len(s)-1)),s]
    return "\n".join(z)+"\n"

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
