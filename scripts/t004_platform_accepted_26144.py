# External reference: statistics page /practice/26144/
# Accepted submission: 51527404
# Source: http://cs101.openjudge.cn/practice/solution/51527404/
# License: not declared on the submission page; no license is inferred.

n = int(input())
temp = []
for i in range(1, n+1):
    for j in range(1, i+1):
        temp.append(f'{j}x{i}={i*j}')
    print(*temp)
    temp = []