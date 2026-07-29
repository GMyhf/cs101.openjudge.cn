# External reference: http://cs101.openjudge.cn/practice/01004/statistics/
# Accepted submission: 52722947
# Source: http://cs101.openjudge.cn/practice/solution/52722947/
# License: not declared on the submission page; no license is inferred.

total = 0.0
# 读取12行输入
for _ in range(12):
    money = float(input())
    total += money

avg = total / 12
# 格式化输出，保留两位小数
print(f"${avg:.2f}")
