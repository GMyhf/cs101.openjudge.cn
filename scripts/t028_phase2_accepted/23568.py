# External reference: http://cs101.openjudge.cn/practice/23568/statistics/
# Accepted submission: 52652379
# Source: http://cs101.openjudge.cn/practice/solution/52652379/
# License: not declared on the submission page; no license is inferred.

def trans(s):
    start,end,value=s.split()
    startmonth=int(start[0])
    startdata=int(start[2:])
    endmonth=int(end[0])
    enddata=int(end[2:])
    transstart=31*(startmonth-1)+startdata-7
    transend=31*(endmonth-1)+enddata-7
    return (transstart,transend,int(value))

n=int(input())
data=[]
for _ in range(0,n):
    temp=trans(input())
    if temp[1]<45:
        data.append(temp)
n=len(data)
data.sort(key=lambda x:x[1])
dp=[0]*(n+1)
lastdata=[-1]*(n+1)
for i in range(1,n+1):
    lastdata[i]=data[i-1][1]
for i in range(1,n+1):
    tempj=i
    while lastdata[tempj]>=data[i-1][0]:
        tempj-=1
    dp[i]=max(dp[tempj]+data[i-1][2],dp[i-1])

print(dp[n])
