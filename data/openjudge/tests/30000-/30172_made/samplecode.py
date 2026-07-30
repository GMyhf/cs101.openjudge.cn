# External reference: http://cs101.openjudge.cn/practice/30172/statistics/
# Accepted submission: 51832210
# Source: http://cs101.openjudge.cn/practice/solution/51832210/
# License: not declared on the submission page; no license is inferred.

import sys
from collections import deque

# 增加递归深度以防万一（虽然这里是迭代逻辑）
sys.setrecursionlimit(20000)


def solve():
    # 使用 generator 节省内存并防止一次性读取过大导致的内存错误
    def get_input():
        for line in sys.stdin:
            for word in line.split():
                yield word

    tokens = get_input()

    try:
        line1 = next(tokens)
    except StopIteration:
        return

    n = int(line1)
    st = next(tokens)
    en = next(tokens)

    mp = {}
    orig = []  # 改用列表动态存储
    cnt = 0

    def get_id(s):
        nonlocal cnt
        if s not in mp:
            mp[s] = cnt
            orig.append(s)
            cnt += 1
        return mp[s]

    # 初始化起点和终点
    st_id = get_id(st)
    en_id = get_id(en)

    # 动态初始化
    # 注意：节点数可能比 n 大，因为 n 是父节点数量
    adj = []
    ind = []

    def ensure_capacity(target_id):
        while len(adj) <= target_id:
            adj.append([])
            ind.append(0)

    ensure_capacity(max(st_id, en_id))

    for _ in range(1, n):
        node = next(tokens)
        k = int(next(tokens))

        u = get_id(node)
        ensure_capacity(u)
        ind[u] = k  # 更新入度

        for _ in range(k):
            to_node = next(tokens)
            w = int(next(tokens))
            v = get_id(to_node)
            ensure_capacity(v)
            adj[v].append((u, w))  # 建立反向边

    INF = float('inf')
    dp = [-INF] * cnt
    pre = [-1] * cnt

    q = deque()
    q.append(en_id)
    dp[en_id] = 0

    tot = 0
    while q:
        u = q.popleft()
        tot += 1

        # 遍历所有以 u 为终点的边 (v -> u 在原图中，这里是 u -> v)
        if u < len(adj):
            for v, w in adj[u]:
                ind[v] -= 1
                if ind[v] == 0:
                    q.append(v)

                # 最长路更新
                if dp[u] + w > dp[v]:
                    dp[v] = dp[u] + w
                    pre[v] = u
                elif dp[u] + w == dp[v]:
                    # 严格遵循 C++ 逻辑：orig[u] > orig[pre[v]] ? pre[v] : u
                    if pre[v] == -1 or orig[u] < orig[pre[v]]:
                        pre[v] = u

    # 判定条件：tot 指的是进入过队列的节点数
    # 原代码用的是 tot < n，这里 tot 对应原代码的 tot
    if tot < n or dp[st_id] == -INF:
        print("WRONG INPUT")
    else:
        print(dp[st_id])
        res = []
        curr = st_id
        path_valid = True
        while curr != en_id:
            if curr == -1:
                path_valid = False
                break
            res.append(orig[curr])
            curr = pre[curr]

        if not path_valid:
            print("WRONG INPUT")  # 补丁逻辑
        else:
            res.append(orig[en_id])
            print(" ".join(res))


if __name__ == "__main__":
    solve()
