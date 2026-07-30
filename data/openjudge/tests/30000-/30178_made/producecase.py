#!/usr/bin/env python3
"""Problem-specific generators and input contracts for T-028 phase-2 round 22."""
from __future__ import annotations
import random,re

NUMBERS={30339,30163,30868,30178,29335,19959,20101,27150,27947,28193,
28276,28912,29256,29886,29950,29952,29954,30172,30442,27093}
EXEMPTIONS={27150:"only the unique NO branch is generated because successful divisible subsequences are non-unique"}
MULTI_ANSWER_EXEMPTIONS={27150:{"reason":"every generated digit string has no divisible-by-eight subsequence","unique_output_tokens":["NO"]}}
FILTER_INVALID_ARCHIVE_INPUTS={30172}
INPUT_DOMAINS={
30339:"第一行两个整数 N,M（1≤N,M≤50）。",
30163:"M (0 < M <= 30)、N (0 < N <= 30)。",
30868:"对于全部数据， 0 ≤ hi ≤ n, 0 ≤ q ≤ 10^5, 1 ≤ n ≤ 10^{18}, 0 ≤ a,b,c ≤ 10^6 。",
30178:"第 1 行：一个整数 n ，(2 <= n <= 1000)",
29335:"1 <= len(path) <= 3000 path 由英文字母，数字， '.' ， '/' 或 '_' 组成。",
19959:"第一行为一个正整数n，n<=10^12",
20101:"输入的多项式次数不超过9次，各系数绝对值不超过9。",
27150:"一个不超过200万位的非负整数，且没有前导零。",
27947:"1<=M<=99999 且所有 M 相加之和不超过500000。",
28193:"第一行包含两个整数n和m（1 ≤ n ≤ 10**5， 0 ≤ m ≤ 10**5）",
28276:"第一行：正整数 n<50, 代表输入的字符串数量。",
28912:"第1行，2个正整数 n,M。1 ≤ n ≤ 3000；1 ≤ M ≤ 10^9；",
29256:"第一行为两个整数 n ​和 m ​，分别表示有 n​ 位选手和 m 个组（1 < n < 50000，1 <= m <= n)",
29886:"1 <= power.length <= 19 1 <= power[i] <= 10^9",
29950:"一行，一个仅包含小写英文字母的字符串 s (1 <= 字符串长度 <= 50000)。",
29952:"一行，一个只包含 ( 和 ) 的字符串，长度不超过 30000。",
29954:"第一行包含三个整数 R, C, K (1 <= R, C <= 100, 0 <= K <= 10)。",
30172:"第一行是数字n (n <= 1000)，表示节点的总数（包括起始节点和终止节点）",
30442:"保证所有测试用例中 n 的总和不超过 2*10^5。",
27093:"第一行包含两个正整数 N, D (1<=N<=10^5, 1<=D<=10^9)。",
}
SAMPLE_INPUTS={30868:"7 3 5\n4\n4\n10\n13\n41\n",29335:"/home/\n",19959:"9\n",20101:"-1\nx^2+2x+1\n",27150:"111111\n",
29886:"3 1 4\n",
28193:"5 2\n2 5 3 4 8\n1 4\n4 5\n",28276:"2\na==b b!=a\n",
28912:"3 5\n1 3 1\n1 -4 -4\n-2 5 1\n",29256:"5 2\n100 80 90 75 95\n"}
SAMPLE_OUTPUTS={30868:"No\nYes\nYes\nYes\n",29335:"/home\n",19959:"130\n",20101:"(x+1)^2\n",27150:"NO\n",
30163:"11\n",29886:"4\n",28193:"10\n",28276:"False\n",28912:"10 -8\n",
29256:"260\n",30442:"11\n2\n12\n"}
LABELS={
30339:"a 1..50 rectangular dot-X grid contains exactly three four-connected islands",
30163:"1 or more groups contain 1..30 rectangular height grids in -65..319 and an in-bounds water source",
30868:"three step sizes in 0..10^6 precede 1..100000 query heights in 0..10^18",
30178:"a 2..1000 square board is a permutation of 0..n^2-1",
29335:"the single 1..3000-character valid absolute Unix path uses only the stated character alphabet",
19959:"the input is one positive integer at most 10^12",
20101:"a nonzero shift and a nonzero descending polynomial of degree at most 9 have coefficients in -9..9",
27150:"the 1..2000000-digit nonnegative integer has no leading zero",
27947:"1..100 datasets have 1..99999 integers each and at most 500000 integers in total",
28193:"a graph of 1..100000 vertices has at most 100000 unique non-loop edges and bounded nonnegative costs",
28276:"1..49 four-character lowercase equality or inequality relations follow the declared count",
28912:"1..3000 absolute-value terms obey all coefficient bounds and 1<=M<=10^9",
29256:"2..49999 positive scores in 2..999 are partitioned into 1..n nonempty consecutive groups",
29886:"the single row contains 1..19 boss powers in 1..10^9",
29950:"the single string has 1..50000 lowercase letters",
29952:"the single nonempty string has at most 30000 parentheses",
29954:"a 1..100 rectangular grid over dot-hash-S-E has exactly one start and one exit with 0<=K<=10",
30172:"2..1000 named nodes define every nonterminal row with at most 10 weighted outgoing edges",
30442:"1..10000 arrays have lengths 3..200000, values 1..100 and total length at most 200000",
27093:"1..100000 positive heights at most 10^9 follow a distance in 1..10^9",
}
INVALID={30339:"2 2\nXX\nXX\n",30163:"1\n31 1\n0\n1 1\n",30868:"1 2 3\n1\n-1\n",
30178:"2\n0 1\n1 3\n",29335:"relative/path\n",19959:"0\n",20101:"0\nx+1\n",27150:"0123\n",
27947:"1\n\n",28193:"2 1\n1 2\n1 1\n",28276:"1\na=b\n",28912:"1 0\n1 2 3\n",
29256:"2 3\n4 5\n",29886:"0 1\n",29950:"abcD\n",29952:"()a\n",29954:"2 2 0\nS.\n..\n",
30172:"1\na a\n",30442:"1\n2\n1 2\n",27093:"2 0\n1 2\n"}

