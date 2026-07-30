# External reference: http://cs101.openjudge.cn/practice/30442/statistics/
# Accepted submission: 52831649
# Source: http://cs101.openjudge.cn/practice/solution/52831649/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    # 使用快速输入读取所有数据
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    t = int(input_data[0])
    idx = 1

    out = []
    for _ in range(t):
        n = int(input_data[idx])
        a = [int(x) for x in input_data[idx+1 : idx+1+n]]
        idx += 1 + n

        # 1. 计算初始邻项差绝对值总和 S
        total_diff = 0
        for i in range(n - 1):
            total_diff += abs(a[i+1] - a[i])

        # 2. 考虑删除第一个元素
        min_sum = total_diff - abs(a[1] - a[0])

        # 3. 考虑删除最后一个元素
        last_removal = total_diff - abs(a[n-1] - a[n-2])
        if last_removal < min_sum:
            min_sum = last_removal

        # 4. 考虑删除中间的第 i 个元素 (0 < i < n-1)
        for i in range(1, n - 1):
            current_sum = total_diff - abs(a[i] - a[i-1]) - abs(a[i+1] - a[i]) + abs(a[i+1] - a[i-1])
            if current_sum < min_sum:
                min_sum = current_sum

        out.append(str(min_sum))

    # 批量输出结果
    print('\n'.join(out))

if __name__ == '__main__':
    solve()
