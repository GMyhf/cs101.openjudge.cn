# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2676: 整数的个数
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02676/
# License: not declared; no license is inferred.
import sys
k = int(input())
numbers = list(map(int, input().split()))

# 初始化计数器
count_1 = 0
count_5 = 0
count_10 = 0

# 遍历列表，统计1、5和10出现的次数
for num in numbers:
    if num == 1:
        count_1 += 1
    elif num == 5:
        count_5 += 1
    elif num == 10:
        count_10 += 1

print(count_1)
print(count_5)
print(count_10)
