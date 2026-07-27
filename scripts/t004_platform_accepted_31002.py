# External reference: /practice/31002/statistics/
# Accepted submission: 52760512
# Source: http://cs101.openjudge.cn/practice/solution/52760512/
# License: not declared on the submission page; no license is inferred.

import sys


def find_treasure():
    # 读取输入
    try:
        map_str = sys.stdin.readline().strip()
        treasure = sys.stdin.readline().strip()
    except Exception:
        return

    # 获取字符串长度
    map_len = len(map_str)
    treasure_len = len(treasure)

    # 存储所有找到的起始索引
    indices = []

    # 只有当地图长度不小于宝藏长度时才进行匹配
    if map_len >= treasure_len and treasure_len > 0:
        for i in range(map_len - treasure_len + 1):
            # 截取等长子串并对比
            if map_str[i : i + treasure_len] == treasure:
                indices.append(i)

    # 输出结果
    print(treasure)
    if indices:
        print(" ".join(map(str, indices)))
    else:
        print("NoTreasure")


if __name__ == "__main__":
    find_treasure()