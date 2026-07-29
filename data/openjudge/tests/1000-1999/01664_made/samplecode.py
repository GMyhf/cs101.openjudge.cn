# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1664: 放苹果
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01664/
# License: not declared in source collection; no license is inferred.
import sys
def apple_distribution(t, cases):
    # 最大苹果数和盘子数
    max_m = max(c[0] for c in cases)
    max_n = max(c[1] for c in cases)

    # 初始化DP数组
    dp = [[0] * (max_n + 1) for _ in range(max_m + 1)]

    # 基础情况
    for m in range(max_m + 1):
        dp[m][1] = 1  # 只有一个盘子
    for n in range(max_n + 1):
        dp[0][n] = 1  # 没有苹果

    # 填表
    for m in range(1, max_m + 1):
        for n in range(2, max_n + 1):
            if n > m:
                dp[m][n] = dp[m][m]  # 盘子多于苹果
            else:
                dp[m][n] = dp[m][n-1] + dp[m-n][n]

    # 处理每个测试用例
    results = []
    for m, n in cases:
        results.append(dp[m][n])

    return results

# 主函数
def main():
    t = int(input())  # 测试数据数目
    cases = []
    for _ in range(t):
        m, n = map(int, input().split())
        cases.append((m, n))
    results = apple_distribution(t, cases)
    for res in results:
        print(res)

# 样例测试
if __name__ == "__main__":
    main()
