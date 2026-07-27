# External reference: statistics page /practice/23745/
# Accepted submission: 52740135
# Source: http://cs101.openjudge.cn/practice/solution/52740135/
# License: not declared on the submission page; no license is inferred.

# External reference: statistics page /practice/23745/
# Accepted submission: 52740135
# Source: http://cs101.openjudge.cn/practice/solution/52740135/
# License: not declared on the submission page; no license is inferred.

n = int(input())
orig = list(map(int, input().split()))
disc = list(map(int, input().split()))

sum_o = sum(orig)
sum_d = sum(disc)

# 方案1总价：满足满55-20才减20，否则原价
if sum_o >= 55:
    cost1 = sum_o - 20
else:
    cost1 = sum_o
cost2 = sum_d

# 判断输出
if cost1 < cost2:
    print(1)
elif cost2 < cost1:
    print(2)
else:
    print(3)