#!/usr/bin/env python3
# Codeforces 1793C Dora and Search —— 参考实现。
# 为本仓库编写的交接件（2026-09-17，特判数据重建），不取自任何提交，不套用外部许可。
#
# 双指针从两端往里收：区间 [l, r] 里的值恰是 lo..hi 这一段（排列的性质），端点若等于
# 当前最小值 lo 或最大值 hi，它不可能出现在任何更大的合法区间里，删掉它并收缩 lo/hi；
# 两端都不是最值时 [l, r] 就是答案。收到 l >= r 仍没找到则输出 -1。
import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0]); p = 1; out = []
    for _ in range(t):
        n = int(data[p]); a = data[p + 1:p + 1 + n]; p += 1 + n
        a = list(map(int, a))
        l, r, lo, hi = 0, n - 1, 1, n
        found = False
        while l < r:
            if a[l] == lo:
                l += 1; lo += 1
            elif a[l] == hi:
                l += 1; hi -= 1
            elif a[r] == lo:
                r -= 1; lo += 1
            elif a[r] == hi:
                r -= 1; hi -= 1
            else:
                found = True
                break
        out.append(f"{l + 1} {r + 1}" if found else "-1")
    sys.stdout.write("\n".join(out) + "\n")


main()
