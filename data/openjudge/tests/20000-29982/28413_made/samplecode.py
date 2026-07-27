# External reference: statistics page /practice/28413/
# Accepted submission: 52720583
# Source: http://cs101.openjudge.cn/practice/solution/52720583/
# License: not declared on the submission page; no license is inferred.

for _ in range(int(input())):
    n = int(input())
    names = []
    edges = [[] for _ in range(n)]
    for i in range(n):
        s = input().split()
        names.append(s[0])
        for j in s[1:]:
            j = int(j)-1
            edges[i].append(j)
    for i in range(n):
        edges[i].sort()        
    ans = []
    part = []
    for i in range(n):
        cur = []
        cur.append(names[i])
        for ci in edges[i]:
            cur.extend(part[ci])
        part.append(cur)
        ans.extend(part[-1])
    print(len(ans))
    print(*ans)