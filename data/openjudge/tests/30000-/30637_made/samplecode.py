# External reference: http://cs101.openjudge.cn/practice/30637/statistics/
# Accepted submission: 52789468
# Source: http://cs101.openjudge.cn/practice/solution/52789468/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    # 读取所有输入行并去除两端的空白字符
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return

    # 第一行是原始入栈顺序字符串 x
    x = input_data[0].strip()

    # 后续行是需要判断的序列
    for line in input_data[1:]:
        target = line.strip()

        # 1. 长度如果不相等，肯定不是合法出栈序列
        if len(target) != len(x):
            print("NO")
            continue

        # 2. 模拟入栈出栈过程
        stack = []
        x_idx = 0  # 指向 x 中准备入栈的字符
        target_idx = 0  # 指向 target 中准备匹配的字符

        is_possible = True

        # 将 x 中的字符依次入栈
        for char in x:
            stack.append(char)
            # 只要栈不为空，且栈顶元素等于当前目标序列需要出栈的元素
            while stack and target_idx < len(target) and stack[-1] == target[target_idx]:
                stack.pop()
                target_idx += 1

        # 如果最后栈清空了，且目标序列所有字符都匹配完了
        if not stack and target_idx == len(x):
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
