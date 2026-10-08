import random, re, subprocess, tempfile
from pathlib import Path
REFERENCE="# include <bits/stdc++.h>\nusing namespace std;\nusing int64 = long long;\nconstexpr int64 INF = (1LL << 62);\nstruct Edge { int to; int next; int cost; };\nint main() {\n    ios::sync_with_stdio(false); cin.tie(nullptr);\n    int N, M; cin >> N >> M;\n    vector<vector<char>> village(N, vector<char>(M));\n    for (int r = 0; r < N; ++r) for (int c = 0; c < M; ++c) { int x; cin >> x; village[r][c] = x; }\n    vector<vector<int>> vertical(N, vector<int>(M + 1));\n    vector<vector<int>> horizontal(N + 1, vector<int>(M));\n    for (int r = 0; r < N; ++r) for (int c = 0; c <= M; ++c) cin >> vertical[r][c];\n    for (int r = 0; r <= N; ++r) for (int c = 0; c < M; ++c) cin >> horizontal[r][c];\n    const int columns = M + 1; const int pointCount = (N + 1) * (M + 1);\n    auto pointId = [&](int r, int c) { return r * columns + c; };\n    vector<int64> dist(pointCount, INF); vector<int> parent(pointCount, -1);\n    vector<char> visited(pointCount, false);\n    using State = pair<int64, int>;\n    priority_queue<State, vector<State>, greater<State>> heap;\n    dist[pointId(0, 0)] = 0; heap.push({0, pointId(0, 0)});\n    auto relax = [&](int u, int v, int cost) {\n        if (dist[v] > dist[u] + cost) { dist[v] = dist[u] + cost; parent[v] = u; heap.push({dist[v], v}); } };\n    while (!heap.empty()) {\n        auto [currentDistance, u] = heap.top(); heap.pop();\n        if (visited[u]) continue; visited[u] = true;\n        int r = u / columns; int c = u % columns;\n        if (r > 0) relax(u, pointId(r - 1, c), vertical[r - 1][c]);\n        if (r < N) relax(u, pointId(r + 1, c), vertical[r][c]);\n        if (c > 0) relax(u, pointId(r, c - 1), horizontal[r][c - 1]);\n        if (c < M) relax(u, pointId(r, c + 1), horizontal[r][c]);\n    }\n    vector<vector<char>> blockedVertical(N, vector<char>(M + 1, false));\n    vector<vector<char>> blockedHorizontal(N + 1, vector<char>(M, false));\n    auto markEdge = [&](int u, int v) -> bool {\n        int ur = u / columns, uc = u % columns, vr = v / columns, vc = v % columns;\n        if (ur == vr) { int c = min(uc, vc); bool old = blockedHorizontal[ur][c]; blockedHorizontal[ur][c] = true; return old; }\n        else { int r = min(ur, vr); bool old = blockedVertical[r][uc]; blockedVertical[r][uc] = true; return old; } };\n    for (int r = 0; r < N; ++r) for (int c = 0; c < M; ++c) {\n        if (!village[r][c]) continue;\n        int u = pointId(r, c);\n        while (u != pointId(0, 0)) { int p = parent[u]; if (markEdge(u, p)) break; u = p; } }\n    for (int r = 0; r < N; ++r) for (int c = 0; c < M; ++c) {\n        if (!village[r][c]) continue;\n        blockedHorizontal[r][c] = true; blockedHorizontal[r + 1][c] = true;\n        blockedVertical[r][c] = true; blockedVertical[r][c + 1] = true; }\n    const int expandedPointCount = 4 * pointCount;\n    auto stateId = [&](int r, int c, int quadrant) { return 4 * pointId(r, c) + quadrant; };\n    vector<int> head(expandedPointCount, -1); vector<Edge> edges;\n    edges.reserve(20LL * pointCount);\n    auto addDirectedEdge = [&](int u, int v, int cost) { edges.push_back({v, head[u], cost}); head[u] = (int)edges.size() - 1; };\n    auto addUndirectedEdge = [&](int u, int v, int cost) { addDirectedEdge(u, v, cost); addDirectedEdge(v, u, cost); };\n    for (int r = 0; r <= N; ++r) for (int c = 0; c <= M; ++c) {\n        bool isRoot = (r == 0 && c == 0);\n        if (!isRoot && (r == 0 || !blockedVertical[r - 1][c])) addUndirectedEdge(stateId(r,c,0), stateId(r,c,1), 0);\n        if (r == N || !blockedVertical[r][c]) addUndirectedEdge(stateId(r,c,2), stateId(r,c,3), 0);\n        if (!isRoot && (c == 0 || !blockedHorizontal[r][c - 1])) addUndirectedEdge(stateId(r,c,0), stateId(r,c,3), 0);\n        if (c == M || !blockedHorizontal[r][c]) addUndirectedEdge(stateId(r,c,1), stateId(r,c,2), 0); }\n    for (int r = 0; r < N; ++r) for (int c = 0; c < M; ++c) {\n        if (village[r][c]) continue;\n        addUndirectedEdge(stateId(r,c,2), stateId(r,c+1,3), horizontal[r][c]);\n        addUndirectedEdge(stateId(r,c+1,3), stateId(r+1,c+1,0), vertical[r][c+1]);\n        addUndirectedEdge(stateId(r+1,c+1,0), stateId(r+1,c,1), horizontal[r+1][c]);\n        addUndirectedEdge(stateId(r,c,2), stateId(r+1,c,1), vertical[r][c]); }\n    for (int r = 0; r < N; ++r) {\n        addUndirectedEdge(stateId(r,0,3), stateId(r+1,0,0), vertical[r][0]);\n        addUndirectedEdge(stateId(r,M,2), stateId(r+1,M,1), vertical[r][M]); }\n    for (int c = 0; c < M; ++c) {\n        addUndirectedEdge(stateId(0,c,1), stateId(0,c+1,0), horizontal[0][c]);\n        addUndirectedEdge(stateId(N,c,2), stateId(N,c+1,3), horizontal[N][c]); }\n    const int source = stateId(0,0,1); const int target = stateId(0,0,3);\n    vector<int64> answerDistance(expandedPointCount, INF); vector<char> finalized(expandedPointCount, false);\n    while (!heap.empty()) heap.pop();\n    answerDistance[source] = 0; heap.push({0, source});\n    while (!heap.empty()) {\n        auto [currentDistance, u] = heap.top(); heap.pop();\n        if (finalized[u]) continue; finalized[u] = true;\n        if (u == target) break;\n        for (int ei = head[u]; ei != -1; ei = edges[ei].next) {\n            const Edge &e = edges[ei]; int v = e.to;\n            int64 nd = currentDistance + (int64)e.cost;\n            if (nd < answerDistance[v]) { answerDistance[v] = nd; heap.push({nd, v}); } } }\n    cout << answerDistance[target] << '\\n';\n    return 0;\n}\n"
SAMPLE='3 3\n1 0 0\n1 0 0\n0 0 1\n1 4 9 4\n1 6 6 6\n1 2 2 9\n1 1 1\n4 4 4\n2 4 2\n6 6 6\n'
SAMPLE2='3 3\n1 0 1\n0 0 0\n0 1 0\n2 1 1 3\n5 6 1 1\n2 1 1 3\n2 1 1\n3 4 1\n4 1 1\n5 1 2\n'
# 题面提示：1<=N,M<=400，1<=v<=1e9，网格左上角为 1。
# 单组 .in 限 1MB：400x400 满规模只能用 1..9 的代价；大代价（卡 int 溢出）放在 150x150 规模。
MAXNM=400; MAXV=10**9

