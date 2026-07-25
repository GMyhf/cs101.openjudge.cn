# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
from itertools import product

def right_shift(row, shift):
    return row[-shift:] + row[:-shift]

def calculate_max_column_sum(matrix):
    n = len(matrix)
    column_sums = [0] * n
    for row in matrix:
        for i, val in enumerate(row):
            column_sums[i] += val
    return max(column_sums)

def find_min_max_column_sum(n, original_matrix):
    min_max_sum = float('inf')

    # 产生所有行可能的移动方式
    all_shifts = list(product(range(n), repeat=n))
    for shifts in all_shifts:
        # 应用移动
        shifted_matrix = [
            right_shift(original_matrix[i], shifts[i]) for i in range(n)
        ]
        # 计算当前移动方式下的最大列和
        max_column_sum = calculate_max_column_sum(shifted_matrix)
        # 更新最小的最大列和
        min_max_sum = min(min_max_sum, max_column_sum)
    
    return min_max_sum

# 输入处理
results = []
while True:
    n = int(input())
    if n == 0:
        break
    
    original_matrix = [list(map(int, input().split())) for _ in range(n)]
    result = find_min_max_column_sum(n, original_matrix)
    results.append(result)

# 输出结果
for result in results:
    print(result)
