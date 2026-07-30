# External reference: http://cs101.openjudge.cn/practice/25561/statistics/
# Accepted submission: 51529390
# Source: http://cs101.openjudge.cn/practice/solution/51529390/
# License: not declared on the submission page; no license is inferred.

# 25561: 2022决战双十一
# n<9, m<6  —— 规模很小，直接枚举每个商品在哪个店买（DFS/暴力）就能过
#
# 规则梳理（从样例可验证）：
# 1) 跨店满减：按“所有商品标价总和”计算，每满 300 减 50，可叠加
#    cross = (total_price // 300) * 50
# 2) 店铺券：每家店最多用 1 张；若该店购买标价之和 >= q，则可减 x
#    若多张券都满足门槛，选“减免 x 最大”的那张；也可以不用券（等价于减 0）
# 3) 最终价 = total_price - cross - sum(store_best_coupon_discount)

import sys
input = sys.stdin.readline

n, m = map(int, input().split())

# offers[i] = [(shop, price), ...]  表示第 i 个商品在不同店铺的报价
offers = []
for _ in range(n):
    parts = input().split()
    opts = []
    for tok in parts:
        s_str, p_str = tok.split(':')
        opts.append((int(s_str), int(p_str)))
    offers.append(opts)

# coupons[j] = [(q,x), ...]  第 j 家店的所有券
coupons = [[] for _ in range(m + 1)]
for shop in range(1, m + 1):
    line = input().strip()
    if not line:
        coupons[shop] = []
        continue
    for tok in line.split():
        q_str, x_str = tok.split('-')
        coupons[shop].append((int(q_str), int(x_str)))

def best_coupon_discount(shop_sum: int, shop: int) -> int:
    """给定某店标价总和 shop_sum，返回该店最多能减多少（最多用一张券）"""
    best = 0
    for q, x in coupons[shop]:
        if shop_sum >= q and x > best:
            best = x
    return best

# DFS 枚举每个商品的购买店铺
store_sum = [0] * (m + 1)
best_final = 10**30  # 记录全局最小成交价

def dfs(i: int, total: int):
    global best_final
    if i == n:
        cross = (total // 300) * 50
        store_discount = 0
        for shop in range(1, m + 1):
            if store_sum[shop] > 0:
                store_discount += best_coupon_discount(store_sum[shop], shop)
        final = total - cross - store_discount
        if final < best_final:
            best_final = final
        return

    # 选择第 i 个商品在哪个店买
    for shop, price in offers[i]:
        store_sum[shop] += price
        dfs(i + 1, total + price)
        store_sum[shop] -= price

dfs(0, 0)
print(best_final)
