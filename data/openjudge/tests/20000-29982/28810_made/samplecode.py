# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def insert(root, val):
    if not root:
        return TreeNode(val)
    if val < root.val:
        root.left = insert(root.left, val)
    else:
        root.right = insert(root.right, val)
    return root

def build_bst(sequence):
    root = None
    for num in sequence:
        root = insert(root, num)
    return root

def is_same_tree(t1, t2):
    if not t1 and not t2:
        return True
    if not t1 or not t2:
        return False
    if t1.val != t2.val:
        return False
    return is_same_tree(t1.left, t2.left) and is_same_tree(t1.right, t2.right)

# 主程序
def main():
    while True:
        try:
            N, L = map(int, input().split())
            if N == 0:
                break
            base_seq = list(map(int, input().split()))
            base_tree = build_bst(base_seq)

            for _ in range(L):
                check_seq = list(map(int, input().split()))
                check_tree = build_bst(check_seq)
                print("Yes" if is_same_tree(base_tree, check_tree) else "No")
        except EOFError:
            break

# 示例输入运行
if __name__ == "__main__":
    main()

