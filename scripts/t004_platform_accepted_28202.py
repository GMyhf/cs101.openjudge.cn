# External reference: statistics page /practice/28202/
# Accepted submission: 52825193
# Source: http://cs101.openjudge.cn/practice/solution/52825193/
# License: not declared on the submission page; no license is inferred.

import sys

# 增加递归深度限制，防止大样本下发生溢出
sys.setrecursionlimit(2000)

def solve():
    # 使用快速输入读取所有数据
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    T = int(input_data[0])
    idx = 1
    out = []

    for _ in range(T):
        N = int(input_data[idx])
        S = input_data[idx+1]
        idx += 2

        def get_min_ops(L, R, char_val):
            # 基准情况：长度为 1
            if L == R:
                target_char = chr(97 + char_val)  # 97 是 'a' 的 ASCII 码
                return 0 if S[L] == target_char else 1

            M = (L + R) // 2
            target_char = chr(97 + char_val)

            # 选择一：左半部分全为 target_char，右半部分递归
            cnt_left = S.count(target_char, L, M + 1)
            cost_left = (M - L + 1) - cnt_left
            opt1 = cost_left + get_min_ops(M + 1, R, char_val + 1)

            # 选择二：左半部分递归，右半部分全为 target_char
            cnt_right = S.count(target_char, M + 1, R + 1)
            cost_right = (R - M) - cnt_right
            opt2 = get_min_ops(L, M, char_val + 1) + cost_right

            return opt1 if opt1 < opt2 else opt2

        # 从 1-阶好串开始，对应字符 'a' (char_val = 0)
        ans = get_min_ops(0, N - 1, 0)
        out.append(str(ans))

    print('\n'.join(out))

if __name__ == '__main__':
    solve()