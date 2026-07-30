# External reference: http://cs101.openjudge.cn/practice/18176/statistics/
# Accepted submission: 51529047
# Source: http://cs101.openjudge.cn/practice/solution/51529047/
# License: not declared on the submission page; no license is inferred.

# 18176: 2050年成绩计算
# 规则：成绩必须是 t-prime 才算“有效成绩”，否则按 0 分计入平均分。
# t-prime 定义：整数 t 恰好有且仅有 3 个不同因子
# 结论：t-prime <=> t = p^2（p 为素数）
# 因为：p^2 的因子只有 1, p, p^2 三个（刚好3个）

import sys
import math

# ---------- 预处理：筛出 1e4 内的素数 ----------
# Xi <= 1e8 -> sqrt(Xi) <= 10000
MAX_R = 10000

is_prime = [True] * (MAX_R + 1)
is_prime[0] = is_prime[1] = False
for i in range(2, int(MAX_R ** 0.5) + 1):
    if is_prime[i]:
        step = i
        start = i * i
        for j in range(start, MAX_R + 1, step):
            is_prime[j] = False

def is_tprime(x: int) -> bool:
    """判断 x 是否为 t-prime：x 必须是某个素数的平方。"""
    if x < 4:  # 1,2,3 不可能是 t-prime；最小的 t-prime 是 4=2^2
        return False
    r = math.isqrt(x)         # r = floor(sqrt(x))
    if r * r != x:            # 不是完全平方数 => 不可能是 p^2
        return False
    return is_prime[r]        # sqrt(x) 是素数 => x 是 t-prime

# ---------- 读入并处理 ----------
input = sys.stdin.readline
m, n = map(int, input().split())  # n 仅给出“最多课程数”，每行实际可能少于 n

for _ in range(m):
    line = input().strip()

    # 极端情况：如果这一行为空（理论上不太会给），就按 0 输出
    if not line:
        print("0")
        continue

    scores = list(map(int, line.split()))
    cnt = len(scores)

    valid_sum = 0
    for x in scores:
        if is_tprime(x):
            valid_sum += x    # 有效成绩保留原分数
        # 否则按 0 分计入平均值（即不加到 valid_sum）

    if valid_sum == 0:
        # 题目要求：如果该生所有选课有效成绩是零分，则输出 0（不保留两位）
        print("0")
    else:
        avg = valid_sum / cnt
        print(f"{avg:.2f}")
