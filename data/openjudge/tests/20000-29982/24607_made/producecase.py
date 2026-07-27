import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/24607/\n# Accepted submission: 44525274\n# Source: http://cs101.openjudge.cn/practice/solution/44525274/\n# License: not declared on the submission page; no license is inferred.\n\n# -*- coding: utf-8 -*-\n"""\nCreated on Thu Apr  4 10:35:30 2024\n\n@author: Lenovo\n"""\n\nimport heapq\nclass Node:\n    def __init__(self,ind,val,de):\n        self.ind=ind\n        self.val=val\n        self.de=de\n    \n    def __lt__(self,other):\n        if self.val==other.val:\n            return self.de<other.de\n        return self.val<other.val\n\nn,k=map(int,input().split())\ns=" "+input()\nl=[0]*(n+1)\ndp=[0]*(n+1)\nfor i in range(1,n+1):\n    if s[i]=="H":l[i]=l[i-1]+1\n    else:l[i]=l[i-1]-1\nheap=[]\nheapq.heappush(heap,Node(0,0,0))\nfor i in range(1,n+1):\n    while heap[0].ind+k<i:\n        heapq.heappop(heap)\n    tmp=heap[0]\n    dp[i]=tmp.val+int(l[i]-l[tmp.ind]<=0)\n    heapq.heappush(heap,Node(i,dp[i],l[i]))\nprint(dp[n])'
SAMPLE='7 2\nHGHGGHG\n'
GENERATOR_NAME='g24607'
def g24607(r):
    n=r.randint(1,100); k=r.randint(1,n); return f"{n} {k}\n"+"".join(r.choice("HG") for _ in range(n))+"\n"

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
