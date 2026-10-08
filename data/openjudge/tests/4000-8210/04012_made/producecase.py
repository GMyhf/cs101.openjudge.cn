import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE='P=4012\nimport sys, math\nfrom collections import deque\ndef solve(s):\n a=s.split()\n if P==4140:\n  lo,hi=5.0,6.0\n  for _ in range(70):\n   mid=(lo+hi)/2\n   if mid*mid*mid-5*mid*mid+10*mid-80 < 0:lo=mid\n   else:hi=mid\n  return f"{(lo+hi)/2:.9f}\\n"\n if P==7206:\n  x1,y1,x2,y2=int(a[0]),int(a[1]),int(a[2]),int(a[3]); m=int(a[4]); blocked={(int(a[5+2*i]),int(a[6+2*i])) for i in range(m)}\n  moves=((1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1));q=deque([(x1,y1)]);dist={(x1,y1):0};ways={(x1,y1):1}\n  while q:\n   u=q.popleft()\n   for dx,dy in moves:\n    z=(u[0]+dx,u[1]+dy)\n    if not(0<=z[0]<=10 and 0<=z[1]<=10) or z in blocked:continue\n    if z not in dist:dist[z]=dist[u]+1;ways[z]=ways[u];q.append(z)\n    elif dist[z]==dist[u]+1:ways[z]+=ways[u]\n  if (x2,y2) not in dist:return "0\\n"\n  if ways[(x2,y2)]!=1:return str(ways[(x2,y2)])+"\\n"\n  path=[(x2,y2)];u=(x2,y2)\n  while u!=(x1,y1):\n   u=next(v for v in dist if dist.get(v)==dist[u]-1 and (u[0]-v[0],u[1]-v[1]) in moves);path.append(u)\n  return "-".join(f"({x},{y})" for x,y in path[::-1])+"\\n"\n if P==22528:\n  scores=list(map(float,a));need=(3*len(scores)+4)//5;lo,hi=1,10**9\n  while lo<hi:\n   b=(lo+hi)//2; aa=b/1e9\n   if sum(aa*x+1.1**(aa*x)>=85 for x in scores) >= need: hi=b\n   else: lo=b+1\n  return str(lo)+"\\n"\n if P==23554:\n  n=int(a[0]);v=list(map(int,a[1:]));return " ".join(map(str,sorted(set(range(1,n+1))-set(v))))+"\\n"+" ".join(map(str,sorted(x for x in v if x>n)))+"\\n"\n if P==25570:\n  n=int(a[0]);v=list(map(int,a[1:]));ans=[]\n  for layer in range((n+1)//2):\n   z=sum(v[layer*n+j] for j in range(layer,n-layer))\n   z+=sum(v[(n-1-layer)*n+j] for j in range(layer,n-layer)) if n-1-layer!=layer else 0\n   z+=sum(v[i*n+layer] for i in range(layer+1,n-1-layer))\n   z+=sum(v[i*n+n-1-layer] for i in range(layer+1,n-1-layer));ans.append(z)\n  if n%2:ans.append(v[(n//2)*n+n//2])\n  return str(max(ans))+"\\n"\n if P==27384:\n  n,k=int(a[0]),int(a[1]); rec=sorted((int(a[2+2*i]),int(a[3+2*i])) for i in range(n)); target=set(map(int,a[2+2*n:]));cnt={};last=0;ans=0;i=0\n  while i<n:\n   t=rec[i][0]\n   top=sorted(cnt,key=lambda c:-cnt[c])\n   if len(top)>=k and set(top[:k])==target and (len(top)==k or cnt[top[k-1]]>cnt[top[k]]):ans+=t-last\n   while i<n and rec[i][0]==t:cnt[rec[i][1]]=cnt.get(rec[i][1],0)+1;i+=1\n   last=t\n  return str(ans)+"\\n"\n if P==3377:\n  n=int(a[0]);v=a[1:1+n];i,j=0,n-1;out=[]\n  while i<=j:\n   if v[i:j+1] <= v[i:j+1][::-1]:out.append(v[i]);i+=1\n   else:out.append(v[j]);j-=1\n  text="".join(out)\n  return "\\n".join(text[i:i+80] for i in range(0,len(text),80))+"\\n"\n if P==3670:\n  v=[list(map(int,a[i*5:i*5+5])) for i in range(5)];ans=[]\n  for i in range(5):\n   for j in range(5):\n    if v[i][j]==max(v[i]) and v[i][j]==min(v[x][j] for x in range(5)):ans.append((i+1,j+1,v[i][j]))\n  return ("%d %d %d\\n"%ans[0]) if len(ans)==1 else "not found\\n"\n if P==4022:\n  n,k=map(int,a);house=200.;saved=0.\n  for y in range(1, 40):\n   saved+=n\n   if saved>=house:return str(y)+"\\n"\n   house*=1+k/100\n  return "Impossible\\n"\n if P==4031:\n  n,R,Q=map(int,a[:3]);s=list(map(int,a[3:3+2*n]));w=list(map(int,a[3+2*n:]))\n  order=list(range(2*n))\n  for _ in range(R):\n   order.sort(key=lambda i:(-s[i],i));\n   for x,y in zip(order[::2],order[1::2]):s[x if w[x]>w[y] else y]+=1\n  order.sort(key=lambda i:(-s[i],i));return str(order[Q-1]+1)+"\\n"\n if P==4037:\n  n,m,S=map(int,a[:3]);v=[(int(a[3+2*i]),int(a[4+2*i])) for i in range(n)];q=[(int(a[3+2*n+2*i]),int(a[4+2*n+2*i])) for i in range(m)];lo,hi=0,max(x[0] for x in v)+1\n  def f(W):\n   z=[0]\n   for w,x in v:z.append(z[-1]+(x if w>=W else 0))\n   return sum((z[r]-z[l-1])*(sum(1 for w,x in v[l-1:r] if w>=W)) for l,r in q)\n  return str(min(abs(f(W)-S) for W in range(lo,hi)))+"\\n"\n if P==4076:\n  m,n=int(a[0]),int(a[1]);g=[list(map(int,a[2+i*n:2+(i+1)*n])) for i in range(m)];k=int(a[2+m*n]);pat=list(map(int,a[3+m*n:]))\n  def dfs(x,y,p,used):\n   if p==k:return True\n   for u,v in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):\n    if 0<=u<m and 0<=v<n and (u,v) not in used and g[u][v]==pat[p]:\n     used.add((u,v))\n     if dfs(u,v,p+1,used):return True\n     used.remove((u,v))\n   return False\n  return ("1\\n" if any(dfs(i,j,1,{(i,j)}) for i in range(m) for j in range(n) if g[i][j]==pat[0]) else "0\\n")\n if P==4011:\n  p=0;out=[]\n  while p<len(a):\n   N,M=map(int,a[p:p+2]);p+=2\n   if N==0:break\n   edges=[[] for _ in range(N)]\n   for _ in range(M):u,v,w=map(int,a[p:p+3]);p+=3;edges[u].append((v,w));edges[v].append((u,w))\n   agents=int(a[p]);p+=1;prob=[[0.0]+list(map(float,a[p+i*agents:p+(i+1)*agents])) for i in range(N)];p+=N*agents\n   import heapq\n   dist=[10**18]*N;dist[0]=0;h=[(0,0)]\n   while h:\n    du,u=heapq.heappop(h)\n    if du!=dist[u]:continue\n    for v,w in edges[u]:\n     if du+w<dist[v]:dist[v]=du+w;heapq.heappush(h,(dist[v],v))\n   best=0.0\n   def evaluate(plan):\n    q=[0.0]*N\n    for u in sorted(range(N),key=lambda x:-dist[x]):\n     nxt=[v for v,w in edges[u] if dist[v]==dist[u]+w];future=sum(q[v] for v in nxt)/len(nxt) if nxt else 0\n     q[u]=prob[u][plan[u]]+(1-prob[u][plan[u]])*future\n    return q[0]\n   def distribute(i,left,plan):\n    nonlocal best\n    if i==N:\n     if left==0:best=max(best,evaluate(plan))\n     return\n    for x in range(left+1):distribute(i+1,left-x,plan+[x])\n   distribute(0,agents,[]);out.append(f\'{best*100:.2f}\')\n  return \'\\n\'.join(out)+\'\\n\'\n if P==4038:\n  n,m,k=map(int,a[:3]);d=list(map(int,a[3:3+n-1]));ps=[tuple(map(int,a[3+n-1+3*i:3+n-1+3*i+3])) for i in range(m)]\n  def total(cut):\n   travel=[d[i]-cut[i] for i in range(n-1)];clock=0;ans=0;waiting={i:[] for i in range(1,n+1)};active=[]\n   for t,x,y in ps:waiting[x].append((t,y))\n   for station in range(1,n):\n    if waiting[station]:clock=max(clock,max(t for t,_ in waiting[station]));active.extend(waiting[station])\n    clock+=travel[station-1];done=[z for z in active if z[1]==station+1];ans+=sum(clock-t for t,_ in done);active=[z for z in active if z[1]!=station+1]\n   return ans\n  best=10**18\n  def distribute(i,left,cut):\n   nonlocal best\n   if i==n-1:best=min(best,total(cut));return\n   for x in range(min(left,d[i])+1):distribute(i+1,left-x,cut+[x])\n  distribute(0,k,[]);return str(best)+\'\\n\'\n if P==3750:\n  q=0;tc=int(a[q]);q+=1;ans=[];nm=(\'dragon\',\'ninja\',\'iceman\',\'lion\',\'wolf\');ordr=((2,3,4,1,0),(3,0,1,2,4))\n  class W:\n   def __init__(self,s,t,i,h,f,pos):self.s=s;self.t=t;self.i=i;self.h=h;self.f=f;self.pos=pos;self.step=0;self.kills=0\n   def name(self):return (\'red\' if self.s==0 else \'blue\')+\' \'+nm[self.t]+\' \'+str(self.i)\n  for case in range(1,tc+1):\n   M,N,T=map(int,a[q:q+3]);q+=3;hp=list(map(int,a[q:q+5]));q+=5;atk=list(map(int,a[q:q+5]));q+=5;E=[M,M];idx=[0,0];num=[0,0];units=[];cities=[[None,None] for _ in range(N+2)];gold=[0]*(N+2);lastwin=[-1]*(N+2);flag=[-1]*(N+2);lines=[f\'Case:{case}\'];dead=[False]\n   def put(t,s):lines.append(f\'{t//60:03d}:{t%60:02d} \'+s)\n   def born(s,t):\n    z=ordr[s][idx[s]]\n    if E[s]<hp[z]:return\n    E[s]-=hp[z];idx[s]=(idx[s]+1)%5;num[s]+=1;w=W(s,z,num[s],hp[z],atk[z],0 if s==0 else N+1);units.append(w);put(t,w.name()+\' born\')\n   for t in range(0,T+1,10):\n    if dead[0]:break\n    if t%60==0:born(0,t);born(1,t)\n    elif t%60==10:\n     ev=[]\n     for w in units:\n      if w.h<=0 or w.pos==(N+1 if w.s==0 else 0):continue\n      old=w.pos\n      if 1<=old<=N:cities[old][w.s]=None\n      w.pos+=1 if w.s==0 else -1;w.step+=1\n      if w.t==2 and w.step%2==0:w.h=max(1,w.h-9);w.f+=20\n      if 1<=w.pos<=N:cities[w.pos][w.s]=w\n      if w.pos==(N+1 if w.s==0 else 0):msg=w.name()+f" reached {\'blue\' if w.s==0 else \'red\'} headquarter with {w.h} elements and force {w.f}"\n      else:msg=w.name()+f\' marched to city {w.pos} with {w.h} elements and force {w.f}\'\n      ev.append((w.pos,w.s,msg))\n     for _,s,msg in sorted(ev):put(t,msg)\n     for s,label in ((0,\'blue\'),(1,\'red\')):\n      if sum(w.h>0 and w.pos==(N+1 if s==0 else 0) for w in units)>=2:put(t,label+\' headquarter was taken\');dead[0]=True\n    elif t%60==20:\n     for i in range(1,N+1):gold[i]+=10\n    elif t%60==30:\n     for i in range(1,N+1):\n      live=[w for w in cities[i] if w and w.h>0]\n      if len(live)==1: E[live[0].s]+=gold[i];put(t,live[0].name()+f\' earned {gold[i]} elements for his headquarter\');gold[i]=0\n    elif t%60==40:\n     vict=[]\n     for i in range(1,N+1):\n      r,b=cities[i]\n      if not(r and b):continue\n      x,y=(r,b) if i%2 else (b,r);put(t,x.name()+f\' attacked {y.name()} in city {i} with {x.h} elements and force {x.f}\');x_before=x.h;y_before=y.h;y.h-=x.f\n      if y.h<=0:\n       put(t,y.name()+f\' was killed in city {i}\');cities[i][y.s]=None\n       if x.t==4:\n        x.kills+=1\n        if x.kills%2==0:x.h*=2;x.f*=2\n       if y.t==3:x.h+=y_before\n       if x.t==0 and x.h>0:put(t,x.name()+f\' yelled in city {i}\')\n       vict.append((i,x,gold[i]));put(t,x.name()+f\' earned {gold[i]} elements for his headquarter\');gold[i]=0\n       if lastwin[i]==x.s and flag[i]!=x.s:flag[i]=x.s;put(t,(\'red\' if x.s==0 else \'blue\')+f\' flag raised in city {i}\')\n       lastwin[i]=x.s\n      elif y.t!=1:\n       put(t,y.name()+f\' fought back against {x.name()} in city {i}\');x.h-=y.f//2\n       if x.h<=0:\n        put(t,x.name()+f\' was killed in city {i}\');cities[i][x.s]=None\n        if x.t==3:y.h+=x_before\n        vict.append((i,y,gold[i]));put(t,y.name()+f\' earned {gold[i]} elements for his headquarter\');gold[i]=0\n        if lastwin[i]==y.s and flag[i]!=y.s:flag[i]=y.s;put(t,(\'red\' if y.s==0 else \'blue\')+f\' flag raised in city {i}\')\n        lastwin[i]=y.s\n     for i,w,_ in sorted(vict,key=lambda z:(-z[0] if z[1].s==0 else z[0])):\n      if E[w.s]>=8:E[w.s]-=8;w.h+=8\n     for i,w,loot in vict:E[w.s]+=loot\n    elif t%60==50:put(t,f\'{E[0]} elements in red headquarter\');put(t,f\'{E[1]} elements in blue headquarter\')\n   ans.append(\'\\n\'.join(lines))\n  return \'\\n\'.join(ans)+\'\\n\'\n if P==4054:\n  directions=((1,0),(0,1),(-1,0),(0,-1));rotates=((5,2,1,4,3,0),(3,4,5,0,1,2));colors={\'E\':(6,),\'W\':(0,1),\'R\':(2,3),\'B\':(4,5)};p=0;out=[]\n  def possible(target):\n   vals=[6]*9;ans=[]\n   def dfs(i):\n    if i==9:ans.append(sum(7**j*vals[j] for j in range(9)));return\n    for z in colors[target[i]]:vals[i]=z;dfs(i+1)\n   dfs(0);return target.index(\'E\'),ans\n  def solve_one(sx,sy,target):\n   start=3*sx+sy;cur=7**start*6;q1=deque([cur]);start_sum=0\n   for _ in range(9):start_sum+=cur%7;cur//=7\n   s1={start};blank,goals=possible(target);q2=deque();\n   for z in goals:\n    v=z;sm=0\n    for _ in range(9):sm+=v%7;v//=7\n    if (sm-start_sum-blank+start)&1==0:q2.append(z)\n   s2=set(q2)\n   for depth in range(31):\n    if len(q2)<len(q1):q1,q2=q2,q1;s1,s2=s2,s1\n    for _ in range(len(q1)):\n     state=q1.popleft()\n     if state in s2:return depth\n     if depth==30:continue\n     cur=[];v=state;bx=by=pos=-1\n     for i in range(9):\n      z=v%7;v//=7;cur.append(z)\n      if z==6:bx,by,pos=i//3,i%3,i\n     for dx,dy in directions:\n      nx,ny=bx+dx,by+dy\n      if not(0<=nx<3 and 0<=ny<3):continue\n      j=nx*3+ny;new=cur[:];new[pos]=rotates[dx][cur[j]];new[j]=6;z=sum(7**i*new[i] for i in range(9))\n      if z not in s1:s1.add(z);q1.append(z)\n   return -1\n  while p<len(a):\n   sy,sx=int(a[p])-1,int(a[p+1])-1;p+=2\n   if sx==sy==-1:break\n   target=a[p:p+9];p+=9;out.append(str(solve_one(sx,sy,target)))\n  return \'\\n\'.join(out)+\'\\n\'\n if P==4035:\n  n=int(a[0]);g=[[0]*7 for _ in range(5)];p=1\n  for x in range(5):\n   y=0\n   while int(a[p]):g[x][y]=int(a[p]);y+=1;p+=1\n   p+=1\n  def settle(b):\n   while True:\n    rm=[[False]*7 for _ in range(5)]\n    for x in range(5):\n     y=0\n     while y<7:\n      if not b[x][y]:y+=1;continue\n      z=y+1\n      while z<7 and b[x][z]==b[x][y]:z+=1\n      if z-y>=3:\n       for q in range(y,z):rm[x][q]=True\n      y=z\n    for y in range(7):\n     x=0\n     while x<5:\n      if not b[x][y]:x+=1;continue\n      z=x+1\n      while z<5 and b[z][y]==b[x][y]:z+=1\n      if z-x>=3:\n       for q in range(x,z):rm[q][y]=True\n      x=z\n    if not any(any(r) for r in rm):return\n    for x in range(5):\n     vals=[b[x][y] for y in range(7) if not rm[x][y]]\n     b[x]=vals+[0]*(7-len(vals))\n  def move(b,x,y,d):\n   z=[r[:] for r in b];q=x+d\n   if not(0<=q<5) or z[x][y]==0 or z[q][y]==z[x][y] and z[q][y]!=0:return None\n   if z[q][y]:z[x][y],z[q][y]=z[q][y],z[x][y]\n   else:\n    z[q][y]=z[x][y];z[x][y]=0\n    vals=[z[q][j] for j in range(7) if z[q][j]];z[q]=vals+[0]*(7-len(vals))\n   settle(z);return z\n  path=[]\n  def dfs(b,dep):\n   if dep==n:return all(not b[x][y] for x in range(5) for y in range(7))\n   for x in range(5):\n    for y in range(7):\n     if not b[x][y]:continue\n     for d in (1,-1):\n      z=move(b,x,y,d)\n      if z is None:continue\n      path.append((x,y,d))\n      if dfs(z,dep+1):return True\n      path.pop()\n   return False\n  if not dfs(g,0):return \'-1\\n\'\n  return \'\\n\'.join(f\'{x} {y} {d}\' for x,y,d in path)+\'\\n\'\n if P==4012:\n  # 自右向左求 M[pos]=后缀 s[pos:] 合法拆分时首个数的最大可能值，再自左向右贪心取最小可行数；O(L^3)\n  def mn(pat,lo):\n   n=len(pat);t=str(lo+1)\n   if pat[0]==\'0\' or len(t)>n:return None\n   if len(t)<n:return \'\'.join((\'1\' if i==0 else \'0\') if c==\'?\' else c for i,c in enumerate(pat))\n   if all(c==\'?\' or c==d for c,d in zip(pat,t)):return t\n   pre=0\n   while pre<n and (pat[pre]==\'?\' or pat[pre]==t[pre]):pre+=1\n   for i in range(min(pre,n-1),-1,-1):\n    c=pat[i];td=int(t[i])\n    if c==\'?\':\n     if td==9:continue\n     d=str(td+1)\n    elif int(c)<=td:continue\n    else:d=c\n    return t[:i]+d+\'\'.join(\'0\' if x==\'?\' else x for x in pat[i+1:])\n   return None\n  def mx(pat,hi):\n   n=len(pat)\n   if pat[0]==\'0\':return None\n   if hi is None or len(str(hi-1))>n:return \'\'.join(\'9\' if c==\'?\' else c for c in pat)\n   t=str(hi-1)\n   if hi-1<=0 or len(t)<n:return None\n   if all(c==\'?\' or c==d for c,d in zip(pat,t)):return t\n   pre=0\n   while pre<n and (pat[pre]==\'?\' or pat[pre]==t[pre]):pre+=1\n   for i in range(min(pre,n-1),-1,-1):\n    c=pat[i];td=int(t[i]);lowd=1 if i==0 else 0\n    if c==\'?\':\n     if td-1<lowd:continue\n     d=str(td-1)\n    elif int(c)>=td:continue\n    else:d=c\n    return t[:i]+d+\'\'.join(\'9\' if x==\'?\' else x for x in pat[i+1:])\n   return None\n  def one(s):\n   L=len(s);M=[False]*(L+1)\n   def segs(pos):\n    for ln in range(1,L-pos+1):\n     if s[pos+ln-1]==\',\':break\n     e=pos+ln\n     if e==L:yield ln,None\n     elif s[e] in \',?\' and e+1<L:yield ln,e+1\n   for pos in range(L-1,-1,-1):\n    best=False\n    for ln,nx in segs(pos):\n     if nx is not None and M[nx] is False:continue\n     x=mx(s[pos:pos+ln],None if nx is None else M[nx])\n     if x is not None and (best is False or int(x)>best):best=int(x)\n    M[pos]=best\n   if M[0] is False:return \'impossible\'\n   out=[];pos=0;prev=0\n   while True:\n    for ln,nx in segs(pos):\n     x=mn(s[pos:pos+ln],prev)\n     if x is None:continue\n     if nx is not None and (M[nx] is False or int(x)>=M[nx]):continue\n     break\n    out.append(x)\n    if nx is None:break\n    pos=nx;prev=int(x)\n   return \',\'.join(out)\n  return \'\\n\'.join(one(line.strip()) for line in s.splitlines() if line.strip())+\'\\n\'\n if P==4083:\n  p=0;N=int(a[p]);p+=1;names=a[p:p+N];p+=N;M=int(a[p]);p+=1;adj={x:[] for x in names}\n  for _ in range(M):u,v,w=a[p:p+3];p+=3;w=int(w);adj[u].append((v,w));adj[v].append((u,w))\n  Q=int(a[p]);p+=1;out=[]\n  import heapq\n  for _ in range(Q):\n   src,dst=a[p:p+2];p+=2;d={src:0};prev={};h=[(0,src)]\n   while h:\n    z,u=heapq.heappop(h)\n    if z!=d[u]:continue\n    for v,w in adj[u]:\n     if z+w<d.get(v,10**9):d[v]=z+w;prev[v]=u;heapq.heappush(h,(z+w,v))\n   path=[];u=dst\n   while u!=src:path.append((prev[u],d[u]-d[prev[u]],u));u=prev[u]\n   path.reverse();out.append(src+\'\'.join(f"->({w})->{v}" for _,w,v in path))\n  return \'\\n\'.join(out)+\'\\n\'\n raise LookupError(P)\nsys.stdout.write(solve(sys.stdin.read()))\n'
SAMPLE_IN='?,10,?????????????????,16,??\n?2?5??7?,??\n???????????????????????????????,???\n'


