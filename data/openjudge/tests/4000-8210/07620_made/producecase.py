import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='n=int(input())\nintervals=[]\nfor i in range(n):\n    intervals.append(tuple(int(i) for i in input().split()))\nintervals.sort()\ncleft=intervals[0][0]\ncright=intervals[0][1]\nfor left,right in intervals:\n    if left>cright:\n        print("no")\n        break\n    else:\n        cright=max(right,cright)\nelse:\n    print(cleft,cright)'
SAMPLE='5\n5 6\n1 5\n10 10\n6 9\n8 10\n'
GENERATOR_NAME='g7620'
def g7620(r):
    n=r.randint(3,15); connected=r.random()<.7
    starts=[]; left=r.randint(1,20)
    for _ in range(n):
        if connected: a=left; b=a+r.randint(0,8); left=b
        else: a=r.randint(1,60); b=r.randint(a, min(100,a+10))
        starts.append((a,b))
    return f"{n}\n"+"\n".join(f"{a} {b}" for a,b in starts)+"\n"

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
