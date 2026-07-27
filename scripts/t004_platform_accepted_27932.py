# External reference: statistics page /practice/27932/
# Accepted submission: 52723138
# Source: http://cs101.openjudge.cn/practice/solution/52723138/
# License: not declared on the submission page; no license is inferred.

n, k = map(int, input().split())
a = list(map(int, input().split()))
a.sort()
if k == 0:
    print(1 if a[0] != 1 else -1)
elif k == n:
    print(a[-1])
else:
    if a[k-1] == a[k]:
        print(-1)
    else:
        print(a[k-1])