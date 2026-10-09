#!/usr/bin/env python3
"""1000000 KMP 字符比较次数（nextval）—— 参考实现（仓库交接件，非平台提交，不套用外部许可）。

先求 next（next[0] = -1，next[j] = p[0..j-1] 的最长相等真前后缀长度），再按
「p[j] == p[next[j]] 则 nextval[j] = nextval[next[j]]，否则 nextval[j] = next[j]」
求 nextval。匹配时每做一次 t[i] 与 p[j] 的比较计 1 次；j == -1 时只把 i、j 各后移，
不计数。第一次匹配成功（j == |p|）或主串扫完即停。
"""
import sys


def nextval_of(p):
    m = len(p)
    nxt = [-1] * m
    j, k = 0, -1
    while j < m - 1:
        if k == -1 or p[j] == p[k]:
            j += 1
            k += 1
            nxt[j] = k
        else:
            k = nxt[k]
    val = [-1] * m
    for j in range(1, m):
        val[j] = val[nxt[j]] if p[j] == p[nxt[j]] else nxt[j]
    return val


def main():
    p, t = sys.stdin.read().split()
    val = nextval_of(p)
    i = j = count = 0
    n, m = len(t), len(p)
    while i < n and j < m:
        if j == -1:
            i += 1
            j = 0
            continue
        count += 1
        if t[i] == p[j]:
            i += 1
            j += 1
        else:
            j = val[j]
    print(count, i - m if j == m else -1)


if __name__ == "__main__":
    main()
