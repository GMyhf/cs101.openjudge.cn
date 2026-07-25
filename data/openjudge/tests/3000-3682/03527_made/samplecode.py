# LLM-written reference implementation
import sys
from collections import Counter
def ok(v):
 if len(v)<2 or (len(v)-2)%3: return "XIANGGONG"
 def f(c,p):
  if not sum(c.values()): return p
  x=min(k for k,v in c.items() if v)
  if p is None and c[x]>=2:
   c[x]-=2
   if f(c,x): return x
   c[x]+=2
  if c[x]>=3:
   c[x]-=3
   if f(c,p): return p
   c[x]+=3
  if c.get(x+1,0) and c.get(x+2,0):
   for y in (x,x+1,x+2): c[y]-=1
   if f(c,p): return p
   for y in (x,x+1,x+2): c[y]+=1
  return None
 return "HU" if f(Counter(v),None) is not None else "BUHU"
out=[]
for line in sys.stdin:
 v=list(map(int,line.split()))
 if v and v[0]==0: break
 out.append(ok(v))
print("\n".join(out))