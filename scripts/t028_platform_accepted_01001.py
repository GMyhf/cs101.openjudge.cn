# External reference: http://cs101.openjudge.cn/practice/01001/statistics/
# Accepted submission: 52522080
# Source: http://cs101.openjudge.cn/practice/solution/52522080/
# License: not declared on the submission page; no license is inferred.

from decimal import Decimal, getcontext
import sys

# 设置全局精度
# 题目中 R < 100, n <= 25，结果最多可能有约 150 位数字
# 设置 200 位足以覆盖所有情况
getcontext().prec = 200

def solve():
    for line in sys.stdin:
        parts = line.split()
        if not parts: continue

        # 使用 Decimal 读取 R
        r = Decimal(parts[0])
        n = int(parts[1])

        # 计算幂
        result = r ** n

        # 格式化输出
        # '{:f}'.format(result) 可以防止 Decimal 使用科学计数法输出
        s = '{:f}'.format(result.normalize())

        # 如果结果包含小数点
        if '.' in s:
            # 去掉末尾无意义的 0
            s = s.rstrip('0').rstrip('.')

        # 去掉前导的 0 (例如 0.123 -> .123)
        if s.startswith('0.'):
            s = s[1:]

        print(s)

if __name__ == "__main__":
    solve()
