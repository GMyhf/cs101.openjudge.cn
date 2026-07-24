# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def insert_into_bst(root, val):
    if root is None:
        return TreeNode(val)
    if val < root.val:
        root.left = insert_into_bst(root.left, val)
    elif val > root.val:
        root.right = insert_into_bst(root.right, val)
    return root

def preorder_traversal(root):
    return [root.val] + preorder_traversal(root.left) + preorder_traversal(root.right) if root else []

def preorderTraversal(root):
    if root is None:
        return []

    stack = []
    result = []
    stack.append(root)

    while stack:
        node = stack.pop()
        result.append(node.val)

        # 先将右子节点入栈，再将左子节点入栈
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return result

# 读取输入并转换成整数列表
numbers = list(map(int, input().split()))

# 构造二叉搜索树
bst_root = None
for num in numbers:
    bst_root = insert_into_bst(bst_root, num)

# 前序遍历二叉搜索树并输出
#print(' '.join(map(str, preorder_traversal(bst_root))))
print(' '.join(map(str, preorderTraversal(bst_root))))
