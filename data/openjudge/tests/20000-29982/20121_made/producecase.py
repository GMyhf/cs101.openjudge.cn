import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/20121 statistics, Accepted solution 52495947.\n# Source: http://cs101.openjudge.cn/practice/solution/52495947/\n# Statistics: http://cs101.openjudge.cn/practice/20121/statistics/\n# License: not declared on submission page; no license inferred\nn=int(input())\nlis=[]\nfor i in range(n):\n    lis.append(input().split())\nvis=[[False for _ in range(n)] for _ in range(n)]\nans=""\nnow=0\nx=0\ny=-1\ndx=0\ndy=1\nfor _ in range(n*n):\n    if 0<=x+dx<=n-1 and 0<=y+dy<=n-1 and not vis[x+dx][y+dy]:\n        vis[x+dx][y+dy]=True\n        x=x+dx\n        y=y+dy\n        ans=ans+lis[x][y]\n        continue\n    else:\n        dx,dy=dy,-dx\n        vis[x+dx][y+dy]=True\n        x=x+dx\n        y=y+dy\n        ans=ans+lis[x][y]\n        continue\nprint(ans)\n'
SAMPLE='3\n2 5 7\n3 9 1\n8 6 4\n'
GENERATOR_NAME='g20121'
def g20121(r):
    n = r.randint(2, 8)
    return f"{n}\n" + "\n".join(" ".join(str(r.randint(1, 9)) for _ in range(n)) for _ in range(n)) + "\n"

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
