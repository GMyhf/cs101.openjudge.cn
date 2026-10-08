import random, subprocess, sys, tempfile
from pathlib import Path

import re

_TOK = re.compile(r"\s*(?:(\((\d+),(\d+)\)(\d+))|(\((\d+)\)(\d+))|(\d+))")

def valid(text):
    # 题面：0<=n<=100, 0<=np<=n, 0<=nc<=n, 0<=m<=n^2；(u,v)z 中 0<=z<=1000，u,v 为 0..n-1，
    # 每个有序对至多一条线；(u)z 电站 0<=z<=10000、(u)z 用户 0<=z<=10000；电站与用户互不重复。
    pos, toks = 0, []
    while True:
        mt = _TOK.match(text, pos)
        if not mt or mt.end() == pos:
            break
        toks.append(mt); pos = mt.end()
    if text[pos:].strip():
        return False
    if not toks:
        return False
    i = 0
    def num():
        nonlocal i
        if i >= len(toks) or toks[i].group(8) is None: raise ValueError
        i += 1; return int(toks[i - 1].group(8))
    try:
        while i < len(toks):
            n, np_, nc, m = num(), num(), num(), num()
            if not (0 <= n <= 100 and 0 <= np_ <= n and 0 <= nc <= n and 0 <= m <= n * n):
                return False
            seen = set()
            for _ in range(m):
                if i >= len(toks) or toks[i].group(1) is None: return False
                u, v, z = int(toks[i].group(2)), int(toks[i].group(3)), int(toks[i].group(4)); i += 1
                if not (0 <= u < n and 0 <= v < n and 0 <= z <= 1000) or (u, v) in seen: return False
                seen.add((u, v))
            roles = set()
            for cnt in (np_, nc):
                for _ in range(cnt):
                    if i >= len(toks) or toks[i].group(5) is None: return False
                    u, z = int(toks[i].group(6)), int(toks[i].group(7)); i += 1
                    if not (0 <= u < n and 0 <= z <= 10000) or u in roles: return False
                    roles.add(u)
    except ValueError:
        return False
    return True

def ws(r):
    return r.choice([" ", " ", " ", "\n", "  ", "\t", "\n   "])

def dataset(r, n, np_, nc, m, lmax=1000, pmax=10000, cmax=10000, edges=None, self_loops=True):
    roles = r.sample(range(n), np_ + nc)
    stations, consumers = roles[:np_], roles[np_:]
    if edges is None:
        if m > n * n // 3:
            allp = [(u, v) for u in range(n) for v in range(n) if self_loops or u != v]
            edges = r.sample(allp, min(m, len(allp)))
        else:
            es = set()
            while len(es) < m:
                u, v = r.randrange(n), r.randrange(n)
                if self_loops or u != v: es.add((u, v))
            edges = list(es)
        r.shuffle(edges)
    toks = [str(n), str(np_), str(nc), str(len(edges))]
    toks += [f"({u},{v}){r.randint(0, lmax)}" for u, v in edges]
    toks += [f"({u}){r.randint(0, pmax)}" for u in stations]
    toks += [f"({u}){r.randint(0, cmax)}" for u in consumers]
    return "".join(t + ws(r) for t in toks).rstrip() + "\n"

