"""本仓库自写参考解；原题：dsa.openjudge.cn/2024final/C/。旋转坐标后求二维偏序。"""
import sys


def solve(text):
    a = list(map(int, text.split()))
    points = sorted((x+y, x-y) for x, y in zip(a[1::2], a[2::2]))
    ranks = {v: i+1 for i, v in enumerate(sorted({v for _, v in points}))}
    bit = [0] * (len(ranks) + 1)
    answer = 0
    for _, v in points:
        i = ranks[v]
        j = i
        while j:
            answer += bit[j]
            j -= j & -j
        while i < len(bit):
            bit[i] += 1
            i += i & -i
    return str(answer) + '\n'


if __name__ == '__main__':
    print(solve(sys.stdin.read()), end='')
