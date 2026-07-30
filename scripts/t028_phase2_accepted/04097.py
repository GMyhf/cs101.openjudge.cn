# External reference: http://cs101.openjudge.cn/practice/04097/statistics/
# Accepted submission: 50953078
# Source: http://cs101.openjudge.cn/practice/solution/50953078/
# License: not declared on the submission page; no license is inferred.

n = int(input())
d1 = {}
d2 = {}
for i in range(n):
    station_name = input()
    d1[station_name] = i
    d2[i] = station_name
m = int(input())
for _ in range(m):
    s, e = input().split()
    res = []
    s_idx, e_idx = d1[s], d1[e]
    if s_idx < e_idx:
        for i in range(s_idx, e_idx+1):
            res.append(d2[i])
    else:
        for i in range(s_idx, e_idx-1, -1):
            res.append(d2[i])
    print(*res)
