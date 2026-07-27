# External reference: statistics page /practice/27832/
# Accepted submission: 48145494
# Source: http://cs101.openjudge.cn/practice/solution/48145494/
# License: not declared on the submission page; no license is inferred.

n,m=map(int,input().split())
a=list(map(int,input().split()))
add=0
sum1=[[0]*(1<<(_+1)) for _ in range(16)]
sum2=[[0]*(1<<(_+1)) for _ in range(16)]
for i in range(n):
    for j in range(16):
        sum1[j][a[i]%(1<<(j+1))]+=1
for j in range(16):
    for i in range(1<<j,1<<(j+1)):
        sum2[j][0]+=sum1[j][i]
    for i in range(1,1<<(j+1)):
        sum2[j][i]=sum2[j][i-1]+sum1[j][(-i+3*(1<<j))%(1<<(j+1))]-sum1[j][(-i+(1<<(j+1)))%(1<<(j+1))]
for _ in range(m):
    s,k=input().split()
    k=int(k)
    if s=='C':add+=k
    else:print(sum2[k][add%(1<<(k+1))])