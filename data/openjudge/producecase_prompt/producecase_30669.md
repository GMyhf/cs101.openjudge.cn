请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py。



## T30669:地铁换乘

B 市有 n 个地点，编号为 1 ~ n，可视为根节点为编号 t 的树，交通管理局在根节点上。

记每个节点的深度为其到 t 的边数，如根节点 t 的深度为 0。

作为交通管理局局长的小 W 计划修一趟地铁，线路 A 从编号为 p 的地点出发，线路 B 从编号为 q 的地点出发，修线路 A 的施工队 1 速度为一天修 v1 条边，修线路 B 的施工队 2 速度为一天修 v2 条边，而小 W 想构建一个换乘站，所以他指挥施工队 1 从 p 出发往 q 修，施工队 2 从 q 出发往 p 修，数据保证某一天他们一定会在一个节点相遇，该节点即为换乘站。

小 W 想知道多少天后两个施工队会相遇，并且小 W 想知道换乘站的深度，以便于他能及时地从交通管理局赶到换乘站。



数据范围：1 ≤ n ≤ 2×10^5, 1 ≤ t,p,q ≤ n, 1 ≤ v1,v2 ≤ 10^9, 1 ≤ u,v ≤ n,u≠v

保证输入构成一棵树。保证 p 到q 的距离L 满足 L mod (v1+v2) = 0。

保证相遇点一定在某个节点上，且相遇天数为整数。

**输入**

第一行两个正整数 n,t，代表地点个数与根节点编号。

接下来 n-1 行，每行两个正整数 u,v，代表编号为 u,v 的两个地点相连。

接下来一行四个正整数 p,q,v1,v2，分别代表施工队 1、施工队 2 的出发节点与施工速度。

**输出**

一行用空格隔开的两个正整数，分别代表相遇天数与换乘站深度。

样例输入

```
7 1
1 2
1 3
2 4
2 5
3 6
3 7
4 7 1 3
```

样例输出

```
1 1
```

提示

LCA（最近公共祖先） 和 倍增法（Binary Lifting）



producecase_template.py

```python
import random
import time
import os

# 确保 data 目录存在
os.makedirs("data", exist_ok=True)

def solve(m, n, k):
    """等价类划分问题逻辑 (ac.py 同款)"""
    groups = {}
    for num in range(m + 1, n):
        s = sum(map(int, str(num)))
        if s % k == 0:
            groups.setdefault(s, []).append(num)

    result_lines = []
    for s in sorted(groups):
        result_lines.append(','.join(map(str, sorted(groups[s]))))
    return result_lines


for epoch in range(30):
    # 随机生成 m, n, k
    m = random.randint(1, 9000)
    n = random.randint(m + 2, min(m + 2000, 10000))  # 保证范围合理
    k = random.randint(1, 9)

    # 写入输入文件
    with open(f"data/{epoch}.in", "w") as f:
        f.write(f"{m},{n},{k}\n")

    start = time.time()

    # 调用逻辑
    result = solve(m, n, k)

    end = time.time() - start
    print(f"[{epoch}] {end:.3f}s | m={m}, n={n}, k={k}")

    # 写入输出文件
    with open(f"data/{epoch}.out", "w") as f:
        if result:
            f.write("\n".join(result) + "\n")
        else:
            f.write("\n")  # 没有满足条件的情况


```



ac.py

```python
import sys

# 增加递归深度
sys.setrecursionlimit(200000)

def solve():
    # 读取 n 和 根节点 t
    try:
        line1 = sys.stdin.readline().split()
        if not line1: return
        n, t = map(int, line1)
    except ValueError: return

    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, sys.stdin.readline().split())
        adj[u].append(v)
        adj[v].append(u)

    p, q, v1, v2 = map(int, sys.stdin.readline().split())

    # 倍增预处理
    LOG = 18  # 2^18 > 200,000
    depth = [0] * (n + 1)
    up = [[0] * LOG for _ in range(n + 1)]

    def dfs(u, fa, d):
        depth[u] = d
        up[u][0] = fa
        for v in adj[u]:
            if v != fa:
                dfs(v, u, d + 1)

    dfs(t, 0, 0)

    # 构建倍增表
    for i in range(1, LOG):
        for u in range(1, n + 1):
            if up[u][i-1] != 0:
                up[u][i] = up[up[u][i-1]][i-1]

    # 求 LCA 函数
    def get_lca(u, v):
        if depth[u] < depth[v]:
            u, v = v, u
        # 爬升到同一深度
        diff = depth[u] - depth[v]
        for i in range(LOG):
            if (diff >> i) & 1:
                u = up[u][i]
        if u == v:
            return u
        # 同时向上跳
        for i in range(LOG - 1, -1, -1):
            if up[u][i] != up[v][i]:
                u = up[u][i]
                v = up[v][i]
        return up[u][0]

    # 求第 k 个祖先
    def get_kth_ancestor(u, k):
        for i in range(LOG):
            if (k >> i) & 1:
                u = up[u][i]
        return u

    # 1. 计算 LCA 和 距离
    r = get_lca(p, q)
    dist_p_r = depth[p] - depth[r]
    dist_q_r = depth[q] - depth[r]
    L = dist_p_r + dist_q_r

    # 2. 计算天数
    days = L // (v1 + v2)

    # 3. 找到相遇节点
    dist_from_p = v1 * days
    if dist_from_p <= dist_p_r:
        # 相遇点在 p 到 LCA 的链上，是 p 的祖先
        meeting_node = get_kth_ancestor(p, dist_from_p)
    else:
        # 相遇点在 q 到 LCA 的链上，是 q 的祖先
        dist_from_q = v2 * days
        meeting_node = get_kth_ancestor(q, dist_from_q)

    print(f"{days} {depth[meeting_node]}")
    # 如果想知道编号，打印 meeting_node 即可

# 示例运行
if __name__ == "__main__":
    solve()

```

