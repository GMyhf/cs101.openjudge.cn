"""独立复核树、图、状态空间与若干数论题。"""
from gmyhf_oracles_basic import oracle,integers,lines,matrix
from gmyhf_oracles_structures import Fenwick
from collections import defaultdict,deque,Counter
from functools import lru_cache
from fractions import Fraction
from itertools import product
from math import gcd,isqrt
from bisect import bisect_right
import heapq,random

@oracle(27638)
def height_leaves(text):
    rows=[integers(r)for r in text.splitlines()];n=rows[0][0];children=rows[1:];roots=set(range(n))-{v for r in children for v in r if v>=0};assert len(roots)==1
    queue=[(roots.pop(),0)];height=leaves=0;seen=set()
    while queue:
        v,d=queue.pop();assert v not in seen;seen.add(v);height=max(height,d)
        if children[v]==[-1,-1]:leaves+=1
        queue.extend((u,d+1)for u in children[v]if u>=0)
    assert len(seen)==n
    return f'{height} {leaves}'

@oracle(27653)
def fraction_sum(text):
    a,b,c,d=integers(text);v=Fraction(a,b)+Fraction(c,d);return f'{v.numerator}/{v.denominator}'

@oracle(27862)
def game_tree(text):
    words=iter(integers(text));out=[]
    while True:
        try:n=next(words)
        except StopIteration:break
        g=defaultdict(list)
        for _ in range(n-1):a,b=next(words),next(words);g[a].append(b);g[b].append(a)
        leaves={}
        for _ in range(next(words)):v,a,b=next(words),next(words),next(words);leaves[v]=(a,b)
        parent={1:0};depth={1:0};order=[1]
        for v in order:
            for u in g[v]:
                if u!=parent[v]:parent[u]=v;depth[u]=depth[v]+1;order.append(u)
        result=dict(leaves)
        for v in reversed(order):
            if v in result:continue
            choices=[result[u]for u in g[v]if u!=parent[v]];index=depth[v]%2;assert len(choices)==2 and choices[0][index]!=choices[1][index]
            result[v]=max(choices,key=lambda p:p[index])
        out.append(f'{result[1][0]} {result[1][1]}')
    return lines(out)

@oracle(27925)
def teams(text):
    rows=text.splitlines();n=int(rows[0]);membership={v:i for i,row in enumerate(rows[1:n+1])for v in integers(row)};groups=deque();contents={};out=[]
    for row in rows[n+1:]:
        command,*words=row.split()
        if command=='STOP':break
        if command=='ENQUEUE':
            v=int(words[0]);group=membership.get(v,('散客',v))
            if group not in contents:contents[group]=deque();groups.append(group)
            contents[group].append(v)
        else:
            group=groups[0];out.append(contents[group].popleft())
            if not contents[group]:groups.popleft();del contents[group]
    return lines(out)

@oracle(27928)
def ordered_tree(text):
    rows=[integers(r)for r in text.splitlines()[1:]];g={r[0]:r[1:]for r in rows};root=(set(g)-{v for r in rows for v in r[1:]}).pop();out=[];stack=[(False,root)]
    while stack:
        emit,v=stack.pop()
        if emit:out.append(v);continue
        stack.extend((u==v,u)for u in sorted(g.get(v,[])+[v],reverse=True))
    return lines(out)

