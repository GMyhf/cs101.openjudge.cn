import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/18189 statistics, Accepted solution 51284569.\n# Source: http://cs101.openjudge.cn/practice/solution/51284569/\n# Statistics: http://cs101.openjudge.cn/practice/18189/statistics/\n# License: not declared on submission page; no license inferred\nn, p = map(int, input().split())\nn = n/60\nres = 0\nif n <= 0.5:\n    res += 720*n\nelse:\n    res += 360\n    n -= 0.5\n    if n <= 1:\n        res += 600*n\n    else:\n        n -= 1\n        res += 600\n        if n <= 1.5:\n            res += 360*n\n        else:\n            n -= 1.5\n            res += 540\n            res += 240*min(3, n)\nprint(int(res*p))\n'
LANGUAGE='Python3'
SAMPLE='120 2\n'
GENERATOR_NAME='g18189'
def g18189(r): return f"{r.randint(1,600)} {r.randint(1,20)}\n"

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
