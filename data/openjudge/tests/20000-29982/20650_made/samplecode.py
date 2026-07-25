# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
def longest_common_subsequence(s1, s2):
    dp = [[0 for _ in range(len(s2)+1)] for _ in range(len(s1)+1)]
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i] == s2[j]:
                dp[i+1][j+1] = dp[i][j] + 1
            else:
                dp[i+1][j+1] = max(dp[i+1][j], dp[i][j+1])
    return dp[len(s1)][len(s2)]

s1 = input()
s2 = input()
print(longest_common_subsequence(s1, s2))
