import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: cs101.openjudge.cn practice/20090 statistics, Accepted solution 42650453.\n# Source: http://cs101.openjudge.cn/practice/solution/42650453/\n# Statistics: http://cs101.openjudge.cn/practice/20090/statistics/\n# License: not declared on submission page; no license inferred\nfor _ in range(int(input())):print((' 1','3971')[(n:=int(input()))>1][n%4])\n"
SAMPLE='1\n2\n'
GENERATOR_NAME='g20090'
def g20090(r):
    q = r.randint(5, 20)
    return f"{q}\n" + "\n".join(str(r.randint(1, 1008612138)) for _ in range(q)) + "\n"

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
