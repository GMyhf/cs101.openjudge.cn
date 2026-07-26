# External reference: cs101.openjudge.cn practice/15265 statistics, Accepted solution 52720895.
# Source: http://cs101.openjudge.cn/practice/solution/52720895/
# Statistics: http://cs101.openjudge.cn/practice/15265/statistics/
# License: not declared on submission page; no license inferred
import sys
n=int(input())
nums=[int(x) for x in input().split()]
output=[]
k=4
while (1<<k)>n:
    k-=1
while k>0:
    t=(1<<k)-1
    for i in range(t):
        for j in range((n-1-i)//t+1):
            e,kk=nums[i+t*j],j
            while kk>0 and e<nums[i+t*(kk-1)]:
                nums[i+t*kk]=nums[i+t*(kk-1)]
                kk-=1
            nums[i+t*kk]=e
    output.append(' '.join(map(str,nums)))
    k-=1
sys.stdout.write('\n'.join(output)+'\n')
