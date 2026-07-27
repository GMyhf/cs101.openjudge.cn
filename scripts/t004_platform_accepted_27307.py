# External reference: statistics page /practice/27307/
# Accepted submission: 52740030
# Source: http://cs101.openjudge.cn/practice/solution/52740030/
# License: not declared on the submission page; no license is inferred.

n = int(input())

hp = list(map(int, input().split()))
time = list(map(int, input().split()))

INF = 10**18

dp = [INF] * (n + 1)
dp[0] = 0

for i in range(n):
    value = time[i] + 1
    cost = hp[i]

    ndp = dp[:]

    for j in range(n + 1):
        if dp[j] == INF:
            continue

        nj = min(n, j + value)
        ndp[nj] = min(ndp[nj], dp[j] + cost)

    dp = ndp

print(dp[n])