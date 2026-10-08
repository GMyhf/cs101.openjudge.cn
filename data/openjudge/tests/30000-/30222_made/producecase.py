import random
REFERENCE="# External reference: /practice/30222/statistics/\n# Accepted submission: 52829485\n# Source: http://cs101.openjudge.cn/practice/solution/52829485/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\nfrom collections import deque\n\ndef solve():\n    # 读取所有输入\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    N = int(input_data[0])\n    M = int(input_data[1])\n    \n    # 任务耗时，采用1-based索引\n    T = [0] + [int(x) for x in input_data[2:2+N]]\n    \n    adj = [[] for _ in range(N + 1)]\n    in_degree = [0] * (N + 1)\n    \n    # 构建邻接表和入度数组\n    idx = 2 + N\n    for _ in range(M):\n        if idx >= len(input_data):\n            break\n        u = int(input_data[idx])\n        v = int(input_data[idx+1])\n        adj[u].append(v)\n        in_degree[v] += 1\n        idx += 2\n        \n    # 拓扑排序队列\n    queue = deque()\n    dp = [0] * (N + 1)\n    \n    # 初始化入度为 0 的节点\n    for i in range(1, N + 1):\n        dp[i] = T[i]\n        if in_degree[i] == 0:\n            queue.append(i)\n            \n    processed_count = 0\n    \n    # 拓扑排序与动态规划更新\n    while queue:\n        u = queue.popleft()\n        processed_count += 1\n        for v in adj[u]:\n            if dp[u] + T[v] > dp[v]:\n                dp[v] = dp[u] + T[v]\n            in_degree[v] -= 1\n            if in_degree[v] == 0:\n                queue.append(v)\n                \n    # 判断是否存在环\n    if processed_count < N:\n        print(-1)\n    else:\n        print(max(dp))\n\nif __name__ == '__main__':\n    solve()"
SAMPLE='3 2\n5 10 5\n1 2\n1 3\n'
GENERATOR_NAME='g30222'
CPP=False
def valid(text):
    # 题面：第一行 N M；第二行 N 个 T_i；接着 M 行 u v（任务编号 1..N）；1<=N<=2000，1<=M<=1e5，1<=T_i<=100
    if not text.endswith('\n'): return False
    lines = text[:-1].split('\n')
    try:
        rows = [[int(x) for x in ln.split(' ')] for ln in lines]
    except ValueError: return False
    if len(rows) < 2 or len(rows[0]) != 2: return False
    n, m = rows[0]
    if not (1 <= n <= 2000 and 1 <= m <= 100000) or len(rows) != m + 2: return False
    if len(rows[1]) != n or any(not (1 <= t <= 100) for t in rows[1]): return False
    return all(len(e) == 2 and 1 <= e[0] <= n and 1 <= e[1] <= n for e in rows[2:])

def g30222(r):
    n = r.randint(2, 30); edges = [(i, r.randint(1, i-1)) for i in range(2, n+1) if r.random()<.5]
    return f"{n} {len(edges)}\n{' '.join(str(r.randint(1,100)) for _ in range(n))}\n" + "\n".join(f"{a} {b}" for a,b in edges) + "\n"

def fmt(n, T, edges):
    return f"{n} {len(edges)}\n{' '.join(map(str,T))}\n" + "\n".join(f"{a} {b}" for a,b in edges) + "\n"

def relabel(r, n, edges, shuffle_edges=True):
    perm = list(range(1, n + 1)); r.shuffle(perm)
    e = [(perm[a - 1], perm[b - 1]) for a, b in edges]
    if shuffle_edges: r.shuffle(e)
    return e

def rand_dag(r, n, m):
    # 按拓扑序 1..n 只连前往后的边，互不重复
    s = set()
    while len(s) < m:
        a, b = r.randint(1, n), r.randint(1, n)
        if a < b: s.add((a, b))
    return sorted(s)

