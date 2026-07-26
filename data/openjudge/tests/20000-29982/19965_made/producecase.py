import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/19965 statistics, Accepted solution 43122751.\n# Source: http://cs101.openjudge.cn/practice/solution/43122751/\n# Statistics: http://cs101.openjudge.cn/practice/19965/statistics/\n# License: not declared on submission page; no license inferred\ndef f(a,b):\n    if a%b==0:\n        return a//b\n    else:\n        return a//b+1\na,b,c=map(int,input().split())\nwhile b<=a and c>=f(a,b):\n    c-=f(a, b)\n    b+=a//b\nprint(b)    \n'
LANGUAGE='Python3'
SAMPLE='5 2 10\n'
GENERATOR_NAME='g19965'
def g19965(r): return f"{r.randint(1,10000)} {r.randint(1,10000)} {r.randint(1,10000)}\n"

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
