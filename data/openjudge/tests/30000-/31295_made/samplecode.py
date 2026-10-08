#!/usr/bin/env python3
"""31295 宿舍的空调 —— 参考实现（仓库交接件，非平台提交，不套用外部许可）。

所有闭区间的交集是 [max l, min r]；非空时最低可行温度就是 max l，否则输出 -1。
注意 -1 本身也可能是合法温度（max l = -1 且交集非空），两种情况输出相同但含义不同。
"""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    ls = data[1:1 + 2 * n:2]
    rs = data[2:2 + 2 * n:2]
    low = max(map(int, ls))
    high = min(map(int, rs))
    print(low if low <= high else -1)


if __name__ == "__main__":
    main()
