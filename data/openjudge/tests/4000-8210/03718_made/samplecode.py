# T-004-r2 reference implementation
import sys
a=list(map(int,sys.stdin.read().split())); out=[]
for x,y in zip(a[1::2],a[2::2]):
    out.append("YES" if any(((x<<k)|(x>>(16-k)))&65535==y for k in range(16)) else "NO")
print("\n".join(out))