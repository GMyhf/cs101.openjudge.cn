#!/usr/bin/env python3
"""Problem-specific generators and input contracts for T-028 phase-2 round 18."""
from __future__ import annotations
import random
import re

NUMBERS={29917,4099,4100,12558,18106,18108,21608,12559,28334,18159,
         18160,20089,16532,18177,18188,18224,28674,28914,29918,29947}
EXEMPTIONS={}
INPUT_DOMAINS={4100:"开始时间和截止时间均为非负整数，且不超过100。",
18106:"给定一个n(1<=n<=20)，生成一个n*n的二维数组",
18159:"当输入一个整数 n(2<=n<=10001),要求输出所有从 1 到这个整数之间"}
SAMPLE_INPUTS={
  12559:"4\n23 9 182 79\n",21608:"5\n53 : -1\n118 : 119 136 137\n92 : 107 93 102 91\n102 : -1\n130 : 66 132 135 103\n",
  18160:"2\n2 2\nW.\n.W\n10 12\nW........WW.\n.WWW.....WWW\n....WW...WW.\n.........WW.\n.........W..\n..W......W..\n.W.W.....WW.\nW.W.W.....W.\n.W.W......W.\n..W.......W.\n",
  20089:"5500\n3 3 3 3 3 3 3\n",16532:"1 1\n2 2\n-1 -1\n10\n",
  18188:"3 3\n2 3 2\n3 2 1\n1 1 1\n",28674:"5\nLfrjXhnjshj\n",
  29918:"1500\n",29947:"500 3\n150 300\n100 200\n470 471\n",
}
SAMPLE_OUTPUTS={12559:"97923182 18223799\n",21608:"5\n",18160:"2\n16\n",
  20089:"2\n",16532:"-1\n",18188:"2 2 2\n2 1 1\n1 1 1\n",
  28674:"GameScience\n",28914:"0\n2\n3\n-1\n1\n-1\n3\n1\n3\n-1\n",
  29918:"220 284\n1184 1210\n",29947:"298\n"}
LABELS={
29917:"each nonempty input line is a positive decimal number",
4099:"1<=m<100 and each group has 0<=n<150 syntactically valid push-integer or pop operations with live size at most 100",
4100:"1<=k<100 and each group has 1<=n<50 start-end pairs with 0<=start<=end<=100",
12558:"1<=n,m<=100 binary grid contains one nonempty four-connected island",
18106:"the input is one integer n in 1..20",
18108:"pond-count input has 1<=T<=100 exact nonempty N-by-M grids over W and dot",
21608:"2<=n<=200 unique questionnaire rows use name-colon-friend syntax and at least one respondent has a friend",
12559:"1<=n<=1000 followed by exactly n positive decimal integers",
28334:"1<=n<=10 and 1<=m<=100 distinct non-loop edges form a directed acyclic graph",
18159:"2<=T<=10000 followed by T integers in 2..10001",
18160:"largest-area input has 1<=T<=100 exact nonempty N-by-M grids over W and dot",
20089:"50<=N<=1000000 and exactly seven nonnegative ticket inventories follow",
16532:"distinct interior ball coordinates, diagonal unit direction and nonnegative energy describe the 16-by-5 table",
18177:"2<=N<=20 and 4<=D<=30 positive price rows have nonzero pairwise prefix variance and a unique best pair",
18188:"1<=M,N<=100 followed by an exact matrix of positive pixels",
18224:"1<=m<=100 followed by exactly m integers in 1..1000",
28674:"1<=k<=108000 and the second line is 1..342 ASCII letters",
28914:"1<=t<=10000 and every case satisfies -10^10<=l<=a,b<=r<=10^10 and 1<=x<=10^10",
29918:"the input is one integer n in 1..100000",
29947:"1<=L<=10^9, 1<=M<=100 and M distinct-endpoint closed intervals lie inside 0..L",
}
INVALID={29917:"-1\n",4099:"1\n1\npush\n",4100:"1\n1\n5 2\n",12558:"2 2\n1 0\n0 1\n",
18106:"0\n",18108:"1\n2 2\nW.\n",21608:"2\n1 : -1\n1 : 2\n",12559:"2\n1 0\n",
28334:"2 2\n0 1\n1 0\n",18159:"1\n5\n",18160:"1\n1 2\nWX\n",20089:"49\n1 1 1 1 1 1 1\n",
16532:"1 1\n1 1\n1 0\n2\n",18177:"3 5\n1 1 1 1 1\n2 2 2 2 2\n3 3 3 3 3\n",18188:"1 2\n3 0\n",
18224:"2\n1\n",28674:"0\nabc\n",28914:"1\n5 3 1\n4 4\n",29918:"100001\n",29947:"10 1\n2 11\n"}

