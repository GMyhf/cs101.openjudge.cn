# External reference: http://cs101.openjudge.cn/practice/01458/statistics/
# Accepted submission: 51703529
# Source: http://cs101.openjudge.cn/practice/solution/51703529/
# License: not declared on the submission page; no license is inferred.

while True:
    try:
        sa, sb = input().split()
        m, n = len(sa), len(sb)
        dp = [[0]*(n+1) for _ in range(m+1)]
        for i in range(1, m+1):
            for j in range(1, n+1):
                if sa[i-1] == sb[j-1]:
                    dp[i][j] = dp[i-1][j-1]+1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        print(dp[m][n])
    except EOFError:
        break
