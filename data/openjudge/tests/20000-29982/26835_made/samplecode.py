# External reference: statistics page /practice/26835/
# Accepted submission: 52824863
# Source: http://cs101.openjudge.cn/practice/solution/52824863/
# License: not declared on the submission page; no license is inferred.

import sys


def solve():
    # 使用 sys.stdin.read 能够一次性读取所有输入，避免因多余空格或换行导致解析错误
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    m = int(input_data[1])

    edges = []
    idx = 2
    for _ in range(m):
        u = int(input_data[idx])
        v = int(input_data[idx + 1])
        w = float(input_data[idx + 2])
        idx += 3
        # 保证编号小的在前面，方便后续输出
        if u > v:
            u, v = v, u
        edges.append((w, u, v))

    # 按花费从小到大排序
    edges.sort(key=lambda x: x[0])

    # 并查集初始化
    parent = list(range(n))

    def find(i):
        if parent[i] == i:
            return i
        parent[i] = find(parent[i])  # 路径压缩
        return parent[i]

    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            parent[root_i] = root_j
            return True
        return False

    mst_edges = []
    total_cost = 0.0
    edges_count = 0

    # Kruskal 算法核心
    for w, u, v in edges:
        if union(u, v):
            total_cost += w
            mst_edges.append((u, v))
            edges_count += 1
            if edges_count == n - 1:
                break

    # 检查是否所有人都连通
    # 找寻所有节点的根节点，如果唯一，说明全部连通
    roots = set(find(i) for i in range(n))

    if len(roots) == 1:
        # 输出最小花销，保留两位小数
        print(f"{total_cost:.2f}")
        # 按照花费从小到大输出每一对人（因为 edges 已经按花费排过序，mst_edges 里的顺序自然也是从小到大）
        for u, v in mst_edges:
            print(f"{u} {v}")
    else:
        print("NOT CONNECTED")


if __name__ == "__main__":
    solve()