def _grid(r,n,m): return [''.join(r.choice('W.') for _ in range(m)) for _ in range(n)]

def _scores(rows):
 import math
 n,d=len(rows),len(rows[0]);out=[]
 for i in range(n):
  for j in range(i+1,n):
   total=0
   for k in range(3,d-1):
    g=[rows[i][s]-rows[j][s] for s in range(k)];p=sum(g)/k;q=(sum((z-p)**2 for z in g)/k)**.5
    if q==0:return None
    diff=rows[i][k]-rows[j][k]
    count=(diff-p)//q if diff>p else (p-diff)//q
    gain=rows[i][k]-rows[i][k+1]+rows[j][k+1]-rows[j][k]
    total += count*gain if diff>p else -count*gain
   out.append((total,i,j))
 return out

def generate(number,seed):
 r=random.Random(number*1_000_003+seed)
 if number==29917:
  values=[str(r.randint(1,10**6)),f"{r.uniform(.01,10000):.6f}",f"{r.randint(1,999)}.{r.randint(0,999):03d}"]
  return '\n'.join(values[:1+(seed%3)])+'\n'
 if number==4099:
  groups=r.randint(1,12);chunks=[]
  for _ in range(groups):
   n=r.randint(0,149);size=0;ops=[]
   for _ in range(n):
    if size<100 and (size==0 or r.random()<.6):ops.append(f"push {r.randint(-10**9,10**9)}");size+=1
    else:ops.append('pop');size=max(0,size-1)
   chunks.append(str(n)+(('\n'+'\n'.join(ops)) if ops else ''))
  return f"{groups}\n"+'\n'.join(chunks)+'\n'
 if number==4100:
  k=r.randint(1,20);chunks=[]
  for _ in range(k):
   n=r.randint(1,49);rows=[]
   for _ in range(n):a=r.randint(0,100);rows.append((a,r.randint(a,100)))
   chunks.append(str(n)+'\n'+'\n'.join(f'{a} {b}' for a,b in rows))
  return f"{k}\n"+'\n'.join(chunks)+'\n'
 if number==12558:
  n,m=(100,100) if seed==20 else (r.randint(1,30),r.randint(1,30));a=[[0]*m for _ in range(n)];x,y=r.randrange(n),r.randrange(m);a[x][y]=1
  for _ in range(r.randint(0,n*m*2)):
   dx,dy=r.choice(((1,0),(-1,0),(0,1),(0,-1)));x=max(0,min(n-1,x+dx));y=max(0,min(m-1,y+dy));a[x][y]=1
  return f"{n} {m}\n"+'\n'.join(' '.join(map(str,row)) for row in a)+'\n'
 if number==18106:return f"{(seed-1)%20+1}\n"
 if number in (18108,18160):
  t=r.randint(1,10);chunks=[]
  for k in range(t):
   n,m=((100,100) if seed==20 and k==0 else (r.randint(1,30),r.randint(1,30)));chunks.append(f"{n} {m}\n"+'\n'.join(_grid(r,n,m)))
  return f"{t}\n"+'\n'.join(chunks)+'\n'
 if number==21608:
  n=r.randint(2,200);names=r.sample(range(1,1000000),n);rows=[]
  for i,name in enumerate(names):
   pool=names+list(range(1000001,1000051));friends=r.sample(pool,r.randint(0,min(8,len(pool))))
   if i==0 and not friends:friends=[names[1]]
   rows.append(f"{name} : "+(' '.join(map(str,friends)) if friends else '-1'))
  return f"{n}\n"+'\n'.join(rows)+'\n'
 if number==12559:
  n=1000 if seed==20 else r.randint(1,100);return f"{n}\n"+' '.join(str(r.randint(1,10**12)) for _ in range(n))+'\n'
 if number==28334:
  n=r.randint(2,10);order=list(range(n));r.shuffle(order);possible=[(order[i],order[j]) for i in range(n) for j in range(i+1,n)];r.shuffle(possible);edges=possible[:r.randint(1,min(100,len(possible)))]
  return f"{n} {len(edges)}\n"+'\n'.join(f'{a} {b}' for a,b in edges)+'\n'
 if number==18159:
  t=10000 if seed==20 else r.randint(2,10)
  values=([2+(i%29) for i in range(t)] if seed==20 else [r.randint(2,10001) for _ in range(t)])
  return f"{t}\n"+'\n'.join(map(str,values))+'\n'
 if number==20089:
  target=1000000 if seed==20 else r.randrange(1,20001)*50;stock=[r.randint(0,30) for _ in range(7)];return f"{target}\n"+' '.join(map(str,stock))+'\n'
 if number==16532:
  a=(r.randint(1,15),r.randint(1,4));b=(r.randint(1,15),r.randint(1,4))
  while b==a:b=(r.randint(1,15),r.randint(1,4))
  return f"{a[0]} {a[1]}\n{b[0]} {b[1]}\n{r.choice((-1,1))} {r.choice((-1,1))}\n{r.randint(0,250)}\n"
 if number==18177:
  n,d=r.randint(2,8),r.randint(5,15)
  while True:
   rows=[[r.randint(1,1000) for _ in range(d)] for _ in range(n)];scores=_scores(rows)
   if scores and len([x for x in scores if x[0]==max(y[0] for y in scores)])==1:break
  return f"{n} {d}\n"+'\n'.join(' '.join(map(str,row)) for row in rows)+'\n'
 if number==18188:
  m,n=(100,100) if seed==20 else (r.randint(1,30),r.randint(1,30));return f"{m} {n}\n"+'\n'.join(' '.join(str(r.randint(1,65535)) for _ in range(n)) for _ in range(m))+'\n'
 if number==18224:
  m=r.randint(1,100);return f"{m}\n"+' '.join(str(r.randint(1,1000)) for _ in range(m))+'\n'
 if number==28674:
  n=342 if seed==20 else r.randint(1,100);return f"{r.randint(1,108000)}\n"+''.join(r.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(n))+'\n'
 if number==28914:
  t=10000 if seed==20 else r.randint(1,200);rows=[]
  for _ in range(t):
   l=r.randint(-10**10,10**10);rr=r.randint(l,10**10);rows.append((l,rr,r.randint(1,10**10),r.randint(l,rr),r.randint(l,rr)))
  return f"{t}\n"+'\n'.join(f'{l} {rr} {x}\n{a} {b}' for l,rr,x,a,b in rows)+'\n'
 if number==29918:return f"{[1,219,220,284,1500,100000][seed%6] if seed<12 else r.randint(1,100000)}\n"
 if number==29947:
  L=10**9 if seed==20 else r.randint(1,100000);m=r.randint(1,100);rows=[]
  for _ in range(m):
   a,b=r.sample(range(0,min(L,100000)+1),2) if L<=100000 else (r.randint(0,L),r.randint(0,L))
   if a>b:a,b=b,a
   rows.append((a,b))
  return f"{L} {m}\n"+'\n'.join(f'{a} {b}' for a,b in rows)+'\n'
 raise KeyError(number)

