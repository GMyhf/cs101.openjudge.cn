# External reference: http://cs101.openjudge.cn/practice/04099/statistics/
# Accepted submission: 52687214
# Source: http://cs101.openjudge.cn/practice/solution/52687214/
# License: not declared on the submission page; no license is inferred.

from collections import deque

m=int(input())
for _ in range(m):
    n=int(input())
    q=deque()
    stack=[]
    check=True
    for i in range(n):
        op=input().split()
        if len(op)==2:
            q.append(op[1])
            stack.append(op[1])
        else:
            if stack:
                q.popleft()
                stack.pop()
            else:
                check=False
    if check:
        print(*q)
        print(*stack)
    else:
        print('error')
        print('error')
