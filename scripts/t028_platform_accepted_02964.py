# External reference: http://cs101.openjudge.cn/practice/02964/statistics/
# Accepted submission: 46688207
# Source: http://cs101.openjudge.cn/practice/solution/46688207/
# License: not declared on the submission page; no license is inferred.

import calendar

def is_leap_year(year):
    """判断是否为闰年"""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def find_date_from_days(days):
    # 2000年1月1日是星期六
    start_year = 2000
    start_day_of_week = 6  # 0代表星期一，6代表星期日

    # 存储每个星期的名字
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # 逐年减少天数，直到找出是哪一年
    year = start_year
    while True:
        days_in_year = 366 if is_leap_year(year) else 365
        if days < days_in_year:
            break
        days -= days_in_year
        year += 1

    # 每年每个月的天数
    days_in_months = [31, 28 + is_leap_year(year), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # 逐月减少天数，直到找出是哪一月
    month = 1
    for days_in_month in days_in_months:
        if days < days_in_month:
            break
        days -= days_in_month
        month += 1

    # 此时days是当月的第几天（从0开始，所以要加1）
    day = days + 1

    # 计算总天数，并根据它确定星期几
    total_days = (days + (year - start_year) * 365 + sum([is_leap_year(y) for y in range(start_year, year)]))
    day_of_week = calendar.weekday(year, month, day)

    # 返回日期格式
    return f"{year:04d}-{month:02d}-{day:02d} {week_days[day_of_week]}"

# 处理输入输出
while True:
    days_since_2000 = int(input())
    if days_since_2000 == -1:
        break
    print(find_date_from_days(days_since_2000))
