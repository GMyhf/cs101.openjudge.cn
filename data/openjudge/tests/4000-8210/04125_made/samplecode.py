# T-004-r6

import sys,math,re
from collections import deque
P=4125
def r4087(a):
 n,k=a[:2];print(sorted(a[2:2+n])[k-1])
def r4088(a):
 n=a[0];A=set(a[1:n+1]);m=a[n+1];B=set(a[n+2:n+2+m]);print(*sorted(A^B))
def r4090(t):
 a=t.split();i=0;n=int(a[i]);i+=1;v=list(map(int,a[i:i+n]));i+=n;q=int(a[i]);i+=1;o=[]
 for _ in range(q):
  z=a[i];i+=1
  if z=="ADD":x,y,d=map(int,a[i:i+3]);i+=3;v[x-1:y]=[q+d for q in v[x-1:y]]
  elif z=="REVERSE":x,y=map(int,a[i:i+2]);i+=2;v[x-1:y]=v[x-1:y][::-1]
  elif z=="REVOLVE":x,y,k=map(int,a[i:i+3]);i+=3;w=v[x-1:y];k%=len(w);v[x-1:y]=w[-k:]+w[:-k] if k else w
  elif z=="INSERT":x,d=map(int,a[i:i+2]);i+=2;v.insert(x,d)
  elif z=="DELETE":x=int(a[i]);i+=1;v.pop(x-1)
  else:x,y=map(int,a[i:i+2]);i+=2;o.append(str(min(v[x-1:y])))
 print("\n".join(o))
def r4091(a):
 i=0;o=[]
 while i<len(a):
  n,k=a[i:i+2];i+=2;p=[tuple(a[i+j*k:i+(j+1)*k]) for j in range(n)];i+=n*k;q=a[i];i+=1
  for _ in range(q):
   x=tuple(a[i:i+k]);i+=k;m=a[i];i+=1;p2=sorted(p,key=lambda z:sum((z[j]-x[j])**2 for j in range(k)))[:m];o+=["the closest %d points are:"%m]+[" ".join(map(str,z)) for z in p2]
 print("\n".join(o))
def r4092(a):
 i=1;o=[]
 for _ in range(int(a[0])):
  m=int(a[i]);i+=1;s=a[i:i+m];i+=m;best=""
  for L in range(60,2,-1):
   q=sorted({s[0][j:j+L] for j in range(61-L)})
   q=[x for x in q if all(x in z for z in s[1:])]
   if q:best=q[0];break
  o.append(best if len(best)>=3 else"no significant commonalities")
 print("\n".join(o))
def r4104(t):
 print(re.sub(r"\S+",lambda m:m.group()[::-1],t.splitlines()[0] if t.splitlines() else""))
def r4105(a):
 i=1;o=[]
 for _ in range(int(a[0])):
  R,C,K=map(int,a[i:i+3]);i+=3;g=a[i:i+R];i+=R;S=E=None;ps=[];full=0
  for r in range(R):
   for c,ch in enumerate(g[r]):
    if ch=="S":S=(r,c)
    if ch=="E":E=(r,c)
    if ch=="$":ps.append((r,c))
    if ch.isdigit() and int(ch)<K:full|=1<<int(ch)
  q=deque([(S[0],S[1],0,0)]);seen={(S[0],S[1],0)};ans=None
  while q:
   r,c,m,d=q.popleft()
   if (r,c)==E and m==full:ans=d;break
   ns=([(x,y) for x,y in ps if (x,y)!=(r,c)] if g[r][c]=="$" else [])
   ns += [(r+dr,c+dc) for dr,dc in((1,0),(-1,0),(0,1),(0,-1))]
   for x,y in ns:
    if not(0<=x<R and 0<=y<C) or g[x][y]=="#":continue
    mm=m|(1<<int(g[x][y])) if g[x][y].isdigit() and int(g[x][y])<K else m
    st=(x,y,mm)
    if st not in seen:seen.add(st);q.append((x,y,mm,d+(0 if g[r][c]=="$" and (x,y) in ps else 1)))
  o.append(str(ans) if ans is not None else"oop!")
 print("\n".join(o))
def r4106(a):
 print("\n".join(next(c for c in s if s.count(c)==2) for s in a[1:1+int(a[0])]))
def r4108(a):
 ns=a[1:1+a[0]];f=[1,1,1]
 for n in range(3,max(ns,default=2)+1):f.append(f[-1]+f[n-3])
 print("\n".join(map(str,(f[n] for n in ns))))
def r4110(a):
 n=int(a[0]);cap=a[1];x=[(a[i+2]/a[i+3],a[i+2],a[i+3]) for i in range(0,2*n,2)];o=0
 for z,v,w in sorted(x,reverse=True):q=min(cap,w);o+=q*z;cap-=q
 print("%.1f"%o)
def r4111(a):
 def f(x):b=bin(int(x,16))[2:];return sum(c=="1" and (i==0 or b[i-1]=="0") for i,c in enumerate(b))
 print("\n".join("Alice" if f(x)>f(y) else"Bob" if f(x)<f(y) else"Tie" for x,y in zip(a[1::2],a[2::2])))
