# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
import sys
input = sys.stdin.read
data = input().split()

def main():
    ptr = 0
    n, t = int(data[ptr]), int(data[ptr+1])
    ptr += 2

    # 建图
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u = int(data[ptr])
        v = int(data[ptr+1])
        adj[u].append(v)
        adj[v].append(u)
        ptr += 2

    # 倍增预处理
    LOG = 18
    depth = [0] * (n + 1)
    up = [[0] * LOG for _ in range(n + 1)]

    # DFS 初始化
    stack = [(t, 0, 0)]
    while stack:
        u, fa, d = stack.pop()
        depth[u] = d
        up[u][0] = fa
        for v in adj[u]:
            if v != fa:
                stack.append((v, u, d + 1))

    # 构建倍增表
    for j in range(1, LOG):
        for i in range(1, n + 1):
            up[i][j] = up[up[i][j-1]][j-1]

    # LCA
    def lca(u, v):
        if depth[u] < depth[v]:
            u, v = v, u
        # 对齐深度
        for j in range(LOG-1, -1, -1):
            if depth[u] - (1 << j) >= depth[v]:
                u = up[u][j]
        if u == v:
            return u
        for j in range(LOG-1, -1, -1):
            if up[u][j] != up[v][j]:
                u = up[u][j]
                v = up[v][j]
        return up[u][0]

    # 第 k 个祖先
    def kth_ancestor(u, k):
        for j in range(LOG-1, -1, -1):
            if k >= (1 << j):
                u = up[u][j]
                k -= (1 << j)
        return u

    # 读取查询数量 m
    m = int(data[ptr])
    ptr += 1

    # 处理 m 组查询
    res = []
    for _ in range(m):
        p = int(data[ptr])
        q = int(data[ptr+1])
        v1 = int(data[ptr+2])
        v2 = int(data[ptr+3])
        ptr += 4

        r = lca(p, q)
        L = (depth[p] - depth[r]) + (depth[q] - depth[r])
        days = L // (v1 + v2)
        s = v1 * days

        # 找相遇点
        if s <= depth[p] - depth[r]:
            meet = kth_ancestor(p, s)
        else:
            s2 = L - s
            meet = kth_ancestor(q, s2)

        res.append(f"{days} {depth[meet]}")
    
    print('\n'.join(res))

if __name__ == "__main__":
    main()
