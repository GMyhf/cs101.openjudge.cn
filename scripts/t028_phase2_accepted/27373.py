# External reference: http://cs101.openjudge.cn/practice/27373/statistics/
# Accepted submission: 52527803
# Source: http://cs101.openjudge.cn/practice/solution/52527803/
# License: not declared on the submission page; no license is inferred.

from functools import cmp_to_key

m=int(input())
n=int(input())
arr=input().split()

def compare(x,y):
    if x+y>y+x:
        return -1
    elif x+y<y+x:
        return 1
    else:
        return 0
arr.sort(key=cmp_to_key(compare))

def newmax(a,b):
    if len(a)>len(b):
        return a
    elif len(a)<len(b):
        return b
    else:
        return a if a>b else b
#dp[i] 表示，长度不超过i的最大值
dp=[""]*(m+1)
for num in arr:
    ll=len(num)
    for j in range(m,ll-1,-1):
        dp[j]=newmax(dp[j],dp[j-ll]+num)
print(dp[-1])
