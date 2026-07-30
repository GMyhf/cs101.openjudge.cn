#!/usr/bin/env python3
"""Problem-specific generators and input contracts for T-028 phase-2 round 16."""
from __future__ import annotations

import math
import random
import re

NUMBERS = {16531,18211,27103,27625,26978,27653,26971,27104,18156,4018,
           18182,12556,12560,4101,28050,4030,16528,20134,18146,18176}
EXEMPTIONS = {}
INPUT_DOMAINS = {27625: "输入n(0<n<50),输出一个n层的AVL树至少有多少个结点。"}
SAMPLE_INPUTS = {
  16531:"2 5\n0 1 2 3 4\n5 6 7 8 9\n1 1 1\n1 0 1\n0 0 0\n0 0 1\n0 0 0\n1 1 1\n1 1 1\n1 1 1\n1 1 1\n1 1 1\n",
  18211:"10\n20 30 40\n",26978:"8 3\n1 3 -1 -3 5 3 6 7\n",
  26971:"3\n1 0 2\n",4030:"To\nto be or not to be is a question\n",
  20134:"475.6 11.9 27.4 14.98 6\n102.0 9.99\n220.0 13.29\n256.3 14.79\n275.0 10.29\n277.6 11.29\n381.8 10.09\n",
  18146:"1 2\n4 4\n",
}
SAMPLE_OUTPUTS={16531:"6 0\n",18211:"0\n",26978:"3 3 5 5 6 7\n",26971:"5\n",
4030:"2 0\n",20134:"192.15\n",18146:"YES\n",27103:"3\n"}
LABELS={
16531:"the M-by-N seating grid is a permutation of 0..M*N-1 followed by exactly one binary answer row per student",
18211:"the initial budget and every one-use blueprint cost are nonnegative integers",
27103:"the note row contains exactly N values in 1..M with 1<=M<=N",
27625:"the requested AVL height is a positive integer less than 50",
26978:"1<=k<=n<=100000 and the second line contains exactly n integers in -10000..10000",
27653:"four integers describe two fractions whose denominators are nonzero",
26971:"1<=n<=20000 and exactly n ratings lie in 0..20000",
27104:"1<=N<=500000 and exactly N observation radii lie in 0..N",
18156:"the second line contains 2..100000 integers from which two distinct positions are chosen",
4018:"each EOF-driven dataset contains two nonempty whitespace-free strings",
18182:"1..100 cases contain the stated 1..1000 skills with positive bounded time, damage, capacity and health",
12556:"the input is one 1..1000-character alphabetic string",
12560:"the n-by-m board has exact dimensions and contains only zero and one",
4101:"the case count matches square 3..30 grids over r, b and non-mineral cells",
28050:"3<=n<=19 and the knight start coordinates lie inside the n-by-n board",
4030:"the first line is one alphabetic word and the second contains only letters and spaces",
16528:"0<=n<10000 activities each satisfy 0<=start<=end<=60",
20134:"stations are unique inside the route and all distance, capacity, mileage and price values are positive",
18146:"1<=n<=10000, 1<=k<=100 and exactly k nest sizes lie in 1..10000",
18176:"1<=m<=2000 and each of m nonempty score rows has at most n values in 1..100000000",
}
INVALID={16531:"1 2\n0 0\n1\n0\n",18211:"10\n5 -1 8\n",27103:"4 3\n1 2 4 1\n",
27625:"0\n",26978:"3 4\n1 2 3\n",27653:"1 0 2 3\n",26971:"3\n1 2\n",
27104:"3\n0 4 1\n",18156:"10\n5\n",4018:"abc\n",18182:"1\n2 1 10\n1 5\n",
12556:"abc1\n",12560:"2 3\n0 1\n1 0 1\n",4101:"1\n2\nrb\nbr\n",
28050:"5\n5 0\n",4030:"two words\na short article\n",16528:"1\n10 9\n",
20134:"100 0 10 5 0\n",18146:"2 3\n1 2\n",18176:"2 2\n4 9\n\n"}

