# External reference: http://cs101.openjudge.cn/practice/02576/statistics/
# Accepted submission: 41410928
# Source: http://cs101.openjudge.cn/practice/solution/41410928/
# License: not declared on the submission page; no license is inferred.

import math


def tow(n, weights):
    sum_weights = sum(weights)
    half_n = math.ceil(n / 2)
    half_sum = math.ceil(sum_weights / 2)
    dp = [[False] * (half_sum + 10) for _ in range(half_n + 10)]
    dp[0][0] = True

    for i in range(n):
        for j in range(half_n, 0, -1):
            for k in range(half_sum, weights[i] - 1, -1):
                if dp[j - 1][k - weights[i]]:
                    dp[j][k] = True

    team1_sum = 0
    team2_sum = 0
    for i in range(half_sum,-1,-1):
        if dp[half_n][i]:
            team1_sum = i
            break

    if team1_sum == 0:
        for i in range(half_sum, -1,-1):
            if dp[half_n - 1][i]:
                team1_sum = i
                break

    team2_sum = sum_weights - team1_sum
    return min(team1_sum, team2_sum), max(team1_sum, team2_sum)


n = int(input())
weights = []
for i in range(n):
    weights.append(int(input()))

r = tow(n, weights)
print(r[0], r[1])
