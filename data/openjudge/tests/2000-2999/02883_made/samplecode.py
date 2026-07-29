# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2883: Checking order
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02883/
# License: not declared; no license is inferred.
import sys
while True:
    try:
        # 读取输入的长度为 5 的数字串
        nums = list(map(int, input().split()))
        # 复制一份原始列表用于排序
        sorted_nums = sorted(nums)

        if nums == sorted_nums:
            print("Yes")
        else:
            print("No", " ".join(map(str, sorted_nums)))
    except EOFError:
        break
