# External reference: statistics page /practice/23805/
# Accepted submission: 43290402
# Source: http://cs101.openjudge.cn/practice/solution/43290402/
# License: not declared on the submission page; no license is inferred.

# External reference: statistics page /practice/23805/
# Accepted submission: 43290402
# Source: http://cs101.openjudge.cn/practice/solution/43290402/
# License: not declared on the submission page; no license is inferred.

# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 14:11 2023

@author: 谢宇翔
"""
mdays = [
    0
    , 31
    , 28 + 31
    , 31 + 28 + 31
    , 30 + 31 + 28 + 31
    , 31 + 30 + 31 + 28 + 31
    , 30 + 31 + 30 + 31 + 28 + 31
    , 31 + 30 + 31 + 30 + 31 + 28 + 31
    , 31 + 31 + 30 + 31 + 30 + 31 + 28 + 31
    , 30 + 31 + 31 + 30 + 31 + 30 + 31 + 28 + 31
    , 31 + 30 + 31 + 31 + 30 + 31 + 30 + 31 + 28 + 31
    , 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30 + 31 + 28 + 31
    , 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30 + 31 + 28 + 31
]


def convert(hour, minute, sec, day, mon, year):
    total = 0
    for year_ in range(2000, year):
        if year_ % 4 == 0 and not (year_ % 100 == 0 and year_ % 400):
            total += 366
        else:
            total += 365
    if year % 4 == 0 and not (year % 100 == 0 and year % 400):
        if mon > 2:
            total += 1
    total += day - 1
    total += mdays[mon-1]
    mday = total % 100
    total //= 100
    mmonth = total % 10
    myear = total // 10
    total = hour * 3600 + minute * 60 + sec
    total = int(total * 100000 / (24 * 3600))
    msec = total % 100
    total //= 100
    mmin = total % 100
    mhour = total // 100

    print('{}:{}:{} {}.{}.{}'.format(mhour, mmin, msec, mday + 1, mmonth + 1, myear))


n = int(input())
for _ in range(n):
    p, q = input().split()
    a, b, c = map(int, p.split(":"))
    d, e, f = map(int, q.split("."))
    convert(a, b, c, d, e, f)


