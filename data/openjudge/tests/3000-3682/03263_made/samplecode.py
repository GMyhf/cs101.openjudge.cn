# LLM-written reference implementation
import sys
a=iter(sys.stdin.read().split()); out=[]
while True:
 n=int(next(a))
 if n==0: break
 nrows=[[int(next(a)) for _ in range(i+1)] for i in range(n)]
 row,col=int(next(a))-1,int(next(a))-1
 def f(i,j):
  if i==n-1:return nrows[i][j]
  return max(nrows[i][j],f(i+1,j),f(i+1,j+1))
 out.append(str(f(row,col)))
print("\n".join(out))