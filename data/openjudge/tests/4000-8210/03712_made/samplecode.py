# LLM-written reference implementation
import sys
m={"2":set("abc"),"3":set("def"),"4":set("ghi"),"5":set("jkl"),"6":set("mno"),"7":set("pqrs"),"8":set("tuv"),"9":set("wxyz")}
a=sys.stdin.read().split(); n=int(a[0]) if a else 0; out=[]
for i in range(n):
 w,d=a[1+2*i],a[2+2*i]
 out.append("Y" if len(w)==len(d) and all(x.lower() in m.get(y,set()) for x,y in zip(w,d)) else "N")
print("\n".join(out))