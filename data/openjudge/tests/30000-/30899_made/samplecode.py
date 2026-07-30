# External reference: http://cs101.openjudge.cn/practice/30899/statistics/
# Accepted submission: 52727498
# Source: http://cs101.openjudge.cn/practice/solution/52727498/
# License: not declared on the submission page; no license is inferred.

import sys
from collections import deque

def solve():
    # 读取所有输入
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    m = int(input_data[1])

    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    edges = []

    idx = 2
    for _ in range(m):
        u = int(input_data[idx])
        v = int(input_data[idx+1])
        w = int(input_data[idx+2])
        idx += 3
        adj[u].append((v, w))
        in_degree[v] += 1
        edges.append((u, v, w))

    # 1. 拓扑排序计算最早开始时间 (EST)
    est = [0] * (n + 1)
    queue = deque()
    topo_order = []

    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)

    while queue:
        u = queue.popleft()
        topo_order.append(u)
        for v, w in adj[u]:
            if est[u] + w > est[v]:
                est[v] = est[u] + w
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    # 总工期
    max_time = max(est) if est else 0
    print(max_time)

    # 2. 逆拓扑排序计算最晚开始时间 (LST)
    lst = [max_time] * (n + 1)
    # 按照拓扑序的反序遍历
    for u in reversed(topo_order):
        for v, w in adj[u]:
            if lst[v] - w < lst[u]:
                lst[u] = lst[v] - w

    # 3. 寻找关键任务 (开始时间必须确定的任务)
    critical_tasks = []
    for u, v, w in edges:
        # 任务 (u, v) 的最早开始是 est[u]
        # 任务 (u, v) 的最晚结束是 lst[v]
        # 如果 est[u] + w == lst[v]，则为关键路径上的边
        if est[u] + w == lst[v]:
            critical_tasks.append((u, v))

    # 按字典序排序输出
    critical_tasks.sort()

    # 去重处理（如果存在多条同起点终点的关键边，题目要求输出二元组）
    unique_tasks = []
    if critical_tasks:
        unique_tasks.append(critical_tasks[0])
        for i in range(1, len(critical_tasks)):
            if critical_tasks[i] != critical_tasks[i-1]:
                unique_tasks.append(critical_tasks[i])

    for u, v in unique_tasks:
        print(f"{u} {v}")

if __name__ == "__main__":
    solve()
