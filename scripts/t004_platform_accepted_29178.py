# External reference: statistics page /practice/29178/
# Accepted submission: 52734219
# Source: http://cs101.openjudge.cn/practice/solution/52734219/
# License: not declared on the submission page; no license is inferred.

n = int(input())
a = list(map(int, input().split()))
cnt = 0

for i in range(n):
    if i == 0:
        # 第一个
        if a[i] > a[i+1]:
            cnt += 1
    elif i == n-1:
        # 最后一个
        if a[i] > a[i-1]:
            cnt += 1
    else:
        # 中间
        if a[i] > a[i-1] and a[i] > a[i+1]:
            cnt += 1

print(cnt)