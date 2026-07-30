# External reference: http://cs101.openjudge.cn/practice/26978/statistics/
# Accepted submission: 52325412
# Source: http://cs101.openjudge.cn/practice/solution/52325412/
# License: not declared on the submission page; no license is inferred.

from collections import deque
n,k=map(int,input().split())
nums=list(map(int,input().split()))
window=deque()
ans=[]
for i in range(n):
    while window:
        if window[-1][0]<=nums[i]:
            window.pop()
        else:
            break
    window.append((nums[i],i))
    j=0
    while True:
        if window[j][1]<i-k+1:
            window.popleft()
        else:
            break
    if i>=k-1:
        ans.append(window[0][0])
print(*ans)
