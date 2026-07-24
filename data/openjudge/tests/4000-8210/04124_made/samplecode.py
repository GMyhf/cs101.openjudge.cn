# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    cost = [[int(next(it)) for _ in range(N)] for _ in range(N)]

    INF = 10**12
    # dp[mask][i]: 已访问mask，最后在i的最小花费
    dp = [[INF] * N for _ in range(1 << N)]
    dp[1][0] = 0  # 起点(编号0)

    for mask in range(1 << N):
        for i in range(N):
            if dp[mask][i] == INF:
                continue
            for j in range(N):
                if mask >> j & 1:  # j 已经访问过
                    continue
                new_mask = mask | (1 << j)
                dp[new_mask][j] = min(dp[new_mask][j],
                                      dp[mask][i] + cost[i][j])

    print(dp[(1 << N) - 1][N - 1])

if __name__ == "__main__":
    solve()
