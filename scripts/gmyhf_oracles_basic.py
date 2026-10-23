"""依题面重建的基础题独立算法；不导入题目参考解。"""
from collections import Counter, defaultdict, deque
from datetime import date
from decimal import Decimal
from fractions import Fraction
from functools import cmp_to_key
from itertools import groupby, product
from math import comb, isqrt
import heapq
import re

SOLVERS = {}

def oracle(*numbers):
    def register(function):
        for number in numbers: SOLVERS[number] = function
        return function
    return register


def integers(text): return list(map(int, text.split()))
def lines(values): return '\n'.join(map(str, values))
def matrix(rows): return '\n'.join(' '.join(map(str, row)) for row in rows)


@oracle(12555)
def quartiles(text):
    words=text.split(); n=int(words[0]); values=sorted(map(Decimal,words[1:])); assert len(values)==n
    result=[]
    for numerator in (1,2,3):
        i,r=divmod((n-1)*numerator,4)
        result.append(f'{values[i]+(values[min(i+1,n-1)]-values[i])*r/4:.2f}')
    return lines(result)

@oracle(12556)
def runs(text): return ''.join(f'({c},{sum(1 for _ in g)})' for c,g in groupby(text.strip().lower()))

@oracle(12557)
def versions(text):
    a,b=text.split(); aa=list(map(int,a.split('.'))); bb=list(map(int,b.split('.')))
    width=max(len(aa),len(bb)); aa += [0]*(width-len(aa)); bb += [0]*(width-len(bb))
    return a if aa>=bb else b

@oracle(12559)
def concatenations(text):
    words=text.split()[1:]; ordered=sorted(words,key=cmp_to_key(lambda a,b:(a+b>b+a)-(a+b<b+a)))
    return ''.join(reversed(ordered))+' '+''.join(ordered)

@oracle(12560)
def life(text):
    rows=[integers(s) for s in text.splitlines()]; n,m=rows[0]; grid=rows[1:]
    result=[]
    for i in range(n):
        row=[]
        for j in range(m):
            count=sum(grid[x][y] for x in range(max(0,i-1),min(n,i+2)) for y in range(max(0,j-1),min(m,j+2)) if (x,y)!=(i,j))
            row.append(int(count==3 or grid[i][j] and count==2))
        result.append(row)
    return matrix(result)

@oracle(16527)
def connection(text):
    a,b=text.splitlines()[:2]
    return str(next(len(a)-n for n in range(1,min(len(a),len(b))+1) if a[-n:]==b[:n]))

@oracle(16528)
def vacation(text):
    words=integers(text); plans=defaultdict(list)
    for a,b in zip(words[1::2],words[2::2]): plans[b].append(a)
    dp=[0]*62
    for d in range(61): dp[d+1]=max([dp[d]]+[dp[a]+1 for a in plans[d]])
    return str(dp[-1])

@oracle(16529)
def stock(text):
    values=list(map(Fraction,text.split()[1:])); low=values[0]; best=Fraction(1)
    for v in values:
        best=max(best,v/low); low=min(low,v)
    return f'{float(100*best):.2f}'

@oracle(16532)
def billiards(text):
    wx,wy,bx,by,dx,dy,energy=integers(text); positions=[(wx,wy),(bx,by)]; moving=0; seen=set()
    holes={(0,0),(8,0),(16,0),(0,5),(8,5),(16,5)}
    while energy:
        state=(*positions,moving,dx,dy)
        if state in seen:return '0'
        seen.add(state); x,y=positions[moving]
        if x+dx not in range(17):dx=-dx
        if y+dy not in range(6):dy=-dy
        positions[moving]=(x+dx,y+dy);energy-=1
        if positions[moving] in holes:return '-1' if moving==0 else '1'
        if positions[moving]==positions[1-moving]:moving=1-moving
    return '0'

@oracle(18105)
def hindex(text):
    values=integers(text); buckets=Counter(min(len(values),v) for v in values); count=0
    for h in reversed(range(len(values)+1)):
        count+=buckets[h]
        if count>=h:return str(h)

