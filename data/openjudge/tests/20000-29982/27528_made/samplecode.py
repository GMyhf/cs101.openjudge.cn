# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
def count_ways(N):
    if N == 1:
        return 1
    dp = [0] * (N + 1)
    dp[0] = 1  # Base case: 1 way to stay at the ground (0 steps)
    
    for i in range(1, N + 1):
        for j in range(1, i + 1):
            dp[i] += dp[i - j]
    
    return dp[N]

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    N = int(input().strip())
    print(count_ways(N))
