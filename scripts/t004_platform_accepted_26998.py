# External reference: statistics page /practice/26998/
# Accepted submission: 52740058
# Source: http://cs101.openjudge.cn/practice/solution/52740058/
# License: not declared on the submission page; no license is inferred.

import sys
input = sys.stdin.read
data = input().split()

idx = 0
T = int(data[idx])
idx += 1

for _ in range(T):
    n = int(data[idx])
    idx += 1
    a = list(map(int, data[idx:idx+n]))
    idx += n

    dp = [0] * 32  # 0~31位足够

    for num in a:
        if num == 0:
            continue  # 0 & 任何数 =0，不能选

        # 收集所有为1的二进制位
        bits = []
        for b in range(32):
            if num & (1 << b):
                bits.append(b)

        # 当前能达到的最大长度
        max_len = 0
        for b in bits:
            if dp[b] > max_len:
                max_len = dp[b]
        cur = max_len + 1

        # 更新所有位
        for b in bits:
            if cur > dp[b]:
                dp[b] = cur

    print(max(dp))