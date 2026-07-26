# External reference: statistics page /practice/19962/
# Accepted submission: 52530564
# Source: http://cs101.openjudge.cn/practice/solution/52530564/
# License: not declared on the submission page; no license is inferred.

# External reference: cs101.openjudge.cn practice/19962 statistics, Accepted solution 52530564.
# Source: http://cs101.openjudge.cn/practice/solution/52530564/
# Statistics: http://cs101.openjudge.cn/practice/19962/statistics/
# License: not declared on submission page; no license inferred
n=int(input())
lis=list(map(int,input().split()))
lis=sorted(lis)
l=0
r=n-1
ans=0
while r>=l:
    ans=ans+lis[r]-lis[l]
    l+=1
    r-=1
print(ans)
