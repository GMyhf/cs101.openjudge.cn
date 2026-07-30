# External reference: http://cs101.openjudge.cn/practice/18167/statistics/
# Accepted submission: 51284168
# Source: http://cs101.openjudge.cn/practice/solution/51284168/
# License: not declared on the submission page; no license is inferred.

N = int(input())
for _ in range(N):
    inp = input().strip()
    l = len(inp)
    for i in range(1, l+1):
        if l % i != 0:
            continue
        if inp == inp[:i]*(l//i):
            print(i)
            break
