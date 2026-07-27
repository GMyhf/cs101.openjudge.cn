# External reference: statistics page /practice/26267/
# Accepted submission: 52740064
# Source: http://cs101.openjudge.cn/practice/solution/52740064/
# License: not declared on the submission page; no license is inferred.

def kmp_match(s, t):
    n = len(s)
    m = len(t)
    if m == 0:
        return True
    # 计算前缀函数
    pi = [0] * m
    for i in range(1, m):
        j = pi[i-1]
        while j > 0 and t[i] != t[j]:
            j = pi[j-1]
        if t[i] == t[j]:
            j += 1
        pi[i] = j
    # KMP匹配
    j = 0
    for i in range(n):
        while j > 0 and s[i] != t[j]:
            j = pi[j-1]
        if s[i] == t[j]:
            j += 1
        if j == m:
            return True
    return False

# 读取输入
S = input().strip()
T = input().strip()

# 输出结果
print("YES" if kmp_match(S, T) else "NO")