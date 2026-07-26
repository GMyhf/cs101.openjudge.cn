# External reference: statistics page /practice/07615/
# Accepted submission: 51084596
# Source: http://cs101.openjudge.cn/practice/solution/51084596/
# License: not declared on the submission page; no license is inferred.

n = int(input())
table = []
for _ in range(n):
    a, b = input().split()
    table.append((a, int(b)))
table.sort(key = lambda x: (-x[1], x[0]))
for i in table:
    print(*i)