# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1064: 网线主管
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01064/
# License: not declared in source collection; no license is inferred.
import sys
def max_cable_length(cables, K):
    # 转换为整数（厘米）
    cables_cm = [int(round(c * 100)) for c in cables]
    low, high = 1, max(cables_cm) + 1  # 长度至少为1cm

    result = 0
    while low < high:
        mid = (low + high) // 2
        count = sum(cable // mid for cable in cables_cm)

        if count >= K:
            result = mid  # 尝试更长
            low = mid + 1
        else:
            high = mid

    # 输出结果以米为单位，并保留两位小数
    return f"{result / 100:.2f}" if result > 0 else "0.00"

# 输入读取部分
def main():
    N, K = map(int, input().split())
    cables = [float(input()) for _ in range(N)]
    print(max_cable_length(cables, K))


main()
