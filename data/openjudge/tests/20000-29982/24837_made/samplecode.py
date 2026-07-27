# External reference: statistics page /practice/24837/
# Accepted submission: 52715349
# Source: http://cs101.openjudge.cn/practice/solution/52715349/
# License: not declared on the submission page; no license is inferred.

from collections import deque
p,q,x,y = map(int,input().split())
qu = deque([p])
ans,found = 1,0
vis = {p}
while qu and ans <= 52:
    l = len(qu)
    for _ in range(l):
        qi = qu.popleft()
        if qi >= x and qi-x not in vis:
            vis.add(qi-x)
            qu.append(qi-x)
            if qi-x == q:
                found = 1
                break
        if qi*y not in vis and qi*y <= (52-ans)*x+q:
            qu.append(qi*y)
            vis.add(qi*y)
            if qi*y == q:
                found = 1
                break
    if found:
        break
    ans += 1
print(ans if found else "Failed")