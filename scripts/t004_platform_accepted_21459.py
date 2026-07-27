# External reference: statistics page /practice/21459/
# Accepted submission: 52832820
# Source: http://cs101.openjudge.cn/practice/solution/52832820/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    # 读取输入的正整数
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    x = int(input_data[0])
    
    # 当 x 大于 1 时，持续进行变换
    while x > 1:
        if x % 2 == 1:
            next_x = x * 3 + 1
            print(f"{x}*3+1={next_x}")
        else:
            next_x = x // 2
            print(f"{x}/2={next_x}")
        # 更新 x 的值
        x = next_x

if __name__ == '__main__':
    solve()