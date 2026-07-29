# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1958: Strange Towers of Hanoi
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01958/
# License: not declared in source collection; no license is inferred.
import sys
d = [0] * 15
f = [float('inf')] * 15

d[1] = 1
for i in range(2, 13):
    d[i] = d[i - 1] * 2 + 1

f[1] = 1
for i in range(2, 13):
    for j in range(1, i):
        f[i] = min(f[i], f[i - j] * 2 + d[j])

for i in range(1, 13):
    print(f[i])
