# External reference: http://cs101.openjudge.cn/practice/30276/statistics/
# Accepted submission: 52723593
# Source: http://cs101.openjudge.cn/practice/solution/52723593/
# License: not declared on the submission page; no license is inferred.

def main():
    import sys
    k, n = map(int, sys.stdin.readline().split())

    # 初始化DP数组，无穷大表示未计算
    INF = float('inf')
    dp = [[INF] * (n + 1) for _ in range(k + 1)]

    # 边界条件1：所有柱子，0个盘子=0步，1个盘子=1步
    for i in range(3, k + 1):
        dp[i][0] = 0
        dp[i][1] = 1

    # 边界条件2：经典3柱汉诺塔，dp[3][j] = 2^j -1
    for j in range(2, n + 1):
        dp[3][j] = (1 << j) - 1  # 等价于2^j -1

    # 递推计算：柱子数从4到k，盘子数从2到n
    for i in range(4, k + 1):
        for j in range(2, n + 1):
            # 枚举m，找最优解
            for m in range(1, j):
                dp[i][j] = min(dp[i][j], 2 * dp[i][m] + dp[i-1][j - m])

    print(dp[k][n])

if __name__ == "__main__":
    main()
