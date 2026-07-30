# External reference: http://cs101.openjudge.cn/practice/04068/statistics/
# Accepted submission: 52833058
# Source: http://cs101.openjudge.cn/practice/solution/52833058/
# License: not declared on the submission page; no license is inferred.

import sys


def solve():
    # 读取所有输入行
    input_lines = sys.stdin.read().splitlines()
    if not input_lines:
        return

    try:
        # 第一行为需要检测的数组个数 N
        n = int(input_lines[0].strip())
    except ValueError:
        return

    # 处理接下来的 N 行数据
    for i in range(1, n + 1):
        if i >= len(input_lines):
            break

        line = input_lines[i].strip()
        if not line:
            continue

        # 将输入的字符串转换为整数列表
        nums = list(map(int, line.split()))

        # 长度小于等于 2 的数组默认可以视为等差数列
        if len(nums) <= 2:
            print("True")
            continue

        # 排序
        nums.sort()

        # 计算初始公差
        diff = nums[1] - nums[0]
        is_ap = True

        # 验证后续相邻元素的差值是否一致
        for j in range(2, len(nums)):
            if nums[j] - nums[j - 1] != diff:
                is_ap = False
                break

        if is_ap:
            print("True")
        else:
            print("False")


if __name__ == "__main__":
    solve()
