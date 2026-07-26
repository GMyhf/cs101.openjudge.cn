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