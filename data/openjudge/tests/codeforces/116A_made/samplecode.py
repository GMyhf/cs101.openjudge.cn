# Written for this repository from the public problem statement; no external submission used.
# 116A Tram —— 逐站模拟：先下车、再上车，记下车上人数的最大值。
import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    inside = best = 0
    for stop in range(n):
        leave, enter = int(data[1 + 2 * stop]), int(data[2 + 2 * stop])
        inside -= leave          # 题面：每一站所有下车的人先下
        inside += enter
        best = max(best, inside)
    print(best)


main()
