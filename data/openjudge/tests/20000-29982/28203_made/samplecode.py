# External reference: http://cs101.openjudge.cn/practice/28203/statistics/
# Accepted submission: 52700864
# Source: http://cs101.openjudge.cn/practice/solution/52700864/
# License: not declared on the submission page; no license is inferred.

from array import array

n = int(input())
a = array('I', map(int, input().split()))
f = array('I', [0])*n
s = array('I')

for i in range(n):
    while s and a[s[-1]] < a[i]:
        f[s.pop()] = i + 1
    s.append(i)
print(' '.join(map(str, f)))
