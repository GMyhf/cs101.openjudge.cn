import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/23744/\n# Accepted submission: 52178544\n# Source: http://cs101.openjudge.cn/practice/solution/52178544/\n# License: not declared on the submission page; no license is inferred.\n\na,b,c=map(float,input().split())\nx=min(a,b+c)\ny=min(b,a+c)\nxy=min(c,a+b)\nlis=[]\nfor i in range(3):\n    lis.append(list(input().split()))\n    lis[i][1]=int(lis[i][1])\n    lis[i][2]=int(lis[i][2])\ndir=[(0,1,2),(0,2,1),(1,2,0),(1,0,2),(2,0,1),(2,1,0)]\nmi=float("inf")\ndef path(x1,y1,x2,y2):\n    p=abs(x1-x2)\n    q=abs(y1-y2)\n    zan=min(p,q)\n    p-=zan\n    q-=zan\n    return zan*xy+p*x+q*y\ndef shi(aa,bb,cc):\n    zan=0\n    zan+=path(0,0,lis[aa][1],lis[aa][2])\n    zan+=path(lis[bb][1],lis[bb][2],lis[aa][1],lis[aa][2])\n    zan+=path(lis[cc][1],lis[cc][2],lis[bb][1],lis[bb][2])\n    zan+=path(lis[cc][1],lis[cc][2],100,100)\n    return zan\nans1,ans2,ans3="a","a","a"\nfor dx,dy,dz in dir:\n    k=shi(dx,dy,dz)\n    if (k<mi):\n        mi=k\n        ans1,ans2,ans3=dx,dy,dz\nprint(lis[ans1][0],lis[ans2][0],lis[ans3][0])\nprint(f"{mi:.2f}")'
SAMPLE='1.0 1.0 1.4\nAdamantium 92 40\ninfinity_gauntlet -74 -25\ndecade_armor 95 72\n'
GENERATOR_NAME='g23744'
def g23744(r):
    costs=[r.uniform(.1,5) for _ in range(3)]; names=["a","b","c"]
    pts=[(r.randint(-99,99),r.randint(-99,99)) for _ in range(3)]
    return " ".join(map(str,costs))+"\n"+"\n".join(f"{s} {x} {y}" for s,(x,y) in zip(names,pts))+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+(['8\n','9\n'] if GENERATOR_NAME == 'g22007' else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
