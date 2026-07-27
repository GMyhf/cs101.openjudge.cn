import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/20137 statistics, Accepted solution 32302039.\n# Source: http://cs101.openjudge.cn/practice/solution/32302039/\n# Statistics: http://cs101.openjudge.cn/practice/20137/statistics/\n# License: not declared on submission page; no license inferred\nr,c=map(int,input().split())\na,b=map(int,input().split())\nd1,d2=map(int,input().split())\nflag=[[-1]*(c+3),*[[-1]+[0]*(c+1)+[-1] for _ in range(r+1)],[-1]*(c+3)]\na+=1;b+=1\nflag[a][b]=1\ncnt=1\nwhile(True):\n    a+=d1;b+=d2\n    if(flag[a][b]==1 or (flag[a-d1][b]==1 and flag[a][b-d2]==1)):\n        break\n    if(flag[a][b]==-1):\n        if(flag[a-d1][b]==-1 and flag[a][b-d2]==-1):\n            break\n        elif(a==0 or a==r+2):\n            a-=d1\n            if(flag[a][b]==1):\n                break\n            flag[a][b]=1;cnt+=1\n            if(flag[a+d1][b]==-1 and flag[a][b+d2]==-1):\n                break\n            d1=-d1\n        else:\n            b -= d2\n            if (flag[a][b] == 1):\n                break\n            cnt += 1\n            flag[a][b] = 1\n            if (flag[a + d1][b] == -1 and flag[a][b + d2] == -1):\n                break\n            d2=-d2\n    else: flag[a][b]=1;cnt+=1\nprint(cnt)\n\n'
SAMPLE='5 7\n0 1\n1 1\n'
GENERATOR_NAME='g20137'
def g20137(r):
    rows, cols = r.randint(3, 12), r.randint(3, 12)
    return f"{rows} {cols}\n0 {r.randint(1, cols - 1)}\n1 1\n"

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
