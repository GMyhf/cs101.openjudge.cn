# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2946: 玩游戏
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02946/
# License: not declared in source collection; no license is inferred.
import sys
# 读取第一行输入，获取起始整数 k 和游戏轮数 N
k, N = map(int, input().split())

# 循环进行 N 轮游戏
for _ in range(N):
    # 读取每一轮的运算符和整数
    operator, a = input().split()
    a = int(a)
    # 根据运算符进行相应的运算
    if operator == "plus":
        k = k + a
    elif operator == "minus":
        k = k - a
    elif operator == "multiply":
        k = k * a

# 输出最后一轮的运算结果
print(k)
