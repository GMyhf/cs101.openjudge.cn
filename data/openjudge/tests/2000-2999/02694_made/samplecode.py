# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2694: 波兰表达式
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024fallroutine/02694/
# License: not declared in source collection; no license is inferred.
import sys
'''
前缀表达式是运算符在前，操作数其后，
就是假如碰到一个运算符，其后就需要有连续的两个操作数才能运算消去，
否则就一直等待输入或者等待后面的运算结束得到操作数,
这恰好能用递归实现。
'''
# pylint: skip-file
def Exp():
    global pos
    pos += 1
    chr = calculatelist[pos]
    if chr == '+':
        return Exp() + Exp()
    elif chr == '-':
        return Exp() - Exp()
    elif chr == '*':
        return Exp() * Exp()
    elif chr == '/':
        return Exp() / Exp()
    else:
        return float(chr)



calculatelist = []
pos = -1
calculatelist = list(input().split())
result = Exp()
print(f"{result:.6f}")