def generate(number,seed):
 r=random.Random(number*1_000_003+seed)
 if number==16531:
  m,n=(25,25) if seed==20 else (r.randint(1,8),r.randint(1,8));total=m*n;ids=list(range(total));r.shuffle(ids);p=r.randint(1,20);ans=[[r.randint(0,1) for _ in range(p)] for _ in range(total)]
  if total>1 and seed%2==0:ans[ids[1]]=ans[ids[0]][:]
  return f"{m} {n}\n"+'\n'.join(' '.join(map(str,ids[i*n:(i+1)*n])) for i in range(m))+'\n'+'\n'.join(' '.join(map(str,x)) for x in ans)+'\n'
 if number==18211:return f"{r.randint(0,100000)}\n"+' '.join(str(r.randint(0,100000)) for _ in range(r.randint(1,150)))+'\n'
 if number==27103:
  n=100000 if seed==20 else r.randint(1,300);m=r.randint(1,min(n,50));return f"{n} {m}\n"+' '.join(str(r.randint(1,m)) for _ in range(n))+'\n'
 if number==27625:return f"{([*range(1,20),49])[(seed-1)%20]}\n"
 if number==26978:
  n=100000 if seed==20 else r.randint(1,500);k=r.randint(1,n);return f"{n} {k}\n"+' '.join(str(r.randint(-10000,10000)) for _ in range(n))+'\n'
 if number==27653:
  b=r.choice([-1,1])*r.randint(1,10000);d=r.choice([-1,1])*r.randint(1,10000);return f"{r.randint(-10000,10000)} {b} {r.randint(-10000,10000)} {d}\n"
 if number==26971:
  n=20000 if seed==20 else r.randint(1,500);return f"{n}\n"+' '.join(str(r.randint(0,20000)) for _ in range(n))+'\n'
 if number==27104:
  n=500000 if seed==20 else r.randint(1,1000)
  if seed%4==0:a=[0]*n
  elif seed%4==1:a=[n]*n
  else:a=[r.randint(0,min(5,n)) for _ in range(n)]
  return f"{n}\n"+' '.join(map(str,a))+'\n'
 if number==18156:
  n=100000 if seed==20 else r.randint(2,500);return f"{r.randint(-10**9,10**9)}\n"+' '.join(str(r.randint(-10**9,10**9)) for _ in range(n))+'\n'
 if number==4018:
  rows=[]
  for _ in range(r.randint(4,14)):
   t=''.join(r.choice('abcdef') for _ in range(r.randint(2,20)));s=t[::r.randint(1,3)] if r.random()<.6 else ''.join(r.choice('xyz') for _ in range(r.randint(1,8)));rows.append(f"{s} {t}")
  return '\n'.join(rows)+'\n'
 if number==18182:
  cases=r.randint(1,8);chunks=[]
  for _ in range(cases):
   n=r.randint(1,100 if seed<20 else 1000);m=r.randint(1,1000);b=r.randint(1,10**9);rows=[(r.randint(1,30),r.randint(1,10**9)) for _ in range(n)];chunks.append(f"{n} {m} {b}\n"+'\n'.join(f'{a} {x}' for a,x in rows))
  return f"{cases}\n"+'\n'.join(chunks)+'\n'
 if number==12556:
  n=1000 if seed==20 else r.randint(1,150);return ''.join(r.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(n))+'\n'
 if number==12560:
  n,m=(100,100) if seed==20 else (r.randint(1,30),r.randint(1,30));return f"{n} {m}\n"+'\n'.join(' '.join(str(r.randint(0,1)) for _ in range(m)) for _ in range(n))+'\n'
 if number==4101:
  k=r.randint(1,6);chunks=[]
  for _ in range(k):
   n=30 if seed==20 else r.randint(3,15);chunks.append(str(n)+'\n'+'\n'.join(''.join(r.choice('rb#.') for _ in range(n)) for _ in range(n)))
  return f"{k}\n"+'\n'.join(chunks)+'\n'
 if number==28050:
  n=3+(seed-1)%17;return f"{n}\n{r.randrange(n)} {r.randrange(n)}\n"
 if number==4030:
  word=''.join(r.choice('abcdef') for _ in range(r.randint(1,8)));words=[''.join(r.choice('abcdef') for _ in range(r.randint(1,8))) for _ in range(r.randint(3,30))];
  if seed%2==0:words[r.randrange(len(words))]=word.upper() if seed%4==0 else word
  return word+'\n'+' '.join(words)+'\n'
 if number==16528:
  n=9999 if seed==20 else r.randint(0,300);rows=[]
  for _ in range(n):
   a=r.randint(0,60);rows.append((a,r.randint(a,60)))
  return f"{n}\n"+'\n'.join(f'{a} {b}' for a,b in rows)+'\n'
 if number==20134:
  dest=r.uniform(100,1000);cap=r.uniform(5,30);mileage=r.uniform(5,30);start_price=r.uniform(1,20);n=r.randint(0,20);stations=sorted(r.sample(range(1,int(dest)),min(n,max(0,int(dest)-1))));return f"{dest:.2f} {cap:.2f} {mileage:.2f} {start_price:.2f} {len(stations)}\n"+'\n'.join(f'{d:.2f} {r.uniform(1,20):.2f}' for d in stations)+'\n'
 if number==18146:
  n=r.randint(1,10000)
  if seed%2==0:
   k=r.randint(1,min(100,2*n));a=[1]*k
  else:
   k=r.randint(1,100);a=[10000]*k
  return f"{n} {k}\n"+' '.join(map(str,a))+'\n'
 if number==18176:
  m=2000 if seed==20 else r.randint(1,100);n=r.randint(1,100);primes=[2,3,5,7,11,13,17,19,23,29,31,97,9973];rows=[]
  for _ in range(m):
   count=r.randint(1,n);vals=[r.choice(primes)**2 if r.random()<.35 else r.randint(1,10**8) for _ in range(count)];rows.append(' '.join(map(str,vals)))
  return f"{m} {n}\n"+'\n'.join(rows)+'\n'
 raise KeyError(number)

