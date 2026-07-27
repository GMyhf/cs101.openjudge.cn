import random
REFERENCE='# External reference: /practice/30041/statistics/\n# Accepted submission: 52212520\n# Source: http://cs101.openjudge.cn/practice/solution/52212520/\n# License: not declared on the submission page; no license is inferred.\n\nn,m=[int(i) for i in input().split()]\nprev_array=[int(i) for i in input().split()]\nnow_array=prev_array\n\ndp=[[0 for i in range(m)] for j in range(n)]\nfor i in range(m):\n    dp[0][i]=1\nfor i in range(1,n):\n    ptr1=0\n    current=0\n    prev_array=now_array[:]\n    now_array=[int(i) for i in input().split()]\n    for ptr2 in range(m):\n        while ptr1<=m-1 and now_array[ptr2]>=prev_array[ptr1]:\n            current+=dp[i-1][ptr1]\n            ptr1+=1\n        dp[i][ptr2]=current\ns=0\nfor i in dp[-1]:\n    s+=i\nprint(s)'
SAMPLE='3 3\n1 2 3\n2 3 4\n3 4 4\n'
GENERATOR_NAME='g30041'
def g30041(r):
    n, m = r.randint(1, 35), r.randint(1, 35); rows = []
    for _ in range(n):
        row = sorted(r.randint(0, 100) for _ in range(m)); rows.append(" ".join(map(str, row)))
    return f"{n} {m}\n" + "\n".join(rows) + "\n"

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
