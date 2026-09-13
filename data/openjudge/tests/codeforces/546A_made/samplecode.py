# Written for this repository from the public problem statement; no external submission used.
# 546A Soldier and Bananas —— 总价是等差数列 k·(1 + 2 + … + w)，钱够就不用借。
k, n, w = map(int, input().split())
cost = k * w * (w + 1) // 2
print(max(0, cost - n))
