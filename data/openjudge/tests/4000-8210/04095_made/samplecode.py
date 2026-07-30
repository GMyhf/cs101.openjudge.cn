# External reference: http://cs101.openjudge.cn/practice/04095/statistics/
# Accepted submission: 50952971
# Source: http://cs101.openjudge.cn/practice/solution/50952971/
# License: not declared on the submission page; no license is inferred.

def judge(x):
    if x.isupper():
        return 1
    return 0
n = int(input())
for _ in range(n):
    con = 0
    res = 0
    for char in input():
        if judge(char) == con:
            res += 1
        else:
            res += 2
            con = judge(char)
    print(res)
