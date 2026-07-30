# External reference: http://cs101.openjudge.cn/practice/04013/statistics/
# Accepted submission: 51369214
# Source: http://cs101.openjudge.cn/practice/solution/51369214/
# License: not declared on the submission page; no license is inferred.

while True:
    n = int(input())
    if not n:
        break
    a = sorted([int(input()) for i in range(n)])
    print(a[(n - 1)//2] if n % 2 else (a[n//2] + a[n//2 - 1])//2)
