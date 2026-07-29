# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2287: Tian Ji -- The Horse Racing
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/pctbook/02287/
# License: not declared in source collection; no license is inferred.
import sys
import sys


def solve():
    # 读取所有输入
    input_data = sys.stdin.read().split()
    it = iter(input_data)

    while True:
        n = int(next(it))
        if n == 0:
            break

        tian = [int(next(it)) for _ in range(n)]
        king = [int(next(it)) for _ in range(n)]

        # 1. 排序
        tian.sort()
        king.sort()

        # 2. 初始化双指针
        # 田忌的头尾指针
        t_slow, t_fast = 0, n - 1
        # 齐王的头尾指针
        k_slow, k_fast = 0, n - 1

        money = 0

        # 进行 N 轮比赛
        for _ in range(n):
            # 情况1: 田忌最快 > 齐王最快 -> 赢
            if tian[t_fast] > king[k_fast]:
                money += 200
                t_fast -= 1
                k_fast -= 1

            # 情况2: 田忌最快 < 齐王最快 -> 输（用最慢消耗对方最快）
            elif tian[t_fast] < king[k_fast]:
                money -= 200
                t_slow += 1
                k_fast -= 1

            # 情况3: 田忌最快 == 齐王最快 -> 比较慢马
            else:
                # 3.1 田忌最慢 > 齐王最慢 -> 赢（用慢马拿下一胜）
                if tian[t_slow] > king[k_slow]:
                    money += 200
                    t_slow += 1
                    k_slow += 1
                # 3.2 其他情况 -> 用田忌最慢消耗齐王最快
                else:
                    # 这里需要判断一下胜负平
                    if tian[t_slow] < king[k_fast]:
                        money -= 200
                    # 如果相等则不加不减（平局），例如全员速度一样的情况

                    t_slow += 1
                    k_fast -= 1

        print(money)


if __name__ == "__main__":
    solve()
