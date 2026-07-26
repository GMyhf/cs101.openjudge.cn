# External reference: statistics page /practice/19947/
# Accepted submission: 51286241
# Source: http://cs101.openjudge.cn/practice/solution/51286241/
# License: not declared on the submission page; no license is inferred.

# External reference: cs101.openjudge.cn practice/19947 statistics, Accepted solution 51286241.
# Source: http://cs101.openjudge.cn/practice/solution/51286241/
# Statistics: http://cs101.openjudge.cn/practice/19947/statistics/
# License: not declared on submission page; no license inferred
n = int(input())
l = [int(x) for x in input().split()]
l.sort()
a = sum(l)
b = l[-1]
if a % 2 == 1:
    print('NO')
else:
    if a >= 2*b:
        print('YES')
    else:
        print('NO')
