# External reference: cs101.openjudge.cn practice/18189 statistics, Accepted solution 51284569.
# Source: http://cs101.openjudge.cn/practice/solution/51284569/
# Statistics: http://cs101.openjudge.cn/practice/18189/statistics/
# License: not declared on submission page; no license inferred
n, p = map(int, input().split())
n = n/60
res = 0
if n <= 0.5:
    res += 720*n
else:
    res += 360
    n -= 0.5
    if n <= 1:
        res += 600*n
    else:
        n -= 1
        res += 600
        if n <= 1.5:
            res += 360*n
        else:
            n -= 1.5
            res += 540
            res += 240*min(3, n)
print(int(res*p))