@oracle(27947)
def dynamic_medians(text):
    out=[]
    for row in text.splitlines()[1:]:
        a=integers(row);values=sorted(set(a));ids={v:i for i,v in enumerate(values)};tree=Fenwick(len(values));medians=[]
        for i,v in enumerate(a,1):
            tree.add(ids[v],1)
            if i%2:medians.append(values[tree.kth((i+1)//2)])
        out.extend((str(len(medians)),' '.join(map(str,medians))))
    return lines(out)

@oracle(27948)
def fbi(text):
    s=text.split()[1];prefix=[0]
    for c in s:prefix.append(prefix[-1]+int(c))
    out=[];stack=[(0,len(s),False)]
    while stack:
        a,b,emit=stack.pop()
        if emit:
            count=prefix[b]-prefix[a];out.append('B'if count==0 else 'I'if count==b-a else 'F')
        else:
            stack.append((a,b,True))
            if b-a>1:mid=(a+b)//2;stack.extend(((mid,b,False),(a,mid,False)))
    return ''.join(out)

@oracle(27951)
def translation(text):
    values=integers(text);capacity,n=values[:2];cache=deque();answer=0
    for v in values[2:]:
        if v not in cache:
            answer+=1
            if len(cache)==capacity:cache.popleft()
            cache.append(v)
    return str(answer)

@oracle(28012)
def restricted(text):
    rows=[integers(r)for r in text.splitlines()];n=rows[0][0];g=[[]for _ in range(n)]
    for a,b in rows[1:n]:g[a].append(b);g[b].append(a)
    banned=set(rows[n])if len(rows)>n else set();seen={0};stack=[0]
    while stack:
        for u in g[stack.pop()]:
            if u not in seen and u not in banned:seen.add(u);stack.append(u)
    return str(len(seen))

@oracle(28050)
def knight_tour(text):
    n,sr,sc=integers(text)
    if n in(3,4)or n%2 and(sr+sc)%2:return 'fail'
    g={i*n+j:[x*n+y for di,dj in((1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1))for x,y in[(i+di,j+dj)]if 0<=x<n and 0<=y<n]for i in range(n)for j in range(n)}
    rng=random.Random(28050)
    for _ in range(100):
        path=[sr*n+sc];seen=set(path)
        while len(path)<n*n:
            options=[v for v in g[path[-1]]if v not in seen]
            if not options:break
            rng.shuffle(options);v=min(options,key=lambda v:sum(u not in seen for u in g[v]));path.append(v);seen.add(v)
        if len(path)==n*n:
            assert len(set(path))==n*n and all(b in g[a]for a,b in zip(path,path[1:]));return 'success'
    raise ValueError('未找到周游证书，不能据此判fail')

@oracle(28052)
def hex_chess(text):
    rows=[integers(r)for r in text.splitlines()];n=rows[0][0];g=rows[1:];counts=Counter(v for r in g for v in r);own=1 if counts[1]==counts[2]else 2;enemy=3-own;dist={};q=deque()
    for k in range(n):
        i,j=(0,k)if own==1 else(k,0)
        if g[i][j]!=enemy:dist[i,j]=int(g[i][j]==0);q.append((i,j))
    while q:
        i,j=q.popleft()
        for di,dj in((-1,0),(-1,-1),(0,-1),(0,1),(1,1),(1,0)):
            x,y=i+di,j+dj
            if 0<=x<n and 0<=y<n and g[x][y]!=enemy:
                weight=int(g[x][y]==0);cost=dist[i,j]+weight
                if cost<dist.get((x,y),10**12):
                    dist[x,y]=cost
                    if weight:q.append((x,y))
                    else:q.appendleft((x,y))
    answer=min(dist.get((n-1,k)if own==1 else(k,n-1),10**12)for k in range(n))
    return str(answer)if answer<10**12 else '-1'

@oracle(28186)
def last_child(text):
    values=integers(text);n,m=values[:2];a=values[2:]
    return str(max(range(n),key=lambda i:((a[i]+m-1)//m,i))+1)

@oracle(28193)
def rumors(text):
    rows=[integers(r)for r in text.splitlines()];n,m=rows[0];prices=rows[1];g=[[]for _ in range(n)]
    for a,b in rows[2:]:g[a-1].append(b-1);g[b-1].append(a-1)
    seen=set();answer=0
    for root in range(n):
        if root in seen:continue
        seen.add(root);stack=[root];least=prices[root]
        while stack:
            v=stack.pop();least=min(least,prices[v])
            for u in g[v]:
                if u not in seen:seen.add(u);stack.append(u)
        answer+=least
    return str(answer)

@oracle(28334)
def dag_extension(text):
    rows=[integers(r)for r in text.splitlines()];n,m=rows[0];edges=set(map(tuple,rows[1:]));reach=[0]*n
    for a,b in edges:reach[a]|=1<<b
    for k in range(n):
        for i in range(n):
            if reach[i]>>k&1:reach[i]|=reach[k]
    assert all(not(reach[i]>>i&1)for i in range(n))
    return str(n*(n-1)//2-len(edges))

@oracle(28664)
def id_card(text):
    weights=(7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2);mapping='10X98765432'
    return lines('YES'if mapping[sum(int(c)*w for c,w in zip(s,weights))%11]==s[-1]else 'NO'for s in text.split()[1:])

@oracle(28674)
def caesar(text):
    k,source=text.split();k=int(k)
    return ''.join(chr((ord(c)-(65 if c.isupper()else 97)-k)%26+(65 if c.isupper()else 97))for c in source)

@oracle(28700)
def roman(text):
    s=text.strip();values={'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
    if not s.isdigit():return str(sum(-values[c]if i+1<len(s)and values[c]<values[s[i+1]]else values[c]for i,c in enumerate(s)))
    n=int(s);out=''
    for number,symbol in((1000,'M'),(900,'CM'),(500,'D'),(400,'CD'),(100,'C'),(90,'XC'),(50,'L'),(40,'XL'),(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')):
        count,n=divmod(n,number);out+=symbol*count
    return out

@oracle(28702)
def meal_design(text):
    out=[]
    for m,k,n in[integers(r)for r in text.splitlines()[1:]]:
        if k==1:out.append(int(m==n));continue
        @lru_cache(None)
        def search(denominations):
            reachable={0}
            for _ in range(k):reachable|={v+d for v in reachable for d in denominations if v+d<=n+1}
            missing=next((v for v in range(1,n+2)if v not in reachable),n+2)
            if len(denominations)==m:return int(missing==n+1)
            if missing>n+1:return 0
            return sum(search(denominations+(d,))for d in range(denominations[-1]+1,missing+1))
        out.append(search((1,)))
    return lines(out)

@oracle(28749)
def recruitment(text):
    rows=text.splitlines();n,m=integers(rows[0]);colors=rows[1];students=[[]for _ in range(n)];g=[[]for _ in range(m)];forced=[[]for _ in range(m)]
    for i,row in enumerate(rows[2:]):
        for v in integers(row)[1:]:students[v-1].append(i)
    target={'R':0,'P':2,'W':1}
    for color,volunteers in zip(colors,students):
        value=target[color]
        if not volunteers:
            if value:return 'impossible'
        elif len(volunteers)==1:forced[volunteers[0]].append(value)
        else:a,b=volunteers;g[a].append((b,value));g[b].append((a,value))
    visited=set();total=0
    for root in range(m):
        if root in visited:continue
        component=[];stack=[root];visited.add(root)
        while stack:
            v=stack.pop();component.append(v)
            for u,w in g[v]:
                if u not in visited:visited.add(u);stack.append(u)
        best=None
        for initial in range(3):
            labels={root:initial};q=[root];valid=True
            while q and valid:
                v=q.pop()
                if any(labels[v]!=t for t in forced[v]):valid=False;break
                for u,w in g[v]:
                    wanted=(w-labels[v])%3
                    if u in labels:
                        if labels[u]!=wanted:valid=False;break
                    else:labels[u]=wanted;q.append(u)
            if valid:cost=sum(labels.values());best=cost if best is None else min(best,cost)
        if best is None:return 'impossible'
        total+=best
    return str(total)

@oracle(28914)
def thermostat(text):
    values=integers(text);out=[]
    for i in range(1,len(values),5):
        lo,hi,step,start,end=values[i:i+5];points={lo,hi,start,end};distance={start:0};q=deque([start])
        while q:
            v=q.popleft()
            for u in points:
                if u not in distance and abs(u-v)>=step:distance[u]=distance[v]+1;q.append(u)
        out.append(distance.get(end,-1))
    return lines(out)

@oracle(29256)
def team_partition(text):
    values=integers(text);n,m=values[:2];a=values[2:];low=max(a)-1;high=sum(a)
    while high-low>1:
        bound=(low+high)//2;groups=1;current=0
        for v in a:
            if current+v>bound:groups+=1;current=0
            current+=v
        if groups<=m:high=bound
        else:low=bound
    return str(high)

@oracle(29335)
def simplify_path(text):
    out=[]
    for token in text.strip().split('/'):
        if token=='..':
            if out:out.pop()
        elif token and token!='.':out.append(token)
    return '/'+'/'.join(out)

@oracle(29646)
def bacteria(text):
    values=integers(text);out=[]
    for harmful,good in zip(values[1::2],values[2::2]):
        hours=0;seen=set()
        while harmful>0:
            if(harmful,good)in seen:raise ValueError('有害菌无法消灭')
            seen.add((harmful,good));harmful=min(1000000,max(0,harmful-good)*2);good=good*21//20;hours+=1
        out.append(hours)
    return lines(out)

@oracle(29740)
def neural(text):
    rows=[integers(r)for r in text.splitlines()];n,m=rows[0];initial=rows[1:n+1];edges=defaultdict(int);g=[[]for _ in range(n)];indegree=[0]*n
    for a,b,w in rows[n+1:]:edges[a-1,b-1]+=w
    for (a,b),w in edges.items():g[a].append((b,w));indegree[b]+=1
    value=[v if indegree[i]==0 else -bias for i,(v,bias)in enumerate(initial)];q=deque(i for i in range(n)if indegree[i]==0);seen=0
    while q:
        a=q.popleft();seen+=1
        for b,w in g[a]:
            value[b]+=max(0,value[a])*w;indegree[b]-=1
            if indegree[b]==0:q.append(b)
    if seen!=n:return 'NULL'
    return lines(f'{i+1} {value[i]}'for i in range(n)if not g[i]and value[i]>0)or 'NULL'

@oracle(29886)
def bosses(text):
    a=integers(text);n=len(a);dp=[10**30]*(1<<n);dp[0]=0
    for mask in range(1,1<<n):
        gain=bin(mask).count('1');bits=mask
        while bits:
            bit=bits&-bits;index=bit.bit_length()-1;dp[mask]=min(dp[mask],dp[mask^bit]+(a[index]+gain-1)//gain);bits-=bit
    return str(dp[-1])

@oracle(29896)
def shopping_coins(text):
    values=integers(text);target,n=values[:2];denominations=sorted(values[2:]);covered=coins=0
    if denominations[0]!=1:return '-1'
    while covered<target:
        v=denominations[bisect_right(denominations,covered+1)-1];covered+=v;coins+=1
    return str(coins)

@oracle(29917)
def newton(text):
    out=[]
    for number in map(float,text.split()):
        estimate=1.0;steps=0
        while True:
            following=(estimate+number/estimate)/2;steps+=1
            if abs(estimate-following)<=1e-6:break
            estimate=following
        out.append(f'{steps} {following:.2f}')
    return lines(out)

@oracle(29918)
def amicable(text):
    n=int(text);sums=[0]*(n+1)
    for divisor in range(1,n//2+1):
        for multiple in range(2*divisor,n+1,divisor):sums[multiple]+=divisor
    return lines(f'{a} {sums[a]}'for a in range(1,n+1)if a<sums[a]<=n and sums[sums[a]]==a)

@oracle(29947)
def roadside(text):
    rows=[integers(r)for r in text.splitlines()];length,n=rows[0];intervals=sorted((min(r),max(r)+1)for r in rows[1:]);removed=0;end=-1
    for a,b in intervals:
        if b>end:removed+=b-max(a,end);end=b
    return str(length+1-removed)

@oracle(29949)
def fractional_knapsack(text):
    rows=[integers(r)for r in text.splitlines()];n,capacity=rows[0];answer=Fraction(0)
    for value,weight in sorted(rows[1:],key=lambda r:Fraction(r[0],r[1]),reverse=True):
        take=min(capacity,weight);answer+=Fraction(value*take,weight);capacity-=take
    return f'{float(answer):.2f}'
