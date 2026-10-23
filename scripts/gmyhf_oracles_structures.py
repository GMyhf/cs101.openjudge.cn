"""独立复核数据结构、子集、排列和树题。"""
from gmyhf_oracles_basic import oracle,integers,lines,matrix
from collections import Counter,defaultdict,deque
from functools import lru_cache,cmp_to_key
from itertools import product
from math import comb
from decimal import Decimal
from bisect import bisect_left,bisect_right
from array import array
import heapq,re

@oracle(25538)
def binary_palindrome(text):
    s=bin(int(text))[2:];return 'Yes'if s==s[::-1]else 'No'

@oracle(25561)
def shopping(text):
    rows=text.splitlines();n,m=integers(rows[0]);choices=[[(int(a)-1,int(b))for a,b in re.findall(r'(\d+):(\d+)',row)]for row in rows[1:n+1]]
    coupons=[[(int(a),int(b))for a,b in re.findall(r'(\d+)-(\d+)',row)]for row in rows[n+1:]];best=None
    for selected in product(*choices):
        totals=[0]*m
        for s,p in selected:totals[s]+=p
        total=sum(totals);cost=total-total//300*50-sum(max([0]+[discount for threshold,discount in shop if total_shop>=threshold])for total_shop,shop in zip(totals,coupons))
        best=cost if best is None else min(best,cost)
    return str(best)

@oracle(25566)
def cpu(text):
    jobs=[integers(r)for r in text.splitlines()[1:]];elapsed=answer=0
    for compute,write in sorted(jobs,key=lambda r:-r[1]):elapsed+=compute;answer=max(answer,elapsed+write)
    return str(answer)

@oracle(25572)
def crab(text):
    rows=[integers(r)for r in text.splitlines()];n=rows[0][0];g=rows[1:];body=tuple((i,j)for i in range(n)for j in range(n)if g[i][j]==5)
    assert len(body)==2
    queue=[body];seen={body}
    while queue:
        state=queue.pop()
        if any(g[i][j]==9 for i,j in state):return 'yes'
        for di,dj in((1,0),(-1,0),(0,1),(0,-1)):
            following=tuple((i+di,j+dj)for i,j in state)
            if all(0<=i<n and 0<=j<n and g[i][j]!=1 for i,j in following)and following not in seen:seen.add(following);queue.append(following)
    return 'no'

@oracle(26971)
def candy(text):
    a=integers(text)[1:];dp=[1]*len(a)
    for i in sorted(range(len(a)),key=lambda i:a[i]):
        dp[i]=max([1]+[dp[j]+1 for j in(i-1,i+1)if 0<=j<len(a)and a[j]<a[i]])
    return str(sum(dp))

@oracle(26976)
def wiggle(text):
    a=integers(text)[1:];previous=0;answer=1
    for x,y in zip(a,a[1:]):
        sign=(y>x)-(y<x)
        if sign and sign!=previous:answer+=1;previous=sign
    return str(answer)

@oracle(26977)
def rain(text):
    a=integers(text)[1:];left=[];v=0
    for x in a:v=max(v,x);left.append(v)
    right=0;answer=0
    for x,l in zip(reversed(a),reversed(left)):right=max(right,x);answer+=min(l,right)-x
    return str(answer)

@oracle(26978)
def window_max(text):
    values=integers(text);n,k=values[:2];a=values[2:];heap=[];out=[]
    for i,v in enumerate(a):
        heapq.heappush(heap,(-v,i))
        while heap[0][1]<=i-k:heapq.heappop(heap)
        if i>=k-1:out.append(-heap[0][0])
    return ' '.join(map(str,out))

@oracle(26999)
def occurrences(text):
    out=[]
    for row in text.splitlines()[1:]:
        a,b=row.split();positions=[];start=0
        while True:
            found=a.find(b,start)
            if found<0:break
            positions.append(found);start=found+1
        out.append(' '.join(map(str,positions))or 'no')
    return lines(out)

class Fenwick:
    def __init__(self,n):self.a=[0]*(n+1)
    def add(self,i,value):
        i+=1
        while i<len(self.a):self.a[i]+=value;i+=i&-i
    def prefix(self,i):
        value=0
        while i:value+=self.a[i];i-=i&-i
        return value
    def kth(self,k):
        index=0;step=1<<(len(self.a).bit_length()-1)
        while step:
            following=index+step
            if following<len(self.a)and self.a[following]<k:k-=self.a[following];index=following
            step//=2
        return index

