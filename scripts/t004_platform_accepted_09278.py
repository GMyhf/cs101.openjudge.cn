# External reference: cs101.openjudge.cn practice/09278 statistics, Accepted solution 51174670.
# Source: http://cs101.openjudge.cn/practice/solution/51174670/
# Statistics: http://cs101.openjudge.cn/practice/09278/statistics/
# License: not declared on submission page; no license inferred
n = int(input())
dp = [1]+[0]*n
for i in range(2, n+1):
    dp[i] = (i-1)*(dp[i-2]+dp[i-1])
print(dp[n])