# External reference: statistics page /practice/09278/
# Accepted submission: 51174670
# Source: http://cs101.openjudge.cn/practice/solution/51174670/
# License: not declared on the submission page; no license is inferred.

n = int(input())
dp = [1]+[0]*n
for i in range(2, n+1):
    dp[i] = (i-1)*(dp[i-2]+dp[i-1])
print(dp[n])