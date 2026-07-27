# External reference: /practice/29656/statistics/
# Accepted submission: 52686108
# Source: http://cs101.openjudge.cn/practice/solution/52686108/
# License: not declared on the submission page; no license is inferred.

n = int(input())
left = [0] * (n + 1)
right = [0] * (n + 1)
parent = [0] * (n + 1)

for i in range(1, n + 1):
    l, r = map(int, input().split())
    left[i] = l
    right[i] = r
    if l:
        parent[l] = i
    if r:
        parent[r] = i

# 后序遍历计算 left_len 和 right_len（一直向左/右的节点数，包括自身）
left_len = [1] * (n + 1)
right_len = [1] * (n + 1)
stack = [(1, 0)]  # (node, state) 0=未处理子节点, 1=子节点已处理
order = []
while stack:
    u, state = stack.pop()
    if state == 0:
        stack.append((u, 1))
        if right[u]:
            stack.append((right[u], 0))
        if left[u]:
            stack.append((left[u], 0))
    else:
        order.append(u)

for u in order:
    if left[u]:
        left_len[u] = 1 + left_len[left[u]]
    if right[u]:
        right_len[u] = 1 + right_len[right[u]]

# 计算 up_len（向上直线可达节点数，包括自身）
up_len = [1] * (n + 1)  # 根节点 up_len[1]=1
for v in range(2, n + 1):
    p = parent[v]
    # 判断是否与父节点的方向一致，且父节点也满足相同方向（或父节点为根）
    if (left[p] == v and (p == 1 or (parent[p] and left[parent[p]] == p))) or \
       (right[p] == v and (p == 1 or (parent[p] and right[parent[p]] == p))):
        up_len[v] = up_len[p] + 1
    else:
        up_len[v] = 2   # 只能到自身和父节点

best_cnt = -1
best_node = -1
for v in range(1, n + 1):
    cnt = left_len[v] + right_len[v] + up_len[v] - 2   # 减去重复的自身（被加了3次，应只算1次）
    if cnt > best_cnt or (cnt == best_cnt and v < best_node):
        best_cnt = cnt
        best_node = v

print(best_node, best_cnt)