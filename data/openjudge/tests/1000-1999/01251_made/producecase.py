import random,subprocess,sys,tempfile
from pathlib import Path
import re

# ---- 输入契约（照题面）：1~100 个数据集，最后一行 0。每个数据集首行 n（1<n<27），
# 接着 n-1 行，按字母顺序依次为 A.. 第 n-1 个村庄：村名 k，再跟 k 对 "村名 费用"，
# 这些村庄编号都在本村之后（不重复），费用为不超过 100 的正整数；
# 路总数不超过 75，每个村庄关联的路不超过 15 条；题意要求所有村落能互相到达，故图连通。
_INT=re.compile(r'(0|[1-9][0-9]*)$')
def valid(text):
    try:
        if not text.endswith('\n'): return False
        lines=text[:-1].split('\n')
        if lines[-1]!='0': return False
        i=0;ds=0
        while lines[i]!='0':
            if not _INT.match(lines[i]): return False
            n=int(lines[i]);i+=1;ds+=1
            if not 1<n<27: return False
            deg=[0]*n;tot=0;adj=[set() for _ in range(n)]
            for v in range(n-1):
                t=lines[i].split(' ');i+=1
                if t[0]!=chr(65+v) or not _INT.match(t[1]): return False
                k=int(t[1])
                if len(t)!=2+2*k: return False
                for q in range(k):
                    u,c=t[2+2*q],t[3+2*q]
                    if len(u)!=1 or not 'A'<=u<=chr(64+n) or not _INT.match(c): return False
                    ui=ord(u)-65
                    if ui<=v or ui in adj[v] or not 1<=int(c)<=100: return False
                    adj[v].add(ui);adj[ui].add(v);deg[v]+=1;deg[ui]+=1;tot+=1
            if tot>75 or max(deg)>15: return False
            seen={0};st=[0]
            while st:
                x=st.pop()
                for y in adj[x]:
                    if y not in seen: seen.add(y);st.append(y)
            if len(seen)!=n: return False
        return i==len(lines)-1 and 1<=ds<=100
    except Exception:
        return False

def _dataset(r,n,m,wmax=100,shape='rand'):
    # n 个村庄、目标 m 条路（受 75 条/度数 15 限制），先造生成树保证连通
    perm=list(range(n));r.shuffle(perm)
    deg=[0]*n;E={}
    def add(a,b,w):
        a,b=min(a,b),max(a,b)
        if a==b or (a,b) in E or deg[a]>=15 or deg[b]>=15: return False
        E[(a,b)]=w;deg[a]+=1;deg[b]+=1;return True
    for i in range(1,n):
        while True:
            if shape=='path': p=perm[i-1]
            else: p=perm[r.randrange(max(0,i-3) if shape=='deep' else 0,i)]
            if add(perm[i],p,r.randint(1,wmax)) or shape=='path': break
    tries=0
    while len(E)<min(m,75) and tries<20000:
        tries+=1;add(r.randrange(n),r.randrange(n),r.randint(1,wmax))
    rows=[]
    for v in range(n-1):
        nb=sorted((b,w) for (a,b),w in E.items() if a==v)
        rows.append(" ".join([chr(65+v),str(len(nb))]+[f"{chr(65+b)} {w}" for b,w in nb]))
    return f"{n}\n"+"\n".join(rows)

def generate(seed):
    r=random.Random(1251*1_000_003+seed)
    ds=[]
    if seed==1: ds=[_dataset(r,2,1),"2\nA 1 B 100","2\nA 1 B 1"]
    elif seed==2: ds=[_dataset(r,26,25,shape='path') for _ in range(3)]      # 只有树：答案为全部路费之和
    elif seed==3: ds=[_dataset(r,26,75) for _ in range(100)]                 # 100 个满规模数据集
    elif seed==4: ds=[_dataset(r,26,75,wmax=2) for _ in range(30)]           # 大量等权边
    elif seed==5: ds=[_dataset(r,26,75,wmax=1) for _ in range(5)]+[_dataset(r,n,75) for n in (3,4,5,6,12,13)]
    elif seed==6: ds=[_dataset(r,26,75,shape='deep') for _ in range(50)]
    else:
        for _ in range(r.randint(1,100) if seed%2 else r.randint(1,10)):
            n=r.choice([r.randint(2,26),26,r.randint(20,26)])
            ds.append(_dataset(r,n,r.choice([n-1,r.randint(n-1,75),75]),wmax=r.choice([100,100,10]),shape=r.choice(['rand','rand','deep'])))
    return "\n".join(ds)+"\n0\n"

REFERENCE="# External reference: http://cs101.openjudge.cn/practice/01251/statistics/\n# Accepted submission: 51699516\n# Source: http://cs101.openjudge.cn/practice/solution/51699516/\n# License: not declared on the submission page; no license is inferred.\n\nwhile True:\n    n = int(input())\n    if n == 0:\n        break\n    INF = float('inf')\n    matrix = [[INF]*n for _ in range(n)]\n    for _ in range(n-1):\n        inp = input().split()\n        village = inp[0]\n        v1 = ord(village)-ord('A')\n        num = int(inp[1])\n        for i in range(1, num+1):\n            neighbor, cost = inp[2*i], int(inp[2*i+1])\n            v2 = ord(neighbor)-ord('A')\n            matrix[v1][v2] = cost\n            matrix[v2][v1] = cost\n    total_cost = 0\n    visited = [False]*n\n    min_edge = [INF]*n\n    min_edge[0] = 0\n    for _ in range(n):\n        u = -1\n        for v in range(n):\n            if not visited[v] and (u == -1 or min_edge[v] < min_edge[u]):\n                u = v\n        visited[u] = True\n        total_cost += min_edge[u]\n        for v in range(n):\n            if matrix[u][v] < INF and not visited[v]:\n                if matrix[u][v] < min_edge[v]:\n                    min_edge[v] = matrix[u][v]\n    print(total_cost)\n"
NUMBER=1251
SAMPLE='9\nA 2 B 12 I 25\nB 3 C 10 H 40 I 8\nC 2 D 18 G 55\nD 1 E 44\nE 2 F 60 G 38\nF 0\nG 1 H 35\nH 1 I 35\n3\nA 2 B 10 C 40\nB 1 C 20\n0\n'
CASES=40
def run(x):
 with tempfile.TemporaryDirectory() as t:
  p=Path(t)/'s.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)
  if q.returncode:raise SystemExit(q.stderr)
  return '\n'.join(line.rstrip() for line in q.stdout.rstrip().splitlines())+'\n'
def main():
 d=Path('data');d.mkdir(exist_ok=True)
 for p in d.glob('*'):p.unlink()
 for i,x in enumerate([SAMPLE]+[generate(s) for s in range(1, CASES)]):
  assert valid(x),i
  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))
if __name__=='__main__':main()
