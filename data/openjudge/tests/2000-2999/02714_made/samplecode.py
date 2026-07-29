# External reference: http://cs101.openjudge.cn/practice/02714/statistics/
# Accepted submission: 51866391
# Source: http://cs101.openjudge.cn/practice/solution/51866391/
# License: not declared on the submission page; no license is inferred.

n=int(input())
s=0
for _ in range(n):
    s+=int(input())
print(f'{s/n:.2f}')
