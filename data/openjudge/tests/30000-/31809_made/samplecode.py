"""本仓库自写参考解；原题：dsa.openjudge.cn/2023final/2/。"""
import sys


def solve(text):
    it = iter(map(int, text.split()))
    answer = []
    for _ in range(next(it)):
        first = {}
        found = False
        for i in range(next(it)):
            x = next(it)
            if x in first and i-first[x] >= 2:
                found = True
            first.setdefault(x, i)
        answer.append('YES' if found else 'NO')
    return '\n'.join(answer) + '\n'


if __name__ == '__main__':
    print(solve(sys.stdin.read()), end='')
