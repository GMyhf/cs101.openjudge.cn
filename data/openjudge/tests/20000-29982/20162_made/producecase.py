import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/20162 statistics, Accepted solution 51463351.\n# Source: http://cs101.openjudge.cn/practice/solution/51463351/\n# Statistics: http://cs101.openjudge.cn/practice/20162/statistics/\n# License: not declared on submission page; no license inferred\nt = int(input())\nfor _ in range(t):\n    a, b, c, r = map(int, input().split())\n    a, b = min(a, b), max(a, b)\n    if b <= c-r or a >= c+r:\n        print(b-a)\n    else:\n        print(b-a-min(b, c+r)+max(a, c-r))\n'
SAMPLE='9\n1 10 7 1\n3 3 3 0\n8 2 10 4\n8 2 10 100\n-10 20 -17 2\n-3 2 2 0\n-3 1 2 0\n2 3 2 3\n-1 3 -2 2\n'
GENERATOR_NAME='g20162'
def g20162(r):
    t = r.randint(5, 20)
    rows = [f"{r.randint(-1000, 1000)} {r.randint(-1000, 1000)} {r.randint(-1000, 1000)} {r.randint(1, 1000)}" for _ in range(t)]
    return f"{t}\n" + "\n".join(rows) + "\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        src=Path(d)/'main.py'; src.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(src)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f'{i}.in').write_text(text); (data/f'{i}.out').write_text(run(text))
if __name__=='__main__': main()
