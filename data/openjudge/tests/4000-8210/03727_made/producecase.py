import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys, heapq\nfrom collections import deque\nP=3727\ndef go(s):\n a=s.split()\n if P==3723:\n  n=int(a[0]);g=a[1:];seen=set();z=[sum(row.count("B") for row in g),sum(row.count("W") for row in g)]\n  for i in range(n):\n   for j in range(n):\n    if g[i][j]!="." or (i,j) in seen:continue\n    q=[(i,j)];seen.add((i,j));e=set();c=0\n    while q:\n     x,y=q.pop();c+=1\n     for u,v in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):\n      if 0<=u<n and 0<=v<n:\n       if g[u][v]=="." and (u,v) not in seen:seen.add((u,v));q.append((u,v))\n       elif g[u][v] in "BW":e.add(g[u][v])\n    if len(e)==1:z["BW".index(next(iter(e)))]+=c\n  return f"{z[0]} {z[1]}\\n"\n if P==3725:\n  x=list(map(int,a));v=sorted(x[1:],reverse=True);M=max(v);best=(10**9,0)\n  for k in range(1,len(v)+1):\n   q=[0]*k\n   for y in v:q[q.index(min(q))]+=y\n   best=min(best,(sum(abs(y-M) for y in q),-k))\n  return f"{-best[1]}\\n"\n if P==3726 or P==3866:\n  p=0;out=[]\n  while p<len(a):\n   R,C=map(int,a[p:p+2]);p+=2\n   if not R:break\n   g=a[p:p+(R if P==3726 else C)];p+=len(g)\n   target="*" if P==3726 else "@"; src=next((i,j) for i in range(len(g)) for j in range(len(g[0]) if g else 0) if g[i][j]==target)\n   q=deque([src]);seen={src}\n   while q:\n    x,y=q.popleft()\n    for u,v in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):\n     if 0<=u<len(g) and 0<=v<len(g[0]) and g[u][v]!="#" and (u,v) not in seen:seen.add((u,v));q.append((u,v))\n   if P==3726:\n    start=next((i,j) for i in range(R) for j in range(C) if g[i][j]=="@");q=deque([(start[0],start[1],0)]);vis={start};ans=-1\n    while q:\n     x,y,d=q.popleft()\n     if g[x][y]=="*":ans=d;break\n     for u,v in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):\n      if 0<=u<R and 0<=v<C and g[u][v]!="#" and (u,v) not in vis:vis.add((u,v));q.append((u,v,d+1))\n    out.append(str(ans))\n   else:out.append(str(len(seen)))\n  return "\\n".join(out)+"\\n"\n if P==3727:\n  p=1;out=[]\n  for _ in range(int(a[0])):\n   R,C=map(int,a[p:p+2]);p+=2;d=[0]*C\n   for i in range(R):\n    for j in range(C):d[j]=max(d[j],d[j-1] if j else 0)+int(a[p]);p+=1\n   out.append(str(d[-1]))\n  return "\\n".join(out)+"\\n"\n if P==3728:\n  out=[]\n  for line in s.splitlines():\n   b,n=map(int,line.split());q={b};h=[b];outv=[]\n   while len(outv)<n:\n    x=heapq.heappop(h);outv.append(x)\n    for y in (2*x+1,3*x+1):\n     if y not in q:q.add(y);heapq.heappush(h,y)\n   out.append(str(outv[-1]))\n  return "\\n".join(out)+"\\n"\n if P==3744:\n  return "\\n".join(str(min(2*(x*y+x*w+y*w) for x in range(1,n+1) for y in range(x,n+1) if n%(x*y)==0 for w in [n//(x*y)])) for n in map(int,a[1:]))+"\\n"\n if P==3789:\n  n,k=map(int,a[:2]);v=list(map(int,a[2:]))\n  for L in range(n,0,-1):\n   if any(sum(v[i:i+L]==v[j:j+L] for j in range(n-L+1))>=k for i in range(n-L+1)):return str(L)+"\\n"\n if P==3791:\n  p=1;out=[]\n  for _ in range(int(a[0])):\n   n=int(a[p]);p+=1;q=sorted(a[p:p+n]);p+=n;out.append("NO" if any(y.startswith(x) for x,y in zip(q,q[1:])) else "YES")\n  return "\\n".join(out)+"\\n"\n if P==3906:\n  m,n=map(int,a[:2]);v=list(map(int,a[2:]));D={(0,0,0,0):v[0]}\n  for _ in range(m+n-2):\n   N={}\n   for (x,y,u,w),z in D.items():\n    for dx,dy in ((1,0),(0,1)):\n     for du,dw in ((1,0),(0,1)):\n      X,Y=x+dx,y+dy;U,W=u+du,w+dw\n      if X<m and Y<n and U<m and W<n and ((X,Y)!=(U,W) or (X,Y)==(m-1,n-1)):N[X,Y,U,W]=max(N.get((X,Y,U,W),-1),z+v[X*n+Y]+v[U*n+W])\n   D=N\n  return str(max(D.values()))+"\\n"\n if P==4001:\n  n,k=map(int,a);q=deque([(n,0)]);vis={n}\n  while q:\n   x,d=q.popleft()\n   if x==k:return str(d)+"\\n"\n   for y in (x-1,x+1,2*x):\n    if 0<=y<=100000 and y not in vis:vis.add(y);q.append((y,d+1))\n if P==4002:\n  v=list(map(int,a[2:]));return "".join((str(v.count(x)-1) if v.count(x)>1 else "BeiJu")+"\\n" for x in v)\n if P==4006:\n  q,n=map(int,a[:2]);out=[]\n  for i,j in zip(map(int,a[2::2]),map(int,a[3::2])):\n   l=min(i-1,j-1,n-i,n-j);z=n-2*l;st=n*n-z*z+1;u=i-l-1;v=j-l-1\n   out.append(str(st+v if u==0 else st+z-1+u if v==z-1 else st+2*z-2+z-1-v if u==z-1 else st+3*z-3+z-1-u))\n  return "\\n".join(out)+"\\n"\n if P==4007:\n  p=1;out=[]\n  for _ in range(int(a[0])):\n   x,y=a[p:p+2];p+=2;d=list(range(len(y)+1))\n   for c in x:\n    old=d;d=[old[0]+1]\n    for j in range(len(y)):d.append(min(old[j+1]+1,d[-1]+1,old[j]+(c!=y[j])))\n   out.append(str(d[-1]))\n  return "\\n".join(out)+"\\n"\n if P==4008:\n  n,k=map(int,a[:2]);d=[-10**9]*k;d[0]=0\n  for x in map(int,a[2:]):d=[max(d[j],d[(j-x)%k]+x) for j in range(k)]\n  return str(d[0])+"\\n"\n if P==4009:\n  pc=[bin(x).count("1") for x in range(65536)]\n  def pop(x):return pc[x&65535]+pc[x>>16]\n  out=[]\n  for n in map(int,a):\n   if not n:break\n   c=0\n   for mask in range(1<<n):\n    row=mask;z=2*pop(mask)-n\n    for width in range(n,1,-1):\n     row=(~(row^(row>>1)))&((1<<(width-1))-1);z+=2*pop(row)-(width-1)\n    c+=z==0\n   out.append(f"{n} {c}")\n  return "\\n".join(out)+"\\n"\n if P==4010:return "\\n".join(str(pow(2011,int(x),10000)) for x in a[1:])+"\\n"\n if P==4021:\n  p=1;out=[]\n  for _ in range(int(a[0])):\n   n=int(a[p]);v=list(map(int,a[p+1:p+1+n]));p+=n+1\n   z=[__import__("math").prod(v[:i]+v[i+1:]) for i in range(n)];out.append(str(v[z.index(max(z))]))\n  return "\\n".join(out)+"\\n"\n if P==4033:\n  n=int(a[0]);x,y=map(int,a[1+4*n:]);ans=-1\n  for i in range(n):\n   A,B,G,K=map(int,a[1+4*i:5+4*i])\n   if A<=x<=A+G and B<=y<=B+K:ans=i+1\n  return str(ans)+"\\n"\n if P==4034:\n  n,k,p=map(int,a[:3]);v=[tuple(map(int,a[i:i+2])) for i in range(3,3+2*n,2)]\n  return str(sum(v[i][0]==v[j][0] and min(x[1] for x in v[i:j+1])<=p for i in range(n) for j in range(i+1,n)))+"\\n"\nfor line in []:pass\nsys.stdout.write(go(sys.stdin.read()))\n'
SAMPLE_IN='2\n2 2\n1 1\n3 4\n2 3\n2 3 4\n1 6 5\n'


def valid(text):
    """题面：首行 T（1<=T<=100）；每组首行 R C（1<=R,C<=100），接着 R 行每行 C 个整数 M（0<=M<=1000）。"""
    if not text.endswith("\n"):
        return False
    lines=text[:-1].split("\n")

    def ints(line,k):
        t=line.split()
        if len(t)!=k or not all(x.isdigit() for x in t):
            return None
        return [int(x) for x in t]

    head=ints(lines[0],1)
    if head is None or not 1<=head[0]<=100:
        return False
    p=1
    for _ in range(head[0]):
        if p>=len(lines):
            return False
        rc=ints(lines[p],2);p+=1
        if rc is None or not (1<=rc[0]<=100 and 1<=rc[1]<=100):
            return False
        if p+rc[0]>len(lines):
            return False
        for i in range(rc[0]):
            row=ints(lines[p+i],rc[1])
            if row is None or any(x>1000 for x in row):
                return False
        p+=rc[0]
    return p==len(lines)


def grid(R,C,r,lo=0,hi=1000):
    return [[r.randint(lo,hi) for _ in range(C)] for _ in range(R)]


def trap(r):
    """贪心（每步走较大的邻格）会走错的构造：起点下方 6 > 右方 5，贪心向南走进全 0 区，
    最优解却是先向东沿第 0 行拿走一排 1000。"""
    R,C=r.randint(3,10),r.randint(3,10)
    g=[[0]*C for _ in range(R)]
    g[1][0]=6;g[0][1]=5
    for j in range(2,C): g[0][j]=1000
    return g


def case_text(g):
    return f"{len(g)} {len(g[0])}\n"+"".join(" ".join(map(str,row))+"\n" for row in g)


def g3727(index,r):
    if index==1: cases=[[[0]]]
    elif index==2: cases=[[[1000]]]
    elif index==3: cases=[[[1000]*100 for _ in range(100)]]
    elif index==4: cases=[grid(100,100,r) for _ in range(10)]
    elif index==5: cases=[grid(100,100,r) for _ in range(18)]
    elif index==6: cases=[grid(100,100,r,900,1000) for _ in range(15)]
    elif index==7: cases=[grid(r.randint(1,20),r.randint(1,20),r) for _ in range(100)]
    elif index==8: cases=[grid(1,r.randint(1,100),r) if r.random()<0.5 else grid(r.randint(1,100),1,r) for _ in range(100)]
    elif index==9: cases=[trap(r) for _ in range(30)]
    elif index==10: cases=[grid(100,100,r,0,0),grid(1,100,r),grid(100,1,r)]
    else:
        cases=[];budget=180000
        for _ in range(r.randint(1,100)):
            R,C=r.randint(1,100),r.randint(1,100)
            if r.random()<0.6: R,C=max(1,R//5),max(1,C//5)
            if R*C>budget: break
            budget-=R*C
            cases.append(trap(r) if r.random()<0.1 else grid(R,C,r,0,r.choice([0,1,20,1000])))
        if not cases: cases=[grid(2,2,r)]
    return f"{len(cases)}\n"+"".join(case_text(g) for g in cases)


def main():
    with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as h:
        h.write(REFERENCE_SOURCE);h.flush();root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
        for i in range(40):
            if i==0:c=SAMPLE_IN
            else:
                for j in range(100):
                    c=g3727(i,random.Random(3727+i+j*1000))
                    if c not in seen:break
                else:raise AssertionError("diversity")
                seen.append(c)
            assert valid(c),i
            p=subprocess.run(["python3",h.name],input=c,text=True,capture_output=True,check=True)
            (root/f"{i}.in").write_text(c,encoding="utf-8");(root/f"{i}.out").write_text(p.stdout,encoding="utf-8")


if __name__=="__main__":
    main()
