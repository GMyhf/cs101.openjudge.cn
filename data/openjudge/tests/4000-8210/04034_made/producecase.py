import random,re,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys, heapq\nfrom collections import deque\nP=4034\ndef go(s):\n a=s.split()\n if P==3723:\n  n=int(a[0]);g=a[1:];seen=set();z=[sum(row.count("B") for row in g),sum(row.count("W") for row in g)]\n  for i in range(n):\n   for j in range(n):\n    if g[i][j]!="." or (i,j) in seen:continue\n    q=[(i,j)];seen.add((i,j));e=set();c=0\n    while q:\n     x,y=q.pop();c+=1\n     for u,v in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):\n      if 0<=u<n and 0<=v<n:\n       if g[u][v]=="." and (u,v) not in seen:seen.add((u,v));q.append((u,v))\n       elif g[u][v] in "BW":e.add(g[u][v])\n    if len(e)==1:z["BW".index(next(iter(e)))]+=c\n  return f"{z[0]} {z[1]}\\n"\n if P==3725:\n  x=list(map(int,a));v=sorted(x[1:],reverse=True);M=max(v);best=(10**9,0)\n  for k in range(1,len(v)+1):\n   q=[0]*k\n   for y in v:q[q.index(min(q))]+=y\n   best=min(best,(sum(abs(y-M) for y in q),-k))\n  return f"{-best[1]}\\n"\n if P==3726 or P==3866:\n  p=0;out=[]\n  while p<len(a):\n   R,C=map(int,a[p:p+2]);p+=2\n   if not R:break\n   g=a[p:p+(R if P==3726 else C)];p+=len(g)\n   target="*" if P==3726 else "@"; src=next((i,j) for i in range(len(g)) for j in range(len(g[0]) if g else 0) if g[i][j]==target)\n   q=deque([src]);seen={src}\n   while q:\n    x,y=q.popleft()\n    for u,v in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):\n     if 0<=u<len(g) and 0<=v<len(g[0]) and g[u][v]!="#" and (u,v) not in seen:seen.add((u,v));q.append((u,v))\n   if P==3726:\n    start=next((i,j) for i in range(R) for j in range(C) if g[i][j]=="@");q=deque([(start[0],start[1],0)]);vis={start};ans=-1\n    while q:\n     x,y,d=q.popleft()\n     if g[x][y]=="*":ans=d;break\n     for u,v in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):\n      if 0<=u<R and 0<=v<C and g[u][v]!="#" and (u,v) not in vis:vis.add((u,v));q.append((u,v,d+1))\n    out.append(str(ans))\n   else:out.append(str(len(seen)))\n  return "\\n".join(out)+"\\n"\n if P==3727:\n  p=1;out=[]\n  for _ in range(int(a[0])):\n   R,C=map(int,a[p:p+2]);p+=2;d=[0]*C\n   for i in range(R):\n    for j in range(C):d[j]=max(d[j],d[j-1] if j else 0)+int(a[p]);p+=1\n   out.append(str(d[-1]))\n  return "\\n".join(out)+"\\n"\n if P==3728:\n  out=[]\n  for line in s.splitlines():\n   b,n=map(int,line.split());v=[b];i2=i3=0\n   while len(v)<n:\n    x=min(2*v[i2]+1,3*v[i3]+1);v.append(x)\n    while 2*v[i2]+1<=x:i2+=1\n    while 3*v[i3]+1<=x:i3+=1\n   out.append(str(v[-1]))\n  return "\\n".join(out)+"\\n"\n if P==3744:\n  return "\\n".join(str(min(2*(x*y+x*w+y*w) for x in range(1,n+1) for y in range(x,n+1) if n%(x*y)==0 for w in [n//(x*y)])) for n in map(int,a[1:]))+"\\n"\n if P==3789:\n  n,k=map(int,a[:2]);v=list(map(int,a[2:]));sa=list(range(n));rank=v[:];step=1\n  while step<n:\n   sa.sort(key=lambda i:(rank[i],rank[i+step] if i+step<n else -1));nr=[0]*n\n   for j in range(1,n):nr[sa[j]]=nr[sa[j-1]]+((rank[sa[j-1]],rank[sa[j-1]+step] if sa[j-1]+step<n else -1)<(rank[sa[j]],rank[sa[j]+step] if sa[j]+step<n else -1))\n   rank=nr;step*=2\n  pos=[0]*n\n  for i,x in enumerate(sa):pos[x]=i\n  lcp=[0]*n;h=0\n  for i in range(n):\n   p=pos[i]\n   if p==0:continue\n   j=sa[p-1]\n   while i+h<n and j+h<n and v[i+h]==v[j+h]:h+=1\n   lcp[p]=h\n   if h:h-=1\n  best=0\n  for i in range(n-k+1):\n   best=max(best,min(lcp[i+1:i+k]))\n  return str(best)+"\\n"\n if P==3791:\n  p=1;out=[]\n  for _ in range(int(a[0])):\n   n=int(a[p]);p+=1;q=sorted(a[p:p+n]);p+=n;out.append("NO" if any(y.startswith(x) for x,y in zip(q,q[1:])) else "YES")\n  return "\\n".join(out)+"\\n"\n if P==3906:\n  m,n=map(int,a[:2]);v=list(map(int,a[2:]));D={(0,0,0,0):v[0]}\n  for _ in range(m+n-2):\n   N={}\n   for (x,y,u,w),z in D.items():\n    for dx,dy in ((1,0),(0,1)):\n     for du,dw in ((1,0),(0,1)):\n      X,Y=x+dx,y+dy;U,W=u+du,w+dw\n      if X<m and Y<n and U<m and W<n and ((X,Y)!=(U,W) or (X,Y)==(m-1,n-1)):N[X,Y,U,W]=max(N.get((X,Y,U,W),-1),z+v[X*n+Y]+v[U*n+W])\n   D=N\n  return str(max(D.values()))+"\\n"\n if P==4001:\n  n,k=map(int,a);q=deque([(n,0)]);vis={n}\n  while q:\n   x,d=q.popleft()\n   if x==k:return str(d)+"\\n"\n   for y in (x-1,x+1,2*x):\n    if 0<=y<=100000 and y not in vis:vis.add(y);q.append((y,d+1))\n if P==4002:\n  v=list(map(int,a[2:]));return "".join((str(v.count(x)-1) if v.count(x)>1 else "BeiJu")+"\\n" for x in v)\n if P==4006:\n  q,n=map(int,a[:2]);out=[]\n  for i,j in zip(map(int,a[2::2]),map(int,a[3::2])):\n   l=min(i-1,j-1,n-i,n-j);z=n-2*l;st=n*n-z*z+1;u=i-l-1;v=j-l-1\n   out.append(str(st+v if u==0 else st+z-1+u if v==z-1 else st+2*z-2+z-1-v if u==z-1 else st+3*z-3+z-1-u))\n  return "\\n".join(out)+"\\n"\n if P==4007:\n  p=1;out=[]\n  for _ in range(int(a[0])):\n   x,y=a[p:p+2];p+=2;d=list(range(len(y)+1))\n   for c in x:\n    old=d;d=[old[0]+1]\n    for j in range(len(y)):d.append(min(old[j+1]+1,d[-1]+1,old[j]+(c!=y[j])))\n   out.append(str(d[-1]))\n  return "\\n".join(out)+"\\n"\n if P==4008:\n  n,k=map(int,a[:2]);d=[-10**9]*k;d[0]=0\n  for x in map(int,a[2:]):d=[max(d[j],d[(j-x)%k]+x) for j in range(k)]\n  return str(d[0])+"\\n"\n if P==4009:\n  pc=[bin(x).count("1") for x in range(65536)]\n  def pop(x):return pc[x&65535]+pc[x>>16]\n  out=[]\n  for n in map(int,a):\n   if not n:break\n   c=0\n   for mask in range(1<<n):\n    row=mask;z=2*pop(mask)-n\n    for width in range(n,1,-1):\n     row=(~(row^(row>>1)))&((1<<(width-1))-1);z+=2*pop(row)-(width-1)\n    c+=z==0\n   out.append(f"{n} {c}")\n  return "\\n".join(out)+"\\n"\n if P==4010:return "\\n".join(str(pow(2011,int(x),10000)) for x in a[1:])+"\\n"\n if P==4021:\n  p=1;out=[]\n  for _ in range(int(a[0])):\n   n=int(a[p]);v=list(map(int,a[p+1:p+1+n]));p+=n+1\n   z=[__import__("math").prod(v[:i]+v[i+1:]) for i in range(n)];out.append(str(v[z.index(max(z))]))\n  return "\\n".join(out)+"\\n"\n if P==4033:\n  n=int(a[0]);x,y=map(int,a[1+4*n:]);ans=-1\n  for i in range(n):\n   A,B,G,K=map(int,a[1+4*i:5+4*i])\n   if A<=x<=A+G and B<=y<=B+K:ans=i+1\n  return str(ans)+"\\n"\n if P==4034:\n  import bisect\n  n,k,p=map(int,a[:3]);v=[tuple(map(int,a[i:i+2])) for i in range(3,3+2*n,2)];ans=0;positions={};last_good=-1\n  for j,(color,cost) in enumerate(v):\n   if cost<=p:last_good=j\n   if last_good>=0:\n    same=positions.get(color,[]);ans+=bisect.bisect_right(same,last_good)\n   positions.setdefault(color,[]).append(j)\n  return str(ans)+"\\n"\nfor line in []:pass\nsys.stdout.write(go(sys.stdin.read()))\n'
SAMPLE_IN='5 2 3 \n0 5 \n1 3 \n0 2 \n1 4 \n1 5 \n'


def valid(text):
    """题面契约：n k p（2<=n<=200000，0<k<=50，0<=p<=100）；n 行“色调 最低消费”，色调 0..k-1，消费 0..100。
    样例行尾带空格，行尾空白放过。"""
    if not text.endswith("\n"):
        return False
    lines = [ln.rstrip(" ") for ln in text[:-1].split("\n")]
    try:
        rows = []
        for ln in lines:
            if ln == "" or ln.startswith(" ") or "  " in ln:
                return False
            toks = ln.split(" ")
            if not all(re.fullmatch(r"0|[1-9][0-9]*", t) for t in toks):  # 只收规范的非负十进制整数
                return False
            rows.append([int(x) for x in toks])
    except ValueError:
        return False
    if len(rows[0]) != 3:
        return False
    n, k, p = rows[0]
    if not (2 <= n <= 200000 and 1 <= k <= 50 and 0 <= p <= 100) or len(rows) != n + 1:
        return False
    return all(len(row) == 2 and 0 <= row[0] < k and 0 <= row[1] <= 100 for row in rows[1:])


def make(r, n, k, p, cost_lo=0, cost_hi=100, colors=None, good_rate=None):
    """good_rate 不为 None 时，按该比例放消费 <=p 的店，其余 >p（p=100 时无法 >p）。"""
    rows = []
    for _ in range(n):
        c = r.randrange(k) if colors is None else r.choice(colors)
        if good_rate is not None and p < 100:
            cost = r.randint(0, p) if r.random() < good_rate else r.randint(p + 1, 100)
        else:
            cost = r.randint(cost_lo, cost_hi)
        rows.append(f"{c} {cost}")
    return f"{n} {k} {p}\n" + "\n".join(rows) + "\n"


def gen(i):
    r = random.Random(4034 * 1000 + i)
    if i == 0:
        return SAMPLE_IN
    fixed = {
        1: "2 1 0\n0 0\n0 0\n",            # 最小规模，可行
        2: "2 1 0\n0 1\n0 1\n",            # 最小规模，不可行
        3: "2 2 100\n0 100\n1 100\n",      # 颜色不同
        4: "3 1 5\n0 9\n0 5\n0 9\n",       # 只有中间的店可去
        5: "4 50 100\n49 100\n0 0\n49 0\n0 100\n",
    }
    if i in fixed:
        return fixed[i]
    if i <= 18:
        n = r.randint(2, 30)
        k = r.choice([1, 2, 3, 50])
        return make(r, n, k, r.randint(0, 100), good_rate=r.choice([None, 0.05, 0.3, 0.8]))
    if i <= 26:
        n = r.randint(1000, 5000)
        return make(r, n, r.choice([1, 5, 50]), r.randint(0, 100), good_rate=r.choice([None, 0.001, 0.05, 0.5]))
    # 大规模；受单组 .in <= 1MB 约束：色调和消费都取一位数时 n 才能取满 2e5
    # 27..32：中等规模（4e4..8e4），体积控制在 10MB 内；满规模由 33..35 承担
    if i <= 32:
        return make(r, r.randint(40000, 80000), r.choice([1, 2, 10]), r.randint(0, 8), cost_hi=9,
                    colors=None, good_rate=None) if i % 2 else \
            make(r, r.randint(40000, 80000), 10, r.choice([0, 3]), cost_hi=9, good_rate=None)
    if i == 33:
        return make(r, 200000, 1, 9, cost_hi=9)            # 全部同色且都能去：答案约 2e10，超 32 位
    if i == 34:
        return make(r, 200000, 2, 0, cost_lo=1, cost_hi=9)  # 没有一家能去：答案 0
    if i == 35:
        return make(r, 200000, 50, 9, cost_hi=9, colors=list(range(10)))  # k=50 但只用到一位数色调
    # n 约 1.3e5、色调到 49、消费到 100
    n = 130000
    return make(r, n, 50, [100, 50, 0, 99][i - 36], good_rate=[None, 0.01, 0.2, 0.9][i - 36])


def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as h:
        h.write(REFERENCE_SOURCE)
        h.flush()
        root = Path(__file__).parent / "data"
        seen = set()
        for i in range(40):
            c = gen(i)
            assert valid(c) and c not in seen, i
            seen.add(c)
            p = subprocess.run(["python3", h.name], input=c, text=True, capture_output=True, check=True)
            (root / f"{i}.in").write_text(c, encoding="utf-8")
            (root / f"{i}.out").write_text(p.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
