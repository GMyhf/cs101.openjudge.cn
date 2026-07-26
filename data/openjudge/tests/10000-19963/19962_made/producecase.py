import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/19962 statistics, Accepted solution 52530564.\n# Source: http://cs101.openjudge.cn/practice/solution/52530564/\n# Statistics: http://cs101.openjudge.cn/practice/19962/statistics/\n# License: not declared on submission page; no license inferred\nn=int(input())\nlis=list(map(int,input().split()))\nlis=sorted(lis)\nl=0\nr=n-1\nans=0\nwhile r>=l:\n    ans=ans+lis[r]-lis[l]\n    l+=1\n    r-=1\nprint(ans)\n'
LANGUAGE='Python3'
SAMPLE='4\n6 2 9 1\n'
GENERATOR_NAME='g19962'
def g19962(r):
    n=r.randint(2,30); return f"{n}\n"+" ".join(str(r.randint(-100,100)) for _ in range(n))+"\n"

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
