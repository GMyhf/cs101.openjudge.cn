# T-004-r2 reference implementation
import sys
a=list(map(int,sys.stdin.read().split()))
odd=sorted((x for x in a if x%2),reverse=True)
even=sorted(x for x in a if not x%2)
print(" ".join(map(str,odd+even)))