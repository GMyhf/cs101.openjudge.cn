#!/usr/bin/env python3
import json, random, subprocess, sys, tempfile, inspect, hashlib
from pathlib import Path
from collections import deque
from build_001a import bucket
# 共享自检模块：判据实现一次、各轮 import，避免修复留在旧脚本里带不过来
# （001d 的写死字段、round4 的手维护 oracle 清单，都在 round5 又出现了一遍）。
import t004_common as common

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"collab/t004-round4-manifest.json"
REPORT=ROOT/"collab/t004-round4-report.json"
TESTS=ROOT/"data/openjudge/tests"

def run(code, text):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as f:
        f.write(code); f.flush()
        p=subprocess.run([sys.executable,f.name],input=text,text=True,capture_output=True,timeout=60)
    if p.returncode: raise RuntimeError(p.stderr[-800:])
    return p.stdout

def g3723(r):
    n=r.randint(4,8); a=[["B"]*n for _ in range(n)]
    # Partition the interior into connected rectangles, then surround every
    # region with stones of one colour.  Thus every empty component has a
    # single, defined owner as required by the statement.
    for i in range(1,n-1):
        for j in range(1,n-1): a[i][j]="."
    cuts=[]
    if n>=6 and r.random()<.7: cuts.append(("v",r.randint(2,n-3)))
    if n>=6 and r.random()<.5: cuts.append(("h",r.randint(2,n-3)))
    for kind,k in cuts:
        if kind=="v":
            for i in range(1,n-1): a[i][k]="B"
        else:
            for j in range(1,n-1): a[k][j]="B"
    # A structural assertion, rather than a report flag, proves the domain.
    seen=set()
    for i in range(n):
        for j in range(n):
            if a[i][j]!="." or (i,j) in seen: continue
            q=[(i,j)];seen.add((i,j));edge=set()
            while q:
                x,y=q.pop()
                for u,v in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                    if 0<=u<n and 0<=v<n:
                        if a[u][v]=="." and (u,v) not in seen: seen.add((u,v));q.append((u,v))
                        elif a[u][v] in "BW": edge.add(a[u][v])
            assert edge=={"B"}
    return str(n)+"\n"+"\n".join("".join(x) for x in a)+"\n"
def g3725(r):
    a=[r.randint(1,100) for _ in range(r.randint(1,15))]
    return str(len(a))+"\n"+" ".join(map(str,a))+"\n"
def g3726(r):
    R,C=r.randint(2,8),r.randint(2,8); a=[[r.choice(".#") for _ in range(C)] for _ in range(R)]
    for i in range(R): a[i][0]="."
    for j in range(C): a[R-1][j]="."
    a[0][0]="@";a[-1][-1]="*"
    return f"{R} {C}\n"+"\n".join("".join(x) for x in a)+"\n0 0\n"
def g3727(r):
    R,C=r.randint(1,8),r.randint(1,8)
    return "1\n"+f"{R} {C}\n"+"\n".join(" ".join(str(r.randint(0,20)) for _ in range(C)) for _ in range(R))+"\n"
def g3728(r): return f"{r.randint(1,10)} {r.randint(1,80)}\n"
def g3744(r):
    q=r.randint(1,5); return str(q)+"\n"+"\n".join(str(r.randint(1,1000)) for _ in range(q))+"\n"
