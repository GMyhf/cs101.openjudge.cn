"""本仓库自写参考解；原题：dsa.openjudge.cn/2025final/C/。"""
from bisect import bisect_right
import sys


def solve(text):
    tokens = text.split()
    na, nb, k, q = map(int, tokens[:4])
    a, b = tokens[4:6]
    forbidden = {(tokens[6 + 2*i], tokens[7 + 2*i]) for i in range(k)}
    allowed = {c: ''.join(d for d in b if (c, d) not in forbidden) for c in set(a)}
    ends = [0]
    for c in a:
        ends.append(ends[-1] + 2 * len(allowed[c]))
    answer = []
    for t in map(int, tokens[6 + 2*k:]):
        i = bisect_right(ends, t) - 1
        offset = t - ends[i]
        answer.append(a[i] if offset % 2 == 0 else allowed[a[i]][offset // 2])
    return '\n'.join(answer) + '\n'


if __name__ == '__main__':
    print(solve(sys.stdin.read()), end='')
