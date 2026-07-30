# External reference: http://cs101.openjudge.cn/practice/12559/statistics/
# Accepted submission: 52536073
# Source: http://cs101.openjudge.cn/practice/solution/52536073/
# License: not declared on the submission page; no license is inferred.

from functools import cmp_to_key

def compare(a,b):
    if a+b<b+a:
        return -1
    elif a+b>b+a:
        return 1
    else:
        return 0

n=int(input())
num=input().split()
num.sort(key=cmp_to_key(compare))
a="".join(num)
b="".join(reversed(num))
print(b,a)
