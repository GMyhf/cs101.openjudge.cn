# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2701: 与7无关的数
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024fallroutine/02701/
# License: not declared in source collection; no license is inferred.
n = int(input())

# 初始化平方和变量
square_sum = 0

# 遍历所有小于等于n的正整数
for num in range(1, n + 1):
    # 检查是否与7相关
    if num % 7 != 0 and '7' not in str(num):  # 不被7整除且十进制表示中不含数字7
        square_sum += num ** 2  # 累加平方值

print(square_sum)
