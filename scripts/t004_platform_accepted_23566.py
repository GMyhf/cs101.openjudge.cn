# External reference: statistics page /practice/23566/
# Accepted submission: 52178654
# Source: http://cs101.openjudge.cn/practice/solution/52178654/
# License: not declared on the submission page; no license is inferred.

n,m=map(int,input().split())
lis=[0 for i in range(m)]
total=0
for i in range(n):
    x,y=map(int,input().split())
    lis[x-1]+=y
total=sum(lis)
total-=(total//200)*30
for i in range(m):
    s=input()
    ptr=0
    while "0"<=s[ptr]<="9":
        ptr+=1
    if lis[i]>=int(s[0:ptr]):
        total-=int(s[ptr+1:len(s)])
print(total)