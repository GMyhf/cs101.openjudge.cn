import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/19946 statistics, Accepted solution 51285749.\n# Source: http://cs101.openjudge.cn/practice/solution/51285749/\n# Statistics: http://cs101.openjudge.cn/practice/19946/statistics/\n# License: not declared on submission page; no license inferred\nm, n = map(int, input().split())\nworkers = [int(x) for x in input().split()]\nhamburgers = [int(x) for x in input().split()]\nworkers.sort()\nhamburgers.sort()\ni, j, res = 0, 0, 0\nwhile i < m and j < n:\n    if workers[i] >= hamburgers[j]:\n        res += 1\n        i += 1\n        j += 1\n    else:\n        i += 1\nprint(res)\n'
LANGUAGE='Python3'
SAMPLE='2 2\n1 2\n2 1\n'
GENERATOR_NAME='g19946'
def g19946(r):
    m,n=r.randint(1,15),r.randint(1,15); return f"{m} {n}\n"+" ".join(str(r.randint(1,50)) for _ in range(m))+"\n"+" ".join(str(r.randint(1,50)) for _ in range(n))+"\n"

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
