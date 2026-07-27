import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/29178/\n# Accepted submission: 52734219\n# Source: http://cs101.openjudge.cn/practice/solution/52734219/\n# License: not declared on the submission page; no license is inferred.\n\nn = int(input())\na = list(map(int, input().split()))\ncnt = 0\n\nfor i in range(n):\n    if i == 0:\n        # 第一个\n        if a[i] > a[i+1]:\n            cnt += 1\n    elif i == n-1:\n        # 最后一个\n        if a[i] > a[i-1]:\n            cnt += 1\n    else:\n        # 中间\n        if a[i] > a[i-1] and a[i] > a[i+1]:\n            cnt += 1\n\nprint(cnt)'
SAMPLE='5\n8 12 7 3 6\n'
EXTRA_CASE=None
GENERATOR_NAME='g29178'
def g29178(r):
    n = r.randint(2, 100); return f"{n}\n" + " ".join(str(r.randint(-1000, 1000)) for _ in range(n)) + "\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+([EXTRA_CASE] if EXTRA_CASE else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