def r4112(t):
 o=[]
 for line in t.splitlines():
  num=[0]
  def f(m):
   num[0]+=1;k=num[0];return"".join(chr((ord(c)-(65 if c.isupper() else 97)-k)%26+(65 if c.isupper() else 97)) for c in m.group()[::-1])
  o.append(re.sub("[A-Za-z]+",f,line))
 print("\n".join(o))
def r4114(a):
 i=1;o=[]
 for _ in range(int(a[0])):
  n=int(a[i]);i+=1;s=[a[i+j*4:i+j*4+4] for j in range(n)];i+=4*n;ok=False
  for q in range(7200):
   t=math.pi*q/7200;u,v=math.cos(t),math.sin(t);lo=-1e99;hi=1e99
   for x,y,X,Y in s:lo=max(lo,min(x*u+y*v,X*u+Y*v));hi=min(hi,max(x*u+y*v,X*u+Y*v))
   if lo<=hi+1e-8:ok=True;break
  o.append("Yes!" if ok else"No!")
 print("\n".join(o))
def r4120(a):
 n,x=a[:2];c=a[2:2+n];must=[]
 for k in range(n):
  d={0}
  for j,z in enumerate(c):
   if j!=k:d|={q+z for q in tuple(d) if q+z<=x}
  if x not in d:must.append(c[k])
 print(len(must));print(*must)
def r4122(a):
 o=[]
 for s in a[1:1+a[0]]:
  n=len(s);d=[n+1]*(n+1);d[0]=-1
  for j in range(n):
   for i in range(j+1):
    if s[i:j+1]==s[i:j+1][::-1]:d[j+1]=min(d[j+1],d[i]+1)
  o.append(str(d[n]))
 print("\n".join(o))
def r4125(a):
 i=0;o=[]
 while i<len(a):
  n=int(a[i]);i+=1;p=[(a[i+2*j],a[i+2*j+1]) for j in range(n)];i+=2*n
  d=lambda x,y:math.hypot(p[x][0]-p[y][0],p[x][1]-p[y][1]);dp=[[1e99]*n for _ in range(n)];dp[0][1]=d(0,1)
  for j in range(2,n):
   for k in range(j-1):dp[k][j]=dp[k][j-1]+d(j-1,j)
   dp[j-1][j]=min(dp[k][j-1]+d(k,j) for k in range(j-1))
  o.append("%.2f"%(dp[n-2][n-1]+d(n-2,n-1)))
 print("\n".join(o))
def r4126(a):
 i=1;o=[]
 for _ in range(a[0]):
  n=int(a[i]);i+=1;s=a[i:i+n];i+=n;s=[x for j,x in enumerate(s) if not any(j!=k and x in s[k] for k in range(n))];n=len(s);ov=[[0]*n for _ in range(n)]
  for x in range(n):
   for y in range(n):
    for k in range(min(len(s[x]),len(s[y])),-1,-1):
     if s[y].endswith(s[x][:k]):ov[x][y]=k;break
  d={(1<<j,j):len(s[j]) for j in range(n)}
  for m in range(1,1<<n):
   for j in range(n):
    if(m,j)not in d:continue
    for k in range(n):
     if not m>>k&1:d[m|1<<k,k]=min(d.get((m|1<<k,k),9999),d[m,j]+len(s[k])-ov[j][k])
  o.append(str(min(d[(1<<n)-1,j] for j in range(n))))
 print("\n".join(o))
def r4127(a):
 g=[a[i*5:i*5+5] for i in range(5)];q=deque([(0,0)]);p={(0,0):None}
 while q:
  u=q.popleft()
  for x,y in((u[0]+1,u[1]),(u[0]-1,u[1]),(u[0],u[1]+1),(u[0],u[1]-1)):
   if 0<=x<5 and 0<=y<5 and g[x][y]==0 and(x,y)not in p:p[x,y]=u;q.append((x,y))
 u=(4,4);o=[]
 while u is not None:o.append("(%d, %d)"%u);u=p[u]
 print("\n".join(o[::-1]))
def r4128(a):
 s,e=a[0].split();w=a[1].split() if len(a)>1 else[];q=deque([(s,1)]);v={s};ans=0
 while q:
  x,d=q.popleft()
  if x==e:ans=d;break
  for y in w+[e]:
   if y not in v and len(x)==len(y) and sum(i!=j for i,j in zip(x,y))==1:v.add(y);q.append((y,d+1))
 print(ans)
def r4131(a):
 n,m=a[:2];d=[0]*(m+1);i=2
 for _ in range(n):
  w,v=a[i:i+2];i+=2
  for j in range(m,w-1,-1):d[j]=max(d[j],d[j-w]+v)
 print(d[m])
F={4087:r4087,4088:r4088,4090:r4090,4091:r4091,4092:r4092,4104:r4104,4105:r4105,4106:r4106,4108:r4108,4110:r4110,4111:r4111,4112:r4112,4114:r4114,4120:r4120,4122:r4122,4125:r4125,4126:r4126,4127:r4127,4128:r4128,4131:r4131}
a=sys.stdin.read();F[P](a if P in(4090,4104,4112) else list(map(float,a.split())) if P in(4110,4114,4125) else a.splitlines() if P==4128 else [int(a.split()[0])]+a.split()[1:] if P in(4122,4126) else a.split() if P in(4092,4105,4106,4111) else list(map(int,a.split())))
