# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1159: Palindrome
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/2025sp_routine/01159/
# License: not declared in source collection; no license is inferred.
import sys
N=int(input())
s=input()
if N==1:
    print(0)
    exit()
dp1=[0]*N
dp2=[0]*(N-1)
for i in range(N-1):
    if s[i]==s[i+1]:
        dp2[i]=0
    else:
        dp2[i]=1
for d in range(2,N):
    dp3=[0]*(N-d)
    for i in range(N-d):
        if s[i]==s[i+d]:
            dp3[i]=dp1[i+1]
        else:
            dp3[i]=min(dp2[i],dp2[i+1])+1
    dp1=dp2[:]
    dp2=dp3[:]
print(dp2[0])
