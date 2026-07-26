# LLM-written reference implementation
import sys
a=list(map(int,sys.stdin.read().split())); i=0; out=[]
while i+1<len(a):
 cap,n=a[i],a[i+1]; i+=2; dp=[0]*(cap+1)
 for _ in range(n):
  p,v=a[i],a[i+1]; i+=2
  for x in range(cap,p-1,-1): dp[x]=max(dp[x],dp[x-p]+v)
 out.append(str(dp[cap]))
print("\n".join(out))