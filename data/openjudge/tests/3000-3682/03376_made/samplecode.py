# LLM-written reference implementation
import sys
a=sys.stdin.read().split(); s="".join(a[1:])
l,rr,out=0,len(s)-1,[]
while l<=rr:
 if s[l]<s[rr]: out.append(s[l]); l+=1
 elif s[l]>s[rr]: out.append(s[rr]); rr-=1
 else:
  i,j=l,rr
  while i<=j and s[i]==s[j]: i+=1; j-=1
  if i>j or s[i]<=s[j]: out.append(s[l]); l+=1
  else: out.append(s[rr]); rr-=1
print("".join(out))