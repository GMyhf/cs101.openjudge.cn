# LLM-written reference implementation
import sys
def f(s):
 n=int(s,2); out=[]
 if not n:return "0"
 while n: out.append(str(n%3)); n//=3
 return "".join(out[::-1])
a=sys.stdin.read().split(); print("\n".join(f(x) for x in a[1:]))