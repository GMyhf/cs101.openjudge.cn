import random
REFERENCE='# External reference: /practice/29853/statistics/\n# Accepted submission: 52288129\n# Source: http://cs101.openjudge.cn/practice/solution/52288129/\n# License: not declared on the submission page; no license is inferred.\n\nn=int(input())\na=[int(i) for i in input().split()]\nb=[int(i) for i in input().split()]\nminb=min(b)\nmaxb=max(b)\ncalc=[max(abs(minb-i),abs(maxb-i)) for i in a]\nprint(min(calc))'
SAMPLE='2\n1 10\n2 20\n'
GENERATOR_NAME='g29853'
def g29853(r):
    n = r.randint(1, 100); a = [r.randint(-1000, 1000) for _ in range(n)]; b = [r.randint(-1000, 1000) for _ in range(n)]
    return f"{n}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n"

from pathlib import Path
import random, subprocess, sys, tempfile
REFERENCE = REFERENCE
def solve(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        result=subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()
