import random,subprocess,sys,tempfile
from pathlib import Path
import re

# ---- 输入契约（照题面）：若干组，每组首行 "N M"（0<=N<=200，2<=M<=200），其后恰 N 行 "Si Ei Ci"，
# 1<=Si,Ei<=M，0<=Ci<=10,000,000。题面未禁止重边、自环、反向边。读到文件尾结束。
_INT=re.compile(r'(0|[1-9][0-9]*)$')
def valid(text):
    try:
        if not text.endswith('\n'): return False
        lines=text[:-1].split('\n');i=0;cases=0
        while i<len(lines):
            h=lines[i].split(' ');i+=1
            if len(h)!=2 or any(not _INT.match(x) for x in h): return False
            n,m=map(int,h)
            if not (0<=n<=200 and 2<=m<=200) or i+n>len(lines): return False
            for _ in range(n):
                t=lines[i].split(' ');i+=1
                if len(t)!=3 or any(not _INT.match(x) for x in t): return False
                s,e,c=map(int,t)
                if not (1<=s<=m and 1<=e<=m and 0<=c<=10_000_000): return False
            cases+=1
        return cases>=1
    except Exception:
        return False

def _fmt(m,E):
    return f"{len(E)} {m}\n"+"".join(f"{a} {b} {c}\n" for a,b,c in E)

def _cap(r,mode):
    if mode=='big': return r.randint(9_000_000,10_000_000)
    if mode=='small': return r.randint(0,20)
    return r.choice([r.randint(0,10_000_000),r.randint(1,1000),0])

def _rand(r,m,n,mode='mix'):
    E=[]
    for _ in range(n):
        a=r.randint(1,m);b=r.randint(1,m)
        if r.random()<.15: a=1
        if r.random()<.15: b=m
        E.append((a,b,_cap(r,mode)))
    return E

def _layered(r,m,n,mode='mix'):
    # 1 -> 若干层 -> m，再加反向/跨层边
    mid=list(range(2,m));r.shuffle(mid)
    L=max(1,r.randint(1,6));layers=[[1]]+[mid[i::L] for i in range(L)]+[[m]]
    layers=[x for x in layers if x]
    E=[]
    for i in range(len(layers)-1):
        for v in layers[i+1]:
            E.append((r.choice(layers[i]),v,_cap(r,mode)))
    while len(E)<n:
        i=r.randrange(len(layers)-1);j=r.randrange(len(layers))
        E.append((r.choice(layers[i]),r.choice(layers[j]),_cap(r,mode)))
    E=E[:n];r.shuffle(E);return E

def generate(seed):
    r=random.Random(1273*1_000_003+seed)
    cs=[]
    if seed==1: cs=[_fmt(2,[]),_fmt(200,[]),_fmt(2,[(1,2,0)]),_fmt(2,[(2,1,5)]),_fmt(2,[(1,2,10_000_000)]),_fmt(3,[(1,1,7),(3,3,9),(1,2,4),(2,3,6)])]
    elif seed==2: cs=[_fmt(2,[(1,2,10_000_000)]*200)]                     # 200 条重边：答案 2e9（逼近 32 位上限）
    elif seed==3: cs=[_fmt(5,[(1,2,3),(1,2,4),(2,5,10),(2,5,1),(1,5,2),(5,1,100)])]   # 重边要累加而不是覆盖
    elif seed==4: cs=[_fmt(200,[(i,i+1,r.randint(1,10_000_000)) for i in range(1,200)])]  # 长链 199 条边
    elif seed==5: cs=[_fmt(200,_layered(r,200,200,'big')) for _ in range(3)]
    elif seed==6: cs=[_fmt(15,_rand(r,15,200,'mix')) for _ in range(10)]
    elif seed==7:                                                        # 汇点不可达：答案 0
        cs=[_fmt(100,[(a,b,c) for a,b,c in _rand(r,100,200) if b!=100]),_fmt(50,[(a,b,c) for a,b,c in _rand(r,50,150) if a!=1])]
    elif seed==8:                                                        # 需要反悔（退流）的经典结构
        cs=[_fmt(4,[(1,2,1),(1,3,1),(2,3,1),(2,4,1),(3,4,1)]),_fmt(6,[(1,2,10),(1,3,10),(2,4,10),(3,4,1),(2,5,1),(4,6,10),(5,6,10),(3,5,10)])]
    else:
        for _ in range(r.randint(1,8)):
            m=r.choice([r.randint(2,200),200,r.randint(2,20)])
            n=r.choice([r.randint(0,200),200,200])
            mode=r.choice(['mix','big','small'])
            cs.append(_fmt(m,(_layered if r.random()<.6 and m>2 else _rand)(r,m,n,mode)))
    return "".join(cs)