@oracle(18106)
def spiral(text):
    n=int(text); grid=[[0]*n for _ in range(n)];i=j=0;di,dj=0,1
    for value in range(1,n*n+1):
        grid[i][j]=value;x,y=i+di,j+dj
        if not(0<=x<n and 0<=y<n) or grid[x][y]:di,dj=dj,-di
        i+=di;j+=dj
    return matrix(grid)

@oracle(18107)
def primes(text):
    values=integers(text); bound=max(values[2::2]); sieve=bytearray(b'\1')*(bound+1)
    sieve[:2]=b'\0\0'
    for p in range(2,isqrt(bound)+1):
        if sieve[p]:sieve[p*p::p]=b'\0'*((bound-p*p)//p+1)
    return lines(' '.join(str(v) for v in range(max(2,a),b+1) if sieve[v]) or '-1' for a,b in zip(values[1::2],values[2::2]))

@oracle(18109)
def frequent(text):
    s=text.strip().lower(); counts=Counter(s); char=max(counts,key=lambda c:(counts[c],-s.index(c)))
    return f'{char} {counts[char]}'

@oracle(18146)
def airplane(text):
    values=integers(text); n,k=values[:2]; flocks=values[2:];assert len(flocks)==k
    base=sum((v+1)//2 for v in flocks); full=sum(v//4 for v in flocks)
    used=min(n,full); capacity=n-used; best=base-2*used
    one=sum(v%4==1 for v in flocks);two=sum(v%4==2 for v in flocks);three=sum(v%4==3 for v in flocks)
    for large in range(min(three,capacity)+1):
        singles=one+three-large; pairs=two+three-large; available=capacity-large
        for splits in range(pairs+1):
            aa=singles+2*splits;bb=pairs-splits
            doubles=min(available,aa,(aa+bb)//2)
            savings=2*large+2*doubles+min(available-doubles,aa+bb-2*doubles)-splits
            best=min(best,base-2*used-savings)
    return 'YES' if best<=2*n else 'NO'

@oracle(18155)
def subset_product(text):
    values=integers(text);target=values[0]; a=values[1:]; possible=set()
    for v in a:possible |= {v}|{v*p for p in possible}
    return 'YES' if target in possible else 'NO'

@oracle(18156)
def nearest_sum(text):
    from bisect import bisect_left
    values=integers(text); target=values[0];a=sorted(values[1:]);best=None
    for i,x in enumerate(a[:-1]):
        j=bisect_left(a,target-x,i+1)
        for k in (j-1,j):
            if i<k<len(a):
                value=x+a[k]
                if best is None or (abs(value-target),value)<(abs(best-target),best):best=value
    return str(best)

@oracle(18161)
def multiply_add(text):
    values=iter(integers(text)); matrices=[];sizes=[]
    for _ in range(3):
        n,m=next(values),next(values);sizes.append((n,m));matrices.append([[next(values)for _ in range(m)]for _ in range(n)])
    (n,k),(kk,m),(nn,mm)=sizes
    if k!=kk or (n,m)!=(nn,mm):return 'Error!'
    a,b,c=matrices; columns=list(zip(*b))
    return matrix([[sum(x*y for x,y in zip(row,col))+c[i][j]for j,col in enumerate(columns)]for i,row in enumerate(a)])

@oracle(18164)
def rope(text):
    # 两条已排序队列的 Huffman 合并，不使用参考解的堆。
    raw=deque(sorted(integers(text)[1:])); merged=deque(); answer=0
    def take():
        if not merged or raw and raw[0]<=merged[0]:return raw.popleft()
        return merged.popleft()
    while len(raw)+len(merged)>1:
        cost=take()+take();answer+=cost;merged.append(cost)
    return str(answer)

@oracle(18167)
def period(text):
    return lines(next(p for p in range(1,len(s)+1) if len(s)%p==0 and s[:p]*(len(s)//p)==s) for s in text.split()[1:])

@oracle(18176)
def grades(text):
    result=[]
    for row in text.splitlines()[1:]:
        a=integers(row);total=0
        for v in a:
            p=isqrt(v)
            if p*p==v and p>=2 and all(p%d for d in range(2,isqrt(p)+1)):total+=v
        result.append(f'{total/len(a):.2f}' if total else '0')
    return lines(result)

@oracle(18182)
def monster(text):
    values=iter(integers(text));answer=[]
    for _ in range(next(values)):
        n,m,b=next(values),next(values),next(values); groups=defaultdict(list)
        for _ in range(n):t,x=next(values),next(values);groups[t].append(x)
        result='alive'
        for t in sorted(groups):
            b-=sum(sorted(groups[t],reverse=True)[:m])
            if b<=0:result=str(t);break
        answer.append(result)
    return lines(answer)

@oracle(18188)
def mean_filter(text):
    rows=[integers(s)for s in text.splitlines()]; n,m=rows[0];grid=rows[1:]; sums=[[0]*(m+1)for _ in range(n+1)]
    for i in range(n):
        for j in range(m):sums[i+1][j+1]=grid[i][j]+sums[i][j+1]+sums[i+1][j]-sums[i][j]
    result=[]
    for i in range(n):
        row=[]
        for j in range(m):
            a,b=max(0,i-1),max(0,j-1);c,d=min(n,i+2),min(m,j+2)
            row.append((sums[c][d]-sums[a][d]-sums[c][b]+sums[a][b])//((c-a)*(d-b)))
        result.append(row)
    return matrix(result)

@oracle(18189)
def exercise(text):
    n,p=integers(text);profit=0
    for limit,rate in ((30,12),(60,10),(90,6),(180,4)):
        take=min(n,limit);profit+=take*rate*p;n-=take
    return str(profit)

@oracle(18211)
def armament(text):
    values=integers(text);money=values[0];costs=sorted(values[1:]); prefix=[0]
    for c in costs:prefix.append(prefix[-1]+c)
    # 固定出售数 s 后，购买最便宜的、出售最贵的；可执行性要求先买得起一件。
    if not costs or costs[0]>money:return '0'
    best=0;n=len(costs)
    from bisect import bisect_right
    for sold in range(n//2+1):
        budget=money+prefix[n]-prefix[n-sold]
        bought=min(n-sold,bisect_right(prefix,budget)-1)
        if bought>=sold:best=max(best,bought-sold)
    return str(best)

@oracle(18223)
def twenty_four(text):
    values=integers(text);return lines('YES' if any(sum(v*s for v,s in zip(row,signs))==24 and 1 in signs for signs in product((-1,1),repeat=4))else 'NO'for row in [values[i:i+4]for i in range(1,len(values),4)])

@oracle(18224)
def magic(text):
    values=integers(text)[1:]; good={a*a+b*b for a in range(1,32)for b in range(1,32)}
    return lines(f'{bin(v)} {oct(v)} {hex(v)}' for v in values if v in good)

@oracle(19546)
def momentum(text):
    return lines(' '.join(f'{b-a:.2f}'for a,b in zip(values,values[5:]))for values in [list(map(Decimal,row.split()))for row in text.splitlines()[1:]])

@oracle(19929)
def shuttle(text):
    rows=[integers(s)for s in text.splitlines()];m,n=rows[0];a,w=rows[1:];dp=[0]*(n+1)
    for target,weight in zip(a,w):dp[target]=max(dp[target],max(dp[:target+1])+weight)
    return str(max(dp))

@oracle(19930)
def treasure(text):
    rows=[integers(s)for s in text.splitlines()]; n,m=rows[0];g=rows[1:];q=deque([(0,0,0)]);seen={(0,0)}
    while q:
        i,j,d=q.popleft()
        if g[i][j]==1:return str(d)
        for x,y in ((i-1,j),(i+1,j),(i,j-1),(i,j+1)):
            if 0<=x<n and 0<=y<m and g[x][y]!=2 and (x,y)not in seen:seen.add((x,y));q.append((x,y,d+1))
    return 'NO'

@oracle(19944)
def weekdays(text):
    names=('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')
    return lines(names[date(int(s[:4]),int(s[4:6]),int(s[6:])).weekday()]for s in text.split()[1:])

@oracle(19952)
def paint(text):
    result=[]
    for n in integers(text)[1:]:
        dp=[1,1,1]
        for _ in range(n-1):dp=[sum(dp),sum(dp),dp[0]+dp[1]]
        result.append(sum(dp))
    return lines(result)

@oracle(19959)
def multiples(text):
    n=int(text);answer=0;left=1
    while left<=n:
        quotient=n//left;right=n//quotient
        answer+=(left+right)*(right-left+1)//2*(quotient*(quotient+1)//2);left=right+1
    return str(answer)

@oracle(19960)
def enigma(text):
    rows=text.splitlines();rotors=[]
    for start in (0,6,12):rotors.append({a-1:b-1 for a,b in map(integers,rows[start:start+6])})
    reflector={}
    for a,b in map(integers,rows[18:21]):reflector[a-1]=b-1;reflector[b-1]=a-1
    result=[]
    for index,char in enumerate(rows[21]):
        offsets=(index%6,index//6%6,index//36%6);v=ord(char)-97
        for rotor,offset in zip(rotors,offsets):v=(rotor[(v-offset)%6]+offset)%6
        v=reflector[v]
        for rotor,offset in reversed(list(zip(rotors,offsets))):v=({b:a for a,b in rotor.items()}[(v-offset)%6]+offset)%6
        result.append(chr(v+97))
    return ''.join(result)

def search2048(text,chain):
    rows=[integers(s)for s in text.splitlines()]; n,m,limit=rows[0];initial=tuple(tuple(r)for r in rows[1:]);# 分别按太空连续碰撞和标准2048规则枚举状态。
    def move(board,direction,chain):
        out=[list(r)for r in board]; vertical=direction<2;reverse=direction%2==1
        for j in range(m if vertical else n):
            coordinates=[(i,j)if vertical else(j,i)for i in range(n if vertical else m)]
            if reverse:coordinates.reverse()
            values=[board[x][y]for x,y in coordinates if board[x][y]]
            if chain:values.reverse()
            merged=[];locked=set()
            for v in values:
                if merged and merged[-1]==v and (chain or len(merged)-1 not in locked):
                    merged[-1]*=2;locked.add(len(merged)-1)
                    if chain:
                        while len(merged)>1 and merged[-2]==merged[-1]:merged[-2]*=2;merged.pop()
                else:merged.append(v)
            if chain:merged.reverse()
            merged += [0]*(len(coordinates)-len(merged))
            for (x,y),v in zip(coordinates,merged):out[x][y]=v
        return tuple(tuple(r)for r in out)
    states={initial};best=max(map(max,initial))
    for _ in range(limit):
        following=set()
        for board in states:
            for direction in range(4):
                new=move(board,direction,chain);best=max(best,max(map(max,new)))
                if new!=board:following.add(new)
        states=following
    return str(best)

@oracle(19961)
def game2048(text):
    return search2048(text,True)

@oracle(20052)
def standard2048(text):
    return search2048(text,False)

@oracle(20025)
def factors(text):
    result=[]
    for token in text.split():
        if not token.isdecimal():continue
        n=int(token);v=n;parts=[];p=2
        if n<=1:result.append('no');continue
        while p*p<=v:
            power=0
            while v%p==0:v//=p;power+=1
            if power:parts.append(str(p)+(f'^{power}'if power>1 else ''))
            p+=1
        if v>1:parts.append(str(v))
        result.append(str(n)+'='+'*'.join(parts))
    return lines(result)if result else 'error'


def exact_airplane(planes,flocks):
    """小规模座位块穷举；2座块只能容纳一窝，4座块的不同窝之间必须留空。"""
    from functools import lru_cache
    @lru_cache(None)
    def possible(four,two,remaining):
        if not remaining:return True
        if sum(remaining)>4*four+2*two:return False
        if not four and not two:return False
        capacity=4 if four else 2;following=(four-1,two)if four else(four,two-1)
        options={remaining}
        for i,count in enumerate(remaining):
            for take in range(1,min(capacity,count)+1):
                values=list(remaining);values[i]-=take;options.add(tuple(sorted(v for v in values if v)))
            if capacity==4:
                for j in range(i+1,len(remaining)):
                    for a,b in((1,1),(1,2),(2,1)):
                        if a<=count and b<=remaining[j]:
                            values=list(remaining);values[i]-=a;values[j]-=b;options.add(tuple(sorted(v for v in values if v)))
        return any(possible(*following,state)for state in sorted(options,key=lambda s:(sum(s),s)))
    return possible(planes,2*planes,tuple(sorted(flocks)))
