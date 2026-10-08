import random,re,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='import math\nN, A, B = map(int, input().split())\nres = 0\nans = (0, 0)\nfor i in range(1, N+1):\n    j = math.ceil(i*A/B-1)\n    if j/i > res:\n        res = j/i\n        ans = (j, i)\nprint(*ans)'
SAMPLE='100 7 13\n'
GENERATOR_NAME='g7832'
def g7832(r):
    n=r.randint(10,200); a=r.randint(1,n-2); b=r.randint(a+1,n-1)
    return f"{n} {a} {b}\n"

def valid(text):
    """题面契约：一行三个正整数 N A B，单空格分隔，1 <= A < B < N <= 1000。"""
    if not text.endswith("\n") or "\n" in text[:-1]:
        return False
    t=text[:-1].split(" ")
    if len(t)!=3 or not all(re.fullmatch(r"[1-9][0-9]*",x) for x in t):
        return False
    n,a,b=map(int,t)
    return 1<=a<b<n<=1000

# 追加的边界/规模组：原 40 组 N <= 195，没有 N 接近 1000、最小规模 N=3、A/B 非最简、A/B 极小或极接近 1
EXTRA=['3 1 2\n','4 2 3\n','1000 998 999\n','1000 1 999\n','1000 1 2\n','1000 2 4\n','1000 333 999\n',
       '1000 500 999\n','1000 997 998\n','999 1 998\n','1000 377 610\n','1000 610 987\n']
def g7832_big(r):
    n=r.randint(900,1000); b=r.randint(2,n-1); a=r.randint(1,b-1)
    return f"{n} {a} {b}\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"; p.write_text(REFERENCE,encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 40)]
    cases+=EXTRA+[g7832_big(random.Random(78320+seed)) for seed in range(8)]
    assert all(valid(c) for c in cases) and len(set(cases))==len(cases)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text,encoding="utf-8")
        (data/f"{i}.out").write_text(run(text),encoding="utf-8")
if __name__=="__main__": main()
