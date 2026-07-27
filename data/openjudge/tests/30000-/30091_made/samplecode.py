# External reference: /practice/30091/statistics/
# Accepted submission: 52732776
# Source: http://cs101.openjudge.cn/practice/solution/52732776/
# License: not declared on the submission page; no license is inferred.

L = int(input())
N = int(input())
if N == 0:
    print(0, 0)
else:
    pos = list(map(int, input().split()))
    min_ans = 0
    max_ans = 0
    for x in pos:
        t1 = min(x, L + 1 - x)
        t2 = max(x, L + 1 - x)
        if t1 > min_ans:
            min_ans = t1
        if t2 > max_ans:
            max_ans = t2
    print(min_ans, max_ans)