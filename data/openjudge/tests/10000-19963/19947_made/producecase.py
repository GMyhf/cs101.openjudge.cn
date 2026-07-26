import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE="# External reference: cs101.openjudge.cn practice/19947 statistics, Accepted solution 51286241.\n# Source: http://cs101.openjudge.cn/practice/solution/51286241/\n# Statistics: http://cs101.openjudge.cn/practice/19947/statistics/\n# License: not declared on submission page; no license inferred\nn = int(input())\nl = [int(x) for x in input().split()]\nl.sort()\na = sum(l)\nb = l[-1]\nif a % 2 == 1:\n    print('NO')\nelse:\n    if a >= 2*b:\n        print('YES')\n    else:\n        print('NO')\n"
LANGUAGE='Python3'
SAMPLE='3\n1 2 3\n'
GENERATOR_NAME='g19947'
def g19947(r):
    n=r.randint(2,30); return f"{n}\n"+" ".join(str(r.randint(1,1000)) for _ in range(n))+"\n"

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
