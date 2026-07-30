# External reference: http://cs101.openjudge.cn/practice/04018/statistics/
# Accepted submission: 52517182
# Source: http://cs101.openjudge.cn/practice/solution/52517182/
# License: not declared on the submission page; no license is inferred.

import sys
from collections import deque

def dfs(key,whole):
    if not key:
        return True
    if not whole:
        return False
    h=whole.copy()
    while h:
        if key[0]==h[0]:
            a=key.popleft()
            h.popleft()
            status=dfs(key,h)
            if status:
                return True
            else:
                key.appendleft(a)
        else:
            h.popleft()
    return False
content=sys.stdin.read().split()
ptr=0
while ptr<len(content):
    s=deque(i for i in content[ptr])
    t=deque(i for i in content[ptr+1])
    ptr+=2
    status=dfs(s,t)
    if status:
        print("Yes")
    else:
        print("No")
