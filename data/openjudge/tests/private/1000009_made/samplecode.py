"""本仓库自写参考解；原题：dsa.openjudge.cn/2022final1/1/。"""
import sys


def solve(text):
    s = text.strip()
    n = len(s)
    pi = [0] * n
    for i in range(1, n):
        j = pi[i-1]
        while j and s[i] != s[j]:
            j = pi[j-1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    period = n - pi[-1]
    return str(period if period == n else (-n) % period) + '\n'


if __name__ == '__main__':
    print(solve(sys.stdin.read()), end='')
