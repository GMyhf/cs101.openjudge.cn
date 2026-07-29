# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 1577: Falling Leaves
# Fenced code block index: 5
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/01577/
# License: not declared in source collection; no license is inferred.
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def build_bst(leaves):
    if not leaves:
        return None

    root = TreeNode(leaves[0])
    for leaf in leaves[1:]:
        insert_node(root, leaf)

    return root


def insert_node(root, leaf):
    if leaf < root.data:
        if root.left is None:
            root.left = TreeNode(leaf)
        else:
            insert_node(root.left, leaf)
    else:
        if root.right is None:
            root.right = TreeNode(leaf)
        else:
            insert_node(root.right, leaf)


def preorder_traversal(root):
    if root is None:
        return []
    traversal = [root.data]
    traversal.extend(preorder_traversal(root.left))
    traversal.extend(preorder_traversal(root.right))
    return traversal


# 读取输入数据
flag = 0
while True:
    leaves = []
    while True:
        line = input().strip()
        if line == '*':
            break
        elif line == '$':
            flag = 1
            break
        else:
            leaves.extend(line)

    # 构建二叉搜索树
    root = build_bst(leaves[::-1])

    # 输出前序遍历结果
    traversal_result = preorder_traversal(root)
    print(''.join(traversal_result))

    if flag:
        break
