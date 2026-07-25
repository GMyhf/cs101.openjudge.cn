# T-004-r3 reference implementation
import sys
m,n=map(int,sys.stdin.read().split()); dp=[1]*n
for _ in range(m-1):
    for j in range(1,n): dp[j]+=dp[j-1]
print(dp[n-1])