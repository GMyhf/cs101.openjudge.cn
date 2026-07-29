# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2746: 约瑟夫问题
# Fenced code block index: 3
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024fallroutine/02746/
# License: not declared in source collection; no license is inferred.
import sys
while True:
    n, m = map(int, input().split())
    if n + m == 0:
        break
    a = 1  # 初始化 a 为 0，表示从 0 开始编号
    for i in range(2, n + 1):
        a = (a + m - 1) % i + 1
    print(a)  # 最终结果需要加 1，因为编号从 1 开始
