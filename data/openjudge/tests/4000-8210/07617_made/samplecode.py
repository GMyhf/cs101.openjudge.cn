# External reference: statistics page /practice/07617/
# Accepted submission: 51084713
# Source: http://cs101.openjudge.cn/practice/solution/51084713/
# License: not declared on the submission page; no license is inferred.

n = int(input())
l = [int(x) for x in input().split()]
k = int(input())
l.sort()
for i in range(-1, -k-1, -1):
    print(l[i])