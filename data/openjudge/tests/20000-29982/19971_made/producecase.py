import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/19971 statistics, Accepted solution 43885342.\n# Source: http://cs101.openjudge.cn/practice/solution/43885342/\n# Statistics: http://cs101.openjudge.cn/practice/19971/statistics/\n# License: not declared on submission page; no license inferred\na=[[1]]\nfor i in range(1,1001):\n    a.append([1])\n    if i%2:\n        for j in range(i//2):a[-1].append(a[-2][j]+a[-2][j+1])\n    else:\n        for j in range(i//2-1):a[-1].append(a[-2][j]+a[-2][j+1])\n        a[-1].append(a[-2][-1]*2)\nfor i in range(int(input())):c,b=map(int,input().split());print(a[b][b-c]if c*2>b else a[b][c])\n'
LANGUAGE='Python3'
SAMPLE='3\n2 4\n10 34\n2 7\n'
GENERATOR_NAME='g19971'
def g19971(r):
    t=r.randint(1,12); return f"{t}\n"+"\n".join((lambda b: f"{r.randint(0,b)} {b}")(r.randint(0,100)) for _ in range(t))+"\n"

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
