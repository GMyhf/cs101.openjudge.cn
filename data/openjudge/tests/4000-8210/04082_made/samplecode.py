# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
from collections import defaultdict

n = int(input())
if n == 0:
    print()
    exit()

preorder = input().split()

# 初始化根节点
root = preorder[0][0]
root_type = preorder[0][1]

tier = defaultdict(list)
tier[0].append(root)

nodes = [root]
level = 0
types = {root: root_type}

for i in range(1, n):
    current = preorder[i]
    name = current[0]
    typ = current[1]
    types[name] = typ

    prev_node = nodes[-1]
    prev_type = types[prev_node]

    # 计算层级变化
    if prev_type == '1':
        level -= 1
    else:
        level += 1

    nodes.append(name)

    # 只添加非虚节点到对应层级
    if name != '$':
        tier[level].append(name)

# 按层级顺序排序并逆序每层节点
sorted_levels = sorted(tier.items(), key=lambda x: x[0])
result = []
for level, chars in sorted_levels:
    result.extend(reversed(chars))

print(' '.join(result))
