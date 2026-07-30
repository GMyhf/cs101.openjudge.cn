# External reference: http://cs101.openjudge.cn/practice/21554/statistics/
# Accepted submission: 52224332
# Source: http://cs101.openjudge.cn/practice/solution/52224332/
# License: not declared on the submission page; no license is inferred.

n=int(input())
t=list(map(int,input().split()))
T=[]
for i in range(n):
    T.append((t[i],i+1))
T.sort()
ans1=[]
ans2=0
for i in range(n):
    a,x=T[i]
    ans1.append(x)
    ans2+=a*(n-i-1)
print(*ans1)
print(f'{ans2/n:.2f}')
