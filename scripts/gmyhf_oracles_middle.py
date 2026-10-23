"""依题面独立复核：日历、图、字符串、数论与动态规划。"""
from gmyhf_oracles_basic import oracle, integers, lines, matrix
from collections import Counter,defaultdict,deque
from datetime import date
from decimal import Decimal
from fractions import Fraction
from math import comb,isqrt,gcd
import heapq
import re

@oracle(20026)
def orthogonal(text):
    n=int(text)
    if n%2:return '1'
    if n%4:return '2'
    # 维数给出上界；Sylvester(2)和Paley(12)的Kronecker积给出达到上界的显式构造。
    a=b=0;remaining=n
    while remaining%2==0:a+=1;remaining//=2
    while remaining%3==0:b+=1;remaining//=3
    if remaining!=1 or a<2*b:raise ValueError('尚未构造此阶Hadamard证书')
    residues={i*i%11 for i in range(1,11)}
    h=[[1]*12]+[[1]+[-1 if i==j else 1 if (j-i)%11 in residues else -1 for j in range(11)]for i in range(11)]
    assert all(sum(x*y for x,y in zip(h[i],h[j]))==0 for i in range(12)for j in range(i))
    return str(n)

@oracle(20027)
def string_successor(text):
    a,k=text.split();value=0
    for c in a:value=value*26+ord(c)-97
    value+=int(k)+1;result=[]
    for _ in a:value,r=divmod(value,26);result.append(chr(97+r))
    assert value==0
    return ''.join(reversed(result))

@oracle(20074)
def bmi(text):
    result={'M':0,'F':0}
    for row in text.splitlines()[1:]:
        h,w,s=row.split();h=int(h);w=int(w);seen=set();months=0
        while not 185*h*h<=w*100000<=249*h*h:
            if w in seen:raise ValueError('按题面增减体重规则不能进入正常区间')
            seen.add(w);w+=8 if w*100000<185*h*h else -5;months+=1
        result[s]=max(result[s],months)
    return f"{result['M']} {result['F']}"

@oracle(20075)
def many_treasures(text):
    rows=text.splitlines();n,m,p=integers(rows[0]);g=[integers(r)for r in rows[1:n+1]]
    target=next((i,j)for i in range(n)for j in range(m)if g[i][j]==1);dist={target:0};q=deque([target])
    while q:
        i,j=q.popleft()
        for x,y in ((i-1,j),(i+1,j),(i,j-1),(i,j+1)):
            if 0<=x<n and 0<=y<m and g[x][y]!=2 and (x,y)not in dist:dist[x,y]=dist[i,j]+1;q.append((x,y))
    return lines(dist.get((y-1,x-1),'NO')for x,y in map(integers,rows[n+1:]))

@oracle(20089)
def tickets(text):
    values=integers(text);budget=values[0]
    if budget%50:return 'Fail'
    budget//=50;dp=[budget+1]*(budget+1);dp[0]=0
    for price,count in zip((1,2,5,10,20,50,100),values[1:]):
        size=1
        while count:
            take=min(size,count);count-=take;weight=price*take
            for j in range(budget,weight-1,-1):dp[j]=min(dp[j],dp[j-weight]+take)
            size*=2
    return str(dp[-1])if dp[-1]<=budget else 'Fail'

@oracle(20090)
def recurrence_digit(text):
    # 直接整数平方根生成精确前缀，再证明误差按(4-sqrt(11))递减，得到二阶递推。
    x,y=1,7
    for _ in range(40):
        z=4*y+isqrt(11*y*y);assert z==8*y-5*x;x,y=y,z
    def multiply(a,b):return tuple(sum(a[i*2+k]*b[k*2+j]for k in range(2))%10 for i in range(2)for j in range(2))
    result=[]
    for n in integers(text)[1:]:
        power=n-1;acc=(1,0,0,1);base=(8,5,1,0)
        while power:
            if power&1:acc=multiply(acc,base)
            base=multiply(base,base);power//=2
        result.append((acc[2]*7+acc[3])%10)
    return lines(result)

@oracle(20091)
def locks(text):
    # Pascal逐行相加，全程整数；不复用阶乘或浮点参考公式。
    result=[]
    for n in integers(text)[1:]:
        row=[1]
        for _ in range(n):row=[1]+[a+b for a,b in zip(row,row[1:])]+[1]
        result.append(max(row))
    return lines(result)

@oracle(20100)
def swimming(text):
    rows=[integers(r)for r in text.splitlines()];dist,record,actual=rows[1:];least=None;fastest=Fraction(0);answer=0
    for d,t,a in zip(dist,record,actual):
        speed=Fraction(d,a)
        answer+=int(a<t and ((least is None or a<least)or speed>fastest))
        least=a if least is None else min(least,a);fastest=max(fastest,speed)
    return str(answer)

