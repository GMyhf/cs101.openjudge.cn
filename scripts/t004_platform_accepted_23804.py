# External reference: statistics page /practice/23804/
# Accepted submission: 52740130
# Source: http://cs101.openjudge.cn/practice/solution/52740130/
# License: not declared on the submission page; no license is inferred.

n, m = map(int, input().split())
ans = input().split()
for _ in range(m):
    stu = input().split()
    cnt = 0
    for a, s in zip(ans, stu):
        if a == s:
            cnt += 1
    print(cnt)