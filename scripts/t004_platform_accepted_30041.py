# External reference: /practice/30041/statistics/
# Accepted submission: 52212520
# Source: http://cs101.openjudge.cn/practice/solution/52212520/
# License: not declared on the submission page; no license is inferred.

n,m=[int(i) for i in input().split()]
prev_array=[int(i) for i in input().split()]
now_array=prev_array

dp=[[0 for i in range(m)] for j in range(n)]
for i in range(m):
    dp[0][i]=1
for i in range(1,n):
    ptr1=0
    current=0
    prev_array=now_array[:]
    now_array=[int(i) for i in input().split()]
    for ptr2 in range(m):
        while ptr1<=m-1 and now_array[ptr2]>=prev_array[ptr1]:
            current+=dp[i-1][ptr1]
            ptr1+=1
        dp[i][ptr2]=current
s=0
for i in dp[-1]:
    s+=i
print(s)