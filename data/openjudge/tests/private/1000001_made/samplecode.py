#!/usr/bin/env python3
"""筛选法自底向上建立最小堆，返回实际交换次数。"""
import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    heap = [0] + data[1:n + 1]
    swaps = 0
    for root in range(n // 2, 0, -1):
        pos = root
        while 2 * pos <= n:
            child = 2 * pos
            if child + 1 <= n and heap[child + 1] < heap[child]:
                child += 1
            if heap[pos] <= heap[child]:
                break
            heap[pos], heap[child] = heap[child], heap[pos]
            swaps += 1
            pos = child
    print(swaps)


if __name__ == "__main__":
    main()
