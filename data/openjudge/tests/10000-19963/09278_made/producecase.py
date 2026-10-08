import random,re,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='n = int(input())\ndp = [1]+[0]*n\nfor i in range(2, n+1):\n    dp[i] = (i-1)*(dp[i-2]+dp[i-1])\nprint(dp[n])'
SAMPLE='3\n'
GENERATOR_NAME='g9278'
def valid(text):
    # 题面：一个正整数 n (n<200)
    toks=text.split()
    if len(toks)!=1 or not re.fullmatch(r"[1-9][0-9]*",toks[0]): return False
    return 1<=int(toks[0])<200
# 固定覆盖：最小 n=1（答案 0）、n=2、上限 199 附近（大整数，卡 long long 溢出）
FIXED=[1,2,4,5,10,20,21,25,30,50,100,150,190,195,196,197,198,199]
def g9278(r): return f"{r.randint(1,199)}\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"; p.write_text(REFERENCE,encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[f"{n}\n" for n in FIXED]
    r=random.Random(9278)
    while len(cases)<40:
        t=g9278(r)
        if t not in cases: cases.append(t)
    assert all(valid(t) for t in cases) and len(set(cases))==len(cases), "有数据越出题面约束"
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text,encoding="utf-8")
        (data/f"{i}.out").write_text(run(text),encoding="utf-8")
if __name__=="__main__": main()
