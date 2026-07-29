#!/usr/bin/env python3
"""Shared builder for priority-ordered T-028 rounds 2 through 4."""
from __future__ import annotations

import argparse
import inspect
import json
import math
import random
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import t004_common as common
from build_001b import first_sample
from select_solution_batch import SOURCES, sections

ROOT = Path(__file__).resolve().parents[1]
OPENJUDGE = ROOT / "data" / "openjudge"
CANDIDATES = ROOT / "collab" / "t028-candidates.json"
SOURCE_URLS = {
    0: "https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md",
    1: "https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md",
}

# Source collection index and fenced-code index. Exceptions below use compact,
# format-robust implementations because the archived input is from an older
# batched statement or the problem permits several different correct outputs.
SOURCE_SPEC = {
    2694:(0,2),2945:(0,2),2746:(0,3),2773:(0,2),2734:(0,0),2488:(1,2),
    2810:(0,2),2299:(1,2),2775:(1,3),2815:(0,3),2524:(0,2),1088:(0,3),
    1182:(1,2),1760:(1,2),2386:(0,2),2456:(0,2),2808:(0,2),2995:(0,2),
    2760:(0,3),2733:(0,2),2774:(1,2),2806:(0,2),2754:(0,2),2783:(0,2),
    1094:(1,2),1376:(1,2),1833:(0,2),1961:(0,2),2255:(1,2),3248:(0,4),
    2692:(0,2),3143:(0,2),1035:(0,2),2431:(0,2),2756:(1,2),2757:(0,2),
    1159:(0,2),2706:(0,2),2996:(0,2),3254:(0,3),2502:(1,2),2748:(0,2),
    1191:(0,2),2287:(0,2),2981:(0,2),2788:(1,2),2802:(0,6),1003:(0,2),
    1011:(0,2),1017:(0,2),1065:(0,2),1218:(0,2),1724:(1,8),
}

CUSTOM = {
1426:r'''from collections import deque
for line in sys.stdin:
 n=int(line)
 if n==0: break
 q=deque([1%n]); parent={1%n:(None,'1')}
 while q:
  x=q.popleft()
  if x==0: break
  for d in '01':
   y=(x*10+int(d))%n
   if y not in parent: parent[y]=(x,d);q.append(y)
 out=[];x=0
 while x is not None: x,d=parent[x];out.append(d)
 print(''.join(reversed(out)))
''',
1724:r'''import heapq
t=list(map(int,sys.stdin.buffer.read().split())); p=0
K,N,R=t[p:p+3];p+=3;g=[[] for _ in range(N)]
for _ in range(R):
 a,b,d,c=t[p:p+4];p+=4;g[a-1].append((b-1,d,c))
q=[(0,0,0)];best=[{} for _ in range(N)];best[0][0]=0
while q:
 d,u,c=heapq.heappop(q)
 if best[u].get(c)!=d:continue
 if u==N-1:print(d);break
 for v,w,z in g[u]:
  nc=c+z;nd=d+w
  if nc>K or any(pc<=nc and pd<=nd for pc,pd in best[v].items()):continue
  for pc in [pc for pc,pd in best[v].items() if pc>=nc and pd>=nd]:del best[v][pc]
  best[v][nc]=nd;heapq.heappush(q,(nd,v,nc))
else:print(-1)
''',
1852:r'''a=list(map(int,sys.stdin.buffer.read().split()));p=1
for _ in range(a[0]):
 L,n=a[p:p+2];p+=2;x=a[p:p+n];p+=n
 print(max(min(v,L-v) for v in x),max(max(v,L-v) for v in x))
''',
1860:r'''a=sys.stdin.buffer.read().split();it=iter(a);n=int(next(it));m=int(next(it));s=int(next(it))-1;v=float(next(it));e=[]
for _ in range(m):
 x=int(next(it))-1;y=int(next(it))-1;r1=float(next(it));c1=float(next(it));r2=float(next(it));c2=float(next(it));e += [(x,y,r1,c1),(y,x,r2,c2)]
d=[0.0]*n;d[s]=v
gain=False
for i in range(n):
 changed=False
 for x,y,r,c in e:
  z=(d[x]-c)*r
  if z>d[y]:d[y]=z;changed=True
 if i==n-1 and changed:gain=True
 if not changed:break
print('YES' if gain else 'NO')
''',
2039:r'''a=sys.stdin.read().split();cols=int(a[0]);s=a[1];g=[s[i:i+cols] for i in range(0,len(s),cols)]
for i in range(1,len(g),2):g[i]=g[i][::-1]
print(''.join(g[i][j] for j in range(cols) for i in range(len(g))))
''',
2750:r'''a=int(input());print((f'{(a+3)//4} {a//2}') if a%2==0 else '0 0')
''',
2811:r'''x=[list(map(int,input().split())) for _ in range(5)]
for mask in range(64):
 p=[[0]*6 for _ in range(5)];p[0]=[(mask>>j)&1 for j in range(6)]
 for i in range(1,5):
  for j in range(6):p[i][j]=x[i-1][j]^p[i-1][j]^(p[i-2][j] if i>1 else 0)^(p[i-1][j-1] if j else 0)^(p[i-1][j+1] if j<5 else 0)
 if all((x[4][j]^p[4][j]^p[3][j]^(p[4][j-1] if j else 0)^(p[4][j+1] if j<5 else 0))==0 for j in range(6)):
  print('\n'.join(' '.join(map(str,row)) for row in p));break
''',
3151:r'''from collections import deque
A,B,C=map(int,input().split());q=deque([(0,0)]);prev={(0,0):None};how={}
while q:
 x,y=q.popleft()
 if x==C or y==C:
  out=[]
  while prev[(x,y)] is not None:out.append(how[(x,y)]);x,y=prev[(x,y)]
  print(len(out));print('\n'.join(reversed(out)));break
 z=min(x,B-y);w=min(y,A-x)
 for state,op in [((A,y),'FILL(1)'),((x,B),'FILL(2)'),((0,y),'DROP(1)'),((x,0),'DROP(2)'),((x-z,y+z),'POUR(1,2)'),((x+w,y-w),'POUR(2,1)')]:
  if state not in prev:prev[state]=(x,y);how[state]=op;q.append(state)
else:print('impossible')
''',
}


