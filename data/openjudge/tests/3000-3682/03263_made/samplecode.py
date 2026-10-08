# 参考实现：记忆化递归 f(i,j)=max(a[i][j], f(i+1,j), f(i+1,j+1))，O(N^2)。
# （原版本未记忆化，O(2^N)，N=100 时无法在时限内完成。）
import sys
from functools import lru_cache
sys.setrecursionlimit(10000)
a=iter(sys.stdin.read().split()); out=[]
while True:
 n=int(next(a))
 if n==0: break
 nrows=[[int(next(a)) for _ in range(i+1)] for i in range(n)]
 row,col=int(next(a))-1,int(next(a))-1
 @lru_cache(maxsize=None)
 def f(i,j):
  if i==n-1:return nrows[i][j]
  return max(nrows[i][j],f(i+1,j),f(i+1,j+1))
 out.append(str(f(row,col)))
print("\n".join(out))
