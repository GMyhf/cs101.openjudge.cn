# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
def insert_hash_table(keys, M):
    table = [0.5] * M  # 用 0.5 表示空位
    result = []

    for key in keys:
        index = key % M
        i = index

        while True:
            if table[i] == 0.5 or table[i] == key:
                result.append(i)
                table[i] = key
                break
            i = (i + 1) % M

    return result

# 使用标准输入读取数据
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
M = int(data[1])
keys = list(map(int, data[2:2 + N]))

positions = insert_hash_table(keys, M)
print(*positions)

