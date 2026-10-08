import random, subprocess, sys, tempfile
from pathlib import Path
def valid(text):
    """题面契约：多组，每组首行人数 N（1<=N<=100），随后 N 行：联系人数 c（0<=c<=N-1）
    与 c 对 (编号, 时间)，编号 1..N 且同一行互不相同，时间 1..10；以单独的 0 结束。"""
    import re
    if not text.endswith('\n'):return False
    lines=text[:-1].split('\n');i=0;sets=0
    def ints(s):
        t=s.split()
        if not t or not all(re.fullmatch(r'\d+',x) for x in t):return None
        return list(map(int,t))
    while True:
        if i>=len(lines):return False
        h=ints(lines[i]);i+=1
        if not h or len(h)!=1:return False
        N=h[0]
        if N==0:break
        if not 1<=N<=100:return False
        for _ in range(N):
            if i>=len(lines):return False
            v=ints(lines[i]);i+=1
            if not v or not 0<=v[0]<=N-1 or len(v)!=1+2*v[0]:return False
            ids=v[1::2];ts=v[2::2]
            if len(set(ids))!=len(ids) or not all(1<=x<=N for x in ids) or not all(1<=t<=10 for t in ts):return False
        sets+=1
    return i==len(lines) and sets>=1

def _best1125(n,adj):
    import heapq
    res=[]
    for s in range(1,n+1):
        d=[None]*(n+1);h=[(0,s)]
        while h:
            t,u=heapq.heappop(h)
            if d[u] is not None:continue
            d[u]=t
            for v,w in adj[u]:
                if d[v] is None:heapq.heappush(h,(t+w,v))
        if all(x is not None for x in d[1:]):res.append((max(d[1:]),s))
    return sorted(res)

def _inst1125(r,n,kind):
    while True:
        adj=[[] for _ in range(n+1)]
        dens=r.choice([0.02,0.05,0.1,0.3,1.0])
        for u in range(1,n+1):
            vs=[v for v in range(1,n+1) if v!=u and r.random()<dens]
            adj[u]=[(v,r.choice([1,10,r.randint(1,10)])) for v in vs]
        if kind!='disjoint' and n>1:   # 加一条随机 Hamilton 环保证强连通
            p=list(range(1,n+1));r.shuffle(p)
            for k in range(n):
                u,v=p[k],p[(k+1)%n]
                if all(x!=v for x,_ in adj[u]):adj[u].append((v,r.randint(1,10)))
            if kind=='tree':   # 从某人出发的单向树，仅他可达所有人
                adj=[[] for _ in range(n+1)];root=p[0]
                for k in range(1,n):
                    par=p[r.randrange(k)];adj[par].append((p[k],r.randint(1,10)))
        elif kind=='disjoint' and n>1:
            # 某人入度为 0 且另有一人出度为 0 => 无人能传遍
            a,b=r.sample(range(1,n+1),2)
            for u in range(1,n+1):adj[u]=[(v,w) for v,w in adj[u] if v!=a]
            adj[b]=[]
        for u in range(1,n+1):r.shuffle(adj[u])
        res=_best1125(n,adj)
        if kind=='disjoint' and res:continue
        if kind!='disjoint' and not res:continue
        if len(res)>=2 and res[0][0]==res[1][0]:continue   # 题面未规定并列取谁，避开并列
        return f'{n}\n'+''.join(f'{len(adj[u])}'+''.join(f' {v} {w}' for v,w in adj[u])+'\n' for u in range(1,n+1))

def g1125(k):
    r=random.Random(k)
    if k==1:parts=['1\n0\n','2\n1 2 3\n0\n','2\n1 2 1\n1 1 4\n','2\n1 2 7\n1 1 2\n']
    elif k==2:parts=[_inst1125(r,100,'conn') for _ in range(3)]
    elif k==3:parts=[_inst1125(r,100,'disjoint'),_inst1125(r,100,'tree')]
    elif k>=35:parts=[_inst1125(r,100,r.choice(['conn','conn','tree','disjoint'])) for _ in range(6)]
    else:parts=[_inst1125(r,r.choice([r.randint(2,10),r.randint(2,100)]),r.choice(['conn','conn','tree','disjoint'])) for _ in range(r.randint(1,6))]
    return ''.join(parts)+'0\n'

REFERENCE="# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 1125: Stockbroker Grapevine\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/practice/01125/\n# License: not declared in source collection; no license is inferred.\nimport heapq\nwhile True:\n    n=int(input())\n    if n==0:\n        break\n    contact=[{}]\n    for _ in range(n):\n        list1=list(map(int,input().split()))\n        dict1={}\n        for i in range((len(list1)-1)//2):\n            dict1[list1[2*i+1]]=list1[2*i+2]\n        contact.append(dict1)\n    i0=0\n    s=float('inf')\n    for i in range(1,n+1):\n        heap=[(0,i)]\n        heapq.heapify(heap)\n        time=[0]+[float('inf')]*n\n        time[i]=0\n        condition=[True]+[False]*n\n        while heap:\n            t,j=heapq.heappop(heap)\n            if condition[j]:\n                continue\n            condition[j]=True\n            if sum(condition)==n+1:\n                if max(time)<s:\n                    s=max(time)\n                    i0=i\n                break\n            for k in contact[j]:\n                t1=t+contact[j][k]\n                if not condition[k] and time[k]>t1:\n                    time[k]=t1\n                    heapq.heappush(heap,(t1,k))\n    if i0==0:\n        print('disjoint')\n    else:\n        print(f'{i0} {s}')\n"
SAMPLE='3\n2 2 4 3 5\n2 1 2 3 6\n2 1 2 2 2\n5\n3 4 4 2 8 5 3\n1 5 8\n4 1 6 4 10 2 7 5 2\n0\n2 2 5 1 5\n0\n'
GENERATOR='g1125'

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as folder:
        script=Path(folder)/"main.py"; script.write_text(REFERENCE)
        result=subprocess.run([sys.executable,"-I",str(script)],input=text,text=True,capture_output=True,timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    for old in data.glob("*"): old.unlink()
    cases=[SAMPLE]+[globals()[GENERATOR](seed) for seed in range(1, 40)]
    for i,case in enumerate(cases):
        assert valid(case),i
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()