def layered(r, n, width):
    # 电站 -> 若干层调度点 -> 用户，迫使多次增广
    nodes = list(range(n)); r.shuffle(nodes)
    np_ = width; nc = width
    stations, consumers, mid = nodes[:np_], nodes[np_:np_ + nc], nodes[np_ + nc:]
    layers = [stations] + [mid[i:i + width] for i in range(0, len(mid), width)] + [consumers]
    edges = []
    for a, b in zip(layers, layers[1:]):
        for u in a:
            for v in b:
                if r.random() < 0.7: edges.append((u, v))
    edges += [(v, u) for u, v in r.sample(edges, len(edges) // 5)
              if (v, u) not in set(edges)]
    edges = list(dict.fromkeys(edges)); r.shuffle(edges)
    toks = [str(n), str(np_), str(nc), str(len(edges))]
    toks += [f"({u},{v}){r.randint(1, 1000)}" for u, v in edges]
    toks += [f"({u}){r.randint(1000, 10000)}" for u in stations]
    toks += [f"({u}){r.randint(1000, 10000)}" for u in consumers]
    return "".join(t + ws(r) for t in toks).rstrip() + "\n"

def build_cases():
    r = random.Random(1459)
    cases = []
    # 小规模随机
    for _ in range(12):
        ds = []
        for _ in range(r.randint(1, 4)):
            n = r.randint(1, 10); np_ = r.randint(0, n); nc = r.randint(0, n - np_)
            ds.append(dataset(r, n, np_, nc, r.randint(0, n * n), lmax=r.choice([30, 1000]),
                              pmax=r.choice([50, 10000]), cmax=r.choice([50, 10000])))
        cases.append("".join(ds))
    # 边界：n=0、n=1、没有电站、没有用户、没有边、全零容量、原题面样例那样的自环
    cases.append("0 0 0 0\n1 0 0 0\n1 1 0 1 (0,0)5 (0)7\n2 1 1 0 (0)10 (1)10\n"
                 "2 1 1 1 (1,0)1000 (0)10000 (1)10000\n2 1 1 1 (0,1)1000\n(0)10000 (1)10000\n"
                 "3 1 1 2 (0,1)0 (1,2)9 (0)9 (2)9\n")
    cases.append(dataset(r, 50, 0, 20, 400) + dataset(r, 50, 20, 0, 400) + dataset(r, 30, 5, 5, 0))
    # 同一节点同时有出入、线容量是瓶颈 / 电站是瓶颈 / 用户是瓶颈
    cases.append(dataset(r, 40, 10, 10, 600, lmax=1000, pmax=50, cmax=10000) +
                 dataset(r, 40, 10, 10, 600, lmax=1000, pmax=10000, cmax=50) +
                 dataset(r, 40, 10, 10, 600, lmax=5, pmax=10000, cmax=10000))
    # 中等规模
    for _ in range(8):
        ds = []
        for _ in range(r.randint(1, 3)):
            n = r.randint(20, 60); np_ = r.randint(1, n // 3); nc = r.randint(1, n // 3)
            ds.append(dataset(r, n, np_, nc, r.randint(n, n * n // 2)))
        cases.append("".join(ds))
    # 分层图
    for w in (5, 10, 20):
        cases.append(layered(r, 100, w))
    # 满规模：n=100、m=n^2（含自环）、多组
    cases.append(dataset(r, 100, 30, 30, 10000))
    cases.append(dataset(r, 100, 50, 50, 10000, lmax=1000, pmax=10000, cmax=10000))
    cases.append(dataset(r, 100, 1, 1, 9900, self_loops=False) + dataset(r, 100, 1, 99, 5000))
    cases.append(dataset(r, 100, 45, 45, 3000) + dataset(r, 100, 10, 80, 8000) + dataset(r, 100, 80, 10, 8000))
    while len(cases) < 39:
        cases.append(dataset(r, 100, r.randint(1, 50), r.randint(1, 50), r.randint(200, 2000)))
    return cases

REFERENCE='// External reference: http://cs101.openjudge.cn/practice/01459/statistics/\n// Accepted submission: 51691692\n// Source: http://cs101.openjudge.cn/practice/solution/51691692/\n// License: not declared on the submission page; no license is inferred.\n\n#include <bits/stdc++.h>\nusing namespace std;\n\nstruct FastScanner {\n    // 读取下一个非负整数；到 EOF 返回 false\n    bool readInt(int &x) {\n        x = 0;\n        int c = getchar();\n        if (c == EOF) return false;\n        while (c != EOF && (c < \'0\' || c > \'9\')) c = getchar();\n        if (c == EOF) return false;\n        while (c != EOF && (c >= \'0\' && c <= \'9\')) {\n            x = x * 10 + (c - \'0\');\n            c = getchar();\n        }\n        return true;\n    }\n};\n\nstruct Dinic {\n    struct Edge {\n        int to, rev;\n        long long cap;\n    };\n    int N;\n    vector<vector<Edge>> G;\n    vector<int> level, it;\n\n    Dinic(int n=0) { init(n); }\n    void init(int n) {\n        N = n;\n        G.assign(N, {});\n        level.assign(N, 0);\n        it.assign(N, 0);\n    }\n\n    void addEdge(int fr, int to, long long cap) {\n        Edge a{to, (int)G[to].size(), cap};\n        Edge b{fr, (int)G[fr].size(), 0};\n        G[fr].push_back(a);\n        G[to].push_back(b);\n    }\n\n    bool bfs(int s, int t) {\n        fill(level.begin(), level.end(), -1);\n        queue<int> q;\n        level[s] = 0;\n        q.push(s);\n        while (!q.empty()) {\n            int v = q.front(); q.pop();\n            for (auto &e : G[v]) {\n                if (e.cap > 0 && level[e.to] < 0) {\n                    level[e.to] = level[v] + 1;\n                    q.push(e.to);\n                }\n            }\n        }\n        return level[t] >= 0;\n    }\n\n    long long dfs(int v, int t, long long f) {\n        if (v == t) return f;\n        for (int &i = it[v]; i < (int)G[v].size(); i++) {\n            Edge &e = G[v][i];\n            if (e.cap <= 0) continue;\n            if (level[e.to] != level[v] + 1) continue;\n            long long ret = dfs(e.to, t, min(f, e.cap));\n            if (ret > 0) {\n                e.cap -= ret;\n                G[e.to][e.rev].cap += ret;\n                return ret;\n            }\n        }\n        return 0;\n    }\n\n    long long maxflow(int s, int t) {\n        long long flow = 0;\n        while (bfs(s, t)) {\n            fill(it.begin(), it.end(), 0);\n            while (true) {\n                long long pushed = dfs(s, t, (long long)4e18);\n                if (!pushed) break;\n                flow += pushed;\n            }\n        }\n        return flow;\n    }\n};\n\nint main() {\n    FastScanner fs;\n    int n, np, nc, m;\n\n    while (true) {\n        if (!fs.readInt(n)) break;\n        fs.readInt(np); fs.readInt(nc); fs.readInt(m);\n\n        int S = n, T = n + 1;\n        Dinic dinic(n + 2);\n\n        for (int i = 0; i < m; i++) {\n            int u, v, z;\n            fs.readInt(u); fs.readInt(v); fs.readInt(z);\n            dinic.addEdge(u, v, z);\n        }\n\n        for (int i = 0; i < np; i++) {\n            int u, z;\n            fs.readInt(u); fs.readInt(z);\n            dinic.addEdge(S, u, z);\n        }\n\n        for (int i = 0; i < nc; i++) {\n            int u, z;\n            fs.readInt(u); fs.readInt(z);\n            dinic.addEdge(u, T, z);\n        }\n\n        cout << dinic.maxflow(S, T) << "\\n";\n    }\n    return 0;\n}\n'
LANGUAGE='G++'
SAMPLE='2 1 1 2 (0,1)20 (1,0)10 (0)15 (1)20\n7 2 3 13 (0,0)1 (0,1)2 (0,2)5 (1,0)1 (1,2)8 (2,3)1 (2,4)7\n         (3,5)2 (3,6)5 (4,2)7 (4,3)5 (4,5)1 (6,0)5\n         (0)5 (1)2 (3)2 (4)1 (5)4\n'

def run_all(cases):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp); src = tmp/('s.py' if LANGUAGE == 'Python3' else 's.cpp'); src.write_text(REFERENCE)
        cmd = [sys.executable, '-I', str(src)]
        if LANGUAGE != 'Python3':
            exe = tmp/'s'; subprocess.run(['g++', '-std=c++20', '-O2', '-pipe', str(src), '-o', str(exe)], check=True); cmd = [str(exe)]
        outs = []
        for x in cases:
            q = subprocess.run(cmd, input=x, text=True, capture_output=True, timeout=120, check=True)
            outs.append('\n'.join(line.rstrip() for line in q.stdout.rstrip().splitlines()) + '\n')
        return outs

def main():
    cases = [SAMPLE] + build_cases()
    for i, x in enumerate(cases):
        assert valid(x), f"第 {i} 组不满足题面约束"
    outs = run_all(cases)
    out = Path('data'); out.mkdir(exist_ok=True)
    for p in out.glob('*'): p.unlink()
    for i, (x, y) in enumerate(zip(cases, outs)):
        (out/f'{i}.in').write_text(x); (out/f'{i}.out').write_text(y)

if __name__ == '__main__':
    main()