@oracle(20101)
def polynomial(text):
    raw_n,poly=text.split();n=int(raw_n);coeff=[0]*10
    for token in re.findall(r'[+-]?[^+-]+',poly):
        if 'x'in token:
            a,_,power=token.partition('x');a=int(a)if a not in('','+','-')else(-1 if a=='-'else 1)
            exponent=int(power[1:])if power else 1
        else:a=int(token);exponent=0
        coeff[exponent]+=a
    transformed=[sum(a*comb(i,k)*n**(i-k)for i,a in enumerate(coeff)if i>=k)for k in range(10)]
    terms=[];base=f'(x{-n:+d})'
    for k,a in enumerate(transformed):
        if not a:continue
        sign='-'if a<0 else '+';magnitude=abs(a)
        term=str(magnitude)if not k else (str(magnitude)if magnitude!=1 else '')+base+(f'^{k}'if k>1 else '')
        terms.append((sign if terms or a<0 else '')+term)
    return ''.join(terms)or '0'

@oracle(20106)
def mountain(text):
    rows=text.splitlines();n,m,p=integers(rows[0]);grid=[r.split()for r in rows[1:n+1]];result=[]
    for row in rows[n+1:]:
        a,b,c,d=integers(row)
        if grid[a][b]=='#'or grid[c][d]=='#':result.append('NO');continue
        distances={(a,b):0};queue=[(0,a,b)]
        while queue:
            cost,i,j=heapq.heappop(queue)
            if cost!=distances[i,j]:continue
            if (i,j)==(c,d):break
            for x,y in((i-1,j),(i+1,j),(i,j-1),(i,j+1)):
                if 0<=x<n and 0<=y<m and grid[x][y]!='#':
                    new=cost+abs(int(grid[i][j])-int(grid[x][y]))
                    if new<distances.get((x,y),float('inf')):distances[x,y]=new;heapq.heappush(queue,(new,x,y))
        result.append(str(distances.get((c,d),'NO')))
    return lines(result)

@oracle(20107)
def bomb(text):
    rows=[integers(r)for r in text.splitlines()if r.strip()];d=rows[0][0];k,t=rows[1];best=-1;count=0;when=0
    for hour in range(t):
        difference=[[0]*130 for _ in range(130)]
        for x,y,*people in rows[2:]:
            a,b=max(0,x-d),max(0,y-d);c,e=min(129,x+d+1),min(129,y+d+1);v=people[hour]
            difference[a][b]+=v;difference[c][b]-=v;difference[a][e]-=v;difference[c][e]+=v
        subtotal=0;places=0
        for i in range(129):
            for j in range(129):
                if i:difference[i][j]+=difference[i-1][j]
                if j:difference[i][j]+=difference[i][j-1]
                if i and j:difference[i][j]-=difference[i-1][j-1]
                v=difference[i][j]
                if v>subtotal:subtotal=v;places=1
                elif v==subtotal:places+=1
        if subtotal>best:best=subtotal;count=places;when=hour
    return f'{count} {when} {best}'

@oracle(20121,21462)
def unspiral(text):
    rows=[integers(r)for r in text.splitlines()];n=rows[0][0];g=rows[1:];out=[];top=left=0;bottom=right=n-1
    while top<=bottom and left<=right:
        out.extend(g[top][left:right+1]);top+=1
        out.extend(g[i][right]for i in range(top,bottom+1));right-=1
        if top<=bottom:out.extend(reversed(g[bottom][left:right+1]));bottom-=1
        if left<=right:out.extend(g[i][left]for i in range(bottom,top-1,-1));left+=1
    return ''.join(map(str,out))

@oracle(21462)
def encrypted_compliment(text):
    rows=[integers(r)for r in text.splitlines()];n=rows[0][0];g=rows[1:];values=[];top=left=0;bottom=right=n-1
    while top<=bottom and left<=right:
        values.extend(g[i][left]for i in range(top,bottom+1));left+=1
        values.extend(g[bottom][j]for j in range(left,right+1));bottom-=1
        if left<=right:values.extend(g[i][right]for i in range(bottom,top-1,-1));right-=1
        if top<=bottom:values.extend(g[top][j]for j in range(right,left-1,-1));top+=1
    return ''.join(chr(v)for v in values if v)

@oracle(20122)
def financial_date(text):
    rows=[integers(r)for r in text.splitlines()];n,today=rows[0];quarters=(-4,1,2,3)
    return lines(next((quarters[i]for i in reversed(range(4))if r[i]<=today),-3)for r in rows[1:])

