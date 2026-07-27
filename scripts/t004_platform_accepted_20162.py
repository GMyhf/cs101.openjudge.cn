# External reference: cs101.openjudge.cn practice/20162 statistics, Accepted solution 51463351.
# Source: http://cs101.openjudge.cn/practice/solution/51463351/
# Statistics: http://cs101.openjudge.cn/practice/20162/statistics/
# License: not declared on submission page; no license inferred
t = int(input())
for _ in range(t):
    a, b, c, r = map(int, input().split())
    a, b = min(a, b), max(a, b)
    if b <= c-r or a >= c+r:
        print(b-a)
    else:
        print(b-a-min(b, c+r)+max(a, c-r))
