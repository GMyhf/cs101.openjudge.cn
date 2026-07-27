import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/20102 statistics, Accepted solution 52482499.\n# Source: http://cs101.openjudge.cn/practice/solution/52482499/\n# Statistics: http://cs101.openjudge.cn/practice/20102/statistics/\n# License: not declared on submission page; no license inferred\nimport math\n\nt = int(input())\nwhile t > 0:\n    t-=1\n    n = int(input())\n    print(1+math.comb(n,2)+math.comb(n,4))\n'
SAMPLE='4\n1\n2\n3\n4\n'
GENERATOR_NAME='g20102'
def g20102(r):
    t = r.randint(5, 20)
    return f"{t}\n" + "\n".join(str(r.randint(1, 1000)) for _ in range(t)) + "\n"

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
