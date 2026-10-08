#!/usr/bin/env python3
"""31297 恒星共振裂变 —— 参考实现（仓库交接件，非平台提交，不套用外部许可）。

p1 + p2 = N 固定时，p1·p2 = p1(N-p1) 随 p1 越接近 N/2 越大，所以从 p1 = N/2 往下找
第一个使 p1 与 N-p1 都是质数的值。筛到 10^6（p2 最大接近 N，只筛到 N/2 不够）。
"""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    queries = list(map(int, data[1:1 + t]))
    limit = max(queries) + 1
    sieve = bytearray([1]) * limit
    sieve[0] = sieve[1] = 0
    for p in range(2, int(limit ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p::p] = bytes(len(range(p * p, limit, p)))
    out = []
    for n in queries:
        p = n // 2
        while not (sieve[p] and sieve[n - p]):
            p -= 1
        out.append(f"{p} {n - p}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
