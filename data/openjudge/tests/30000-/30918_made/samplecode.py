# External reference: /practice/30918/statistics/
# Accepted submission: 52760611
# Source: http://cs101.openjudge.cn/practice/solution/52760611/
# License: not declared on the submission page; no license is inferred.

import sys
from array import array

# 一次性读取所有输入并切分
input_data = sys.stdin.buffer.read().split()
if not input_data:
    sys.exit(0)

n = int(input_data[0])
total_elements = n * n

# 预定义一个返回无穷大的常量（因为 array 不支持 float('inf')，我们用一个大数代替）
INF = 10**9 

def count_factor(x, p):
    """计算 x 中包含质因数 p 的个数"""
    if x == 0:
        return INF  
    cnt = 0
    while x % p == 0:
        cnt += 1
        x //= p
    return cnt

def solve_min_path(matrix_bytes, factor_type):
    """
    利用一维原生数组实现滚动 DP
    matrix_bytes: 包含所有矩阵元素的一维字节流解析后的原生数组
    factor_type: 2 或 5
    """
    # 使用 'i' (signed int) 创建紧凑的一维数组，极大节省内存
    dp = array('i', [INF] * n)
    
    # 初始化第一行第一个元素
    first_val = int(matrix_bytes[0])
    dp[0] = count_factor(first_val, factor_type)
    
    # 初始化第一行剩余元素
    for j in range(1, n):
        val = int(matrix_bytes[j])
        dp[j] = dp[j-1] + count_factor(val, factor_type)
        
    # 逐行进行状态转移
    row_idx = 1
    while row_idx < n:
        start_pos = row_idx * n
        
        # 处理每一行的第一个元素（第一列）
        first_val = int(matrix_bytes[start_pos])
        dp[0] = dp[0] + count_factor(first_val, factor_type)
        
        # 处理该行剩余的元素
        for j in range(1, n):
            val = int(matrix_bytes[start_pos + j])
            # dp[j] 未更新前是上一行的值（正上方），dp[j-1] 是当前行已更新的值（正左方）
            top = dp[j]
            left = dp[j-1]
            dp[j] = (top if top < left else left) + count_factor(val, factor_type)
            
        row_idx += 1
        
    return dp[n-1]

# 将输入数据直接映射为紧凑的原生整数数组，避免 Python list 的巨大开销
matrix_flat = array('i', (int(x) for x in input_data[1:1+total_elements]))

# 检查是否存在 0
has_zero = any(val == 0 for val in matrix_flat)

# 分别计算最少因子 2 和最少因子 5
min_2 = solve_min_path(matrix_flat, 2)
min_5 = solve_min_path(matrix_flat, 5)

ans = min_2 if min_2 < min_5 else min_5

# 如果原矩阵中有 0，那么一定存在一条经过 0 的路径，其乘积为 0，末尾恰好有 1 个 0
if has_zero:
    ans = 1 if ans > 1 else ans

print(ans)