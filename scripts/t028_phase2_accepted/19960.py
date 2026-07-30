# External reference: http://cs101.openjudge.cn/practice/19960/statistics/
# Accepted submission: 51286823
# Source: http://cs101.openjudge.cn/practice/solution/51286823/
# License: not declared on the submission page; no license is inferred.

def rotate(a):
    return (a % 6) + 1
def update_rotation(dic):
    return {rotate(k): rotate(v) for k, v in dic.items()}
L, M, R = {}, {}, {}
reL, reM, reR = {}, {}, {}
trans, alpha = {}, {}
for i in range(6):
    come, go = map(int, input().split())
    L[come] = go
    reL[go] = come
for i in range(6):
    come, go = map(int, input().split())
    M[come] = go
    reM[go] = come
for i in range(6):
    come, go = map(int, input().split())
    R[come] = go
    reR[go] = come
for i in range(3):
    come, go = map(int, input().split())
    trans[come] = go
    trans[go] = come
for i in ['a', 'b', 'c', 'd', 'e', 'f']:
    alpha[i] = ord(i) - 96
    alpha[ord(i)- 96] = i
string = list(input())
ans = ''
count = 0
for i in string:
    ans += alpha[reL[reM[reR[trans[R[M[L[alpha[i]]]]]]]]]
    L = update_rotation(L)
    reL = update_rotation(reL)
    count += 1
    if count % 6 == 0:
        M = update_rotation(M)
        reM = update_rotation(reM)
    if count % 36 == 0:
        R = update_rotation(R)
        reR = update_rotation(reR)
print(ans)
