# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
def is_beautiful_brackets(sequence):
    stack = []
    # 对应关系字典，键为右括号，值为对应的左括号
    bracket_pairs = {')': '(', ']': '[', '}': '{'}
    
    for bracket in sequence:
        if bracket in bracket_pairs.values():
            # 若是左括号，压入栈中
            stack.append(bracket)
        elif bracket in bracket_pairs:
            # 若是右括号，检查栈顶元素是否匹配
            if stack and stack[-1] == bracket_pairs[bracket]:
                stack.pop()
            else:
                return "No"
        else:
            # 输入不合法的字符时，直接返回No
            return "No"
    # 栈为空表示括号序列美观
    return "Yes" if not stack else "No"

# 输入处理
sequence = input().strip()

# 输出结果
print(is_beautiful_brackets(sequence))
