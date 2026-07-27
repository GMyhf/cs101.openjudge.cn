# External reference: /practice/30936/statistics/
# Accepted submission: 52760548
# Source: http://cs101.openjudge.cn/practice/solution/52760548/
# License: not declared on the submission page; no license is inferred.

import sys
from collections import deque

def solve():
    # 读取输入
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    
    # 初始化牌堆，将 1 到 N 依次放入双端队列
    q = deque(range(1, N + 1))
    result = []
    
    # 模拟发牌过程
    while q:
        # 步骤1：取出最顶上的一张牌亮出来
        top_card = q.popleft()
        result.append(str(top_card))
        
        # 步骤2：如果牌堆不空，把新的最顶上的牌移到最底下
        if q:
            next_card = q.popleft()
            q.append(next_card)
            
    # 输出结果
    print(" ".join(result))

if __name__ == "__main__":
    solve()