# External reference: http://cs101.openjudge.cn/practice/01610/statistics/
# Accepted submission: 44188104
# Source: http://cs101.openjudge.cn/practice/solution/44188104/
# License: not declared on the submission page; no license is inferred.

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.children = []

def build(n, matrix):
    check = sum(sum(row) for row in matrix)
    if check == 0:
        return TreeNode('00')
    elif check == n**2:
        return TreeNode('01')
    else:
        a = [matrix[i][:n//2] for i in range(n//2)]
        b = [matrix[i][n//2:] for i in range(n//2)]
        c = [matrix[i][:n//2] for i in range(n//2, n)]
        d = [matrix[i][n//2:] for i in range(n//2, n)]
        root = TreeNode('1')
        for p in [a, b, c, d]:
            root.children.append(build(n//2, p))
        return root

def get(root):
    result = ''
    queue = [root]
    while queue:
        node = queue.pop(0)
        result += node.val
        queue += node.children
    return result

for _ in range(int(input())):
    n = int(input())
    matrix = [list(map(int, input().split())) for _ in range(n)]
    ans = get(build(n, matrix))
    p = int(ans, 2)
    print(hex(p)[2:].upper())
