# External reference: http://cs101.openjudge.cn/practice/27928/statistics/
# Accepted submission: 52727159
# Source: http://cs101.openjudge.cn/practice/solution/52727159/
# License: not declared on the submission page; no license is inferred.

import sys

# 增加递归深度，防止在处理较深的树时溢出
sys.setrecursionlimit(2000)

def solve():
    # 读取所有输入行
    input_lines = sys.stdin.read().splitlines()
    if not input_lines:
        return

    # 找到第一个包含整数（节点总数 n）的行
    n = -1
    line_idx = 0
    for i, line in enumerate(input_lines):
        import re
        nums = re.findall(r'\d+', line)
        if nums:
            n = int(nums[0])
            line_idx = i + 1
            break

    if n <= 0:
        return

    adj = {}        # 存储父子关系
    all_nodes = set()    # 存储所有出现的节点
    child_nodes = set()  # 存储所有作为子节点的节点

    # 读取接下来的 n 行关系
    processed_count = 0
    while processed_count < n and line_idx < len(input_lines):
        import re
        # 使用正则表达式提取行中所有的数字
        nums = [int(x) for x in re.findall(r'\d+', input_lines[line_idx])]
        if not nums:
            line_idx += 1
            continue

        parent = nums[0]
        children = nums[1:]

        adj[parent] = children
        all_nodes.add(parent)
        for c in children:
            child_nodes.add(c)
            all_nodes.add(c)

        processed_count += 1
        line_idx += 1

    # 寻找根节点：在所有节点中但从未作为子节点出现的节点
    root = -1
    for node in all_nodes:
        if node not in child_nodes:
            root = node
            break

    if root == -1:
        return

    # 按照题目要求的规则进行深度优先遍历
    def traverse(u):
        # 获取当前节点的直接子节点列表
        children_list = adj.get(u, [])
        # 将当前节点和所有子节点放在一起
        context = [u] + children_list
        # 按值从小到大排序
        context.sort()

        for val in context:
            if val == u:
                # 如果是当前节点，打印它的值
                print(val)
            else:
                # 如果是子节点，递归遍历子树
                traverse(val)

    traverse(root)

if __name__ == '__main__':
    solve()
