# External reference: http://cs101.openjudge.cn/practice/08210/statistics/
# Accepted submission: 51539263
# Source: http://cs101.openjudge.cn/practice/solution/51539263/
# License: not declared on the submission page; no license is inferred.

l,n,m=map(int,input().split())
stones=[0]
for i in range(n):
    a=int(input())
    stones.append(a)
stones.append(l)
delta=[stones[i+1]-stones[i] for i in range(n)]
def needed(s,steplength):
    cur=0
    re=0
    for i in range(1,len(s)):
        diff=s[i]-s[cur]
        if diff<steplength:
            re+=1
        else:
            cur=i
    return re

left=min(delta)
right=l
#j=0
while left<right:
    mid=(left+right+1)//2
    #print('mid=',mid)
    a=needed(stones,mid)
    #print('needed=',a)
    #print('left=',left)
    #print('right=',right)
    if a<=m:
        left=mid
    else:
        right=mid-1
    #j+=1
    #print()
print(left)
