# External reference: http://cs101.openjudge.cn/practice/04042/statistics/
# Accepted submission: 50793790
# Source: http://cs101.openjudge.cn/practice/solution/50793790/
# License: not declared on the submission page; no license is inferred.

def fun(x):
    return ord(x)-96
N = int(input())
for _ in range(N):
    S, m, q = input().split()
    m, q = int(m), int(q)
    l, r = 0, m
    res = 0
    for i in range(l, r):
        res += fun(S[i])
    ans = []
    if res == q:
        ans.append(S[l:r])
    for i in range(len(S)-m):
        res += fun(S[r])-fun(S[l])
        l += 1
        r += 1
        if res == q:
            ans.append(S[l:r])
    print(len(ans))
    for a in ans:
        print(a)
