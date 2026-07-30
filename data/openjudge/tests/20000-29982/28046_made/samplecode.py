# External reference: http://cs101.openjudge.cn/practice/28046/statistics/
# Accepted submission: 52829414
# Source: http://cs101.openjudge.cn/practice/solution/52829414/
# License: not declared on the submission page; no license is inferred.

from collections import deque,defaultdict
n=int(input())
w=set()
pat=defaultdict(list)
for _ in range(n):
    s=input().strip()
    w.add(s)
    for i in range(4):
        p=s[:i]+"*"+s[i+1:]
        pat[p].append(s)
s,t=input().split()
vis=dict()
q=deque([s])
vis[s]=[s]
f=0
while q:
    u=q.popleft()
    if u==t:
        print(' '.join(vis[u]))
        f=1
        break
    for i in range(4):
        p=u[:i]+"*"+u[i+1:]
        for v in pat[p]:
            if v not in vis:
                vis[v]=vis[u]+[v]
                q.append(v)
if not f:
    print("NO")
