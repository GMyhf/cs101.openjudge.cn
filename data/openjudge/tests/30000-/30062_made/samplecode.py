# External reference: /practice/30062/statistics/
# Accepted submission: 52831617
# Source: http://cs101.openjudge.cn/practice/solution/52831617/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    # 从标准输入读取所有数据并解析为整数
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    nums = []
    for token in input_data:
        try:
            nums.append(int(token))
        except ValueError:
            pass
            
    count = 0
    n = len(nums)
    
    def backtrack(start, path):
        nonlocal count
        # 如果当前子序列长度大于等于 2，计数加 1
        if len(path) >= 2:
            count += 1
            
        # 使用集合对当前层级的选择进行去重
        used = set()
        for i in range(start, n):
            # 如果当前元素已经在这一层被使用过，则跳过
            if nums[i] in used:
                continue
            
            # 判断是否满足非递减条件
            if not path or nums[i] >= path[-1]:
                used.add(nums[i])
                backtrack(i + 1, path + [nums[i]])
                
    backtrack(0, [])
    print(count)

if __name__ == '__main__':
    solve()