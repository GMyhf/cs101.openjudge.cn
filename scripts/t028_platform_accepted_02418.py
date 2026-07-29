# External reference: http://cs101.openjudge.cn/practice/02418/statistics/
# Accepted submission: 52718621
# Source: http://cs101.openjudge.cn/practice/solution/52718621/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    # 使用 sys.stdin.readline 替代 input() 以提高读取速度并节省内存
    readline = sys.stdin.readline

    counts = {}
    total = 0

    while True:
        line = readline()
        if not line:
            break

        # 去除行末的换行符，保留树木名称（名称中可能包含空格，所以不能直接 strip()）
        species = line.rstrip('\r\n')

        # 排除可能存在的空行
        if species:
            counts[species] = counts.get(species, 0) + 1
            total += 1

    if total == 0:
        return

    # 将树木名称按字典序排序
    sorted_species = sorted(counts.keys())

    # 格式化输出
    out = sys.stdout.write
    for species in sorted_species:
        # 计算百分比并保留 4 位小数
        percentage = (counts[species] / total) * 100
        out(f"{species} {percentage:.4f}\n")

if __name__ == '__main__':
    solve()
