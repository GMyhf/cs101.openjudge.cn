# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2754: 八皇后
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/02754/
# License: not declared in source collection; no license is inferred.
import sys
# 02754 八皇后, http://cs101.openjudge.cn/practice/02754/
list1 = []

def queen(s):
    if len(s) == 8:
        list1.append(s)
        return
    for i in range(1, 9):
        if all(str(i) != s[j] and abs(len(s) - j) != abs(i - int(s[j])) for j in range(len(s))):
            queen(s + str(i))

queen('')
samples = int(input())
for k in range(samples):
    print(list1[int(input()) - 1])

"""
abs(len(s) - j) != abs(i - int(s[j])) for j in range(len(s)) 是一个生成器表达式，
用于检查当前尝试放置的皇后是否与已经放置的皇后在同一条对角线上。具体解释如下：

- len(s) 表示当前已经放置的皇后的数量，即当前正在尝试放置的皇后的行号。
- j 是已经放置的皇后的列号。
- i 是当前尝试放置的皇后的列号。
- s[j] 是已经放置的皇后所在的列号。

对于每一个已经放置的皇后，检查以下条件：
- abs(len(s) - j) 计算当前尝试放置的皇后与已经放置的皇后之间的行差。
- abs(i - int(s[j])) 计算当前尝试放置的皇后与已经放置的皇后之间的列差。

如果行差和列差相等，说明两皇后在同一条对角线上，返回 `False`，否则返回 `True`。
"""
