import random
REFERENCE='# External reference: /practice/30091/statistics/\n# Accepted submission: 52732776\n# Source: http://cs101.openjudge.cn/practice/solution/52732776/\n# License: not declared on the submission page; no license is inferred.\n\nL = int(input())\nN = int(input())\nif N == 0:\n    print(0, 0)\nelse:\n    pos = list(map(int, input().split()))\n    min_ans = 0\n    max_ans = 0\n    for x in pos:\n        t1 = min(x, L + 1 - x)\n        t2 = max(x, L + 1 - x)\n        if t1 > min_ans:\n            min_ans = t1\n        if t2 > max_ans:\n            max_ans = t2\n    print(min_ans, max_ans)'
SAMPLE='4\n2\n1 3\n'
GENERATOR_NAME='g30091'
CPP=False
def g30091(r):
    L, n = r.randint(2, 5000), r.randint(0, 30)
    n = min(n, L)
    p = sorted(r.sample(range(1, L + 1), n)) if n else []
    return f"{L}\n{n}\n{' '.join(map(str,p))}\n" if n else f"{L}\n0\n"

from pathlib import Path
import subprocess, sys, tempfile
def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/('main.cpp' if CPP else 'main.py'); p.write_text(REFERENCE)
        if CPP:
            exe=Path(d)/'main'; c=subprocess.run(['g++','-O2','-std=c++17',str(p),'-o',str(exe)],capture_output=True,text=True,timeout=30)
            if c.returncode: raise SystemExit(c.stderr)
            cmd=[str(exe)]
        else: cmd=[sys.executable,str(p)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
