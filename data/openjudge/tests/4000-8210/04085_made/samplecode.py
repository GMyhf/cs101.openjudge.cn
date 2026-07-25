# T-004-r2 reference implementation
import sys
a=list(map(int,sys.stdin.read().split())); n=a[0]
print(" ".join(map(str,sorted(set(a[1:n+1])))))