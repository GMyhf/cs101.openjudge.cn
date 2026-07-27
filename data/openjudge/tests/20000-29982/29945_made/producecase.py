import random
REFERENCE='# External reference: /practice/29945/statistics/\n# Accepted submission: 52733426\n# Source: http://cs101.openjudge.cn/practice/solution/52733426/\n# License: not declared on the submission page; no license is inferred.\n\nn = int(input())\nwhile n != 1:\n    if n % 2 == 1:\n        nxt = n * 3 + 1\n        print(f"{n}*3+1={nxt}")\n    else:\n        nxt = n // 2\n        print(f"{n}/2={nxt}")\n    n = nxt\nprint("End")'
SAMPLE='5\n'
GENERATOR_NAME='g29945'
def g29945(r): return f"{r.randint(1, 100000)}\n"

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
