# External reference: http://cs101.openjudge.cn/practice/25538/statistics/
# Accepted submission: 52832336
# Source: http://cs101.openjudge.cn/practice/solution/52832336/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    # 从标准输入读取数据
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])

    # 获取二进制表示并去除前缀 '0b'
    binary_str = bin(n)[2:]

    # 判断是否为回文串
    if binary_str == binary_str[::-1]:
        print("Yes")
    else:
        print("No")

if __name__ == '__main__':
    solve()
