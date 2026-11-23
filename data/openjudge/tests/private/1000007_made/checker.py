"""按实际出现位置检查任意合法 T；不要求与参考字符串相同。"""
from pathlib import Path
import sys


def check(data, actual, expected):
    s, p = data.split()
    tokens = actual.split()
    if len(tokens) != 1:
        return False
    t = tokens[0]
    if t == '-1':
        return expected.strip() == '-1'
    if not 1 <= len(t) <= 1000001 or any(not 'a' <= c <= 'z' for c in t):
        return False
    # KMP 与题意等价；线性扫描防止大量重叠出现导致检查器超时。
    pi = [0] * len(t)
    j = 0
    for i in range(1, len(t)):
        while j and t[i] != t[j]:
            j = pi[j-1]
        if t[i] == t[j]:
            j += 1
        pi[i] = j
    count = 0
    j = 0
    for i, c in enumerate(s):
        while j and c != t[j]:
            j = pi[j-1]
        if c == t[j]:
            j += 1
        if j == len(t):
            if p[i-len(t)+1] != '1':
                return False
            count += 1
            j = pi[j-1]
    return count == p.count('1')


if __name__ == '__main__':
    try:
        ok = check(*(Path(p).read_text(encoding='utf-8') for p in sys.argv[1:4]))
    except (ValueError, UnicodeError, IndexError):
        ok = False
    sys.exit(0 if ok else 1)
