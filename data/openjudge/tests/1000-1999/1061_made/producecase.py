import random, subprocess, sys, tempfile
from pathlib import Path
def g1061(r):
    # The collected reference divides by (a*i)%L.  A prime circumference and
    # non-zero speed difference keep that expression non-zero for i=1..L-1.
    L = r.choice([101, 211, 307, 401, 503, 601, 701, 809, 907, 1009, 2003, 3001, 4001])
    x = r.randrange(L); y = r.randrange(L)
    while y == x: y = r.randrange(L)
    m = r.randrange(1, L); n = r.randrange(1, L)
    while n == m: n = r.randrange(1, L)
    return f"{x} {y} {m} {n} {L}\n"

REFERENCE="# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 1061: 青蛙的约会\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/practice/01061/\n# License: not declared in source collection; no license is inferred.\nx,y,m,n,L=map(int,input().split())\na,b=m-n,y-x\n# 目标值t满足(t*a)%L==b\nif a==0:\n    print('Impossible')\n    exit()\nelif a<0:\n    a,b=-a,-b\nif b<0:\n    b+=L\nif L%a==0:\n    if b%a==0:\n        print(b//a)\n        exit()\n    else:\n        print('Impossible')\n        exit()\nfor i in range(1,L):\n    c=(a*i)%L\n    if b%c==0:\n        print(i*(b//c))\n        exit()\n"
SAMPLE='1 2 3 4 5\n'
GENERATOR='g1061'

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as folder:
        script=Path(folder)/"main.py"; script.write_text(REFERENCE)
        result=subprocess.run([sys.executable,"-I",str(script)],input=text,text=True,capture_output=True,timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    for old in data.glob("*"): old.unlink()
    cases=[SAMPLE]+[globals()[GENERATOR](random.Random(seed)) for seed in range(1,21)]
    for i,case in enumerate(cases):
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()
