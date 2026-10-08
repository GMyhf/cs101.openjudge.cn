import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys, heapq\nfrom collections import deque\nP=3789\ndef go(s):\n a=s.split()\n if P==3723:\n  n=int(a[0]);g=a[1:];seen=set();z=[sum(row.count("B") for row in g),sum(row.count("W") for row in g)]\n  for i in range(n):\n   for j in range(n):\n    if g[i][j]!="." or (i,j) in seen:continue\n    q=[(i,j)];seen.add((i,j));e=set();c=0\n    while q:\n     x,y=q.pop();c+=1\n     for u,v in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):\n      if 0<=u<n and 0<=v<n:\n       if g[u][v]=="." and (u,v) not in seen:seen.add((u,v));q.append((u,v))\n       elif g[u][v] in "BW":e.add(g[u][v])\n    if len(e)==1:z["BW".index(next(iter(e)))]+=c\n  return f"{z[0]} {z[1]}\\n"\n if P==3725:\n  x=list(map(int,a));v=sorted(x[1:],reverse=True);M=max(v);best=(10**9,0)\n  for k in range(1,len(v)+1):\n   q=[0]*k\n   for y in v:q[q.index(min(q))]+=y\n   best=min(best,(sum(abs(y-M) for y in q),-k))\n  return f"{-best[1]}\\n"\n if P==3726 or P==3866:\n  p=0;out=[]\n  while p<len(a):\n   R,C=map(int,a[p:p+2]);p+=2\n   if not R:break\n   g=a[p:p+(R if P==3726 else C)];p+=len(g)\n   target="*" if P==3726 else "@"; src=next((i,j) for i in range(len(g)) for j in range(len(g[0]) if g else 0) if g[i][j]==target)\n   q=deque([src]);seen={src}\n   while q:\n    x,y=q.popleft()\n    for u,v in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):\n     if 0<=u<len(g) and 0<=v<len(g[0]) and g[u][v]!="#" and (u,v) not in seen:seen.add((u,v));q.append((u,v))\n   if P==3726:\n    start=next((i,j) for i in range(R) for j in range(C) if g[i][j]=="@");q=deque([(start[0],start[1],0)]);vis={start};ans=-1\n    while q:\n     x,y,d=q.popleft()\n     if g[x][y]=="*":ans=d;break\n     for u,v in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):\n      if 0<=u<R and 0<=v<C and g[u][v]!="#" and (u,v) not in vis:vis.add((u,v));q.append((u,v,d+1))\n    out.append(str(ans))\n   else:out.append(str(len(seen)))\n  return "\\n".join(out)+"\\n"\n if P==3727:\n  p=1;out=[]\n  for _ in range(int(a[0])):\n   R,C=map(int,a[p:p+2]);p+=2;d=[0]*C\n   for i in range(R):\n    for j in range(C):d[j]=max(d[j],d[j-1] if j else 0)+int(a[p]);p+=1\n   out.append(str(d[-1]))\n  return "\\n".join(out)+"\\n"\n if P==3728:\n  out=[]\n  for line in s.splitlines():\n   b,n=map(int,line.split());v=[b];i2=i3=0\n   while len(v)<n:\n    x=min(2*v[i2]+1,3*v[i3]+1);v.append(x)\n    while 2*v[i2]+1<=x:i2+=1\n    while 3*v[i3]+1<=x:i3+=1\n   out.append(str(v[-1]))\n  return "\\n".join(out)+"\\n"\n if P==3744:\n  return "\\n".join(str(min(2*(x*y+x*w+y*w) for x in range(1,n+1) for y in range(x,n+1) if n%(x*y)==0 for w in [n//(x*y)])) for n in map(int,a[1:]))+"\\n"\n if P==3789:\n  n,k=map(int,a[:2]);v=list(map(int,a[2:]));sa=list(range(n));rank=v[:];step=1\n  while step<n:\n   sa.sort(key=lambda i:(rank[i],rank[i+step] if i+step<n else -1));nr=[0]*n\n   for j in range(1,n):nr[sa[j]]=nr[sa[j-1]]+((rank[sa[j-1]],rank[sa[j-1]+step] if sa[j-1]+step<n else -1)<(rank[sa[j]],rank[sa[j]+step] if sa[j]+step<n else -1))\n   rank=nr;step*=2\n  pos=[0]*n\n  for i,x in enumerate(sa):pos[x]=i\n  lcp=[0]*n;h=0\n  for i in range(n):\n   p=pos[i]\n   if p==0:continue\n   j=sa[p-1]\n   while i+h<n and j+h<n and v[i+h]==v[j+h]:h+=1\n   lcp[p]=h\n   if h:h-=1\n  best=0\n  for i in range(n-k+1):\n   best=max(best,min(lcp[i+1:i+k]))\n  return str(best)+"\\n"\n if P==3791:\n  p=1;out=[]\n  for _ in range(int(a[0])):\n   n=int(a[p]);p+=1;q=sorted(a[p:p+n]);p+=n;out.append("NO" if any(y.startswith(x) for x,y in zip(q,q[1:])) else "YES")\n  return "\\n".join(out)+"\\n"\n if P==3906:\n  m,n=map(int,a[:2]);v=list(map(int,a[2:]));D={(0,0,0,0):v[0]}\n  for _ in range(m+n-2):\n   N={}\n   for (x,y,u,w),z in D.items():\n    for dx,dy in ((1,0),(0,1)):\n     for du,dw in ((1,0),(0,1)):\n      X,Y=x+dx,y+dy;U,W=u+du,w+dw\n      if X<m and Y<n and U<m and W<n and ((X,Y)!=(U,W) or (X,Y)==(m-1,n-1)):N[X,Y,U,W]=max(N.get((X,Y,U,W),-1),z+v[X*n+Y]+v[U*n+W])\n   D=N\n  return str(max(D.values()))+"\\n"\n if P==4001:\n  n,k=map(int,a);q=deque([(n,0)]);vis={n}\n  while q:\n   x,d=q.popleft()\n   if x==k:return str(d)+"\\n"\n   for y in (x-1,x+1,2*x):\n    if 0<=y<=100000 and y not in vis:vis.add(y);q.append((y,d+1))\n if P==4002:\n  v=list(map(int,a[2:]));return "".join((str(v.count(x)-1) if v.count(x)>1 else "BeiJu")+"\\n" for x in v)\n if P==4006:\n  q,n=map(int,a[:2]);out=[]\n  for i,j in zip(map(int,a[2::2]),map(int,a[3::2])):\n   l=min(i-1,j-1,n-i,n-j);z=n-2*l;st=n*n-z*z+1;u=i-l-1;v=j-l-1\n   out.append(str(st+v if u==0 else st+z-1+u if v==z-1 else st+2*z-2+z-1-v if u==z-1 else st+3*z-3+z-1-u))\n  return "\\n".join(out)+"\\n"\n if P==4007:\n  p=1;out=[]\n  for _ in range(int(a[0])):\n   x,y=a[p:p+2];p+=2;d=list(range(len(y)+1))\n   for c in x:\n    old=d;d=[old[0]+1]\n    for j in range(len(y)):d.append(min(old[j+1]+1,d[-1]+1,old[j]+(c!=y[j])))\n   out.append(str(d[-1]))\n  return "\\n".join(out)+"\\n"\n if P==4008:\n  n,k=map(int,a[:2]);d=[-10**9]*k;d[0]=0\n  for x in map(int,a[2:]):d=[max(d[j],d[(j-x)%k]+x) for j in range(k)]\n  return str(d[0])+"\\n"\n if P==4009:\n  pc=[bin(x).count("1") for x in range(65536)]\n  def pop(x):return pc[x&65535]+pc[x>>16]\n  out=[]\n  for n in map(int,a):\n   if not n:break\n   c=0\n   for mask in range(1<<n):\n    row=mask;z=2*pop(mask)-n\n    for width in range(n,1,-1):\n     row=(~(row^(row>>1)))&((1<<(width-1))-1);z+=2*pop(row)-(width-1)\n    c+=z==0\n   out.append(f"{n} {c}")\n  return "\\n".join(out)+"\\n"\n if P==4010:return "\\n".join(str(pow(2011,int(x),10000)) for x in a[1:])+"\\n"\n if P==4021:\n  p=1;out=[]\n  for _ in range(int(a[0])):\n   n=int(a[p]);v=list(map(int,a[p+1:p+1+n]));p+=n+1\n   z=[__import__("math").prod(v[:i]+v[i+1:]) for i in range(n)];out.append(str(v[z.index(max(z))]))\n  return "\\n".join(out)+"\\n"\n if P==4033:\n  n=int(a[0]);x,y=map(int,a[1+4*n:]);ans=-1\n  for i in range(n):\n   A,B,G,K=map(int,a[1+4*i:5+4*i])\n   if A<=x<=A+G and B<=y<=B+K:ans=i+1\n  return str(ans)+"\\n"\n if P==4034:\n  n,k,p=map(int,a[:3]);v=[tuple(map(int,a[i:i+2])) for i in range(3,3+2*n,2)];ans=0\n  for i in range(n):\n   low=10**18\n   for j in range(i+1,n):\n    low=min(low,v[j-1][1])\n    if v[i][0]==v[j][0] and min(low,v[j][1])<=p:ans+=1\n  return str(ans)+"\\n"\nfor line in []:pass\nsys.stdout.write(go(sys.stdin.read()))\n'
SAMPLE_IN='8 2\n1\n2\n3\n2\n3\n2\n3\n1\n'
from collections import Counter

def valid(text):
    """题面契约：第1行 N K；其后 N 行各一个整数；1<=N<=20000，2<=K<=N，
    每个值 0..1000000；保证至少有一个子序列重复至少 K 次（即某个值出现 >=K 次）。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    head = lines[0].split(" ")
    if len(head) != 2 or not all(t.isdigit() for t in head):
        return False
    n, k = map(int, head)
    if not (1 <= n <= 20000 and 2 <= k <= n) or len(lines) != n + 1:
        return False
    v = []
    for s in lines[1:]:
        if not s.isdigit() or (len(s) > 1 and s[0] == "0"):
            return False
        x = int(s)
        if not 0 <= x <= 1000000:
            return False
        v.append(x)
    return max(Counter(v).values()) >= k

def fmt(v, k):
    return f"{len(v)} {k}\n" + "\n".join(map(str, v)) + "\n"

def g_small(r):
    # 原有小规模随机构造：n<=14，模式重复 k 次后补随机值
    n = r.randint(2, 14); k = r.randint(2, n); L = r.randint(1, max(1, n // k))
    hi = r.choice([1, 5, 1000000])
    pat = [r.randint(0, hi) for _ in range(L)]; v = (pat * k)[:n]
    while len(v) < n: v.append(r.randint(0, hi))
    return fmt(v, k)

def planted(r, n, k, L, hi):
    # 随机大值序列里不重叠地植入 k 份长度 L 的模式
    v = [r.randint(0, hi) for _ in range(n)]
    pat = [r.randint(0, hi) for _ in range(L)]
    slots = sorted(r.sample(range(n // L), k))
    for s in slots:
        v[s * L:(s + 1) * L] = pat
    return v

def fib_word(n):
    a, b = [0], [0, 1]
    while len(b) < n: a, b = b, b + a
    return b[:n]

def thue_morse(n):
    return [bin(i).count("1") & 1 for i in range(n)]

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 14):
        for j in range(100):
            c = g_small(random.Random(3789 + i + j * 1000))
            if c not in cases: break
        cases.append(c)
    r = random.Random(37890)
    N = 20000
    # 中等规模
    cases.append(fmt(planted(r, 500, 3, 40, 1000000), 3))
    cases.append(fmt([r.randint(0, 1) for _ in range(2000)], 7))
    cases.append(fmt([r.randint(0, 3) for _ in range(3000)], 2))
    cases.append(fmt([1000000, 0] * 1000, 2))           # 周期 2：答案 n-2
    # 满规模
    cases.append(fmt([7] * N, N))                         # K=N，全同：答案 1
    cases.append(fmt([1000000] * N, 2))                   # 全同 K=2：答案 N-1
    cases.append(fmt([5] * N, 12345))                     # 全同：答案 N-K+1
    cases.append(fmt([r.randint(0, 1000000) for _ in range(N - 1)] + [0], 2))  # 随机大值，答案多为 1
    cases.append(fmt(planted(r, N, 2, 3000, 1000000), 2))
    cases.append(fmt(planted(r, N, 5, 1500, 1000000), 5))
    cases.append(fmt(planted(r, N, 100, 150, 1000000), 100))
    cases.append(fmt(planted(r, N, 2, 9000, 1000000), 2))
    cases.append(fmt([r.randint(0, 1) for _ in range(N)], 2))
    cases.append(fmt([r.randint(0, 1) for _ in range(N)], 50))
    cases.append(fmt([r.randint(0, 1) for _ in range(N)], 5000))
    cases.append(fmt([r.randint(0, 2) for _ in range(N)], 1000))
    cases.append(fmt([x * 999999 for x in fib_word(N)], 2))
    cases.append(fmt(fib_word(N), 300))
    cases.append(fmt(thue_morse(N), 3))
    cases.append(fmt(thue_morse(N), 64))
    per = [r.randint(0, 1000000) for _ in range(137)]
    cases.append(fmt((per * (N // 137 + 1))[:N], 10))      # 周期 137
    cases.append(fmt((per[:7] * (N // 7 + 1))[:N], 2800))   # 周期 7，大 K
    v = [r.randint(0, 1000000) for _ in range(N)]
    for x in range(0, N, 2): v[x] = 1                      # 偶数位全 1、K 接近出现次数
    cases.append(fmt(v, 9999))
    v = [r.randint(0, 9) for _ in range(N)]
    cases.append(fmt(v, 2))
    v = [r.randint(10, 12) for _ in range(N)]
    cases.append(fmt(v, 20))
    v = [1, 2, 3] * 6666 + [1, 2]
    cases.append(fmt(v, 6667))                              # 周期 3：答案 2
    return cases

def main():
    cases = build_cases()
    assert len(cases) == 40 and len(set(cases)) == 40
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as h:
        h.write(REFERENCE_SOURCE); h.flush(); root = Path(__file__).parent / "data"
        for i, c in enumerate(cases):
            assert valid(c), i
            p = subprocess.run(["python3", h.name], input=c, text=True, capture_output=True, check=True)
            (root / f"{i}.in").write_text(c, encoding="utf-8"); (root / f"{i}.out").write_text(p.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()