def valid(number,text):
 try:
  lines=text.rstrip('\n').splitlines();tokens=text.split()
  if number==16531:
   m,n=map(int,lines[0].split());total=m*n;seat=[int(x) for line in lines[1:1+m] for x in line.split()];answers=lines[1+m:];return m>=1 and n>=1 and len(seat)==total and sorted(seat)==list(range(total)) and len(answers)==total and len({len(x.split()) for x in answers})==1 and all(set(x.split())<={'0','1'} for x in answers)
  if number==18211:return len(lines)==2 and int(lines[0])>=0 and bool(lines[1].split()) and all(int(x)>=0 for x in lines[1].split())
  if number==27103:
   n,m=map(int,lines[0].split());a=list(map(int,lines[1].split()));return len(lines)==2 and 1<=m<=n and len(a)==n and all(1<=x<=m for x in a)
  if number==27625:return len(tokens)==1 and 1<=int(tokens[0])<50
  if number==26978:
   n,k=map(int,lines[0].split());a=list(map(int,lines[1].split()));return len(lines)==2 and 1<=k<=n<=100000 and len(a)==n and all(-10000<=x<=10000 for x in a)
  if number==27653:return len(tokens)==4 and all(re.fullmatch(r'-?\d+',x) for x in tokens) and int(tokens[1])!=0 and int(tokens[3])!=0
  if number==26971:
   n=int(lines[0]);a=list(map(int,lines[1].split()));return len(lines)==2 and 1<=n<=20000 and len(a)==n and all(0<=x<=20000 for x in a)
  if number==27104:
   n=int(lines[0]);a=list(map(int,lines[1].split()));return len(lines)==2 and 1<=n<=500000 and len(a)==n and all(0<=x<=n for x in a)
  if number==18156:return len(lines)==2 and 2<=len(lines[1].split())<=100000 and all(re.fullmatch(r'-?\d+',x) for x in tokens)
  if number==4018:return len(tokens)>=2 and len(tokens)%2==0 and all(x and not any(c.isspace() for c in x) for x in tokens)
  if number==18182:
   c=int(lines[0]);i=1
   if not 1<=c<=100:return False
   for _ in range(c):
    n,m,b=map(int,lines[i].split());i+=1
    if not 1<=n<=1000 or not 1<=m<=1000 or not 1<=b<=10**9 or i+n>len(lines):return False
    if any(len(row.split())!=2 or not all(1<=int(x)<=10**9 for x in row.split()) for row in lines[i:i+n]):return False
    i+=n
   return i==len(lines)
  if number==12556:return len(lines)==1 and 1<=len(lines[0])<=1000 and lines[0].isalpha()
  if number==12560:
   n,m=map(int,lines[0].split());return n>=1 and m>=1 and len(lines)==n+1 and all(len(row.split())==m and set(row.split())<={'0','1'} for row in lines[1:])
  if number==4101:
   k=int(lines[0]);i=1
   for _ in range(k):
    n=int(lines[i]);i+=1
    if not 3<=n<=30 or i+n>len(lines) or any(len(row)!=n or set(row)-set('rb#.') for row in lines[i:i+n]):return False
    i+=n
   return k>=1 and i==len(lines)
  if number==28050:
   n=int(lines[0]);a,b=map(int,lines[1].split());return len(lines)==2 and 3<=n<=19 and 0<=a<n and 0<=b<n
  if number==4030:return len(lines)==2 and lines[0].isalpha() and all(c.isalpha() or c==' ' for c in lines[1])
  if number==16528:
   n=int(lines[0]);rows=[list(map(int,x.split())) for x in lines[1:]];return 0<=n<10000 and len(rows)==n and all(len(x)==2 and 0<=x[0]<=x[1]<=60 for x in rows)
  if number==20134:
   d,c,mileage,price,n=map(float,lines[0].split());n=int(n);rows=[list(map(float,x.split())) for x in lines[1:]];return d>0 and c>0 and mileage>0 and price>0 and n>=0 and len(rows)==n and all(len(x)==2 and 0<x[0]<d and x[1]>0 for x in rows) and len({x[0] for x in rows})==n
  if number==18146:
   n,k=map(int,lines[0].split());a=list(map(int,lines[1].split()));return len(lines)==2 and 1<=n<=10000 and 1<=k<=100 and len(a)==k and all(1<=x<=10000 for x in a)
  if number==18176:
   m,n=map(int,lines[0].split());return 1<=m<=2000 and 1<=n<=100 and len(lines)==m+1 and all(1<=len(row.split())<=n and all(1<=int(x)<=10**8 for x in row.split()) for row in lines[1:])
 except (ValueError,IndexError,TypeError):return False
 return False


import subprocess as _subprocess, sys as _sys, tempfile as _tempfile
from pathlib import Path as _Path
REFERENCE="# External reference: http://cs101.openjudge.cn/practice/18182/statistics/\n# Accepted submission: 52705451\n# Source: http://cs101.openjudge.cn/practice/solution/52705451/\n# License: not declared on the submission page; no license is inferred.\n\nnCases = int(input())\nfor _ in range(nCases):\n    n, m, b = map(int, input().split())\n    ways = {}\n    times = []\n    for i in range(n):\n        ti, xi = map(int, input().split())\n        if ti not in ways:\n            times.append(ti)\n            ways[ti] = [xi]\n        else:\n            a = ways[ti]\n            ways[ti] = a + [xi]\n    times.sort()\n    tot = 0\n    jud = True\n    for t in times:\n        a1 = ways[t]\n        a1.sort()\n        tot += sum(a1[-m:])\n        if tot >= b:\n            print(t)\n            jud = False\n            break\n    if jud == True:\n        print('alive')\n"
LANGUAGE='Python3'
NUMBER=18182
SAMPLE='2\n1 1 10\n1 5\n2 2 10\n1 5\n1 5\n'
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
