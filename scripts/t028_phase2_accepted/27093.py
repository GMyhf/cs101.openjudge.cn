# External reference: http://cs101.openjudge.cn/practice/27093/statistics/
# Accepted submission: 52792293
# Source: http://cs101.openjudge.cn/practice/solution/52792293/
# License: not declared on the submission page; no license is inferred.

import sys
from bisect import bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    n, D = int(data[0]), int(data[1])

    T = 1
    while T < n + 2:
        T <<= 1
    NEG, POS = -1 << 60, 1 << 60
    smax = [NEG] * (2 * T)   # 每块最大值
    smin = [POS] * (2 * T)   # 每块最小值

    blocks = []   # blocks[j]: 该块的 chunk 列表（拼接后递增）
    cmins = []    # cmins[j]: 各 chunk 的首元素，用于块内二分
    nb = 0
    CH = 2048

    for tok in data[2:2 + n]:
        h = int(tok)
        hd, hD = h - D, h + D

        # 1. 从右数第一个含 [hd,hD] 之外元素的块 t（h 的可达范围到此为止）
        if smax[1] <= hD and smin[1] >= hd:
            t = -1
        else:
            x = 1
            while x < T:
                r = 2 * x + 1
                x = r if (smax[r] > hD or smin[r] < hd) else 2 * x
            t = x - T

        # 2. 定位插入块：优先 t 块的可达后缀，其次 t 之后第一个含 >h 元素的块
        j = -1
        if t >= 0:
            bm = smax[t + T]
            if bm <= hD and bm > h:
                j = t
        if j < 0:
            x = t + 1 + T
            while True:
                if smax[x] > h:
                    while x < T:
                        x <<= 1
                        if smax[x] <= h:
                            x |= 1
                    j = x - T
                    break
                while x & 1:
                    x >>= 1
                if x <= 1:
                    break
                x += 1

        if j >= 0:
            # 插入块 j 的有序位置
            cm, ch = cmins[j], blocks[j]
            ci = bisect_right(cm, h) - 1
            if ci < 0:
                ci = 0
            c = ch[ci]
            q = bisect_right(c, h)
            c.insert(q, h)
            if q == 0:
                cm[ci] = h
                if ci == 0 and h < smin[j + T]:
                    x = j + T
                    smin[x] = h
                    x >>= 1
                    while x:
                        a, b = smin[2 * x], smin[2 * x + 1]
                        smin[x] = a if a < b else b
                        x >>= 1
            if len(c) > CH:
                mid = len(c) >> 1
                ch[ci:ci + 1] = [c[:mid], c[mid:]]
                cm.insert(ci + 1, c[mid])
        else:
            if nb and smax[nb - 1 + T] <= h:
                # 追加到最后一块尾部
                jj = nb - 1
                c = blocks[jj][-1]
                c.append(h)
                if len(c) > CH:
                    mid = len(c) >> 1
                    blocks[jj][-1:] = [c[:mid], c[mid:]]
                    cmins[jj].append(c[mid])
                x = jj + T
                if h > smax[x]:
                    smax[x] = h
                    x >>= 1
                    while x:
                        a, b = smax[2 * x], smax[2 * x + 1]
                        smax[x] = a if a > b else b
                        x >>= 1
            else:
                # 新开一块
                blocks.append([[h]])
                cmins.append([h])
                x = nb + T
                smax[x] = smin[x] = h
                x >>= 1
                while x:
                    a, b = smax[2 * x], smax[2 * x + 1]
                    smax[x] = a if a > b else b
                    a, b = smin[2 * x], smin[2 * x + 1]
                    smin[x] = a if a < b else b
                    x >>= 1
                nb += 1

    out = []
    for ch in blocks:
        for c in ch:
            out.extend(c)
    sys.stdout.write(' '.join(map(str, out)))

main()
