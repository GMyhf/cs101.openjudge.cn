# External reference: http://cs101.openjudge.cn/practice/04045/statistics/
# Accepted submission: 50794807
# Source: http://cs101.openjudge.cn/practice/solution/50794807/
# License: not declared on the submission page; no license is inferred.

def judge_3_5(x):
    if x % 3 == 0 or x % 5 == 0 or '3' in str(x) or '5' in str(x):
        return False
    return True
res = 0
n = int(input())
for i in range(1, n+1):
    if judge_3_5(i):
        res += i**2
print(res)
