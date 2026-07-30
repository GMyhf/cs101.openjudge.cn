# External reference: http://cs101.openjudge.cn/practice/30212/statistics/
# Accepted submission: 52459310
# Source: http://cs101.openjudge.cn/practice/solution/52459310/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    # 读取输入 N 和 K
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    k = int(input_data[1])

    # 1. 预处理组合数 C(n, k)
    # N <= 10^18, 其二进制长度约为 60 层，预处理 66 层足够
    limit = 66
    c = [[0] * limit for _ in range(limit)]
    for i in range(limit):
        c[i][0] = 1
        for j in range(1, i + 1):
            c[i][j] = c[i-1][j-1] + c[i-1][j]

    # 2. 将 N 转换为二进制字符串
    s = bin(n)[2:]
    length = len(s)

    ans = 0
    ones_seen = 0

    # 3. 从高位向低位进行统计
    for i in range(length):
        if s[i] == '1':
            # 如果当前位在 N 中是 '1'
            # 我们尝试在这里填入 '0'，则构造出的数一定比 N 小
            # 剩余的可选位数
            remaining_positions = length - 1 - i
            # 还需要填入的 '1' 的数量
            needed_ones = k - ones_seen

            # 如果需要的 '1' 的数量在合理范围内，累加组合数
            if 0 <= needed_ones <= remaining_positions:
                ans += c[remaining_positions][needed_ones]

            # 填入 '1' 保持与 N 一致，继续向后看
            ones_seen += 1

    # 4. 判断 N 本身是否符合条件
    if ones_seen == k:
        ans += 1

    # 输出结果
    print(ans)

if __name__ == "__main__":
    solve()
