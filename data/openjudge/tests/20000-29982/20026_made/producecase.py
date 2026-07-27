import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/20026 statistics, Accepted solution 52332704.\n# Source: http://cs101.openjudge.cn/practice/solution/52332704/\n# Statistics: http://cs101.openjudge.cn/practice/20026/statistics/\n# License: not declared on submission page; no license inferred\nn=int(input())\nif n%2==1:\n    print(1)\nif n%4==2:\n    print(2)\nif n%4==0:\n    print(n)\n'
SAMPLE='1\n'
GENERATOR_NAME='g20026'
def g20026(r):
    a, b = r.randint(0, 8), r.randint(0, 6)
    return f"{2 ** a * 3 ** b}\n"

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
