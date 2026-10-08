import random,re,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='import heapq\n\nk = int(input())\nn = int(input())\nroad = [set() for i in range(n + 1)]\nfor i in range(int(input())):\n    s, d, l, t = map(int, input().split())\n    road[s].add((d, l, t))\n\ndis = [{} for i in range(n + 1)]\ndis[1][0] = 0\nh = [(0, 1, 0)]\n\nwhile h:\n    d, u, c = heapq.heappop(h)\n    if u == n:\n        print(d)\n        break\n    for v, l, t in road[u]:\n        if c + t > k:\n            continue\n        if c + t not in dis[v] or d + l < dis[v][c + t]:\n            dis[v][c + t] = d + l\n            heapq.heappush(h, (d + l, v, c + t))\nelse:\n    print(-1)'
SAMPLE='5\n6\n7\n1 2 2 3\n2 4 3 3\n3 4 2 4\n1 3 4 1\n4 6 2 1\n3 5 2 0\n5 4 3 2\n'
GENERATOR_NAME='g7735'
def valid(text):
    """题面：K（0≤K≤10000）、N（2≤N≤100）、R（1≤R≤10000）各占一行；随后 R 行「S D L T」，
    1≤S,D≤N，1≤L≤100，0≤T≤100，空格分隔。"""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if len(lines) < 3 or not all(re.fullmatch(r"0|[1-9][0-9]*", x) for x in lines[:3]):
        return False
    k, n, r = map(int, lines[:3])
    if not (0 <= k <= 10000 and 2 <= n <= 100 and 1 <= r <= 10000) or len(lines) != 3 + r:
        return False
    for line in lines[3:]:
        e = re.fullmatch(r"(0|[1-9][0-9]*) (0|[1-9][0-9]*) (0|[1-9][0-9]*) (0|[1-9][0-9]*)", line)
        if not e:
            return False
        s, d, l, t = map(int, e.groups())
        if not (1 <= s <= n and 1 <= d <= n and 1 <= l <= 100 and 0 <= t <= 100):
            return False
    return True


def rand_edges(r,n,m,lmax=100,tmax=100,forward_only=False):
    es=[]
    for _ in range(m):
        u=r.randint(1,n); v=r.randint(1,n)
        if forward_only and u>=v: u,v=min(u,v),max(u,v)
        if u==v and r.random()<.8: v=v%n+1          # 少量自环，题面未禁止
        es.append((u,v,r.randint(1,lmax),r.randint(0,tmax)))
    return es

def trap(r,n,k):
    # 短而贵的路 vs 长而便宜的路：只看长度的贪心会超预算；按城市记 visited 的 Dijkstra 会错
    es=[]
    mid=list(range(2,n)); r.shuffle(mid)
    a,b=mid[:len(mid)//2],mid[len(mid)//2:]
    path_a=[1]+a+[n]; path_b=[1]+b+[n]
    ca=k+r.randint(1,5); cb=r.randint(0,k)            # a 路超预算，b 路在预算内
    for path,cost,lo,hi in ((path_a,ca,1,3),(path_b,cb,20,100)):
        m=len(path)-1; parts=[cost//m]*m
        for i in range(cost%m): parts[i]+=1
        for i in range(m):
            es.append((path[i],path[i+1],r.randint(lo,hi),min(100,parts[i])))
    # 交叉边：便宜但长，接到短路中段
    for _ in range(n):
        u=r.choice(path_a); v=r.choice(path_b)
        es.append((u,v,r.randint(1,100),r.randint(0,100)))
        es.append((v,u,r.randint(1,100),r.randint(0,100)))
    return es

def tradeoff(r,n,m,layers):
    # 分层图：边长与通行费此消彼长（短路贵、长路便宜），并带少量回边成环；
    # 预算卡在中间，最优解必须在长度与花费之间权衡
    nodes=list(range(2,n)); r.shuffle(nodes)
    w=len(nodes)//layers; lay=[[1]]+[nodes[i*w:(i+1)*w] for i in range(layers)]+[[n]]
    lay[-2]+=nodes[layers*w:]
    es=[]
    while len(es)<m:
        i=r.randrange(len(lay)-1)
        if r.random()<.05 and i>0:        # 回边
            u=r.choice(lay[i]); v=r.choice(lay[i-1])
        else:
            u=r.choice(lay[i]); v=r.choice(lay[i+1])
        l=r.randint(1,100); t=max(0,min(100,100-l+r.randint(-10,10)))
        es.append((u,v,l,t))
    return es

def g7735(r,seed):
    if seed<=3:                       # 最小规模 N=2
        n=2; k=[0,5,0][seed-1]
        es=[(1,2,r.randint(1,100),[0,7,3][seed-1])]
        if seed==3: es.append((2,1,1,0))                 # 只有反向的免费路 → -1
    elif seed<=14:                    # 小图随机（含回边、重边、自环）
        n=r.randint(3,10); k=r.randint(0,60)
        es=rand_edges(r,n,r.randint(1,30),r.choice([5,100]),r.choice([3,30,100]))
    elif seed<=20:                    # 小图陷阱
        n=r.randint(4,12); k=r.randint(5,60); es=trap(r,n,k)
    elif seed<=23:                    # -1：N 不可达 / 预算不够
        n=r.randint(5,100); k=r.randint(0,200)
        if seed==21:
            es=[e for e in rand_edges(r,n,r.randint(1,3000)) if e[1]!=n]
            es=es or [(1,1,1,0)]
        else:
            es=[(u,v,l,max(t,1) if v==n else t) for u,v,l,t in rand_edges(r,n,r.randint(10,2000))]
            es+=[(u,n,l,min(100,k+1)) for u,v,l,t in rand_edges(r,n,5)]
            k=min(k,100)
            es=[(u,v,l,(k+1 if v==n and k+1<=100 else t)) for u,v,l,t in es]
    elif seed<=30:                    # 中等规模
        n=r.randint(20,100); k=r.choice([0,r.randint(1,500),r.randint(500,3000)])
        es=rand_edges(r,n,r.randint(100,3000),100,r.choice([10,100]))
    else:                             # 满规模：N=100, R=10000, K 取到 10000
        n=100; k=[10000,10000,5000,1000,300,10000,100,2000,10000][seed-31]
        es=rand_edges(r,n,10000,100,r.choice([100,100,20]),forward_only=(seed%3==0))
        if seed in (36,37): es=trap(r,n,min(k,100*40))[:200]+es[:9800]
        if seed in (32,33,34,35,38,39):
            # (层数, 边数, 预算系数)：参考解在满规模下状态数随层数×预算膨胀，
            # 这里按「参考解单组 ≤ Python 时限一半（5s）」挑参数
            layers,m,f={32:(5,10000,.8),33:(7,10000,.7),34:(15,3000,.8),35:(20,2000,.8),38:(49,1000,.8),39:(98,400,None)}[seed]
            es=tradeoff(r,n,m,layers)
            k=10000 if f is None else int(50*(layers+1)*f)
    r.shuffle(es)
    return f"{k}\n{n}\n{len(es)}\n"+"\n".join(" ".join(map(str,e)) for e in es)+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"; p.write_text(REFERENCE,encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[g7735(random.Random(seed),seed) for seed in range(1, 40)]
    assert all(valid(t) for t in cases), "有数据越出题面约束"
    assert len(set(cases))==len(cases), "有重复数据"
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text,encoding="utf-8")
        (data/f"{i}.out").write_text(run(text),encoding="utf-8")
if __name__=="__main__": main()
