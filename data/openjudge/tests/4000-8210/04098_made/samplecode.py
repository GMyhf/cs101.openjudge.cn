# External reference: http://cs101.openjudge.cn/practice/04098/statistics/
# Accepted submission: 50953107
# Source: http://cs101.openjudge.cn/practice/solution/50953107/
# License: not declared on the submission page; no license is inferred.

m = int(input())
for _ in range(m):
    N = int(input())
    fruits = []
    for _ in range(N):
        id, a, b = map(int, input().split())
        fruits.append([id, a, b, a+b])
    fruits.sort(key = lambda x: x[3])
    res = fruits[-2]
    print(*res)
