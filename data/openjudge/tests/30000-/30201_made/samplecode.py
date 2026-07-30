# External reference: http://cs101.openjudge.cn/practice/30201/statistics/
# Accepted submission: 52726532
# Source: http://cs101.openjudge.cn/practice/solution/52726532/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    # 使用快速读取
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    adj = []
    idx = 1
    for i in range(n):
        row = [int(x) for x in input_data[idx : idx + n]]
        adj.append(row)
        idx += n

    # 特判
    if n == 1:
        print(0)
        return

    # 为了优化，固定最后一个城市 (n-1) 作为起点和终点
    # mask 只表示前 m 个城市 (0 到 n-2) 的访问状态
    m = n - 1
    limit = 1 << m
    inf = float('inf')

    # dp[mask][i] 表示访问了 mask 中的城市，且当前在 i，从起点 n-1 出发的开销
    dp = [[inf] * m for _ in range(limit)]

    # 初始化：从起点 n-1 去往第一个城市 i
    for i in range(m):
        dp[1 << i][i] = adj[m][i]

    # 状态压缩 DP
    for mask in range(1, limit):
        # 提取当前 mask 中所有的城市（置为 1 的位）
        bits = []
        temp = mask
        while temp:
            b = (temp & -temp).bit_length() - 1
            bits.append(b)
            temp &= temp - 1

        # 如果只有一个城市，已经在初始化中处理过了
        if len(bits) < 2:
            continue

        for u in bits:
            prev_mask = mask ^ (1 << u)
            dp_prev = dp[prev_mask]
            adj_u = adj[u]

            # 找到一个中间城市 v，使得 cost 最小
            best = inf
            for v in bits:
                if v == u:
                    continue
                # 从起点经过 prev_mask 停在 v，再从 v 走到 u
                res = dp_prev[v] + adj_u[v]
                if res < best:
                    best = res
            dp[mask][u] = best

    # 最后回到起点 n-1
    full_mask = limit - 1
    final_ans = inf
    dp_full = dp[full_mask]
    adj_last = adj[m]
    for i in range(m):
        res = dp_full[i] + adj_last[i]
        if res < final_ans:
            final_ans = res

    print(final_ans)

if __name__ == "__main__":
    solve()
