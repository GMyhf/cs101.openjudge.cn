# External reference: statistics page /practice/28013/
# Accepted submission: 52734750
# Source: http://cs101.openjudge.cn/practice/solution/52734750/
# License: not declared on the submission page; no license is inferred.

n = int(input())
tree = list(map(int, input().split()))
paths = []

# 1. DFS遍历：先右 后左，收集所有根到叶子的路径
def dfs(idx, path):
    path.append(tree[idx])
    # 判断是否是叶子节点
    left = 2 * idx + 1
    right = 2 * idx + 2
    if left >= n and right >= n:
        paths.append(path.copy())
        path.pop()
        return
    # 关键：先右 后左
    if right < n:
        dfs(right, path)
    if left < n:
        dfs(left, path)
    path.pop()

dfs(0, [])

# 2. 输出所有路径
for p in paths:
    print(' '.join(map(str, p)))

# 3. 判断大顶堆 / 小顶堆
is_max = True
is_min = True

for i in range(n):
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n:
        if tree[i] < tree[left]:
            is_max = False
        if tree[i] > tree[left]:
            is_min = False
    if right < n:
        if tree[i] < tree[right]:
            is_max = False
        if tree[i] > tree[right]:
            is_min = False

if is_max:
    print("Max Heap")
elif is_min:
    print("Min Heap")
else:
    print("Not Heap")