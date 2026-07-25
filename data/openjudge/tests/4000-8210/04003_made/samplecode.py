# T-004-r2 reference implementation
import sys
a=sys.stdin.read().split(); t=int(a[0])
print("\n".join(str(int(x,16)) for x in a[1:t+1]))