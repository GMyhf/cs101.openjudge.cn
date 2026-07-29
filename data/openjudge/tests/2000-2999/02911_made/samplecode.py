# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2911: 受限完全平方数
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02911/
# License: not declared; no license is inferred.
import sys
# 生成所有四位数的完全平方数
perfect_squares = []
for i in range(32, 100):  # 32^2 = 1024 是最小的四位数完全平方数，99^2 = 9801 是最大的四位数完全平方数
    perfect_squares.append(i ** 2)

# 生成所有每一位数字都相同的四位数
same_digit_numbers = []
for digit in range(1, 10):
    same_digit_numbers.append(int(str(digit) * 4))

# 读取输入的 MAX
MAX = int(input())

# 遍历所有可能的 A 和 B
for A in perfect_squares:
    if A >= MAX:
        continue
    for B in perfect_squares:
        if A > B:
            C = A - B
            if C in same_digit_numbers:
                print(A)
