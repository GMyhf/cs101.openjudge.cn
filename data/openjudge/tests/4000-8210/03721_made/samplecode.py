# T-004-r3 reference implementation
import sys
a=list(map(int,sys.stdin.read().split())); n=a[0]; v=a[1:1+n]; ans=0
for i,x in enumerate(v):
    seen=set()
    for j,y in enumerate(v):
        if j!=i and x-y in seen: ans+=1; break
        if j!=i: seen.add(y)
print(ans)