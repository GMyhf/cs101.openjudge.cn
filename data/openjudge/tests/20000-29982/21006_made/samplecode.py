# User-supplied verified reference; platform Accepted submission #53000146
# Source: http://cs101.openjudge.cn/practice/solution/53000146/
# License: not declared; no license is inferred.

import sys


def count_ways(m, n):
    # 边界条件
    if m == 0 or n == 1:
        return 1

    # 苹果数少于盘子数
    if m < n:
        return count_ways(m, m)

    # 苹果数大于等于盘子数：有空盘子 + 没有空盘子
    return count_ways(m, n - 1) + count_ways(m - n, n)


def main():
    # 读取所有输入
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    m = int(input_data[0])
    n = int(input_data[1])

    # 计算并输出结果
    print(count_ways(m, n))


if __name__ == "__main__":
    main()
