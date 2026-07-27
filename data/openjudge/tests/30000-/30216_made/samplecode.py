# External reference: /practice/30216/statistics/
# Accepted submission: 52831634
# Source: http://cs101.openjudge.cn/practice/solution/52831634/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    # 读取输入
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    size = 1 << n
    
    # 1 代表不被赦免，初始化整个矩阵
    grid = [[1] * size for _ in range(size)]
    
    def pardon(x, y, L):
        if L == 1:
            return
        
        half = L // 2
        # 将左上角的子矩阵全部设为 0 (赦免)
        for r in range(x, x + half):
            grid[r][y : y + half] = [0] * half
            
        # 递归处理剩下的 3 个子矩阵
        pardon(x, y + half, half)          # 右上角
        pardon(x + half, y, half)          # 左下角
        pardon(x + half, y + half, half)    # 右下角
        
    # 从整个矩阵开始分治
    pardon(0, 0, size)
    
    # 按要求输出矩阵
    for row in grid:
        print(*(row))

if __name__ == '__main__':
    solve()