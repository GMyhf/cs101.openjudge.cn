# LLM-written reference implementation
import sys
a=list(map(int,sys.stdin.read().split())); cap,n=a[:2]; dp=[0]*(cap+1)
for p,v in zip(a[2::2],a[3::2]):
 for x in range(cap,p-1,-1): dp[x]=max(dp[x],dp[x-p]+v)
print(dp[cap])