def valid(text):
    lines=text.split("\n")
    if lines[-1]!="": return False
    lines=lines[:-1]
    def ints(ln,k):
        t=ln.split(" ")
        if len(t)!=k or any(not re.fullmatch(r"0|[1-9][0-9]*",x) for x in t): return None
        return list(map(int,t))
    h=ints(lines[0],2) if lines else None
    if not h: return False
    n,m=h
    if not (1<=n<=MAXNM and 1<=m<=MAXNM): return False
    if len(lines)!=1+n+n+(n+1): return False
    for i in range(n):
        row=ints(lines[1+i],m)
        if row is None or any(x not in (0,1) for x in row): return False
        if i==0 and row[0]!=1: return False
    for i in range(n):
        row=ints(lines[1+n+i],m+1)
        if row is None or any(not 1<=x<=MAXV for x in row): return False
    for i in range(n+1):
        row=ints(lines[1+2*n+i],m)
        if row is None or any(not 1<=x<=MAXV for x in row): return False
    return True

def fmt(cells,vertical,horizontal):
    n,m=len(cells),len(cells[0])
    return (f"{n} {m}\n" + "\n".join(" ".join(map(str, row)) for row in cells) + "\n" +
            "\n".join(" ".join(map(str, row)) for row in vertical) + "\n" +
            "\n".join(" ".join(map(str, row)) for row in horizontal) + "\n")

