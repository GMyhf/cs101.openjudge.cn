# External reference: http://cs101.openjudge.cn/practice/01080/statistics/
# Accepted submission: 51690585
# Source: http://cs101.openjudge.cn/practice/solution/51690585/
# License: not declared on the submission page; no license is inferred.

t = int(input())
scores = {('A', 'A'):5, ('C', 'C'):5, ('G', 'G'):5, ('T', 'T'):5, ('A', 'C'):-1, ('C', 'A'):-1, ('A', 'G'):-2, ('G', 'A'):-2, ('A', 'T'):-1, ('T', 'A'):-1, ('C', 'G'):-3, ('G', 'C'):-3, ('C', 'T'):-2, ('T', 'C'):-2, ('G', 'T'):-2, ('T', 'G'): -2, 'A':-3, 'C':-4, 'G':-2, 'T':-1 }
for _ in range(t):
    l1, g1 = input().split()
    l2, g2 = input().split()
    l1, l2 = int(l1), int(l2)
    dp = [[-float('inf')]*(l2+1) for _ in range(l1+1)]
    dp[0][0] = 0
    for i in range(1, l1+1):
        dp[i][0] = dp[i-1][0]+scores[g1[i-1]]
    for j in range(1, l2+1):
        dp[0][j] = dp[0][j-1]+scores[g2[j-1]]
    for i in range(1, l1+1):
        for j in range(1, l2+1):
            dp[i][j] = max(dp[i-1][j]+scores[g1[i-1]], dp[i][j-1]+scores[g2[j-1]], dp[i-1][j-1]+scores[(g1[i-1], g2[j-1])])
    print(dp[l1][l2])
