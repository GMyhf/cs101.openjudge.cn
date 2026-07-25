# T-004-r3 reference implementation
import sys
n,m=map(int,sys.stdin.read().split()); answer=-1
for a in range(1,m):
    if n%a==0 and n%(m-a)==0: answer=a; break
print(answer)