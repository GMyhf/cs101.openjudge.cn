# External reference: statistics page /practice/20102/
# Accepted submission: 52482499
# Source: http://cs101.openjudge.cn/practice/solution/52482499/
# License: not declared on the submission page; no license is inferred.

# External reference: cs101.openjudge.cn practice/20102 statistics, Accepted solution 52482499.
# Source: http://cs101.openjudge.cn/practice/solution/52482499/
# Statistics: http://cs101.openjudge.cn/practice/20102/statistics/
# License: not declared on submission page; no license inferred
import math

t = int(input())
while t > 0:
    t-=1
    n = int(input())
    print(1+math.comb(n,2)+math.comb(n,4))
