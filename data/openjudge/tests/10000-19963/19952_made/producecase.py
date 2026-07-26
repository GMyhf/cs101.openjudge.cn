import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/19952 statistics, Accepted solution 52328950.\n# Source: http://cs101.openjudge.cn/practice/solution/52328950/\n# Statistics: http://cs101.openjudge.cn/practice/19952/statistics/\n# License: not declared on submission page; no license inferred\na=[0 for i in range(201)]\nb=[0 for i in range(201)]\na[1]=2\nb[1]=1\nfor k in range(2,201):\n    a[k]=2*a[k-1]+2*b[k-1]\n    b[k]=a[k-1]\nt=int(input())\nfor i in range(t):\n    n=int(input())\n    print(a[n]+b[n])\n'
LANGUAGE='Python3'
SAMPLE='1\n1\n'
GENERATOR_NAME='g19952'
def g19952(r):
    t=r.randint(1,12); return f"{t}\n"+"\n".join(str(r.randint(1,200)) for _ in range(t))+"\n"

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
