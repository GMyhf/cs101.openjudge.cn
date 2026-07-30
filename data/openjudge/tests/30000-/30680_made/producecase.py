#!/usr/bin/env python3
"""Problem-specific generators and input contracts for T-028 phase-2 round 24."""
from __future__ import annotations
import heapq
import random
import re
import string

NUMBERS={30637,30669,30680,30720,30889,30894,30899,30908,30909,30910,
30942,30943,30953,31069,30888,30911,28749,30571,30937,30887}
EXEMPTIONS={}
BROKEN_ARCHIVE_FILTERS={30720:lambda case:(
 "non-power-of-two legacy output uses a tree layout inconsistent with all 42 scanned platform Accepted sources"
 if (lambda n:(n & (n-1)) != 0)(int(case.split()[0])) else None)}
INPUT_DOMAINS={
30637:"第一行是原始字符串x 后面有若干行(不超过50行)，每行一个字符串，所有字符串长度不超过100",
30669:"1 ≤ n ≤ 2×10^5, 1 ≤ t,p,q ≤ n, 1 ≤ v1,v2 ≤ 10^9, 1 ≤ u,v ≤ n,u≠v",
30680:"第一行：节点总个数 n (n < 1000)。",30720:"数据范围：1 <= n <= 10^5，0 <= m <= 10^5，注意：保证 (n+1)×(m+1)≤2×10^6",
30889:"The first line contains an integer n (1 ≤ n ≤ 2 × 10^5).",
30894:"第一行是整数n，表示字符集有n个字符。",30899:"1 < n,m <=3000",
30908:"数据范围 1 <= N <= 10^9， 1 <= Q <= 10^5",
30909:"第1行是整数n和m,表示山地是一个n×m的网格( 1 < n,m <= 100)",
30910:"第一行包括两个整数，n 和 m，表示村庄的村庄数量和道路数量。(n 不超过 1100,m 不超过 100000）",
30942:"给定一个长度不超过20000的由'T'或'F'构成的字符串，允许修改字符最多k次",
30943:"第一行包含两个整数 n，m，（2 <= n <= 50, 1 <= m <= 100）分别表示参与考试的学生人数，和小明做出提问数量。",
30953:"1 ≤ N, M ≤ 10^5",31069:"对所有数据, LA, LB <= 200000, k <= 26^2, q <= 100000 .",
30888:"The first line contains two integers N and B (1 ≤ N ≤ 10^5, 1 ≤ B ≤ 10^5).",
30911:"一行，包括三个整数n,delay和forget ( 1 <= n <= 100)",
28749:"输入的第一行包含两个整数n和m，其中n（1 <= n <= 2*10^5）是考得比较好的同学的数量，同学编号从1到n；m（0 <= m <= 2n）是志愿者的数量。",
30571:"非负整数N，0 <= N < 10^9",30937:"第一行两个数字 n, m 表示点数,以及边权为 1 的边数。(m <= min{200000, n(n-1)/2})",
30887:"The first line contains a single integer n (1 <= n <= 10^5).",
}
LABELS={
30637:"a unique 1..62 alphanumeric push string precedes at most 50 candidate lines of at most 100 characters",
30669:"a rooted tree and positive speeds place both teams on the same node after an integer number of days",
30680:"fewer than 1000 uniquely valued nodes form an acyclic forest and every node has one declaration row",
30720:"1..100000 values and 0..100000 indexed updates obey the product bound",
30889:"1..200000 parent-before-child rows form a rooted binary tree with unique L and R slots",
30894:"2..52 distinct letter weights define a Huffman tree and all following lines are encodable text or complete codes",
30899:"2..3000 stations and 2..3000 distinct positive weighted dependencies form a DAG",
30908:"1..10^9 particles receive 1..100000 syntactically valid online Add or Query operations",
30909:"a 2..100 rectangular height grid has values in 0..10000",
30910:"a directed positive weighted graph within stated size limits makes every village reachable both ways from village 1",
30942:"a nonempty T-F string of at most 20000 characters is paired with 0<=k<=length",
30943:"2..50 students and 1..100 unique consistent comparison answers use ordered x<y pairs",
30953:"1..100000 directed edges connect vertices in 1..N with exact row count",
31069:"bounded lowercase A and B, unique forbidden pairs, and in-range zero-based C queries follow declared counts",
30888:"1..100000 songs have difficulty 1..100 and accuracy 0..100 with B in 1..100000",
30911:"n is 1..100 and positive delay is strictly less than forget",
28749:"bounded R-P-W students and nonempty volunteer lists give every student degree at most two",
30571:"the sole integer is in 0..999999999",
30937:"distinct ordered one-edges fit the complete graph and m<=200000",
30887:"1..100000 positive values at most 10^9 follow the declared count",
}
INVALID={30637:"aa\naa\n",30669:"2 1\n1 2\n1 2 1 2\n",30680:"2\n1 2\n2 1\n",
30720:"2 1\n1 2\n2 3\n",30889:"3\n- -\n1 L\n1 L\n",30894:"2\na 1\na 2\na\n",
30899:"3 2\n1 2 1\n2 1 1\n",30908:"2 1\nQuery -1 0\n",30909:"1 2\n0 1\n",
30910:"2 1\n1 2 1\n",30942:"TFX\n1\n",30943:"3 2\n0 1 1\n0 1 0\n",
30953:"2 1\n1 3\n",31069:"1 1 1 1\na\na\na a\n0\n",30888:"1 0\n1 100\n",
30911:"4 3 3\n",28749:"1 1\nR\n2 1 1\n",30571:"1000000000\n",
30937:"3 2\n1 2\n1 2\n",30887:"2\n1 0\n"}
SAMPLE_INPUTS={30637:"abc\nabc\nbca\ncab\n",30680:"4\n15 2\n2\n8 20\n20\n",
30720:"8 1\n10 9 20 6 16 12 90 17\n3 15\n",30888:"3 2\n10 100\n8 95\n5 80\n",
30911:"4 1 3\n",28749:"8 6\nPWRWRRRP\n2 1 4\n1 2\n4 4 5 6 7\n3 5 6 7\n1 8\n1 8\n",
30571:"5\n",30937:"6 11\n1 3\n1 4\n1 5\n1 6\n2 3\n2 4\n2 5\n2 6\n3 4\n3 5\n3 6\n",
30887:"3\n1 2 3\n",30943:"5 4\n0 2 0\n1 2 0\n2 3 0\n2 4 0\n"}
SAMPLE_OUTPUTS={30637:"YES\nYES\nNO\n",30680:"8\n20\n2\n15\n",
30720:"6 12 9 17 10 20 16 90\n9 12 15 17 10 20 16 90\n",30888:"8.900000\n",
30911:"6\n",28749:"8\n",30571:"2\n",30937:"2\n",30887:"3\n",30943:"1\n"}

