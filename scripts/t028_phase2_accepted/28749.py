# External reference: http://cs101.openjudge.cn/practice/28749/statistics/
# Accepted submission: 52718921
# Source: http://cs101.openjudge.cn/practice/solution/52718921/
# License: not declared on the submission page; no license is inferred.

import sys
sys.setrecursionlimit(1<<30)
from collections import deque

def solve() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    m = int(next(it))
    s = next(it).strip()
    col = {'R': 0, 'P': 1, 'W': 2}
    need = [0] * n
    for i, ch in enumerate(s):
        v = col[ch]
        need[i] = (-v) % 3
    stu_vol = [[] for _ in range(n)]
    vol_to_stu = [[] for _ in range(m)]
    for vol in range(m):
        k = int(next(it))
        lst = [int(next(it)) - 1 for _ in range(k)]
        vol_to_stu[vol] = lst
        for stu in lst:
            stu_vol[stu].append(vol)
    val = [-1] * m
    edges = []
    for stu in range(n):
        lst = stu_vol[stu]
        if not lst:
            if need[stu] != 0:
                print("impossible")
                return
        elif len(lst) == 1:
            v = lst[0]
            if val[v] == -1:
                val[v] = need[stu]
            elif val[v] != need[stu]:
                print("impossible")
                return
        else:
            u, v = lst[0], lst[1]
            edges.append((u, v, need[stu]))
    adj = [[] for _ in range(m)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    q = deque([i for i in range(m) if val[i] != -1])
    while q:
        u = q.popleft()
        for v, w in adj[u]:
            expected = (w - val[u]) % 3
            if val[v] == -1:
                val[v] = expected
                q.append(v)
            elif val[v] != expected:
                print("impossible")
                return
    visited = [False] * m
    total = 0
    for i in range(m):
        if val[i] != -1:
            total += val[i]
            visited[i] = True
    for i in range(m):
        if not visited[i] and val[i] == -1:
            comp = []
            dq = deque([i])
            visited[i] = True
            while dq:
                u = dq.popleft()
                comp.append(u)
                for v, _ in adj[u]:
                    if not visited[v] and val[v] == -1:
                        visited[v] = True
                        dq.append(v)
            best = None
            for root_val in range(3):
                tmp = {i: root_val}
                ok = True
                qq = deque([i])
                while qq:
                    u = qq.popleft()
                    cur = tmp[u]
                    for v, w in adj[u]:
                        exp = (w - cur) % 3
                        if v in tmp:
                            if tmp[v] != exp:
                                ok = False
                                break
                        else:
                            tmp[v] = exp
                            qq.append(v)
                    if not ok:
                        break
                if ok:
                    ssum = sum(tmp.values())
                    if best is None or ssum < best:
                        best = ssum
            if best is None:
                print("impossible")
                return
            total += best
    print(total)
if __name__ == "__main__":
    solve()
