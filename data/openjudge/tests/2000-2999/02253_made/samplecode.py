# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 2253: Frogger
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02253/
# License: not declared; no license is inferred.
import sys
_frog_lines = iter(sys.stdin.read().splitlines())
def input():
    for _frog_line in _frog_lines:
        if _frog_line.strip(): return _frog_line
    raise EOFError
"""
定义了一个frog_distance函数，它接受一个石头列表，并计算出青蛙从第一个石头跳到第二个石头的最小跳跃距离。
使用动态规划的思想，通过计算任意两个石头之间的直线距离，并利用最短路径算法（Floyd-Warshall算法）计算出最小跳跃距离。

在主循环中，读取输入并计算每个测试用例的青蛙距离。当输入的石头数量为0时，循环终止。

输出每个测试用例的结果，包括测试用例的序号和青蛙距离，保留3位小数。在每个测试用例后输出一个空行。
"""
import math

def frog_distance(stones):
    n = len(stones)
    distances = [[float('inf')] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i == j:
                distances[i][j] = 0
            else:
                x1, y1 = stones[i]
                x2, y2 = stones[j]
                distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                distances[i][j] = distance

    for k in range(n):
        for i in range(n):
            for j in range(n):
                distances[i][j] = min(distances[i][j], max(distances[i][k], distances[k][j]))

    return distances[0][1]

# 读取输入
test_case = 1
while True:
    n = int(input())
    if n == 0:
        break

    stones = []
    for _ in range(n):
        x, y = map(int, input().split())
        stones.append((x, y))

    # 计算青蛙距离
    distance = frog_distance(stones)

    # 输出结果
    print("Scenario #{}".format(test_case))
    print("Frog Distance = {:.3f}".format(distance))
    print()
    test_case += 1