@oracle(20125)
def antichain(text):
    sizes=integers(text)[1:]
    if len(sizes)==1:return '1'
    polynomial=[1]
    for size in sizes:
        out=[];window=0
        for degree in range(len(polynomial)+size):
            if degree<len(polynomial):window+=polynomial[degree]
            if 0<=degree-size-1<len(polynomial):window-=polynomial[degree-size-1]
            out.append(window)
        polynomial=out
    return str(max(polynomial))

@oracle(20127)
def supplies(text):
    rows=[integers(r)for r in text.splitlines()];n,m=rows[0];g=rows[1:];dist={(0,0):0};queue=deque([(0,0)])
    while queue:
        i,j=queue.popleft()
        for x,y in((i-1,j),(i+1,j),(i,j-1),(i,j+1)):
            if 0<=x<n and 0<=y<m and g[x][y]!=2:
                weight=int(g[x][y]!=3);candidate=dist[i,j]+weight
                if candidate<dist.get((x,y),float('inf')):
                    dist[x,y]=candidate
                    if weight:queue.append((x,y))
                    else:queue.appendleft((x,y))
    target=next((i,j)for i in range(n)for j in range(m)if g[i][j]==1)
    return str(dist.get(target,'NO'))

@oracle(20134)
def fueling(text):
    rows=[list(map(Decimal,r.split()))for r in text.splitlines()];destination,capacity,mileage,price,n=rows[0]
    stations=[(Decimal(0),price)]+[(r[0],r[1])for r in rows[1:]];reach=capacity*mileage
    events=sorted({Decimal(0),destination}|{x for x,p in stations if 0<=x<destination}|{x+reach for x,p in stations if x+reach<destination})
    stations.sort();index=0;heap=[];cost=Decimal(0)
    for a,b in zip(events,events[1:]):
        while index<len(stations)and stations[index][0]<=a:
            position,p=stations[index];heapq.heappush(heap,(p,position+reach));index+=1
        while heap and heap[0][1]<=a:heapq.heappop(heap)
        if not heap:return 'No Solution'
        cost+=(b-a)*heap[0][0]/mileage
    return f'{cost:.2f}'

@oracle(20136)
def rick(text):
    rows=[integers(r)for r in text.splitlines()];police,n=rows[0];g={r[0]:r[1:]for r in rows[1:]}
    if police==1:return 'YES!'if any(v!=0 for v in g.get(1,[]))else 'NO!'
    depth={1:0};stack=[(1,None,iter(g[1]))]
    while stack:
        vertex,parent,it=stack[-1]
        try:neighbor=next(it)
        except StopIteration:stack.pop();continue
        if neighbor==parent:continue
        if neighbor not in depth:depth[neighbor]=depth[vertex]+1;stack.append((neighbor,vertex,iter(g[neighbor])))
        elif depth[neighbor]<depth[vertex]and depth[vertex]-depth[neighbor]+1>police:return 'YES!'
    return 'NO!'

@oracle(20140)
def decompress(text):
    stack=[];current='';number=''
    for c in text.strip():
        if c=='[':stack.append((current,number));current='';number=''
        elif c.isdigit():number+=c
        elif c==']':
            prefix,unused=stack.pop();count=int(number)if number else 1
            # 重复次数出现在每个左括号后，先在读取首字母时保存。
            current=prefix+current*count;number=unused
        else:current+=c
    assert not stack
    return current

@oracle(20162)
def offline(text):
    values=integers(text);out=[]
    for i in range(1,len(values),4):
        a,b,c,r=values[i:i+4];a,b=sorted((a,b));out.append(b-a-max(0,min(b,c+r)-max(a,c-r)))
    return lines(out)

@oracle(20163)
def proper_names(text):
    out=[];seen=set();sentence_start=True
    for paragraph in text.splitlines()[1:]:
        words=paragraph.split();i=0
        while i<len(words):
            w=words[i]
            if 'A'<=w[0]<='Z':
                end=i+1
                while end<len(words)and 'A'<=words[end][0]<='Z':end+=1
                if end-i>1 or not sentence_start:
                    name=' '.join(words[i:end])
                    if name not in seen:seen.add(name);out.append(name)
                i=end;sentence_start=False
            else:sentence_start=w=='.';i+=1
    return lines(out)or 'Khong!'

@oracle(20196)
def islamic(text):
    year,month,day=integers(text);length=366 if year%4==0 and(year%100!=0 or year%400==0)else 365
    elapsed=(date(year,month,day)-date(year,1,1)).days
    h=(Fraction(year)+Fraction(elapsed,length)-Fraction(6215774,10000))/Fraction(970224,1000000)
    y=h.numerator//h.denominator;leap=y%30 in(2,5,7,10,13,16,18,21,24,26,29)
    fraction=(h-y)*(355 if leap else 354);ordinal=(fraction.numerator+fraction.denominator-1)//fraction.denominator
    m=1
    while ordinal>(30 if m%2 or m==12 and leap else 29):ordinal-=30 if m%2 or m==12 and leap else 29;m+=1
    return f'{y} {m} {ordinal}'

