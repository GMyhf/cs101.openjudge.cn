# Source: /home/ubuntu/hongfei/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
from math import log2

def find_x(y):
    # 定义方程
    def equation(x):
        return x**2 + x + 1 + log2(x)

    # 二分查找解
    left, right = 0, y  # x的解显然在0和y之间，因为当x=y时，x^2 + x + 1 + log2(x) > y
    while right - left > 1e-8:  # 精确到小数点后8位
        mid = (left + right) / 2
        if equation(mid) < y:
            left = mid
        else:
            right = mid
    return (left + right) / 2

# 主程序开始
# 读取输入并计算答案
results = []
try:
    while True:
        y = int(input())
        x = find_x(y)
        results.append(x)
except EOFError:
    pass

# 输出结果
for x in results:
    print(f"{x:.4f}")
