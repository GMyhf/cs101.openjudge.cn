# T-004-r5
P=4076
import sys, math
from collections import deque
def solve(s):
 a=s.split()
 if P==4140:
  lo,hi=5.0,6.0
  for _ in range(70):
   mid=(lo+hi)/2
   if mid*mid*mid-5*mid*mid+10*mid-80 < 0:lo=mid
   else:hi=mid
  return f"{(lo+hi)/2:.9f}\n"
 if P==7206:
  x1,y1,x2,y2=int(a[0]),int(a[1]),int(a[2]),int(a[3]); m=int(a[4]); blocked={(int(a[5+2*i]),int(a[6+2*i])) for i in range(m)}
  moves=((1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1));q=deque([(x1,y1)]);dist={(x1,y1):0};ways={(x1,y1):1}
  while q:
   u=q.popleft()
   for dx,dy in moves:
    z=(u[0]+dx,u[1]+dy)
    if not(0<=z[0]<=10 and 0<=z[1]<=10) or z in blocked:continue
    if z not in dist:dist[z]=dist[u]+1;ways[z]=ways[u];q.append(z)
    elif dist[z]==dist[u]+1:ways[z]+=ways[u]
  if (x2,y2) not in dist:return "0\n"
  if ways[(x2,y2)]!=1:return str(ways[(x2,y2)])+"\n"
  path=[(x2,y2)];u=(x2,y2)
  while u!=(x1,y1):
   u=next(v for v in dist if dist.get(v)==dist[u]-1 and (u[0]-v[0],u[1]-v[1]) in moves);path.append(u)
  return "-".join(f"({x},{y})" for x,y in path[::-1])+"\n"
 if P==22528:
  scores=list(map(float,a));need=(3*len(scores)+4)//5;lo,hi=1,10**9
  while lo<hi:
   b=(lo+hi)//2; aa=b/1e9
   if sum(aa*x+1.1**(aa*x)>=85 for x in scores) >= need: hi=b
   else: lo=b+1
  return str(lo)+"\n"
 if P==23554:
  n=int(a[0]);v=list(map(int,a[1:]));return " ".join(map(str,sorted(set(range(1,n+1))-set(v))))+"\n"+" ".join(map(str,sorted(x for x in v if x>n)))+"\n"
 if P==25570:
  n=int(a[0]);v=list(map(int,a[1:]));ans=[]
  for layer in range((n+1)//2):
   z=sum(v[layer*n+j] for j in range(layer,n-layer))
   z+=sum(v[(n-1-layer)*n+j] for j in range(layer,n-layer)) if n-1-layer!=layer else 0
   z+=sum(v[i*n+layer] for i in range(layer+1,n-1-layer))
   z+=sum(v[i*n+n-1-layer] for i in range(layer+1,n-1-layer));ans.append(z)
  if n%2:ans.append(v[(n//2)*n+n//2])
  return str(max(ans))+"\n"
 if P==27384:
  n,k=int(a[0]),int(a[1]); rec=sorted((int(a[2+2*i]),int(a[3+2*i])) for i in range(n)); target=set(map(int,a[2+2*n:]));cnt={};last=0;ans=0;i=0
  while i<n:
   t=rec[i][0]
   top=sorted(cnt,key=lambda c:-cnt[c])
   if len(top)>=k and set(top[:k])==target and (len(top)==k or cnt[top[k-1]]>cnt[top[k]]):ans+=t-last
   while i<n and rec[i][0]==t:cnt[rec[i][1]]=cnt.get(rec[i][1],0)+1;i+=1
   last=t
  return str(ans)+"\n"
 if P==3377:
  n=int(a[0]);v=a[1:1+n];i,j=0,n-1;out=[]
  while i<=j:
   if v[i:j+1] <= v[i:j+1][::-1]:out.append(v[i]);i+=1
   else:out.append(v[j]);j-=1
  text="".join(out)
  return "\n".join(text[i:i+80] for i in range(0,len(text),80))+"\n"
 if P==3670:
  v=[list(map(int,a[i*5:i*5+5])) for i in range(5)];ans=[]
  for i in range(5):
   for j in range(5):
    if v[i][j]==max(v[i]) and v[i][j]==min(v[x][j] for x in range(5)):ans.append((i+1,j+1,v[i][j]))
  return ("%d %d %d\n"%ans[0]) if len(ans)==1 else "not found\n"
 if P==4022:
  n,k=map(int,a);house=200.;saved=0.
  for y in range(1,21):
   saved+=n
   if saved>=house:return str(y)+"\n"
   house*=1+k/100
  return "Impossible\n"
 if P==4031:
  n,R,Q=map(int,a[:3]);s=list(map(int,a[3:3+2*n]));w=list(map(int,a[3+2*n:]))
  order=list(range(2*n))
  for _ in range(R):
   order.sort(key=lambda i:(-s[i],i));
   for x,y in zip(order[::2],order[1::2]):s[x if w[x]>w[y] else y]+=1
  order.sort(key=lambda i:(-s[i],i));return str(order[Q-1]+1)+"\n"
 if P==4037:
  n,m,S=map(int,a[:3]);v=[(int(a[3+2*i]),int(a[4+2*i])) for i in range(n)];q=[(int(a[3+2*n+2*i]),int(a[4+2*n+2*i])) for i in range(m)];lo,hi=0,max(x[0] for x in v)+1
  def f(W):
   z=[0]
   for w,x in v:z.append(z[-1]+(x if w>=W else 0))
   return sum((z[r]-z[l-1])*(sum(1 for w,x in v[l-1:r] if w>=W)) for l,r in q)
  return str(min(abs(f(W)-S) for W in range(lo,hi)))+"\n"
 if P==4076:
  m,n=int(a[0]),int(a[1]);g=[list(map(int,a[2+i*n:2+(i+1)*n])) for i in range(m)];k=int(a[2+m*n]);pat=list(map(int,a[3+m*n:]))
  def dfs(x,y,p,used):
   if p==k:return True
   for u,v in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
    if 0<=u<m and 0<=v<n and (u,v) not in used and g[u][v]==pat[p]:
     used.add((u,v))
     if dfs(u,v,p+1,used):return True
     used.remove((u,v))
   return False
  return ("1\n" if any(dfs(i,j,1,{(i,j)}) for i in range(m) for j in range(n) if g[i][j]==pat[0]) else "0\n")
 if P==4011:
  p=0;out=[]
  while p<len(a):
   N,M=map(int,a[p:p+2]);p+=2
   if N==0:break
   edges=[[] for _ in range(N)]
   for _ in range(M):u,v,w=map(int,a[p:p+3]);p+=3;edges[u].append((v,w));edges[v].append((u,w))
   agents=int(a[p]);p+=1;prob=[[0.0]+list(map(float,a[p+i*agents:p+(i+1)*agents])) for i in range(N)];p+=N*agents
   import heapq
   dist=[10**18]*N;dist[0]=0;h=[(0,0)]
   while h:
    du,u=heapq.heappop(h)
    if du!=dist[u]:continue
    for v,w in edges[u]:
     if du+w<dist[v]:dist[v]=du+w;heapq.heappush(h,(dist[v],v))
   best=0.0
   def evaluate(plan):
    q=[0.0]*N
    for u in sorted(range(N),key=lambda x:-dist[x]):
     nxt=[v for v,w in edges[u] if dist[v]==dist[u]+w];future=sum(q[v] for v in nxt)/len(nxt) if nxt else 0
     q[u]=prob[u][plan[u]]+(1-prob[u][plan[u]])*future
    return q[0]
   def distribute(i,left,plan):
    nonlocal best
    if i==N:
     if left==0:best=max(best,evaluate(plan))
     return
    for x in range(left+1):distribute(i+1,left-x,plan+[x])
   distribute(0,agents,[]);out.append(f'{best*100:.2f}')
  return '\n'.join(out)+'\n'
 if P==4038:
  n,m,k=map(int,a[:3]);d=list(map(int,a[3:3+n-1]));ps=[tuple(map(int,a[3+n-1+3*i:3+n-1+3*i+3])) for i in range(m)]
  def total(cut):
   travel=[d[i]-cut[i] for i in range(n-1)];clock=0;ans=0;waiting={i:[] for i in range(1,n+1)};active=[]
   for t,x,y in ps:waiting[x].append((t,y))
   for station in range(1,n):
    if waiting[station]:clock=max(clock,max(t for t,_ in waiting[station]));active.extend(waiting[station])
    clock+=travel[station-1];done=[z for z in active if z[1]==station+1];ans+=sum(clock-t for t,_ in done);active=[z for z in active if z[1]!=station+1]
   return ans
  best=10**18
  def distribute(i,left,cut):
   nonlocal best
   if i==n-1:best=min(best,total(cut));return
   for x in range(min(left,d[i])+1):distribute(i+1,left-x,cut+[x])
  distribute(0,k,[]);return str(best)+'\n'
 if P==3750:
  q=0;tc=int(a[q]);q+=1;ans=[];nm=('dragon','ninja','iceman','lion','wolf');ordr=((2,3,4,1,0),(3,0,1,2,4))
  class W:
   def __init__(self,s,t,i,h,f,pos):self.s=s;self.t=t;self.i=i;self.h=h;self.f=f;self.pos=pos;self.step=0;self.kills=0
   def name(self):return ('red' if self.s==0 else 'blue')+' '+nm[self.t]+' '+str(self.i)
  for case in range(1,tc+1):
   M,N,T=map(int,a[q:q+3]);q+=3;hp=list(map(int,a[q:q+5]));q+=5;atk=list(map(int,a[q:q+5]));q+=5;E=[M,M];idx=[0,0];num=[0,0];units=[];cities=[[None,None] for _ in range(N+2)];gold=[0]*(N+2);lastwin=[-1]*(N+2);flag=[-1]*(N+2);lines=[f'Case:{case}'];dead=[False]
   def put(t,s):lines.append(f'{t//60:03d}:{t%60:02d} '+s)
   def born(s,t):
    z=ordr[s][idx[s]]
    if E[s]<hp[z]:return
    E[s]-=hp[z];idx[s]=(idx[s]+1)%5;num[s]+=1;w=W(s,z,num[s],hp[z],atk[z],0 if s==0 else N+1);units.append(w);put(t,w.name()+' born')
   for t in range(0,T+1,10):
    if dead[0]:break
    if t%60==0:born(0,t);born(1,t)
    elif t%60==10:
     ev=[]
     for w in units:
      if w.h<=0 or w.pos==(N+1 if w.s==0 else 0):continue
      old=w.pos
      if 1<=old<=N:cities[old][w.s]=None
      w.pos+=1 if w.s==0 else -1;w.step+=1
      if w.t==2 and w.step%2==0:w.h=max(1,w.h-9);w.f+=20
      if 1<=w.pos<=N:cities[w.pos][w.s]=w
      if w.pos==(N+1 if w.s==0 else 0):msg=w.name()+f" reached {'blue' if w.s==0 else 'red'} headquarter with {w.h} elements and force {w.f}"
      else:msg=w.name()+f' marched to city {w.pos} with {w.h} elements and force {w.f}'
      ev.append((w.pos,w.s,msg))
     for _,s,msg in sorted(ev):put(t,msg)
     for s,label in ((0,'blue'),(1,'red')):
      if sum(w.h>0 and w.pos==(N+1 if s==0 else 0) for w in units)>=2:put(t,label+' headquarter was taken');dead[0]=True
    elif t%60==20:
     for i in range(1,N+1):gold[i]+=10
    elif t%60==30:
     for i in range(1,N+1):
      live=[w for w in cities[i] if w and w.h>0]
      if len(live)==1: E[live[0].s]+=gold[i];put(t,live[0].name()+f' earned {gold[i]} elements for his headquarter');gold[i]=0
    elif t%60==40:
     vict=[]
     for i in range(1,N+1):
      r,b=cities[i]
      if not(r and b):continue
      x,y=(r,b) if i%2 else (b,r);put(t,x.name()+f' attacked {y.name()} in city {i} with {x.h} elements and force {x.f}');x_before=x.h;y_before=y.h;y.h-=x.f
      if y.h<=0:
       put(t,y.name()+f' was killed in city {i}');cities[i][y.s]=None
       if x.t==4:
        x.kills+=1
        if x.kills%2==0:x.h*=2;x.f*=2
       if y.t==3:x.h+=y_before
       if x.t==0 and x.h>0:put(t,x.name()+f' yelled in city {i}')
       vict.append((i,x,gold[i]));put(t,x.name()+f' earned {gold[i]} elements for his headquarter');gold[i]=0
       if lastwin[i]==x.s and flag[i]!=x.s:flag[i]=x.s;put(t,('red' if x.s==0 else 'blue')+f' flag raised in city {i}')
       lastwin[i]=x.s
      elif y.t!=1:
       put(t,y.name()+f' fought back against {x.name()} in city {i}');x.h-=y.f//2
       if x.h<=0:
        put(t,x.name()+f' was killed in city {i}');cities[i][x.s]=None
        if x.t==3:y.h+=x_before
        vict.append((i,y,gold[i]));put(t,y.name()+f' earned {gold[i]} elements for his headquarter');gold[i]=0
        if lastwin[i]==y.s and flag[i]!=y.s:flag[i]=y.s;put(t,('red' if y.s==0 else 'blue')+f' flag raised in city {i}')
        lastwin[i]=y.s
     for i,w,_ in sorted(vict,key=lambda z:(-z[0] if z[1].s==0 else z[0])):
      if E[w.s]>=8:E[w.s]-=8;w.h+=8
     for i,w,loot in vict:E[w.s]+=loot
    elif t%60==50:put(t,f'{E[0]} elements in red headquarter');put(t,f'{E[1]} elements in blue headquarter')
   ans.append('\n'.join(lines))
  return '\n'.join(ans)+'\n'
 if P==4054:
  directions=((1,0),(0,1),(-1,0),(0,-1));rotates=((5,2,1,4,3,0),(3,4,5,0,1,2));colors={'E':(6,),'W':(0,1),'R':(2,3),'B':(4,5)};p=0;out=[]
  def possible(target):
   vals=[6]*9;ans=[]
   def dfs(i):
    if i==9:ans.append(sum(7**j*vals[j] for j in range(9)));return
    for z in colors[target[i]]:vals[i]=z;dfs(i+1)
   dfs(0);return target.index('E'),ans
  def solve_one(sx,sy,target):
   start=3*sx+sy;cur=7**start*6;q1=deque([cur]);start_sum=0
   for _ in range(9):start_sum+=cur%7;cur//=7
   s1={start};blank,goals=possible(target);q2=deque();
   for z in goals:
    v=z;sm=0
    for _ in range(9):sm+=v%7;v//=7
    if (sm-start_sum-blank+start)&1==0:q2.append(z)
   s2=set(q2)
   for depth in range(31):
    if len(q2)<len(q1):q1,q2=q2,q1;s1,s2=s2,s1
    for _ in range(len(q1)):
     state=q1.popleft()
     if state in s2:return depth
     if depth==30:continue
     cur=[];v=state;bx=by=pos=-1
     for i in range(9):
      z=v%7;v//=7;cur.append(z)
      if z==6:bx,by,pos=i//3,i%3,i
     for dx,dy in directions:
      nx,ny=bx+dx,by+dy
      if not(0<=nx<3 and 0<=ny<3):continue
      j=nx*3+ny;new=cur[:];new[pos]=rotates[dx][cur[j]];new[j]=6;z=sum(7**i*new[i] for i in range(9))
      if z not in s1:s1.add(z);q1.append(z)
   return -1
  while p<len(a):
   sy,sx=int(a[p])-1,int(a[p+1])-1;p+=2
   if sx==sy==-1:break
   target=a[p:p+9];p+=9;out.append(str(solve_one(sx,sy,target)))
  return '\n'.join(out)+'\n'
 if P==4035:
  n=int(a[0]);g=[[0]*7 for _ in range(5)];p=1
  for x in range(5):
   y=0
   while int(a[p]):g[x][y]=int(a[p]);y+=1;p+=1
   p+=1
  def settle(b):
   while True:
    rm=[[False]*7 for _ in range(5)]
    for x in range(5):
     y=0
     while y<7:
      if not b[x][y]:y+=1;continue
      z=y+1
      while z<7 and b[x][z]==b[x][y]:z+=1
      if z-y>=3:
       for q in range(y,z):rm[x][q]=True
      y=z
    for y in range(7):
     x=0
     while x<5:
      if not b[x][y]:x+=1;continue
      z=x+1
      while z<5 and b[z][y]==b[x][y]:z+=1
      if z-x>=3:
       for q in range(x,z):rm[q][y]=True
      x=z
    if not any(any(r) for r in rm):return
    for x in range(5):
     vals=[b[x][y] for y in range(7) if not rm[x][y]]
     b[x]=vals+[0]*(7-len(vals))
  def move(b,x,y,d):
   z=[r[:] for r in b];q=x+d
   if not(0<=q<5) or z[x][y]==0 or z[q][y]==z[x][y] and z[q][y]!=0:return None
   if z[q][y]:z[x][y],z[q][y]=z[q][y],z[x][y]
   else:
    z[q][y]=z[x][y];z[x][y]=0
    vals=[z[q][j] for j in range(7) if z[q][j]];z[q]=vals+[0]*(7-len(vals))
   settle(z);return z
  path=[]
  def dfs(b,dep):
   if dep==n:return all(not b[x][y] for x in range(5) for y in range(7))
   for x in range(5):
    for y in range(7):
     if not b[x][y]:continue
     for d in (1,-1):
      z=move(b,x,y,d)
      if z is None:continue
      path.append((x,y,d))
      if dfs(z,dep+1):return True
      path.pop()
   return False
  if not dfs(g,0):return '-1\n'
  return '\n'.join(f'{x} {y} {d}' for x,y,d in path)+'\n'
 if P==4012:
  def one(s):
   L=len(s);memo={}
   def smallest(pos,ln,prev):
    pat=s[pos:pos+ln]
    if any(ch==',' for ch in pat):return None
    bound=str(int(prev)+1) if prev else '1'
    if len(bound)<ln:bound='1'+'0'*(ln-1);strict=False
    elif len(bound)>ln:return None
    else:strict=True
    def build(i,rel,out):
     if i==ln:return ''.join(out) if (not strict or rel in (0,1)) else None
     low=int(bound[i]) if strict and rel==0 else 0
     for d in range(low,10):
      if i==0 and d==0:continue
      ch=pat[i]
      if ch!='?' and int(ch)!=d:continue
      nr=1 if (strict and (rel==1 or d>int(bound[i]))) else 0
      z=build(i+1,nr,out+[str(d)])
      if z is not None:return z
     return None
    return build(0,0,[])
   def dfs(pos,prev):
    key=(pos,prev)
    if key in memo:return memo[key]
    if pos==L:return ''
    best=None
    for ln in range(1,L-pos+1):
     if pos+ln<L and s[pos+ln] not in ',?':continue
     cur=smallest(pos,ln,prev)
     if cur is None:continue
     nxt=pos+ln
     if nxt==L:tail=''
     else:
      tail=dfs(nxt+1,cur)
      if tail is None:continue
     best=cur+(','+tail if tail else '');break
    memo[key]=best;return best
   z=dfs(0,'')
   return z if z is not None else 'impossible'
  return '\n'.join(one(line.strip()) for line in s.splitlines() if line.strip())+'\n'
 if P==4083:
  p=0;N=int(a[p]);p+=1;names=a[p:p+N];p+=N;M=int(a[p]);p+=1;adj={x:[] for x in names}
  for _ in range(M):u,v,w=a[p:p+3];p+=3;w=int(w);adj[u].append((v,w));adj[v].append((u,w))
  Q=int(a[p]);p+=1;out=[]
  import heapq
  for _ in range(Q):
   src,dst=a[p:p+2];p+=2;d={src:0};prev={};h=[(0,src)]
   while h:
    z,u=heapq.heappop(h)
    if z!=d[u]:continue
    for v,w in adj[u]:
     if z+w<d.get(v,10**9):d[v]=z+w;prev[v]=u;heapq.heappush(h,(z+w,v))
   path=[];u=dst
   while u!=src:path.append((prev[u],d[u]-d[prev[u]],u));u=prev[u]
   path.reverse();out.append(src+''.join(f"->({w})->{v}" for _,w,v in path))
  return '\n'.join(out)+'\n'
 raise LookupError(P)
sys.stdout.write(solve(sys.stdin.read()))
