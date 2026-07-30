# External reference: http://cs101.openjudge.cn/practice/04069/statistics/
# Accepted submission: 52833072
# Source: http://cs101.openjudge.cn/practice/solution/52833072/
# License: not declared on the submission page; no license is inferred.

import sys


def solve():
    # 使用 split() 可以自动忽略所有的换行符和多余空格，从而获取所有的输入 Token
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)

    try:
        m = int(next(iterator))  # 测试样例组数
    except StopIteration:
        return

    for _ in range(m):
        k = int(next(iterator))  # 预算
        n = int(next(iterator))  # 手机总数

        phones = []
        for _ in range(n):
            pid = int(next(iterator))
            price = int(next(iterator))
            sales = int(next(iterator))
            rating = int(next(iterator))
            phones.append((pid, price, sales, rating))

        # 1. 过滤：只保留价格在预算 k 以内的手机
        affordable = [p for p in phones if p[1] <= k]

        # 2. 排序：
        # 销量降序（对应 -p[2]）
        # 评分降序（对应 -p[3]）
        # 价格升序（对应 p[1]）
        affordable.sort(key=lambda p: (-p[2], -p[3], p[1]))

        # 3. 输出排序后的手机 id
        for p in affordable:
            print(p[0])


if __name__ == "__main__":
    solve()
