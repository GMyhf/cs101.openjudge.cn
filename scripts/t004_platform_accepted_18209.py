# External reference: cs101.openjudge.cn practice/18209 statistics, Accepted solution 38077709.
# Source: http://cs101.openjudge.cn/practice/solution/38077709/
# Statistics: http://cs101.openjudge.cn/practice/18209/statistics/
# License: not declared on submission page; no license inferred
from math import log
n = int(input())
a, b = 0, 0
lst = list(map(float, input().split()))
lst.sort()
for i in range(n):
    a -= log(lst[i], 2) * lst[i]
    if i != 0 and i != n - 1:
        b -= log(lst[i], 2) * lst[i]
print('%.3f' % a)
print('%.3f' % b)
