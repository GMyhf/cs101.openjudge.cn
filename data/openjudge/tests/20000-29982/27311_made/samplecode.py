# External reference: statistics page /practice/27311/
# Accepted submission: 52740023
# Source: http://cs101.openjudge.cn/practice/solution/52740023/
# License: not declared on the submission page; no license is inferred.

N = int(input())

p = list(map(int, input().split()))
t = list(map(int, input().split()))

ans = 0
prev_pos = 0
prev_neg = 0

for i in range(N):
    d = p[i] - t[i]

    pos = max(d, 0)
    neg = max(-d, 0)

    ans += max(0, pos - prev_pos)
    ans += max(0, neg - prev_neg)

    prev_pos = pos
    prev_neg = neg

print(ans)