# External reference: http://cs101.openjudge.cn/practice/04044/statistics/
# Accepted submission: 50794714
# Source: http://cs101.openjudge.cn/practice/solution/50794714/
# License: not declared on the submission page; no license is inferred.

N = int(input())
l = []
for _ in range(N):
    w, c = input().split()
    l.append((int(w), c))
l.sort(key=lambda x: x[0])
for x in l:
    print(x[1])
