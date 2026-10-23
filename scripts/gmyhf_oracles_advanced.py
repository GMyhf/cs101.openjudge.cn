"""独立复核大规模序列、路径与状态动态规划。"""
from gmyhf_oracles_basic import oracle,integers,lines,matrix
from collections import Counter,defaultdict,deque
from bisect import bisect_left,bisect_right
from math import comb
import heapq

@oracle(29950)
def unique_run(text):
    seen={};left=best=0
    for i,c in enumerate(text.strip()):left=max(left,seen.get(c,-1)+1);seen[c]=i;best=max(best,i-left+1)
    return str(best)

@oracle(29952)
def parentheses(text):
    a=text.strip();dp=[0]*(len(a)+1);best=0
    for i,c in enumerate(a,1):
        if c==')':
            preceding=i-dp[i-1]-1
            if preceding>=1 and a[preceding-1]=='(':dp[i]=dp[i-1]+2+dp[preceding-1];best=max(best,dp[i])
    return str(best)

@oracle(29954)
def blink(text):
    rows=text.splitlines();n,m,k=integers(rows[0]);g=rows[1:];start=next((i,j)for i in range(n)for j in range(m)if g[i][j]=='S');q=deque([(*start,0,0)]);seen={(*start,0)}
    while q:
        i,j,used,d=q.popleft()
        if g[i][j]=='E':return str(d)
        for x,y in((i-1,j),(i+1,j),(i,j-1),(i,j+1)):
            if 0<=x<n and 0<=y<m:
                spent=used+(g[x][y]=='#');state=(x,y,spent)
                if spent<=k and state not in seen:seen.add(state);q.append((*state,d+1))
    return '-1'

@oracle(29982)
def digit_classes(text):
    a,b,k=map(int,text.strip().split(','));groups=defaultdict(list)
    for v in range(a+1,b):
        total=sum(map(int,str(v)))
        if total%k==0:groups[total].append(v)
    return lines(','.join(map(str,groups[t]))for t in sorted(groups))

@oracle(30102)
def perfect_window(text):
    a=integers(text)[1:];minima=[];maxima=[];answer=0
    for j,v in enumerate(a):
        while minima and a[minima[-1]]>=v:minima.pop()
        while maxima and a[maxima[-1]]<v:maxima.pop()
        bound=maxima[-1]if maxima else -1
        index=bisect_right(minima,bound)
        if index<len(minima):answer=max(answer,j-minima[index]+1)
        minima.append(j);maxima.append(j)
    return str(answer)

@oracle(30158)
def affine_recurrence(text):
    a,b,p,q,r,n,mod=integers(text)
    def multiply(x,y):return [[sum(x[i][k]*y[k][j]for k in range(3))%mod for j in range(3)]for i in range(3)]
    acc=[[1,0,0],[0,1,0],[0,0,1]];base=[[p,q,r],[1,0,0],[0,0,1]];power=n-2
    while power:
        if power&1:acc=multiply(acc,base)
        base=multiply(base,base);power//=2
    return str((acc[0][0]*b+acc[0][1]*a+acc[0][2])%mod)

@oracle(30163)
def minecraft(text):
    values=iter(integers(text));out=[]
    for _ in range(next(values)):
        n,m=next(values),next(values);g=[[next(values)for _ in range(m)]for _ in range(n)];start=(next(values)-1,next(values)-1);depth={start:0};q=deque([start]);flow_cache={}
        def neighbors(i,j):return [(x,y)for x,y in((i-1,j),(i+1,j),(i,j-1),(i,j+1))if 0<=x<n and 0<=y<m and g[x][y]<=g[i][j]]
        def flows(i,j):
            if (i,j)in flow_cache:return flow_cache[i,j]
            choices=neighbors(i,j);routes=[];least=6
            for x,y in choices:
                # 对每个第一步分别BFS找距离5以内的下落点，保留所有最短第一步。
                queue=deque([(x,y,1)]);seen={(i,j),(x,y)};distance=6
                while queue:
                    a,b,d=queue.popleft()
                    if g[a][b]<g[i][j]:distance=d;break
                    if d==5:continue
                    for aa,bb in neighbors(a,b):
                        if (aa,bb)not in seen:seen.add((aa,bb));queue.append((aa,bb,d+1))
                routes.append((distance,(x,y)));least=min(least,distance)
            selected=[point for d,point in routes if least==6 or d==least];flow_cache[i,j]=selected;return selected
        while q:
            i,j=q.popleft();d=depth[i,j]
            if d==7:continue
            for x,y in flows(i,j):
                following=0 if g[x][y]<g[i][j]else d+1
                if following<depth.get((x,y),8):depth[x,y]=following;q.append((x,y))
        out.append(len(depth))
    return lines(out)

