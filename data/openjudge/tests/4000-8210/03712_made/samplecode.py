# LLM-written reference implementation
import sys
m={"2":"abc","3":"def","4":"ghi","5":"jkl","6":"mno","7":"pqrs","8":"tuv","9":"wxyz"}
a=sys.stdin.read().split(); out=[]
for w,d in zip(a[1::2],a[2::2]): out.append("Y" if len(w)==len(d) and all(x.lower() in m[y] for x,y in zip(w,d)) else "N")
print("\n".join(out))