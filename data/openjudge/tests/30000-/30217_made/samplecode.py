# External reference: /practice/30217/statistics/
# Accepted submission: 52829473
# Source: http://cs101.openjudge.cn/practice/solution/52829473/
# License: not declared on the submission page; no license is inferred.

import sys
import bisect

def solve():
    # 快速读取输入
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    T = int(input_data[1])
    
    # 齿轮的最大齿数限制为 1,000,000
    MAX_VAL = 1000000
    pos = [None] * (MAX_VAL + 1)
    
    # 读取齿轮数据
    A = [int(x) for x in input_data[2:2+N]]
    
    # 记录每个数值出现的所有 1-based 索引位置
    for idx in range(1, N + 1):
        val = A[idx - 1]
        if pos[val] is None:
            pos[val] = []
        pos[val].append(idx)
        
    # 遍历每个 i，寻找符合条件的最小 j
    for i in range(1, N + 1):
        val = A[i - 1]
        target = T - val
        
        # 目标值必须在合法范围内
        if 1 <= target <= MAX_VAL:
            lst = pos[target]
            if lst is not None:
                # 使用二分查找在递增的索引列表中寻找第一个大于 i 的位置
                idx_in_lst = bisect.bisect_right(lst, i)
                if idx_in_lst < len(lst):
                    j = lst[idx_in_lst]
                    print(f"{i} {j}")
                    return

if __name__ == '__main__':
    solve()