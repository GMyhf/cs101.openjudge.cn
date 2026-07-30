# External reference: http://cs101.openjudge.cn/practice/04072/statistics/
# Accepted submission: 52833092
# Source: http://cs101.openjudge.cn/practice/solution/52833092/
# License: not declared on the submission page; no license is inferred.

import sys


def solve():
    # 使用 split() 读取所有输入，可以很好地处理空格与换行
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)

    try:
        t = int(next(iterator))  # 测试组数
    except StopIteration:
        return

    for _ in range(t):
        n = int(next(iterator))  # 当前组的点数
        points = []
        for _ in range(n):
            x = float(next(iterator))
            y = float(next(iterator))
            points.append((x, y))

        # 点数小于或等于 2 时，必然共线
        if n <= 2:
            print("True")
            continue

        x0, y0 = points[0]
        x1, y1 = points[1]
        dx1 = x1 - x0
        dy1 = y1 - y0

        is_collinear = True
        # 依次检查后续所有点是否与前两个点共线
        for i in range(2, n):
            xi, yi = points[i]
            dxi = xi - x0
            dyi = yi - y0

            # 叉乘判断：(y1 - y0) * (xi - x0) == (yi - y0) * (x1 - x0)
            # 引入 1e-9 的容差解决浮点数精度问题
            if abs(dy1 * dxi - dyi * dx1) > 1e-9:
                is_collinear = False
                break

        if is_collinear:
            print("True")
        else:
            print("False")


if __name__ == "__main__":
    solve()