@oracle(21458)
def workout(text):
    rows=[integers(r)for r in text.splitlines()];budget,n=rows[0];dp={0:0}
    for duration,value in rows[1:]:
        for t,v in list(dp.items()):
            if t+duration<=budget:dp[t+duration]=max(dp.get(t+duration,-1),v+value)
    return str(dp.get(budget,-1))

@oracle(21459)
def collatz(text):
    n=int(text);out=[]
    while n!=1:
        value=n//2 if n%2==0 else 3*n+1
        out.append(f'{n}/2={value}'if n%2==0 else f'{n}*3+1={value}');n=value
    return lines(out)

@oracle(21532)
def gcd_password(text):
    n=int(text);divisors=[]
    for d in range(1,isqrt(n)+1):
        if n%d==0:divisors.extend((d,n//d))
    # 三个互异正整数至少为g,2g,3g；每个和>=6的约化和可取1,2,s-3（s=6例外同样成立）。
    return str(max(d for d in divisors if n//d>=6))

@oracle(21554)
def experiments(text):
    values=integers(text);n=values[0];order=sorted(range(n),key=lambda i:(values[i+1],i));elapsed=wait=0
    for i in order:wait+=elapsed;elapsed+=values[i+1]
    return ' '.join(str(i+1)for i in order)+f'\n{wait/n:.2f}'

@oracle(21608)
def classmates(text):
    g={};vertices=set()
    for row in text.splitlines()[1:]:
        a,b=row.split(':');a=int(a);neighbors=[v for v in integers(b)if v!=-1];g[a]=neighbors;vertices.add(a);vertices.update(neighbors)
    ids={v:i for i,v in enumerate(vertices)};reach={v:(1<<ids[v])|sum(1<<ids[u]for u in set(g.get(v,[])))for v in vertices}
    for k in vertices:
        for v in vertices:
            if reach[v]>>ids[k]&1:reach[v]|=reach[k]
    return str(max(bin(v).count('1')for v in reach.values()))

@oracle(23421)
def knapsack(text):
    rows=[integers(r)for r in text.splitlines()];n,b=rows[0];prices,weights=rows[1:];dp=[0]*(b+1)
    for value,weight in zip(prices,weights):
        for j in range(b,weight-1,-1):dp[j]=max(dp[j],dp[j-weight]+value)
    return str(dp[-1])

@oracle(23454)
def spaces(text):return ' '.join(text.split())

@oracle(23558)
def limited_dfs(text):
    rows=[integers(r)for r in text.splitlines()];n,m,limit=rows[0];g=[[]for _ in range(n)]
    for a,b in rows[1:-1]:g[a].append(b);g[b].append(a)
    start=rows[-1][0];seen=set();out=[];stack=[(start,0)]
    while stack:
        v,depth=stack.pop()
        if v in seen:continue
        seen.add(v);out.append(v)
        if depth<limit:stack.extend((u,depth+1)for u in sorted(g[v],reverse=True)if u not in seen)
    return ' '.join(map(str,out))

@oracle(23564)
def mobius(text):
    n=int(text);answer=1;p=2
    while p*p<=n:
        if n%p==0:
            n//=p;answer=-answer
            if n%p==0:return '0'
        p+=1
    if n>1:answer=-answer
    return str(answer)

@oracle(23566)
def coupons(text):
    rows=text.splitlines();n,m=integers(rows[0]);totals=[0]*m
    for row in rows[1:n+1]:s,p=integers(row);totals[s-1]+=p
    total=sum(totals);total-=total//200*30
    for amount,row in zip(totals,rows[n+1:]):q,x=map(int,row.split('-'));total-=x if amount>=q else 0
    return str(total)

@oracle(25301)
def birthdays(text):
    groups=defaultdict(list)
    for row in text.splitlines()[1:]:name,m,d=row.split();groups[int(m),int(d)].append(name)
    return lines(f'{m} {d} '+' '.join(groups[m,d])for m,d in sorted(groups)if len(groups[m,d])>1)

@oracle(25302)
def concurrency(text):
    values=iter(integers(text));out=[]
    for _ in range(next(values)):
        n=next(values);events=Counter()
        for _ in range(n):a,b=next(values),next(values);events[a]+=1;events[b]-=1
        current=best=0
        for t in sorted(events):current+=events[t];best=max(best,current)
        out.append(best)
    return lines(out)
