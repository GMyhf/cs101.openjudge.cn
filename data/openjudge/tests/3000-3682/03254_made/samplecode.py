# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 3254: 约瑟夫问题No.2
# Fenced code block index: 3
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/pctbook/03254/
# License: not declared in source collection; no license is inferred.
import sys
from collections import deque

while True:
    n, p, m = map(int, input().split())
    if n == p == m == 0:
        break
    queue = deque([i for i in range(p, n + 1)] + [i for i in range(1, p)])
    out = []
    while queue:
        for _ in range(m - 1):
            queue.append(queue.popleft())
        out.append(queue.popleft())
    print(*out, sep=",")
