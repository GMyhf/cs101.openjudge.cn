import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='# 参考解：SPFA（双端队列 + 最短路边数计数判负环），只从 S 可达的点出发松弛。\n# 最短路边数达到 n 即说明 S 可走入负圈，输出 Error；否则不可达点输出 null。\nimport sys\nfrom collections import deque\ndef main():\n    data = sys.stdin.buffer.read().split()\n    pos = 0\n    T = int(data[pos]); pos += 1\n    out = []\n    for _ in range(T):\n        n, m, s = int(data[pos]), int(data[pos+1]), int(data[pos+2]); pos += 3\n        G = [[] for _ in range(n + 1)]\n        for _ in range(m):\n            x, y, z = int(data[pos]), int(data[pos+1]), int(data[pos+2]); pos += 3\n            G[x].append((y, z))\n        INF = None\n        dis = [INF] * (n + 1)\n        length = [0] * (n + 1)\n        inq = [False] * (n + 1)\n        dis[s] = 0\n        q = deque([s]); inq[s] = True\n        bad = False\n        while q and not bad:\n            u = q.popleft(); inq[u] = False\n            du = dis[u]; lu = length[u] + 1\n            for v, w in G[u]:\n                nd = du + w\n                if dis[v] is None or nd < dis[v]:\n                    dis[v] = nd\n                    length[v] = lu\n                    if lu >= n:\n                        bad = True\n                        break\n                    if not inq[v]:\n                        inq[v] = True\n                        q.append(v)\n        if bad:\n            out.append("Error")\n        else:\n            out.append(" ".join("null" if d is None else str(d) for d in dis[1:]))\n    sys.stdout.write("\\n".join(out) + "\\n")\nmain()\n'
LANGUAGE='Python3'
SAMPLE='4\n5 7 1\n1 2 3\n2 3 4\n3 4 8\n1 3 9\n4 5 1\n1 4 5\n1 5 10\n4 4 1\n1 2 -4\n2 3 8\n1 3 5\n3 4 0\n3 3 2\n1 2 -3\n2 3 -4\n3 1 6\n4 2 1\n1 2 1\n3 4 2\n'
GENERATOR_NAME='g18252'
def valid(text):
    """题面：第一行 T；每组第一行 n m S，接着 m 行 x y z（1≤x,y≤n）。
    T<=10, n<=10000, m<=20000, |z|<=10000；所有数据 n 之和<=30000，m 之和<=60000。
    （n≥1、1≤S≤n 由「点的编号从1到n」「起点为S」推出。）"""
    lines=text.split("\n")
    if lines[-1]!="": return False
    lines=lines[:-1]
    def ints(line,k):
        t=line.split(" ")
        if len(t)!=k: return None
        try: v=[int(x) for x in t]
        except ValueError: return None
        if any(str(a)!=b for a,b in zip(v,t)): return None
        return v
    if not lines: return False
    h=ints(lines[0],1)
    if h is None: return False
    T=h[0]
    if not 1<=T<=10: return False
    i=1; sn=sm=0
    for _ in range(T):
        if i>=len(lines): return False
        h=ints(lines[i],3); i+=1
        if h is None: return False
        n,m,S=h
        if not (1<=n<=10000 and 0<=m<=20000 and 1<=S<=n): return False
        sn+=n; sm+=m
        if i+m>len(lines): return False
        for j in range(m):
            e=ints(lines[i+j],3)
            if e is None: return False
            x,y,z=e
            if not (1<=x<=n and 1<=y<=n and abs(z)<=10000): return False
        i+=m
    return i==len(lines) and sn<=30000 and sm<=60000