def extra_cases():
    r = random.Random(30222)
    N, M = 2000, 100000
    out = []
    out.append(fmt(2, [3, 4], [(1, 2), (2, 1)]))                  # 最小的环 -> -1
    out.append(fmt(2, [100, 1], [(2, 1)]))
    out.append(fmt(3, [1, 1, 100], [(1, 2)]))                     # 孤立点耗时最大
    out.append(fmt(4, [5, 5, 5, 5], [(1, 2), (2, 3), (3, 2)]))    # 环之外还有入度 0 的点
    out.append(fmt(5, [1, 2, 3, 4, 5], [(1, 2), (1, 2), (2, 3)])) # 重复边
    # 满规模随机 DAG
    T = [r.randint(1, 100) for _ in range(N)]
    out.append(fmt(N, T, relabel(r, N, rand_dag(r, N, M))))
    T = [100] * N
    out.append(fmt(N, T, relabel(r, N, rand_dag(r, N, M))))
    # 长链 N=2000：答案 200000，递归 DFS 会爆栈
    chain = [(i, i + 1) for i in range(1, N)]
    out.append(fmt(N, [100] * N, chain))
    out.append(fmt(N, [r.randint(1, 100) for _ in range(N)], relabel(r, N, chain)))
    # 长链 + 稠密的前向边，M=1e5
    e = sorted(set(chain) | set(rand_dag(r, N, M - len(chain))))
    while len(e) < M:
        a, b = sorted(r.sample(range(1, N + 1), 2)); 
        if (a, b) not in set(e): e.append((a, b))
    out.append(fmt(N, [r.randint(1, 100) for _ in range(N)], relabel(r, N, e[:M])))
    # 整个大环
    cyc = [(i, i % N + 1) for i in range(1, N + 1)]
    out.append(fmt(N, [r.randint(1, 100) for _ in range(N)], relabel(r, N, cyc)))
    # 满规模 DAG 中加一条回边，在深处形成环
    e = rand_dag(r, N, M - 1) + [(1900, 100)]
    out.append(fmt(N, [r.randint(1, 100) for _ in range(N)], relabel(r, N, e)))
    # 链末端一个自成一体的小环，其余都是 DAG
    e = chain[:1500] + [(1700, 1701), (1701, 1702), (1702, 1700)]
    out.append(fmt(N, [r.randint(1, 100) for _ in range(N)], relabel(r, N, e)))
    # 星形：一个源点指向所有点 / 所有点指向一个汇点
    out.append(fmt(N, [r.randint(1, 100) for _ in range(N)], relabel(r, N, [(1, i) for i in range(2, N + 1)])))
    out.append(fmt(N, [r.randint(1, 100) for _ in range(N)], relabel(r, N, [(i, N) for i in range(1, N)])))
    # 中等规模随机 DAG 与有环图
    for _ in range(4):
        n = r.randint(50, 2000); m = r.randint(1, min(M, n * (n - 1) // 2))
        out.append(fmt(n, [r.randint(1, 100) for _ in range(n)], relabel(r, n, rand_dag(r, n, m))))
    for _ in range(3):
        n = r.randint(50, 2000); m = r.randint(n, min(M, n * (n - 1) // 2))
        e = rand_dag(r, n, m); a, b = r.choice(e); e.append((b, a))
        out.append(fmt(n, [r.randint(1, 100) for _ in range(n)], relabel(r, n, e)))
    return out

from pathlib import Path
import subprocess, sys, tempfile
def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/('main.cpp' if CPP else 'main.py'); p.write_text(REFERENCE)
        if CPP:
            exe=Path(d)/'main'; c=subprocess.run(['g++','-O2','-std=c++17',str(p),'-o',str(exe)],capture_output=True,text=True,timeout=30)
            if c.returncode: raise SystemExit(c.stderr)
            cmd=[str(exe)]
        else: cmd=[sys.executable,str(p)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1, 40)]+extra_cases()
    assert all(valid(c) for c in cases) and len(set(cases))==len(cases)
    for i,c in enumerate(cases): (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
