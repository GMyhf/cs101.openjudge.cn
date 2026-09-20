#!/usr/bin/env python3
"""2140B 参考实现：y = 2x 恒成立。

设 y 有 L 位，则 concat(x, y) = x*10^L + y。取 y = 2x：
    concat = x*10^L + 2x = x*(10^L + 2)，而 x + y = 3x，
而 10^L ≡ 1 (mod 3)，所以 10^L + 2 ≡ 0 (mod 3)，于是 3x | x*(10^L+2)。
题面 x <= 10^8，故 y = 2x <= 2*10^8 <= 10^9，始终合法。

2026-09-20 之前这里写的是「在 y < 10^5 里线性扫」—— 那在 x 稍大时根本找不到解
（官方样例的 x = 9876543 就会直接抛异常），不是这道题的正确解法。
"""
import sys


def main():
    values = list(map(int, sys.stdin.buffer.read().split()))
    sys.stdout.write("\n".join(str(2 * x) for x in values[1:]) + "\n")


if __name__ == "__main__":
    main()
