import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/19948 statistics, Accepted solution 52600565.\n# Source: http://cs101.openjudge.cn/practice/solution/52600565/\n# Statistics: http://cs101.openjudge.cn/practice/19948/statistics/\n# License: not declared on submission page; no license inferred\nn, m = map(int, input().split())\na = list(map(int, input().split()))\na.sort()\n\nif m >= n:\n    print(0)\nelse:\n    diff = [a[i] - a[i-1] for i in range(1, n)]\n    diff.sort()\n    total = a[-1] - a[0]\n    for i in range(m-1):\n        total -= diff[-1 - i]\n    print(total)\n'
LANGUAGE='Python3'
SAMPLE='7 3\n2 7 9 9 16 28 45\n'
GENERATOR_NAME='g19948'
def g19948(r):
    n=r.randint(1,30); m=r.randint(1,n); return f"{n} {m}\n"+" ".join(str(r.randint(1,1000)) for _ in range(n))+"\n"

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
