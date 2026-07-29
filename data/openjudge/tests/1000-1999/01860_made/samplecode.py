# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 1860: Currency Exchange
# Fenced code block index: None
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/2025sp_routine/01860/
# License: not declared in source collection; no license is inferred.
import sys
a=sys.stdin.buffer.read().split();it=iter(a);n=int(next(it));m=int(next(it));s=int(next(it))-1;v=float(next(it));e=[]
for _ in range(m):
 x=int(next(it))-1;y=int(next(it))-1;r1=float(next(it));c1=float(next(it));r2=float(next(it));c2=float(next(it));e += [(x,y,r1,c1),(y,x,r2,c2)]
d=[0.0]*n;d[s]=v
gain=False
for i in range(n):
 changed=False
 for x,y,r,c in e:
  z=(d[x]-c)*r
  if z>d[y]:d[y]=z;changed=True
 if i==n-1 and changed:gain=True
 if not changed:break
print('YES' if gain else 'NO')
