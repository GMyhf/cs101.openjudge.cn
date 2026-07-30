# External reference: http://cs101.openjudge.cn/practice/27862/statistics/
# Accepted submission: 44323135
# Source: http://cs101.openjudge.cn/practice/solution/44323135/
# License: not declared on the submission page; no license is inferred.

class TreeNode:
    def __init__(self):
        self.d = 0
        self.w = 0
        self.child = []

def dfs(root, now):
    if root.child:
        tmp = []
        for node in root.child:
            tmp.append(dfs(node, (now+1) % 2))
        if now:
            tmp.sort(key=lambda x: (x[1], x[0]), reverse=True)
            return tmp[0]
        else:
            tmp.sort(key=lambda x: (x[0], x[1]), reverse=True)
            return tmp[0]
    else:
        return [root.d, root.w]

n = int(input())
tree = [TreeNode() for _ in range(n+1)]
for _ in range(n-1):
    a, b = map(int, input().split())
    tree[a].child.append(tree[b])
for _ in range(int(input())):
    l, a, b = map(int, input().split())
    tree[l].d = a
    tree[l].w = b
root = tree[1]
ans = dfs(root, 0)
print(*ans)
