# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
from collections import deque

n = int(input())
ans = []

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.first_child = None
        self.next_sibling = None
    def __str__(self):
        return str(self.val)

def postorder(x):
    global ans
    if x is None:
        return
    y = x.first_child
    while y:
        postorder(y)
        y = y.next_sibling
    ans.append(x.val)

def inorder(x):
    global ans
    if x:
        inorder(x.first_child)
        ans.append(x.val)
        inorder(x.next_sibling)


for _ in range(n):
    s = input().split()
    root = TreeNode(s[0])
    q = deque([[root, int(s[1])]])
    i = 2
    while q:
        front = q.popleft()
        cur = front[0]
        for j in range(front[1]):
            if j == 0:
                cur.first_child = TreeNode(s[i])
                cur = cur.first_child
            else:
                cur.next_sibling = TreeNode(s[i])
                cur = cur.next_sibling
            q.append((cur, int(s[i+1])))
            i += 2
    #postorder(root)
    inorder(root)   #二叉树的中序遍历 = 原多叉树的后序遍历
print(*ans)
