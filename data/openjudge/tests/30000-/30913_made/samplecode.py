# External reference: http://cs101.openjudge.cn/practice/30913/statistics/
# Accepted submission: 52756598
# Source: http://cs101.openjudge.cn/practice/solution/52756598/
# License: not declared on the submission page; no license is inferred.

import sys


def solve():
    # 使用 sys.stdin.read 快速读取输入，防止 I/O 成为瓶颈
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    m = int(input_data[1])

    adj = [[] for _ in range(n + 1)]
    radj = [[] for _ in range(n + 1)]

    idx = 2
    for _ in range(m):
        u = int(input_data[idx])
        v = int(input_data[idx + 1])
        w = int(input_data[idx + 2])
        adj[u].append((v, w))
        radj[v].append(u)
        idx += 3

    s = int(input_data[idx])

    # ---------------- Kosaraju 算法求强连通分量 (SCC) ----------------

    # 步骤 1：在原图上运行非递归 DFS，求得后序遍历序列
    visited = [False] * (n + 1)
    order = []

    for i in range(1, n + 1):
        if not visited[i]:
            state_stack = [(i, 0)]
            visited[i] = True
            while state_stack:
                u, edge_idx = state_stack[-1]
                if edge_idx < len(adj[u]):
                    v, _ = adj[u][edge_idx]
                    state_stack[-1] = (u, edge_idx + 1)
                    if not visited[v]:
                        visited[v] = True
                        state_stack.append((v, 0))
                else:
                    order.append(u)
                    state_stack.pop()

    # 步骤 2：在反图上，按照后序遍历的逆序进行非递归 DFS，划分 SCC
    visited2 = [False] * (n + 1)
    scc_id = [-1] * (n + 1)
    scc_count = 0

    for u in reversed(order):
        if not visited2[u]:
            stack = [u]
            visited2[u] = True
            while stack:
                curr = stack.pop()
                scc_id[curr] = scc_count
                for v in radj[curr]:
                    if not visited2[v]:
                        visited2[v] = True
                        stack.append(v)
            scc_count += 1

    # ---------------- 榨干单条边能获得的最大愉悦度 ----------------
    def harvest(w):
        if w <= 0:
            return 0
        # 求解 T * (T - 1) / 2 < w 时的最大正整数 T
        val = 1 + 8 * w
        r = int(val**0.5)
        T = (1 + r) // 2
        # 对 T 进行微调以确保 100% 精确
        while T * (T - 1) // 2 >= w:
            T -= 1
        while (T + 1) * T // 2 < w:
            T += 1
        return T * w - (T - 1) * T * (T + 1) // 6

    # ---------------- 缩点构建 DAG ----------------
    scc_val = [0] * scc_count
    dag_edges = [{} for _ in range(scc_count)]

    for u in range(1, n + 1):
        su = scc_id[u]
        for v, w in adj[u]:
            sv = scc_id[v]
            if su == sv:
                # 强连通分量内部的边可以被无限次榨干
                scc_val[su] += harvest(w)
            else:
                # 强连通分量之间的跨越边，只能走一次，多条边时保留权值最大的一条
                if sv not in dag_edges[su] or dag_edges[su][sv] < w:
                    dag_edges[su][sv] = w

    # ---------------- 拓扑排序 (Kahn 算法) ----------------
    in_degree = [0] * scc_count
    for su in range(scc_count):
        for sv in dag_edges[su]:
            in_degree[sv] += 1

    from collections import deque

    queue = deque([i for i in range(scc_count) if in_degree[i] == 0])
    topo_order = []
    while queue:
        u = queue.popleft()
        topo_order.append(u)
        for v in dag_edges[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    # ---------------- DAG 上的动态规划 (DP) ----------------
    dp = [-1] * scc_count
    scc_s = scc_id[s]
    dp[scc_s] = scc_val[scc_s]

    for u in topo_order:
        if dp[u] == -1:
            continue
        for v, w in dag_edges[u].items():
            val = dp[u] + w + scc_val[v]
            if val > dp[v]:
                dp[v] = val

    # 最大的愉悦度是所有可达节点中 dp 值的最大值
    print(max(dp))


if __name__ == "__main__":
    solve()