@oracle(30178)
def sliding_puzzle(text):
    values=integers(text);n=values[0];a=values[1:];permutation=[v-1 if v else n*n-1 for v in a];seen=bytearray(n*n);cycles=0
    for i in range(n*n):
        if seen[i]:continue
        cycles+=1;j=i
        while not seen[j]:seen[j]=1;j=permutation[j]
    permutation_parity=(n*n-cycles)%2;zero=a.index(0);distance_parity=(2*n-2-zero//n-zero%n)%2
    return 'yes'if permutation_parity==distance_parity else 'no'

@oracle(30201)
def salesman(text):
    rows=[integers(r)for r in text.splitlines()];n=rows[0][0];cost=rows[1:];full=(1<<n)-1
    # 逐层字典DP只保留同一访问数的状态，不读取参考实现。
    dp={(1,0):0}
    for count in range(1,n):
        following={}
        for (mask,last),value in dp.items():
            remaining=full^mask
            while remaining:
                bit=remaining&-remaining;vertex=bit.bit_length()-1;key=(mask|bit,vertex);candidate=value+cost[last][vertex]
                if candidate<following.get(key,10**20):following[key]=candidate
                remaining-=bit
        dp=following
    return str(min(value+cost[last][0]for (mask,last),value in dp.items()))

@oracle(30204)
def inference(text):
    rows=[integers(r)for r in text.splitlines()];n,budget=rows[0];pair=min(x+y for x,y in rows[1:]);cold=sorted(x for x,y in rows[1:]);prefix=0;answer=2*(budget//pair)
    for k,x in enumerate(cold,1):
        prefix+=x
        if prefix>budget:break
        answer=max(answer,k+2*((budget-prefix)//pair))
    return str(answer)

@oracle(30212)
def binary_ones(text):
    n,k=integers(text);answer=0;remaining=k
    for bit in reversed(range(n.bit_length())):
        if n>>bit&1:
            if 0<=remaining<=bit:answer+=comb(bit,remaining)
            remaining-=1
            if remaining<0:break
    if remaining==0:answer+=1
    if k==0:answer-=1
    return str(answer)

@oracle(30216)
def pardon(text):
    n=int(text);size=1<<n;full=size-1
    return matrix([[int((i|j)==full)for j in range(size)]for i in range(size)])

@oracle(30218)
def collision(text):
    stack=[]
    for v in integers(text)[1:]:
        while v<0 and stack and stack[-1]>0:
            previous=stack.pop();total=previous+v
            if total>0:stack.append(total);v=0
            else:v=total
        if v:stack.append(v)
    return str(len(stack))+'\n'+' '.join(map(str,stack))

@oracle(30220)
def trade(text):
    rows=[integers(r)for r in text.splitlines()];n,m=rows[0];no=[-10**12]*m;yes=[-10**12]*m
    for i,row in enumerate(rows[1:]):
        for j,v in enumerate(row):
            previous_no=max(no[j],no[j-1]if j else -10**12)if i or j else 0
            previous_yes=max(yes[j],yes[j-1]if j else -10**12)
            no[j]=previous_no+v;yes[j]=max(previous_yes+v,previous_no-v if v<0 else -10**12)
    return str(max(no[-1],yes[-1]))

@oracle(30274)
def explosions(text):
    values=integers(text);n,limit=values[:2];a=values[2:];dp={};empty=1<<limit
    for i,v in enumerate(a):dp[i,i+1]=1<<v
    for length in range(2,n+1):
        for left in range(n-length+1):
            right=left+length;possible=0
            for split in range(left+1,right):
                first=dp[left,split];second=dp[split,right]
                if first&empty:possible|=second
                if second&empty:possible|=first
                aa=[v for v in range(limit)if first>>v&1];bb=[v for v in range(limit)if second>>v&1]
                for x in aa:
                    for y in bb:possible|=empty if x+y>=limit else 1<<(x+y)
            dp[left,right]=possible
    states=dp[0,n];return str(max([0]+[v for v in range(limit)if states>>v&1]))

@oracle(30276)
def hanoi(text):
    k,n=integers(text);level=answer=0
    while n:
        capacity=comb(level+k-3,k-3);take=min(n,capacity);answer+=take*(1<<level);n-=take;level+=1
    return str(answer)

@oracle(30283)
def knight_distance(text):
    def infinite(x,y):
        x,y=sorted((abs(x),abs(y)),reverse=True)
        if(x,y)==(1,0):return 3
        if(x,y)==(2,2):return 4
        d=max((x+1)//2,(x+y+2)//3);return d+((d+x+y)%2)
    out=[]
    for row in text.splitlines()[1:]:
        x,y,a,b=integers(row);distance=infinite(x-a,y-b)
        if abs(x-a)==abs(y-b)==1 and any(point in((0,0),(0,999),(999,0),(999,999))for point in((x,y),(a,b))):distance=4
        # 每步必须降低下界，构造完整的棋盘内证书以核对有限边界。
        path=[(x,y)];remaining=distance
        while remaining:
            options=[(xx,yy)for dx,dy in((1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1))for xx,yy in[(x+dx,y+dy)]if 0<=xx<=999 and 0<=yy<=999 and infinite(xx-a,yy-b)==remaining-1]
            if not options:raise ValueError('未构造达到距离下界的棋盘内路径')
            x,y=options[0];path.append((x,y));remaining-=1
        assert(x,y)==(a,b)
        out.append(distance)
    return lines(out)

@oracle(30313)
def complement_mst(text):
    rows=[integers(r)for r in text.splitlines()];n,m=rows[0];blocked=[set()for _ in range(n)];edges=[]
    for a,b,w in rows[1:]:a-=1;b-=1;blocked[a].add(b);blocked[b].add(a);edges.append((w,a,b))
    remaining=set(range(n));component=[-1]*n;count=0
    while remaining:
        root=remaining.pop();component[root]=count;queue=[root]
        while queue:
            v=queue.pop();neighbors=remaining-blocked[v]
            for u in neighbors:component[u]=count
            remaining-=neighbors;queue.extend(neighbors)
        count+=1
    parent=list(range(count))
    def find(x):
        while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
        return x
    answer=0
    for w,a,b in sorted(edges):
        aa,bb=find(component[a]),find(component[b])
        if aa!=bb:parent[aa]=bb;answer+=w
    return str(answer)

@oracle(30339)
def islands(text):
    rows=text.splitlines();n,m=integers(rows[0]);grid=rows[1:];remaining={(i,j)for i in range(n)for j in range(m)if grid[i][j]=='X'};components=[]
    def neighbors(i,j):return[(x,y)for x,y in((i-1,j),(i+1,j),(i,j-1),(i,j+1))if 0<=x<n and 0<=y<m]
    while remaining:
        root=remaining.pop();group=[root]
        for i,j in group:
            for u in neighbors(i,j):
                if u in remaining:remaining.remove(u);group.append(u)
        components.append(group)
    assert len(components)==3;distances=[]
    for group in components:
        d={v:0 for v in group};q=deque(group)
        while q:
            i,j=q.popleft()
            for x,y in neighbors(i,j):
                weight=int(grid[x][y]=='.');new=d[i,j]+weight
                if new<d.get((x,y),10**9):
                    d[x,y]=new
                    if weight:q.append((x,y))
                    else:q.appendleft((x,y))
        distances.append(d)
    return str(min(sum(d[i,j]for d in distances)-2*(grid[i][j]=='.')for i in range(n)for j in range(m)))

@oracle(30363)
def dynamic_components(text):
    values=integers(text);n,q=values[:2];parent=list(range(n));size=[1]*n;answer=0;out=[]
    def find(v):
        while parent[v]!=v:parent[v]=parent[parent[v]];v=parent[v]
        return v
    for x,y in zip(values[2::2],values[3::2]):
        a,b=find(x-1),find(y-1)
        if a!=b:
            if size[a]<size[b]:a,b=b,a
            answer+=size[a]*size[b];size[a]+=size[b];parent[b]=a
        out.append(answer)
    return lines(out)

@oracle(30376)
def absent_password(text):
    seen=set();answer=1
    for c in text.strip():
        seen.add(c)
        if len(seen)==26:seen.clear();answer+=1
    return str(answer)

@oracle(30381)
def cards(text):
    values=integers(text);n,wild=values[:2];a=values[2:];low=0;high=(sum(a)+wild)//n+1
    while high-low>1:
        copies=(low+high)//2;deficit=sum(max(0,copies-v)for v in a)
        if deficit<=wild and deficit<=copies:low=copies
        else:high=copies
    return str(low)

@oracle(30382)
def copy_paste(text):
    source,target=text.split();positions=defaultdict(list)
    for i,c in enumerate(target):positions[c].append(i)
    copies=1;current=-1
    for c in source:
        if c not in positions:return '-1'
        where=bisect_right(positions[c],current)
        if where==len(positions[c]):copies+=1;current=positions[c][0]
        else:current=positions[c][where]
    achievable=[1]
    while achievable[-1]<copies:
        operations=len(achievable);achievable.append(max([achievable[-1]]+[achievable[operations-k]*k for k in range(2,operations+1)]))
    return str(len(achievable)-1)

@oracle(30399)
def skiing(text):
    rows=[integers(r)for r in text.splitlines()];n,m=rows[0];g=rows[1:];nw=[[False]*m for _ in range(n)];se=[[False]*m for _ in range(n)]
    for i in range(n):
        for j in range(m):nw[i][j]=i==0 or j==0 or(nw[i-1][j]and g[i-1][j]<=g[i][j])or(nw[i][j-1]and g[i][j-1]<=g[i][j])
    for i in reversed(range(n)):
        for j in reversed(range(m)):se[i][j]=i==n-1 or j==m-1 or(se[i+1][j]and g[i+1][j]<=g[i][j])or(se[i][j+1]and g[i][j+1]<=g[i][j])
    return lines(f'{i} {j}'for i in range(n)for j in range(m)if nw[i][j]and se[i][j])or 'None'

@oracle(30442)
def elevator(text):
    values=iter(integers(text));out=[]
    for _ in range(next(values)):
        n=next(values);a=[next(values)for _ in range(n)];total=sum(abs(y-x)for x,y in zip(a,a[1:]));saving=max(abs(a[1]-a[0]),abs(a[-1]-a[-2]))
        for i in range(1,n-1):saving=max(saving,abs(a[i]-a[i-1])+abs(a[i+1]-a[i])-abs(a[i+1]-a[i-1]))
        out.append(total-saving)
    return lines(out)
