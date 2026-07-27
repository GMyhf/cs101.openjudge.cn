# External reference: statistics page /practice/27278/
# Accepted submission: 52692639
# Source: http://cs101.openjudge.cn/practice/solution/52692639/
# License: not declared on the submission page; no license is inferred.

n, m = map(int,input().split())
d = [0] + list(map(int,input().split()))
a = [0] + list(map(int,input().split()))
def can(x):
    last = [0] * (m + 1) #last[i]表示科目i在[1,x]中的最后出现位置 ，m科目数，x表示1~x天
    for i in range(1, x + 1):
        if d[i] != 0:
            last[d[i]] = i
    for i in range(1, m + 1): #有科目没出现
        if last[i] == 0:
            return False
    free = 0  #可用的复习天数
    done = [False] * (m + 1)
    for i in range(1, x + 1):
        subj = d[i]
        if subj != 0 and last[subj] == i:  #这一天是某科目的最后可考日
            need = a[subj]
            if free < need:
                return False
            free -= need
            done[subj] = True
        else:
            free += 1
    return all(done[1:])
lo, hi = 1, n
ans = -1
while lo <= hi:
    mid = (lo + hi) // 2
    if can(mid):
        ans = mid
        hi = mid - 1
    else:
        lo = mid + 1
print(ans)