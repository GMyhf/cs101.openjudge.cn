# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2936: 试剂配制
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02936/
# License: not declared; no license is inferred.
import sys
# 读取配方中物质的种类数目
N = int(input())
# 读取配方中包含的物质编号
formula = list(map(int, input().split()))

# 检查 1 号和 2 号物质是否同时存在
if 1 in formula and 2 in formula:
    print(0)
# 检查 3 号和 4 号物质是否同时存在
elif 3 in formula and 4 in formula:
    print(0)
# 检查 5 号和 6 号物质是否同时存在或同时不存在
elif (5 in formula) != (6 in formula):
    print(0)
# 检查 7 号和 8 号物质是否至少选择了一种
elif 7 not in formula and 8 not in formula:
    print(0)
else:
    # 如果所有条件都满足，输出 1
    print(1)
