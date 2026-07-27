import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: cs101.openjudge.cn practice/20125 statistics, Accepted solution 41484284.\n# Source: http://cs101.openjudge.cn/practice/solution/41484284/\n# Statistics: http://cs101.openjudge.cn/practice/20125/statistics/\n# License: not declared on submission page; no license inferred\n# 王楚惟\nl=int(input())\n'''a=[int(i)for i in input().split()]\ns=list(set(a))\nb=[a.count(i)for i in s]\nl=len(b)\nn=n//2'''\nb=[int(i)for i in input().split()]\nn=0\nfor i in b:\n    n+=i\nn=n//2\n\ncun=0\nif n==0:\n    print(1)\nelse:\n    \n    tem=0\n    def ans(i):\n        global cun\n        global tem\n        if i==l:\n            if tem==n:\n                cun=cun+1\n        else:\n            for j in range(b[i]+1):\n                if tem+j>n:\n                    break\n                else:\n                    tem=tem+j\n                    ans(i+1)\n                    tem=tem-j\n\n    if l==1:\n        print(1)\n    elif l==2:\n        print(min(b[0],b[1])+1)\n    else:\n        ans(0)\n        print(cun)\n"
SAMPLE='2\n100 100\n'
GENERATOR_NAME='g20125'
def g20125(r):
    n = r.randint(1, 8)
    return f"{n}\n" + " ".join(str(r.randint(1, 4)) for _ in range(n)) + "\n"

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
