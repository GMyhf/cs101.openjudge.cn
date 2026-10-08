# 双指针贪心；并列时用反串切片比较（C 速度），O(N^2) 字节比较但常数极小。
import sys
a=sys.stdin.read().split();s=''.join(a[1:]);n=len(s);rv=s[::-1];l,r,out=0,n-1,[]
while l<=r:
    if s[l]<s[r]:out.append(s[l]);l+=1
    elif s[l]>s[r]:out.append(s[r]);r-=1
    elif s[l:r+1]<=rv[n-1-r:n-l]:out.append(s[l]);l+=1
    else:out.append(s[r]);r-=1
t=''.join(out);print('\n'.join(t[i:i+80] for i in range(0,len(t),80)))
