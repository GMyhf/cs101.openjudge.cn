"""独立复核最后一组：SCC、博弈、文本算法和数值优化。"""
from gmyhf_oracles_basic import oracle,integers,lines,matrix
from collections import Counter,defaultdict,deque
from functools import lru_cache
from fractions import Fraction
from math import gcd,isqrt
from array import array
import heapq

@oracle(30571)
def complement(text):
    n=int(text);return str(((1<<max(1,n.bit_length()))-1)^n)

@oracle(30637)
def pop_sequences(text):
    rows=text.splitlines();source=rows[0];out=[]
    for candidate in rows[1:]:
        if len(candidate)!=len(source)or sorted(candidate)!=sorted(source):out.append('NO');continue
        stack=[];i=0
        for v in candidate:
            while(not stack or stack[-1]!=v)and i<len(source):stack.append(source[i]);i+=1
            if not stack or stack[-1]!=v:break
            stack.pop()
        else:out.append('YES');continue
        out.append('NO')
    return lines(out)

@oracle(30669)
def subway(text):
    rows=[integers(r)for r in text.splitlines()];n,root=rows[0];g=[[]for _ in range(n)]
    for a,b in rows[1:n]:g[a-1].append(b-1);g[b-1].append(a-1)
    depth=[-1]*n;depth[root-1]=0;order=[root-1]
    for v in order:
        for u in g[v]:
            if depth[u]<0:depth[u]=depth[v]+1;order.append(u)
    p,q,v1,v2=rows[n];p-=1;q-=1;parent={p:-1};queue=deque([p])
    while q not in parent:
        v=queue.popleft()
        for u in g[v]:
            if u not in parent:parent[u]=v;queue.append(u)
    path=[q]
    while path[-1]!=p:path.append(parent[path[-1]])
    path.reverse();distance=len(path)-1;assert distance%(v1+v2)==0;days=distance//(v1+v2)
    return f'{days} {depth[path[days*v1]]}'

@oracle(30680)
def forest(text):
    rows=[integers(r)for r in text.splitlines()[1:]];g={r[0]:r[1:]for r in rows};roots=sorted(set(g)-{v for r in rows for v in r[1:]});stack=[(False,v)for v in reversed(roots)];out=[]
    while stack:
        emit,v=stack.pop()
        if emit:out.append(v)
        else:stack.extend((u==v,u)for u in sorted(g[v]+[v],reverse=True))
    return lines(out)

