# External reference: http://cs101.openjudge.cn/practice/04074/statistics/
# Accepted submission: 50858090
# Source: http://cs101.openjudge.cn/practice/solution/50858090/
# License: not declared on the submission page; no license is inferred.

m = int(input())
for _ in range(m):
    n = int(input())
    H = [int(x) for x in input().split()]
    max_h = max(H)
    h = 1
    res = 0
    li = [x for x in range(n) if H[x] >= h]
    while h <= max_h or len(li) > 1:
        h += 1
        res += li[-1]-li[0]-len(li)+1
        li = [x for x in li if H[x] >= h]
    print(res)
