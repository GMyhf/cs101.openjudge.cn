import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/21577/\n# Accepted submission: 52726677\n# Source: http://cs101.openjudge.cn/practice/solution/52726677/\n# License: not declared on the submission page; no license is inferred.\n\n\ndef max_area(line,c):\n    stack=[-1]\n    m=-114514\n    line.append(0)\n    for i in range(c+1):\n        while stack[-1]!=-1 and line[i]<line[stack[-1]]:\n            idx=stack.pop()\n            now_area=line[idx]*(i-stack[-1]-1)\n            if now_area>m:\n                m=now_area\n        stack.append(i)\n    return m\n\nans=float("-inf")\nr,c=map(int,input().split())\ntrees=[]\nfor i in range(r):\n    trees.append(list(map(int,input().split())))\nmatrix=[[0 for _ in range(c)] for _ in range(r)]\nfor i in range(c):\n    if trees[0][i]==0:\n        matrix[0][i]=1\nfor i in range(c):\n    for j in range(1,r):\n        if trees[j][i]==0:\n            matrix[j][i]=matrix[j-1][i]+1\n        else:\n            matrix[j][i]=0\nfor line in matrix:\n    ans=max(ans,max_area(line,c))\nprint(ans)\n'
SAMPLE='4 5\n0 1 0 1 1\n0 1 0 0 1\n0 0 0 0 0\n0 1 1 0 1\n'
GENERATOR_NAME='g21577'
def g21577(r):
    m, n = r.randint(1, 20), r.randint(1, 20)
    return f"{m} {n}\n" + "\n".join(" ".join(str(r.randint(0, 1)) for _ in range(n)) for _ in range(m)) + "\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