def _poly(r):
 d=r.randint(1,9);terms=[]
 for power in range(d,-1,-1):
  c=r.randint(-9,9)
  if power==d and c==0:c=1
  if c==0:continue
  sign='-' if c<0 else ('+' if terms else '')
  a=abs(c)
  if power==0:body=str(a)
  else:body=('' if a==1 else str(a))+'x'+('' if power==1 else '^'+str(power))
  terms.append(sign+body)
 return ''.join(terms)

def generate(number,seed):
 r=random.Random(number*1_000_003+seed)
 if number==30339:
  n,m=r.randint(3,50),r.randint(3,50);g=[['.']*m for _ in range(n)]
  points=r.sample([(i,j) for i in range(n) for j in range(m)],3)
  while min(abs(a-c)+abs(b-d) for i,(a,b) in enumerate(points) for c,d in points[i+1:])<2:points=r.sample([(i,j) for i in range(n) for j in range(m)],3)
  for i,j in points:g[i][j]='X'
  return f"{n} {m}\n"+'\n'.join(''.join(x) for x in g)+'\n'
 if number==30163:
  blocks=[]
  for _ in range(r.randint(1,5)):
   m,n=r.randint(1,8),r.randint(1,8);rows=[[r.randint(-65,319) for _ in range(n)] for _ in range(m)]
   blocks.append(f"{m} {n}\n"+'\n'.join(' '.join(map(str,x)) for x in rows)+f"\n{r.randint(1,m)} {r.randint(1,n)}")
  return f"{len(blocks)}\n"+'\n'.join(blocks)+'\n'
 if number==30868:
  steps=[r.randint(0,10**6) for _ in range(3)];q=r.randint(1,200);h=[r.randint(0,10**18) for _ in range(q)]
  return ' '.join(map(str,steps))+f"\n{q}\n"+'\n'.join(map(str,h))+'\n'
 if number==30178:
  n=30 if seed==20 else r.randint(2,12);a=list(range(n*n));r.shuffle(a)
  return f"{n}\n"+'\n'.join(' '.join(map(str,a[i*n:(i+1)*n])) for i in range(n))+'\n'
 if number==29335:
  parts=[]
  for _ in range(r.randint(1,100)):
   parts.append(r.choice(('.', '..', '...', ''.join(r.choice('abcXYZ012_') for _ in range(r.randint(1,12))))))
  return '/'+'/'.join(parts)+('/'*r.randint(0,4))+'\n'
 if number==19959:return f"{10**12 if seed==20 else r.randint(1,10**12)}\n"
 if number==20101:return f"{r.choice([x for x in range(-20,21) if x])}\n{_poly(r)}\n"
 if number==27150:return '1'*(seed%1999+2)+'\n'
 if number==27947:
  rows=[];total=0
  for _ in range(r.randint(1,10)):
   n=r.randint(1,min(2000,500000-total));total+=n;rows.append(' '.join(str(r.randint(-10**9,10**9)) for _ in range(n)))
  return f"{len(rows)}\n"+'\n'.join(rows)+'\n'
 if number==28193:
  n=r.randint(1,500);maxe=min(1000,n*(n-1)//2);m=r.randint(0,maxe);edges=set()
  while len(edges)<m:
   a,b=r.sample(range(1,n+1),2);edges.add(tuple(sorted((a,b))))
  return f"{n} {m}\n"+' '.join(str(r.randint(0,10**9)) for _ in range(n))+'\n'+'\n'.join(f'{a} {b}' for a,b in sorted(edges))+('\n' if edges else '')
 if number==28276:
  rows=[]
  for _ in range(r.randint(1,49)):
   rows.append(r.choice('abcdefghijklmnopqrstuvwxyz')+r.choice(('==','!='))+r.choice('abcdefghijklmnopqrstuvwxyz'))
  return f"{len(rows)}\n"+' '.join(rows)+'\n'
 if number==28912:
  n=r.randint(1,300);M=r.randint(1,10**9);rows=[f"{r.randint(-1000,1000)} {r.randint(-10**9,10**9)} {r.randint(-1000,1000)}" for _ in range(n)]
  return f"{n} {M}\n"+'\n'.join(rows)+'\n'
 if number==29256:
  n=49999 if seed==20 else r.randint(2,1000);return f"{n} {r.randint(1,n)}\n"+' '.join(str(r.randint(2,999)) for _ in range(n))+'\n'
 if number==29886:
  n=16 if seed==20 else r.randint(1,12);return ' '.join(str(r.randint(1,10**9)) for _ in range(n))+'\n'
 if number==29950:
  n=50000 if seed==20 else r.randint(1,3000);return ''.join(r.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(n))+'\n'
 if number==29952:
  n=30000 if seed==20 else r.randint(1,3000);return ''.join(r.choice('()') for _ in range(n))+'\n'
 if number==29954:
  R,C=r.randint(1,20),r.randint(2,20);K=r.randint(0,10);g=[[r.choice('.#') for _ in range(C)] for _ in range(R)];g[0][0]='S';g[-1][-1]='E'
  return f"{R} {C} {K}\n"+'\n'.join(''.join(x) for x in g)+'\n'
 if number==30172:
  n=r.randint(2,30);names=['node'+chr(97+i//26)+chr(97+i%26) for i in range(n)];end=names[-1];rows=[]
  if seed%5==0 and n>=4:
   edges={i:[] for i in range(n-1)};edges[0]=[(1,1)];edges[1]=[(2,1)];edges[2]=[(1,1)]
  else:
   edges={i:[] for i in range(n-1)}
   for i in range(n-1):
    choices=list(range(i+1,min(n,i+11)));pick=r.sample(choices,r.randint(1,min(len(choices),3)))
    edges[i]=[(j,r.randint(-1000,1000)) for j in pick]
  for i in range(n-1):rows.append(names[i]+' '+str(len(edges[i]))+''.join(f' {names[j]} {w}' for j,w in edges[i]))
  return f"{n}\n{names[0]} {end}\n"+'\n'.join(rows)+'\n'
 if number==30442:
  blocks=[];total=0
  for _ in range(r.randint(1,10)):
   n=r.randint(3,min(2000,200000-total));total+=n;blocks.append(f"{n}\n"+' '.join(str(r.randint(1,100)) for _ in range(n)))
  return f"{len(blocks)}\n"+'\n'.join(blocks)+'\n'
 if number==27093:
  n=100000 if seed==20 else r.randint(1,2000);return f"{n} {r.randint(1,10**9)}\n"+' '.join(str(r.randint(1,10**9)) for _ in range(n))+'\n'
 raise KeyError(number)

def valid(number,text):
 try:
  lines=text.rstrip('\n').splitlines();tokens=text.split()
  if number==30339:
   n,m=map(int,lines[0].split());g=lines[1:];seen=set();count=0
   for i in range(n):
    for j in range(m):
     if g[i][j]=='X' and (i,j) not in seen:
      count+=1;stack=[(i,j)];seen.add((i,j))
      while stack:
       x,y=stack.pop()
       for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
        p=(x+dx,y+dy)
        if 0<=p[0]<n and 0<=p[1]<m and g[p[0]][p[1]]=='X' and p not in seen:seen.add(p);stack.append(p)
   return 1<=n<=50 and 1<=m<=50 and len(g)==n and all(len(x)==m and set(x)<={'.','X'} for x in g) and count==3
  if number==30163:
   k=int(lines[0]);pos=1
   if k<1:return False
   for _ in range(k):
    m,n=map(int,lines[pos].split());pos+=1;rows=[list(map(int,x.split())) for x in lines[pos:pos+m]];pos+=m;x,y=map(int,lines[pos].split());pos+=1
    if not 1<=m<=30 or not 1<=n<=30 or len(rows)!=m or any(len(a)!=n or any(not -65<=v<=319 for v in a) for a in rows) or not(1<=x<=m and 1<=y<=n):return False
   return pos==len(lines)
  if number==30868:
   a,b,c=map(int,lines[0].split());q=int(lines[1]);h=list(map(int,lines[2:]));return all(0<=x<=10**6 for x in(a,b,c)) and 1<=q<=10**5 and len(h)==q and all(0<=x<=10**18 for x in h)
  if number==30178:
   n=int(lines[0]);rows=[list(map(int,x.split())) for x in lines[1:]];return 2<=n<=1000 and len(rows)==n and all(len(x)==n for x in rows) and {v for x in rows for v in x}==set(range(n*n))
  if number==29335:return len(lines)==1 and 1<=len(lines[0])<=3000 and lines[0].startswith('/') and bool(re.fullmatch(r'[A-Za-z0-9._/]+',lines[0]))
  if number==19959:return len(tokens)==1 and 1<=int(tokens[0])<=10**12
  if number==20101:return len(lines)==2 and int(lines[0])!=0 and lines[1]!='0' and bool(re.fullmatch(r'[+-]?(?:(?:[1-9]?x(?:\^[1-9])?)|[1-9])(?:[+-](?:(?:[1-9]?x(?:\^[1-9])?)|[1-9]))*',lines[1]))
  if number==27150:return len(lines)==1 and bool(re.fullmatch(r'(?:0|[1-9]\d{0,1999999})',lines[0]))
  if number==27947:
   t=int(lines[0]);rows=[list(map(int,x.split())) for x in lines[1:]];return 1<=t<=100 and len(rows)==t and all(1<=len(x)<=99999 for x in rows) and sum(map(len,rows))<=500000
  if number==28193:
   n,m=map(int,lines[0].split());cost=list(map(int,lines[1].split()));edges=[tuple(map(int,x.split())) for x in lines[2:]];return 1<=n<=10**5 and 0<=m<=10**5 and len(cost)==n and all(0<=x<=10**9 for x in cost) and len(edges)==len(set(tuple(sorted(x)) for x in edges))==m and all(len(x)==2 and 1<=x[0]<=n and 1<=x[1]<=n and x[0]!=x[1] for x in edges)
  if number==28276:return 1<=int(tokens[0])<50 and len(tokens)==int(tokens[0])+1 and all(re.fullmatch(r'[a-z](?:==|!=)[a-z]',x) for x in tokens[1:])
  if number==28912:
   n,M=map(int,lines[0].split());rows=[list(map(int,x.split())) for x in lines[1:]];return 1<=n<=3000 and 1<=M<=10**9 and len(rows)==n and all(len(x)==3 and -1000<=x[0]<=1000 and -10**9<=x[1]<=10**9 and -1000<=x[2]<=1000 for x in rows)
  if number==29256:
   n,m=map(int,lines[0].split());a=list(map(int,lines[1].split()));return len(lines)==2 and 1<n<50000 and 1<=m<=n and len(a)==n and all(1<x<1000 for x in a)
  if number==29886:return len(lines)==1 and 1<=len(tokens)<=19 and all(1<=int(x)<=10**9 for x in tokens)
  if number==29950:return bool(re.fullmatch(r'[a-z]{1,50000}\n?',text))
  if number==29952:return bool(re.fullmatch(r'[()]{1,30000}\n?',text))
  if number==29954:
   R,C,K=map(int,lines[0].split());g=lines[1:];s=''.join(g);return 1<=R<=100 and 1<=C<=100 and 0<=K<=10 and len(g)==R and all(len(x)==C and set(x)<={'.','#','S','E'} for x in g) and s.count('S')==s.count('E')==1
  if number==30172:
   n=int(lines[0]);start,end=lines[1].split();rows=lines[2:];names=set((start,end))
   if not 2<=n<=1000 or len(rows)!=n-1 or not all(re.fullmatch(r'[a-z_]+',x) for x in(start,end)):return False
   for row in rows:
    p=row.split();m=int(p[1])
    if not 0<=m<=10 or len(p)!=2+2*m or not re.fullmatch(r'[a-z_]+',p[0]):return False
    names.add(p[0])
    for i in range(m):
     if not re.fullmatch(r'[a-z_]+',p[2+2*i]):return False
     int(p[3+2*i]);names.add(p[2+2*i])
   return len(names)==n and start not in {p[2+2*i] for row in rows for p in [row.split()] for i in range(int(p[1]))} and end not in {row.split()[0] for row in rows}
  if number==30442:
   t=int(lines[0]);pos=1;total=0
   if not 1<=t<=10**4:return False
   for _ in range(t):
    n=int(lines[pos]);pos+=1;a=list(map(int,lines[pos].split()));pos+=1;total+=n
    if not 3<=n<=2*10**5 or len(a)!=n or any(not 1<=x<=100 for x in a):return False
   return pos==len(lines) and total<=2*10**5
  if number==27093:
   n,D=map(int,lines[0].split());a=list(map(int,lines[1].split()));return len(lines)==2 and 1<=n<=10**5 and 1<=D<=10**9 and len(a)==n and all(1<=x<=10**9 for x in a)
 except (ValueError,IndexError,TypeError):return False
 return False


import subprocess as _subprocess, sys as _sys, tempfile as _tempfile
from pathlib import Path as _Path
REFERENCE='# External reference: http://cs101.openjudge.cn/practice/30178/statistics/\n# Accepted submission: 52726449\n# Source: http://cs101.openjudge.cn/practice/solution/52726449/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef solve():\n    # 使用快速读取\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n\n    n = int(input_data[0])\n    matrix = list(map(int, input_data[1:]))\n\n    zero_row = 0\n    sequence = []\n\n    # 找到 0 的位置并提取非零序列\n    for i in range(len(matrix)):\n        val = matrix[i]\n        if val == 0:\n            zero_row = i // n\n        else:\n            sequence.append(val)\n\n    # 计算逆序对奇偶性 (使用 O(N) 的环分解算法)\n    # 逆序对奇偶性 = (元素个数 - 环的个数) % 2\n    l = len(sequence)\n    visited = [False] * l\n    cycles = 0\n\n    # 建立数值到索引的映射（如果数值不是 1~N-1，则需要离散化，这里题目说是 1 到 n^2-1）\n    # 由于数值是 1 到 n^2-1，我们可以直接计算\n    for i in range(l):\n        if not visited[i]:\n            cycles += 1\n            curr = i\n            while not visited[curr]:\n                visited[curr] = True\n                # sequence[curr] 是 1 到 n^2-1，映射回索引要减 1\n                curr = sequence[curr] - 1\n\n    inv_parity = (l - cycles) % 2\n\n    # 判断逻辑\n    if n % 2 != 0:\n        # n 为奇数：逆序对必须为偶数\n        if inv_parity == 0:\n            print("yes")\n        else:\n            print("no")\n    else:\n        # n 为偶数：(逆序对 + 空格行号) 的奇偶性必须与 (0 + n-1) 一致\n        if (inv_parity + zero_row) % 2 == (n - 1) % 2:\n            print("yes")\n        else:\n            print("no")\n\nif __name__ == "__main__":\n    solve()\n'
LANGUAGE='Python3'
NUMBER=30178
SAMPLE='4\n1 2 3 4\n5 6 7 8\n9 10 11 12\n13 14 15 0\n'
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
