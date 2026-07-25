# T-004-r2 reference implementation
import sys
a=sys.stdin.read().split(); n=int(a[0]); versions=a[1:1+n]
def key(v): return tuple(map(int,v.split(".")))
print("\n".join(sorted(versions,key=key)))