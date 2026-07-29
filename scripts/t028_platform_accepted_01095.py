# External reference: http://cs101.openjudge.cn/practice/01095/statistics/
# Accepted submission: 52165931
# Source: http://cs101.openjudge.cn/practice/solution/52165931/
# License: not declared on the submission page; no license is inferred.

cata=[1]
s=500000000
i=0
while s>0:
    cata.append(cata[i]*(4*i+2)//(i+2))
    s-=cata[-1]
    i+=1
def build(m,k):
    if m==1:
        return "X"
    l=0
    while k > cata[l] * cata[m-1-l]:
        k -= cata[l] * cata[m-1-l]
        l += 1
    lk = (k - 1) // cata[m-1-l] + 1
    rk =k-(lk-1)*(cata[m-1-l])
    left = f"({build(l, lk)})" if l != 0 else ""
    right = f"({build(m-1-l, rk)})" if (m-1-l) != 0 else ""
    return left + "X" + right

while True:
    n=int(input())
    x=n
    if n==0:
        break
    else:
        i=1
        x=0
        while x+cata[i]<n:
            x+=cata[i]
            i+=1
        n-=x
        print(build(i,n))
