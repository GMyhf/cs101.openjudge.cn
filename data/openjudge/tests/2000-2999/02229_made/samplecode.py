# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2229: Sumsets
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02229/
# License: not declared in source collection; no license is inferred.
import sys
# 按照整数划分来做
'''
递推式：
如果i为奇数：那么它一定可以由f[i-1]转移过来，是前面的那个数所有方案里都加了一个1

如果i为偶数：它可以看成是f[i-2]中的方案加了一个2，或者是f[i/2]的方案里乘了一个2；
所以应该是f[i-2]和f[i/2]的和

'''
MOD = 10**9
N = int(input())
dp = [1] + [0]*N
for i in range(1, N+1):
    if i & 1:
        dp[i] = dp[i-1]
    else:
        dp[i] = (dp[i-2] + dp[i//2]) % MOD #

print(dp[-1])
