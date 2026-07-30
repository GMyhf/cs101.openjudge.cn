#!/usr/bin/env python3
"""Problem-specific generators and input contracts for T-028 phase-2 round 19."""
from __future__ import annotations
import random,re
from functools import cmp_to_key

NUMBERS={16529,27626,29949,30947,16530,27122,27925,27373,27363,18155,
28700,4013,4014,4016,4017,4019,4020,4042,4044,4068}
EXEMPTIONS={}
SAMPLE_INPUTS={16529:"5\n0.1 0.8 20 0.5 0.01\n",16530:"2\nLARHONDA\nLARSEN\n",
27122:"5 3\n1 2 3 4 7\n",27373:"4\n4\n23 9 182 79\n",27363:"7\n0 1 4 5 1 3 3\n",
18155:"12\n1 2 3 4 5\n",27925:"2\n101 102 103\n201 202 203\nENQUEUE 101\nENQUEUE 201\nENQUEUE 102\nENQUEUE 202\nENQUEUE 103\nENQUEUE 203\nDEQUEUE\nDEQUEUE\nDEQUEUE\nDEQUEUE\nDEQUEUE\nDEQUEUE\nSTOP\n"}
SAMPLE_OUTPUTS={16529:"20000.00\n",16530:"LARI\n",27122:"3\n",27373:"9182\n",
27363:"2\n",18155:"YES\n",27925:"101\n102\n103\n201\n202\n203\n"}
LABELS={
16529:"1<=N<=100000 followed by exactly N positive decimal stock prices",
27626:"the input is one integer n with 0<n<50000000",
29949:"1<=N<=100, 1<=M<=10000 and N ore rows have value and weight in 1..1000",
30947:"1<=n<=100000, 1<=q<=100, n counts in 0..10^9 and q targets in 1..10^9",
16530:"even 2<=n<=1000 followed by n uppercase names shorter than 30 characters",
27122:"2<=m<=n<=100000 and n distinct basket positions are integers",
27925:"1<=t<100 nonempty disjoint member rows precede at most 50000 valid queue commands ending STOP",
27373:"1<=m<=200, 1<=n<=1000 and n positive integers each use at most 20 digits",
27363:"1<=n<50000 followed by n colors in 0..n",
18155:"the target is an integer and the second line has 1..16 positive integers",
28700:"the input is either an integer in 1..3999 or its canonical uppercase Roman representation",
4013:"one or more 1..15000-sized integer datasets are encoded one value per line and terminated by zero",
4014:"each EOF-driven row contains an uppercase word, integer shift and a permutation of all positions",
4016:"1<=N<=500 followed by unique numeric IDs shorter than 10 digits and grades in 1..100",
4017:"each nonempty EOF-driven line is an integer N in 1..30",
4019:"each nonempty EOF-driven line is a weekday integer in 1..7",
4020:"1<=N<=100 and every case contains exactly 53 distinct cards from the 54-card deck",
4042:"1<=N<=100 and every row has lowercase S, 1<=m<len(S), and integer q",
4044:"1<=N<=1000 followed by distinct positive weights and nonempty colors of at most 10 characters",
4068:"1<=N<=100 followed by N nonempty integer arrays, one per line",
}
INVALID={16529:"2\n1 0\n",27626:"50000000\n",29949:"1 0\n1 1\n",30947:"1 1\n-1\n2\n",
16530:"3\nA\nB\nC\n",27122:"3 4\n1 2 3\n",27925:"1\n\nSTOP\n",27373:"0\n1\n5\n",
27363:"2\n0 3\n",18155:"1\n\n",28700:"IIII\n",4013:"2\n1\n0\n",4014:"ABC 2 1 1 3\n",
4016:"2\n1 50\n1 60\n",4017:"31\n",4019:"0\n",4020:"1\nJoker\n",4042:"1\nabc 3 2\n",
4044:"2\n1 red\n1 blue\n",4068:"2\n1 2\n"}

