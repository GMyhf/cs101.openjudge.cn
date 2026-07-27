import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/20974/\n# Accepted submission: 52686810\n# Source: http://cs101.openjudge.cn/practice/solution/52686810/\n# License: not declared on the submission page; no license is inferred.\n\nm, s, c = map(int, input().split())\ncows = [int(input()) for _ in range(c)]\nif c == 0:\n    print(0)\nelse:\n    cows.sort()\n    if m >= c:\n        print(c)\n    else:\n        total = cows[-1] - cows[0] + 1\n        gaps = [cows[i] - cows[i-1] - 1 for i in range(1, c)]\n        gaps.sort(reverse=True)\n        total -= sum(gaps[:m-1])\n        print(total)'
SAMPLE='4 50 18\n3 \n4 \n6 \n8 \n14\n15 \n16 \n17 \n21\n25 \n26 \n27 \n30 \n31 \n40 \n41 \n42 \n43\n'
GENERATOR_NAME='g20974'
def g20974(r):
    s = r.randint(1, 200)
    c = r.randint(1, min(50, s))
    cows = sorted(r.sample(range(1, s + 1), c))
    return f"{r.randint(1, 50)} {s} {c}\n" + "\n".join(map(str, cows)) + "\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
