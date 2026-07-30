# External reference: http://cs101.openjudge.cn/practice/18146/statistics/
# Accepted submission: 51465624
# Source: http://cs101.openjudge.cn/practice/solution/51465624/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    # 读取所有输入数据
    input_data = sys.stdin.read().split()

    if not input_data:
        return

    iterator = iter(input_data)

    try:
        n = int(next(iterator))
        k = int(next(iterator))

        a = []
        for _ in range(k):
            a.append(int(next(iterator)))
    except StopIteration:
        return

    # 资源初始化
    # cnt4: 中间 4 人座 (3-4-5-6) 的数量
    cnt4 = n
    # cnt2: 两侧 2 人座 (1-2 和 7-8) 的数量
    cnt2 = 2 * n
    # cnt1: 拆分座位后产生的额外单人座数量
    cnt1 = 0

    # 第一步：处理 4 只一组的需求
    # 必须使用中间的 4 人座
    for i in range(k):
        while a[i] >= 4 and cnt4 > 0:
            a[i] -= 4
            cnt4 -= 1

    # 第二步：处理 2 只一组的需求
    # 优先使用两侧的 2 人座 (完美匹配，不浪费)
    for i in range(k):
        while a[i] >= 2 and cnt2 > 0:
            a[i] -= 2
            cnt2 -= 1

    # 第三步：如果还有 2 只一组的需求，只能拆中间的 4 人座
    # 逻辑：占用了中间的2个位(如3-4)，导致5必须空着(缓冲)，剩下6可以坐1个散客
    # 所以：消耗1个cnt4 -> 解决2只乌鸦 -> 产生1个cnt1
    for i in range(k):
        while a[i] >= 2 and cnt4 > 0:
            a[i] -= 2
            cnt4 -= 1
            cnt1 += 1

    # 第四步：统计剩余所有散客的总数
    remaining_crows = sum(a)

    # 第五步：计算剩余资源能容纳多少个散客 (单人容量)
    # 1. cnt1: 第三步拆分产生的单座
    # 2. cnt2: 剩下的2人座，每个只能坐1个散客 (另一个必须空着缓冲)
    # 3. cnt4: 剩下的4人座，每个可以坐2个散客 (例如坐3和6，中间4-5空着)
    total_capacity_1 = cnt1 + cnt2 + (cnt4 * 2)

    if remaining_crows <= total_capacity_1:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()
