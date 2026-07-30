# External reference: http://cs101.openjudge.cn/practice/18104/statistics/
# Accepted submission: 52523211
# Source: http://cs101.openjudge.cn/practice/solution/52523211/
# License: not declared on the submission page; no license is inferred.

s = sorted(list(map(int,input().split())))+[float("inf")]
p = sorted(list(map(int,input().split())))
j = 0
for pi in p:
    if pi >= s[j]:
        j += 1
print(j)