def generate(n, seed):
    r=random.Random(seed)
    if n==2694:
        return f"+ * {r.randint(-20,20)} {r.randint(-20,20)} / {r.randint(-20,20)} {r.randint(1,20)}\n"
    if n==2945:
        k=r.randint(3,25);return f"{k}\n"+' '.join(str(r.randint(1,500)) for _ in range(k))+'\n'
    if n==2746:
        return '\n'.join(f"{r.randint(1,80)} {r.randint(1,80)}" for _ in range(r.randint(1,5)))+'\n0 0\n'
    if n==2773:
        T=r.randint(20,300);m=r.randint(2,20);return f"{T} {m}\n"+'\n'.join(f"{r.randint(1,100)} {r.randint(1,100)}" for _ in range(m))+'\n'
    if n==2734:return f"{r.randint(1,65535)}\n"
    if n==2488:
        z=[(r.randint(1,6),r.randint(1,6)) for _ in range(r.randint(1,4))];return str(len(z))+'\n'+'\n'.join(f'{a} {b}' for a,b in z)+'\n'
    if n==2810:return f"{r.randint(2,45)}\n"
    if n==2299:
        a=[r.randint(0,10**9) for _ in range(r.randint(2,40))];return f"{len(a)}\n"+'\n'.join(map(str,a))+'\n0\n'
    if n==2775:return f"file{seed}\ndir{seed}\nfileA\n]\nfileZ\n*\n#\n"
    if n==2815:
        rows,cols=r.randint(2,7),r.randint(2,7);g=[[0]*cols for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                if j==0:g[i][j]|=1
                if i==0:g[i][j]|=2
                if j==cols-1:g[i][j]|=4
                if i==rows-1:g[i][j]|=8
                if j+1<cols and r.random()<.35:g[i][j]|=4;g[i][j+1]|=1
                if i+1<rows and r.random()<.35:g[i][j]|=8;g[i+1][j]|=2
        return f"{rows}\n{cols}\n"+'\n'.join(' '.join(map(str,x)) for x in g)+'\n'
    if n==2524:
        out=[]
        for _ in range(r.randint(1,3)):
            a=r.randint(2,30);edges={(r.randint(1,a),r.randint(1,a)) for _ in range(r.randint(0,a))};edges={(x,y) for x,y in edges if x!=y};out.append(f'{a} {len(edges)}');out += [f'{x} {y}' for x,y in edges]
        return '\n'.join(out)+'\n0 0\n'
    if n==1088:
        a,b=r.randint(2,12),r.randint(2,12);return f'{a} {b}\n'+'\n'.join(' '.join(str(r.randint(0,500)) for _ in range(b)) for _ in range(a))+'\n'
    if n==1182:
        N=r.randint(3,50);k=r.randint(2,70);return f'{N} {k}\n'+'\n'.join(f'{r.randint(1,2)} {r.randint(1,N+3)} {r.randint(1,N+3)}' for _ in range(k))+'\n'
    if n==1760:
        paths=[]
        for i in range(r.randint(2,20)):paths.append('\\'.join(f'D{r.randint(1,8)}' for _ in range(r.randint(1,5))))
        return str(len(paths))+'\n'+'\n'.join(paths)+'\n'
    if n==2386:
        a,b=r.randint(2,15),r.randint(2,15);return f'{a} {b}\n'+'\n'.join(''.join(r.choice('W..') for _ in range(b)) for _ in range(a))+'\n'
    if n==2456:
        N=r.randint(3,30);C=r.randint(2,N);x=sorted(r.sample(range(1,10000),N));return f'{N} {C}\n'+'\n'.join(map(str,x))+'\n'
    if n==2808:
        L=r.randint(10,1000);m=r.randint(1,15);return f'{L} {m}\n'+'\n'.join(f'{(a:=r.randint(0,L))} {r.randint(a,L)}' for _ in range(m))+'\n'
    if n==2995:
        N=r.randint(2,80);return f'{N}\n'+' '.join(str(r.randint(1,1000)) for _ in range(N))+'\n'
    if n==2760:
        N=r.randint(2,20);return f'{N}\n'+'\n'.join(' '.join(str(r.randint(0,100)) for _ in range(i)) for i in range(1,N+1))+'\n'
    if n==3151:
        A,B=r.randint(2,30),r.randint(2,30);C=r.randint(1,max(A,B));return f'{A} {B} {C}\n'
    if n==2733:return f'{r.randint(1,2999)}\n'
    if n==2774:
        N=r.randint(2,30);K=r.randint(1,100);return f'{N} {K}\n'+'\n'.join(str(r.randint(1,10000)) for _ in range(N))+'\n'
    if n==2806:
        return '\n'.join(f"{''.join(r.choice('abcd') for _ in range(r.randint(1,20)))} {''.join(r.choice('abcd') for _ in range(r.randint(1,20)))}" for _ in range(r.randint(1,6)))+'\n'
    if n==1426:return '\n'.join(str(r.randint(1,200)) for _ in range(r.randint(1,6)))+'\n0\n'
    if n==1852:
        out=[str(r.randint(1,4))]
        for _ in range(int(out[0])):
            L=r.randint(10,1000);x=sorted(r.sample(range(1,L),r.randint(1,min(20,L-1))));out += [f'{L} {len(x)}',' '.join(map(str,x))]
        return '\n'.join(out)+'\n'
    if n==2039:
        c=r.randint(2,20);s=''.join(r.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(c*r.randint(1,10)));return f'{c}\n{s}\n'
    if n==2754:
        q=[r.randint(1,92) for _ in range(r.randint(1,8))];return str(len(q))+'\n'+'\n'.join(map(str,q))+'\n'
    if n==2783:
        N=r.randint(2,30);return f'{N}\n'+'\n'.join(f'{r.randint(1,10000)} {r.randint(1,10000)}' for _ in range(N))+'\n0\n'
    if n==1094:
        N=r.randint(3,10);rels=[]
        for _ in range(r.randint(1,20)):
            a,b=r.sample(range(N),2);rels.append(f'{chr(65+a)}<{chr(65+b)}')
        return f'{N} {len(rels)}\n'+'\n'.join(rels)+'\n0 0\n'
    if n==1376:
        a,b=r.randint(5,12),r.randint(5,12);g=[[0]*b for _ in range(a)];sx,sy=1,1;tx,ty=a-2,b-2
        return f'{a} {b}\n'+'\n'.join(' '.join(map(str,x)) for x in g)+f'\n{sx} {sy} {tx} {ty} east\n0 0\n'
    if n==1833:
        out=[str(r.randint(1,4))]
        for _ in range(int(out[0])):
            N=r.randint(2,30);p=list(range(1,N+1));r.shuffle(p);out += [f'{N} {r.randint(1,min(20,N))}',' '.join(map(str,p))]
        return '\n'.join(out)+'\n'
    if n==1961:
        out=[]
        for _ in range(r.randint(1,4)):
            s=''.join(r.choice('abc') for _ in range(r.randint(2,100)));out += [str(len(s)),s]
        return '\n'.join(out)+'\n0\n'
    if n==2255:
        def traversals(vals):
            if not vals:return '',''
            k=r.randrange(len(vals));a,b=traversals(vals[:k]);c,d=traversals(vals[k+1:]);return vals[k]+a+c,a+vals[k]+d
        rows=[]
        for _ in range(r.randint(1,4)):
            s=''.join(r.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ',r.randint(1,12)));rows.append(' '.join(traversals(s)))
        return '\n'.join(rows)+'\n'
    if n==2811:return '\n'.join(' '.join(str(r.randint(0,1)) for _ in range(6)) for _ in range(5))+'\n'
    if n==3248:return '\n'.join(f'{r.randint(1,2**31-1)} {r.randint(1,2**31-1)}' for _ in range(r.randint(1,8)))+'\n'
    if n==2692:
        coins=list('ABCDEFGHIJKL');coin=r.choice(coins);heavy=r.choice([True,False]);normal=[x for x in coins if x!=coin];r.shuffle(normal);x=normal[0]
        state='down' if heavy else 'up'
        a,b,c,d=map(''.join,(normal[:4],normal[4:8],normal[3:7],normal[7:11]))
        return f'1\n{coin} {x} {state}\n{a} {b} even\n{c} {d} even\n'
    if n==3143:return f'{r.randint(4,2000)}\n'
    if n==1860:
        N=r.randint(2,8);edges=[]
        for _ in range(r.randint(N-1,20)):
            a,b=r.sample(range(1,N+1),2);edges.append(f'{a} {b} {r.uniform(.5,1.6):.2f} {r.uniform(0,2):.2f} {r.uniform(.5,1.6):.2f} {r.uniform(0,2):.2f}')
        return f'{N} {len(edges)} 1 {r.uniform(10,100):.2f}\n'+'\n'.join(edges)+'\n'
    if n==1035:
        words=['cat','dog','apple','word'+chr(97+seed%26)];queries=[words[-1],words[-1][:-1]+'z','dogs'];return '\n'.join(words+['#']+queries+['#'])+'\n'
    if n==2431:
        N=r.randint(1,20);L=r.randint(20,500);stops=sorted({r.randint(1,L-1):r.randint(1,100) for _ in range(N)}.items(),reverse=True);return str(len(stops))+'\n'+'\n'.join(f'{d} {f}' for d,f in stops)+f'\n{L} {r.randint(1,100)}\n'
    if n==2756:return f'{r.randint(1,1000)} {r.randint(1,1000)}\n'
    if n==2757:
        N=r.randint(1,80);return f'{N}\n'+' '.join(str(r.randint(0,10000)) for _ in range(N))+'\n'
    if n==1159:
        N=r.randint(3,100);s=''.join(r.choice('abcXYZ09') for _ in range(N));return f'{N}\n{s}\n'
    if n==1724:
        N=r.randint(2,12);K=r.randint(0,50);edges=[]
        for i in range(1,N):edges.append((i,i+1,r.randint(1,30),r.randint(0,10)))
        for _ in range(r.randint(0,20)):
            a,b=r.sample(range(1,N+1),2);edges.append((a,b,r.randint(1,50),r.randint(0,15)))
        return f'{K}\n{N}\n{len(edges)}\n'+'\n'.join(' '.join(map(str,e)) for e in edges)+'\n'
    if n==2706:return f"{1000+seed}\n"
    if n==2996:
        N=r.randint(2,80);p=list(range(1,N+1));r.shuffle(p);return f'{N}\n{r.randint(1,min(30,N))}\n'+' '.join(map(str,p))+'\n'
    if n==3254:return '\n'.join(f'{r.randint(2,100)} {r.randint(1,100)} {r.randint(1,100)}' for _ in range(r.randint(1,5)))+'\n0 0 0\n'
    if n==2502:
        hx,hy,sx,sy=[r.randint(0,10000) for _ in range(4)];return f'{hx} {hy} {sx} {sy}\n{r.randint(0,10000)} {r.randint(0,10000)} {r.randint(0,10000)} {r.randint(0,10000)} -1 -1\n'
    if n==2748:return ''.join(r.sample('abcdefghi',r.randint(1,5)))+'\n'
    if n==1191:return f'{r.randint(2,10)}\n'+'\n'.join(' '.join(str(r.randint(0,99)) for _ in range(8)) for _ in range(8))+'\n'
    if n==2287:
        N=r.randint(1,30);return f'{N}\n'+' '.join(str(r.randint(1,100)) for _ in range(N))+'\n'+' '.join(str(r.randint(1,100)) for _ in range(N))+'\n0\n'
    if n==2981:return str(r.randrange(10**50))+'\n'+str(r.randrange(10**50))+'\n'
    if n==2750:return f'{r.randint(1,32767)}\n'
    if n==2788:
        rows=[]
        for _ in range(r.randint(1,6)):
            m=r.randint(1,100000);rows.append(f'{m} {r.randint(m,1000000000)}')
        return '\n'.join(rows)+'\n0 0\n'
    if n==2802:
        w,h=r.randint(2,8),r.randint(2,8);board=[' '*w for _ in range(h)];y2=1 if seed%2==0 else h
        return f'{w} {h}\n'+'\n'.join(board)+f'\n1 1 {w} {y2}\n0 0 0 0\n0 0\n'
    if n==1003:return '\n'.join(f'{r.uniform(.01,5.20):.2f}' for _ in range(r.randint(1,6)))+'\n0.00\n'
    if n==1011:
        a=[r.randint(1,30) for _ in range(r.randint(3,20))];return f'{len(a)}\n'+' '.join(map(str,a))+'\n0\n'
    if n==1017:return ' '.join(str(r.randint(0,20)) for _ in range(6))+'\n0 0 0 0 0 0\n'
    if n==1065:
        out=[str(r.randint(1,3))]
        for _ in range(int(out[0])):
            N=r.randint(1,30);out += [str(N),' '.join(f'{r.randint(1,30)} {r.randint(1,30)}' for _ in range(N))]
        return '\n'.join(out)+'\n'
    if n==1218:
        q=[r.randint(5,100) for _ in range(r.randint(1,10))];return str(len(q))+'\n'+'\n'.join(map(str,q))+'\n'
    raise KeyError(n)


LABELS = {
 n:f"{n:05d}: generated input follows the current statement's numeric bounds, dimensions, and terminator"
 for n in set(SOURCE_SPEC)|set(CUSTOM)
}
LABELS.update({
2694:'prefix expression has binary operators and numeric operands',2945:'missile count matches 3..25 positive heights',
2746:'Josephus cases use positive n/m <= 300 and end in 0 0',2773:'herb count matches rows and time/value bounds',
2734:'decimal integer satisfies 0 < a < 65536',2488:'journey boards have 1 <= p,q <= 26',
2810:'perfect-cube search bound satisfies 1 <= N <= 100',2299:'sort cases match n and end in zero',
2775:'file tree closes directories and ends each data set with * then #',2815:'castle dimensions match a symmetric wall grid',
2524:'religion pairs use student ids in 1..n and data ends in 0 0',1088:'ski grid has exactly R rows and C bounded heights',
1182:'food-chain statements have D in {1,2} and declared K rows',1760:'disk-tree count matches non-space paths',
2386:'lake grid has N rows of exactly M W/dot cells',2456:'stall count matches N distinct positive positions and 2 <= C <= N',
2808:'tree-removal intervals lie inside 0..L',2995:'mountain count matches N heights with N >= 2',
2760:'number triangle has row i containing exactly i values in 0..100',3151:'pot capacities and target are in 1..100 with C <= max(A,B)',
2733:'year satisfies 0 < a < 3000',2774:'log rows match N and lengths are in 1..10000',
2806:'each LCS row contains two strings no longer than 200',1426:'each multiple query is in 1..200 and input ends in zero',
1852:'ant cases match n positions strictly inside a positive pole',2039:'cipher length is at most 200 and divisible by 2..20 columns',
2754:'queen query count matches ranks in 1..92',2783:'hotel cases match N positive distance/cost pairs and end in zero',
1094:'sorting relations use the first N uppercase objects and end in 0 0',1376:'robot grid dimensions and command coordinates are interior and end in 0 0',
1833:'permutation cases match n distinct values 1..n and valid k',1961:'period strings match declared lengths and end in zero',
2255:'preorder and inorder rows contain the same distinct uppercase nodes',2811:'lights-out input is exactly a 5 by 6 binary grid',
3248:'each GCD row contains two positive int-range values',2692:'each counterfeit case has three equal-pan weighings over coins A..L',
3143:'Goldbach input is a single positive integer no greater than 2000',1860:'exchange count matches M valid bidirectional currency rows',
1035:'lowercase dictionary and query sections each end in #',2431:'expedition stop count matches distances before the town and positive fuel',
2756:'binary-tree node labels x and y are positive and at most 1000',2757:'LIS count matches N values in 0..10000',
1159:'palindrome string length equals N in 3..5000',1724:'road count matches R with cities in 1..N and toll budget K',
2706:'Mersenne exponent satisfies 1000 < P < 3100000',2996:'course permutation contains each value 1..N exactly once',
3254:'Josephus cases use positive n,p,m below 300 and end in 0 0 0',2502:'subway coordinates are nonnegative and every line ends in -1 -1',
2748:'permutation input has 1..6 distinct lowercase letters',1191:'board split input has n in 2..14 and exactly 64 scores below 100',
2287:'horse-racing cases contain two N-speed lists and end in zero',2981:'big-addition input has two nonnegative integers of at most 200 digits',
2750:'animal leg count is a single positive integer below 32768',2788:'tree-range rows satisfy 1 <= m <= n <= 1e9 and end in 0 0',
2802:'game boards preserve w characters per row and query/board terminators',1003:'hangover queries are 0.01..5.20 and end in 0.00',
1011:'stick-part count matches positive lengths and input ends in zero',1017:'packing orders contain six nonnegative counts and end in six zeros',
1065:'wooden-stick cases match n positive length/weight pairs',1218:'jailer case count matches cell counts in 5..100',
})


def valid(n, text):
    """Mechanical current-statement check; malformed counterexamples are false."""
    try:
        lines=text.strip().splitlines();tok=text.split()
        if not lines:return False
        if n==2694:
            need=1
            for value in tok:
                if need<1:return False
                need-=1
                if value in '+-*/':need+=2
                else:float(value)
            return need==0
        if n==2945:
            k=int(lines[0]);values=list(map(int,lines[1].split()));return len(lines)==2 and 1<=k<=25 and len(values)==k and all(x>0 for x in values)
        if n==2746:
            return lines[-1]=='0 0' and all(len(x.split())==2 and all(0<int(v)<=300 for v in x.split()) for x in lines[:-1])
        if n==2773:
            T,m=map(int,lines[0].split());return 1<=T<=1000 and 1<=m<=100 and len(lines)==m+1 and all(len(x.split())==2 and all(1<=int(v)<=100 for v in x.split()) for x in lines[1:])
        if n in (2733,2734,2810,3143,2706):return len(tok)==1 and int(tok[0])>0
        if n==2488:
            return int(lines[0])==len(lines)-1 and all(len(x.split())==2 and all(1<=int(v)<=26 for v in x.split()) for x in lines[1:])
        if n==2299:
            p=0
            while int(tok[p]):
                count=int(tok[p]);p+=1
                if count<1 or p+count>len(tok):return False
                values=list(map(int,tok[p:p+count]));p+=count
                if any(not 0<=x<=999999999 for x in values):return False
            return p==len(tok)-1
        if n==2811:return len(tok)==30 and set(tok)<={'0','1'}
        if n==2815:
            a,b=map(int,lines[:2]);g=[list(map(int,x.split())) for x in lines[2:]]
            if not (1<a<=50 and 1<b<=50 and len(g)==a and all(len(x)==b and all(0<=v<=15 for v in x) for x in g)):return False
            return all((j>0 or v&1) and (i>0 or v&2) and (j<b-1 or v&4) and (i<a-1 or v&8)
                and (j==b-1 or bool(v&4)==bool(g[i][j+1]&1)) and (i==a-1 or bool(v&8)==bool(g[i+1][j]&2))
                for i,row in enumerate(g) for j,v in enumerate(row))
        if n==2775:return lines[-1]=='#' and '*' in lines
        if n==2524:
            p=0
            while lines[p]!='0 0':
                students,m=map(int,lines[p].split());p+=1
                if students<1 or m<0 or p+m>len(lines):return False
                for row in lines[p:p+m]:
                    a,b=map(int,row.split())
                    if not 1<=a<=students or not 1<=b<=students:return False
                p+=m
            return p==len(lines)-1
        if n==1182:
            N,k=map(int,lines[0].split());return 1<=N<=50000 and 1<=k<=100000 and len(lines)==k+1 and all(len(x.split())==3 and int(x.split()[0]) in (1,2) for x in lines[1:])
        if n==1035:return lines.count('#')==2
        if n==1376:
            a,b=map(int,lines[0].split());return 1<a<=50 and 1<b<=50 and len(lines)==a+3 and all(len(x.split())==b and set(x.split())<={'0','1'} for x in lines[1:a+1]) and lines[-1]=='0 0'
        if n==2802:
            w,h=map(int,lines[0].split());return 1<=w<=75 and 1<=h<=75 and len(lines)>=h+4 and all(len(x)==w and set(x)<={'X',' '} for x in lines[1:h+1]) and lines[-2:] == ['0 0 0 0','0 0']
        if n==1003:return lines[-1]=='0.00' and all(.01<=float(x)<=5.20 for x in lines[:-1])
        if n==1011:
            p=0
            while int(tok[p]):
                count=int(tok[p]);p+=1
                if not 1<=count<=64 or p+count>len(tok) or any(int(x)<=0 for x in tok[p:p+count]):return False
                p+=count
            return p==len(tok)-1
        if n==1017:return lines[-1]=='0 0 0 0 0 0' and all(len(x.split())==6 and all(int(v)>=0 for v in x.split()) for x in lines)
        if n==3248:return all(len(x.split())==2 and all(int(v)>0 for v in x.split()) for x in lines)
        if n==2748:return len(lines)==1 and 1<=len(lines[0])<=6 and len(set(lines[0]))==len(lines[0]) and lines[0].islower()
        if n==2981:return len(lines)==2 and all(x.isdigit() and len(x)<=200 for x in lines)
        if n==1159:return int(lines[0])==len(lines[1]) and 3<=int(lines[0])<=5000
        if n==2386:
            a,b=map(int,lines[0].split());return len(lines)==a+1 and all(len(x)==b and set(x)<={'W','.'} for x in lines[1:])
        if n==1088:
            a,b=map(int,lines[0].split());return len(lines)==a+1 and all(len(x.split())==b for x in lines[1:])
        if n==1760:return int(lines[0])==len(lines)-1 and all(' ' not in x for x in lines[1:])
        if n==2039:return len(lines)==2 and 2<=int(lines[0])<=20 and len(lines[1])<=200 and len(lines[1])%int(lines[0])==0
        if n==2806:return all(len(x.split())==2 and all(1<=len(v)<=200 for v in x.split()) for x in lines)
        if n==2456:
            N,C=map(int,lines[0].split());values=list(map(int,lines[1:]));return len(values)==N and 2<=C<=N<=100000 and len(set(values))==N and all(x>0 for x in values)
        if n==2808:
            L,m=map(int,lines[0].split());return 1<=L<=10000 and 1<=m<=100 and len(lines)==m+1 and all(0<=int(x.split()[0])<=int(x.split()[1])<=L for x in lines[1:])
        if n==2995:
            N=int(lines[0]);values=list(map(int,lines[1].split()));return len(lines)==2 and 2<=N<=1000 and len(values)==N
        if n==2760:
            N=int(lines[0]);return 1<N<=100 and len(lines)==N+1 and all(len(lines[i].split())==i and all(0<=int(v)<=100 for v in lines[i].split()) for i in range(1,N+1))
        if n==2774:
            N,K=map(int,lines[0].split());return len(lines)==N+1 and 1<=N<=10000 and 1<=K<=10000 and all(1<=int(x)<=10000 for x in lines[1:])
        if n==1426:return lines[-1]=='0' and all(1<=int(x)<=200 for x in lines[:-1])
        if n==1852:
            p=1
            for _ in range(int(tok[0])):
                L,count=map(int,tok[p:p+2]);p+=2;values=list(map(int,tok[p:p+count]));p+=count
                if len(values)!=count or any(not 0<x<L for x in values):return False
            return p==len(tok)
        if n==2750:return len(tok)==1 and 0<int(tok[0])<32768
        if n==2754:return int(lines[0])==len(lines)-1 and all(1<=int(x)<=92 for x in lines[1:])
        if n==2783:
            p=0
            while int(lines[p]):
                count=int(lines[p]);p+=1
                if not 1<=count<=10000 or p+count>len(lines):return False
                if any(len(x.split())!=2 or any(not 1<=int(v)<=10000 for v in x.split()) for x in lines[p:p+count]):return False
                p+=count
            return p==len(lines)-1
        if n==1094:
            p=0
            while lines[p]!='0 0':
                count,m=map(int,lines[p].split());p+=1
                if not 2<=count<=26 or m<1 or p+m>len(lines):return False
                if any(len(row)!=3 or row[1]!='<' or not ('A'<=row[0]<chr(65+count) and 'A'<=row[2]<chr(65+count)) for row in lines[p:p+m]):return False
                p+=m
            return p==len(lines)-1
        if n==1833:
            p=1
            for _ in range(int(lines[0])):
                N,k=map(int,lines[p].split());values=list(map(int,lines[p+1].split()));p+=2
                if not 1<=N<1024 or not 1<=k<=64 or sorted(values)!=list(range(1,N+1)):return False
            return p==len(lines)
        if n==1961:
            p=0
            while lines[p]!='0':
                count=int(lines[p]);p+=1
                if not 2<=count<=1000000 or len(lines[p])!=count:return False
                p+=1
            return p==len(lines)-1
        if n==3151:return len(tok)==3 and all(1<=int(x)<=100 for x in tok) and int(tok[2])<=max(map(int,tok[:2]))
        if n==1724:
            K,N,R=map(int,lines[:3]);return len(lines)==3+R and 0<=K<=10000 and 2<=N<=100
        if n==1860:
            N,M,S,V=lines[0].split();return len(lines)==1+int(M) and 1<=int(S)<=int(N)<=100
        if n==2692:return int(lines[0])>=1 and len(lines)==1+3*int(lines[0]) and all(len(x.split())==3 and len(x.split()[0])==len(x.split()[1]) and set(x.split()[0]+x.split()[1])<set('ABCDEFGHIJKLM') and x.split()[2] in ('up','down','even') for x in lines[1:])
        if n==2431:
            count=int(lines[0]);town,fuel=map(int,lines[-1].split());return len(lines)==count+2 and town>0 and fuel>0 and all(0<int(x.split()[0])<town and int(x.split()[1])>0 for x in lines[1:-1])
        if n==2756:return len(tok)==2 and all(1<=int(x)<=1000 for x in tok)
        if n==2757:
            N=int(lines[0]);values=list(map(int,lines[1].split()));return len(lines)==2 and 1<=N<=1000 and len(values)==N and all(0<=x<=10000 for x in values)
        if n==2996:
            N=int(lines[0]);m=int(lines[1]);values=list(map(int,lines[2].split()));return len(lines)==3 and 1<=N<=10000 and 1<=m<=100 and sorted(values)==list(range(1,N+1))
        if n==3254:return lines[-1]=='0 0 0' and all(len(x.split())==3 and all(0<int(v)<300 for v in x.split()) for x in lines[:-1])
        if n==2502:return len(lines)>=2 and lines[-1].endswith('-1 -1') and all(int(x)>=0 or int(x)==-1 for x in tok)
        if n==2255:return all(len(x.split())==2 and set(x.split()[0])==set(x.split()[1]) for x in lines)
        if n==1191:return len(tok)==65 and 1<int(tok[0])<15 and all(0<=int(x)<100 for x in tok[1:])
        if n==2287:
            p=0
            while int(tok[p]):
                count=int(tok[p]);p+=1
                if count<1 or p+2*count>len(tok):return False
                p+=2*count
            return p==len(tok)-1
        if n==2788:return lines[-1]=='0 0' and all(len(x.split())==2 and 1<=int(x.split()[0])<=int(x.split()[1])<=1000000000 for x in lines[:-1])
        if n==1065:
            p=1
            for _ in range(int(tok[0])):
                count=int(tok[p]);p+=1
                if not 1<=count<=5000 or p+2*count>len(tok):return False
                if any(int(x)<=0 for x in tok[p:p+2*count]):return False
                p+=2*count
            return p==len(tok)
        if n==1218:return int(lines[0])==len(lines)-1 and all(5<=int(x)<=100 for x in lines[1:])
        return False
    except (ValueError,IndexError,TypeError):return False


def run_source(source, input_text, timeout=120):
    with tempfile.TemporaryDirectory(prefix='t028-') as folder:
        p=Path(folder)/'main.py';p.write_text(source)
        q=subprocess.run([sys.executable,'-I',str(p)],input=input_text,text=True,capture_output=True,timeout=timeout)
    if q.returncode:raise RuntimeError((q.stderr or q.stdout)[-500:])
    return q.stdout


def source_sections(numbers):
    found={}
    for si,path in enumerate(SOURCES):
        for n,title,body,codes,_samples in sections(path):
            if n in numbers and n in SOURCE_SPEC and SOURCE_SPEC[n][0]==si and len(codes)>SOURCE_SPEC[n][1]:
                found[n]=(title,body,codes[SOURCE_SPEC[n][1]],path,SOURCE_SPEC[n][1],si)
            elif n in numbers and n in CUSTOM and n not in found:
                found[n]=(title,body,CUSTOM[n],path,None,si)
    missing=numbers-set(found)
    if missing:raise SystemExit(f'missing sections: {sorted(missing)}')
    return found


def clean(text):return '\n'.join(x.rstrip() for x in text.rstrip().splitlines())+'\n'


def archive_output(n, source, text):
    """Run current single-case sources against known older batch wrappers."""
    tokens=text.replace('\x1a',' ').split()
    if n==2039:
        out=[];p=0
        while int(tokens[p]):
            out.append(run_source(source,f'{tokens[p]}\n{tokens[p+1]}\n'));p+=2
        return ''.join(out)
    if n==2750:
        return ''.join(run_source(source,f'{value}\n') for value in tokens[1:1+int(tokens[0])])
    if n==2811:
        count=int(tokens[0]);values=tokens[1:];out=[]
        for i in range(count):
            block=values[i*30:(i+1)*30]
            case='\n'.join(' '.join(block[j:j+6]) for j in range(0,30,6))+'\n'
            out.append(run_source(source,case))
        return ''.join(out)
    return run_source(source,text)


def archive_semantics(n, input_text, got, expected):
    if n==1426:
        queries=[int(x) for x in input_text.replace('\x1a',' ').split() if int(x)]
        rows=got.split()
        return len(rows)==len(queries) and all(set(value)<={'0','1'} and value[0]=='1'
            and len(value)<=100 and int(value)%query==0 for query,value in zip(queries,rows))
    if n==3151:
        # Different shortest operation sequences are valid; the archive fixes
        # the independently known minimum length (or impossible).
        return got.split()[:1]==expected.replace('\x1a',' ').split()[:1]
    return None


def archive_check(source, entry):
    paths=sorted((OPENJUDGE/entry['oracle_dir']).glob('*.in'))
    mismatched=[];semantic=[]
    for p in paths:
        text=p.read_text(errors='replace');expected=p.with_suffix('.out').read_text(errors='replace')
        try: got=archive_output(int(entry['number']),source,text)
        except Exception: mismatched.append(p.name);continue
        got_tokens=got.replace('\x1a',' ').split();expected_tokens=expected.replace('\x1a',' ').split()
        if int(entry['number'])==2811:
            expected_tokens=[x for x in expected_tokens if x in ('0','1')]
        if got_tokens!=expected_tokens:
            if archive_semantics(int(entry['number']),text,got,expected):semantic.append(p.name)
            else:mismatched.append(p.name)
    status='passed' if paths and not mismatched else 'FAILED'
    return {'status':status,'cases':len(paths),'mismatched':mismatched,'semantic_cases':semantic,
            'method':'exact tokens after adapting old batch wrappers; semantic validation for non-unique outputs',
            'note':None if status=='passed' else 'archive cross-check did not validate'}


def write_producecase(made, number, source, sample):
    program=("import random,subprocess,sys,tempfile\nfrom pathlib import Path\n"+inspect.getsource(generate)+
f"\nREFERENCE={source!r}\nNUMBER={number}\nSAMPLE={sample!r}\n"
"def run(x):\n with tempfile.TemporaryDirectory() as d:\n  p=Path(d)/'m.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)\n  if q.returncode:raise SystemExit(q.stderr)\n  return q.stdout\n"
"def main():\n d=Path('data');d.mkdir(exist_ok=True)\n for p in d.glob('*'):p.unlink()\n for i,x in enumerate([SAMPLE]+[generate(NUMBER,s) for s in range(1,21)]):\n  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))\n"
"if __name__=='__main__':main()\n")
    (made/'producecase.py').write_text(program)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('round',type=int,choices=(2,3,4));opt=ap.parse_args()
    all_entries=json.loads(CANDIDATES.read_text())['entries'];chosen=all_entries[(opt.round-2)*20:(opt.round-1)*20]
    if [x['priority'] for x in chosen] != list(range((opt.round-2)*20+1,(opt.round-1)*20+1)):raise SystemExit('priority slice changed')
    numbers={int(x['number']) for x in chosen};selected=source_sections(numbers)
    platform_path=ROOT/'collab'/f't028-round{opt.round}-platform.json';platform_rows={}
    if platform_path.exists():platform_rows={int(x['local_number']):x for x in json.loads(platform_path.read_text()).get('results',[])}
    manifest=[];report=[]
    for entry in chosen:
        n=int(entry['number']);title,body,raw,path,ci,si=selected[n]
        try:sample=clean(first_sample(body,'样例输入'))
        except ValueError:
            sample={2734:'10\n',1724:'5\n6\n7\n1 2 2 3\n2 4 3 3\n3 4 2 4\n1 3 4 1\n4 6 2 1\n3 5 2 0\n5 4 3 2\n'}[n]
        try:sample_out=clean(first_sample(body,'样例输出'))
        except ValueError:sample_out={2734:'12\n'}.get(n)
        if n==3143:
            sample='10\n';sample_out='10=3+7\n10=5+5\n'
        if n==1724:
            sample_out='11\n'
        if n==1426:
            sample_out=None
        if n==2802:
            sample=('5 4\nXXXXX\nX   X\nXXX X\n XXX \n2 3 5 3\n1 3 4 4\n'
                    '2 3 3 4\n0 0 0 0\n0 0\n')
        attribution=(f'# Source collection: {path}\n# Heading: {n}: {title}\n# Fenced code block index: {ci}\n'
                     f'# Source URL: {SOURCE_URLS[si]}\n# Upstream problem: http://cs101.openjudge.cn/{entry["books"][0]}/{entry["ids"][0]}/\n'
                     '# License: not declared in source collection; no license is inferred.\nimport sys\n')
        source=attribution+clean(raw);cross=archive_check(source,entry)
        if cross['status']=='FAILED':raise SystemExit(f'{n} archive cross-check failed')
        cases=[sample]+[generate(n,s) for s in range(1,21)];outputs=[run_source(source,x) for x in cases]
        made_rel=str(Path(entry['oracle_dir']).parent/f'{n:05d}_made');made=OPENJUDGE/made_rel;data=made/'data';data.mkdir(parents=True,exist_ok=True)
        for old in data.glob('*'):old.unlink()
        for i,(x,y) in enumerate(zip(cases,outputs)):(data/f'{i}.in').write_text(x);(data/f'{i}.out').write_text(y)
        (made/'samplecode.py').write_text(source);write_producecase(made,n,source,sample)
        invalid=f'invalid-{n}\n';rows=[(LABELS[n],all(valid(n,x) for x in cases[1:]))]
        audit=common.audit(made,cases=cases[1:],outputs=outputs[1:],sample_input=sample,sample_output=sample_out,
            sample_output_exemption=('problem permits multiple correct outputs' if n in (1426,3151) else None),
            constraints=rows,constraint_counterexample=(invalid.strip(),[(LABELS[n],valid(n,invalid))]))
        prow=platform_rows.get(n);platform_failed=prow is not None and prow.get('verdict')!='Accepted'
        status='passed' if not audit['failed'] and not platform_failed else 'FAILED'
        manifest.append({**entry,'local_number':n,'title':title,'made_dir':made_rel,'sample_input':sample,
                         'solution_collection':str(path),'solution_code_index':ci,'pending_rework':[]})
        smoke_bad=[s for s in range(20000) if not valid(n,generate(n,s))]
        if smoke_bad: status='FAILED'
        report.append({'local_number':n,'title':title,'priority':entry['priority'],'tier':entry['tier'],'status':status,
            'reference_source':'solution collection or format-robust equivalent, checked against archive where exact output is defined',
            'solution_collection':str(path),'solution_code_index':ci,'source_url':SOURCE_URLS[si],
            'license_status':'not declared in source collection; no license is inferred','submission_id':prow.get('solution_id') if prow else None,
            'platform_verdict':prow.get('verdict') if prow else 'not_run','archive_cross_check':cross,
            'generator':'generate','generator_seed_smoke':{'seeds':20000,'status':'passed' if not smoke_bad else 'FAILED','failed_seeds':smoke_bad[:8]},'test_cases':len(cases),
            'max_input_bytes':max(len(x.encode()) for x in cases),'max_output_bytes':max(len(x.encode()) for x in outputs),
            'constraints':rows,'constraint_counterexample':invalid.strip(),'self_audit':audit})
        print(n,'built',flush=True)
    mp=ROOT/'collab'/f't028-round{opt.round}-manifest.json';rp=ROOT/'collab'/f't028-round{opt.round}-report.json'
    mp.write_text(json.dumps({'task':'T-028','round':opt.round,'count':20,'priority_range':[chosen[0]['priority'],chosen[-1]['priority']],
      'entries':manifest},ensure_ascii=False,indent=2)+'\n')
    failed=[x['local_number'] for x in report if x['status']!='passed']
    rp.write_text(json.dumps({'task':'T-028','round':opt.round,'updated_at':datetime.now(timezone.utc).isoformat(),'count':20,
      'pending_rework_status':common.pending_rework_status([],OPENJUDGE/'tests'),'entries':report,'failed':failed},ensure_ascii=False,indent=2)+'\n')
    if failed:raise SystemExit(f'self-audit failed: {failed}')


if __name__=='__main__':main()
