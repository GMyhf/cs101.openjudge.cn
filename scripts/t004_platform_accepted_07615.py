# External reference: cs101.openjudge.cn practice/07615 statistics, Accepted solution 51084596.
# Source: http://cs101.openjudge.cn/practice/solution/51084596/
# Statistics: http://cs101.openjudge.cn/practice/07615/statistics/
# License: not declared on submission page; no license inferred
n = int(input())
table = []
for _ in range(n):
    a, b = input().split()
    table.append((a, int(b)))
table.sort(key = lambda x: (-x[1], x[0]))
for i in table:
    print(*i)