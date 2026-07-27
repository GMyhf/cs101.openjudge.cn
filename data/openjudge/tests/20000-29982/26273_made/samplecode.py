# External reference: statistics page /practice/26273/
# Accepted submission: 52740062
# Source: http://cs101.openjudge.cn/practice/solution/52740062/
# License: not declared on the submission page; no license is inferred.

def main():
    import sys
    s = sys.stdin.readline().strip()
    n = len(s)
    if n == 0:
        print()
        return

    # 计算前缀函数（next数组）
    pi = [0] * n
    for i in range(1, n):
        j = pi[i-1]
        while j > 0 and s[i] != s[j]:
            j = pi[j-1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j

    res = []
    cur = pi[-1]
    while cur > 0:
        res.append(n - cur)
        cur = pi[cur - 1]
    res.append(n)  # 自身一定是周期

    res.sort()
    print(' '.join(map(str, res)))

if __name__ == "__main__":
    main()