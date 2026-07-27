import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/20091 statistics, Accepted solution 42729047.\n# Source: http://cs101.openjudge.cn/practice/solution/42729047/\n# Statistics: http://cs101.openjudge.cn/practice/20091/statistics/\n# License: not declared on submission page; no license inferred\nfrom math import factorial\n\n\ndef c(n, k):\n    return factorial(n) / (factorial(k) * factorial(n - k))\n\n\nt = int(input())\nfor i in range(t):\n    n = int(input())\n    print(int(max(c(n, n // 2), c(n, n // 2 + 1))))\n'
SAMPLE='1\n3\n'
GENERATOR_NAME='g20091'
def g20091(r):
    t = r.randint(3, 20)
    return f"{t}\n" + "\n".join(str(r.randint(3, 1000)) for _ in range(t)) + "\n"

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
