# External reference: statistics page /practice/23556/
# Accepted submission: 52832495
# Source: http://cs101.openjudge.cn/practice/solution/52832495/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    # 从标准输入读取荷叶数量 n
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])

    # 边界情况处理
    if n == 1:
        print(1)
        return
    if n == 2:
        print(2)
        return

    # 使用滚动变量优化空间复杂度到 O(1)
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b

    print(b)

if __name__ == '__main__':
    solve()