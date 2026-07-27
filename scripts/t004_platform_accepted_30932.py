# External reference: /practice/30932/statistics/
# Accepted submission: 52760572
# Source: http://cs101.openjudge.cn/practice/solution/52760572/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    line = sys.stdin.readline().strip()
    if not line:
        return
    
    tokens = line.split()
    n = len(tokens)
    
    # 将字符串转换为整数或 None
    tree = []
    for token in tokens:
        if token == "null":
            tree.append(None)
        else:
            tree.append(int(token))
            
    result = []
    level = 0
    
    while True:
        start_idx = (1 << level) - 1      # 2^level - 1
        end_idx = (1 << (level + 1)) - 2  # 2^(level+1) - 2
        
        # 如果当前层的起始位置已经越界，说明没有更多层了
        if start_idx >= n:
            break
            
        max_val = None
        # 遍历当前层的所有可能位置
        for i in range(start_idx, min(end_idx + 1, n)):
            if tree[i] is not None:
                if max_val is None or tree[i] > max_val:
                    max_val = tree[i]
        
        # 题目保证第一个元素不是null，且层序遍历连续，所以max_val一定有值
        if max_val is not None:
            result.append(str(max_val))
        else:
            # 理论上不会出现全为null的情况，但为了严谨加上break
            break
            
        level += 1
        
    print(" ".join(result))

if __name__ == "__main__":
    solve()