def costs(r,n,m,mode,hi):
    if mode=="uniform":
        f=lambda i,j,o: r.randint(1,hi)
    elif mode=="lanes":   # 少数行/列整条很便宜，其余很贵：最优墙要走「走廊」（同一段走两次）
        cr={i for i in range(n+1) if r.random()<.15}|{0}; cc={j for j in range(m+1) if r.random()<.15}|{0}
        f=lambda i,j,o: r.randint(1,max(1,hi//1000)) if ((o=="v" and j in cc) or (o=="h" and i in cr)) else r.randint(hi//2,hi)
    elif mode=="noise":   # 大部分贵，随机少量便宜段
        f=lambda i,j,o: r.randint(1,max(1,hi//100)) if r.random()<.3 else r.randint(hi//2,hi)
    vertical=[[f(i,j,"v") for j in range(m+1)] for i in range(n)]
    horizontal=[[f(i,j,"h") for j in range(m)] for i in range(n+1)]
    return vertical,horizontal

def villages(r,n,m,mode,k):
    cells=[[0]*m for _ in range(n)]
    if mode=="sparse":
        for x,y in r.sample([(x,y) for x in range(n) for y in range(m)],min(k,n*m)): cells[x][y]=1
    elif mode=="density":
        p=k/100
        for x in range(n):
            for y in range(m):
                if r.random()<p: cells[x][y]=1
    elif mode=="blobs":   # k 个随机矩形村落群，可能围出空洞
        for _ in range(k):
            h,w=r.randint(1,max(1,n//6)),r.randint(1,max(1,m//6))
            x,y=r.randrange(n-h+1),r.randrange(m-w+1)
            hollow=r.random()<.4 and h>=3 and w>=3
            for i in range(x,x+h):
                for j in range(y,y+w):
                    if not hollow or i in (x,x+h-1) or j in (y,y+w-1): cells[i][j]=1
    elif mode=="full":
        cells=[[1]*m for _ in range(n)]
    elif mode=="edge":    # 村子都在网格最外一圈
        for x in range(n):
            for y in range(m):
                if (x in (0,n-1) or y in (0,m-1)) and r.random()<k/100: cells[x][y]=1
    cells[0][0]=1
    return cells

def gen(r,n,m,vmode,k,cmode,hi):
    cells=villages(r,n,m,vmode,k)
    v,h=costs(r,n,m,cmode,hi)
    return fmt(cells,v,h)

def g21520(r):
    # 小规模随机（村子数 <= 8，可用状压暴力核对）
    n,m=r.randint(1,12),r.randint(1,12)
    return gen(r,n,m,"sparse",r.randint(1,8),r.choice(("uniform","lanes","noise")),r.choice((12,1000,MAXV)))

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        d=Path(d); p=d/'main.cpp'; exe=d/'main'; p.write_text(REFERENCE)
        c=subprocess.run(['g++','-std=c++17','-O2',str(p),'-o',str(exe)],capture_output=True,text=True,timeout=60)
        if c.returncode: raise SystemExit(c.stderr)
        x=subprocess.run([str(exe)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    R=random.Random(21520)
    cases=[SAMPLE,SAMPLE2]
    cases.append(fmt([[1]],[[5,7]],[[MAXV],[MAXV]]))                       # 1x1
    cases.append(gen(R,1,MAXNM,"density",30,"uniform",MAXV))             # 单行
    cases.append(gen(R,MAXNM,1,"density",30,"uniform",MAXV))             # 单列
    cases.append(gen(R,2,2,"sparse",1,"uniform",9))                        # 只有首格
    for s in range(1,15):                                                  # 小规模随机，可暴力核对
        cases.append(g21520(random.Random(s)))
    for n,m,vm,k,cm,hi in ((40,40,"sparse",10,"lanes",MAXV),(40,40,"sparse",8,"noise",1000),
                           (40,37,"blobs",4,"uniform",MAXV),(30,40,"edge",20,"lanes",MAXV),
                           (60,60,"density",2,"lanes",MAXV),(80,100,"blobs",8,"noise",MAXV),
                           (100,100,"full",0,"uniform",MAXV),(120,90,"sparse",30,"lanes",MAXV),
                           (150,150,"density",1,"lanes",MAXV),(150,150,"blobs",10,"uniform",MAXV),
                           (150,150,"edge",10,"noise",MAXV),(200,200,"sparse",2,"lanes",9999),
                           (250,200,"blobs",12,"lanes",999),(300,300,"density",3,"lanes",99),
                           (MAXNM,300,"sparse",5,"lanes",99),(MAXNM,MAXNM,"sparse",3,"lanes",9),
                           (MAXNM,MAXNM,"density",2,"noise",9),(MAXNM,MAXNM,"blobs",15,"uniform",9),
                           (MAXNM,MAXNM,"edge",5,"lanes",9),(150,150,"full",0,"uniform",MAXV)):
        cases.append(gen(R,n,m,vm,k,cm,hi))
    assert len(cases)==40 and len(set(cases))==40
    for i,c in enumerate(cases):
        assert valid(c), i
        (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