@oracle(27018)
def cantor(text):
    values=integers(text);n=values[0];a=values[1:];tree=Fenwick(n+1);mod=998244353;answer=0
    for i,v in enumerate(reversed(a),1):answer=(answer+tree.prefix(v)*factorial(i-1,mod))%mod;tree.add(v,1)
    return str((answer+1)%mod)

@lru_cache(None)
def factorial(n,mod):
    # 缓存整条阶乘表，而不递归到百万层。
    while len(FACTORIALS)<=n:FACTORIALS.append(FACTORIALS[-1]*len(FACTORIALS)%mod)
    return FACTORIALS[n]
FACTORIALS=[1]

@oracle(27072)
def sum_lcs(text):
    n=int(text);numbers=[str(i)for i in range(1,n+1)];answer=0
    # LCS长度和=对每个长度，统计至少共享一个子串的有序对数。对子串集合容斥。
    for width in range(1,len(str(n))+1):
        counts=Counter()
        for s in numbers:
            pieces=sorted({s[i:i+width]for i in range(len(s)-width+1)})
            for mask in range(1,1<<len(pieces)):
                key=tuple(pieces[i]for i in range(len(pieces))if mask>>i&1);counts[key]+=1
        answer+=sum(v*v*(1 if len(key)%2 else -1)for key,v in counts.items())
    return str(answer)

@oracle(27093)
def constrained_queue(text):
    values=integers(text);n,d=values[:2];a=values[2:];ordered=sorted(set(a));size=len(ordered)
    # 持久化值域树把所有不可交换的先后约束编码为DAG；以最小堆取字典序最小拓扑序。
    head=array('i',[-1])*n;degree=array('i',[0])*n;left=array('i',[-1])*n;right=array('i',[-1])*n
    destination=array('i');following=array('i')
    def node(l,r):
        k=len(head);head.append(-1);degree.append(0);left.append(l);right.append(r)
        for child in(l,r):
            if child>=0:edge(child,k)
        return k
    def edge(source,target):destination.append(target);following.append(head[source]);head[source]=len(destination)-1;degree[target]+=1
    def update(old,lo,hi,index,value):
        if hi-lo==1:
            if old>=0:edge(old,value)
            return value
        mid=(lo+hi)//2;l=left[old]if old>=0 else -1;r=right[old]if old>=0 else -1
        if index<mid:l=update(l,lo,mid,index,value)
        else:r=update(r,mid,hi,index,value)
        return node(l,r)
    def connect(root,lo,hi,start,end,target):
        if root<0 or end<=lo or hi<=start:return
        if start<=lo and hi<=end:edge(root,target);return
        mid=(lo+hi)//2;connect(left[root],lo,mid,start,end,target);connect(right[root],mid,hi,start,end,target)
    root=-1
    for i,v in enumerate(a):
        lower=bisect_left(ordered,v-d);upper=bisect_right(ordered,v+d)
        connect(root,0,size,0,lower,i);connect(root,0,size,upper,size,i);root=update(root,0,size,bisect_left(ordered,v),i)
    pending=deque(i for i in range(len(head))if degree[i]==0 and i>=n);heap=[(a[i],i)for i in range(n)if degree[i]==0];heapq.heapify(heap);out=[]
    def release(vertex):
        link=head[vertex]
        while link>=0:
            v=destination[link];degree[v]-=1
            if degree[v]==0:
                if v<n:heapq.heappush(heap,(a[v],v))
                else:pending.append(v)
            link=following[link]
    while heap or pending:
        while pending:release(pending.popleft())
        if heap:v,i=heapq.heappop(heap);out.append(v);release(i)
    assert len(out)==n
    return ' '.join(map(str,out))

@oracle(27103)
def absent_melody(text):
    values=integers(text);n,m=values[:2];seen=set();length=1
    for v in values[2:]:
        seen.add(v)
        if len(seen)==m:seen.clear();length+=1
    return str(length)

@oracle(27104)
def cameras(text):
    a=integers(text)[1:];n=len(a);reach=[-1]*n
    for i,r in enumerate(a):start=max(0,i-r);reach[start]=max(reach[start],i+r)
    current=answer=index=0;farthest=-1
    while current<n:
        while index<n and index<=current:farthest=max(farthest,reach[index]);index+=1
        assert farthest>=current
        current=farthest+1;answer+=1
    return str(answer)

@oracle(27122)
def magnetism(text):
    values=integers(text);n,m=values[:2];a=sorted(values[2:]);low=0;high=(a[-1]-a[0])//(m-1)+1
    while high-low>1:
        distance=(low+high)//2;count=1;previous=a[0]
        for x in a[1:]:
            if x-previous>=distance:count+=1;previous=x
        if count>=m:low=distance
        else:high=distance
    return str(low)