def valid(text):
    """题面契约：多组数据，每行一个由数字、'?'、',' 组成的串，长度不超过 500。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not lines:
        return False
    for line in lines:
        if not (1 <= len(line) <= 500):
            return False
        if any(ch not in "0123456789?," for ch in line):
            return False
    return True


def mask(r, s, pq, pc=None):
    """把一串真实的递增序列打码：数字以 pq 概率变 '?'，逗号以 pc 概率变 '?'。"""
    if pc is None:
        pc = pq
    return "".join("?" if r.random() < (pc if ch == "," else pq) else ch for ch in s)


def increasing(r, max_len, step_lo=1, step_hi=40, start_hi=20):
    value = r.randint(1, start_hi)
    nums = [str(value)]
    while True:
        value += r.randint(step_lo, step_hi)
        if len(",".join(nums)) + 1 + len(str(value)) > max_len:
            break
        nums.append(str(value))
    return ",".join(nums)


def mutate(r, s):
    """随机改动一两个字符，常常把有解改成无解。"""
    s = list(s)
    for _ in range(r.randint(1, 2)):
        s[r.randrange(len(s))] = r.choice("0123456789,?")
    return "".join(s)


EDGE_LINES = [
    "?", "1", "9", "0", ",", "?,", ",?", "??", "?,?", "???", "1,1", "2,1",
    "9,?", "9??", "9,??", "10", "01", "0?", "?0", "??,?", "1,,2", "1?",
    "?9", "?,0", "0,?", ",,", "?,,?", "1,2,", ",1,2", "99,??", "99,???",
    "?????", "1?1", "12,1?", "12,?1", "19,?0", "100,???", "999,???", "???,999",
]


def gen(i):
    r = random.Random(4012 * 1000 + i)
    if i == 0:
        return SAMPLE_IN
    if i <= 2:
        # 手写边界：单字符、首尾逗号、连续逗号、前导零、必须进位才能递增等
        lines = EDGE_LINES[(i - 1) * 20:(i - 1) * 20 + 20]
        return "\n".join(lines) + "\n"
    if i <= 12:
        # 小规模随机串，字符随意混杂，有解无解都有
        lines = []
        for _ in range(30):
            n = r.randint(1, 14)
            alph = r.choice(["0123456789??,,", "?????,1", "??0", "123??,"])
            lines.append("".join(r.choice(alph) for _ in range(n)))
        return "\n".join(lines) + "\n"
    if i <= 22:
        # 中等规模：真实递增序列打码，部分再扰动成无解
        lines = []
        for _ in range(12):
            s = increasing(r, r.randint(10, 120), 1, r.choice([3, 40, 900]))
            s = mask(r, s, r.choice([0.2, 0.4, 0.7]), r.choice([0.3, 0.8, 1.0]))
            if r.random() < 0.3:
                s = mutate(r, s)
            lines.append(s)
        return "\n".join(lines) + "\n"
    if i <= 32:
        # 满长度 500：真实递增序列打码 / 扰动
        lines = []
        for _ in range(4):
            s = increasing(r, 500, 1, r.choice([2, 60, 5000, 10 ** 6]), r.choice([9, 10 ** 4]))
            s = mask(r, s, r.choice([0.15, 0.35, 0.6]), r.choice([0.5, 0.9, 1.0]))
            if r.random() < 0.25:
                s = mutate(r, s)
            lines.append(s)
        return "\n".join(lines) + "\n"
    # 33..39：长度 500 的特殊形状（全问号、数字很长、末尾卡死需要回溯等）
    special = {
        33: ["?" * 500, "?" * 499 + "1", "9" + "?" * 499],
        34: ["?" * 250 + "," + "?" * 249, "9" * 250 + "?" + "9" * 249, ("9?" * 250)[:500]],
        35: ["".join(r.choice("??????,") for _ in range(500)) for _ in range(3)],
        36: ["".join(r.choice("???0") for _ in range(500)) for _ in range(3)],
        37: ["".join(r.choice("?????9") for _ in range(497)) + "111" for _ in range(2)],
        38: ["".join(r.choice("0123456789????") for _ in range(500)) for _ in range(3)],
        39: ["1" + "0" * 498 + "?", "?" * 498 + ",1", "1," + "0?" * 249],
    }[i]
    return "\n".join(special) + "\n"


def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py") as h:
        h.write(REFERENCE_SOURCE)
        h.flush()
        root = Path(__file__).parent / "data"
        for i in range(40):
            c = gen(i)
            assert valid(c), i
            p = subprocess.run(["python3", h.name], input=c, text=True, capture_output=True, check=True)
            (root / f"{i}.in").write_text(c)
            (root / f"{i}.out").write_text(p.stdout)


if __name__ == "__main__":
    main()
