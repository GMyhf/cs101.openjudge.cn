# External reference: http://cs101.openjudge.cn/practice/30382/statistics/
# Accepted submission: 52740194
# Source: http://cs101.openjudge.cn/practice/solution/52740194/
# License: not declared on the submission page; no license is inferred.

import sys
from bisect import bisect_left

def solve():
    # 使用 sys.stdin.read 一次性读取，防止多次 I/O 带来的开销
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    s = input_data[0]
    t = input_data[1]

    n = len(s)
    m = len(t)

    # 1. 预处理 T 中每个字符出现的所有索引位置
    char_indices = [[] for _ in range(26)]
    ord_a = ord('a')
    for i, char in enumerate(t):
        char_indices[ord(char) - ord_a].append(i)

    # 2. 贪心计算最少需要的副本数 k
    k = 1
    curr_pos = 0 # 当前在 T 副本中的匹配位置

    for char in s:
        indices = char_indices[ord(char) - ord_a]
        if not indices:
            # S 中存在 T 中没有的字符，无法匹配
            print("-1")
            return

        # 使用二分查找寻找当前副本中第一个大于等于 curr_pos 的字符索引
        it = bisect_left(indices, curr_pos)

        if it < len(indices):
            # 在当前副本的剩余部分找到了
            curr_pos = indices[it] + 1
        else:
            # 当前副本匹配完了，需要开启一个新副本
            k += 1
            curr_pos = indices[0] + 1

    # 如果 1 个副本就够了，不需要任何操作
    if k == 1:
        print(0)
        return

    # 3. DP 计算最少操作次数
    # 这是一个经典的“复制与粘贴”问题，目标是得到至少 k 个副本。
    # 达到 x 个副本的最少次数等于其所有质因数之和。
    # 由于可以超过 k，我们需要在一个范围内寻找最小值。

    # 设置上限。考虑到 2^17 > 10^5，在这个范围内一定能找到最优解。
    limit = max(k + 500, 131072)
    if limit > 200005:
        limit = 200005

    # dp[i] 表示得到恰好 i 个副本的最少操作次数
    # 初始值设为 i，表示 1 次复制后进行 i-1 次粘贴
    dp = list(range(limit + 1))
    dp[0] = 0
    dp[1] = 0

    # 状态转移：从 i 个副本出发，复制一次，粘贴 (j-1) 次，得到 i*j 个副本
    # 总代价 = dp[i] + j
    for i in range(2, limit // 2 + 1):
        base_cost = dp[i]
        # v = i * j, 则 j = v // i
        # 这个循环类似于素数筛法，复杂度为 O(N log N)
        for v in range(i * 2, limit + 1, i):
            cost = base_cost + (v // i)
            if cost < dp[v]:
                dp[v] = cost

    # 在所有大于等于 k 的副本数中找最小值
    print(min(dp[k:]))

if __name__ == "__main__":
    solve()
