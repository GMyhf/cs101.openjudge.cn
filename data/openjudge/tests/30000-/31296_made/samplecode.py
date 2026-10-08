#!/usr/bin/env python3
"""31296 “淹园”救援 —— 参考实现（仓库交接件，非平台提交，不套用外部许可）。

排序后双指针：最重的人必须上船，能带上当前最轻的人就一起走（和恰好等于 C 也行），
带不上就独自一船。若最重的人连最轻的都带不上，他跟谁都配不成，单走不亏；
若带得上，把最轻的换给他也不会让剩下的人更难配对。
"""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    n, cap = int(data[0]), int(data[1])
    weights = sorted(map(int, data[2:2 + n]))
    i, j, boats = 0, n - 1, 0
    while i <= j:
        if i < j and weights[i] + weights[j] <= cap:
            i += 1
        j -= 1
        boats += 1
    print(boats)


if __name__ == "__main__":
    main()
