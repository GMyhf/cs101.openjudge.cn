# External reference: http://cs101.openjudge.cn/practice/19944/statistics/
# Accepted submission: 51455521
# Source: http://cs101.openjudge.cn/practice/solution/51455521/
# License: not declared on the submission page; no license is inferred.

import sys

e = {0:"Sunday",1:"Monday",2:"Tuesday",
    3:"Wednesday",4:"Thursday",5:"Friday",6:"Saturday"}
n = int(input())


def gauss(t):
    return int(t//1)

for line in sys.stdin.read().splitlines():
    c = int(line[:2])
    y = int(line[2:4])
    m = int(line[4:6])
    if m == 1 or m == 2:
        m += 12
        y -= 1
    if y == -1:
        y = 99
        c -= 1
    d = int(line[6:])
    w = (y + gauss(y/4) + gauss(c/4) - 2*c + gauss(26*(m+1)/10) + d - 1) % 7
    print(e[w])
