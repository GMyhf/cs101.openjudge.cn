import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/18071 statistics, Accepted solution 52688789.\n# Source: http://cs101.openjudge.cn/practice/solution/52688789/\n# Statistics: http://cs101.openjudge.cn/practice/18071/statistics/\n# License: not declared on submission page; no license inferred\nimport sys\n\ndata = sys.stdin.read().strip().splitlines()\nM, N = map(int, data[0].strip().split())\nmatrix = []\nfor i in range(1, M + 1):\n    line = list(map(int, data[i].split()))\n    matrix.append(line)\ngraph = {(i, j): [] for i in range(M) for j in range(N)}\n\ndire = [(0, 1), (0, -1), (1, 0), (-1, 0)]\nfor i in range(M):\n    for j in range(N):\n        if matrix[i][j] == 1:\n            for dx, dy in dire:\n                if 0 <= i + dx <= M - 1 and 0 <= j + dy <= N - 1:\n\n                    if matrix[i + dx][j + dy] == 1:\n                        graph[(i, j)].append((i + dx, j + dy))\n\n\ndef topological_sort_dfs(M, N, graph):\n    visited = [[0] * N for _ in range(M)]\n\n    def dfs(i, j, fi, fj):\n        visited[i][j] = 1\n        for v in graph[(i, j)]:\n            if v[0] == fi and v[1] == fj:\n                continue\n            if visited[v[0]][v[1]] == 1:\n                return False\n            if visited[v[0]][v[1]] == 0:\n                if not dfs(v[0], v[1], i, j):\n                    return False\n        visited[i][j] = 2\n        return True\n\n    for i in range(M):\n        for j in range(N):\n            if visited[i][j] == 0:\n                if not dfs(i, j, -1, -1):\n                    return None\n    return 1\n\n\nt = topological_sort_dfs(M, N, graph)\nif not t:\n    print("YES")\nelse:\n    print("NO")\n'
LANGUAGE='Python3'
SAMPLE='2 3\n1 1 0\n1 1 1\n'
GENERATOR_NAME='g18071'
def valid(text):
    """题面：第一行 M N（M,N<=30，取正整数）；接下来 M 行每行 N 个整数，只可能为 0 或 1。"""
    if not text.endswith("\n"): return False
    lines=text[:-1].split("\n")
    try:
        head=lines[0].split()
        if len(head)!=2 or lines[0]!=" ".join(head): return False
        m,n=map(int,head)
    except ValueError:
        return False
    if not (1<=m<=30 and 1<=n<=30) or len(lines)!=m+1: return False
    for s in lines[1:]:
        t=s.split()
        if len(t)!=n or s!=" ".join(t) or any(x not in ("0","1") for x in t): return False
    return True

def _tree(r,m,n,keep):
    """在 m×n 格点上随机取点，再用并查集挑出一组无环的邻接边（随机生成森林），返回边集。"""
    cells=[(i,j) for i in range(m) for j in range(n) if r.random()<keep]
    on=set(cells); par={c:c for c in cells}
    def f(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    edges=[(a,(a[0]+di,a[1]+dj)) for a in cells for di,dj in ((0,1),(1,0)) if (a[0]+di,a[1]+dj) in on]
    r.shuffle(edges); used=set()
    for a,b in edges:
        if f(a)!=f(b): par[f(a)]=f(b); used.add((a,b))
    return used

def _forest_grid(r,m,n):
    """相邻碳原子一律算成键，所以把森林放大一倍画：节点放在偶数坐标，树边画成两节点间的中点格。
    这样 1 格之间的邻接恰好就是森林的边，整张图一定无环。"""
    hm,hn=(m+1)//2,(n+1)//2
    used=_tree(r,hm,hn,r.choice([1.0,0.9,0.7]))
    g=[[0]*n for _ in range(m)]
    nodes=set()
    for a,b in used:
        nodes.add(a); nodes.add(b)
        g[a[0]+b[0]][a[1]+b[1]]=1
    for a in nodes: g[2*a[0]][2*a[1]]=1
    for i in range(hm):
        for j in range(hn):
            if r.random()<0.1: g[2*i][2*j]=1      # 孤立原子
    return g

def g18071(r,kind):
    if kind=="legacy":                         # 原有形状：L 形（NO）或 2×2 方块（YES）
        m,n=r.randint(2,8),r.randint(2,8); g=[[0]*n for _ in range(m)]
        if r.random()<.5:
            for i in range(1,m): g[i][0]=1
            for j in range(n): g[0][j]=1
        else:
            for i in range(2):
                for j in range(2): g[i][j]=1
    elif kind=="random":                       # 随机密度
        m,n=r.randint(1,30),r.randint(1,30); p=r.choice([0.2,0.35,0.5,0.8])
        g=[[int(r.random()<p) for _ in range(n)] for _ in range(m)]
    elif kind=="forest":                       # 大规模无环（NO），卡「有大连通块就判 YES」之类错误
        m,n=r.choice([29,30,r.randint(5,30)]),r.choice([29,30,r.randint(5,30)])
        g=_forest_grid(r,m,n)
    elif kind=="forest_plus":                  # 无环森林再补一条边成大环（YES）
        m,n=r.choice([29,30]),r.choice([29,30])
        while True:
            g=_forest_grid(r,m,n)
            zs=[(i,j) for i in range(m) for j in range(n) if g[i][j]==0 and (i+j)%2==1]
            r.shuffle(zs)
            for i,j in zs:
                if i%2==0 and 0<j<n-1 and g[i][j-1] and g[i][j+1]: g[i][j]=1; break
                if i%2==1 and 0<i<m-1 and g[i-1][j] and g[i+1][j]: g[i][j]=1; break
            else: continue
            break
    elif kind=="ring":                         # 单个大环 / 边框（YES），以及断开一格（NO）
        m,n=r.randint(2,30),r.randint(2,30); g=[[0]*n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if i in (0,m-1) or j in (0,n-1): g[i][j]=1
        if r.random()<0.5: g[r.choice([0,m-1])][r.randrange(n)]=0
    return f"{len(g)} {len(g[0])}\n"+"\n".join(" ".join(map(str,x)) for x in g)+"\n"

SAMPLE2='3 3\n1 0 1\n0 1 0\n1 0 1\n'
FIXED=[SAMPLE2,"1 1\n0\n","1 1\n1\n","1 30\n"+" ".join(["1"]*30)+"\n","30 1\n"+"1\n"*30,
       "30 30\n"+("1 "*29+"1\n")*30,"30 30\n"+("0 "*29+"0\n")*30,"2 2\n1 1\n1 1\n","2 2\n1 1\n1 0\n"]
KINDS=["legacy"]*4+["random"]*10+["forest"]*6+["forest_plus"]*5+["ring"]*5

def build_cases():
    cases=[SAMPLE]+list(FIXED)
    for seed,kind in enumerate(KINDS,1):
        for attempt in range(100):
            t=g18071(random.Random(seed*1000+attempt),kind)
            if t not in cases: cases.append(t); break
        else: raise AssertionError("生成器多样性不足")
    return cases

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
    cases=build_cases()
    assert len(cases)==40 and all(valid(t) for t in cases)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text)
        (data/f"{i}.out").write_text(run(text))
if __name__=="__main__": main()
