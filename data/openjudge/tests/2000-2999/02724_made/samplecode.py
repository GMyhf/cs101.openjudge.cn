# External reference: http://cs101.openjudge.cn/practice/02724/statistics/
# Accepted submission: 52721409
# Source: http://cs101.openjudge.cn/practice/solution/52721409/
# License: not declared on the submission page; no license is inferred.

from collections import defaultdict
def solve():
    n = int(input())
    cnt = defaultdict(list)
    day = list()
    for i in range(n):
        idx, m, d = input().split()
        m, d = int(m), int(d)
        cnt[(m, d)].append(idx)
        if (m, d) in day:
            continue
        day.append((m, d))
    day.sort()
    for i in day:
        if len(cnt[i]) <= 1:
            continue
        print(*(i[0], i[1], *cnt[i]))
    return
solve()