@oracle(30868)
def upstairs(text):
    values=integers(text);steps=sorted({v for v in values[:3]if v});queries=values[4:]
    if not steps:return lines('Yes'if h==0 else 'No'for h in queries)
    common=0
    for step in steps:common=gcd(common,step)
    a=steps[0]//common;others=[step//common for step in steps[1:]];dist=[10**30]*a;dist[0]=0;queue=[(0,0)]
    while queue:
        value,residue=heapq.heappop(queue)
        if value!=dist[residue]:continue
        for step in others:
            following=(residue+step)%a;candidate=value+step
            if candidate<dist[following]:dist[following]=candidate;heapq.heappush(queue,(candidate,following))
    return lines('Yes'if h%common==0 and dist[(h//common)%a]<=h//common else 'No'for h in queries)

@oracle(30887)
def equal_sequence(text):
    a=sorted(integers(text)[1:]);n=len(a);candidates={v+delta for v in a[max(0,2*n//3-3):min(n,2*n//3+4)]for delta in(-2,-1,0,1,2)}
    def cost(target):return sum(v-target if v>=target else (target-v)//2+(2 if(target-v)%2 else 0)for v in a)
    return str(min(map(cost,candidates)))

@oracle(30888)
def rating(text):
    rows=[integers(r)for r in text.splitlines()];n,b=rows[0];scores=[]
    for difficulty,accuracy in rows[1:]:
        factor=Fraction(1)if accuracy==100 else Fraction(100+accuracy,200)if accuracy>=95 else Fraction(accuracy,150)-Fraction(1,6)if accuracy>=70 else Fraction(0)
        scores.append(difficulty*factor)
    scores.sort(reverse=True);value=sum(scores[:b])/min(n,b)
    return f'{float(value):.6f}'

@oracle(30889)
def registers(text):
    rows=text.splitlines();n=int(rows[0]);children=[[]for _ in range(n)];cost=[1]*n
    for i,row in enumerate(rows[2:],1):parent,d=row.split();children[int(parent)-1].append(i)
    for v in reversed(range(n)):
        values=sorted((cost[u]for u in children[v]),reverse=True)
        cost[v]=max([1]+[value+i for i,value in enumerate(values)])
    return str(cost[0])

@oracle(30894)
def huffman_codec(text):
    rows=text.splitlines();n=int(rows[0]);heap=[];index=0;nodes={}
    for row in rows[1:n+1]:
        char,weight=row.split();nodes[index]=(char,None,None);heapq.heappush(heap,(int(weight),char,index));index+=1
    while len(heap)>1:
        a,c,x=heapq.heappop(heap);b,d,y=heapq.heappop(heap);nodes[index]=('',x,y);heapq.heappush(heap,(a+b,min(c,d),index));index+=1
    root=heap[0][2];codes={};stack=[(root,'')]
    while stack:
        v,prefix=stack.pop();char,left,right=nodes[v]
        if char:codes[char]=prefix or '0'
        else:stack.extend(((left,prefix+'0'),(right,prefix+'1')))
    out=[]
    for row in rows[n+1:]:
        if not row:continue
        if row[0].isalpha():out.append(''.join(codes[c]for c in row))
        else:
            decoded='';v=root
            for bit in row:
                if nodes[v][1]is not None:v=nodes[v][1 if bit=='0'else 2]
                if nodes[v][0]:decoded+=nodes[v][0];v=root
            assert v==root;out.append(decoded)
    return lines(out)

@oracle(30901)
def xor67(text):
    values=iter(integers(text));out=[]
    for _ in range(next(values)):
        n=next(values);a=[next(values)for _ in range(n)]
        if n==1:out.append(a[0]);continue
        answer=0;mask=0
        for bit in reversed(range(max(a).bit_length())):
            mask|=1<<bit;prefix={v&mask for v in a};trial=answer|1<<bit
            if any((v^trial)in prefix for v in prefix):answer=trial
        out.append(answer)
    return lines(out)

@oracle(30909)
def minimax_mountain(text):
    rows=[integers(r)for r in text.splitlines()];n,m=rows[0];g=rows[1:];dist={(0,0):0};queue=[(0,0,0)]
    while queue:
        effort,i,j=heapq.heappop(queue)
        if effort!=dist[i,j]:continue
        if(i,j)==(n-1,m-1):return str(effort)
        for x,y in((i-1,j),(i+1,j),(i,j-1),(i,j+1)):
            if 0<=x<n and 0<=y<m:
                candidate=max(effort,abs(g[x][y]-g[i][j]))
                if candidate<dist.get((x,y),10**20):dist[x,y]=candidate;heapq.heappush(queue,(candidate,x,y))

@oracle(30910)
def mail(text):
    rows=[integers(r)for r in text.splitlines()];n,m=rows[0];forward=[[]for _ in range(n)];reverse=[[]for _ in range(n)]
    for a,b,w in rows[1:]:forward[a-1].append((b-1,w));reverse[b-1].append((a-1,w))
    answer=0
    for g in(forward,reverse):
        dist=[10**30]*n;dist[0]=0;queue=deque([0]);pending={0}
        while queue:
            v=queue.popleft();pending.remove(v)
            for u,w in g[v]:
                if dist[v]+w<dist[u]:
                    dist[u]=dist[v]+w
                    if u not in pending:pending.add(u);queue.append(u)
        assert max(dist)<10**30
        answer+=sum(dist)
    return str(answer)

@oracle(30911)
def secrets(text):
    n,delay,forget=integers(text);cohorts=[0]*(n+1);cohorts[1]=1;mod=1000000007
    for day in range(2,n+1):cohorts[day]=sum(cohorts[known]for known in range(1,day)if delay<=day-known<forget)%mod
    return str(sum(cohorts[max(1,n-forget+1):])%mod)

@oracle(30912)
def cumulative_tree(text):
    a=integers(text)[1:];n=len(a);left=[-1]*n;right=[-1]*n
    for i in range(1,n):
        v=0
        while True:
            branch=left if a[i]<a[v]else right
            if branch[v]<0:branch[v]=i;break
            v=branch[v]
    totals={};total=0
    for value,count in sorted(Counter(a).items(),reverse=True):total+=value*count;totals[value]=total
    order=[0]
    for v in order:
        if left[v]>=0:order.append(left[v])
        if right[v]>=0:order.append(right[v])
    return ' '.join(str(totals[a[v]])for v in order)

@oracle(30913)
def park(text):
    rows=[integers(r)for r in text.splitlines()];n,m=rows[0];g=[[]for _ in range(n)];reverse=[[]for _ in range(n)];edges=[]
    for a,b,w in rows[1:m+1]:a-=1;b-=1;g[a].append(b);reverse[b].append(a);edges.append((a,b,w))
    visited=bytearray(n);order=[]
    for root in range(n):
        if visited[root]:continue
        visited[root]=1;stack=[(root,iter(g[root]))]
        while stack:
            v,it=stack[-1]
            try:u=next(it)
            except StopIteration:order.append(v);stack.pop();continue
            if not visited[u]:visited[u]=1;stack.append((u,iter(g[u])))
    component=[-1]*n;count=0
    for root in reversed(order):
        if component[root]>=0:continue
        component[root]=count;stack=[root]
        while stack:
            for u in reverse[stack.pop()]:
                if component[u]<0:component[u]=count;stack.append(u)
        count+=1
    gain=[0]*count;dag=[[]for _ in range(count)];indegree=[0]*count
    for a,b,w in edges:
        x,y=component[a],component[b]
        if x==y:
            k=(isqrt(1+8*w)-1)//2;gain[x]+=(k+1)*w-k*(k+1)*(k+2)//6
        else:dag[x].append((y,w));indegree[y]+=1
    queue=deque(i for i in range(count)if indegree[i]==0);topological=[]
    while queue:
        v=queue.popleft();topological.append(v)
        for u,w in dag[v]:
            indegree[u]-=1
            if indegree[u]==0:queue.append(u)
    dp=gain[:]
    for v in reversed(topological):dp[v]+=max([0]+[w+dp[u]for u,w in dag[v]])
    return str(dp[component[rows[-1][0]-1]])

@oracle(30942)
def continuous_answers(text):
    source,raw=text.split();k=int(raw);best=0
    for chosen in 'TF':
        wrong=[-1]+[i for i,c in enumerate(source)if c!=chosen]+[len(source)]
        if len(wrong)-2<=k:return str(len(source))
        for i in range(len(wrong)-k-1):best=max(best,wrong[i+k+1]-wrong[i]-1)
    return str(best)

@oracle(30943)
def ranks(text):
    rows=[integers(r)for r in text.splitlines()];n,m=rows[0];g=[[]for _ in range(n)];reverse=[[]for _ in range(n)]
    for x,y,z in rows[1:]:a,b=(x,y)if z else(y,x);g[a].append(b);reverse[b].append(a)
    def reach(root,graph):
        seen={root};stack=[root]
        while stack:
            for u in graph[stack.pop()]:
                if u not in seen:seen.add(u);stack.append(u)
        return seen
    return str(sum(len(reach(i,g)|reach(i,reverse))==n for i in range(n)))

@lru_cache(8192)
def divisors(n):
    small=[];large=[]
    for d in range(1,isqrt(n)+1):
        if n%d==0:
            small.append(d)
            if d*d!=n:large.append(n//d)
    return tuple(small+large[::-1])

@oracle(30947)
def likes(text):
    rows=[integers(r)for r in text.splitlines()];n,q=rows[0];minimum=sorted((v for v in rows[1]if v>1),reverse=True);out=[];base=1
    for v in minimum:
        base*=v
        if base>10**9:break
    for query in rows[2:]:
        target=query[0]
        if target<base:out.append('No');continue
        if len(minimum)<=1:out.append('Yes');continue
        suffix=[1]*(len(minimum)+1)
        for i in reversed(range(len(minimum))):suffix[i]=suffix[i+1]*minimum[i]
        @lru_cache(None)
        def feasible(index,value):
            if value<suffix[index]:return False
            if index==len(minimum)-1:return value>=minimum[index]
            for d in divisors(value):
                if d>=minimum[index]and value//d>=suffix[index+1]and feasible(index+1,value//d):return True
            return False
        out.append('Yes'if feasible(0,target)else 'No')
    return lines(out)

@oracle(30953)
def forest_minimum(text):
    rows=[integers(r)for r in text.splitlines()];n,m=rows[0];reverse=[[]for _ in range(n)]
    for a,b in rows[1:]:reverse[b-1].append(a-1)
    result=[0]*n
    for root in range(n):
        if result[root]:continue
        result[root]=root+1;stack=[root]
        while stack:
            for u in reverse[stack.pop()]:
                if not result[u]:result[u]=root+1;stack.append(u)
    return ' '.join(map(str,result))

@lru_cache(None)
def nim_table(veto):
    # 按三坐标递增，用每条坐标线已出现的必败态数计算合法制胜移动数。
    width=101;line_a=array('H',[0])*(width*width);line_b=array('H',[0])*(width*width);line_c=array('H',[0])*(width*width);winning=bytearray(width**3)
    for a in range(width):
        for b in range(width):
            ab=a*width+b
            for c in range(width):
                ac=a*width+c;bc=b*width+c;ways=line_a[bc]+line_b[ac]+line_c[ab]
                win=ways>=2 or a+b+c==1 if veto else ways>=1
                winning[(a*width+b)*width+c]=win
                if not win:line_a[bc]+=1;line_b[ac]+=1;line_c[ab]+=1
    return winning

def nim_result(text,veto):
    table=nim_table(veto);return lines('Piggy'if table[(a*101+b)*101+c]else 'KittyPig'for a,b,c in[integers(r)for r in text.splitlines()[1:]])
@oracle(31086)
def nim(text):return nim_result(text,False)
@oracle(31087)
def veto_nim(text):return nim_result(text,True)

@oracle(31378)
def kmp_comparisons(text):
    pattern,source=text.split();n=len(pattern);border=[0]*n
    for i in range(1,n):
        k=border[i-1]
        while k and pattern[i]!=pattern[k]:k=border[k-1]
        if pattern[i]==pattern[k]:k+=1
        border[i]=k
    fallback=[-1]*n
    for j in range(1,n):
        k=border[j-1];fallback[j]=fallback[k]if pattern[j]==pattern[k]else k
    j=0;comparisons=0;position=-1
    for i,c in enumerate(source):
        while j>=0:
            comparisons+=1
            if c==pattern[j]:break
            j=fallback[j]
        j+=1
        if j==n:position=i-n+1;break
    assert position==source.find(pattern)
    return f'{comparisons} {position}'

@oracle(31418)
def heap_swaps(text):
    a=integers(text)[1:];n=len(a);count=0
    for root in reversed(range(n//2)):
        held=a[root];i=root
        while 2*i+1<n:
            child=2*i+1
            if child+1<n and a[child+1]<a[child]:child+=1
            if a[child]>=held:break
            a[i]=a[child];i=child;count+=1
        a[i]=held
    return str(count)
