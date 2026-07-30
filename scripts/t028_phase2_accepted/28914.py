# External reference: http://cs101.openjudge.cn/practice/28914/statistics/
# Accepted submission: 52832137
# Source: http://cs101.openjudge.cn/practice/solution/52832137/
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
        l = int(input_data[idx])
        r = int(input_data[idx+1])
        x = int(input_data[idx+2])
        a = int(input_data[idx+3])
        b = int(input_data[idx+4])
        idx += 5

        # 0 步
        if a == b:
            out.append("0")
            continue

        # 1 步
        if abs(a - b) >= x:
            out.append("1")
            continue

        # 2 步
        # 路径 A: a -> l -> b
        # 路径 B: a -> r -> b
        can_use_l = (abs(a - l) >= x and abs(b - l) >= x)
        can_use_r = (abs(r - a) >= x and abs(r - b) >= x)
        if can_use_l or can_use_r:
            out.append("2")
            continue

        # 3 步
        # 路径 A: a -> l -> r -> b
        # 路径 B: a -> r -> l -> b
        can_l_to_r = (r - l >= x)
        can_path_l_r = (abs(a - l) >= x and can_l_to_r and abs(r - b) >= x)
        can_path_r_l = (abs(r - a) >= x and can_l_to_r and abs(b - l) >= x)
        if can_path_l_r or can_path_r_l:
            out.append("3")
            continue

        # 无法到达
        out.append("-1")

    print('\n'.join(out))

if __name__ == '__main__':
    solve()
