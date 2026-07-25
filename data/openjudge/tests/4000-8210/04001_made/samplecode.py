# T-004-r4
import sys, heapq
from collections import deque
P=4001
def go(s):
 a=s.split()
 if P==3723:
  n=int(a[0]);g=a[1:];seen=set();z=[sum(row.count("B") for row in g),sum(row.count("W") for row in g)]
  for i in range(n):
   for j in range(n):
    if g[i][j]!="." or (i,j) in seen:continue
    q=[(i,j)];seen.add((i,j));e=set();c=0
    while q:
     x,y=q.pop();c+=1
     for u,v in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
      if 0<=u<n and 0<=v<n:
       if g[u][v]=="." and (u,v) not in seen:seen.add((u,v));q.append((u,v))
       elif g[u][v] in "BW":e.add(g[u][v])
    if len(e)==1:z["BW".index(next(iter(e)))]+=c
  return f"{z[0]} {z[1]}\n"
 if P==3725:
  x=list(map(int,a));v=sorted(x[1:],reverse=True);M=max(v);best=(10**9,0)
  for k in range(1,len(v)+1):
   q=[0]*k
   for y in v:q[q.index(min(q))]+=y
   best=min(best,(sum(abs(y-M) for y in q),-k))
  return f"{-best[1]}\n"
 if P==3726 or P==3866:
  p=0;out=[]
  while p<len(a):
   R,C=map(int,a[p:p+2]);p+=2
   if not R:break
   g=a[p:p+(R if P==3726 else C)];p+=len(g)
   target="*" if P==3726 else "@"; src=next((i,j) for i in range(len(g)) for j in range(len(g[0]) if g else 0) if g[i][j]==target)
   q=deque([src]);seen={src}
   while q:
    x,y=q.popleft()
    for u,v in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
     if 0<=u<len(g) and 0<=v<len(g[0]) and g[u][v]!="#" and (u,v) not in seen:seen.add((u,v));q.append((u,v))
   if P==3726:
    start=next((i,j) for i in range(R) for j in range(C) if g[i][j]=="@");q=deque([(start[0],start[1],0)]);vis={start};ans=-1
    while q:
     x,y,d=q.popleft()
     if g[x][y]=="*":ans=d;break
     for u,v in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
      if 0<=u<R and 0<=v<C and g[u][v]!="#" and (u,v) not in vis:vis.add((u,v));q.append((u,v,d+1))
    out.append(str(ans))
   else:out.append(str(len(seen)))
  return "\n".join(out)+"\n"
 if P==3727:
  p=1;out=[]
  for _ in range(int(a[0])):
   R,C=map(int,a[p:p+2]);p+=2;d=[0]*C
   for i in range(R):
    for j in range(C):d[j]=max(d[j],d[j-1] if j else 0)+int(a[p]);p+=1
   out.append(str(d[-1]))
  return "\n".join(out)+"\n"
 if P==3728:
  out=[]
  for line in s.splitlines():
   b,n=map(int,line.split());q={b};h=[b];outv=[]
   while len(outv)<n:
    x=heapq.heappop(h);outv.append(x)
    for y in (2*x+1,3*x+1):
     if y not in q:q.add(y);heapq.heappush(h,y)
   out.append(str(outv[-1]))
  return "\n".join(out)+"\n"
 if P==3744:
  return "\n".join(str(min(2*(x*y+x*w+y*w) for x in range(1,n+1) for y in range(x,n+1) if n%(x*y)==0 for w in [n//(x*y)])) for n in map(int,a[1:]))+"\n"
 if P==3789:
  n,k=map(int,a[:2]);v=list(map(int,a[2:]))
  for L in range(n,0,-1):
   if any(sum(v[i:i+L]==v[j:j+L] for j in range(n-L+1))>=k for i in range(n-L+1)):return str(L)+"\n"
 if P==3791:
  p=1;out=[]
  for _ in range(int(a[0])):
   n=int(a[p]);p+=1;q=sorted(a[p:p+n]);p+=n;out.append("NO" if any(y.startswith(x) for x,y in zip(q,q[1:])) else "YES")
  return "\n".join(out)+"\n"
 if P==3906:
  m,n=map(int,a[:2]);v=list(map(int,a[2:]));D={(0,0,0,0):v[0]}
  for _ in range(m+n-2):
   N={}
   for (x,y,u,w),z in D.items():
    for dx,dy in ((1,0),(0,1)):
     for du,dw in ((1,0),(0,1)):
      X,Y=x+dx,y+dy;U,W=u+du,w+dw
      if X<m and Y<n and U<m and W<n and ((X,Y)!=(U,W) or (X,Y)==(m-1,n-1)):N[X,Y,U,W]=max(N.get((X,Y,U,W),-1),z+v[X*n+Y]+v[U*n+W])
   D=N
  return str(max(D.values()))+"\n"
 if P==4001:
  n,k=map(int,a);q=deque([(n,0)]);vis={n}
  while q:
   x,d=q.popleft()
   if x==k:return str(d)+"\n"
   for y in (x-1,x+1,2*x):
    if 0<=y<=100000 and y not in vis:vis.add(y);q.append((y,d+1))
 if P==4002:
  v=list(map(int,a[2:]));return "".join((str(v.count(x)-1) if v.count(x)>1 else "BeiJu")+"\n" for x in v)
 if P==4006:
  q,n=map(int,a[:2]);out=[]
  for i,j in zip(map(int,a[2::2]),map(int,a[3::2])):
   l=min(i-1,j-1,n-i,n-j);z=n-2*l;st=n*n-z*z+1;u=i-l-1;v=j-l-1
   out.append(str(st+v if u==0 else st+z-1+u if v==z-1 else st+2*z-2+z-1-v if u==z-1 else st+3*z-3+z-1-u))
  return "\n".join(out)+"\n"
 if P==4007:
  p=1;out=[]
  for _ in range(int(a[0])):
   x,y=a[p:p+2];p+=2;d=list(range(len(y)+1))
   for c in x:
    old=d;d=[old[0]+1]
    for j in range(len(y)):d.append(min(old[j+1]+1,d[-1]+1,old[j]+(c!=y[j])))
   out.append(str(d[-1]))
  return "\n".join(out)+"\n"
 if P==4008:
  n,k=map(int,a[:2]);d=[-10**9]*k;d[0]=0
  for x in map(int,a[2:]):d=[max(d[j],d[(j-x)%k]+x) for j in range(k)]
  return str(d[0])+"\n"
 if P==4009:
  out=[]
  for n in map(int,a):
   if not n:break
   c=0
   for mask in range(1<<n):
    row=mask;z=2*bin(mask).count("1")-n
    for width in range(n,1,-1):
     row=(~(row^(row>>1)))&((1<<(width-1))-1);z+=2*bin(row).count("1")-(width-1)
    c+=z==0
   out.append(f"{n} {c}")
  return "\n".join(out)+"\n"
 if P==4010:return "\n".join(str(pow(2011,int(x),10000)) for x in a[1:])+"\n"
 if P==4021:
  p=1;out=[]
  for _ in range(int(a[0])):
   n=int(a[p]);v=list(map(int,a[p+1:p+1+n]));p+=n+1
   z=[__import__("math").prod(v[:i]+v[i+1:]) for i in range(n)];out.append(str(v[z.index(max(z))]))
  return "\n".join(out)+"\n"
 if P==4033:
  n=int(a[0]);x,y=map(int,a[1+4*n:]);ans=-1
  for i in range(n):
   A,B,G,K=map(int,a[1+4*i:5+4*i])
   if A<=x<=A+G and B<=y<=B+K:ans=i+1
  return str(ans)+"\n"
 if P==4034:
  n,k,p=map(int,a[:3]);v=[tuple(map(int,a[i:i+2])) for i in range(3,3+2*n,2)]
  return str(sum(v[i][0]==v[j][0] and min(x[1] for x in v[i:j+1])<=p for i in range(n) for j in range(i+1,n)))+"\n"
for line in []:pass
sys.stdout.write(go(sys.stdin.read()))
