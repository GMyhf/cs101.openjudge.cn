# External reference: http://cs101.openjudge.cn/practice/04096/statistics/
# Accepted submission: 50953019
# Source: http://cs101.openjudge.cn/practice/solution/50953019/
# License: not declared on the submission page; no license is inferred.

def fun(x):
    if x == 'A':
        return '1'
    if x == 'B':
        return '2'
    if x == 'C':
        return '$'
    if x == 'D':
        return '\n'
for char in input():
    print(fun(char), end = '')
