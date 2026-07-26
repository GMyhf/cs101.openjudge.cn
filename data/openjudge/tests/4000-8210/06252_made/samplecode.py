# External reference: statistics page /practice/06252/
# Accepted submission: 52714777
# Source: http://cs101.openjudge.cn/practice/solution/52714777/
# License: not declared on the submission page; no license is inferred.

def is_match(pattern, s):
    m, n = len(pattern), len(s)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    
    dp[0][0] = True  # 空模式匹配空串
    
    # 处理模式开头的 '*'
    for i in range(1, m + 1):
        if pattern[i - 1] == '*':
            dp[i][0] = dp[i - 1][0]
        else:
            break  # 一旦出现非 '*'，后面不可能匹配空串
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if pattern[i - 1] == '*':
                dp[i][j] = dp[i - 1][j] or dp[i][j - 1]
            elif pattern[i - 1] == '?' or pattern[i - 1] == s[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
    
    return dp[m][n]


if __name__ == "__main__":
    pattern = input().strip()
    s = input().strip()
    
    if is_match(pattern, s):
        print("matched")
    else:
        print("not matched")