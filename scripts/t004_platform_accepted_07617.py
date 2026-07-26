# External reference: cs101.openjudge.cn practice/07617 statistics, Accepted solution 51084713.
# Source: http://cs101.openjudge.cn/practice/solution/51084713/
# Statistics: http://cs101.openjudge.cn/practice/07617/statistics/
# License: not declared on submission page; no license inferred
n = int(input())
l = [int(x) for x in input().split()]
k = int(input())
l.sort()
for i in range(-1, -k-1, -1):
    print(l[i])