# External reference: http://cs101.openjudge.cn/practice/29917/statistics/
# Accepted submission: 52278977
# Source: http://cs101.openjudge.cn/practice/solution/52278977/
# License: not declared on the submission page; no license is inferred.

import sys
def iter(x_n,n):
    nxt=(x_n+(n/x_n))
    return nxt/2
nums=[float(i) for i in sys.stdin.readlines()]
for num in nums:
    now=1
    nxt=1
    cnt=0
    while True:
        cnt+=1
        nxt=iter(now,num)
        if abs(nxt-now)<=1E-6:
            break
        now=nxt
    print(cnt,format(nxt,".2f"))
