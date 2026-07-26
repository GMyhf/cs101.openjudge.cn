# External reference: statistics page /practice/06364/
# Accepted submission: 52717482
# Source: http://cs101.openjudge.cn/practice/solution/52717482/
# License: not declared on the submission page; no license is inferred.

n, k = map(int, input().split())

round1 = []
for i in range(n):
    a, b = map(int, input().split())
    round1.append((a, b, i+1))

round1.sort(key = lambda x : -x[0])

round2 = round1[:k]

round2.sort(key = lambda x : -x[1])

print(round2[0][2])