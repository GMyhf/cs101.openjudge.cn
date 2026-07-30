# External reference: http://cs101.openjudge.cn/practice/30947/statistics/
# Accepted submission: 52838616
# Source: http://cs101.openjudge.cn/practice/solution/52838616/
# License: not declared on the submission page; no license is inferred.

import sys
import math
from collections  import deque

input=sys.stdin.readline

n,q=map(int,input().split())
nums=list(map(int,input().split()))
nums = [max(1, v) for v in nums]
nums.sort(reverse=True)

def f(seq):
    key = deque()
    temp = math.isqrt(seq)
    for i in range(temp, 0, -1):
        if seq % i == 0:
            key.append(i)
            if i * i != seq:
                key.appendleft(seq // i)
    return key ,temp

sums=nums[:]
for i in range(n - 2, -1, -1):
    sums[i] = min(10 ** 9 + 1, sums[i + 1] * nums[i])

for t in range(q):

    num=int(input())
    key ,temp=f(num)
    lk=len(key)
    ans=0
    def dfs(key,step,temp,min1):
        global ans
        if step==n:
            if temp==1:
                ans=1
            return
        if temp==1:
            if sums[step]!=1:
                return
            else:
                ans=1
                return
        if step<n and temp<sums[step]:
            return
        for i in range(min1,lk):
            if key[i]<nums[step]:
                break
            if key[i]==1 and temp>1:
                break
            if temp%key[i]==0:
                dfs(key,step+1,temp//key[i],i)
                if ans==1 :
                    break
        if ans==1:
            return

    dfs(key,0,num,0)

    if ans:
        print('Yes')
    else:
        print('No')
