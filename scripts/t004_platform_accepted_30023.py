# External reference: /practice/30023/statistics/
# Accepted submission: 52824900
# Source: http://cs101.openjudge.cn/practice/solution/52824900/
# License: not declared on the submission page; no license is inferred.

import sys
import re

def solve():
    # 读取所有输入数据
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    m = int(input_data[0])
    n = int(input_data[1])
    
    # 读取原子及其分子量
    weights = {}
    idx = 2
    for _ in range(m):
        atom = input_data[idx]
        weight = int(input_data[idx+1])
        weights[atom] = weight
        idx += 2
        
    # 读取待计算的化学式
    formulas = []
    for _ in range(n):
        formulas.append(input_data[idx])
        idx += 1
        
    # 用于匹配原子（一个大写字母或一个大写加一个小写字母）、数字、左括号和右括号的正则表达式
    token_pattern = re.compile(r'([A-Z][a-z]?|\d+|\(|\))')
    
    for formula in formulas:
        tokens = token_pattern.findall(formula)
        stack = []
        
        for token in tokens:
            if token == '(':
                stack.append('(')
            elif token == ')':
                # 弹出并累加，直到遇到 '('
                temp_sum = 0
                while stack and stack[-1] != '(':
                    temp_sum += stack.pop()
                if stack and stack[-1] == '(':
                    stack.pop()  # 弹出左括号
                stack.append(temp_sum)
            elif token.isdigit():
                val = int(token)
                if stack:
                    stack[-1] *= val
            else:
                # 如果是原子，将其分子量入栈
                stack.append(weights.get(token, 0))
        
        # 栈中剩余数值的总和即为该化学式的分子量
        print(sum(stack))

if __name__ == '__main__':
    solve()