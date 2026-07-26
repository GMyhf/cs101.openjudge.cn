# T-004-r2 reference implementation
import sys
a=list(map(int,sys.stdin.buffer.read().split())); n=a[0] if a else 0; out=[]
for i in range(min(n,(len(a)-1)//2)):
    x,y=a[1+2*i],a[2+2*i]
    bits=f"{x:016b}"
    out.append("YES" if any(bits[k:]+bits[:k]==f"{y:016b}" for k in range(16)) else "NO")
print("\n".join(out))