@oracle(27141)
def love(text):
    a=integers(text)[1:];first={0:0};prefix=best=0
    for i,v in enumerate(a,1):
        prefix+=v-520
        if prefix in first:best=max(best,i-first[prefix])
        else:first[prefix]=i
    return str(best*520)

@oracle(27205)
def empty_rectangle(text):
    rows=[integers(r)for r in text.splitlines()];n,m=rows[0];height=[0]*m;answer=0
    for row in rows[1:]:
        for j,v in enumerate(row):height[j]=0 if v else height[j]+1
        stack=[]
        for j,h in enumerate(height+[0]):
            start=j
            while stack and stack[-1][1]>h:
                start,previous=stack.pop();answer=max(answer,previous*(j-start))
            if not stack or stack[-1][1]<h:stack.append((start,h))
    return str(answer)

@oracle(27256)
def queue_median(text):
    rows=text.splitlines()[1:];values=sorted({int(r.split()[1])for r in rows if r.startswith('add')});ids={v:i for i,v in enumerate(values)};tree=Fenwick(len(values));queue=deque();out=[]
    for r in rows:
        if r.startswith('add'):v=int(r.split()[1]);queue.append(v);tree.add(ids[v],1)
        elif r=='del':tree.add(ids[queue.popleft()],-1)
        else:
            n=len(queue);a=values[tree.kth((n+1)//2)];b=values[tree.kth(n//2+1)];twice=a+b
            out.append(str(twice//2)if twice%2==0 else str(twice/2))
    return lines(out)

@oracle(27300)
def models(text):
    groups=defaultdict(list)
    for token in text.split()[1:]:name,size=token.split('-');groups[name].append(size)
    return lines(name+': '+', '.join(sorted(groups[name],key=lambda s:Decimal(s[:-1])*(1000 if s[-1]=='B'else 1)))for name in sorted(groups))

@oracle(27311)
def air_conditioner(text):
    rows=[integers(r)for r in text.splitlines()];delta=[p-t for p,t in zip(rows[1],rows[2])];a=[0]+delta+[0]
    return str(sum(abs(y-x)for x,y in zip(a,a[1:]))//2)

@oracle(27312)
def photograph(text):
    s=text.split()[1];orientations=[int(a=='G')for a,b in zip(s[::2],s[1::2])if a!=b]
    return str(sum(x!=y for x,y in zip(orientations,orientations[1:]+[0])))

@oracle(27313)
def rabbits(text):
    a=tuple(integers(text)[1:]);mod=1000000007
    @lru_cache(None)
    def count(p):
        n=len(p)
        if n<=1:return 1
        smallest=min(p);answer=0
        for k in range(n-1):
            q=list(p);q[k],q[k+1]=q[k+1],q[k]
            if set(q[:k+1])!=set(range(smallest,smallest+k+1)):continue
            answer+=count(tuple(q[:k+1]))*count(tuple(q[k+1:]))*comb(n-2,k)
        return answer%mod
    return str(count(a))

@oracle(27314)
def replace_words(text):
    source,raw=text.splitlines()[:2];old,new=raw.lower().split();source=re.sub('[A-Za-z]+',lambda m:new if m[0].lower()==old else m[0].lower(),source)
    first=True;out=[]
    for c in source:
        if c.isalpha()and first:c=c.upper();first=False
        if c=='.':first=True
        out.append(c)
    return ''.join(out)

@oracle(27363)
def printer(text):
    a=integers(text)[1:];last={v:i for i,v in enumerate(a)if v};stack=[];seen=set();maximum=0
    for i,v in enumerate(a):
        if v==0:
            if stack:return '-1'
            continue
        if v not in seen:seen.add(v);stack.append(v);maximum=max(maximum,len(stack))
        if not stack or stack[-1]!=v:return '-1'
        if last[v]==i:stack.pop()
    return str(maximum)

@oracle(27371)
def playfair(text):
    rows=text.splitlines();alphabet='abcdefghiklmnopqrstuvwxyz';key=''.join(dict.fromkeys(rows[0].replace('j','i')+alphabet));positions={c:divmod(i,5)for i,c in enumerate(key)};out=[]
    for raw in rows[2:]:
        raw=raw.replace('j','i');i=0;cipher=''
        while i<len(raw):
            a=raw[i];i+=1
            if i==len(raw)or raw[i]==a:b='q'if a=='x'else 'x'
            else:b=raw[i];i+=1
            x,y=positions[a];xx,yy=positions[b]
            if x==xx:y=(y+1)%5;yy=(yy+1)%5
            elif y==yy:x=(x+1)%5;xx=(xx+1)%5
            else:y,yy=yy,y
            cipher+=key[5*x+y]+key[5*xx+yy]
        out.append(cipher)
    return lines(out)

@oracle(27372)
def safe_subsets(text):
    words=sorted(text.split()[1:]);children=defaultdict(list);roots=[];stack=[]
    for i,w in enumerate(words):
        while stack and not w.startswith(words[stack[-1]]):stack.pop()
        if stack:children[stack[-1]].append(i)
        else:roots.append(i)
        stack.append(i)
    dp={}
    for i in reversed(range(len(words))):
        total=1
        for child in children[i]:total*=dp[child]
        dp[i]=total+1
    answer=1
    for root in roots:answer*=dp[root]
    return str(answer)

@oracle(27373)
def largest_bounded_number(text):
    tokens=text.split();limit=int(tokens[0]);a=tokens[2:];a.sort(key=cmp_to_key(lambda x,y:(x+y>y+x)-(x+y<y+x)),reverse=True);dp=[None]*(limit+1);dp[0]=''
    for word in a:
        length=len(word)
        for n in range(limit,length-1,-1):
            if dp[n-length]is not None:
                candidate=dp[n-length]+word
                if dp[n]is None or candidate>dp[n]:dp[n]=candidate
    return max((s for s in dp if s is not None),key=lambda s:(len(s),s))or '0'

@oracle(27401)
def order_total(text):
    values=integers(text);n,target=values[:2];possible=1
    for p in values[2:]:possible|=possible<<p
    tail=possible>>target
    return str(target+(tail&-tail).bit_length()-1)if tail else '0'

@oracle(27441)
def general_tickets(text):
    rows=[integers(r)for r in text.splitlines()];budget,m=rows[0];dp=[budget+1]*(budget+1);dp[0]=0
    for price,count in zip(rows[1],rows[2]):
        size=1
        while count:
            take=min(size,count);count-=take;weight=take*price
            for amount in range(budget,weight-1,-1):dp[amount]=min(dp[amount],dp[amount-weight]+take)
            size*=2
    return str(dp[-1])if dp[-1]<=budget else 'Fail'

@oracle(27598)
def timber(text):
    values=integers(text);n,m=values[:2];prices=values[2:];dp=[0]+[-10**9]*n
    for count in range(1,m+1):dp=[-10**9]*count+[max(dp[total-length]+prices[length-1]for length in range(1,total-count+2))for total in range(count,n+1)]
    return str(dp[n])

@oracle(27623)
def euclid_game(text):
    values=integers(text);out=[]
    @lru_cache(None)
    def win(a,b):
        a,b=sorted((a,b))
        if not a:return False
        if b//a>=2:return True
        return not win(b-a,a)
    for a,b in zip(values[::2],values[1::2]):
        if a==b==0:break
        out.append('win'if win(a,b)else 'lose')
    return lines(out)

@oracle(27625)
def avl_nodes(text):
    n=int(text);a,b=0,1
    for _ in range(n):a,b=b,a+b+1
    return str(a)

@oracle(27626)
def avl_height(text):
    n=int(text);a,b=0,1;levels=0
    while b<=n:a,b=b,a+b+1;levels+=1
    return str(levels)

@oracle(27631)
def purse(text):
    values=iter(integers(text));out=[]
    for _ in range(next(values)):
        n=next(values);prices=[next(values)for _ in range(n)]
        if any(p%10 for p in prices):out.append(-1);continue
        prices=[p//10 for p in prices];best=max(prices)+1
        for a,b,c in product(range(19),range(9),range(3)):
            count=a+b+c
            if count>=best:continue
            reachable=1
            for number,coin in((a,1),(b,2),(c,5)):
                for _ in range(number):reachable|=reachable<<coin
            small=[v for v in range(a+2*b+5*c+1)if reachable>>v&1];hundreds=0
            for price in prices:
                feasible=[v for v in small if v<=price and v%10==price%10]
                if not feasible:break
                hundreds=max(hundreds,(price-max(feasible))//10)
            else:best=min(best,count+hundreds)
        out.append(best)
    return lines(out)

@oracle(27637)
def bracket_tree(text):
    out=[]
    for source in text.splitlines()[1:]:
        tokens=iter(source);look=[next(tokens,None)]
        def advance():c=look[0];look[0]=next(tokens,None);return c
        def parse():
            c=advance()
            if c=='*':return ('','')
            left=right=('','')
            if look[0]=='(':
                advance();left=parse()
                if look[0]==',':advance();right=parse()
                assert advance()==')'
            return(c+left[0]+right[0],left[1]+c+right[1])
        preorder,inorder=parse();assert look[0]is None;out.extend((preorder,inorder))
    return lines(out)
