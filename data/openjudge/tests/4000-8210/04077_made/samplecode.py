# 2026-07-25 回归扫描替换：题解原文是暴力 DFS，n=15 要 63.6s，超判题 4s 上限；本实现与题解在 n=1..11 每次生成时对拍，n=15 手工核对一致
# 题解原文见同目录 producecase.py 的 BRUTE_SOURCE。
import math
n = int(input())
print(math.comb(2 * n, n) // (n + 1))