def _huffman(chars,weights):
 heap=[(w,c,c) for c,w in zip(chars,weights)];heapq.heapify(heap);tree={}
 while len(heap)>1:
  w1,k1,a=heapq.heappop(heap);w2,k2,b=heapq.heappop(heap);key=min(k1,k2);node=(a,b);heapq.heappush(heap,(w1+w2,key,node))
 root=heap[0][2];codes={}
 def walk(node,prefix):
  if isinstance(node,str):codes[node]=prefix;return
  walk(node[0],prefix+'0');walk(node[1],prefix+'1')
 walk(root,'');return codes

def generate(number,seed):
 r=random.Random(number*1_000_003+seed)
 if number==30637:
  x=''.join(r.sample(string.ascii_letters+string.digits,r.randint(1,30)));rows=[]
  for i in range(r.randint(2,20)):
   if i%3==0:
    stack=[];out=[];pos=0
    while pos<len(x) or stack:
     if pos<len(x) and (not stack or r.choice((0,1))):stack.append(x[pos]);pos+=1
     else:out.append(stack.pop())
    rows.append(''.join(out))
   else:rows.append(''.join(r.sample(x,len(x))) if i%3==1 else x[:-1])
  return x+'\n'+'\n'.join(rows)+'\n'
 if number==30669:
  days=r.randint(1,20);v1,v2=r.randint(1,20),r.randint(1,20);length=days*(v1+v2);n=length+1;t=r.randint(1,n);p,q=1,n
  return f"{n} {t}\n"+''.join(f"{i} {i+1}\n" for i in range(1,n))+f"{p} {q} {v1} {v2}\n"
 if number==30680:
  n=r.randint(1,100);vals=r.sample(range(1,10000),n);children=[[] for _ in range(n)]
  for i in range(1,n):
   if r.random()<.8:children[r.randrange(i)].append(i)
  rows=[str(vals[i])+(' '+' '.join(str(vals[j]) for j in children[i]) if children[i] else '') for i in range(n)];r.shuffle(rows)
  return f"{n}\n"+'\n'.join(rows)+'\n'
 if number==30720:
  n=2**r.randint(0,10);m=r.randint(0,min(1000,100_000//n-1));a=[r.randint(-10**9,10**9) for _ in range(n)]
  return f"{n} {m}\n"+' '.join(map(str,a))+'\n'+''.join(f"{r.randrange(n)} {r.randint(-10**9,10**9)}\n" for _ in range(m))
 if number==30889:
  n=r.randint(1,1000);slots={1:['L','R']};rows=['- -']
  for i in range(2,n+1):
   p=r.choice(list(slots));d=r.choice(slots[p]);slots[p].remove(d)
   if not slots[p]:del slots[p]
   slots[i]=['L','R'];rows.append(f"{p} {d}")
  return f"{n}\n"+'\n'.join(rows)+'\n'
 if number==30894:
  chars=r.sample(string.ascii_letters,r.randint(2,20));weights=[r.randint(1,1000) for _ in chars];codes=_huffman(chars,weights);rows=[]
  for i in range(r.randint(2,20)):
   plain=''.join(r.choice(chars) for _ in range(r.randint(1,30)));rows.append(plain if i%2==0 else ''.join(codes[x] for x in plain))
  return f"{len(chars)}\n"+''.join(f"{c} {w}\n" for c,w in zip(chars,weights))+'\n'.join(rows)+'\n'
 if number==30899:
  n=r.randint(3,100);all_edges=[(a,b) for a in range(1,n) for b in range(a+1,n+1)];m=r.randint(2,min(500,len(all_edges)));edges=r.sample(all_edges,m)
  return f"{n} {m}\n"+''.join(f"{a} {b} {r.randint(1,1000)}\n" for a,b in edges)
 if number==30908:
  n,q=r.randint(1,10**9),r.randint(1,1000);rows=[]
  for i in range(q):
   a,b=r.randrange(2**31),r.randrange(2**31)
   rows.append(f"Query {a} {b}" if i%4==0 else f"Add {a} {b} {r.randint(-10**9,10**9)}")
  return f"{n} {q}\n"+'\n'.join(rows)+'\n'
 if number==30909:
  n,m=r.randint(2,30),r.randint(2,30);return f"{n} {m}\n"+'\n'.join(' '.join(str(r.randint(0,10000)) for _ in range(m)) for _ in range(n))+'\n'
 if number==30910:
  n=r.randint(2,100);edges={(i,i%n+1):r.randint(1,1000) for i in range(1,n+1)}
  for _ in range(r.randint(0,300)):a,b=r.sample(range(1,n+1),2);edges[(a,b)]=r.randint(1,1000)
  return f"{n} {len(edges)}\n"+''.join(f"{a} {b} {w}\n" for (a,b),w in edges.items())
 if number==30942:
  n=20000 if seed==20 else r.randint(1,3000);s=''.join(r.choice('TF') for _ in range(n));return f"{s}\n{r.randint(0,n)}\n"
 if number==30943:
  n=r.randint(2,50);order=r.sample(range(n),n);rank={v:i for i,v in enumerate(order)};pairs=r.sample([(a,b) for a in range(n) for b in range(a+1,n)],r.randint(1,min(100,n*(n-1)//2)))
  return f"{n} {len(pairs)}\n"+''.join(f"{a} {b} {int(rank[a]<rank[b])}\n" for a,b in pairs)
 if number==30953:
  n=r.randint(1,2000);m=r.randint(1,min(5000,n*n));edges=[(r.randint(1,n),r.randint(1,n)) for _ in range(m)];return f"{n} {m}\n"+''.join(f"{a} {b}\n" for a,b in edges)
 if number==31069:
  la,lb=r.randint(1,80),r.randint(1,80);A=''.join(r.choice(string.ascii_lowercase) for _ in range(la));B=''.join(r.choice(string.ascii_lowercase) for _ in range(lb));pairs=r.sample([(a,b) for a in string.ascii_lowercase for b in string.ascii_lowercase],r.randint(0,100));blocked=set(pairs);C=''.join(a+b for a in A for b in B if (a,b) not in blocked)
  if not C:return generate(number,seed+10000)
  q=r.randint(1,200);queries=[r.randrange(len(C)) for _ in range(q)];return f"{la} {lb} {len(pairs)} {q}\n{A}\n{B}\n"+''.join(f"{a} {b}\n" for a,b in pairs)+'\n'.join(map(str,queries))+'\n'
 if number==30888:
  n,b=r.randint(1,5000),r.randint(1,10**5);return f"{n} {b}\n"+''.join(f"{r.randint(1,100)} {r.randint(0,100)}\n" for _ in range(n))
 if number==30911:
  n=r.randint(1,100);delay=r.randint(1,20);forget=r.randint(delay+1,30);return f"{n} {delay} {forget}\n"
 if number==28749:
  n=r.randint(1,100);m=r.randint(0,min(2*n,30));links=[set() for _ in range(m)]
  if m:
   slots=[student for student in range(1,n+1) for _ in range(2)];r.shuffle(slots)
   degree=[0]*(n+1)
   for volunteer,student in enumerate(slots[:m]):links[volunteer].add(student);degree[student]+=1
   for student in range(1,n+1):
    choices=[volunteer for volunteer in range(m) if student not in links[volunteer]]
    for volunteer in r.sample(choices,r.randint(0,min(2-degree[student],len(choices)))):
     if degree[student]<2 and student not in links[volunteer]:links[volunteer].add(student);degree[student]+=1
  return f"{n} {m}\n"+''.join(r.choice('RPW') for _ in range(n))+'\n'+''.join(str(len(g))+' '+' '.join(map(str,sorted(g)))+'\n' for g in links)
 if number==30571:return f"{r.randrange(10**9)}\n"
 if number==30937:
  n=r.randint(2,40);pairs=[(a,b) for a in range(1,n+1) for b in range(a+1,n+1)]
  if seed%3==0:edges=pairs
  elif seed%3==1:
   cut=r.randint(1,n-1);edges=[(a,b) for a in range(1,cut+1) for b in range(cut+1,n+1)]
  else:edges=r.sample(pairs,r.randint(0,len(pairs)//3))
  return f"{n} {len(edges)}\n"+''.join(f"{a} {b}\n" for a,b in edges)
 if number==30887:
  n=100000 if seed==20 else r.randint(1,5000);return f"{n}\n"+' '.join(str(r.randint(1,10**9)) for _ in range(n))+'\n'
 raise KeyError(number)

def valid(number,text):
 try:
  lines=text.rstrip('\n').splitlines();tokens=text.split()
  if number==30637:return 1<=len(lines[0])<=62 and len(set(lines[0]))==len(lines[0]) and set(lines[0])<=set(string.ascii_letters+string.digits) and 1<=len(lines)-1<=50 and all(len(x)<=100 for x in lines[1:])
  if number==30669:
   n,t=map(int,lines[0].split());edges=[tuple(map(int,x.split())) for x in lines[1:n]];p,q,v1,v2=map(int,lines[n].split())
   if not(1<=n<=200000 and 1<=t<=n and len(edges)==n-1 and all(1<=a<=n and 1<=b<=n and a!=b for a,b in edges) and 1<=p<=n and 1<=q<=n and 1<=v1<=10**9 and 1<=v2<=10**9):return False
   parent=list(range(n+1))
   def find(x):
    while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
    return x
   for a,b in edges:
    a,b=find(a),find(b)
    if a==b:return False
    parent[a]=b
   graph=[[] for _ in range(n+1)]
   for a,b in edges:graph[a].append(b);graph[b].append(a)
   prev={p:0};stack=[p]
   while stack:
    u=stack.pop()
    for v in graph[u]:
     if v not in prev:prev[v]=u;stack.append(v)
   path=[];u=q
   while u:path.append(u);u=prev[u]
   L=len(path)-1
   return L%(v1+v2)==0 and (L//(v1+v2))*v1<=L
  if number==30680:
   n=int(lines[0]);rows=[list(map(int,x.split())) for x in lines[1:]];heads=[x[0] for x in rows];all_children=[v for x in rows for v in x[1:]]
   if not 1<=n<1000 or len(rows)!=n or len(set(heads))!=n or any(not 1<=v<=9999 for v in heads) or any(v not in set(heads) for v in all_children) or len(all_children)!=len(set(all_children)):return False
   parent={v:None for v in heads}
   for row in rows:
    for v in row[1:]:parent[v]=row[0]
   return _forest_acyclic(parent)
  if number==30720:
   n,m=map(int,lines[0].split());a=list(map(int,lines[1].split()));updates=[tuple(map(int,x.split())) for x in lines[2:]];return 1<=n<=10**5 and 0<=m<=10**5 and (n+1)*(m+1)<=2_000_000 and len(a)==n and len(updates)==m and all(0<=i<n for i,v in updates)
  if number==30889:
   n=int(lines[0]);rows=[x.split() for x in lines[1:]];slots=set()
   if not 1<=n<=200000 or len(rows)!=n or rows[0]!=['-','-']:return False
   for i,row in enumerate(rows[1:],2):
    p=int(row[0]);key=(p,row[1])
    if len(row)!=2 or not 1<=p<i or row[1] not in 'LR' or key in slots:return False
    slots.add(key)
   return True
  if number==30894:
   n=int(lines[0]);defs=[x.split() for x in lines[1:n+1]];queries=lines[n+1:]
   if not 2<=n<=52 or len(defs)!=n or len({x[0] for x in defs})!=n or any(len(x)!=2 or len(x[0])!=1 or x[0] not in string.ascii_letters or int(x[1])<=0 for x in defs) or not queries:return False
   chars=[x[0] for x in defs];codes=_huffman(chars,[int(x[1]) for x in defs]);reverse=set(codes.values())
   for query in queries:
    if query.isdigit():
     pos=0
     while pos<len(query):
      hit=next((code for code in reverse if query.startswith(code,pos)),None)
      if hit is None:return False
      pos+=len(hit)
    elif not query or any(ch not in chars for ch in query):return False
   return True
  if number==30899:
   n,m=map(int,lines[0].split());edges=[tuple(map(int,x.split())) for x in lines[1:]];return 1<n<=3000 and 1<m<=3000 and len(edges)==m and len({(a,b) for a,b,w in edges})==m and all(1<=a<b<=n and w>0 for a,b,w in edges)
  if number==30908:
   n,q=map(int,lines[0].split());rows=[x.split() for x in lines[1:]];return 1<=n<=10**9 and 1<=q<=10**5 and len(rows)==q and all((len(x)==4 and x[0]=='Add' and 0<=int(x[1])<2**31 and 0<=int(x[2])<2**31 and -10**9<=int(x[3])<=10**9) or (len(x)==3 and x[0]=='Query' and 0<=int(x[1])<2**31 and 0<=int(x[2])<2**31) for x in rows) and any(x[0]=='Query' for x in rows)
  if number==30909:
   n,m=map(int,lines[0].split());rows=[list(map(int,x.split())) for x in lines[1:]];return 1<n<=100 and 1<m<=100 and len(rows)==n and all(len(x)==m and all(0<=v<=10000 for v in x) for x in rows)
  if number==30910:
   n,m=map(int,lines[0].split());edges=[tuple(map(int,x.split())) for x in lines[1:]]
   if not (2<=n<=1100 and 1<=m<=100000 and len(edges)==m) or any(not(1<=a<=n and 1<=b<=n and w>0) for a,b,w in edges):return False
   g=[[] for _ in range(n+1)];rg=[[] for _ in range(n+1)]
   for a,b,w in edges:g[a].append(b);rg[b].append(a)
   return len(_reach(g,1))==len(_reach(rg,1))==n
  if number==30942:return len(lines)==2 and bool(re.fullmatch(r'[TF]{1,20000}',lines[0])) and 0<=int(lines[1])<=len(lines[0])
  if number==30943:
   n,m=map(int,lines[0].split());rows=[tuple(map(int,x.split())) for x in lines[1:]]
   if not 2<=n<=50 or not 1<=m<=100 or len(rows)!=m or len({(x,y) for x,y,z in rows})!=m or any(not(0<=x<y<n and z in(0,1)) for x,y,z in rows):return False
   g=[[] for _ in range(n)]
   for x,y,z in rows:a,b=(x,y) if z else (y,x);g[a].append(b)
   return _dag(g)
  if number==30953:
   n,m=map(int,lines[0].split());edges=[tuple(map(int,x.split())) for x in lines[1:]];return 1<=n<=10**5 and 1<=m<=10**5 and len(edges)==m and all(1<=a<=n and 1<=b<=n for a,b in edges)
  if number==31069:
   la,lb,k,q=map(int,lines[0].split());A,B=lines[1:3];pairs=[tuple(x.split()) for x in lines[3:3+k]];queries=list(map(int,lines[3+k:]));blocked=set(pairs);length=sum(2 for a in A for b in B if (a,b) not in blocked)
   return 1<=la<=200000 and 1<=lb<=200000 and len(A)==la and len(B)==lb and A.islower() and B.islower() and 0<=k<=676 and len(pairs)==k==len(blocked) and all(len(a)==len(b)==1 and a.islower() and b.islower() for a,b in pairs) and 1<=q<=100000 and len(queries)==q and all(0<=x<length for x in queries)
  if number==30888:
   n,b=map(int,lines[0].split());rows=[tuple(map(int,x.split())) for x in lines[1:]];return 1<=n<=10**5 and 1<=b<=10**5 and len(rows)==n and all(1<=d<=100 and 0<=a<=100 for d,a in rows)
  if number==30911:
   n,d,f=map(int,tokens);return len(tokens)==3 and 1<=n<=100 and 1<=d<f
  if number==28749:
   n,m=map(int,lines[0].split());colors=lines[1];rows=[list(map(int,x.split())) for x in lines[2:]]
   if not 1<=n<=200000 or not 0<=m<=2*n or len(colors)!=n or set(colors)-set('RPW') or len(rows)!=m or any(not row or row[0]!=len(row)-1 or not 1<=row[0]<=n or len(set(row[1:]))!=row[0] or any(not 1<=x<=n for x in row[1:]) for row in rows):return False
   degree=[0]*(n+1)
   for row in rows:
    for x in row[1:]:degree[x]+=1
   return max(degree)<=2
  if number==30571:return len(tokens)==1 and 0<=int(tokens[0])<10**9
  if number==30937:
   n,m=map(int,lines[0].split());edges=[tuple(map(int,x.split())) for x in lines[1:]];return 1<=n<=100000 and 0<=m<=min(200000,n*(n-1)//2) and len(edges)==m==len(set(edges)) and all(1<=a<b<=n for a,b in edges)
  if number==30887:
   n=int(lines[0]);a=list(map(int,lines[1].split()));return len(lines)==2 and 1<=n<=10**5 and len(a)==n and all(1<=x<=10**9 for x in a)
 except (ValueError,IndexError,TypeError,StopIteration):return False
 return False

def _forest_acyclic(parent):
 for start in parent:
  seen=set();u=start
  while u is not None:
   if u in seen:return False
   seen.add(u);u=parent[u]
 return True

def _reach(g,start):
 seen={start};stack=[start]
 while stack:
  for v in g[stack.pop()]:
   if v not in seen:seen.add(v);stack.append(v)
 return seen

def _dag(g):
 state=[0]*len(g)
 def dfs(u):
  state[u]=1
  for v in g[u]:
   if state[v]==1 or (state[v]==0 and not dfs(v)):return False
  state[u]=2;return True
 return all(state[i] or dfs(i) for i in range(len(g)))


import subprocess as _subprocess, sys as _sys, tempfile as _tempfile
from pathlib import Path as _Path
REFERENCE='# External reference: http://cs101.openjudge.cn/practice/30680/statistics/\n# Accepted submission: 52783959\n# Source: http://cs101.openjudge.cn/practice/solution/52783959/\n# License: not declared on the submission page; no license is inferred.\n\nfrom collections import defaultdict\n\nn = int(input())\n\nchildren = defaultdict(list)\nindegree = defaultdict(int)\n\nnodes = set()\n\nfor _ in range(n):\n    arr = list(map(int, input().split()))\n\n    u = arr[0]\n    nodes.add(u)\n\n    for v in arr[1:]:\n        children[u].append(v)\n        indegree[v] += 1\n        nodes.add(v)\n\n# 找根节点\nroots = []\n\nfor x in nodes:\n    if indegree[x] == 0:\n        roots.append(x)\n\nroots.sort()\n\nans = []\n\ndef dfs(u):\n\n    cur = [(u, 0)]\n\n    for v in children[u]:\n        cur.append((v, 1))\n\n    cur.sort(key=lambda x: x[0])\n\n    for x, typ in cur:\n\n        if typ == 0:\n            ans.append(x)\n\n        else:\n            dfs(x)\n\nfor r in roots:\n    dfs(r)\n\nprint(*ans, sep="\\n")\n'
LANGUAGE='Python3'
NUMBER=30680
SAMPLE='4\n15 2\n2\n8 20\n20\n'
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
