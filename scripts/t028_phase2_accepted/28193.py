# External reference: http://cs101.openjudge.cn/practice/28193/statistics/
# Accepted submission: 52734622
# Source: http://cs101.openjudge.cn/practice/solution/52734622/
# License: not declared on the submission page; no license is inferred.

import sys
sys.setrecursionlimit(1000000)

def main():
    input = sys.stdin.read
    data = input().split()
    idx = 0
    n = int(data[idx])
    idx += 1
    m = int(data[idx])
    idx += 1

    c = list(map(int, data[idx:idx+n]))
    idx += n

    # 并查集初始化
    parent = list(range(n + 1))  # 1~n编号

    def find(u):
        while parent[u] != u:
            parent[u] = parent[parent[u]]
            u = parent[u]
        return u

    def union(u, v):
        u_root = find(u)
        v_root = find(v)
        if u_root != v_root:
            parent[v_root] = u_root

    # 合并朋友
    for _ in range(m):
        x = int(data[idx])
        idx += 1
        y = int(data[idx])
        idx += 1
        union(x, y)

    # 统计每个连通块的最小花费
    min_cost = {}
    for i in range(1, n+1):
        root = find(i)
        cost = c[i-1]
        if root not in min_cost or cost < min_cost[root]:
            min_cost[root] = cost

    # 总和就是答案
    print(sum(min_cost.values()))

if __name__ == "__main__":
    main()
