import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/20122 statistics, Accepted solution 42258230.\n# Source: http://cs101.openjudge.cn/practice/solution/42258230/\n# Statistics: http://cs101.openjudge.cn/practice/20122/statistics/\n# License: not declared on submission page; no license inferred\n\'\'\'\n2300015897\n吴杰稀\n光华管理学院\n\'\'\'\ncases,date = map(int,input().split())\ncompany = []\nfor i in range(cases):\n    dates = list(map(int,input().split()))\n    dates.append(date)\n    dates.sort(reverse = True)\n    company.append(dates)\nfor _ in company:\n    t = _.index(date)\n    if t == 0:\n        print("3")\n    elif t == 1:\n        print("2")\n    elif t == 2:\n        print("1")\n    elif t == 3:\n        print("-4")\n    elif t == 4:\n        print("-3")\n'
SAMPLE='1 0626\n0320 0418 0816 1024\n'
GENERATOR_NAME='g20122'
def g20122(r):
    dates = [320, 418, 626, 816, 1024]
    n = r.randint(1, 8)
    date = r.choice(dates)
    rows = []
    for _ in range(n):
        values = r.sample(dates, 4)
        rows.append(" ".join(f"{x:04d}" for x in values))
    return f"{n} {date:04d}\n" + "\n".join(rows) + "\n"

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
