# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2712: 细菌繁殖
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02712/
# License: not declared; no license is inferred.
import sys
# 定义每个月的天数（非闰年）
days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


# 计算某一天是这一年的第几天
def day_of_year(month, day):
    return sum(days_in_month[:month - 1]) + day


# 主程序
n = int(input())
results = []

for _ in range(n):
    # 输入一组测试数据
    month1, day1, count1, month2, day2 = map(int, input().split())

    # 计算第一天和要求的那一天分别是这一年的第几天
    day_of_year1 = day_of_year(month1, day1)
    day_of_year2 = day_of_year(month2, day2)

    # 计算相差的天数
    days_diff = day_of_year2 - day_of_year1

    # 计算细菌数目
    bacteria_count = count1 * (2 ** days_diff)

    # 存储结果
    results.append(bacteria_count)

# 输出所有结果
for result in results:
    print(result)
