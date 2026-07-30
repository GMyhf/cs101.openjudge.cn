# External reference: http://cs101.openjudge.cn/practice/26572/statistics/
# Accepted submission: 52724380
# Source: http://cs101.openjudge.cn/practice/solution/52724380/
# License: not declared on the submission page; no license is inferred.

import sys

sys.setrecursionlimit(10 ** 6)


class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def parse(s):
    n = len(s)
    i = 0

    def expr():
        # expr = term { + term }
        nonlocal i
        node = term()
        while i < n and s[i] == '+':
            op = s[i]
            i += 1
            right = term()
            node = Node(op, node, right)
        return node

    def term():
        # term = factor { * factor }
        nonlocal i
        node = factor()
        while i < n and s[i] == '*':
            op = s[i]
            i += 1
            right = factor()
            node = Node(op, node, right)
        return node

    def factor():
        # factor = number | (expr)
        nonlocal i

        if s[i].isdigit():
            start = i
            while i < n and s[i].isdigit():
                i += 1
            return Node(s[start:i])

        # 遇到左括号
        i += 1
        node = expr()
        i += 1  # 跳过右括号
        return node

    return expr()


def priority(node):
    if node.val == '+':
        return 1
    if node.val == '*':
        return 2
    return 3


def output(node, parent=None, is_right=False):
    # 数字直接输出
    if node.left is None and node.right is None:
        return node.val

    left = output(node.left, node, False)
    right = output(node.right, node, True)

    cur = left + node.val + right

    if parent is None:
        return cur

    p_cur = priority(node)
    p_parent = priority(parent)

    need = False

    # 子表达式优先级低，必须加括号
    if p_cur < p_parent:
        need = True

    # 子表达式优先级相同，并且是右孩子，必须加括号
    elif p_cur == p_parent and is_right:
        need = True

    if need:
        return "(" + cur + ")"
    else:
        return cur


def main():
    for line in sys.stdin:
        s = line.strip()
        if not s:
            continue
        root = parse(s)
        print(output(root))


if __name__ == "__main__":
    main()
