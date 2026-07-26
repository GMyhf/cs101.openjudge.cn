# External reference: cs101.openjudge.cn practice/08780 statistics, Accepted solution 52735269.
# Source: http://cs101.openjudge.cn/practice/solution/52735269/
# Statistics: http://cs101.openjudge.cn/practice/08780/statistics/
# License: not declared on submission page; no license inferred
n = int(input())
a = [*map(int, input().split())]
dp = [1] * n
maxn = -1
for i in range(n):
    for j in range(i):
        if a[j] >= a[i]:
            dp[i] = max(dp[i], dp[j] + 1)
    maxn = max(maxn, dp[i])
print(maxn)