REFERENCE='# External reference: http://cs101.openjudge.cn/practice/01273/statistics/\n# Accepted submission: 43072217\n# Source: http://cs101.openjudge.cn/practice/solution/43072217/\n# License: not declared on the submission page; no license is inferred.\n\n# -*- coding: utf-8 -*-\n"""\nCreated on Sat Nov 11 12:25:49 2023\n\n@author: Lenovo\n"""\n\nfrom collections import deque\ninf=float(\'inf\')\nmaxn=205\nmaxe=4*maxn*maxn\n\nclass Solution:\n    class Edge:\n        def __init__(self,v,w,nxt):\n            self.v=v\n            self.w=w\n            self.nxt=nxt\n\n    def __init__(self):\n        self.edge=[self.Edge(0,0,0)for _ in range(maxe)]\n        self.head=[-1]*maxn\n        self.tot=0\n        self.level=[-1]*maxn\n\n    def init(self):\n        self.head=[-1]*maxn\n        self.tot=0\n\n    def add(self,u,v,w):\n        self.edge[self.tot]=self.Edge(v,w,self.head[u])\n        self.head[u]=self.tot\n        self.edge[self.tot+1]=self.Edge(u,0,self.head[v])\n        self.head[v]=self.tot+1\n        self.tot+=2\n\n    def bfs(self,s,t):\n        self.level=[-1]*maxn\n        q=deque([s])\n        self.level[s]=0\n        while q:\n            u=q.popleft()\n            i=self.head[u]\n            while i!=-1:\n                if self.edge[i].w>0 and self.level[self.edge[i].v]<0:\n                    self.level[self.edge[i].v]=self.level[u]+1\n                    q.append(self.edge[i].v)\n                i=self.edge[i].nxt\n        return self.level[t]>0\n\n    def dfs(self,u,t,f):\n        if u==t:\n            return f\n        i=self.head[u]\n        while i!=-1:\n            v=self.edge[i].v\n            if self.edge[i].w>0 and self.level[v]>self.level[u]:\n                d=self.dfs(v,t,min(f,self.edge[i].w))\n                if d>0:\n                    self.edge[i].w-=d\n                    self.edge[i ^ 1].w+=d\n                    return d\n            i=self.edge[i].nxt\n        self.level[u]=-1\n        return 0\n\n    def solve(self,s,t):\n        flow=0\n        while self.bfs(s,t):\n            while f:=self.dfs(s,t,inf):\n                flow+=f\n        return flow\n\nS=Solution()\nwhile True:\n    try:\n        m,n=map(int,input().split())\n        S.init()\n        for _ in range(m):\n            u,v,c=map(int,input().split())\n            S.add(u,v,c)\n        print(S.solve(1,n))\n    except EOFError:\n        break\n'
NUMBER=1273
SAMPLE='5 4\n1 2 40\n1 4 20\n2 4 20\n2 3 30\n3 4 10\n'
CASES=40
def run(x):
 with tempfile.TemporaryDirectory() as t:
  p=Path(t)/'s.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)
  if q.returncode:raise SystemExit(q.stderr)
  return '\n'.join(line.rstrip() for line in q.stdout.rstrip().splitlines())+'\n'
def main():
 d=Path('data');d.mkdir(exist_ok=True)
 for p in d.glob('*'):p.unlink()
 for i,x in enumerate([SAMPLE]+[generate(s) for s in range(1, CASES)]):
  assert valid(x),i
  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))
if __name__=='__main__':main()
