#!/usr/bin/env python3
"""31298 警察招募又来了 —— 参考实现（仓库交接件，非平台提交，不套用外部许可）。

队列里按入伍时间存 [时刻, 剩余空闲人数]。第 t 分钟出犯罪时，先把队首入伍时刻
s 满足 s + k - 1 < t（已退役）的批次整批弹掉，再从队首（最早入伍）派一人；队列空则
这起犯罪无法处理。每批最多 10 人、每分钟一个事件，总复杂度 O(n)。
"""
import sys
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    queue = deque()
    missed = 0
    for t in range(1, n + 1):
        a = int(data[1 + t])
        if a > 0:
            queue.append([t, a])
            continue
        while queue and queue[0][0] + k - 1 < t:
            queue.popleft()
        if not queue:
            missed += 1
            continue
        queue[0][1] -= 1
        if queue[0][1] == 0:
            queue.popleft()
    print(missed)


if __name__ == "__main__":
    main()
