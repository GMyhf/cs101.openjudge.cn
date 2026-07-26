import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE="# External reference: cs101.openjudge.cn practice/19493 statistics, Accepted solution 43122575.\n# Source: http://cs101.openjudge.cn/practice/solution/43122575/\n# Statistics: http://cs101.openjudge.cn/practice/19493/statistics/\n# License: not declared on submission page; no license inferred\nm=int(input())\nfor _ in range(m):\n    l=list(map(float,input().split()))\n    t=str(l[0])\n    if t[-2]=='.':\n        flag=1\n    else:\n        flag=2\n    ans=[]\n    for i in range(len(l)-4):\n        c=sum(l[i:i+5])/5\n        ans.append(round(c,flag))\n    print(*ans)\n"
LANGUAGE='Python3'
SAMPLE='2\n1.0 2.0 3.0 4.0 5.0 6.0 7.0\n4.97 4.99 5.08 5.03 4.98 4.95 5.02\n'
GENERATOR_NAME='g19493'
def g19493(r):
    line=lambda: " ".join(f"{r.randint(1,999)/100:.2f}" if r.random()<.5 else f"{r.randint(10,999)/10:.1f}" for _ in range(r.randint(6,15)))
    m=r.randint(1,8); return f"{m}\n"+"\n".join(line() for _ in range(m))+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        d=Path(d); src=d/'main.py'
        src.write_text(REFERENCE); cmd=[sys.executable,str(src)]
        if LANGUAGE=="G++":
            exe=d/"main"; subprocess.run(["g++","-std=c++17","-O2",str(src),"-o",str(exe)],check=True)
            cmd=[str(exe)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text)
        (data/f"{i}.out").write_text(run(text))
if __name__=="__main__": main()