def valid(number,text):
 try:
  lines=text.rstrip('\n').splitlines();tokens=text.split()
  if number==29917:return bool(lines) and all(float(x)>0 and re.fullmatch(r'\d+(?:\.\d+)?',x) for x in lines)
  if number in (4099,4100):
   k=int(lines[0]);i=1
   if not 1<=k<100:return False
   for _ in range(k):
    n=int(lines[i]);i+=1
    if not ((0<=n<150) if number==4099 else (1<=n<50)) or i+n>len(lines):return False
    if number==4099:
     size=0
     for row in lines[i:i+n]:
      if row=='pop':size=max(0,size-1)
      elif re.fullmatch(r'push -?\d+',row):size+=1
      else:return False
      if size>100:return False
    elif any(len(row.split())!=2 or not (0<=int(row.split()[0])<=int(row.split()[1])<=100) for row in lines[i:i+n]):return False
    i+=n
   return i==len(lines)
  if number==12558:
   n,m=map(int,lines[0].split());a=[list(map(int,x.split())) for x in lines[1:]]
   if not 1<=n<=100 or not 1<=m<=100 or len(a)!=n or any(len(x)!=m or set(x)-{0,1} for x in a):return False
   cells={(i,j) for i in range(n) for j in range(m) if a[i][j]};seen=set();stack=[next(iter(cells))] if cells else []
   while stack:
    p=stack.pop()
    if p in seen:continue
    seen.add(p);i,j=p;stack += [(x,y) for x,y in ((i+1,j),(i-1,j),(i,j+1),(i,j-1)) if (x,y) in cells-seen]
   return bool(cells) and seen==cells
  if number==18106:return len(tokens)==1 and 1<=int(tokens[0])<=20
  if number in (18108,18160):
   t=int(lines[0]);i=1
   for _ in range(t):
    n,m=map(int,lines[i].split());i+=1
    if n<1 or m<1 or i+n>len(lines) or any(len(x)!=m or set(x)-set('W.') for x in lines[i:i+n]):return False
    i+=n
   return 1<=t<=100 and i==len(lines)
  if number==21608:
   n=int(lines[0]);rows=lines[1:];names=[];has=False
   for row in rows:
    p=row.split()
    if len(p)<3 or p[1]!=':' or not all(re.fullmatch(r'-?\d+',x) for x in p[::2] if False):return False
    names.append(p[0]);has |= p[2:]!=['-1']
   return 2<=n<=200 and len(rows)==n and len(set(names))==n and has and all(re.fullmatch(r'\d+',x) for row in rows for x in row.split()[2:] if x!='-1')
  if number==12559:
   n=int(lines[0]);a=lines[1].split();return len(lines)==2 and 1<=n<=1000 and len(a)==n and all(x.isdigit() and int(x)>0 for x in a)
  if number==28334:
   n,m=map(int,lines[0].split());edges=[tuple(map(int,x.split())) for x in lines[1:]];g={i:[] for i in range(n)}
   if not 1<=n<=10 or not 1<=m<=100 or len(edges)!=m or len(set(edges))!=m or any(a==b or not(0<=a<n and 0<=b<n) for a,b in edges):return False
   for a,b in edges:g[a].append(b)
   color=[0]*n
   def dfs(x):
    if color[x]==1:return False
    if color[x]==2:return True
    color[x]=1
    if not all(dfs(y) for y in g[x]):return False
    color[x]=2;return True
   return all(dfs(i) for i in range(n))
  if number==18159:
   t=int(lines[0]);a=list(map(int,lines[1:]));return 2<=t<=10000 and len(a)==t and all(2<=x<=10001 for x in a)
  if number==20089:return len(lines)==2 and 50<=int(lines[0])<=1000000 and len(lines[1].split())==7 and all(int(x)>=0 for x in lines[1].split())
  if number==16532:
   a=tuple(map(int,lines[0].split()));b=tuple(map(int,lines[1].split()));d=tuple(map(int,lines[2].split()));return len(lines)==4 and a!=b and all(1<=p[0]<=15 and 1<=p[1]<=4 for p in (a,b)) and d[0] in (-1,1) and d[1] in (-1,1) and int(lines[3])>=0
  if number==18177:
   n,d=map(int,lines[0].split());rows=[list(map(int,x.split())) for x in lines[1:]];scores=_scores(rows) if len(rows)==n and all(len(x)==d and min(x)>0 for x in rows) else None
   return 2<=n<=20 and 4<=d<=30 and scores is not None and len([x for x in scores if x[0]==max(y[0] for y in scores)])==1
  if number==18188:
   m,n=map(int,lines[0].split());rows=[list(map(int,x.split())) for x in lines[1:]];return 1<=m<=100 and 1<=n<=100 and len(rows)==m and all(len(x)==n and min(x)>0 for x in rows)
  if number==18224:
   m=int(lines[0]);a=list(map(int,lines[1].split()));return len(lines)==2 and 1<=m<=100 and len(a)==m and all(1<=x<=1000 for x in a)
  if number==28674:return len(lines)==2 and 1<=int(lines[0])<=108000 and 1<=len(lines[1])<=342 and lines[1].isalpha() and lines[1].isascii()
  if number==28914:
   t=int(lines[0]);vals=list(map(int,tokens[1:]));return 1<=t<=10000 and len(vals)==5*t and all(-10**10<=vals[i]<=vals[i+1]<=10**10 and 1<=vals[i+2]<=10**10 and vals[i]<=vals[i+3]<=vals[i+1] and vals[i]<=vals[i+4]<=vals[i+1] for i in range(0,len(vals),5))
  if number==29918:return len(tokens)==1 and 1<=int(tokens[0])<=100000
  if number==29947:
   L,m=map(int,lines[0].split());rows=[tuple(map(int,x.split())) for x in lines[1:]];return 1<=L<=10**9 and 1<=m<=100 and len(rows)==m and all(0<=a<b<=L for a,b in rows)
 except (ValueError,IndexError,TypeError,ZeroDivisionError):return False
 return False


