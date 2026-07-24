# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
import copy
n = int(input())
a = list(map(int, input().split()))
dp = copy.deepcopy(a)
for i in range(n):    
    for j in range(i):        
        if a[j] < a[i]:            
            dp[i] = max(dp[j] + a[i], dp[i])

print(max(dp))
