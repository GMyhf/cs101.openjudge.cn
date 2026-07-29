# External reference: http://cs101.openjudge.cn/practice/02393/statistics/
# Accepted submission: 51766083
# Source: http://cs101.openjudge.cn/practice/solution/51766083/
# License: not declared on the submission page; no license is inferred.

N, S = map(int, input().split())
C0, Y0 = map(int, input().split())
res = C0*Y0
for _ in range(N-1):
    C, Y = map(int, input().split())
    C0 = min(C, C0+S)
    res += C0*Y
print(res)
