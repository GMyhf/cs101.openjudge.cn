# External reference: statistics page /practice/28750/
# Accepted submission: 51077576
# Source: http://cs101.openjudge.cn/practice/solution/51077576/
# License: not declared on the submission page; no license is inferred.

import sys
from math import gcd
sys.setrecursionlimit(2000)
I=iter(sys.stdin.read().split())
try:
 while 1:
  Y,X=int(next(I)),int(next(I))
  def R():return[[0 if c=='.'else ord(c)-96 for c in next(I)]for _ in range(Y)]
  G,G2=R(),R()
  def T(g,d):
   if d&1:g[:]=[list(x)for x in zip(*g)]
   C=len(g[0])
   for i,r in enumerate(g):
    n=[x for x in r if x];z=[0]*(C-len(n))
    g[i]=z+n if d&2 else n+z
   if d&1:g[:]=[list(x)for x in zip(*g)]
  def M(s,t):
   n=len(s);S,T=bytes(s),bytes(t);r=(S+S).find(T)
   if r<0 or r>=n:return 0,0
   m=n
   for k in range(r or 1,n):
    if n%k==0 and S[:-k]==S[k:]:m=k;break
   return r,m
  A="no"
  for s in range(4):
   if A=="yes":break
   for q in(1,3):
    if A=="yes":break
    tg=[r[:]for r in G];d=s
    for i in range(7):
     if tg==G2:A="yes";break
     if i>1:
      ok=1;ng=[]
      for r in range(Y):
       w=[]
       for c in range(X):
        if bool(G2[r][c])!=bool(tg[r][c]):ok=0;break
        w.append(r*X+c+1 if tg[r][c]else 0)
       if not ok:break
       ng.append(w)
      if not ok:T(tg,d);d=(d+q)%4;continue
      sm=[r[:]for r in ng]
      for _ in range(4):T(sm,(d+_)%4)
      rs,ms=[],[]
      for r in range(Y):
       for c in range(X):
        if sm[r][c]:
         u,v=[],[];cr,cc=r,c
         while sm[cr][cc]:
          val=sm[cr][cc];sm[cr][cc]=0;pr,pc=(val-1)//X,(val-1)%X
          u.append(tg[pr][pc]);v.append(G2[pr][pc]);cr,cc=pr,pc
         mr,mm=M(u,v)
         if mm==0:ok=0;break
         if mm==1:continue
         for k in range(len(ms)):
          gv=gcd(mm,ms[k])
          if rs[k]%gv!=mr%gv:ok=0;break
         if not ok:break
         rs.append(mr);ms.append(mm)
       if not ok:break
      if ok:A="yes";break
     T(tg,d);d=(d+q)%4
  print(A)
except StopIteration:pass