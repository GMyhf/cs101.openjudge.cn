# External reference: statistics page /practice/25684/
# Accepted submission: 51527327
# Source: http://cs101.openjudge.cn/practice/solution/51527327/
# License: not declared on the submission page; no license is inferred.

m, c = map(int, input().split())
chairs = [0]*(10**6+1)
for _ in range(m):
    n, s, d = map(int, input().split())
    for i in range(s,s+d):
        chairs[i] += n
if max(chairs) <= c:
    print('Y')
else:
    print('N')