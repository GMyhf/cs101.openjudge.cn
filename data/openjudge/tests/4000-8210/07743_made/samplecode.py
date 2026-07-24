# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
import sys

data = iter(sys.stdin.read().strip().split())
try:
    m = int(next(data))
    n = int(next(data))
except StopIteration:
    # 输入不足
    print(0)
    sys.exit()

# 读取矩阵（假设输入格式正确，恰好有 m*n 个整数）
matrix = [[int(next(data)) for _ in range(n)] for _ in range(m)]

total = 0
if m == 0 or n == 0:
    total = 0
elif m == 1:
    # 只有一行，边缘就是这一整行
    total = sum(matrix[0])
elif n == 1:
    # 只有一列，边缘就是这一整列
    total = sum(row[0] for row in matrix)
else:
    # 普通情况：首行 + 末行 + 中间行的首列和末列
    total += sum(matrix[0])      # 第一行
    total += sum(matrix[-1])     # 最后一行
    for i in range(1, m-1):
        total += matrix[i][0] + matrix[i][-1]

print(total)
