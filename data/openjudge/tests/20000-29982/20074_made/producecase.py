import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: cs101.openjudge.cn practice/20074 statistics, Accepted solution 51318992.\n# Source: http://cs101.openjudge.cn/practice/solution/51318992/\n# Statistics: http://cs101.openjudge.cn/practice/20074/statistics/\n# License: not declared on submission page; no license inferred\nn = int(input())\nMan, Woman = 0, 0\nfor _ in range(n):\n    h, w, s = input().split()\n    min_w = 18.5*(float(h)/100)**2\n    max_w = 24.9*(float(h)/100)**2\n    cur_w = float(w)\n    num = 0\n    while cur_w < min_w or cur_w > max_w:\n        if cur_w < min_w:\n            cur_w += 8\n        elif cur_w > max_w:\n            cur_w -= 5\n        num += 1\n    if s == 'M':\n        Man = max(Man, num)\n    elif s == 'F':\n        Woman = max(Woman, num)\nprint(int(Man), int(Woman))\n"
SAMPLE='2\n170 75 M \n165 45 F\n'
GENERATOR_NAME='g20074'
def g20074(r):
    n = r.randint(1, 12)
    rows = [f"{r.randint(150, 190)} {r.randint(45, 100)} {r.choice(['M', 'F'])}" for _ in range(n)]
    return f"{n}\n" + "\n".join(rows) + "\n"

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
