import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = 'a,b,c=map(int,input().split())\nresult=0\nfor k in range(c//b+1):\n    if (c-b*k)%a==0:\n        result+=1\nprint(result)'
SAMPLE = '2 3 18\n'
GENERATOR_NAME = 'g4139'
def g4139(r):
    a,b=r.randint(1,30),r.randint(1,30); k=r.randint(0,20)
    return f"{a} {b} {a*r.randint(0,k+1)+b*k}\n"

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
