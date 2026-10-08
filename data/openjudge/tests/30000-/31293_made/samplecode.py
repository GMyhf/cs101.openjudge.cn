#!/usr/bin/env python3
"""31293 双十一凑单大作战 —— 参考实现（仓库交接件，非平台提交，不套用外部许可）。

每组免掉的是组里最便宜的那件。把价格从高到低排好，按 (1,2,3)(4,5,6)… 三个一组，
免掉的就是第 3、6、9… 件 —— 这是能免掉的最大总额：第 k 件免费的商品前面至少要有
2k 件不比它便宜的商品陪着，所以第 k 大的免单额不可能超过排序后第 3k 件的价格。
凑不满 3 件的尾巴照原价付。
"""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    prices = sorted(map(int, data[1:1 + n]), reverse=True)
    print(sum(prices) - sum(prices[2::3]))


if __name__ == "__main__":
    main()
