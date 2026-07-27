import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/21727/\n# Accepted submission: 51529747\n# Source: http://cs101.openjudge.cn/practice/solution/51529747/\n# License: not declared on the submission page; no license is inferred.\n\n# 21727: 湾仔码头\n# 贪心：优先装体积最小的砖\n\nN, M = map(int, input().split())\nbricks = list(map(int, input().split()))\n\ntotal = 0\ncount = 0\n\nfor w in bricks:\n    if total + w <= M:\n        total += w\n        count += 1\n    else:\n        break\n\nprint(count)\n'
SAMPLE='3 100\n2 3 99\n'
GENERATOR_NAME='g21727'
def g21727(r):
    n = r.randint(1, 100)
    values = sorted(r.randint(1, 1000) for _ in range(n))
    return f"{n} {r.randint(1, 1000)}\n" + " ".join(map(str, values)) + "\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+(['8\n','9\n'] if GENERATOR_NAME == 'g22007' else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
