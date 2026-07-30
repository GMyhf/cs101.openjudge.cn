# External reference: http://cs101.openjudge.cn/practice/29740/statistics/
# Accepted submission: 52721707
# Source: http://cs101.openjudge.cn/practice/solution/52721707/
# License: not declared on the submission page; no license is inferred.

import sys
from collections import deque

def solve():
    # 快速读入
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    n = int(next(iterator))
    p = int(next(iterator))

    C = [0] * (n + 1)
    U = [0] * (n + 1)

    for i in range(1, n + 1):
        C[i] = int(next(iterator))
        U[i] = int(next(iterator))

    # 1. 合并重复的有向边
    edges = {}
    for _ in range(p):
        u = int(next(iterator))
        v = int(next(iterator))
        w = int(next(iterator))
        edges[(u, v)] = edges.get((u, v), 0) + w

    # 2. 构建图并统计入度、出度
    g = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    out_degree = [0] * (n + 1)

    for (u, v), w in edges.items():
        g[u].append((v, w))
        in_degree[v] += 1
        out_degree[u] += 1

    # 3. 关键修正：非输入层节点初始值全部减去 U[i]（即初始化为 -U[i]）
    # 输入层节点（初始入度为 0）保持原输入值，不减 U[i]
    for i in range(1, n + 1):
        if in_degree[i] > 0:
            C[i] = -U[i]

    # 4. Kahn 拓扑排序与递推
    q = deque([i for i in range(1, n + 1) if in_degree[i] == 0])
    visited_count = 0

    while q:
        u = q.popleft()
        visited_count += 1

        # 只有当前节点状态 C[u] > 0 时，才向下游传递信号
        if C[u] > 0:
            for v, w in g[u]:
                C[v] += C[u] * w

        # 无论当前节点是否兴奋，都必须继续拓扑遍历，减少下游节点的入度
        for v, _ in g[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                q.append(v)

    # 5. 环检测
    if visited_count < n:
        print("NULL")
        return

    # 6. 筛选输出层节点（出度为 0）且最后状态大于 0 的节点
    output_nodes = []
    for i in range(1, n + 1):
        if out_degree[i] == 0 and C[i] > 0:
            output_nodes.append((i, C[i]))

    # 输出结果
    if not output_nodes:
        print("NULL")
    else:
        output_nodes.sort()
        for node_id, state in output_nodes:
            print(f"{node_id} {state}")

if __name__ == '__main__':
    solve()
