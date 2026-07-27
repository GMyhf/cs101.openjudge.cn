# External reference: /practice/29694/statistics/
# Accepted submission: 52824892
# Source: http://cs101.openjudge.cn/practice/solution/52824892/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    # 从标准输入中读取所有音节
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    stack = []
    for x in input_data:
        stack.append(x)
        
        # 优先检测单音节叠音 (如 3 3)
        if len(stack) >= 2 and stack[-1] == stack[-2]:
            stack.pop()
        # 检测双音节叠音 (如 1 2 1 2)
        elif len(stack) >= 4 and stack[-4:-2] == stack[-2:]:
            stack.pop()
            stack.pop()
            
    # 输出还原后的原始歌词
    print(" ".join(stack))

if __name__ == '__main__':
    solve()