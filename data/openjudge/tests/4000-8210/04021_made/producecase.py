import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys, heapq\nfrom collections import deque\nP=4021\ndef go(s):\n a=s.split()\n if P==3723:\n  n=int(a[0]);g=a[1:];seen=set();z=[sum(row.count("B") for row in g),sum(row.count("W") for row in g)]\n  for i in range(n):\n   for j in range(n):\n    if g[i][j]!="." or (i,j) in seen:continue\n    q=[(i,j)];seen.add((i,j));e=set();c=0\n    while q:\n     x,y=q.pop();c+=1\n     for u,v in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):\n      if 0<=u<n and 0<=v<n:\n       if g[u][v]=="." and (u,v) not in seen:seen.add((u,v));q.append((u,v))\n       elif g[u][v] in "BW":e.add(g[u][v])\n    if len(e)==1:z["BW".index(next(iter(e)))]+=c\n  return f"{z[0]} {z[1]}\\n"\n if P==3725:\n  x=list(map(int,a));v=sorted(x[1:],reverse=True);M=max(v);best=(10**9,0)\n  for k in range(1,len(v)+1):\n   q=[0]*k\n   for y in v:q[q.index(min(q))]+=y\n   best=min(best,(sum(abs(y-M) for y in q),-k))\n  return f"{-best[1]}\\n"\n if P==3726 or P==3866:\n  p=0;out=[]\n  while p<len(a):\n   R,C=map(int,a[p:p+2]);p+=2\n   if not R:break\n   g=a[p:p+(R if P==3726 else C)];p+=len(g)\n   target="*" if P==3726 else "@"; src=next((i,j) for i in range(len(g)) for j in range(len(g[0]) if g else 0) if g[i][j]==target)\n   q=deque([src]);seen={src}\n   while q:\n    x,y=q.popleft()\n    for u,v in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):\n     if 0<=u<len(g) and 0<=v<len(g[0]) and g[u][v]!="#" and (u,v) not in seen:seen.add((u,v));q.append((u,v))\n   if P==3726:\n    start=next((i,j) for i in range(R) for j in range(C) if g[i][j]=="@");q=deque([(start[0],start[1],0)]);vis={start};ans=-1\n    while q:\n     x,y,d=q.popleft()\n     if g[x][y]=="*":ans=d;break\n     for u,v in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):\n      if 0<=u<R and 0<=v<C and g[u][v]!="#" and (u,v) not in vis:vis.add((u,v));q.append((u,v,d+1))\n    out.append(str(ans))\n   else:out.append(str(len(seen)))\n  return "\\n".join(out)+"\\n"\n if P==3727:\n  p=1;out=[]\n  for _ in range(int(a[0])):\n   R,C=map(int,a[p:p+2]);p+=2;d=[0]*C\n   for i in range(R):\n    for j in range(C):d[j]=max(d[j],d[j-1] if j else 0)+int(a[p]);p+=1\n   out.append(str(d[-1]))\n  return "\\n".join(out)+"\\n"\n if P==3728:\n  out=[]\n  for line in s.splitlines():\n   b,n=map(int,line.split());q={b};h=[b];outv=[]\n   while len(outv)<n:\n    x=heapq.heappop(h);outv.append(x)\n    for y in (2*x+1,3*x+1):\n     if y not in q:q.add(y);heapq.heappush(h,y)\n   out.append(str(outv[-1]))\n  return "\\n".join(out)+"\\n"\n if P==3744:\n  return "\\n".join(str(min(2*(x*y+x*w+y*w) for x in range(1,n+1) for y in range(x,n+1) if n%(x*y)==0 for w in [n//(x*y)])) for n in map(int,a[1:]))+"\\n"\n if P==3789:\n  n,k=map(int,a[:2]);v=list(map(int,a[2:]))\n  for L in range(n,0,-1):\n   if any(sum(v[i:i+L]==v[j:j+L] for j in range(n-L+1))>=k for i in range(n-L+1)):return str(L)+"\\n"\n if P==3791:\n  p=1;out=[]\n  for _ in range(int(a[0])):\n   n=int(a[p]);p+=1;q=sorted(a[p:p+n]);p+=n;out.append("NO" if any(y.startswith(x) for x,y in zip(q,q[1:])) else "YES")\n  return "\\n".join(out)+"\\n"\n if P==3906:\n  m,n=map(int,a[:2]);v=list(map(int,a[2:]));D={(0,0,0,0):v[0]}\n  for _ in range(m+n-2):\n   N={}\n   for (x,y,u,w),z in D.items():\n    for dx,dy in ((1,0),(0,1)):\n     for du,dw in ((1,0),(0,1)):\n      X,Y=x+dx,y+dy;U,W=u+du,w+dw\n      if X<m and Y<n and U<m and W<n and ((X,Y)!=(U,W) or (X,Y)==(m-1,n-1)):N[X,Y,U,W]=max(N.get((X,Y,U,W),-1),z+v[X*n+Y]+v[U*n+W])\n   D=N\n  return str(max(D.values()))+"\\n"\n if P==4001:\n  n,k=map(int,a);q=deque([(n,0)]);vis={n}\n  while q:\n   x,d=q.popleft()\n   if x==k:return str(d)+"\\n"\n   for y in (x-1,x+1,2*x):\n    if 0<=y<=100000 and y not in vis:vis.add(y);q.append((y,d+1))\n if P==4002:\n  v=list(map(int,a[2:]));return "".join((str(v.count(x)-1) if v.count(x)>1 else "BeiJu")+"\\n" for x in v)\n if P==4006:\n  q,n=map(int,a[:2]);out=[]\n  for i,j in zip(map(int,a[2::2]),map(int,a[3::2])):\n   l=min(i-1,j-1,n-i,n-j);z=n-2*l;st=n*n-z*z+1;u=i-l-1;v=j-l-1\n   out.append(str(st+v if u==0 else st+z-1+u if v==z-1 else st+2*z-2+z-1-v if u==z-1 else st+3*z-3+z-1-u))\n  return "\\n".join(out)+"\\n"\n if P==4007:\n  p=1;out=[]\n  for _ in range(int(a[0])):\n   x,y=a[p:p+2];p+=2;d=list(range(len(y)+1))\n   for c in x:\n    old=d;d=[old[0]+1]\n    for j in range(len(y)):d.append(min(old[j+1]+1,d[-1]+1,old[j]+(c!=y[j])))\n   out.append(str(d[-1]))\n  return "\\n".join(out)+"\\n"\n if P==4008:\n  n,k=map(int,a[:2]);d=[-10**9]*k;d[0]=0\n  for x in map(int,a[2:]):d=[max(d[j],d[(j-x)%k]+x) for j in range(k)]\n  return str(d[0])+"\\n"\n if P==4009:\n  pc=[bin(x).count("1") for x in range(65536)]\n  def pop(x):return pc[x&65535]+pc[x>>16]\n  out=[]\n  for n in map(int,a):\n   if not n:break\n   c=0\n   for mask in range(1<<n):\n    row=mask;z=2*pop(mask)-n\n    for width in range(n,1,-1):\n     row=(~(row^(row>>1)))&((1<<(width-1))-1);z+=2*pop(row)-(width-1)\n    c+=z==0\n   out.append(f"{n} {c}")\n  return "\\n".join(out)+"\\n"\n if P==4010:return "\\n".join(str(pow(2011,int(x),10000)) for x in a[1:])+"\\n"\n if P==4021:\n  p=1;out=[]\n  for _ in range(int(a[0])):\n   n=int(a[p]);v=list(map(int,a[p+1:p+1+n]));p+=n+1\n   z=[__import__("math").prod(v[:i]+v[i+1:]) for i in range(n)];out.append(str(v[z.index(max(z))]))\n  return "\\n".join(out)+"\\n"\n if P==4033:\n  n=int(a[0]);x,y=map(int,a[1+4*n:]);ans=-1\n  for i in range(n):\n   A,B,G,K=map(int,a[1+4*i:5+4*i])\n   if A<=x<=A+G and B<=y<=B+K:ans=i+1\n  return str(ans)+"\\n"\n if P==4034:\n  n,k,p=map(int,a[:3]);v=[tuple(map(int,a[i:i+2])) for i in range(3,3+2*n,2)]\n  return str(sum(v[i][0]==v[j][0] and min(x[1] for x in v[i:j+1])<=p for i in range(n) for j in range(i+1,n)))+"\\n"\nfor line in []:pass\nsys.stdout.write(go(sys.stdin.read()))\n'
SAMPLE_IN='4\n3\n0 1 2\n5\n2 3 5 4 8\n5\n-1 -2 -3 -4 -5\n4\n-1 -2 -3 -4\n'
LIM = 10 ** 7


def valid(text):
    """题面契约：第一行 M；之后每组两行：N（3<=N<=100），以及 N 个 [-1e7,1e7] 内的整数。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    try:
        if lines[0] != lines[0].strip() or len(lines[0].split()) != 1:
            return False
        m = int(lines[0])
        if m < 1 or len(lines) != 1 + 2 * m:
            return False
        for g in range(m):
            nl, vl = lines[1 + 2 * g], lines[2 + 2 * g]
            if len(nl.split()) != 1:
                return False
            n = int(nl)
            if not (3 <= n <= 100):
                return False
            v = vl.split(" ")
            if len(v) != n or any(not -LIM <= int(x) <= LIM for x in v):
                return False
    except ValueError:
        return False
    return True


def group(r, kind, n):
    big = r.random() < 0.5
    def val():
        x = r.randint(1, LIM if big else 9)
        return x if r.random() < 0.5 else -x
    v = [val() for _ in range(n)]
    if kind == "zero1":                       # 恰有一个 0
        v[r.randrange(n)] = 0
    elif kind == "zero2":                     # 两个及以上 0：乘积全为 0，取第一个
        for _ in range(r.randint(2, 3)):
            v[r.randrange(n)] = 0
    elif kind == "allneg":                    # 全负，奇偶个数都有
        v = [-abs(x) for x in v]
    elif kind == "allpos":
        v = [abs(x) for x in v]
    elif kind == "dup":                       # 重复值多，考查“最先输入”
        pool = [val() for _ in range(3)]
        v = [r.choice(pool) for _ in range(n)]
        if r.random() < 0.3:
            v[r.randrange(n)] = 0
    elif kind == "extreme":                   # 绝对值顶到 1e7，乘积远超 64 位
        v = [r.choice([LIM, -LIM, LIM - 1, -(LIM - 1), 1, -1]) for _ in range(n)]
    elif kind == "oneneg":                    # 只有一个负数（含/不含 0）
        v = [abs(x) for x in v]
        v[r.randrange(n)] = -abs(val())
        if r.random() < 0.5:
            v[r.randrange(n)] = 0
    return v


KINDS = ["rand", "zero1", "zero2", "allneg", "allpos", "dup", "extreme", "oneneg"]


def gen(i):
    r = random.Random(4021 * 1000 + i)
    if i == 0:
        return SAMPLE_IN
    if i <= 8:
        # 每种形态各一组文件，N=3 的最小规模与小规模混合
        m = 30
        gs = [group(r, KINDS[i - 1], r.choice([3, 3, 4, 5, r.randint(3, 10)])) for _ in range(m)]
    elif i <= 20:
        m = r.randint(20, 60)
        gs = [group(r, r.choice(KINDS), r.randint(3, 100)) for _ in range(m)]
    elif i <= 32:
        m = r.randint(80, 150)
        gs = [group(r, r.choice(KINDS), r.choice([100, r.randint(90, 100)])) for _ in range(m)]
    else:
        # 满规模：N=100，值域顶满
        m = 200
        gs = [group(r, r.choice(KINDS), 100) for _ in range(m)]
    out = [str(len(gs))]
    for v in gs:
        out.append(str(len(v)))
        out.append(" ".join(map(str, v)))
    return "\n".join(out) + "\n"


def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as h:
        h.write(REFERENCE_SOURCE)
        h.flush()
        root = Path(__file__).parent / "data"
        for i in range(40):
            c = gen(i)
            assert valid(c), i
            p = subprocess.run(["python3", h.name], input=c, text=True, capture_output=True, check=True)
            (root / f"{i}.in").write_text(c, encoding="utf-8")
            (root / f"{i}.out").write_text(p.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
