# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
def min_population_flow(n, m, populations):
    # Initialize the prefix sum array for fast range sum computation
    prefix_sum = [0] * (n + 1)
    for i in range(1, n + 1):
        prefix_sum[i] = prefix_sum[i - 1] + populations[i - 1]
    
    # Initialize the DP table
    dp = [[float('inf')] * (m + 1) for _ in range(n + 1)]
    
    # Base case: with 0 control points, the flow index is just the sum of all populations times their district count
    for i in range(1, n + 1):
        dp[i][0] = prefix_sum[i] * i
    
    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(1, min(i, m) + 1):
            for k in range(j-1, i):
                dp[i][j] = min(dp[i][j], dp[k][j-1] + (prefix_sum[i] - prefix_sum[k]) * (i - k))
    
    # The answer is the minimum flow index after setting up m control points
    return dp[n][m]

# Input
n, m = map(int, input().split())
populations = list(map(int, input().split()))

# Output
print(min_population_flow(n, m, populations))
