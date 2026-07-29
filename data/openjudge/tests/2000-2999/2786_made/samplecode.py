# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2786: Pell数列
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024fallroutine/02786/
# License: not declared in source collection; no license is inferred.
dp = [0]*(1000000+1)
dp[1], dp[2] = 1, 2
for i in range(3, 1000000+1):
    dp[i] = (2*dp[i-1] + dp[i-2])%32767

for _ in range(int(input())):
    k = int(input())
    print(dp[k])
