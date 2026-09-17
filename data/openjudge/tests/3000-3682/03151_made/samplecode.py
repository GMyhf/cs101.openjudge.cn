#!/usr/bin/env python3
"""03151 Pots —— 参考实现（仓库交接件，非平台提交，不套用外部许可）。

状态 (x, y) 是两壶里的水量，最多 101×101 个。从 (0, 0) 做 BFS，先弹出的「某一壶恰好
是 C」的状态就是最短操作数；沿父指针回溯出操作序列。扩展顺序固定为
FILL(1) FILL(2) DROP(1) DROP(2) POUR(1,2) POUR(2,1)。到不了输出 impossible。
最短序列不唯一，判题走 checker.py。
"""
import sys
from collections import deque


def moves(A, B, x, y):
    yield "FILL(1)", (A, y)
    yield "FILL(2)", (x, B)
    yield "DROP(1)", (0, y)
    yield "DROP(2)", (x, 0)
    t = min(x, B - y)
    yield "POUR(1,2)", (x - t, y + t)
    t = min(y, A - x)
    yield "POUR(2,1)", (x + t, y - t)


def solve(A, B, C):
    parent = {(0, 0): None}
    queue = deque([(0, 0)])
    while queue:
        state = queue.popleft()
        if C in state:
            ops = []
            while parent[state] is not None:
                state, op = parent[state]
                ops.append(op)
            return ops[::-1]
        for op, nxt in moves(A, B, *state):
            if nxt not in parent:
                parent[nxt] = (state, op)
                queue.append(nxt)
    return None


def main():
    A, B, C = map(int, sys.stdin.read().split()[:3])
    ops = solve(A, B, C)
    if ops is None:
        print("impossible")
    else:
        print(len(ops))
        print("\n".join(ops))


if __name__ == "__main__":
    main()
