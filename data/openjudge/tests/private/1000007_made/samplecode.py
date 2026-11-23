"""本仓库自写参考解；原题：dsa.openjudge.cn/2024final/E/。Z 函数求最长公共前缀。"""
import sys


def solve(text):
    s, p = text.split()
    first = p.find('1')
    if first < 0:
        return s + 'a\n'
    suffix = s[first:]
    n = len(suffix)
    z = [0] * n
    z[0] = n
    left = right = 0
    for i in range(1, n):
        if i <= right:
            z[i] = min(right-i+1, z[i-left])
        while i+z[i] < n and suffix[z[i]] == suffix[i+z[i]]:
            z[i] += 1
        if i+z[i]-1 > right:
            left, right = i, i+z[i]-1
    length = min(z[i-first] for i in range(first, len(s)) if p[i] == '1')
    if not length:
        return '-1\n'
    candidate = suffix[:length]
    # 用 KMP 检查所有起点，包括第一个 1 以前的非预期匹配。
    pi = [0] * length
    j = 0
    for i in range(1, length):
        while j and candidate[i] != candidate[j]:
            j = pi[j-1]
        if candidate[i] == candidate[j]:
            j += 1
        pi[i] = j
    actual = bytearray(b'0' * len(s))
    j = 0
    for i, c in enumerate(s):
        while j and c != candidate[j]:
            j = pi[j-1]
        if c == candidate[j]:
            j += 1
        if j == length:
            actual[i-length+1] = 49
            j = pi[j-1]
    return candidate + '\n' if actual.decode() == p else '-1\n'


if __name__ == '__main__':
    print(solve(sys.stdin.read()), end='')
