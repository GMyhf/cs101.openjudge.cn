# 2026-07-25 回归扫描替换：题解原文是暴力搜索全部路径，n=18 要 143.5s，超判题 4s 上限；本实现与题解在 n=1..12 每次生成时对拍，n=18 手工核对一致
# 题解原文见同目录 producecase.py 的 BRUTE_SOURCE。
n = int(input())
a, b = 1, 3            # f(0)=1, f(1)=3, f(k)=2*f(k-1)+f(k-2)
for _ in range(max(0, n - 1)):
    a, b = b, 2 * b + a
print(b if n >= 1 else a)
