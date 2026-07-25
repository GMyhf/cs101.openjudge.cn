# LLM-written reference implementation
import sys
def pos(r,c):
 t,l,b,rr=0,0,r-1,c-1
 while t<=b and l<=rr:
  for j in range(l,rr+1): yield t,j
  t+=1
  for i in range(t,b+1): yield i,rr
  rr-=1
  if t<=b:
   for j in range(rr,l-1,-1): yield b,j
   b-=1
  if l<=rr:
   for i in range(b,t-1,-1): yield i,l
   l+=1
r,c,msg=sys.stdin.read().rstrip("\n").split(" ",2); r,c=int(r),int(c)
bits="".join(format(0 if x==" " else ord(x)-64,"05b") for x in msg).ljust(r*c,"0")
g=[["0"]*c for _ in range(r)]
for (i,j),x in zip(pos(r,c),bits): g[i][j]=x
print("".join("".join(x) for x in g))