import subprocess as _subprocess, sys as _sys, tempfile as _tempfile
from pathlib import Path as _Path
REFERENCE='# External reference: http://cs101.openjudge.cn/practice/12559/statistics/\n# Accepted submission: 52536073\n# Source: http://cs101.openjudge.cn/practice/solution/52536073/\n# License: not declared on the submission page; no license is inferred.\n\nfrom functools import cmp_to_key\n\ndef compare(a,b):\n    if a+b<b+a:\n        return -1\n    elif a+b>b+a:\n        return 1\n    else:\n        return 0\n\nn=int(input())\nnum=input().split()\nnum.sort(key=cmp_to_key(compare))\na="".join(num)\nb="".join(reversed(num))\nprint(b,a)\n'
LANGUAGE='Python3'
NUMBER=12559
SAMPLE='4\n23 9 182 79\n'
def _build():
 with _tempfile.TemporaryDirectory() as folder:
  folder=_Path(folder);src=folder/('s.py' if LANGUAGE=='Python3' else 's.cpp');src.write_text(REFERENCE)
  cmd=[_sys.executable,'-I',str(src)]
  if LANGUAGE!='Python3':
   exe=folder/'s';_subprocess.run(['g++','-std=c++20','-O2','-pipe',str(src),'-o',str(exe)],check=True);cmd=[str(exe)]
  out=_Path('data');out.mkdir(exist_ok=True)
  for path in out.glob('*'):path.unlink()
  cases=([SAMPLE] if SAMPLE else [])+[generate(NUMBER,seed) for seed in range(1,21)]
  for index,case in enumerate(cases):
   result=_subprocess.run(cmd,input=case,text=True,capture_output=True,timeout=120,check=True)
   answer='\n'.join(line.rstrip() for line in result.stdout.rstrip().splitlines())+'\n'
   (out/f'{index}.in').write_text(case);(out/f'{index}.out').write_text(answer)
if __name__=='__main__':_build()
