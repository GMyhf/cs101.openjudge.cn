# T-004-r2 reference implementation
import sys
a=list(map(int,sys.stdin.read().split())); n,t=a[:2]; dp=[0]*(t+1); dp[0]=1
for x in a[2:2+n]:
    for s in range(t,x-1,-1): dp[s]+=dp[s-x]
print(dp[t])