def _roman(n):
 vals=((1000,'M'),(900,'CM'),(500,'D'),(400,'CD'),(100,'C'),(90,'XC'),(50,'L'),(40,'XL'),(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I'));s=''
 for v,c in vals:q,n=divmod(n,v);s+=c*q
 return s

def generate(number,seed):
 r=random.Random(number*1_000_003+seed)
 if number==16529:
  n=100000 if seed==20 else r.randint(1,300);return f"{n}\n"+' '.join(f'{10**r.uniform(-2,6):.5f}' for _ in range(n))+'\n'
 if number==27626:return f"{[1,2,3,20,49999999][seed%5] if seed<10 else r.randint(1,49999999)}\n"
 if number==29949:
  n=r.randint(1,100);return f"{n} {r.randint(1,10000)}\n"+'\n'.join(f'{r.randint(1,1000)} {r.randint(1,1000)}' for _ in range(n))+'\n'
 if number==30947:
  if seed==20:n,q=100000,100;a=[1]*n;targets=list(range(1,q+1))
  else:n,q=r.randint(1,10),r.randint(1,20);a=[r.randint(0,20) for _ in range(n)];targets=[r.randint(1,10**6) for _ in range(q)]
  return f"{n} {q}\n"+' '.join(map(str,a))+'\n'+'\n'.join(map(str,targets))+'\n'
 if number==16530:
  n=2*r.randint(1,100);names={}
  while len(names)<n:names[''.join(r.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(r.randint(1,29)))]=1
  return f"{n}\n"+'\n'.join(names)+'\n'
 if number==27122:
  n=100000 if seed==20 else r.randint(2,300);a=r.sample(range(-10**9,10**9),n);return f"{n} {r.randint(2,n)}\n"+' '.join(map(str,a))+'\n'
 if number==27925:
  t=r.randint(1,20);ids=r.sample(range(1000000),r.randint(t,min(1000,t*20)));groups=[[] for _ in range(t)]
  for i,x in enumerate(ids):groups[i%t].append(x)
  active=[];commands=[]
  for _ in range(r.randint(1,500)):
   if active and r.random()<.4:commands.append('DEQUEUE');active.pop(0)
   else:x=r.choice(ids);commands.append(f'ENQUEUE {x}');active.append(x)
  return f"{t}\n"+'\n'.join(' '.join(map(str,g)) for g in groups)+'\n'+'\n'.join(commands)+'\nSTOP\n'
 if number==27373:
  m=r.randint(1,200);n=r.randint(1,1000);a=[str(r.randint(1,10**r.randint(1,20)-1)) for _ in range(n)];return f"{m}\n{n}\n"+' '.join(a)+'\n'
 if number==27363:
  n=49999 if seed==20 else r.randint(4,500)
  if seed%3==0:a=[1,2,1,2]+[0]*(n-4)
  elif seed%3==1:
   d=min((seed%20)+1,n//2);a=list(range(1,d+1))+list(range(d,0,-1))+[0]*(n-2*d)
  else:a=list(range(1,n+1))
  return f"{n}\n"+' '.join(map(str,a))+'\n'
 if number==18155:
  n=r.randint(1,16);a=[r.randint(1,30) for _ in range(n)];target=(r.choice(a) if seed%2 else r.randint(1,10**7));return f"{target}\n"+' '.join(map(str,a))+'\n'
 if number==28700:
  n=r.randint(1,3999);return (_roman(n) if seed%2 else str(n))+'\n'
 if number==4013:
  chunks=[]
  for _ in range(r.randint(1,10)):
   n=15000 if seed==20 and not chunks else r.randint(1,100);chunks.append(str(n));chunks.extend(str(r.randint(-10**9,10**9)) for _ in range(n))
  return '\n'.join(chunks+['0'])+'\n'
 if number==4014:
  rows=[]
  for _ in range(r.randint(1,20)):
   n=r.randint(1,30);s=''.join(r.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(n));p=list(range(1,n+1));r.shuffle(p);rows.append(f"{s} {r.randint(-1000,1000)} "+' '.join(map(str,p)))
  return '\n'.join(rows)+'\n'
 if number==4016:
  n=r.randint(1,500);ids=r.sample(range(1,10**9),n);return f"{n}\n"+'\n'.join(f'{x} {r.randint(1,100)}' for x in ids)+'\n'
 if number==4017:return '\n'.join(str(r.randint(1,30)) for _ in range(r.randint(1,30)))+'\n'
 if number==4019:return '\n'.join(str(r.randint(1,7)) for _ in range(r.randint(1,30)))+'\n'
 if number==4020:
  deck=[s+v for s in ('Heart','Spade','Diamond','Club') for v in ('2','3','4','5','6','7','8','9','10','Ace','Jack','Queen','King')]+['Joker','joker'];count=r.randint(1,30);rows=[]
  for _ in range(count):missing=r.randrange(54);cards=deck[:missing]+deck[missing+1:];r.shuffle(cards);rows.append(' '.join(cards))
  return f"{count}\n"+'\n'.join(rows)+'\n'
 if number==4042:
  count=r.randint(1,50);rows=[]
  for _ in range(count):
   n=r.randint(2,100);s=''.join(r.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(n));rows.append(f"{s} {r.randint(1,n-1)} {r.randint(1,26*n)}")
  return f"{count}\n"+'\n'.join(rows)+'\n'
 if number==4044:
  n=r.randint(1,1000);weights=r.sample(range(1,2**31),n);return f"{n}\n"+'\n'.join(f"{w} {''.join(r.choice('abcdefgh') for _ in range(r.randint(1,10)))}" for w in weights)+'\n'
 if number==4068:
  count=r.randint(1,100);rows=[]
  for _ in range(count):rows.append(' '.join(str(r.randint(-10000,10000)) for _ in range(r.randint(1,100))))
  return f"{count}\n"+'\n'.join(rows)+'\n'
 raise KeyError(number)

def valid(number,text):
 try:
  lines=text.rstrip('\n').splitlines();tokens=text.split()
  if number==16529:
   n=int(lines[0]);a=list(map(float,lines[1].split()));return len(lines)==2 and 1<=n<=100000 and len(a)==n and min(a)>0
  if number==27626:return len(tokens)==1 and 0<int(tokens[0])<50000000
  if number==29949:
   n,m=map(int,lines[0].split());rows=[list(map(int,x.split())) for x in lines[1:]];return 1<=n<=100 and 1<=m<=10000 and len(rows)==n and all(len(x)==2 and all(1<=v<=1000 for v in x) for x in rows)
  if number==30947:
   n,q=map(int,lines[0].split());a=list(map(int,lines[1].split()));x=list(map(int,lines[2:]));return 1<=n<=100000 and 1<=q<=100 and len(a)==n and len(x)==q and all(0<=v<=10**9 for v in a) and all(1<=v<=10**9 for v in x)
  if number==16530:return len(lines)>=3 and 2<=int(lines[0])<=1000 and int(lines[0])%2==0 and len(lines)==int(lines[0])+1 and all(1<=len(x)<30 and x.isupper() and x.isalpha() for x in lines[1:])
  if number==27122:
   n,m=map(int,lines[0].split());a=list(map(int,lines[1].split()));return len(lines)==2 and 2<=m<=n<=100000 and len(a)==len(set(a))==n
  if number==27925:
   t=int(lines[0]);groups=lines[1:1+t]
   if not 1<=t<100 or len(groups)!=t or any(not x.split() or len(x.split())>1000 for x in groups):return False
   ids=[int(v) for row in groups for v in row.split()]
   if len(ids)!=len(set(ids)) or any(not 0<=x<=999999 for x in ids):return False
   live=0
   for row in lines[1+t:]:
    if row=='STOP':return row==lines[-1]
    if row=='DEQUEUE':
     if live==0:return False
     live-=1
    elif re.fullmatch(r'ENQUEUE \d+',row):live+=1
    else:return False
   return False
  if number==27373:
   m=int(lines[0]);n=int(lines[1]);a=lines[2].split();return len(lines)==3 and 1<=m<=200 and 1<=n<=1000 and len(a)==n and all(x.isdigit() and 0<int(x) and len(x)<=20 for x in a)
  if number==27363:
   n=int(lines[0]);a=list(map(int,lines[1].split()));return len(lines)==2 and 1<=n<50000 and len(a)==n and all(0<=x<=n for x in a)
  if number==18155:return len(lines)==2 and 1<=len(lines[1].split())<=16 and all(int(x)>0 for x in lines[1].split())
  if number==28700:
   s=lines[0]
   if len(lines)!=1:return False
   if s.isdigit():return 1<=int(s)<=3999
   values={'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000};total=0;prev=0
   for c in reversed(s):v=values.get(c,0);total += -v if v<prev else v;prev=max(prev,v)
   return bool(s) and _roman(total)==s
  if number==4013:
   i=0;groups=0
   while i<len(lines):
    n=int(lines[i]);i+=1
    if n==0:return groups>0 and i==len(lines)
    if not 1<=n<=15000 or i+n>len(lines):return False
    list(map(int,lines[i:i+n]));i+=n;groups+=1
   return False
  if number==4014:
   for row in lines:
    p=row.split();s=p[0];order=list(map(int,p[2:]));
    if not 1<=len(s)<=30 or not s.isupper() or not s.isalpha() or sorted(order)!=list(range(1,len(s)+1)):return False
   return bool(lines)
  if number==4016:
   n=int(lines[0]);rows=[x.split() for x in lines[1:]];return 1<=n<=500 and len(rows)==n and len({x[0] for x in rows})==n and all(len(x)==2 and x[0].isdigit() and len(x[0])<10 and 1<=int(x[1])<=100 for x in rows)
  if number in (4017,4019):return bool(lines) and all((1<=int(x)<=30 if number==4017 else 1<=int(x)<=7) for x in lines)
  if number==4020:
   deck={s+v for s in ('Heart','Spade','Diamond','Club') for v in ('2','3','4','5','6','7','8','9','10','Ace','Jack','Queen','King')}|{'Joker','joker'};n=int(lines[0]);return 1<=n<=100 and len(lines)==n+1 and all(len(x.split())==len(set(x.split()))==53 and set(x.split())<deck for x in lines[1:])
  if number==4042:
   n=int(lines[0]);rows=[x.split() for x in lines[1:]];return 1<=n<=100 and len(rows)==n and all(len(x)==3 and x[0].islower() and x[0].isalpha() and 1<=int(x[1])<len(x[0]) for x in rows)
  if number==4044:
   n=int(lines[0]);rows=[x.split() for x in lines[1:]];return 1<=n<=1000 and len(rows)==n and len({int(x[0]) for x in rows})==n and all(len(x)==2 and int(x[0])>0 and 1<=len(x[1])<=10 for x in rows)
  if number==4068:return 1<=int(lines[0])<=100 and len(lines)==int(lines[0])+1 and all(x.split() and all(re.fullmatch(r'-?\d+',v) for v in x.split()) for x in lines[1:])
 except (ValueError,IndexError,TypeError,KeyError):return False
 return False


import subprocess as _subprocess, sys as _sys, tempfile as _tempfile
from pathlib import Path as _Path
REFERENCE='# External reference: http://cs101.openjudge.cn/practice/27373/statistics/\n# Accepted submission: 52527803\n# Source: http://cs101.openjudge.cn/practice/solution/52527803/\n# License: not declared on the submission page; no license is inferred.\n\nfrom functools import cmp_to_key\n\nm=int(input())\nn=int(input())\narr=input().split()\n\ndef compare(x,y):\n    if x+y>y+x:\n        return -1\n    elif x+y<y+x:\n        return 1\n    else:\n        return 0\narr.sort(key=cmp_to_key(compare))\n\ndef newmax(a,b):\n    if len(a)>len(b):\n        return a\n    elif len(a)<len(b):\n        return b\n    else:\n        return a if a>b else b\n#dp[i] 表示，长度不超过i的最大值\ndp=[""]*(m+1)\nfor num in arr:\n    ll=len(num)\n    for j in range(m,ll-1,-1):\n        dp[j]=newmax(dp[j],dp[j-ll]+num)\nprint(dp[-1])\n'
LANGUAGE='Python3'
NUMBER=27373
SAMPLE='4\n4\n23 9 182 79\n'
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