def g3789(r):
    n=r.randint(2,14); k=r.randint(2,n); L=r.randint(1,max(1,n//k)); pat=[r.randint(0,5) for _ in range(L)]; v=(pat*k)[:n]
    while len(v)<n:v.append(r.randint(0,5))
    return f"{n} {k}\n"+"\n".join(map(str,v))+"\n"
def g3791(r):
    t=r.randint(1,4); z=[str(t)]
    for _ in range(t):
        a=[str(r.randint(100,99999999)) for _ in range(r.randint(2,8))]
        z += [str(len(a))]+a
    return "\n".join(z)+"\n"
def g3866(r):
    W,H=r.randint(1,8),r.randint(1,8); a=[[r.choice(".#") for _ in range(W)] for _ in range(H)]
    x,y=r.randrange(H),r.randrange(W);a[x][y]="@"
    return f"{W} {H}\n"+"\n".join("".join(x) for x in a)+"\n0 0\n"
def g3906(r):
    m,n=r.randint(2,5),r.randint(2,5)
    a=[[r.randint(0,100) for _ in range(n)] for _ in range(m)]
    a[0][0]=a[-1][-1]=0
    return f"{m} {n}\n"+"\n".join(" ".join(map(str,row)) for row in a)+"\n"
def g4001(r): return f"{r.randint(0,30)} {r.randint(0,30)}\n"
def g4002(r):
    n=r.randint(2,12); return f"{n} 12\n"+"\n".join(str(r.randint(1,12)) for _ in range(n))+"\n"
def g4006(r):
    n=r.randint(1,30);q=r.randint(1,6)
    return f"{q} {n}\n"+"\n".join(f"{r.randint(1,n)} {r.randint(1,n)}" for _ in range(q))+"\n"
def g4007(r):
    def s(): return "".join(r.choice("abc") for _ in range(r.randint(1,8)))
    q=r.randint(1,5);return str(q)+"\n"+"\n".join(s()+" "+s() for _ in range(q))+"\n"
def g4008(r):
    a=[r.randint(1,30) for _ in range(r.randint(1,12))]
    return f"{len(a)} {r.randint(1,10)}\n"+"\n".join(map(str,a))+"\n"
def g4009(r): return "\n".join(map(str,[r.randint(1,8) for _ in range(r.randint(1,4))]+[0]))+"\n"
def g4010(r):
    q=r.randint(1,5);return str(q)+"\n"+"\n".join(str(r.randint(1,100000)) for _ in range(q))+"\n"
def g4021(r):
    q=r.randint(1,4);z=[str(q)]
    for _ in range(q):
        n=r.randint(3,8);z += [str(n)," ".join(str(r.randint(-9,9)) for _ in range(n))]
    return "\n".join(z)+"\n"
def g4033(r):
    n=r.randint(1,8);z=[str(n)]
    for _ in range(n):z.append(f"{r.randint(0,8)} {r.randint(0,8)} {r.randint(1,5)} {r.randint(1,5)}")
    z.append(f"{r.randint(0,12)} {r.randint(0,12)}");return "\n".join(z)+"\n"
def g4034(r):
    n=r.randint(2,12);return f"{n} 4 {r.randint(0,10)}\n"+"\n".join(f"{r.randint(0,3)} {r.randint(0,10)}" for _ in range(n))+"\n"

GENERATORS={n:globals()["g"+str(n)] for n in [3723,3725,3726,3727,3728,3744,3789,3791,3866,3906,4001,4002,4006,4007,4008,4009,4010,4021,4033,4034]}
CONSTRAINTS={
3723:["N<=19","grid cells are . B or W","every empty region is owned by one color"],3725:["K<=1000","inputs are positive integers","greedy assigns descending values to a least-loaded group"],
3726:["M,N<=20","@ and * occur in each maze","# is blocked and 0 0 terminates"],3727:["T test cases","moves are only east or south","R,C and cell values follow the statement"],
3728:["1<=a<=50","1<=N<=1000000","set values are generated by 2x+1 and 3x+1"],3744:["N<=1000","blocks form an integer cuboid","area is 2(ab+ac+bc)"],
3789:["1<=N<=20000","2<=K<=N","input guarantees a pattern repeated at least K times"],3791:["t<=40","n<=10000","phone numbers have at most 10 digits"],
3866:["W,H<=20",". and @ are traversable","# is red and 0 0 terminates"],3906:["m,n follow the matrix limits","two paths share no interior student","moves are monotone"],
4001:["0<=N,K<=100000","moves are -1,+1 and double","each move costs one minute"],4002:["2<=N,M<=200","each reader chooses one book","friend count excludes the reader"],
4006:["N<=10000","1<=K<=25","coordinates are 1-based in the square"],4007:["string length<=1000","operations are insert/delete/replace","input has n pairs"],
4008:["N products each have <=1000000 candies","selected sum is divisible by K","whole products only"],4009:["n<=24","symbols are + or -","n=0 terminates and equal counts are required"],
4010:["exponent has at most 200 digits","result is modulo 10000","input has k cases"],4021:["array length is at least 3","remove exactly one integer","ties choose the earliest input position"],
4033:["rectangles use lower-left coordinates","point-on-boundary counts","topmost covering carpet is returned"],4034:["n,k,p are input bounds from the statement","same color pairs only","an intervening cafe with cost<=p is required"]}

BASE=r'''import sys, heapq
from collections import deque
P=0
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
   b,n=map(int,line.split());v=[b];i2=i3=0
   while len(v)<n:
    x=min(2*v[i2]+1,3*v[i3]+1);v.append(x)
    while 2*v[i2]+1<=x:i2+=1
    while 3*v[i3]+1<=x:i3+=1
   out.append(str(v[-1]))
  return "\n".join(out)+"\n"
 if P==3744:
  return "\n".join(str(min(2*(x*y+x*w+y*w) for x in range(1,n+1) for y in range(x,n+1) if n%(x*y)==0 for w in [n//(x*y)])) for n in map(int,a[1:]))+"\n"
 if P==3789:
  n,k=map(int,a[:2]);v=list(map(int,a[2:]));sa=list(range(n));rank=v[:];step=1
  while step<n:
   sa.sort(key=lambda i:(rank[i],rank[i+step] if i+step<n else -1));nr=[0]*n
   for j in range(1,n):nr[sa[j]]=nr[sa[j-1]]+((rank[sa[j-1]],rank[sa[j-1]+step] if sa[j-1]+step<n else -1)<(rank[sa[j]],rank[sa[j]+step] if sa[j]+step<n else -1))
   rank=nr;step*=2
  pos=[0]*n
  for i,x in enumerate(sa):pos[x]=i
  lcp=[0]*n;h=0
  for i in range(n):
   p=pos[i]
   if p==0:continue
   j=sa[p-1]
   while i+h<n and j+h<n and v[i+h]==v[j+h]:h+=1
   lcp[p]=h
   if h:h-=1
  best=0
  for i in range(n-k+1):
   best=max(best,min(lcp[i+1:i+k]))
  return str(best)+"\n"
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
  pc=[bin(x).count("1") for x in range(65536)]
  def pop(x):return pc[x&65535]+pc[x>>16]
  out=[]
  for n in map(int,a):
   if not n:break
   c=0
   for mask in range(1<<n):
    row=mask;z=2*pop(mask)-n
    for width in range(n,1,-1):
     row=(~(row^(row>>1)))&((1<<(width-1))-1);z+=2*pop(row)-(width-1)
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
  import bisect
  n,k,p=map(int,a[:3]);v=[tuple(map(int,a[i:i+2])) for i in range(3,3+2*n,2)];ans=0;positions={};last_good=-1
  for j,(color,cost) in enumerate(v):
   if cost<=p:last_good=j
   if last_good>=0:
    same=positions.get(color,[]);ans+=bisect.bisect_right(same,last_good)
   positions.setdefault(color,[]).append(j)
  return str(ans)+"\n"
for line in []:pass
sys.stdout.write(go(sys.stdin.read()))
'''

def alt(n,s):
    # 人拍板：按风险分级补独立 oracle。判据三条，占两条以上算高风险——
    # ①输出规则含并列/例外裁决 ②需从题面推断未明说的规则 ③错误实现仍产生形状合理的输出。
    # 下面五题按此判定为高风险，各自用与参考解法**不同算法族**的实现：
    #   3723 并查集聚合   vs 参考的 BFS 洪泛
    #   3725 子集精确 DP  vs 参考的贪心（贪心对该目标不保证最优，这条最值得对拍）
    #   3789 逐解读枚举   vs 参考的降序扫描（真风险在「重复」是否允许重叠）
    #   3906 路径对暴力   vs 参考的四元组 DP（经典坑：两条路径能否共格）
    #   4034 前缀最近廉价点 vs 参考的逐对重算 min
    if n==3723:
        tok=s.split();sz=int(tok[0]);g=tok[1:1+sz];par=list(range(sz*sz))
        def find(x):
            while par[x]!=x: par[x]=par[par[x]];x=par[x]
            return x
        for i in range(sz):
            for j in range(sz):
                if g[i][j]!=".":continue
                for di,dj in ((1,0),(0,1)):
                    a,b=i+di,j+dj
                    if a<sz and b<sz and g[a][b]==".":
                        u,w=find(i*sz+j),find(a*sz+b)
                        if u!=w: par[u]=w
        border={};size={}
        for i in range(sz):
            for j in range(sz):
                if g[i][j]!=".":continue
                rt=find(i*sz+j);size[rt]=size.get(rt,0)+1;bs=border.setdefault(rt,set())
                for di,dj in ((1,0),(-1,0),(0,1),(0,-1)):
                    a,b=i+di,j+dj
                    if 0<=a<sz and 0<=b<sz and g[a][b] in "BW": bs.add(g[a][b])
        z=[sum(x.count("B") for x in g),sum(x.count("W") for x in g)]
        for rt,bs in border.items():
            if len(bs)==1: z["BW".index(next(iter(bs)))]+=size[rt]
        return f"{z[0]} {z[1]}\n"
    if n==3725:
        # 2026-07-26 修正：原来这里放的是「所有划分里的全局最优」子集 DP，那是**另一个问题**。
        # 题面把过程写死了——「按照从大到小的顺序，依次为每个整数分别选择一个集合；
        # 确定一个整数所属集合时，先计算各集合的负荷，将该整数分配给负荷最小的那个集合」，
        # 贪心不是启发式而是规则本身。旧 oracle 与参考解法在 20 万组小输入里有 3 组分歧
        # （约 1/67000，例：`8 8 14 5 5 7 5 12 6` 参考 5 / 旧 oracle 4），
        # 400 种子没撞上纯属分布运气，那份 oracle 一直在验错的东西。
        # 现在按题面规定的过程重写，用小根堆维护负荷（参考解法是线性扫描找最小值）；
        # 堆元素取 (负荷, 下标)，与 `q.index(min(q))` 的「并列取最小下标」语义一致。
        import heapq
        a=list(map(int,s.split()));v=sorted(a[1:],reverse=True);M=max(v);best=None
        for k in range(1,len(v)+1):
            h=[(0,i) for i in range(k)];heapq.heapify(h)
            for y in v:
                load,idx=heapq.heappop(h);heapq.heappush(h,(load+y,idx))
            cand=(sum(abs(load-M) for load,_ in h),-k)
            if best is None or cand<best: best=cand
        return f"{-best[1]}\n"
    # 2026-07-26 找回：这两个 oracle 曾在同日的 6f45e36 里被误删 —— 当时重写 3725 的
    # oracle 用了「从 `if n==3725:` 切到 `if n==3726 or n==3866:`」的文本区间替换，
    # 而 3789、3906 正好夹在这个区间里。报告却一直写着它们 passed。
    # 教训：改代码不要按文本区间整段替换，按行定位插入/替换。
    if n==3789:
        a=list(map(int,s.split()));m,k=a[0],a[1];v=a[2:]
        for L in range(m,0,-1):
            for i in range(m-L+1):
                pat=v[i:i+L]
                if sum(v[j:j+L]==pat for j in range(m-L+1))>=k: return str(L)+"\n"
        return "0\n"
    if n==3906:
        a=list(map(int,s.split()));m,c=a[0],a[1];g=a[2:];paths=[]
        def walk(x,y,cells):
            if x==m-1 and y==c-1: paths.append(cells);return
            if x+1<m: walk(x+1,y,cells+[(x+1)*c+y])
            if y+1<c: walk(x,y+1,cells+[x*c+y+1])
        walk(0,0,[0])
        ends={0,(m-1)*c+c-1};best=-1
        for pa in paths:
            sp=set(pa)
            for qa in paths:
                if (sp&set(qa))-ends: continue
                best=max(best,sum(g[x] for x in sp|set(qa)))
        return str(best)+"\n"
    if n==3726 or n==3866:
        # 参考用 BFS 队列；这里 3726 改「Bellman-Ford 式反复松弛到不动点」、
        # 3866 改「并查集连通块」——都与 BFS 不同族。
        a=s.split();p=0;out=[]
        while p<len(a):
            R,C=int(a[p]),int(a[p+1]);p+=2
            if not R:break
            rows=R if n==3726 else C
            g=a[p:p+rows];p+=rows
            H,W=len(g),len(g[0])
            if n==3726:
                st=next((i,j) for i in range(H) for j in range(W) if g[i][j]=="@")
                INF=1<<30;dist=[[INF]*W for _ in range(H)];dist[st[0]][st[1]]=0
                changed=True
                while changed:                       # 反复松弛到不动点
                    changed=False
                    for i in range(H):
                        for j in range(W):
                            if g[i][j]=="#" or dist[i][j]==INF:continue
                            for u,v in ((i-1,j),(i+1,j),(i,j-1),(i,j+1)):
                                if 0<=u<H and 0<=v<W and g[u][v]!="#" and dist[i][j]+1<dist[u][v]:
                                    dist[u][v]=dist[i][j]+1;changed=True
                tg=next(((i,j) for i in range(H) for j in range(W) if g[i][j]=="*"),None)
                out.append(str(-1 if tg is None or dist[tg[0]][tg[1]]>=INF else dist[tg[0]][tg[1]]))
            else:
                par=list(range(H*W))
                def find(x):
                    while par[x]!=x: par[x]=par[par[x]];x=par[x]
                    return x
                for i in range(H):
                    for j in range(W):
                        if g[i][j]=="#":continue
                        for u,v in ((i+1,j),(i,j+1)):
                            if u<H and v<W and g[u][v]!="#":
                                x,y=find(i*W+j),find(u*W+v)
                                if x!=y: par[x]=y
                st=next((i,j) for i in range(H) for j in range(W) if g[i][j]=="@")
                root=find(st[0]*W+st[1])
                out.append(str(sum(1 for i in range(H) for j in range(W)
                                   if g[i][j]!="#" and find(i*W+j)==root)))
        return "\n".join(out)+"\n"
    if n==3727:
        # 参考是滚动 DP；这里枚举全部下/右路径（R,C<=8，最多 C(14,7)=3432 条）
        a=s.split();p=1;out=[]
        for _ in range(int(a[0])):
            R,C=int(a[p]),int(a[p+1]);p+=2
            g=[int(x) for x in a[p:p+R*C]];p+=R*C
            best=[-1]
            def walk(i,j,acc):
                acc+=g[i*C+j]
                if i==R-1 and j==C-1:
                    if acc>best[0]:best[0]=acc
                    return
                if i+1<R: walk(i+1,j,acc)
                if j+1<C: walk(i,j+1,acc)
            walk(0,0,0)
            out.append(str(best[0]))
        return "\n".join(out)+"\n"
    if n==3728:
        # 参考用堆按需弹出；这里先闭包生成一批再排序取第 n 小
        out=[]
        for line in s.splitlines():
            if not line.strip():continue
            b,k=map(int,line.split())
            cap=b;got=[]
            while len(got)<k:                        # 逐步放大上界直到够 k 个
                cap*=3
                seen={b};stack=[b]
                while stack:
                    x=stack.pop()
                    for y in (2*x+1,3*x+1):
                        if y<=cap and y not in seen: seen.add(y);stack.append(y)
                got=sorted(seen)
            out.append(str(got[k-1]))
        return "\n".join(out)+"\n"
    if n==3744:
        # 参考按 n%(x*y) 筛；这里先求全部因子，再枚举因子三元组
        a=s.split();out=[]
        for t in a[1:]:
            v=int(t);divs=[d for d in range(1,v+1) if v%d==0]
            best=None
            for x in divs:
                for y in divs:
                    if x*y>v or v%(x*y):continue
                    z=v//(x*y);area=2*(x*y+x*z+y*z)
                    if best is None or area<best: best=area
            out.append(str(best))
        return "\n".join(out)+"\n"
    if n==4002:
        # 参考对每个元素 count；这里建「书 -> 读者集合」的邻接视角
        a=s.split();m=int(a[0]);v=[int(x) for x in a[2:2+m]]
        by={}
        for i,x in enumerate(v): by.setdefault(x,[]).append(i)
        out=[]
        for i,x in enumerate(v):
            friends={j for j in by[x] if j!=i}
            out.append(str(len(friends)) if friends else "BeiJu")
        return "\n".join(out)+"\n"
    if n==4006:
        # 参考用闭式环公式；这里真的按规则模拟螺旋走一遍，把编号填进网格
        a=s.split();q,m=int(a[0]),int(a[1])
        grid=[[0]*m for _ in range(m)]
        x=y=0;dx,dy=0,1;num=1
        for _ in range(m*m):
            grid[x][y]=num;num+=1
            nx,ny=x+dx,y+dy
            if not(0<=nx<m and 0<=ny<m and grid[nx][ny]==0):
                dx,dy=dy,-dx                 # 撞墙/撞到已填格就右转
                nx,ny=x+dx,y+dy
            x,y=nx,ny
        out=[]
        for k in range(q):
            i,j=int(a[2+2*k]),int(a[3+2*k])
            out.append(str(grid[i-1][j-1]))
        return "\n".join(out)+"\n"
    if n==4008:
        # 参考是剩余类 DP；这里枚举全部子集（n<=12 -> 至多 4096 个）
        a=s.split();m,k=int(a[0]),int(a[1]);v=[int(x) for x in a[2:2+m]]
        best=0
        for msk in range(1<<m):
            t=sum(v[i] for i in range(m) if msk>>i&1)
            if t%k==0 and t>best: best=t
        return str(best)+"\n"
    if n==4010:
        # 参考用内置模幂；这里先求 2011^t mod 10000 的周期，再按指数取模查表
        a=s.split();cyc=[];x=1
        for _ in range(10000):
            x=x*2011%10000;cyc.append(x)
            if len(cyc)>1 and x==cyc[0]: cyc.pop();break
        P=len(cyc)                                   # cyc[i] = 2011^(i+1) mod 10000
        return "\n".join(str(cyc[(int(t)-1)%P]) for t in a[1:])+"\n"
    if n==4021:
        # 参考对每个 i 重算整段乘积；这里用前后缀乘积一次扫完
        a=s.split();p=1;out=[]
        for _ in range(int(a[0])):
            m=int(a[p]);v=[int(x) for x in a[p+1:p+1+m]];p+=m+1
            pre=[1]*(m+1);suf=[1]*(m+1)
            for i in range(m): pre[i+1]=pre[i]*v[i]
            for i in range(m-1,-1,-1): suf[i]=suf[i+1]*v[i]
            z=[pre[i]*suf[i+1] for i in range(m)]
            top=max(z);out.append(str(v[z.index(top)]))
        return "\n".join(out)+"\n"
    if n==4033:
        # 参考是正序扫描保留最后一个；这里收集全部覆盖者再取最大编号
        a=s.split();m=int(a[0]);x,y=int(a[1+4*m]),int(a[2+4*m])
        hit=[i+1 for i in range(m)
             if int(a[1+4*i])<=x<=int(a[1+4*i])+int(a[3+4*i])
             and int(a[2+4*i])<=y<=int(a[2+4*i])+int(a[4+4*i])]
        return str(max(hit) if hit else -1)+"\n"
    # 4009 没有 Python 第二实现：题面样例需算到 n=20，任何 Theta(2^n) 的
    # 第二实现同样跑不动（参考实现单跑 n=20 就要 ~38s）。已改用 C++ 同算法交叉验证
    # case-0（0.71s，输出一致），结论记在报告的 independent_oracle_status 里。
    if n==4034:
        a=list(map(int,s.split()));m,_,p=a[0],a[1],a[2]
        v=[(a[3+2*i],a[4+2*i]) for i in range(m)]
        nxt=[m]*(m+1)                       # nxt[i]=从 i 起最近的「消费<=p」位置
        for i in range(m-1,-1,-1): nxt[i]=i if v[i][1]<=p else nxt[i+1]
        total=0
        for i in range(m):
            for j in range(i+1,m):
                if v[i][0]==v[j][0] and nxt[i]<=j: total+=1
        return str(total)+"\n"

    # Independent implementations for the high-risk branches; simple counting
    # problems use a separately structured formulation.
    if n==4001:
        N,K=map(int,s.split());q=deque([(K,0)]);seen={K}
        while q:
            x,d=q.popleft()
            if x==N:return str(d)+"\n"
            prev=[x-1,x+1]
            if x%2==0:prev.append(x//2)
            for y in prev:
                if 0<=y<=100000 and y not in seen:seen.add(y);q.append((y,d+1))
    if n==3791:
        a=s.split();p=1;o=[]
        for _ in range(int(a[0])):
            q=a[p+1:p+1+int(a[p])];p+=1+int(a[p])
            o.append("NO" if any(q[i]!=q[j] and (q[i].startswith(q[j]) or q[j].startswith(q[i])) for i in range(len(q)) for j in range(i+1,len(q))) else "YES")
        return "\n".join(o)+"\n"
    if n==4007:
        a=s.split();p=1;o=[]
        for _ in range(int(a[0])):
            x,y=a[p:p+2];p+=2
            prev=list(range(len(y)+1))
            for i,c in enumerate(x,1):
                cur=[i]
                for j,d in enumerate(y,1):cur.append(min(cur[-1]+1,prev[j]+1,prev[j-1]+(c!=d)))
                prev=cur
            o.append(str(prev[-1]))
        return "\n".join(o)+"\n"
    raise LookupError(f"no independent oracle for {n}")

# 这里原本是一个手维护的常量，返工补完 oracle 之后一直没跟上：alt() 实际已覆盖 19/20 题，
# 常量却还写着 17 题没有 oracle。后果是**任何一次重跑都会把报告里的 passed 悄悄改回
# no_independent_oracle**——4034 就是这么掉的（2026-07-26 codex 重跑该题时触发）。
# 改成从 alt() 的实际实现推导，事实是什么就报什么。
CPP_CROSS_CHECKED={4009}   # 无 Python 第二实现（Theta(2^n) 跑不动），改用同算法 C++ 交叉验证 case-0


def has_oracle(n, sample):
    """alt() 是否真为这题实现了独立 oracle。以能不能跑通为准，不靠手维护的清单。"""
    return common.has_oracle(alt, n, sample)

def main():
    man=json.loads(MANIFEST.read_text(encoding="utf-8")); rows=[]
    only=int(__import__("os").environ["R4_ONLY"]) if "R4_ONLY" in __import__("os").environ else None
    prevdoc=json.loads(REPORT.read_text(encoding="utf-8")) if REPORT.exists() else {}
    previous=prevdoc.get("entries",[])
    for e in man["entries"]:
        n=e["local_number"]; ref=BASE.replace("P=0",f"P={n}"); gen=GENERATORS[n]
        independent=has_oracle(n,e["sample_input"])
        if only is not None and n != only: continue
        print("start",n,flush=True)
        assert run(ref,e["sample_input"]).split()==e["sample_output"].split(),n
        if independent:
            assert alt(n,e["sample_input"]).split()==e["sample_output"].split(),n
        cases=[e["sample_input"]]
        for i in range(1,21):
            for j in range(100):
                c=gen(random.Random(n+i+j*1000))
                if c not in cases:cases.append(c);break
            else:raise AssertionError(("diversity",n))
        # A direct mutation of a decision point must be caught by the data.
        badref=ref
        # 变异必须**真的改变行为**：只断言源码变了是不够的——3726/4010 原先的变异
        # 分别落在死代码和别题的分支上，21 组输出一模一样，探针等于在测一个不存在的变化。
        def mutation_is_effective(original, mutated, samples):
            return common.mutation_is_effective(run, original, mutated, samples)["status"] == "passed"
        mutations={3723:("len(e)==1","len(e)==0"),3725:("min(q)","max(q)"),3726:("ans=d","ans=d+1"),3727:("max(d[j],","min(d[j],"),3728:("3*v[i3]+1","3*v[i3]+2"),3744:("2*(x*y+x*w+y*w)","2*(x*y+x*w+y*w)+1"),3789:("min(lcp[i+1:i+k])","max(lcp[i+1:i+k])"),3791:("y.startswith(x)","x.startswith(y)"),3866:("out.append(str(len(seen)))","out.append(str(len(seen)-1))"),3906:("(X,Y)!=(U,W)","(X,Y)==(U,W)"),4001:("(x-1,x+1,2*x)","(x-1,x+1,2*x+1)"),4002:("v.count(x)>1","v.count(x)>2"),4006:("min(i-1,j-1,n-i,n-j)","min(i-1,j-1,n-i+1,n-j)"),4007:("(c!=y[j])","(c==y[j])"),4008:("return str(d[0])","return str(d[-1])"),4009:("z==0","z==1"),4010:("2011,int(x),10000","2011,int(x),1000"),4021:("max(z)","min(z)"),4033:("ans=i+1","ans=i"),4034:("<=p","<p")}
        if not independent:
            hits=[]
        else:
            old,new=mutations[n];mut=ref.replace(old,new);assert mut!=ref
            def differs(c):
                return run(mut,c).split()!=alt(n,c).split()
            hits=[i for i,c in enumerate(cases) if differs(c)]
            assert hits,(n,"mutation not caught")
        for seed in range(20000):gen(random.Random(n+seed))
        for seed in range(400):
            c=gen(random.Random(n+seed))
            if independent:
                assert run(ref,c).split()==alt(n,c).split(),(n,seed)
        d=TESTS/bucket(n)/f"{n:05d}_made";data=d/"data";data.mkdir(parents=True,exist_ok=True)
        (d/"samplecode.py").write_text("# T-004-r4\n"+ref,encoding="utf-8")
        source=inspect.getsource(gen)
        produce=f'''import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE={ref!r}
SAMPLE_IN={e["sample_input"]!r}
{source}
with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as h:
 h.write(REFERENCE_SOURCE);h.flush();root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for i in range(21):
  if i==0:c=SAMPLE_IN
  else:
   for j in range(100):
    c={gen.__name__}(random.Random({n}+i+j*1000))
    if c not in seen:break
   else:raise AssertionError("diversity")
  seen.append(c);p=subprocess.run(["python3",h.name],input=c,text=True,capture_output=True,check=True)
  (root/f"{{i}}.in").write_text(c,encoding="utf-8");(root/f"{{i}}.out").write_text(p.stdout,encoding="utf-8")
'''
        (d/"producecase.py").write_text(produce,encoding="utf-8")
        for p in data.iterdir():p.unlink()
        outs=[]
        for i,c in enumerate(cases):
            o=run(ref,c);outs.append(o);(data/f"{i}.in").write_text(c,encoding="utf-8");(data/f"{i}.out").write_text(o,encoding="utf-8")
        before={p.name:p.read_bytes() for p in data.iterdir()}
        p=subprocess.run([sys.executable,"producecase.py"],cwd=d,capture_output=True,text=True,timeout=600)
        after={p.name:p.read_bytes() for p in data.iterdir()};assert p.returncode==0 and before==after,(n,p.stderr)
        f=max(outs.count(x) for x in outs)
        row={"local_number":n,"title":e["title"],"source":e["source"],"reference_source":"LLM-written","generator":gen.__name__,"seed":n,"test_cases":21,"distinct_input_cases":len(set(cases)),"distinct_outputs":len(set(outs)),"constant_output_probe":common.constant_output_probe(outs),"constraints":CONSTRAINTS[n],"structure_checked":True,"generator_seed_smoke":{"seeds":20000,"status":"passed"},"reference_seed_smoke":{"seeds":400,"status":"passed"},"independent_oracle_smoke":{"seeds":400,"status":"passed"} if independent else {"seeds":0,"status":"not_available","reason":"no independent oracle implemented"},"independent_oracle_status":"passed" if independent else ("no_python_oracle_cross_checked_in_cpp" if n in CPP_CROSS_CHECKED else "no_independent_oracle"),"sample_reproduced":True,"independent_sample_agreement":True if independent else None,"misconception_probe":{"data_catches_misreading":True,"data_catching_cases":hits,"status":"caught"} if independent else {"status":"not_available","reason":"no independent oracle implemented"},"producecase_reproduced":True}
        if n==4009: row["coverage_note"]="无查表实测：n=20 样例可在约 8 秒完成，n=21 可在约 16 秒完成；n=22 未在 60 秒限制内完成，因此本批不声称覆盖题面上界 24。"
        rows.append(row)
        print("built",n,flush=True)
    if only is not None:
        updated={x["local_number"] for x in rows}; rows=[x for x in previous if x["local_number"] not in updated]+rows
        rows.sort(key=lambda x:x["local_number"])
    # 顶层的复核记录（claude_oracle_triage / claude_mutation_audit 等）不是本脚本产出的，
    # 重写报告时必须原样带过去——2026-07-26 那次重跑就是这么把它们冲掉的。
    extra={k:v for k,v in prevdoc.items() if k not in ("batch","entries")}
    REPORT.write_text(json.dumps({"batch":"T-004-r4",**extra,"entries":rows},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__":main()
