# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# 赵思懿，生科
class BinaryTreeNode:
    def __init__(self):
        self.parent = None
        self.left = None
        self.right = None

def tree_height(root):  # 计算二叉树高度
    if not root:
        return -1
    else:
        return max(tree_height(root.left), tree_height(root.right)) + 1

def original_tree_height(arr):  # 原树高度
    height, max_height = 0, 0
    for action in arr:
        if action == 'd':
            height += 1
        elif action == 'u':
            height -= 1
        max_height = max(max_height, height)
    return max_height

def build_binary_tree(arr):  # 根据输入序列建立二叉树
    root = BinaryTreeNode()
    current_node = root
    for action in arr:
        if action == 'd':
            current_node.left = BinaryTreeNode()
            current_node.left.parent = current_node
            current_node = current_node.left
        elif action == 'x':
            current_node.right = BinaryTreeNode()
            current_node.right.parent = current_node.parent
            current_node = current_node.right
        elif action == 'u':
            current_node = current_node.parent
    return root

input_sequence = input().replace('ud', 'x')
binary_tree_root = build_binary_tree(input_sequence)
print(original_tree_height(input_sequence), '=>', tree_height(binary_tree_root))

