# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2940: 求和
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02940/
# License: not declared; no license is inferred.
import sys
# 读取输入的 a 和 n
a, n = map(int, input().split())

# 初始化总和为 0
Sn = 0
# 初始化当前项的值
current_num = 0

# 循环 n 次来计算每一项的值并累加到总和中
for i in range(n):
    # 计算当前项的值
    current_num = current_num * 10 + a
    # 将当前项的值累加到总和中
    Sn += current_num

# 输出总和
print(Sn)
