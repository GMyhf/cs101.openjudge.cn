# External reference: statistics page /practice/19948/
# Accepted submission: 52600565
# Source: http://cs101.openjudge.cn/practice/solution/52600565/
# License: not declared on the submission page; no license is inferred.

# External reference: cs101.openjudge.cn practice/19948 statistics, Accepted solution 52600565.
# Source: http://cs101.openjudge.cn/practice/solution/52600565/
# Statistics: http://cs101.openjudge.cn/practice/19948/statistics/
# License: not declared on submission page; no license inferred
n, m = map(int, input().split())
a = list(map(int, input().split()))
a.sort()

if m >= n:
    print(0)
else:
    diff = [a[i] - a[i-1] for i in range(1, n)]
    diff.sort()
    total = a[-1] - a[0]
    for i in range(m-1):
        total -= diff[-1 - i]
    print(total)
