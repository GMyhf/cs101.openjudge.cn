# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
class Node:
    def __init__(self, x, depth):
        self.x = x
        self.depth = depth
        self.lchild = None
        self.rchild = None

    def preorder_traversal(self):
        nodes = [self.x]
        if self.lchild and self.lchild.x != '*':
            nodes += self.lchild.preorder_traversal()
        if self.rchild and self.rchild.x != '*':
            nodes += self.rchild.preorder_traversal()
        return nodes

    def inorder_traversal(self):
        nodes = []
        if self.lchild and self.lchild.x != '*':
            nodes += self.lchild.inorder_traversal()
        nodes.append(self.x)
        if self.rchild and self.rchild.x != '*':
            nodes += self.rchild.inorder_traversal()
        return nodes

    def postorder_traversal(self):
        nodes = []
        if self.lchild and self.lchild.x != '*':
            nodes += self.lchild.postorder_traversal()
        if self.rchild and self.rchild.x != '*':
            nodes += self.rchild.postorder_traversal()
        nodes.append(self.x)
        return nodes


def build_tree():
    n = int(input())
    for _ in range(n):
        tree = []
        stack = []
        while True:
            s = input()
            if s == '0':
                break
            depth = len(s) - 1
            node = Node(s[-1], depth)
            tree.append(node)

            # Finding the parent for the current node
            while stack and tree[stack[-1]].depth >= depth:
                stack.pop()
            if stack:  # There is a parent
                parent = tree[stack[-1]]
                if not parent.lchild:
                    parent.lchild = node
                else:
                    parent.rchild = node
            stack.append(len(tree) - 1)

        # Now tree[0] is the root of the tree
        yield tree[0]


# Read each tree and perform traversals
for root in build_tree():
    print("".join(root.preorder_traversal()))
    print("".join(root.postorder_traversal()))
    print("".join(root.inorder_traversal()))
    print()

