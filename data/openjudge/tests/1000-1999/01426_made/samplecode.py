#!/usr/bin/env python3
"""01426 Find The Multiple —— 参考实现（仓库交接件，非平台提交，不套用外部许可）。

按余数做 BFS：从 "1" 出发，每步在末尾接 0 或 1，状态是「当前数 mod n」。先到达余数 0
的就是位数最少、同位数里数值最小的 0/1 倍数。n<=200 时最长 19 位（n=198），远在
题面 100 位之内。答案不唯一，判题走 checker.py。
"""
import sys
from collections import deque


def smallest(n):
    parent = {1 % n: None}
    digit = {1 % n: "1"}
    queue = deque([1 % n])
    while queue:
        r = queue.popleft()
        if r == 0:
            break
        for d in (0, 1):
            t = (r * 10 + d) % n
            if t not in parent:
                parent[t] = r
                digit[t] = str(d)
                queue.append(t)
    out, r = [], 0
    while r is not None:
        out.append(digit[r])
        r = parent[r]
    return "".join(reversed(out))


def main():
    out = []
    for token in sys.stdin.read().split():
        n = int(token)
        if n == 0:
            break
        out.append(smallest(n))
    sys.stdout.write("".join(line + "\n" for line in out))


if __name__ == "__main__":
    main()