def _case(r,n,m,mode,S=None,neg_reach=False,neg_unreach=False,reach_frac=1.0,wlo=-10000,whi=10000):
    """mode='pot'：带势能的负权边，保证 S 可达部分无负环；mode='rand'：权值随机（小图里会自然出现负环）。
    reach_frac<1 时一部分点只能从「不可达区」走入，且不可达区里放负权边（卡 INF 加负数后误当可达的写法）。"""
    S=S or r.randint(1,n)
    nodes=list(range(1,n+1)); nodes.remove(S); r.shuffle(nodes)
    C=[]
    if neg_reach and n>=3:                # 负环放在只出不回的小汇点分量里，经一条桥边从可达区进入
        C=nodes[:min(n-2,r.randint(1,5))]; nodes=nodes[len(C):]
    k=int(round((n-1)*reach_frac))
    A=[S]+nodes[:k]; B=nodes[k:]          # A：S 可达；B：不可达
    pot={v:r.randint(0,4000) for v in range(1,n+1)}
    def w(x,y):
        if mode=='pot':
            lo=max(0,-10000-pot[x]+pot[y]); hi=min(10000-pot[x]+pot[y],6000)
            return r.randint(lo,hi)+pot[x]-pot[y] if lo<=hi else 0
        return r.randint(wlo,whi)
    E=[]
    for i in range(1,len(A)):             # A 内随机生成树（链状/随机父亲混合，制造深路径）
        par=A[i-1] if r.random()<0.5 else A[r.randrange(i)]
        E.append((par,A[i],w(par,A[i])))
    for i in range(1,len(B)):
        par=B[r.randrange(i)]
        E.append((par,B[i],w(par,B[i])))
    while len(E)<m:
        t=r.random()
        if B and t<0.3:                    # 不可达区内部 / 从不可达区指向可达区，可带负权
            x=r.choice(B); y=r.choice(B) if r.random()<0.5 else r.choice(A)
            E.append((x,y,r.randint(-10000,10000) if mode=='rand' else w(x,y)))
        else:
            x=r.choice(A); y=r.choice(A)
            E.append((x,y,w(x,y)))
    E=E[:m]
    if C:
        extra=[(r.choice(A),C[0],r.randint(-10000,10000))]
        extra+=[(C[i],C[(i+1)%len(C)],-r.randint(1,10000)) for i in range(len(C))]
        E=extra+E[:max(0,m-len(extra))]
    if neg_unreach and len(B)>=2:
        c=r.sample(B,min(len(B),r.randint(2,5)))
        for i in range(len(c)):
            E[r.randrange(len(E))]=(c[i],c[(i+1)%len(c)],-r.randint(1,10000))
    r.shuffle(E)
    return f"{n} {len(E)} {S}\n"+"".join(f"{x} {y} {z}\n" for x,y,z in E)

def _pack(cs): return f"{len(cs)}\n"+"".join(cs)

def g18252(r):
    T=r.randint(1,10); cs=[]
    for _ in range(T):
        n=r.randint(1,8); m=r.randint(0,14)
        kind=r.random()
        if kind<0.35: cs.append(_case(r,n,max(m,n-1),'rand',wlo=-5,whi=20,reach_frac=r.choice([1,1,0.5])) if n>1 else f"1 {m} 1\n"+"".join(f"1 1 {r.randint(0,9)}\n" for _ in range(m)))
        elif kind<0.7 and n>1: cs.append(_case(r,n,max(m,n-1),'pot',neg_reach=r.random()<0.4,neg_unreach=r.random()<0.5,reach_frac=r.choice([1,0.6,0.3])))
        else:                               # 完全随机边（含自环、重边、孤立点）
            E=[(r.randint(1,n),r.randint(1,n),r.randint(-6,15)) for _ in range(m)]
            cs.append(f"{n} {m} {r.randint(1,n)}\n"+"".join(f"{x} {y} {z}\n" for x,y,z in E))
    return _pack(cs)

def _big(seed):
    r=random.Random(seed); out=[]
    # 满规模：每组 n=10000, m=20000，三组和恰为上限
    out.append(_pack([_case(r,10000,20000,'pot') for _ in range(3)]))
    out.append(_pack([_case(r,10000,20000,'pot',neg_reach=True),_case(r,10000,20000,'pot',neg_unreach=True,reach_frac=0.7),_case(r,10000,20000,'pot',reach_frac=0.5)]))
    out.append(_pack([_case(r,10000,20000,'pot',reach_frac=0.9,neg_unreach=True) for _ in range(3)]))
    # 长链：n=10000 一条负权链，最短路深度 n-1，|dist| 接近 1e8
    chain=f"10000 9999 1\n"+"".join(f"{i} {i+1} -10000\n" for i in range(1,10000))
    chain2=f"10000 10000 10000\n"+"".join(f"{i+1} {i} 10000\n" for i in range(1,10000))+"1 10000 -10000\n"
    out.append(_pack([chain,chain2]))
    # 末端负环：只有走完整条链才进入负圈
    tail=f"10000 10000 1\n"+"".join(f"{i} {i+1} 1\n" for i in range(1,10000))+"10000 9999 -2\n"
    out.append(_pack([tail]))
    # 10 组、每组 n=3000/m=6000，混合各种情况
    out.append(_pack([_case(r,3000,6000,'pot',neg_reach=(i%3==0),neg_unreach=(i%2==0),reach_frac=[1,0.8,0.4][i%3]) for i in range(10)]))
    # 边界：n=1、m=0；全部不可达
    out.append(_pack(["1 0 1\n","2 0 2\n","3 2 1\n2 3 -5\n3 2 -5\n","2 1 1\n1 1 -1\n","2 2 2\n2 2 0\n1 2 -10000\n"]))
    return out

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        d=Path(d); src=d/'main.py'
        src.write_text(REFERENCE); cmd=[sys.executable,str(src)]
        if LANGUAGE=="G++":
            exe=d/"main"; subprocess.run(["g++","-std=c++17","-O2",str(src),"-o",str(exe)],check=True)
            cmd=[str(exe)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 40)]+_big(4242)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text)
        (data/f"{i}.out").write_text(run(text))
if __name__=="__main__": main()
