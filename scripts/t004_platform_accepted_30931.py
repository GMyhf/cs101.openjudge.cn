# External reference: /practice/30931/statistics/
# Accepted submission: 52760575
# Source: http://cs101.openjudge.cn/practice/solution/52760575/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    # 读取输入并去除首尾可能的换行符
    s = sys.stdin.readline().strip()
    
    stack = []
    max_depth = 0
    
    # 定义左右括号的映射关系
    match_map = {')': '(', ']': '[', '}': '{'}
    left_brackets = set(['(', '[', '{'])
    
    for char in s:
        if char in left_brackets:
            # 遇到左括号，入栈
            stack.append(char)
            # 更新最大嵌套深度
            if len(stack) > max_depth:
                max_depth = len(stack)
        elif char in match_map:
            # 遇到右括号
            if not stack:
                print("Invalid")
                return
            top = stack.pop()
            # 检查是否匹配
            if top != match_map[char]:
                print("Invalid")
                return
        else:
            # 题目保证只有这六种字符，但为了严谨可以忽略或报错
            pass
            
    # 遍历结束后，检查栈是否为空
    if stack:
        print("Invalid")
    else:
        print(max_depth)

if __name__ == "__main__":
    solve()